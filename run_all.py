#!/usr/bin/env python3
"""
Replication pipeline: from raw data to all results and figures.

Military mobilisation and HIV transmission in Russia:
a difference-in-differences study.

Usage:
    cd hiv_mobilisation_replication/
    python run_all.py

Structure:
    raw_data/
        bulletins/      — Federal AIDS Centre PDF bulletins (nos 34–50)
        cbr/            — Central Bank regional deposit data (02_06_Dep_ind.xlsx)
        mediazona/      — Mediazona crowdsourced military fatalities
        census/         — 2021 census male working-age population
    scripts/            — All processing and analysis code
    output/             — Generated intermediate and final files (created by this script)
    paper/              — Manuscript and cover letter

Dependencies:
    pip install pandas numpy statsmodels scipy linearmodels pdfplumber openpyxl matplotlib
"""

import subprocess
import sys
import os
import shutil
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(ROOT, 'scripts')
RAW = os.path.join(ROOT, 'raw_data')
OUTPUT = os.path.join(ROOT, 'output')


def setup():
    """Create output dir and symlink raw data so scripts can find files."""
    os.makedirs(OUTPUT, exist_ok=True)

    # Scripts expect all files in one directory.
    # Create symlinks in output/ pointing to raw data and scripts.
    links = {
        # Bulletins
        **{f: os.path.join(RAW, 'bulletins', f)
           for f in os.listdir(os.path.join(RAW, 'bulletins')) if f.endswith('.pdf')},
        # CBR
        '02_06_Dep_ind.xlsx': os.path.join(RAW, 'cbr', '02_06_Dep_ind.xlsx'),
        # Mediazona
        'mediazona_200_by_region_year.csv': os.path.join(RAW, 'mediazona', 'mediazona_200_by_region_year.csv'),
        # Census
        'census2021_nMen16-615.csv': os.path.join(RAW, 'census', 'census2021_nMen16-615.csv'),
    }

    # Also link all scripts into output/ so imports work
    for f in os.listdir(SCRIPTS):
        if f.endswith('.py'):
            links[f] = os.path.join(SCRIPTS, f)

    for name, target in links.items():
        link_path = os.path.join(OUTPUT, name)
        if os.path.exists(link_path) or os.path.islink(link_path):
            os.remove(link_path)
        os.symlink(target, link_path)

    print(f"  Created {len(links)} symlinks in output/")


def run_step(description, script):
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}\n")

    script_path = os.path.join(OUTPUT, script)
    if not os.path.exists(script_path):
        print(f"  ERROR: {script} not found")
        return False

    t0 = time.time()
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True, cwd=OUTPUT
    )

    elapsed = time.time() - t0
    if result.stdout:
        lines = result.stdout.strip().split('\n')
        if len(lines) > 20:
            print(f"  ... ({len(lines)-20} lines omitted)")
        for line in lines[-20:]:
            print(f"  {line}")

    if result.returncode != 0:
        print(f"\n  FAILED (exit code {result.returncode}, {elapsed:.1f}s)")
        if result.stderr:
            for line in result.stderr.strip().split('\n')[-10:]:
                print(f"  STDERR: {line}")
        return False

    print(f"\n  OK ({elapsed:.1f}s)")
    return True


def check_raw_data():
    print("="*70)
    print("  Checking raw data")
    print("="*70)

    missing = 0
    bulletin_dir = os.path.join(RAW, 'bulletins')
    n_bulletins = len([f for f in os.listdir(bulletin_dir) if f.endswith('.pdf')])
    print(f"  Bulletins: {n_bulletins} PDFs")
    if n_bulletins < 16:
        print(f"  WARNING: expected 16+ bulletins, found {n_bulletins}")
        missing += 1

    for desc, path in [
        ('CBR deposits', os.path.join(RAW, 'cbr', '02_06_Dep_ind.xlsx')),
        ('Mediazona', os.path.join(RAW, 'mediazona', 'mediazona_200_by_region_year.csv')),
        ('Census', os.path.join(RAW, 'census', 'census2021_nMen16-615.csv')),
    ]:
        exists = os.path.exists(path)
        print(f"  [{('OK' if exists else 'MISSING'):>7}] {desc}")
        if not exists:
            missing += 1

    return missing == 0


def check_outputs():
    print(f"\n{'='*70}")
    print("  Verifying outputs")
    print("="*70)

    expected = [
        'hiv_codes_2009_2017.csv', 'hiv_codes_2018_2021.csv', 'hiv_codes_2022_2024.csv',
        'deposit_yoy_monthly.csv', 'deposit_yoy_annual.csv',
        'full_panel.csv', 'analysis_output.txt',
        'fig1_event_study.png', 'fig2_three_phases.png',
        'fig3_forest_plot.png', 'fig4_mechanism.png', 'figS1_scatter.png',
    ]

    all_ok = True
    for fname in expected:
        path = os.path.join(OUTPUT, fname)
        if os.path.exists(path) and not os.path.islink(path):
            size = os.path.getsize(path)
            print(f"  [     OK] {fname} ({size:,} bytes)")
        elif os.path.exists(path):
            print(f"  [SYMLINK] {fname} — not a generated file")
            all_ok = False
        else:
            print(f"  [MISSING] {fname}")
            all_ok = False

    return all_ok


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  REPLICATION PIPELINE")
    print("  Military mobilisation and HIV transmission in Russia")
    print("  Belov (2025)")
    print("="*70)

    t_start = time.time()

    check_raw_data()

    print(f"\n{'='*70}")
    print("  Setting up working directory")
    print("="*70)
    setup()

    steps = [
        ("Step 1/7: Extract HIV codes from bulletins 34-43 (2009-2017)",
         "extract_codes_2009_2017.py"),
        ("Step 2/7: Extract HIV codes from bulletins 44-47 (2018-2021)",
         "extract_codes_2018_2021.py"),
        ("Step 3/7: Extract HIV codes from bulletins 48-50 (2022-2024)",
         "extract_codes_2022_2024.py"),
        ("Step 4/7: Process CBR deposit data",
         "process_cbr_deposits.py"),
        ("Step 5/7: Build full panel",
         "build_full_panel.py"),
        ("Step 6/7: Run analysis",
         "analysisv2.py"),
        ("Step 7/7: Generate figures",
         "figures.py"),
    ]

    failed = []
    for desc, script in steps:
        ok = run_step(desc, script)
        if not ok:
            failed.append(script)
            print(f"\n  Pipeline stopped at {script}.")
            break

    if not failed:
        check_outputs()

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    if failed:
        print(f"  PIPELINE FAILED at: {', '.join(failed)}")
    else:
        print(f"  PIPELINE COMPLETE ({elapsed:.0f}s)")
        print(f"  All outputs in: {OUTPUT}/")
    print("="*70 + "\n")
