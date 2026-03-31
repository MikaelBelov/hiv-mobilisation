"""
Extract HIV code tables (100, 109, 111, 112) from bulletins 48-50 (years 2022-2024).
Each bulletin contains 3-year tables; we extract only the last year's columns.
"""
import pdfplumber
import pandas as pd
import re
import os
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def clean_num(s):
    if s is None:
        return None
    s = str(s).strip()
    if s in ('', '-', '‑', '–', '—', '0,0', '0.0'):
        return None
    s = re.sub(r'\s+', '', s)
    s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return None

def clean_region(s):
    if s is None:
        return ''
    return ' '.join(str(s).split())

def is_fo_row(region):
    r = region.lower()
    return any(m in r for m in ['федеральный округ', 'федеральный\nокруг'])

def is_skip_row(region):
    """Skip header, empty, FO subtotal rows (keep RF total and regions)"""
    if not region:
        return True
    if 'Наименование' in region:
        return True
    return False

BULLETINS = [
    # Bulletins 48-50: 22 codes, identical page layout
    # No PDF page offset needed (TOC page = PDF page)
    # Bulletins 48-50: PDF page = printed page + 1 (unnumbered cover page)
    (48, f'{DATA_DIR}/hiv-infection-info-bulletin-48.pdf', 2022, {
        '100': (17, 18), '101': (19, 20), '102': (21, 22), '103': (23, 24),
        '104': (25, 26), '105': (27, 28), '108': (29, 30), '109': (31, 32),
        '110': (33, 34), '111': (35, 36), '112': (37, 38), '113': (39, 40),
        '114': (41, 42), '115': (43, 44), '116': (45, 46), '117': (47, 48),
        '118': (49, 50), '120': (51, 52), '121': (53, 54), '124': (55, 56),
        '125': (57, 58), '200': (59, 60),
    }),
    (49, f'{DATA_DIR}/hiv-infection-info-bulletin-49.pdf', 2023, {
        '100': (17, 18), '101': (19, 20), '102': (21, 22), '103': (23, 24),
        '104': (25, 26), '105': (27, 28), '108': (29, 30), '109': (31, 32),
        '110': (33, 34), '111': (35, 36), '112': (37, 38), '113': (39, 40),
        '114': (41, 42), '115': (43, 44), '116': (45, 46), '117': (47, 48),
        '118': (49, 50), '120': (51, 52), '121': (53, 54), '124': (55, 56),
        '125': (57, 58), '200': (59, 60),
    }),
    (50, f'{DATA_DIR}/hiv-infection-info-bulletin-50.pdf', 2024, {
        '100': (17, 18), '101': (19, 20), '102': (21, 22), '103': (23, 24),
        '104': (25, 26), '105': (27, 28), '108': (29, 30), '109': (31, 32),
        '110': (33, 34), '111': (35, 36), '112': (37, 38), '113': (39, 40),
        '114': (41, 42), '115': (43, 44), '116': (45, 46), '117': (47, 48),
        '118': (49, 50), '120': (51, 52), '121': (53, 54), '124': (55, 56),
        '125': (57, 58), '200': (59, 60),
    }),
]

# For each code, how many columns per year and which position is the rate
# Code 100 has 4 cols/year (tested, pct, hiv, rate); all others have 3 (tested, hiv, rate)
CODE_STRUCTURE = {
    '100': {'cols_per_year': 4, 'col_tested': 0, 'col_pct': 1, 'col_hiv': 2, 'col_rate': 3},
}
# Default for all other codes
DEFAULT_CODE_STRUCTURE = {'cols_per_year': 3, 'col_tested': 0, 'col_pct': None, 'col_hiv': 1, 'col_rate': 2}

all_rows = []

