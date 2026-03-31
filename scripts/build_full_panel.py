"""
build_full_panel.py
-------------------
Собирает полную панель region × year (2009-2024) со всеми кодами ВИЧ-обследований,
данными Медиазоны, депозитами ЦБ и census population.

Входные файлы:
  hiv_codes_2009_2017.csv  — 12 кодов, бюллетени 34-43
  hiv_codes_2018_2021.csv  — 12→15 кодов, бюллетени 44-47
  hiv_codes_2022_2024.csv  — 22 кода, бюллетени 48-50
  mediazona_200_by_region_year.csv — потери по регионам 2022-2025
  census2021_nMen16-615.csv — мужчины трудоспособного возраста
  deposit_yoy_annual.csv — депозиты ЦБ

Выход: full_panel.csv
"""
import pandas as pd
import numpy as np
import os
import sys
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DATA_DIR)
from normalize_regions import normalize_region

# ── 1. Загрузить все 3 файла кодов ──────────────────────────────────────────
c1 = pd.read_csv(f'{DATA_DIR}/hiv_codes_2009_2017.csv')
c2 = pd.read_csv(f'{DATA_DIR}/hiv_codes_2018_2021.csv')
c3 = pd.read_csv(f'{DATA_DIR}/hiv_codes_2022_2024.csv')

codes = pd.concat([c1, c2, c3], ignore_index=True)
print(f"Кодов загружено: {len(codes)} строк, годы {sorted(codes.year.unique())}")

# ── 2. Нормализовать имена регионов ─────────────────────────────────────────
codes['region_raw'] = codes['region']
codes['region'] = codes['region'].apply(normalize_region)

# Удалить None (агрегатные строки типа "Тюменская область включая АО")
codes = codes[codes['region'].notna()].copy()

# Удалить РФ и ФО — оставить только регионы
codes = codes[~codes['is_russia'] & ~codes['is_fo']].copy()

# Удалить упразднённые автономные округа (только в 2009)
DEFUNCT_AO = {
    'Агинский Бурятский авт.округ', 'Агинский Бурятский автономный округ',
    'Таймырский авт.округ', 'Таймырский автономный округ',
    'Таймырский (Долгано-Ненецкий) авт.округ',
    'Эвенкийский авт.округ', 'Эвенкийский автономный округ',
}
before = len(codes)
codes = codes[~codes['region'].isin(DEFUNCT_AO)].copy()
# Also catch by raw name
codes = codes[~codes['region_raw'].isin(DEFUNCT_AO)].copy()
print(f"Удалено упразднённых АО: {before - len(codes)} строк")

# Проверить уникальные регионы
all_regions = codes['region'].unique()
print(f"Уникальных регионов: {len(all_regions)}")

# ── 3. Определить 85 канонических регионов ──────────────────────────────────
# Берём набор регионов из 2024 (самый свежий, 85 субъектов)
regions_2024 = set(codes[codes.year == 2024]['region'].unique())
print(f"Регионов в 2024: {len(regions_2024)}")

# Проверим что ранние годы покрывают те же регионы (минус Крым/Севастополь до 2014)
for yr in [2009, 2014, 2018, 2022, 2024]:
    yr_regs = set(codes[codes.year == yr]['region'].unique())
    diff_missing = regions_2024 - yr_regs
    diff_extra = yr_regs - regions_2024
    print(f"  {yr}: {len(yr_regs)} регионов, "
          f"отсутствуют={diff_missing if diff_missing else 'нет'}, "
          f"лишние={diff_extra if diff_extra else 'нет'}")

# ── 4. Pivot кодов в wide формат ────────────────────────────────────────────
# Для каждого кода: c{code}_tested, c{code}_hiv_pos, c{code}_rate
all_codes = sorted(codes['code'].unique())
print(f"\nВсе коды: {all_codes}")

pivot_dfs = []
for code in all_codes:
    sub = codes[codes.code == code][['region', 'year', 'tested', 'hiv_positive',
                                      'rate_per_100k_tested']].copy()
    prefix = f'c{code}'
    sub = sub.rename(columns={
        'tested': f'{prefix}_tested',
        'hiv_positive': f'{prefix}_hiv_pos',
        'rate_per_100k_tested': f'{prefix}_rate',
    })
    # Убрать дубли (на всякий случай)
    sub = sub.drop_duplicates(subset=['region', 'year'], keep='first')
    pivot_dfs.append((code, sub))

