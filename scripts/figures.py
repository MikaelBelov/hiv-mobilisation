"""
War and HIV Transmission in Russian Regions — Publication Figures

Generates 5 figures (PNG + PDF):
  Fig 1: Scatter — deposit growth vs HIV rate change
  Fig 2: Event study — flat pre, post jump
  Fig 3: Three phases — all 76 regions, spaghetti + highlights
  Fig 4: Forest plot — 10/10 treatment window × post-period matrix
  Fig 5: Mechanism — effect by testing category

Input: full_panel.csv, deposit_yoy_monthly.csv, analysis_output.txt (for event study coefficients)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as sp_stats
import warnings
import os
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════

plt.rcParams.update({
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 12,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.grid': True, 'grid.alpha': 0.25, 'grid.linestyle': '--',
    'font.family': 'sans-serif',
})

RED = '#c0392b'; BLUE = '#2980b9'; DARK = '#2c3e50'; GRAY = '#95a5a6'
GREEN = '#27ae60'; ORANGE = '#e67e22'; YELLOW = '#f1c40f'

OUT = DATA_DIR + '/'

df = pd.read_csv(f'{DATA_DIR}/full_panel.csv')
df = df[(df['year'] >= 2013) & (df['year'] <= 2024)].copy()
dep_m = pd.read_csv(f'{OUT}/deposit_yoy_monthly.csv')
dep_m['date'] = pd.to_datetime(dep_m['date'])

OIL = {'Ханты-Мансийский авт.округ - Югра', 'Ямало-Ненецкий авт.округ',
       'Ненецкий авт. округ', 'Республика Коми', 'Сахалинская область'}
CAP = {'г. Москва', 'г. Санкт-Петербург'}
df_pref = df[~df['region'].isin(OIL | CAP)].copy()
pref_regions = set(df_pref['region'].unique())

dose = dep_m[(dep_m['date'] >= '2022-10-01') & (dep_m['date'] <= '2023-06-01')] \
    .groupby('region')['yoy_growth'].mean()
dose = dose[dose.index.isin(pref_regions)]


# ══════════════════════════════════════════════════════════════
# SUPPLEMENTARY FIGURE: SCATTER — deposit growth vs HIV rate change
# (moved to supplement; Pearson r driven by Chechnya outlier)
# ══════════════════════════════════════════════════════════════

pre = df_pref[df_pref['year'].isin([2019, 2020, 2021])].groupby('region').apply(
    lambda g: g['c109_hiv_pos'].sum() / g['c109_tested'].sum() * 100000)
post = df_pref[df_pref['year'].isin([2023, 2024])].groupby('region').apply(
    lambda g: g['c109_hiv_pos'].sum() / g['c109_tested'].sum() * 100000)
change_pct = ((post - pre) / pre * 100)

m = pd.DataFrame({'dep': dose, 'change': change_pct}).dropna()
m = m[np.isfinite(m['change'])]

fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(m['dep'] * 100, m['change'], color=DARK, alpha=0.45, s=45,
           edgecolors='white', linewidths=0.5)

z = np.polyfit(m['dep'] * 100, m['change'], 1)
x_fit = np.linspace(m['dep'].min() * 100 - 1, m['dep'].max() * 100 + 1, 100)
ax.plot(x_fit, z[0] * x_fit + z[1], color=RED, linewidth=2.5)

labels = {
    'Республика Тыва': ('Tuva', 8, -12),
    'Республика Бурятия': ('Buryatia', 8, 8),
    'Чеченская Республика': ('Chechnya', -60, -12),
    'Белгородская область': ('Belgorod', 8, 8),
    'Свердловская область': ('Sverdlovsk', 8, -12),
    'Республика Дагестан': ('Dagestan', 8, 8),
    'Республика Марий Эл': ('Mari El', 8, -12),
}
for region, (eng, dx, dy) in labels.items():
    if region in m.index:
        x = m.loc[region, 'dep'] * 100
        y = m.loc[region, 'change']
        color_l = RED if x > 15 else DARK
        ax.annotate(eng, (x, y), fontsize=9, color=color_l,
                    fontweight='bold' if x > 15 else 'normal',
                    xytext=(dx, dy), textcoords='offset points',
                    arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.5)
                    if abs(dx) > 15 else None)

ax.axhline(y=0, color=DARK, linestyle='-', linewidth=0.8, alpha=0.4)

r, p = sp_stats.pearsonr(m['dep'], m['change'])
ax.text(0.05, 0.95, f'Pearson r = {r:.2f},  p = {p:.3f}\nN = {len(m)} regions',
        transform=ax.transAxes, fontsize=11, va='top',
        bbox=dict(facecolor='white', edgecolor=DARK, alpha=0.85,
                  boxstyle='round,pad=0.4'))

ax.set_xlabel('Deposit Growth, Oct 2022 – Jun 2023 (%)', fontsize=12)
ax.set_ylabel('Change in HIV Detection Rate Among Pregnant Women (%)\n'
              '2023–24 mean vs. 2019–21 mean', fontsize=11)
ax.set_title('Supplementary Figure: Regional Military Burden and HIV Rate Change', fontsize=14)

plt.tight_layout()
plt.savefig(f'{OUT}/figS1_scatter.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{OUT}/figS1_scatter.pdf', bbox_inches='tight')
plt.close()
print("Supplementary Figure S1 done")


# ══════════════════════════════════════════════════════════════
# FIGURE 1: EVENT STUDY
# ══════════════════════════════════════════════════════════════

# Base year = 2019 (pre-COVID; Miller 2023, JEP)
es_years = [2013, 2014, 2015, 2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024]
es_betas = [-0.1132, -0.0208, -0.0132, -0.0013, 0.0041, 0.0005,
             0.0015, -0.1549,
             0.1185, 0.0707, 0.2055]
es_ses = [0.1182, 0.0828, 0.0725, 0.0516, 0.0447, 0.0428,
          0.0413, 0.2866,
          0.0617, 0.0840, 0.0800]
es_irrs = [np.exp(b) for b in es_betas]
es_ci_lo = [np.exp(b - 1.96 * s) for b, s in zip(es_betas, es_ses)]
es_ci_hi = [np.exp(b + 1.96 * s) for b, s in zip(es_betas, es_ses)]

fig, ax = plt.subplots(figsize=(10, 6))

for i, y in enumerate(es_years):
    if y >= 2022:
        c = RED
    elif y == 2021:
        c = ORANGE
    else:
        c = DARK
    ax.plot([y, y], [es_ci_lo[i], es_ci_hi[i]], color=c, linewidth=2,
            alpha=0.45, solid_capstyle='round')

pre_x = [y for y in es_years if y < 2022 and y != 2021]
pre_irr = [es_irrs[i] for i, y in enumerate(es_years) if y < 2022 and y != 2021]
post_x = [y for y in es_years if y >= 2022]
post_irr = [es_irrs[i] for i, y in enumerate(es_years) if y >= 2022]
covid_x = [y for y in es_years if y == 2021]
covid_irr = [es_irrs[i] for i, y in enumerate(es_years) if y == 2021]

ax.scatter(pre_x, pre_irr, color=DARK, s=60, zorder=5, label='Pre-war')
ax.scatter(post_x, post_irr, color=RED, s=80, zorder=5, marker='D', label='Post-war')
ax.scatter(covid_x, covid_irr, color=ORANGE, s=70, zorder=5, marker='v', label='2021 (COVID disruption)')
ax.scatter([2019], [1.0], color=GRAY, s=90, zorder=5, marker='s',
           label='Base year (2019)')

ax.axhline(y=1.0, color=GRAY, linestyle='--', linewidth=0.8, alpha=0.5)
ax.axvspan(2021.5, 2024.5, alpha=0.05, color=RED)

pre_mean = np.mean(pre_irr)
ax.axhline(y=pre_mean, color=DARK, linestyle=':', linewidth=1, alpha=0.3)
ax.text(2012.7, pre_mean, f'pre-mean\n{pre_mean:.2f}', fontsize=8,
        color=DARK, alpha=0.5, va='center')

ax.annotate('Joint pre-trends test:\nχ²(8) = 11.79, p = 0.161',
            xy=(2015.5, 0.65), fontsize=9, color=DARK,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=DARK, alpha=0.8))

ax.annotate(f'IRR = {es_irrs[-1]:.2f}', xy=(2024, es_irrs[-1]),
            xytext=(2023.2, es_irrs[-1] + 0.20), fontsize=9, color=RED,
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

ax.annotate('COVID\ndisruption', xy=(2021, covid_irr[0]),
            xytext=(2020.2, covid_irr[0] - 0.18), fontsize=8, color=ORANGE,
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1))

ax.set_xlabel('Year')
ax.set_ylabel('Incidence Rate Ratio (IRR)')
ax.set_title('Figure 1: Event Study — HIV Among Pregnant Women (Code 109)')
ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
ax.set_xticks(range(2013, 2025))
ax.set_xticklabels([str(y) if y != 2019 else '2019\n(base)'
                     for y in range(2013, 2025)], fontsize=9)
ax.set_xlim(2012.3, 2024.7)

plt.tight_layout()
plt.savefig(f'{OUT}/fig1_event_study.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{OUT}/fig1_event_study.pdf', bbox_inches='tight')
plt.close()
print("Figure 1 done")


# ══════════════════════════════════════════════════════════════
# FIGURE 2: THREE PHASES — all regions spaghetti + highlights
# ══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 7))

dep_pref = dep_m[dep_m['region'].isin(pref_regions)]
dep_pref = dep_pref[(dep_pref['date'] >= '2021-06-01') &
                     (dep_pref['date'] <= '2024-06-01')]

for region in pref_regions:
    rd = dep_pref[dep_pref['region'] == region].sort_values('date')
    if len(rd) > 3:
        ax.plot(rd['date'], rd['yoy_growth'] * 100, '-', color=GRAY,
                linewidth=0.4, alpha=0.3)

highlights = [
    ('Республика Тыва', 'Tuva', RED, 2.8),
    ('Республика Бурятия', 'Buryatia', ORANGE, 2.5),
    ('Чеченская Республика', 'Chechnya', '#e74c3c', 2.2),
    ('Свердловская область', 'Sverdlovsk', BLUE, 2.5),
    ('Нижегородская область', 'N. Novgorod', '#3498db', 2.0),
]

for region, eng, color, lw in highlights:
    rd = dep_pref[dep_pref['region'] == region].sort_values('date')
    if len(rd) > 3:
        ax.plot(rd['date'], rd['yoy_growth'] * 100, '-', color=color,
                linewidth=lw, label=eng, alpha=0.9, zorder=5)

ax.axvspan(pd.Timestamp('2022-02-24'), pd.Timestamp('2022-09-20'),
           alpha=0.06, color=BLUE)
ax.axvspan(pd.Timestamp('2022-09-21'), pd.Timestamp('2022-12-31'),
           alpha=0.06, color=ORANGE)
ax.axvspan(pd.Timestamp('2023-01-01'), pd.Timestamp('2024-06-01'),
           alpha=0.06, color=RED)

ax.text(pd.Timestamp('2022-05-20'), 93, 'Phase 1\nProfessional\nsoldiers',
        fontsize=8, color=BLUE, ha='center', style='italic')
ax.text(pd.Timestamp('2022-11-10'), 93, 'Phase 2\nMobilization',
        fontsize=8, color=ORANGE, ha='center', style='italic')
ax.text(pd.Timestamp('2023-09-01'), 93, 'Phase 3\nMass contract\nrecruitment',
        fontsize=8, color=RED, ha='center', style='italic')

ax.axvline(pd.Timestamp('2022-02-24'), color=DARK, linestyle=':', linewidth=1, alpha=0.4)
ax.axvline(pd.Timestamp('2022-09-21'), color=DARK, linestyle=':', linewidth=1, alpha=0.4)

ax.set_xlabel('Date')
ax.set_ylabel('Year-on-Year Deposit Growth (%)')
ax.set_title('Figure 2: Monthly Deposit Growth — All 76 Regions, '
             'Three Phases of War')
ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax.set_ylim(-20, 105)
ax.text(0.98, 0.15, '76 regions\n(gray lines)', transform=ax.transAxes,
        fontsize=9, ha='right', color=GRAY, style='italic')

plt.tight_layout()
plt.savefig(f'{OUT}/fig2_three_phases.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{OUT}/fig2_three_phases.pdf', bbox_inches='tight')
plt.close()
print("Figure 2 done")


# ══════════════════════════════════════════════════════════════
# FIGURE 3: FOREST PLOT — 10/10 matrix
# ══════════════════════════════════════════════════════════════

specs = [
    ('Jan–Jun 2023  ×  2022–2024', 0.1761, 0.0644),
    ('Jan–Jun 2023  ×  2023–2024', 0.1748, 0.0649),
    ('Oct 22–Jun 23  ×  2022–2024  ★', 0.1598, 0.0637),
    ('Oct 22–Jun 23  ×  2023–2024', 0.1564, 0.0663),
    ('Mar 22–Jun 23  ×  2022–2024', 0.1440, 0.0633),
    ('Mar 22–Jun 23  ×  2023–2024', 0.1419, 0.0691),
    ('Oct–Dec 2022  ×  2022–2024', 0.0962, 0.0712),
    ('Oct–Dec 2022  ×  2023–2024', 0.0868, 0.0834),
    ('Mar–Sep 2022  ×  2022–2024', 0.0789, 0.0680),
    ('Mar–Sep 2022  ×  2023–2024', 0.0780, 0.0790),
]

fig, ax = plt.subplots(figsize=(10, 7))

for i, (label, beta, se) in enumerate(reversed(specs)):
    irr = np.exp(beta)
    ci_lo = np.exp(beta - 1.96 * se)
    ci_hi = np.exp(beta + 1.96 * se)

    sig = ci_lo > 1.0
    color = RED if sig else DARK
    alpha = 1.0 if sig else 0.5

    ax.plot([ci_lo, ci_hi], [i, i], color=color, linewidth=2.5,
            alpha=alpha * 0.55, solid_capstyle='round')
    ax.scatter([irr], [i], color=color, s=55 if sig else 35,
              zorder=5, alpha=alpha)

    p = 2 * (1 - sp_stats.norm.cdf(abs(beta / se)))
    stars = '***' if p < .01 else '**' if p < .05 else '*' if p < .1 else ''
    ax.text(ci_hi + 0.012, i, f'{irr:.3f} {stars}', fontsize=9,
            va='center', color=color, alpha=alpha)

ax.set_yticks(range(len(specs)))
ax.set_yticklabels([s[0] for s in reversed(specs)], fontsize=10)
ax.axvline(x=1.0, color=DARK, linestyle='--', linewidth=1, alpha=0.5)

n_sig = sum(1 for _, b, s in specs if np.exp(b - 1.96 * s) > 1.0)
ax.text(0.03, 0.97,
        f'{n_sig}/10 significant at 5%\n'
        f'10/10 positive direction\n'
        f'All: 76 regions\n'
        f'(excl. oil&gas + capitals)\n'
        f'★ preferred spec',
        transform=ax.transAxes, fontsize=9, va='top', ha='left',
        bbox=dict(facecolor='white', edgecolor=DARK, alpha=0.85,
                  boxstyle='round,pad=0.5'))

ax.set_xlabel('Incidence Rate Ratio (IRR)', fontsize=12)
ax.set_title('Figure 3: Treatment Window × Post-Period Matrix\n'
             '5 Windows × 2 Post Definitions, Preferred Sample', fontsize=13)
ax.set_xlim(0.82, 1.42)

plt.tight_layout()
plt.savefig(f'{OUT}/fig3_forest_plot.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{OUT}/fig3_forest_plot.pdf', bbox_inches='tight')
plt.close()
print("Figure 3 done")


# ══════════════════════════════════════════════════════════════
# FIGURE 4: MECHANISM — effect by testing category
# ══════════════════════════════════════════════════════════════

outcomes = [
    ('Health workers (115)\nPLACEBO', 0.0031, 0.2269, GREEN, 'p = 0.989'),
    ('IDU / Drug users (102)\nNot injection channel', -0.0839, 0.1045, BLUE, 'p = 0.422'),
    ('All citizens (100)', 0.0105, 0.0742, GRAY, 'p = 0.888'),
    ('STI patients (104)', 0.0535, 0.1658, GRAY, 'p = 0.747'),
    ('Donors (108)\nAmbiguous', 0.1534, 0.0502, ORANGE, 'p = 0.002'),
    ('Prisoners (112)', 0.2145, 0.1129, ORANGE, 'p = 0.058'),
    ('Pregnant women (109)\nMAIN RESULT', 0.1598, 0.0637, RED, 'p = 0.012'),
]

fig, ax = plt.subplots(figsize=(10, 6.5))

for i, (label, beta, se, color, p_text) in enumerate(outcomes):
    irr = np.exp(beta)
    ci_lo = np.exp(beta - 1.96 * se)
    ci_hi = np.exp(beta + 1.96 * se)

    lw = 3 if color == RED else 2.5
    ms = 90 if color == RED else 60

    ax.plot([ci_lo, ci_hi], [i, i], color=color, linewidth=lw, alpha=0.5)
    ax.scatter([irr], [i], color=color, s=ms, zorder=5)
    ax.text(max(ci_hi, 1.55) + 0.03, i, p_text, fontsize=9,
            va='center', color=color)

ax.axvline(x=1.0, color=DARK, linestyle='--', linewidth=1, alpha=0.5)
ax.set_yticks(range(len(outcomes)))
ax.set_yticklabels([o[0] for o in outcomes], fontsize=10)
ax.set_xlabel('Incidence Rate Ratio (IRR)', fontsize=12)
ax.set_title('Figure 4: Effect by Testing Category — Mechanism\n'
             'Preferred Treatment, Preferred Sample', fontsize=13)
ax.set_xlim(0.35, 1.95)

ax.text(0.03, 0.97,
        'Sexual transmission:\n'
        '• Pregnant ↑ (main)\n'
        '• IDU null → not\n'
        '  injection channel\n'
        '• Health workers\n'
        '  null → not general\n'
        '  regional shock',
        transform=ax.transAxes, fontsize=9, va='top', ha='left',
        bbox=dict(facecolor='white', edgecolor=DARK, alpha=0.9,
                  boxstyle='round,pad=0.5'))

plt.tight_layout()
plt.savefig(f'{OUT}/fig4_mechanism.png', dpi=200, bbox_inches='tight')
plt.savefig(f'{OUT}/fig4_mechanism.pdf', bbox_inches='tight')
plt.close()
print("Figure 4 done")

print(f"\nAll 4 main figures + 1 supplementary saved to {OUT}/ (PNG + PDF).")
