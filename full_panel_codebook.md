# full_panel.csv — Codebook

## Overview

Regional panel dataset on HIV testing and detection in Russia, 2009-2024.

-   **Unit of observation**: region x year
-   **Dimensions**: 1,360 rows = 85 regions x 16 years (2009-2024)
-   **Columns**: 86
-   **Source**: HIV bulletins (Informatsionnye byulleteni "VICH-infektsiya") published by the Federal Scientific and Methodological Center for AIDS Prevention and Control (FNMC SPID), bulletins No. 34-50
-   **Verification**: 54,434 individual values checked against source PDFs, 100.00% match rate

------------------------------------------------------------------------

## Panel Structure

| Dimension | Detail |
|----|----|
| Regions | 85 subjects of the Russian Federation |
| Years | 2009-2024 (16 years) |
| Region-years missing HIV data | 10 (Crimea + Sevastopol, 2009-2013 -- not part of RF) |

### Region Coverage Notes

-   **2009-2013**: 83 regions (Crimea and Sevastopol not yet incorporated into RF)
-   **2014-2024**: 85 regions (Crimea and Sevastopol added following 2014 annexation)
-   Defunct autonomous okrugs (Aginsky Buryatsky, Taimyrsky, Evenkiysky) that existed only in bulletin 34 (2009) are excluded -- their data is included in their parent regions (Zabaykalsky krai, Krasnoyarsky krai)
-   Tyumenskaya oblast is recorded as "Tyumenskaya oblast bez AO" (excluding Khanty-Mansiysk and Yamalo-Nenets autonomous okrugs, which appear as separate rows)

------------------------------------------------------------------------

## Identifier Variables

| Variable | Type | Description |
|----|----|----|
| `region` | string | Canonical name of the subject of the Russian Federation |
| `year` | int | Calendar year (2009-2024) |
| `regNameISO` | string | ISO 3166-2:RU region code (e.g., "SVE" for Sverdlovskaya oblast). Source: census2021_nMen16-615.csv |

------------------------------------------------------------------------

## HIV Testing Code Variables

Each code `cXXX` represents a testing category from Form No. 4 of Federal Statistical Observation ("Svedeniya o rezultatakh issledovaniya krovi na antitela k VICH"). For each code, three variables are provided:

-   `cXXX_tested` -- number of blood samples (serum specimens) tested for HIV antibodies
-   `cXXX_hiv_pos` -- number of newly identified HIV-positive individuals
-   `cXXX_rate` -- HIV detection rate per 100,000 tested (= hiv_pos / tested x 100,000)

### Codes Available 2009-2024 (12 codes, full time series)

| Code | Category (Russian) | Category (English) | Mean hiv_pos | Median hiv_pos | Max hiv_pos |
|----|----|----|----|----|----|
| **c100** | Граждане РФ | All tested Russian citizens (total) | 984.9 | 355.5 | 13,199 |
| **c102** | Потребители наркотиков | Injecting drug users (IDU) | 89.2 | 24.0 | 1,615 |
| **c103** | МСМ | Men who have sex with men (MSM) | 5.4 | 0.0 | 332 |
| **c104** | Больные ИППП | Patients with sexually transmitted infections (STI) | 44.0 | 11.0 | 947 |
| **c108** | Доноры | Blood/organ donors | 9.8 | 4.0 | 123 |
| **c109** | Беременные | Pregnant women (mandatory screening) | 59.8 | 20.0 | 663 |
| **c112** | Лица в местах лишения свободы | Persons in places of detention (prisoners) | 96.0 | 35.0 | 1,707 |
| **c113** | По клиническим показаниям | Clinical indications (symptomatic) | 304.0 | 118.0 | 6,002 |
| **c115** | Медицинские сотрудники | Healthcare workers in contact with HIV materials | 1.5 | 0.0 | 42 |
| **c118** | Прочие | Other/miscellaneous screening | 261.5 | 59.0 | 8,384 |
| **c120** | Эпидемиологическое расследование | Epidemiological investigation (contact tracing) | 91.9 | 37.0 | 1,507 |
| **c200** | Иностранные граждане | Foreign citizens | 31.4 | 11.0 | 1,498 |

**Missing values (10 per code)**: Crimea and Sevastopol for years 2009-2013. These regions were not part of the Russian Federation and therefore were not included in Russian HIV surveillance reports.

### Codes Available 2020-2024 (3 codes, introduced in bulletin 46)

| Code | Category (Russian) | Category (English) | Mean hiv_pos | Median hiv_pos | Max hiv_pos |
|----|----|----|----|----|----|
| **c111** | При постановке на воинский учет | Military conscription / enlistment screening | 8.5 | 2.0 | 130 |
| **c117** | Больные гепатитом В или С | Patients with hepatitis B or C diagnosis | 10.7 | 3.0 | 533 |
| **c125** | Аварийная ситуация (укол иглой) | Occupational needlestick / blood exposure incidents | 0.1 | 0.0 | 4 |