# Основа панели: все комбинации region × year
years = sorted(codes['year'].unique())
panel_base = pd.DataFrame(
    [(r, y) for r in sorted(regions_2024) for y in years],
    columns=['region', 'year']
)
print(f"\nОснова панели: {len(panel_base)} строк ({len(regions_2024)} регионов × {len(years)} лет)")

# Мержим все коды
panel = panel_base.copy()
for code, sub in pivot_dfs:
    prefix = f'c{code}'
    merge_cols = ['region', 'year', f'{prefix}_tested', f'{prefix}_hiv_pos', f'{prefix}_rate']
    panel = panel.merge(sub[merge_cols], on=['region', 'year'], how='left')

print(f"Панель после мержа кодов: {panel.shape}")

# ── 5. Добавить Медиазону (потери 2022-2025) ────────────────────────────────
mz = pd.read_csv(f'{DATA_DIR}/mediazona_200_by_region_year.csv')

MZ_EXCLUDE = {'Неизвестно', 'Иностранцы', 'Байконур',
              'Республика Крым', 'Севастополь', 'ДНР', 'ЛНР'}

MZ_TO_PANEL = {
    'Москва': 'г. Москва',
    'Санкт-Петербург': 'г. Санкт-Петербург',
    'Кабардино-Балкарская Республика': 'Кабардино\u2011Балкарская Республика',
    'Республика Карачаево-Черкесия': 'Карачаево\u2011Черкесская Республика',
    'Карачаево-Черкесская Республика': 'Карачаево\u2011Черкесская Республика',
    'Республика Северная Осетия-Алания': 'Республика Северная Осетия - Алания',
    'Ненецкий автономный округ': 'Ненецкий авт. округ',
    'Тюменская область': 'Тюменская область без АО',
    'Ханты-Мансийский автономный округ - Югра': 'Ханты-Мансийский авт.округ - Югра',
    'Чукотский автономный округ': 'Чукотский авт.округ',
    'Ямало-Ненецкий автономный округ': 'Ямало-Ненецкий авт.округ',
}

mz_clean = mz[~mz['region'].isin(MZ_EXCLUDE)].copy()
mz_clean['region'] = mz_clean['region'].map(lambda r: MZ_TO_PANEL.get(r, r))

# Melt → long
mz_long = mz_clean[['region', '2022', '2023', '2024', '2025']].melt(
    id_vars='region', var_name='year', value_name='deaths_annual'
)
mz_long['year'] = mz_long['year'].astype(int)
mz_long['deaths_annual'] = mz_long['deaths_annual'].fillna(0).astype(int)
mz_long = mz_long.sort_values(['region', 'year'])
mz_long['deaths_cum'] = mz_long.groupby('region')['deaths_annual'].cumsum()

# Merge into panel (pre-2022 = 0 deaths)
panel = panel.merge(mz_long[['region', 'year', 'deaths_annual', 'deaths_cum']],
                     on=['region', 'year'], how='left')
panel['deaths_annual'] = panel['deaths_annual'].fillna(0).astype(int)
panel['deaths_cum'] = panel['deaths_cum'].fillna(0).astype(int)

# ── 6. Добавить census (nMen16_615_2021) ────────────────────────────────────
census = pd.read_csv(f'{DATA_DIR}/census2021_nMen16-615.csv')

CENSUS_TO_PANEL = {
    'Москва': 'г. Москва',
    'Санкт-Петербург': 'г. Санкт-Петербург',
    'Севастополь': 'г. Севастополь',
    'Кабардино-Балкарская Республика': 'Кабардино\u2011Балкарская Республика',
    'Карачаево-Черкесская Республика': 'Карачаево\u2011Черкесская Республика',
    'Республика Карачаево-Черкесия': 'Карачаево\u2011Черкесская Республика',
    'Ненецкий автономный округ': 'Ненецкий авт. округ',
    'Тюменская область': 'Тюменская область без АО',
    'Ханты-Мансийский автономный округ - Югра': 'Ханты-Мансийский авт.округ - Югра',
    'Чукотский автономный округ': 'Чукотский авт.округ',
    'Ямало-Ненецкий автономный округ': 'Ямало-Ненецкий авт.округ',
    'Республика Северная Осетия-Алания': 'Республика Северная Осетия - Алания',
    'Республика Северная Осетия - Алания': 'Республика Северная Осетия - Алания',
}

