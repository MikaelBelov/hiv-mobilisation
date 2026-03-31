"""
Extract HIV code tables from bulletins 34-43 (years 2009-2017).

Bulletins 34-43 contain regional code tables for 12 codes:
  100 (граждане РФ), 102 (наркотики), 103 (МСМ), 104 (ИППП),
  108 (доноры), 109 (беременные), 112 (заключённые), 113 (клинические),
  115 (медсотрудники), 118 (прочие), 120 (эпидрасследование), 200 (иностранные)

Each table spans 2 pages with 2 years of data; we extract only the LAST year.
Exception: bulletin 40 (2014) is a scanned PDF that pdfplumber can't read,
so we extract 2014 from bulletin 41 (which has 2014-2015 tables) using FIRST year columns.

Code 100 has 3 cols/year in early bulletins (34-36) and 4 cols/year in later ones (40+).
Other codes always have 3 cols/year.
The detect_structure() function auto-detects from headers.
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
    return any(m in r for m in ['федеральный округ', 'федеральный\nокруг', ' фо'])

def is_skip_row(region):
    if not region:
        return True
    if 'Наименование' in region or 'наименование' in region:
        return True
    if re.match(r'^20\d{2}$', region):
        return True
    return False


# Each entry: (bulletin_num, filepath, data_year, code_pages, extract_first_year)
# extract_first_year=True means we take the FIRST year from the 2-year table
# (used for 2014 since bulletin 40 is a scanned PDF)
BULLETINS = [
    (34, f'{DATA_DIR}/Byulleten-34-VICH-infektsiya-2009-g..pdf', 2009, {
        '100': (8, 9), '102': (10, 11), '103': (12, 13), '104': (14, 15),
        '108': (16, 17), '109': (18, 19), '112': (20, 21), '113': (22, 23),
        '115': (24, 25), '118': (26, 27), '120': (28, 29), '200': (30, 31),
    }, False),
    (35, f'{DATA_DIR}/Byulleten-35-VICH-infektsiya-2010-g..pdf', 2010, {
        '100': (12, 13), '102': (14, 15), '103': (16, 17), '104': (18, 19),
        '108': (20, 21), '109': (22, 23), '112': (24, 25), '113': (26, 27),
        '115': (28, 29), '118': (30, 31), '120': (32, 33), '200': (34, 35),
    }, False),
    (36, f'{DATA_DIR}/Byulleten-36-VICH-infektsiya-2011-g..pdf', 2011, {
        '100': (8, 9), '102': (10, 11), '103': (12, 13), '104': (14, 15),
        '108': (16, 17), '109': (18, 19), '112': (20, 21), '113': (22, 23),
        '115': (24, 25), '118': (26, 27), '120': (28, 29), '200': (30, 31),
    }, False),
    (38, f'{DATA_DIR}/Byulleten-38-VICH-infektsiya-2012-g..pdf', 2012, {
        '100': (8, 9), '102': (10, 11), '103': (12, 13), '104': (14, 15),
        '108': (16, 17), '109': (18, 19), '112': (20, 21), '113': (22, 23),
        '115': (24, 25), '118': (26, 27), '120': (28, 29), '200': (30, 31),
    }, False),
    (39, f'{DATA_DIR}/Byulleten-39-VICH-infektsiya-2013-g..pdf', 2013, {
        '100': (8, 9), '102': (10, 11), '103': (12, 13), '104': (14, 15),
        '108': (16, 17), '109': (18, 19), '112': (20, 21), '113': (22, 23),
        '115': (24, 25), '118': (26, 27), '120': (28, 29), '200': (30, 31),
    }, False),
    # Bulletin 40 is a scanned PDF — extract 2014 from bulletin 41 (first year)
    (41, f'{DATA_DIR}/Byulleten-41-VICH-infektsiya-2015g..pdf', 2014, {
        '100': (11, 12), '102': (13, 14), '103': (15, 16), '104': (17, 18),
        '108': (19, 20), '109': (21, 22), '112': (23, 24), '113': (25, 26),
        '115': (27, 28), '118': (29, 30), '120': (31, 32), '200': (33, 34),
    }, True),
    (41, f'{DATA_DIR}/Byulleten-41-VICH-infektsiya-2015g..pdf', 2015, {
        '100': (11, 12), '102': (13, 14), '103': (15, 16), '104': (17, 18),
        '108': (19, 20), '109': (21, 22), '112': (23, 24), '113': (25, 26),
        '115': (27, 28), '118': (29, 30), '120': (31, 32), '200': (33, 34),
    }, False),
    (42, f'{DATA_DIR}/Byulleten-42-VICH-infektsiya-2016g..pdf', 2016, {
        '100': (11, 12), '102': (13, 14), '103': (15, 16), '104': (17, 18),
        '108': (19, 20), '109': (21, 22), '112': (23, 24), '113': (25, 26),
        '115': (27, 28), '118': (29, 30), '120': (31, 32), '200': (33, 34),
    }, False),
    (43, f'{DATA_DIR}/Byulleten-43-VICH-infektsiya-2017g..pdf', 2017, {
        '100': (11, 12), '102': (13, 14), '103': (15, 16), '104': (17, 18),
        '108': (19, 20), '109': (21, 22), '112': (23, 24), '113': (25, 26),
        '115': (27, 28), '118': (29, 30), '120': (31, 32), '200': (33, 34),
    }, False),
]


def detect_structure(tables):
    """Detect cols per year and number of years from table headers."""
    for t in tables:
        for row in t[:5]:
            year_positions = [i for i, c in enumerate(row)
                             if c and re.match(r'^20\d{2}$', str(c).strip())]
            if len(year_positions) >= 2:
                n_years = len(year_positions)
                cols_per_year = year_positions[1] - year_positions[0]
                return n_years, cols_per_year
    return None, None


def extract_code_table(pdf, pages_1idx, year, code, bnum, extract_first_year=False):
    """Extract data for a specific code, returning list of dicts.
    If extract_first_year=True, take the FIRST year's columns instead of the last."""
    raw_rows = []
    n_years = None
    cols_per_year = None

    for p_1idx in pages_1idx:
        p_0idx = p_1idx - 1
        if p_0idx >= len(pdf.pages):
            print(f"    WARNING: Page {p_1idx} out of range (total {len(pdf.pages)})")
            continue
        page = pdf.pages[p_0idx]
        tables = page.extract_tables()
        if not tables:
            print(f"    WARNING: No table on page {p_1idx}")
            continue

        if n_years is None:
            n_years, cols_per_year = detect_structure(tables)

        t = tables[0]
        for row in t:
            if row[0] is None:
                continue
            region = clean_region(row[0])
            if is_skip_row(region):
                continue
            raw_rows.append((region, row))

    if not raw_rows:
        print(f"    No data found for code {code}")
        return []

    # If detection failed, guess based on total cols
    if n_years is None or cols_per_year is None:
        sample_len = len(raw_rows[0][1])
        if code == '100':
            if (sample_len - 1) % 4 == 0:
                cols_per_year = 4
            else:
                cols_per_year = 3
        else:
            cols_per_year = 3
        n_years = (sample_len - 1) // cols_per_year
        print(f"    WARNING: Auto-detect failed for code {code} bul {bnum}, "
              f"row len={sample_len}, guessing n_years={n_years}, cols_per_year={cols_per_year}")

    # Column indices for target year
    if extract_first_year:
        group_start = 1  # first year starts at column 1
    else:
        group_start = 1 + (n_years - 1) * cols_per_year  # last year

    # Determine if this code 100 table has a pct column
    has_pct = (code == '100' and cols_per_year == 4)

    results = []
    for region, row in raw_rows:
        is_fo = is_fo_row(region)
        is_russia = ('Российская Федерация' in region)

        try:
            tested = clean_num(row[group_start])
            if has_pct:
                pct = clean_num(row[group_start + 1])
                hiv = clean_num(row[group_start + 2])
                rate = clean_num(row[group_start + 3])
            else:
                pct = None
                hiv = clean_num(row[group_start + 1])
                rate = clean_num(row[group_start + 2])
        except IndexError:
            print(f"    IndexError for region '{region}', code {code}, "
                  f"row len={len(row)}, group_start={group_start}, "
                  f"cols_per_year={cols_per_year}")
            continue

        results.append({
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

    return results


all_rows = []

for bnum, fpath, year, code_pages, first_year in BULLETINS:
    label = f"Bulletin {bnum} (year {year})"
    if first_year:
        label += " [FIRST year from bulletin]"
    print(f"\n=== {label} ===")
    with pdfplumber.open(fpath) as pdf:
        for code, pages in sorted(code_pages.items(), key=lambda x: int(x[0])):
            print(f"  Code {code} (pages {pages}):")
            rows = extract_code_table(pdf, list(pages), year, code, bnum, first_year)
            print(f"    Got {len(rows)} rows")
            # Print RF row for verification
            rf = [r for r in rows if r['is_russia']]
            if rf:
                r = rf[0]
                print(f"    RF: tested={r['tested']}, hiv+={r['hiv_positive']}, "
                      f"rate={r['rate_per_100k_tested']}")
            else:
                print(f"    WARNING: RF row not found!")
            all_rows.extend(rows)

df = pd.DataFrame(all_rows)
df.to_csv(f'{DATA_DIR}/hiv_codes_2009_2017.csv', index=False)

# Summary
print(f"\n=== SUMMARY ===")
print(f"Total rows: {len(df)}")
print(f"\nRows per year x code:")
pivot = df.groupby(['year', 'code'])['region'].count().unstack(fill_value=0)
print(pivot.to_string())

# Verification: check that we have RF row for every year x code
print(f"\n=== RF VERIFICATION ===")
rf_df = df[df.is_russia]
for year in sorted(df.year.unique()):
    codes_found = sorted(rf_df[rf_df.year == year].code.unique())
    print(f"  {year}: RF found for codes {codes_found}")

print(f"\nSaved to hiv_codes_2009_2017.csv")
