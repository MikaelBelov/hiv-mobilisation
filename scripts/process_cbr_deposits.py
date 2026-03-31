"""
Process CBR regional household deposit data (02_06_Dep_ind.xlsx)
and construct a Solanko (2024)-style YoY deposit growth variable
for merging with a region-year panel.

Input:  02_06_Dep_ind.xlsx — CBR regional banking statistics
        panel_v2.csv — existing region-year panel

Output: panel_with_deposits.csv — panel with deposit growth variables added
        deposit_yoy_monthly.csv — monthly deposit data (long format)
        deposit_yoy_annual.csv — annual aggregates by region

Source: Solanko, L. (2024). Where do Russia's mobilized soldiers come from?
        Evidence from bank deposits. BOFIT Policy Brief 1/2024.
        https://publications.bof.fi/handle/10024/53281
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
CBR_PATH = Path("02_06_Dep_ind.xlsx")
PANEL_PATH = Path("panel_v2.csv")
OUT_DIR = Path(".")
OUT_DIR.mkdir(exist_ok=True)


# ── 1. Read CBR data ──────────────────────────────────────────────────────
# Sheet "итого" = ruble + foreign currency deposits combined.
# Solanko uses total deposits (not ruble-only), confirmed by her Figure 3
# caption: "Change in household bank deposits across regions."
df_raw = pd.read_excel(CBR_PATH, sheet_name="итого", header=None)

# Row 0 = title, Row 1 = dates, Rows 2+ = region data.
# Column 0 = region names, Columns 1+ = monthly values.
# There is one NaN column (col 11 in the ruble sheet) that splits dates —
# dropna on row 1 handles this automatically.
dates_row = df_raw.iloc[1, 1:].dropna()
date_cols = dates_row.index.tolist()
dates = pd.to_datetime(dates_row.values, format="%d.%m.%Y")

# ── 2. Identify region rows ───────────────────────────────────────────────
# Skip: federal district aggregates, RF total, footnotes, "за пределами РФ"
SKIP_PATTERNS = [
    "ФЕДЕРАЛЬНЫЙ ОКРУГ",
    "ФЕДЕРАЦИЯ",
    "Начиная с",
    "ЗА ПРЕДЕЛАМИ",
]

region_rows = []
for idx in range(2, len(df_raw)):
    name = str(df_raw.iloc[idx, 0]).strip()
    if pd.isna(df_raw.iloc[idx, 0]):
        continue
    if any(p in name for p in SKIP_PATTERNS):
        continue
    # Skip rows with no numeric data
    if pd.isna(df_raw.iloc[idx, date_cols[0]]):
        continue
    region_rows.append((idx, name))

print(f"CBR rows extracted: {len(region_rows)}")

# ── 3. Reshape to long format ─────────────────────────────────────────────
records = []
for row_idx, region_name in region_rows:
    for i, col_idx in enumerate(date_cols):
        val = df_raw.iloc[row_idx, col_idx]
        if pd.notna(val) and val not in ("-", "–"):
            try:
                records.append({
                    "region_cbr": region_name,
                    "date": dates[i],
                    "deposits_mln_rub": float(val),
                })
            except (ValueError, TypeError):
                pass

df = pd.DataFrame(records)
df = df.sort_values(["region_cbr", "date"]).reset_index(drop=True)
print(f"Long dataframe: {df.shape[0]} rows, {df['region_cbr'].nunique()} CBR regions")

# ── 4. Handle matryoshka regions ──────────────────────────────────────────
# CBR reports matryoshka oblasts two ways:
#   (a) Full oblast (e.g. "Тюменская область") = oblast + all AOs inside it
#   (b) "без данных" row = oblast minus AOs
#   (c) "в том числе" rows = individual AOs
#
# Panel uses (b) + (c), i.e. oblast-without-AO as one region and each AO
# as a separate region. So we DROP the full-oblast rows (a) and KEEP (b)+(c).
#
# Affected matryoshkas:
#   Тюменская область = ХМАО + ЯНАО + остаток
#   Архангельская область = НАО + остаток

DROP_FULL_MATRYOSHKA = [
    "Архангельская область",   # full, includes НАО
    "Тюменская область",       # full, includes ХМАО + ЯНАО
]

df = df[~df["region_cbr"].isin(DROP_FULL_MATRYOSHKA)].copy()

# ── 5. Map CBR names → panel names ────────────────────────────────────────
# Panel uses slightly different naming conventions:
#   - non-breaking hyphens (U+2011) in КБР, КЧР
#   - abbreviated "авт. округ" / "авт.округ"
#   - no suffixes like "(Адыгея)", "(Татарстан)", "- Кузбасс", "- Чувашия"
#   - "Тюменская область без АО" for the remainder

NAME_MAP = {
    # Matryoshka remainder rows
    "Архангельская область без данных по Ненецкому автономному округу":
        "Архангельская область",
    "Тюменская область без данных по Ханты-Мансийскому автономному округу"
    " - Югре и Ямало-Ненецкому автономному округу":
        "Тюменская область без АО",
    # Autonomous okrugs ("в том числе" → standalone)
    "в том числе Ненецкий автономный округ":
        "Ненецкий авт. округ",
    "в том числе Ханты-Мансийский автономный округ - Югра":
        "Ханты-Мансийский авт.округ - Югра",
    "в том числе Ямало-Ненецкий автономный округ":
        "Ямало-Ненецкий авт.округ",
    # Suffix removal
    "Республика Адыгея (Адыгея)":
        "Республика Адыгея",
    "Республика Татарстан (Татарстан)":
        "Республика Татарстан",
    "Кемеровская область - Кузбасс":
        "Кемеровская область",
    "Чувашская Республика - Чувашия":
        "Чувашская Республика",
    # Non-breaking hyphens (U+2011) in panel
    "Кабардино-Балкарская Республика":
        "Кабардино\u2011Балкарская Республика",
    "Карачаево-Черкесская Республика":
        "Карачаево\u2011Черкесская Республика",
    # Abbreviation differences
    "Чукотский автономный округ":
        "Чукотский авт.округ",
}

df["region"] = df["region_cbr"].map(NAME_MAP).fillna(df["region_cbr"])

# Drop regions not in the panel (Крым, Севастополь — no HIV data)
DROP_REGIONS = ["Республика Крым", "г. Севастополь"]
df = df[~df["region"].isin(DROP_REGIONS)].copy()

# ── 6. Compute YoY deposit growth ─────────────────────────────────────────
# Solanko's main variable: 12-month (year-on-year) growth in household
# bank deposits. Monthly frequency, not seasonally adjusted.
df = df.sort_values(["region", "date"]).reset_index(drop=True)
df["deposits_lag12"] = df.groupby("region")["deposits_mln_rub"].shift(12)
df["yoy_growth"] = (
    (df["deposits_mln_rub"] - df["deposits_lag12"]) / df["deposits_lag12"]
)

# ── 7. Verify against Solanko Table 1 ─────────────────────────────────────
print("\n── Verification vs Solanko Table 1 (August 2023) ──")
SOLANKO_TABLE1 = {
    "Республика Тыва": 0.53,
    "Республика Бурятия": 0.33,
    "Забайкальский край": 0.28,
    "Республика Дагестан": 0.27,
    "Республика Калмыкия": 0.28,
    "Чеченская Республика": 0.30,
    "Республика Адыгея": 0.32,
    "Республика Алтай": 0.36,
    "Ненецкий авт. округ": 0.40,
    "Республика Северная Осетия - Алания": 0.28,
    "Краснодарский край": 0.27,
    "Ростовская область": 0.21,
    "Ханты-Мансийский авт.округ - Югра": 0.30,
    "Ямало-Ненецкий авт.округ": 0.26,
    "Карачаево\u2011Черкесская Республика": 0.24,
}

aug23 = df[df["date"] == "2023-08-01"].set_index("region")
for region, expected in SOLANKO_TABLE1.items():
    if region in aug23.index:
        actual = aug23.loc[region, "yoy_growth"]
        diff = abs(actual - expected)
        flag = "✓" if diff < 0.03 else ("~" if diff < 0.06 else "✗")
        print(f"  {flag} {actual:6.1%} (Solanko: {expected:.0%})  {region}")
    else:
        print(f"  ? NOT FOUND: {region}")

# ── 8. Aggregate to annual ────────────────────────────────────────────────
df["year"] = df["date"].dt.year

annual = (
    df.groupby(["region", "year"])
    .agg(
        yoy_growth_mean=("yoy_growth", "mean"),
        deposits_avg=("deposits_mln_rub", "mean"),
    )
    .reset_index()
)

# ── 9. Validate panel merge (optional — skipped if panel_v2.csv absent) ──
if PANEL_PATH.exists():
    panel = pd.read_csv(PANEL_PATH)
    panel_regions = set(panel["region"].unique())
    dep_regions = set(df["region"].unique())

    matched = panel_regions & dep_regions
    unmatched_panel = panel_regions - dep_regions

    print(f"\n── Panel merge validation ──")
    print(f"Panel regions:   {len(panel_regions)}")
    print(f"Deposit regions: {len(dep_regions)}")
    print(f"Matched:         {len(matched)}")

    if unmatched_panel:
        print(f"In panel but NOT in deposits ({len(unmatched_panel)}):")
        for r in sorted(unmatched_panel):
            print(f"  {repr(r)}")

    # Merge and save
    merged = panel.merge(annual, on=["region", "year"], how="left")
    merged.to_csv(OUT_DIR / "panel_with_deposits.csv", index=False)
    print(f"  panel_with_deposits.csv : {merged.shape}")
else:
    print(f"\n── Skipping panel merge ({PANEL_PATH} not found) ──")

# ── 10. Save deposit outputs (always) ───────────────────────────────────
out_monthly = df[["region", "date", "deposits_mln_rub", "yoy_growth"]].copy()
out_monthly["date"] = out_monthly["date"].dt.strftime("%Y-%m-%d")
out_monthly.to_csv(OUT_DIR / "deposit_yoy_monthly.csv", index=False)

annual.to_csv(OUT_DIR / "deposit_yoy_annual.csv", index=False)

print(f"\n── Outputs saved to {OUT_DIR}/ ──")
print(f"  deposit_yoy_monthly.csv : {len(out_monthly):,} rows × {out_monthly['region'].nunique()} regions")
print(f"  deposit_yoy_annual.csv  : {len(annual):,} rows")
