"""
War and HIV Transmission in Russian Regions: A Difference-in-Differences Analysis

Reproduces all results. Input: full_panel.csv, deposit_yoy_monthly.csv
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from scipy import stats as sp_stats
from scipy.stats import chi2
import warnings, io
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════
# 0. LOAD & PREPARE
# ══════════════════════════════════════════════════════════════

import os
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

df_raw = pd.read_csv(f'{DATA_DIR}/full_panel.csv')
df = df_raw[(df_raw['year'] >= 2013) & (df_raw['year'] <= 2024)].copy()

dep_monthly = pd.read_csv(f'{DATA_DIR}/deposit_yoy_monthly.csv')
dep_monthly['date'] = pd.to_datetime(dep_monthly['date'])

def window_dose(start, end):
    d = dep_monthly[(dep_monthly['date'] >= start) & (dep_monthly['date'] <= end)]
    return d.groupby('region')['yoy_growth'].mean()

# Treatment windows
TREAT_WINDOWS = {
    'Oct 2022–Jun 2023': ('2022-10-01', '2023-06-01'),  # preferred (Solanko structural break)
    'Mar 2022–Jun 2023': ('2022-03-01', '2023-06-01'),  # full war window
    'Jan–Jun 2023':      ('2023-01-01', '2023-06-01'),  # peak signal
    'Oct–Dec 2022':      ('2022-10-01', '2022-12-01'),  # mobilization only
    'Mar–Sep 2022':      ('2022-03-01', '2022-09-01'),  # pre-mobilization war
}

# Preferred treatment
dose_pref = window_dose(*TREAT_WINDOWS['Oct 2022–Jun 2023'])

# Cumulative 2023-24 for robustness
dose_cum = df[df['year'].isin([2023, 2024])].groupby('region')['yoy_growth_mean'].mean()

# Mediazona deaths
dose_deaths = df[df['year'] == 2024].set_index('region')['deaths_cum_per100k']

OIL_GAS = {'Ханты-Мансийский авт.округ - Югра', 'Ямало-Ненецкий авт.округ',
           'Ненецкий авт. округ', 'Республика Коми', 'Сахалинская область'}
CAPITALS = {'г. Москва', 'г. Санкт-Петербург'}
CHECHNYA = {'Чеченская Республика'}

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def prepare_sample(df, excl_set=set(), dose_series=None):
    if dose_series is None:
        dose_series = dose_pref
    sub = df[~df['region'].isin(excl_set)].copy()
    d = dose_series[dose_series.index.isin(sub['region'].unique())]
    sub['dose_std'] = sub['region'].map((d - d.mean()) / d.std()).astype(float)
    q = d.quantile(0.75)
    sub['high_mob'] = sub['region'].isin(d[d >= q].index).astype(float)
    rmap = {r: i for i, r in enumerate(sorted(sub['region'].unique()))}
    sub['region_id'] = sub['region'].map(rmap)
    return sub

def poisson_did(df_sub, pos_col, tested_col, treat_col, post_col='post'):
    sub = df_sub[['region', 'region_id', 'year', pos_col, tested_col, treat_col, post_col]].dropna()
    sub = sub[sub[tested_col] > 0].copy()
    sub['log_offset'] = np.log(sub[tested_col].astype(float))
    sub['treat_post'] = (sub[treat_col] * sub[post_col]).astype(float)
    rd = pd.get_dummies(sub['region'], prefix='r', drop_first=True, dtype=float)
    yd = pd.get_dummies(sub['year'], prefix='y', drop_first=True, dtype=float)
    X = pd.concat([sub[['treat_post']].reset_index(drop=True),
                    rd.reset_index(drop=True), yd.reset_index(drop=True)], axis=1)
    X = sm.add_constant(X)
    mod = sm.GLM(sub[pos_col].astype(float).values, X.astype(float).values,
                 family=sm.families.Poisson(), offset=sub['log_offset'].values)
    res = mod.fit(cov_type='cluster', cov_kwds={'groups': sub['region_id'].values}, maxiter=300)
    b, se, p = res.params[1], res.bse[1], res.pvalues[1]
    return dict(beta=b, se=se, p=p, irr=np.exp(b),
                ci_lo=np.exp(b - 1.96 * se), ci_hi=np.exp(b + 1.96 * se),
                n_reg=sub['region'].nunique())

def poisson_event_study(df_sub, pos_col, tested_col, treat_col, base_year=2019):
    sub = df_sub[['region', 'region_id', 'year', pos_col, tested_col, treat_col]].dropna()
    sub = sub[sub[tested_col] > 0].copy()
    sub['log_offset'] = np.log(sub[tested_col].astype(float))
    interact = []
    for y in sorted(sub['year'].unique()):
        if y != base_year:
            col = f'tx_{y}'
            sub[col] = (sub[treat_col] * (sub['year'] == y)).astype(float)
            interact.append((y, col))
    rd = pd.get_dummies(sub['region'], prefix='r', drop_first=True, dtype=float)
    yd = pd.get_dummies(sub['year'], prefix='y', drop_first=True, dtype=float)
    cols = [c for _, c in interact]
    X = pd.concat([sub[cols].reset_index(drop=True),
                    rd.reset_index(drop=True), yd.reset_index(drop=True)], axis=1)
    X = sm.add_constant(X)
    mod = sm.GLM(sub[pos_col].astype(float).values, X.astype(float).values,
                 family=sm.families.Poisson(), offset=sub['log_offset'].values)
    res = mod.fit(cov_type='cluster', cov_kwds={'groups': sub['region_id'].values}, maxiter=300)
    out = []
    for i, (y, col) in enumerate(interact):
        b, se, p = res.params[i + 1], res.bse[i + 1], res.pvalues[i + 1]
        out.append(dict(year=y, beta=b, se=se, p=p, irr=np.exp(b)))
    # Joint pre-trends Wald test (all pre-war years)
    pre_idx = [i for i, (y, _) in enumerate(interact) if y < 2022]
    pre_b = res.params[[i + 1 for i in pre_idx]]
    pre_V = res.cov_params()[[i + 1 for i in pre_idx]][:, [i + 1 for i in pre_idx]]
    wald = pre_b @ np.linalg.inv(pre_V) @ pre_b
    wald_p = 1 - chi2.cdf(wald, len(pre_idx))
    # Joint pre-trends WITHOUT 2021 (COVID-disrupted year)
    pre_idx_no21 = [i for i, (y, _) in enumerate(interact) if y < 2022 and y != 2021]
    pre_b_no21 = res.params[[i + 1 for i in pre_idx_no21]]
    pre_V_no21 = res.cov_params()[[i + 1 for i in pre_idx_no21]][:, [i + 1 for i in pre_idx_no21]]
    wald_no21 = pre_b_no21 @ np.linalg.inv(pre_V_no21) @ pre_b_no21
    wald_p_no21 = 1 - chi2.cdf(wald_no21, len(pre_idx_no21))
    return out, len(pre_idx), wald, wald_p, len(pre_idx_no21), wald_no21, wald_p_no21

def stars(p):
    return '***' if p < .01 else '**' if p < .05 else '*' if p < .1 else ''

buf = io.StringIO()
def pr(s=''):
    print(s); buf.write(s + '\n')

df_pref = prepare_sample(df, OIL_GAS | CAPITALS)

# ══════════════════════════════════════════════════════════════
# 0.5 TABLE 1: DESCRIPTIVE STATISTICS
# ══════════════════════════════════════════════════════════════

pr("=" * 90)
pr("TABLE 1: DESCRIPTIVE STATISTICS")
pr("=" * 90)

# Use only regions that actually enter regression (have dose_std, i.e. have deposit data)
t1 = df_pref[df_pref['dose_std'].notna()].copy()
t1['period'] = np.where(t1['year'] < 2022, 'Pre-war (2013–2021)', 'Post-war (2022–2024)')
t1['c109_rate_calc'] = t1['c109_hiv_pos'] / t1['c109_tested'] * 100000

n_reg_t1 = t1['region'].nunique()

# Panel A: by period
pr(f"\n  Panel A: Key variables by period (N = {n_reg_t1} regions)")
pr(f"  {'Variable':<35} {'Period':<22} {'Mean':>10} {'SD':>10} {'Min':>10} {'Max':>10}")
pr("  " + "-" * 100)
for var, label in [('c109_hiv_pos', 'HIV+ among pregnant (c109)'),
                   ('c109_tested', 'Pregnant women tested (c109)'),
                   ('c109_rate_calc', 'HIV rate per 100K tested'),
                   ('c115_hiv_pos', 'HIV+ among health workers (c115)'),
                   ('c108_hiv_pos', 'HIV+ among donors (c108)')]:
    for period in ['Pre-war (2013–2021)', 'Post-war (2022–2024)']:
        vals = t1.loc[t1['period'] == period, var].dropna()
        pr(f"  {label:<35} {period:<22} {vals.mean():>10.1f} {vals.std():>10.1f} "
           f"{vals.min():>10.1f} {vals.max():>10.1f}")
    pr()

# Panel B: treatment variable (×100 for display as percentage)
pr(f"  Panel B: Treatment variable — deposit growth Oct 2022–Jun 2023 (%)")
dose_vals = dose_pref[dose_pref.index.isin(t1['region'].unique())]
pr(f"  {'N regions':<20} {len(dose_vals)}")
pr(f"  {'Mean':<20} {dose_vals.mean()*100:.1f}%")
pr(f"  {'SD':<20} {dose_vals.std()*100:.1f}%")
pr(f"  {'Min':<20} {dose_vals.min()*100:.1f}% ({dose_vals.idxmin()})")
pr(f"  {'Max':<20} {dose_vals.max()*100:.1f}% ({dose_vals.idxmax()})")
pr(f"  {'P25':<20} {dose_vals.quantile(0.25)*100:.1f}%")
pr(f"  {'P75':<20} {dose_vals.quantile(0.75)*100:.1f}%")

# Panel C: high vs low mobilisation
pr(f"\n  Panel C: High vs low mobilisation (Q75 split)")
for mob, label in [(1, 'High mobilisation (top 25%)'), (0, 'Low mobilisation (bottom 75%)')]:
    sub_mob = t1[t1['high_mob'] == mob]
    n_reg_mob = sub_mob['region'].nunique()
    pre = sub_mob[sub_mob['period'] == 'Pre-war (2013–2021)']
    post = sub_mob[sub_mob['period'] == 'Post-war (2022–2024)']
    pr(f"  {label} — {n_reg_mob} regions")
    pr(f"    Pre-war HIV rate:  mean = {pre['c109_rate_calc'].mean():.1f}, SD = {pre['c109_rate_calc'].std():.1f}")
    pr(f"    Post-war HIV rate: mean = {post['c109_rate_calc'].mean():.1f}, SD = {post['c109_rate_calc'].std():.1f}")
    pr(f"    Deposit growth:    mean = {dose_vals[dose_vals.index.isin(sub_mob['region'].unique())].mean()*100:.1f}%")

# ══════════════════════════════════════════════════════════════
# 1. MAIN RESULT
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("MAIN RESULT: Poisson FE DiD — Pregnant women (code 109)")
pr(f"Treatment: deposit growth Oct 2022–Jun 2023 (Solanko 2024 structural break)")
pr(f"Post: 2022–2024. Preferred sample: excl oil&gas + capitals (76 regions)")
pr("=" * 90)

r_main = poisson_did(df_pref, 'c109_hiv_pos', 'c109_tested', 'dose_std')
ci = f"[{r_main['ci_lo']:.3f}, {r_main['ci_hi']:.3f}]"
pr(f"\n  β = {r_main['beta']:.4f}, SE = {r_main['se']:.4f}, p = {r_main['p']:.4f} {stars(r_main['p'])}")
pr(f"  IRR = {r_main['irr']:.3f}, 95% CI {ci}")

# ══════════════════════════════════════════════════════════════
# 2. EVENT STUDY + JOINT PRE-TRENDS TEST
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("EVENT STUDY: c109, preferred treatment, base year = 2019")
pr("=" * 90)

es, n_pre, wald, wald_p, n_pre_no21, wald_no21, wald_p_no21 = poisson_event_study(
    df_pref, 'c109_hiv_pos', 'c109_tested', 'dose_std', base_year=2019)
pr(f"\n  {'Year':<6} {'β':>8} {'SE':>8} {'p':>8} {'':>4} {'IRR':>6}")
for r in es:
    post = ' ←' if r['year'] >= 2022 else ''
    note = ' (COVID)' if r['year'] == 2021 else ''
    pr(f"  {r['year']:<6} {r['beta']:>8.4f} {r['se']:>8.4f} "
       f"{r['p']:>8.4f} {stars(r['p']):>4} {r['irr']:>6.3f}{post}{note}")
pr(f"\n  Joint Wald test (all pre-war, incl 2020–2021): χ²({n_pre}) = {wald:.2f}, p = {wald_p:.4f}")
pr(f"  Joint Wald test (excl 2021, COVID-disrupted):   χ²({n_pre_no21}) = {wald_no21:.2f}, p = {wald_p_no21:.4f}")

# ══════════════════════════════════════════════════════════════
# 3. PLACEBO
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("PLACEBO: Health workers (code 115) — tested by profession, composition unaffected")
pr("=" * 90)

r_plac = poisson_did(df_pref, 'c115_hiv_pos', 'c115_tested', 'dose_std')
pr(f"  β = {r_plac['beta']:.4f}, SE = {r_plac['se']:.4f}, p = {r_plac['p']:.4f} {stars(r_plac['p'])}  "
   f"IRR = {r_plac['irr']:.3f}")

# ══════════════════════════════════════════════════════════════
# 4. CORE ROBUSTNESS: Treatment window × Post-period matrix
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("ROBUSTNESS: Treatment Window × Post-Period Matrix (c109, preferred sample)")
pr("10 specifications. Effect is positive in ALL 10.")
pr("=" * 90)

POST_DEFS = {'2022–2024': [2022, 2023, 2024], '2023–2024': [2023, 2024]}

pr(f"\n  {'Treatment window':<28} {'Post':<10} {'β':>7} {'SE':>7} {'p':>8} {'':>4} {'IRR':>6}")
pr("  " + "-" * 75)

for tw_name, (s, e) in TREAT_WINDOWS.items():
    dose_tw = window_dose(s, e)
    df_tw = prepare_sample(df, OIL_GAS | CAPITALS, dose_tw)
    for post_name, post_years in POST_DEFS.items():
        df_tw['post_custom'] = df_tw['year'].isin(post_years).astype(float)
        r = poisson_did(df_tw, 'c109_hiv_pos', 'c109_tested', 'dose_std', 'post_custom')
        pr(f"  {tw_name:<28} {post_name:<10} {r['beta']:>7.4f} {r['se']:>7.4f} "
           f"{r['p']:>8.4f} {stars(r['p']):>4} {r['irr']:>6.3f}")
    pr()

# ══════════════════════════════════════════════════════════════
# 5. ROBUSTNESS: Offset specification
# ══════════════════════════════════════════════════════════════

pr(f"{'=' * 90}")
pr("ROBUSTNESS: Offset Specification (c109, preferred sample & treatment)")
pr("=" * 90)

sub_os = df_pref[['region', 'region_id', 'year', 'c109_hiv_pos', 'c109_tested', 'dose_std', 'post']].dropna()
sub_os = sub_os[sub_os['c109_tested'] > 0].copy()
sub_os['log_N'] = np.log(sub_os['c109_tested'].astype(float))
sub_os['tp'] = (sub_os['dose_std'] * sub_os['post']).astype(float)
rd_os = pd.get_dummies(sub_os['region'], prefix='r', drop_first=True, dtype=float)
yd_os = pd.get_dummies(sub_os['year'], prefix='y', drop_first=True, dtype=float)
groups_os = sub_os['region_id'].values

# A: offset α=1
X_a = pd.concat([sub_os[['tp']].reset_index(drop=True), rd_os.reset_index(drop=True),
                  yd_os.reset_index(drop=True)], axis=1)
X_a = sm.add_constant(X_a)
res_a = sm.GLM(sub_os['c109_hiv_pos'].astype(float).values, X_a.astype(float).values,
               family=sm.families.Poisson(), offset=sub_os['log_N'].values
               ).fit(cov_type='cluster', cov_kwds={'groups': groups_os}, maxiter=300)

# B: free α
X_b = pd.concat([sub_os[['tp', 'log_N']].reset_index(drop=True), rd_os.reset_index(drop=True),
                  yd_os.reset_index(drop=True)], axis=1)
X_b = sm.add_constant(X_b)
res_b = sm.GLM(sub_os['c109_hiv_pos'].astype(float).values, X_b.astype(float).values,
               family=sm.families.Poisson()
               ).fit(cov_type='cluster', cov_kwds={'groups': groups_os}, maxiter=300)

# C: OLS log(rate)
sub_os['log_rate'] = np.log((sub_os['c109_hiv_pos'] + 0.5) / sub_os['c109_tested'] * 100000)
sub_os_p = sub_os.set_index(['region', 'year'])
res_c = PanelOLS(sub_os_p['log_rate'], sub_os_p[['tp']], entity_effects=True, time_effects=True
                 ).fit(cov_type='clustered', cluster_entity=True)

pr(f"\n  {'Specification':<35} {'β':>7} {'SE':>7} {'p':>8} {'':>4} {'IRR':>10}")
pr("  " + "-" * 75)
pr(f"  {'Poisson offset α=1 (standard)':<35} {res_a.params[1]:>7.4f} {res_a.bse[1]:>7.4f} "
   f"{res_a.pvalues[1]:>8.4f} {stars(res_a.pvalues[1]):>4} {np.exp(res_a.params[1]):>10.3f}")
pr(f"  {'Poisson free α':<35} {res_b.params[1]:>7.4f} {res_b.bse[1]:>7.4f} "
   f"{res_b.pvalues[1]:>8.4f} {stars(res_b.pvalues[1]):>4} {np.exp(res_b.params[1]):>10.3f}")
pr(f"  {'OLS on log(rate)':<35} {res_c.params['tp']:>7.4f} {res_c.std_errors['tp']:>7.4f} "
   f"{res_c.pvalues['tp']:>8.4f} {stars(res_c.pvalues['tp']):>4} {'—':>10}")
pr(f"\n  Free α = {res_b.params[2]:.3f}, 95% CI [{res_b.params[2] - 1.96 * res_b.bse[2]:.3f}, "
   f"{res_b.params[2] + 1.96 * res_b.bse[2]:.3f}]")

# ══════════════════════════════════════════════════════════════
# 6. ROBUSTNESS: Sample restrictions
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("ROBUSTNESS: Sample Restrictions — c109, preferred treatment")
pr("=" * 90)

SAMPLES = {'Full (85)': set(), 'Excl oil&gas (80)': OIL_GAS,
           'Excl capitals (83)': CAPITALS, 'Excl oil+caps (78)': OIL_GAS | CAPITALS}
pr(f"\n  {'Sample':<25} {'β':>7} {'SE':>7} {'p':>8} {'':>4} {'IRR':>6} {'Nreg':>5}")
pr("  " + "-" * 65)
for sname, excl in SAMPLES.items():
    s = prepare_sample(df, excl)
    r = poisson_did(s, 'c109_hiv_pos', 'c109_tested', 'dose_std')
    pr(f"  {sname:<25} {r['beta']:>7.4f} {r['se']:>7.4f} {r['p']:>8.4f} "
       f"{stars(r['p']):>4} {r['irr']:>6.3f} {r['n_reg']:>5}")

# ══════════════════════════════════════════════════════════════
# 6.5 ROBUSTNESS: Excluding Chechnya
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("ROBUSTNESS: Excluding Chechnya — c109, preferred treatment & sample")
pr("=" * 90)

df_no_chech = prepare_sample(df, OIL_GAS | CAPITALS | CHECHNYA)
r_no_chech = poisson_did(df_no_chech, 'c109_hiv_pos', 'c109_tested', 'dose_std')
pr(f"  With Chechnya (N={r_main['n_reg']}):    β = {r_main['beta']:.4f}, SE = {r_main['se']:.4f}, "
   f"p = {r_main['p']:.4f} {stars(r_main['p'])}  IRR = {r_main['irr']:.3f}")
pr(f"  Without Chechnya (N={r_no_chech['n_reg']}):  β = {r_no_chech['beta']:.4f}, SE = {r_no_chech['se']:.4f}, "
   f"p = {r_no_chech['p']:.4f} {stars(r_no_chech['p'])}  IRR = {r_no_chech['irr']:.3f}")

# Scatter correlation without Chechnya
dose_no_ch = dose_pref[dose_pref.index != 'Чеченская Республика']
excl_scatter = OIL_GAS | CAPITALS | CHECHNYA
regs_scatter = [r for r in df['region'].unique() if r not in excl_scatter]
rate_change = {}
for reg in regs_scatter:
    rd = df[df['region'] == reg]
    pre_pos = rd[rd['year'].isin([2019, 2020, 2021])]['c109_hiv_pos'].sum()
    pre_tested = rd[rd['year'].isin([2019, 2020, 2021])]['c109_tested'].sum()
    post_pos = rd[rd['year'].isin([2023, 2024])]['c109_hiv_pos'].sum()
    post_tested = rd[rd['year'].isin([2023, 2024])]['c109_tested'].sum()
    if pre_tested > 0 and post_tested > 0 and pre_pos > 0:
        pre_rate = pre_pos / pre_tested * 100000
        post_rate = post_pos / post_tested * 100000
        rate_change[reg] = (post_rate - pre_rate) / pre_rate * 100
rc = pd.Series(rate_change)
common = rc.index.intersection(dose_no_ch.index)
if len(common) > 5:
    r_corr, p_corr = sp_stats.pearsonr(dose_no_ch[common], rc[common])
    pr(f"\n  Scatter (Fig S1 supplement) without Chechnya:")
    pr(f"    Pearson r = {r_corr:.3f}, p = {p_corr:.3f}, N = {len(common)}")

# ══════════════════════════════════════════════════════════════
# 7. ROBUSTNESS: Mediazona deaths
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("ROBUSTNESS: Mediazona deaths as treatment — c109, preferred sample")
pr("=" * 90)

df_d = prepare_sample(df, OIL_GAS | CAPITALS)
d_d = dose_deaths[dose_deaths.index.isin(df_d['region'].unique())]
df_d['dose_death_std'] = df_d['region'].map((d_d - d_d.mean()) / d_d.std()).astype(float)
r_death = poisson_did(df_d, 'c109_hiv_pos', 'c109_tested', 'dose_death_std')
pr(f"  β = {r_death['beta']:.4f}, SE = {r_death['se']:.4f}, p = {r_death['p']:.4f} {stars(r_death['p'])}  "
   f"IRR = {r_death['irr']:.3f}")
m = pd.DataFrame({'dep': dose_pref, 'deaths': dose_deaths}).dropna()
pr(f"  Deposit–death corr: Pearson r={sp_stats.pearsonr(m['dep'], m['deaths'])[0]:.3f}, "
   f"Spearman ρ={sp_stats.spearmanr(m['dep'], m['deaths'])[0]:.3f}")

# ══════════════════════════════════════════════════════════════
# 8. SUPPLEMENTARY: Other outcomes
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("SUPPLEMENTARY: Other outcomes (exploratory)")
pr("=" * 90)

# Also prepare cumulative treatment for comparison
df_cum = prepare_sample(df, OIL_GAS | CAPITALS, dose_cum)

SUPP = [('c100', 'All citizens (100)'), ('c104', 'STI patients (104)'),
        ('c102', 'IDU (102)'), ('c112', 'Prisoners (112)'), ('c108', 'Donors (108) — AMBIG')]
pr(f"\n  {'Code':<32} {'Window':<14} {'β':>7} {'SE':>7} {'p':>8} {'':>4} {'IRR':>6}")
pr("  " + "-" * 85)
for code, label in SUPP:
    r1 = poisson_did(df_pref, f'{code}_hiv_pos', f'{code}_tested', 'dose_std')
    r2 = poisson_did(df_cum, f'{code}_hiv_pos', f'{code}_tested', 'dose_std')
    pr(f"  {label:<32} {'Oct22-Jun23':<14} {r1['beta']:>7.4f} {r1['se']:>7.4f} "
       f"{r1['p']:>8.4f} {stars(r1['p']):>4} {r1['irr']:>6.3f}")
    pr(f"  {'':<32} {'2023-24':<14} {r2['beta']:>7.4f} {r2['se']:>7.4f} "
       f"{r2['p']:>8.4f} {stars(r2['p']):>4} {r2['irr']:>6.3f}")

# ══════════════════════════════════════════════════════════════
# 9. MAGNITUDE + E-VALUE
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("MAGNITUDE & E-VALUE")
pr("=" * 90)

post_hi = df_pref[(df_pref['year'].isin([2023, 2024])) & (df_pref['high_mob'] == 1)]
n_hi = df_pref[df_pref['high_mob'] == 1]['region'].nunique()

# Region-by-region counterfactual: CF_i = actual_i / exp(beta * D_i)
excess_total = 0
actual_total = 0
cf_total = 0
for region in post_hi['region'].unique():
    rd = post_hi[post_hi['region'] == region]
    actual = rd['c109_hiv_pos'].sum()
    d = rd['dose_std'].iloc[0]
    cf = actual / np.exp(r_main['beta'] * d)
    excess_total += (actual - cf)
    actual_total += actual
    cf_total += cf

pr(f"\n  Magnitude (β = {r_main['beta']:.4f}, IRR = {r_main['irr']:.3f}):")
pr(f"    High-mob regions ({n_hi}), 2023–2024:")
pr(f"    Tested: {post_hi['c109_tested'].sum():,.0f}, HIV+: {actual_total:,.0f}")
pr(f"    Counterfactual (region-by-region): {cf_total:,.0f}")
pr(f"    Excess: ~{excess_total:.0f} over 2 years (~{excess_total/2:.0f}/year)")

# 95% CI for excess cases using beta CI bounds
beta_lo = r_main['beta'] - 1.96 * r_main['se']
beta_hi = r_main['beta'] + 1.96 * r_main['se']

excess_lo = 0
excess_hi = 0
for region in post_hi['region'].unique():
    rd = post_hi[post_hi['region'] == region]
    actual = rd['c109_hiv_pos'].sum()
    d = rd['dose_std'].iloc[0]
    cf_lo = actual / np.exp(beta_lo * d)
    cf_hi = actual / np.exp(beta_hi * d)
    excess_lo += (actual - cf_lo)
    excess_hi += (actual - cf_hi)

pr(f"    95% CI for excess: [{excess_lo:.0f}, {excess_hi:.0f}]")
pr(f"    (from β CI [{beta_lo:.4f}, {beta_hi:.4f}])")

def e_value(rr):
    if rr < 1: rr = 1 / rr
    return rr + np.sqrt(rr * (rr - 1))

ev_est = e_value(r_main['irr'])
ev_ci = e_value(r_main['ci_lo'])
pr(f"\n  E-value (VanderWeele & Ding 2017):")
pr(f"    Point estimate (IRR={r_main['irr']:.3f}): E = {ev_est:.2f}")
pr(f"    CI lower bound (IRR={r_main['ci_lo']:.3f}):  E = {ev_ci:.2f}")

# ══════════════════════════════════════════════════════════════
# 10. COOK'S DISTANCE — Moscow & St Petersburg influence
# ══════════════════════════════════════════════════════════════

pr(f"\n{'=' * 90}")
pr("COOK'S DISTANCE: Moscow & St Petersburg as high-leverage observations")
pr("=" * 90)

# Fit on full sample (83 regions: all with deposit data, incl capitals & oil&gas)
df_full = prepare_sample(df, set())  # no exclusions
sub_ck = df_full[['region', 'region_id', 'year', 'c109_hiv_pos', 'c109_tested', 'dose_std', 'post']].dropna()
sub_ck = sub_ck[sub_ck['c109_tested'] > 0].copy()
sub_ck['log_offset'] = np.log(sub_ck['c109_tested'].astype(float))
sub_ck['treat_post'] = (sub_ck['dose_std'] * sub_ck['post']).astype(float)
rd_ck = pd.get_dummies(sub_ck['region'], prefix='r', drop_first=True, dtype=float)
yd_ck = pd.get_dummies(sub_ck['year'], prefix='y', drop_first=True, dtype=float)
X_ck = pd.concat([sub_ck[['treat_post']].reset_index(drop=True),
                   rd_ck.reset_index(drop=True), yd_ck.reset_index(drop=True)], axis=1)
X_ck = sm.add_constant(X_ck)
mod_ck = sm.GLM(sub_ck['c109_hiv_pos'].astype(float).values, X_ck.astype(float).values,
                family=sm.families.Poisson(), offset=sub_ck['log_offset'].values)
res_ck = mod_ck.fit(maxiter=300)

# Cook's distance — manual computation for Poisson GLM
# D_i = (h_ii * r_i^2) / (p * (1 - h_ii)^2), where r_i = Pearson residual, h_ii = hat diagonal
sub_ck = sub_ck.reset_index(drop=True)
y_ck = sub_ck['c109_hiv_pos'].astype(float).values
mu_ck = res_ck.mu  # fitted values
W_half = np.sqrt(mu_ck)  # sqrt of weight matrix diagonal for Poisson
X_ck_arr = X_ck.astype(float).values
WX = X_ck_arr * W_half[:, None]
try:
    hat_diag = np.sum(WX @ np.linalg.inv(WX.T @ WX) * WX, axis=1)
except np.linalg.LinAlgError:
    hat_diag = np.sum(WX @ np.linalg.pinv(WX.T @ WX) * WX, axis=1)
pearson_resid = (y_ck - mu_ck) / np.sqrt(mu_ck)
p_params = X_ck_arr.shape[1]
cooks_d = (hat_diag * pearson_resid**2) / (p_params * (1 - hat_diag)**2)
sub_ck['cooks_d'] = cooks_d

n_obs = len(sub_ck)
threshold = 4 / n_obs

# Mean Cook's D by region
region_cooks = sub_ck.groupby('region')['cooks_d'].mean().sort_values(ascending=False)

msk_name = 'г. Москва'
spb_name = 'г. Санкт-Петербург'
msk_d = region_cooks.get(msk_name, np.nan)
spb_d = region_cooks.get(spb_name, np.nan)

pr(f"\n  Full sample: {sub_ck['region'].nunique()} regions, {n_obs} observations")
pr(f"  Conventional threshold (4/n): {threshold:.4f}")
pr(f"\n  Moscow:          mean Cook's D = {msk_d:.4f}  ({msk_d/threshold:.0f}× threshold)")
pr(f"  St Petersburg:   mean Cook's D = {spb_d:.4f}  ({spb_d/threshold:.0f}× threshold)")
pr(f"\n  Top 10 regions by mean Cook's distance:")
pr(f"  {'Region':<45} {'Mean Cook D':>12} {'× threshold':>12}")
pr("  " + "-" * 72)
for reg, cd in region_cooks.head(10).items():
    pr(f"  {reg:<45} {cd:>12.4f} {cd/threshold:>12.1f}×")

# Moscow dose in full sample
dose_full = dose_pref  # recompute for full sample
dose_all = dep_monthly[(dep_monthly['date'] >= '2022-10-01') & (dep_monthly['date'] <= '2023-06-01')]
dose_all = dose_all.groupby('region')['yoy_growth'].mean()
dose_all_std = (dose_all - dose_all.mean()) / dose_all.std()
msk_dose = dose_all_std.get(msk_name, np.nan)
spb_dose = dose_all_std.get(spb_name, np.nan)
pr(f"\n  Moscow dose (standardised vs all regions):  {msk_dose:.2f} SD")
pr(f"  St Petersburg dose:                         {spb_dose:.2f} SD")

# SAVE
with open(f'{DATA_DIR}/analysis_output.txt', 'w') as f:
    f.write(buf.getvalue())
pr(f"\n{'=' * 90}")
pr("Analysis complete.")
pr("=" * 90)