census['panel_region'] = census['region'].map(lambda r: CENSUS_TO_PANEL.get(r, r))
pop_map = census.set_index('panel_region')['nMen16_615_2021'].to_dict()
iso_map = census.set_index('panel_region')['regNameISO'].to_dict()

panel['nMen16_615_2021'] = panel['region'].map(pop_map)
panel['regNameISO'] = panel['region'].map(iso_map)

missing_pop = panel[panel['nMen16_615_2021'].isna()]['region'].unique()
if len(missing_pop):
    print(f"WARNING: нет nMen для {len(missing_pop)} регионов: {sorted(missing_pop)}")
else:
    print("OK: nMen16_615_2021 проставлен для всех регионов")

# Per-capita rates
panel['deaths_annual_per100k'] = np.where(
    panel['nMen16_615_2021'] > 0,
    panel['deaths_annual'] / panel['nMen16_615_2021'] * 100_000, 0
)
panel['deaths_cum_per100k'] = np.where(
    panel['nMen16_615_2021'] > 0,
    panel['deaths_cum'] / panel['nMen16_615_2021'] * 100_000, 0
)

# ── 7. Добавить депозиты ────────────────────────────────────────────────────
deposits = pd.read_csv(f'{DATA_DIR}/deposit_yoy_annual.csv')
panel = panel.merge(deposits, on=['region', 'year'], how='left')

# ── 8. Вычисляемые переменные ───────────────────────────────────────────────
panel['post'] = (panel['year'] >= 2022).astype(int)
panel['hiv_available'] = panel['c100_hiv_pos'].notna()

# Log transforms
for col in ['c100_rate', 'c109_rate', 'c100_hiv_pos', 'c109_hiv_pos',
            'c111_hiv_pos', 'c112_rate', 'deaths_cum_per100k', 'deaths_annual_per100k']:
    panel[f'log_{col}'] = np.log1p(panel[col])

# ── 9. Сортировка и сохранение ──────────────────────────────────────────────
panel = panel.sort_values(['region', 'year']).reset_index(drop=True)

# ── 10. Диагностика ─────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"FULL PANEL SUMMARY")
print(f"{'='*60}")
print(f"Строк: {len(panel)}")
print(f"Регионов: {panel['region'].nunique()}")
print(f"Лет: {sorted(panel['year'].unique())}")
print(f"Колонок: {len(panel.columns)}")

# Code coverage
print(f"\nПокрытие кодов (% непустых region×year):")
for code in all_codes:
    col = f'c{code}_hiv_pos'
    if col in panel.columns:
        pct = panel[col].notna().mean() * 100
        years_with_data = sorted(panel[panel[col].notna()]['year'].unique())
        print(f"  c{code}: {pct:5.1f}% ({years_with_data[0]}-{years_with_data[-1]})")

# Mediazona check
print(f"\nСмерти Медиазона (суммарно по годам):")
for yr in [2022, 2023, 2024]:
    total = panel[panel.year == yr]['deaths_annual'].sum()
    print(f"  {yr}: {total:,}")

# Missing check
print(f"\nMissing values (key columns):")
for col in ['c100_hiv_pos', 'c109_hiv_pos', 'c112_hiv_pos', 'nMen16_615_2021',
            'deaths_annual', 'yoy_growth_mean']:
    n_miss = panel[col].isna().sum()
    print(f"  {col}: {n_miss} ({n_miss/len(panel)*100:.1f}%)")

# Sample
print(f"\nSample: Свердловская область")
sverd = panel[panel.region.str.contains('Свердлов')]
print(sverd[['year', 'c100_hiv_pos', 'c109_hiv_pos', 'c112_hiv_pos',
             'deaths_annual', 'yoy_growth_mean']].to_string(index=False))

# ── 11. Сохранить ───────────────────────────────────────────────────────────
panel.to_csv(f'{DATA_DIR}/full_panel.csv', index=False)
print(f"\nСохранено: full_panel.csv ({len(panel)} строк × {len(panel.columns)} колонок)")
print(f"Все колонки: {list(panel.columns)}")