**Missing values (935 per code)**: These testing categories were not part of Form No. 4 before 2020. The codes were introduced when the form was revised to include finer-grained screening categories. Data for 2009-2019 does not exist.

### Codes Available 2022-2024 (7 codes, introduced in bulletin 48)

| Code | Category (Russian) | Category (English) | Mean hiv_pos | Median hiv_pos | Max hiv_pos |
|----|----|----|----|----|----|
| **c101** | Добровольное обследование | Voluntary testing (patient-initiated) | 77.2 | 21.0 | 968 |
| **c105** | Оказание сексуальных услуг | Sex workers | 0.5 | 0.0 | 29 |
| **c110** | Мужья/партнеры беременных | Husbands/partners of pregnant women registered | 6.1 | 3.0 | 67 |
| **c114** | Клинические проявления ВИЧ/СПИД | Clinical manifestations of HIV/AIDS (symptomatic) | 58.5 | 21.0 | 826 |
| **c116** | Обращение за медпомощью | Tested when seeking medical care | 274.5 | 147.0 | 2,448 |
| **c121** | Контактные лица при эпидрасследовании | Contacts identified during epidemiological investigation | 66.9 | 32.0 | 1,084 |
| **c124** | Дети от ВИЧ-инфицированных матерей | Children born to HIV-infected mothers | 31.5 | 2.0 | 517 |

**Missing values (1,105 per code)**: These testing categories were introduced in the 2022 revision of Form No. 4. Data for 2009-2021 does not exist.

------------------------------------------------------------------------

## Mediazona Military Casualties

Source: Mediazona (mediazona.io) independently verified list of Russian military deaths in the war in Ukraine. Data provided as `mediazona_200_by_region_year.csv` with regional attribution of confirmed casualties, 2022-2025.

| Variable | Type | Years | Missing | Description |
|----|----|----|----|----|
| `deaths_annual` | int | 2009-2024 | 0 | Military deaths attributed to the region in a given year. Zero for all pre-2022 years (no war). |
| `deaths_cum` | int | 2009-2024 | 0 | Cumulative military deaths since 2022 (running sum within region). Zero for pre-2022 years. |
| `deaths_annual_per100k` | float | 2009-2024 | 0 | `deaths_annual / nMen16_615_2021 * 100,000` |
| `deaths_cum_per100k` | float | 2009-2024 | 0 | `deaths_cum / nMen16_615_2021 * 100,000` |

### Descriptive Statistics (non-zero values only, 2022-2024)

| Variable           | Mean  | Std   | P25  | Median | P75   | Max     |
|--------------------|-------|-------|------|--------|-------|---------|
| deaths_annual      | 576.5 | 673.5 | 136  | 358    | 712   | 4,407   |
| deaths_cum_per100k | 224.5 | 205.3 | 82.9 | 164.1  | 297.3 | 1,303.8 |

**Note on measurement**: Mediazona counts represent a lower bound of actual casualties. They are based on confirmed reports (obituaries, social media, court records) and systematically undercount true losses. This attenuation bias pushes regression coefficients toward zero.

------------------------------------------------------------------------

## Population Denominator

| Variable | Type | Missing | Description |
|----|----|----|----|
| `nMen16_615_2021` | int | 0 | Male working-age population (16-61.5 years) from the 2021 Russian census. Used as denominator for per-capita casualty rates following the methodology of Bessudnov (2023, ruCasualtiesPublic). Time-invariant. |

### Descriptive Statistics

| Mean    | Std     | Min                | Median  | Max                |
|---------|---------|--------------------|---------|--------------------|
| 522,762 | 590,127 | 12,717 (Nenets AO) | 330,328 | 4,096,435 (Moscow) |

------------------------------------------------------------------------

## Bank Deposits (CBR)

Source: Central Bank of Russia regional banking statistics (Form 02_06_Dep_ind.xlsx). Methodology follows Solanko, L. (2024). "Where do Russia's mobilized soldiers come from? Evidence from bank deposits." BOFIT Policy Brief 1/2024.

| Variable | Type | Years | Missing | Description |
|----|----|----|----|----|
| `yoy_growth_mean` | float | 2012-2024 | 364 (26.8%) | Annual average of monthly year-on-year deposit growth rates. A region's 12-month rolling growth in total household bank deposits (ruble + foreign currency), averaged across months of the year. |
| `deposits_avg` | float | 2012-2024 | 281 (20.7%) | Average monthly total household deposits in the region (millions of rubles). |