for bnum, fpath, year, code_pages in BULLETINS:
    print(f"\n=== Bulletin {bnum} (year {year}) ===")
    with pdfplumber.open(fpath) as pdf:
        for code, (p1, p2) in sorted(code_pages.items(), key=lambda x: int(x[0])):
            struct = CODE_STRUCTURE.get(code, DEFAULT_CODE_STRUCTURE)
            cols_per_year = struct['cols_per_year']

            # Collect rows from both pages
            raw_rows = []
            n_years = None

            for p_idx in [p1 - 1, p2 - 1]:  # convert to 0-indexed
                if p_idx >= len(pdf.pages):
                    continue
                page = pdf.pages[p_idx]
                text = page.extract_text() or ''

                tables = page.extract_tables()
                if not tables:
                    print(f"  WARNING: No table on page {p_idx+1} for code {code}")
                    continue
                t = tables[0]

                # Detect number of years from header
                if n_years is None:
                    for row in t[:3]:
                        years_found = sum(1 for cell in row if cell and re.match(r'^20\d{2}$', str(cell).strip()))
                        if years_found > 0:
                            n_years = years_found
                            break
                    if n_years is None:
                        n_years = 3  # default assumption

                for row in t:
                    if row[0] is None:
                        continue
                    region = clean_region(row[0])
                    if is_skip_row(region):
                        continue
                    # Skip year header rows
                    if re.match(r'^20\d{2}$', region):
                        continue
                    raw_rows.append((region, row))

            if n_years is None:
                n_years = 3

            # The last year's columns start at position: 1 + (n_years-1)*cols_per_year
            last_year_offset = 1 + (n_years - 1) * cols_per_year

            print(f"  Code {code}: {len(raw_rows)} rows, {n_years} years, last year offset={last_year_offset}")

            for region, row in raw_rows:
                is_fo = is_fo_row(region)
                is_russia = (region == 'Российская Федерация')

                try:
                    tested = clean_num(row[last_year_offset + struct['col_tested']])
                    pct = clean_num(row[last_year_offset + struct['col_pct']]) if struct['col_pct'] is not None else None
                    hiv = clean_num(row[last_year_offset + struct['col_hiv']])
                    rate = clean_num(row[last_year_offset + struct['col_rate']])
                except IndexError:
                    print(f"  IndexError for region '{region}' code {code}, row len={len(row)}")
                    continue

                all_rows.append({
                    'region': region,
                    'year': year,
                    'code': int(code),
                    'is_fo': is_fo,
                    'is_russia': is_russia,
                    'tested': tested,
                    'pct_population_tested': pct,
                    'hiv_positive': hiv,
                    'rate_per_100k_tested': rate,
                })

df = pd.DataFrame(all_rows)
df.to_csv(f'{DATA_DIR}/hiv_codes_2022_2024.csv', index=False)

# Verification of known values
print("\n=== VERIFICATION (known RF values) ===")
for year, code, exp_hiv in [(2024, 100, 72361), (2024, 111, 2036), (2024, 109, 1740), (2024, 112, 3801),
                             (2022, 111, 311), (2023, 111, 945)]:
    row = df[(df.year == year) & (df.code == code) & df.is_russia]
    if len(row) > 0:
        actual = row.iloc[0]['hiv_positive']
        status = "OK" if actual == exp_hiv else f"MISMATCH (expected {exp_hiv})"
        print(f"  Year {year}, Code {code}, RF HIV+: {actual} — {status}")
    else:
        print(f"  Year {year}, Code {code}: RF row NOT FOUND")

# Summary
print(f"\n=== SUMMARY ===")
print(f"Total rows saved: {len(df)}")
pivot = df.groupby(['year', 'code'])['region'].count().unstack(fill_value=0)
print(pivot.to_string())

# RF check for every year x code
print(f"\n=== RF PRESENCE CHECK ===")
rf_df = df[df.is_russia]
for year in sorted(df.year.unique()):
    codes = sorted(rf_df[rf_df.year == year].code.unique())
    print(f"  {year}: RF in {len(codes)} codes")

print(f"\nSaved to hiv_codes_2022_2024.csv")
