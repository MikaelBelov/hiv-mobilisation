"""
Extract HIV code tables from bulletins 44-47 (years 2018-2021).

Bulletins 44-45: 2-year tables, no code 111
Bulletins 46-47: 2 or 3-year tables, code 111 available

Column structure for bulletins 44-45 (code 100):
  region | tested_yr1 | pct_yr1 | hiv_yr1 | rate_yr1 | tested_yr2 | pct_yr2 | hiv_yr2 | rate_yr2
  (9 cols total)

Column structure for bulletins 44-45 (codes 109, 112):
  region | tested_yr1 | hiv_yr1 | rate_yr1 | tested_yr2 | hiv_yr2 | rate_yr2
  (7 cols total)

Bulletins 46-47: may vary, detect from header
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
    if s in ('', '-', '‑', '–', '—'):
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
    if 'Наименование' in region:
        return True
    if re.match(r'^20\d{2}$', region):
        return True
    return False

BULLETINS = [
    # (bulletin_num, filepath, data_year, code_pages_dict)
    # Bulletins 44-45: 12 codes (no 111, 117, 125)
    # NOTE: PDF page = TOC page + 1 for these bulletins
    (44, f'{DATA_DIR}/Byulleten-44-VICH-infektsiya-2019-g..pdf', 2018, {
        '100': (12, 13), '102': (14, 15), '103': (16, 17), '104': (18, 19),
        '108': (20, 21), '109': (22, 23), '112': (24, 25), '113': (26, 27),
        '115': (28, 29), '118': (30, 31), '120': (32, 33), '200': (34, 35),
    }),
    (45, f'{DATA_DIR}/Byulleten-45-VICH-infektsiya-2019-g..pdf', 2019, {
        '100': (12, 13), '102': (14, 15), '103': (16, 17), '104': (18, 19),
        '108': (20, 21), '109': (22, 23), '112': (24, 25), '113': (26, 27),
        '115': (28, 29), '118': (30, 31), '120': (32, 33), '200': (34, 35),
    }),
    # Bulletins 46-47: 15 codes (added 111, 117, 125)
    (46, f'{DATA_DIR}/Byulleten-46-VICH-infektsiya-za-2020-g.-.pdf', 2020, {
        '100': (18, 19), '102': (22, 23), '103': (24, 25), '104': (26, 27),
        '108': (30, 31), '109': (32, 33), '111': (36, 37), '112': (38, 39),
        '113': (40, 41), '115': (44, 45), '117': (48, 49), '118': (50, 51),
        '120': (52, 53), '125': (58, 59), '200': (60, 61),
    }),
    (47, f'{DATA_DIR}/Byulleten-47-VICH-infektsiya-za-2021-g.pdf', 2021, {
        '100': (17, 18), '102': (21, 22), '103': (23, 24), '104': (25, 26),
        '108': (29, 30), '109': (31, 32), '111': (35, 36), '112': (37, 38),
        '113': (39, 40), '115': (43, 44), '117': (47, 48), '118': (49, 50),
        '120': (51, 52), '125': (57, 58), '200': (59, 60),
    }),
]

def detect_structure(tables):
    """Detect cols per year and number of years from table headers."""
    for t in tables:
        for row in t[:3]:
            # Find year columns (cells matching 20xx pattern)
            year_positions = [i for i, c in enumerate(row) if c and re.match(r'^20\d{2}$', str(c).strip())]
            if len(year_positions) >= 2:
                n_years = len(year_positions)
                # Distance between first two year positions gives cols per year
                cols_per_year = year_positions[1] - year_positions[0]
                return n_years, cols_per_year
    return None, None

def extract_code_table(pdf, pages_1idx, year, code):
    """Extract data for a specific code, returning list of dicts."""
    raw_rows = []
    n_years = None
    cols_per_year = None

    for p_1idx in pages_1idx:
        p_0idx = p_1idx - 1
        if p_0idx >= len(pdf.pages):
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
        print(f"    WARNING: Could not detect structure from headers for code {code}, row len={sample_len}")
        # Try to guess: for code 100 we have 4 cols/year, others 3
        cols_per_year = 4 if code == '100' else 3
        n_years = (sample_len - 1) // cols_per_year
        print(f"    Guessing: n_years={n_years}, cols_per_year={cols_per_year}")

    # Column indices for the LAST year
    # Structure: region(0), then n_years groups of cols_per_year
    last_group_start = 1 + (n_years - 1) * cols_per_year

    results = []
    for region, row in raw_rows:
        is_fo = is_fo_row(region)
        is_russia = (region == 'Российская Федерация')

        try:
            tested = clean_num(row[last_group_start])
            if code == '100':
                pct = clean_num(row[last_group_start + 1])
                hiv = clean_num(row[last_group_start + 2])
                rate = clean_num(row[last_group_start + 3])
            else:
                pct = None
                hiv = clean_num(row[last_group_start + 1])
                rate = clean_num(row[last_group_start + 2])
        except IndexError:
            print(f"    IndexError for region '{region}', code {code}, row len={len(row)}, expected up to col {last_group_start + cols_per_year - 1}")
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

for bnum, fpath, year, code_pages in BULLETINS:
    print(f"\n=== Bulletin {bnum} (year {year}) ===")
    with pdfplumber.open(fpath) as pdf:
        for code, pages in code_pages.items():
            print(f"  Code {code} (pages {pages}):")
            rows = extract_code_table(pdf, list(pages), year, code)
            print(f"    Got {len(rows)} rows")
            # Print RF row for verification
            rf = [r for r in rows if r['is_russia']]
            if rf:
                r = rf[0]
                print(f"    RF: tested={r['tested']}, hiv+={r['hiv_positive']}, rate={r['rate_per_100k_tested']}")
            all_rows.extend(rows)

df = pd.DataFrame(all_rows)
df.to_csv(f'{DATA_DIR}/hiv_codes_2018_2021.csv', index=False)

print(f"\n=== SUMMARY ===")
print(df.groupby(['year', 'code'])['region'].count().to_string())
print(f"\nTotal rows: {len(df)}")
print("Saved to hiv_codes_2018_2021.csv")