**Missing values explained**: CBR deposit data starts in mid-2011; year-on-year growth requires 12 months of lagged data, so the first complete annual observation is 2012-2013. Missing values for 2009-2011 (and some of 2012) are structural.

### Descriptive Statistics (non-missing)

| Variable               | Mean    | Std       | Min   | Median  | Max        |
|------------------------|---------|-----------|-------|---------|------------|
| yoy_growth_mean        | 0.13    | 0.07      | -0.11 | 0.12    | 0.72       |
| deposits_avg (mln RUB) | 342,860 | 1,227,948 | 2,487 | 129,476 | 19,522,385 |

------------------------------------------------------------------------

## Computed/Derived Variables

| Variable | Type | Description |
|----|----|----|
| `post` | int (0/1) | = 1 if year \>= 2022 (post-invasion indicator for DiD) |
| `hiv_available` | bool | = True if `c100_hiv_pos` is not missing for this row |
| `log_c100_rate` | float | ln(1 + c100_rate) |
| `log_c109_rate` | float | ln(1 + c109_rate) |
| `log_c100_hiv_pos` | float | ln(1 + c100_hiv_pos) |
| `log_c109_hiv_pos` | float | ln(1 + c109_hiv_pos) |
| `log_c111_hiv_pos` | float | ln(1 + c111_hiv_pos) |
| `log_c112_rate` | float | ln(1 + c112_rate) |
| `log_deaths_cum_per100k` | float | ln(1 + deaths_cum_per100k) |
| `log_deaths_annual_per100k` | float | ln(1 + deaths_annual_per100k) |

------------------------------------------------------------------------

## Data Provenance

### HIV Testing Data

Extracted from PDF bulletins using `pdfplumber`. Each bulletin contains multi-year regional tables for each testing code. The extraction pipeline:

1.  `extract_codes_2009_2017.py` -- bulletins 34-43 (9 bulletins, 12 codes)
2.  `extract_codes_2018_2021.py` -- bulletins 44-47 (4 bulletins, 12-15 codes)
3.  `extract_codes_2022_2024.py` -- bulletins 48-50 (3 bulletins, 22 codes)
4.  `normalize_regions.py` -- canonical region name normalization
5.  `build_full_panel.py` -- assembly into region x year panel

**Special case -- 2014**: Bulletin 40 is a scanned PDF (36 MB, image-only) that pdfplumber cannot read. Data for 2014 is extracted from bulletin 41 (which contains 2014-2015 two-year tables) using the first-year columns. Values may reflect minor revisions relative to the original bulletin 40.

### Bulletin-to-Year Mapping

| Bulletin    | Year extracted | \# Codes | Pages per code |
|-------------|----------------|----------|----------------|
| 34          | 2009           | 12       | 2              |
| 35          | 2010           | 12       | 2              |
| 36          | 2011           | 12       | 2              |
| 38          | 2012           | 12       | 2              |
| 39          | 2013           | 12       | 2              |
| 41 (1st yr) | 2014           | 12       | 2              |
| 41 (2nd yr) | 2015           | 12       | 2              |
| 42          | 2016           | 12       | 2              |
| 43          | 2017           | 12       | 2              |
| 44          | 2018           | 12       | 2              |
| 45          | 2019           | 12       | 2              |
| 46          | 2020           | 15       | 2              |
| 47          | 2021           | 15       | 2              |
| 48          | 2022           | 22       | 2              |
| 49          | 2023           | 22       | 2              |
| 50          | 2024           | 22       | 2              |

### Bulletins Not Used

| Bulletin | Year | Reason |
|----|----|----|
| 30 | 2006 | Old format, no regional code tables |
| 31 | 2007 | Old format, no regional code tables |
| 33 | 2008 | Old format, no regional code tables |
| 40 | 2014 | Scanned PDF (image-only), pdfplumber cannot extract. Data sourced from bulletin 41 instead. |

------------------------------------------------------------------------

## Known Data Quality Issues

1.  **Republica Altay, 2016, c112**: `tested=1, hiv_pos=6, rate=600,000`. This is a data entry error in the original bulletin -- HIV-positive count exceeds tested count. Retained as-is from source.

2.  **Six rows across codes 103 and 112** where `tested=0` but `hiv_pos > 0` (typically hiv_pos=1). These reflect cases counted through alternative reporting channels. Rate is undefined (NaN) for these rows.

3.  **Code c103 (MSM)**: Very small sample sizes in most regions (median tested=7). Rates are extremely volatile and should not be interpreted as prevalence. Many regions report zero tested.

4.  **Code c105 (sex workers)**: Available only 2022-2024 with very small samples (median tested=1). Most regions report zero.

5.  **Code c125 (needlestick)**: Median hiv_pos=0 across all region-years. This code captures occupational exposure incidents, which rarely result in HIV transmission.
