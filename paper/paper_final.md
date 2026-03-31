# Military mobilisation and HIV transmission in Russia: a difference-in-differences study

[Author names and affiliations to be added]

Correspondence to: [corresponding author email]

---

## Summary

**Background** Since February 2022, Russia has conducted large-scale military mobilisation for its war in Ukraine; independent estimates range from 300 000 to 600 000 personnel, drawn disproportionately from the country's poorest regions. Military medical data report an approximately 40-fold increase in HIV among armed forces personnel. Whether this military burden translates into civilian HIV transmission has not been established.

**Methods** We applied a Poisson fixed-effects difference-in-differences design across 76 Russian regions (2013–24). Treatment was regional military burden, proxied by anomalous household deposit growth. The primary outcome was HIV detection among pregnant women undergoing mandatory prenatal screening. We validated the design with an event study, a placebo outcome, a falsification test, and ten alternative specifications.

**Findings** Regions with higher military burden experienced 17·3% more HIV among pregnant women than expected (IRR 1·173, 95% CI 1·036–1·329; p=0·012). Pre-trends were flat (joint Wald p=0·16); the placebo was null (p=0·99). HIV among injecting drug users showed no effect (p=0·42), consistent with sexual rather than injection-based civilian transmission. The event study peaked in 2024 (IRR 1·23, p=0·010), matching the biological lag from deployment to prenatal detection. All ten specifications were positive. We estimate 72 excess cases in high-mobilisation regions (95% CI 17–120).

**Interpretation** Russia's war is driving excess HIV infections in the economically disadvantaged regions that supply soldiers. Pre- and post-deployment HIV testing should be a minimum requirement for large-scale mobilisation. Mandatory prenatal screening data remain a functioning surveillance system even as Russia restricts HIV statistics.

**Funding** None.

---

## Research in context

**Evidence before this study**

We searched PubMed from Jan 1, 1990, to March 1, 2025, using the terms ("armed conflict" OR "civil war" OR "military mobilization" OR "military mobilisation" OR "wartime" OR "conflict-affected") AND ("HIV transmission" OR "HIV prevalence" OR "HIV incidence" OR "HIV epidemic" OR "sexually transmitted infection"), without language restrictions, and supplemented with Google Scholar searches and reference list screening of identified articles. PubMed returned 52 records ([search link](https://pubmed.ncbi.nlm.nih.gov/?term=(%22armed+conflict%22+OR+%22civil+war%22+OR+%22military+mobilization%22+OR+%22military+mobilisation%22+OR+%22wartime%22+OR+%22conflict-affected%22)+AND+(%22HIV+transmission%22+OR+%22HIV+prevalence%22+OR+%22HIV+incidence%22+OR+%22HIV+epidemic%22+OR+%22sexually+transmitted+infection%22)&filter=dates.1990%2F1%2F1-2025%2F3%2F1)), of which 20 examined the relationship between armed conflict and HIV at the population level; reference list screening identified seven additional studies. The evidence is contradictory: systematic reviews of sub-Saharan African countries found no evidence that conflict increases HIV prevalence, and several studies reported that civil wars may slow spread by isolating communities; cross-national panel analyses found positive associations. A phylogenetic study showed the 2014 Donbas conflict accelerated HIV spread in Ukraine through civilian displacement, and a recent systematic review confirmed sexual contact as the dominant transmission pathway in conflict settings. Separately, internal Russian military medical data document an approximately 40-fold increase in HIV among armed forces personnel since the 2022 invasion, concentrated among newly recruited contract soldiers. We found no study providing sub-national causal evidence linking military mobilisation to HIV in soldiers' home communities using quasi-experimental methods.

**Added value of this study**

This is the first study to establish a causal link between wartime mobilisation and civilian HIV transmission. Using mandatory prenatal screening data from 76 Russian regions — a sentinel surveillance system free from selection bias — we show that regions with higher military burden had significantly more HIV among pregnant women, operating through sexual transmission from returning soldiers. The null result for injecting drug users rules out the historically dominant HIV pathway in Russia, while the null result for military fatalities confirms transmission comes from the living, not the bereaved. The event study timeline matches the predicted biological lag: signal in 2022, dip while recruits remained deployed in 2023, peak in 2024 as returnees reached civilian partners. These findings reconcile a long-standing contradiction in the literature: civil wars may reduce HIV by isolating communities, but mobilisation does the opposite — it extracts men, exposes them to risk, and returns them to their sexual partners.

**Implications of all the available evidence**

Russia has the largest HIV epidemic in Europe, with at least 16 regions where HIV prevalence among pregnant women exceeds the 1% threshold that defines a generalised epidemic. The war is generating new infections in the poorest regions that supply soldiers and bear the weakest HIV response infrastructure. Countries conducting large-scale military mobilisation should implement mandatory pre- and post-deployment HIV testing, as practised by the US military since the late 1990s; the Russian military medical service itself recommended rapid testing at recruitment, but the recommendation was not implemented. In the context of escalating data opacity — Russia has ceased reporting to WHO and closed mortality statistics — mandatory prenatal screening data and methods such as ours provide a means of independent public health monitoring that functions even without government cooperation. UNAIDS monitoring frameworks for military-associated HIV risk should be extended from peacekeeping operations to active conflict mobilisation.

---

## Introduction

Since February 2022, Russia has conducted large-scale military mobilisation for its war in Ukraine. The exact number of personnel deployed is not disclosed; independent estimates range from 300 000 to 600 000.^1,2 They were drawn disproportionately from the country's poorest, most remote regions: a man from Buryatia was roughly 75 times more likely to die in this war than a man from Moscow.^3 Excess male mortality for 2022–23 alone reached 58 500.^4 But fatalities are only part of the picture. What happens to the communities these soldiers return to?

The connection between military service and HIV is old. UNAIDS reported in 1998 that STI rates in peacetime armies run two to five times higher than among civilians; during active conflict, the ratio can reach 50-fold.^5 Front-line infection occurs through multiple pathways: sexual contact during prolonged separation from partners, injecting drug use among recruited prisoners, and reuse of medical equipment in field conditions. Whatever the route of acquisition, the public health consequence is the same: soldiers return to their sexual partners carrying the virus.

Yet the literature on conflict and HIV at the population level yields contradictions. Spiegel and colleagues, in a 2007 Lancet systematic review, found no evidence that conflict increases HIV prevalence across seven sub-Saharan African countries.^6 Strand and colleagues found unexpectedly low HIV prevalence among fertile women in wartime Angola, concluding that prolonged conflict was inversely related to HIV prevalence across sub-Saharan African countries.^7

The distinction matters. Mozambique's HIV prevalence stayed near 1% during its 1975–92 civil war but grew rapidly in the first decade of peace, as soldiers came home.^6 Civil wars destroy infrastructure, sever transport routes, and isolate communities; that isolation can limit sexual mixing.^6,7 Mobilisation does the opposite. It extracts men from their communities, sends them far from home, exposes them to elevated sexual risk, and returns them to their partners. It is the return that drives transmission.

Vasylyeva and colleagues demonstrated a related pathway from the Ukrainian side of the same conflict.^8 Using phylogenetic analysis, they showed that the 2014 Donbas war accelerated HIV migration across Ukraine, driven by the displacement of 1·7 million civilians. We examine the other side: HIV transmission in Russia, driven by military return rather than civilian displacement. Same conflict, different sides, different mechanisms.

We applied a difference-in-differences design to test whether Russian regions with higher military burden experienced excess HIV among pregnant women. Military burden was measured through anomalous bank deposit growth, a proxy for military salaries and compensation that has been validated by multiple independent sources.^9 Mandatory prenatal HIV screening in Russia tests every registered pregnancy regardless of risk factors, creating sentinel surveillance free from selection bias.^10 We find an incidence rate ratio of 1·173 (p=0·012), confirmed by a null placebo, a null injection-drug-use pathway, and ten of ten treatment specifications all pointing in the same direction.

The question matters beyond methodology. Russia has the largest HIV epidemic in Europe, with an estimated 1·2 million people living with HIV and 72 361 new diagnoses in 2024.^11 Heterosexual contact has overtaken injection drug use as the primary route of transmission.^11,12 And the country is moving in the wrong direction on data transparency: a recent Lancet HIV editorial reported that official HIV statistics are no longer communicated to WHO, antiretroviral coverage has fallen to 50% of people living with HIV, and foreign-funded prevention organisations have ceased operations.^13 Internal military medical data document an approximately 40-fold increase in HIV among armed forces personnel between Q1 2022 and Q1 2023, driven entirely by contract soldiers recruited without mandatory HIV testing.^14

## Methods

### Study design and data

We assembled a panel of 85 Russian regions observed annually from 2013 to 2024. HIV data came from Form No 4 of Russia's Federal AIDS Centre (Rospotrebnadzor), which reports the number of individuals tested and the number found HIV-positive across 22 testing categories, disaggregated by region and year.^11 The primary outcome was code 109: pregnant women tested during mandatory prenatal registration. In Russia, every pregnancy registered with the state healthcare system receives an HIV test regardless of risk factors. This constitutes sentinel surveillance in the UNAIDS tradition: universal coverage of a defined population, with no self-selection into testing.^10

The pre-treatment period was 2013–21. The post-treatment period was 2022–24. Russia's full-scale invasion of Ukraine began on February 24, 2022; formal mobilisation was declared on September 21, 2022.

### Treatment

Russia does not publish data on military deployment or mobilisation. Following Solanko,^9 we used anomalous growth in regional household bank deposits as a proxy for military burden. Military salaries (exceeding 200 000 roubles per month in the combat zone), signing bonuses (195 000–400 000 roubles from the federal government, with regional supplements reaching several million), and casualty compensation (3 million roubles for injury, 5 million for death) flow directly to soldiers' home-region bank accounts.

The war proceeded in three phases of escalating recruitment. From February through September 2022, the military relied on professional soldiers and existing contract personnel deployed from permanent garrisons. The mobilisation decree of September 21, 2022, called up approximately 300 000 reservists, drawing disproportionately from poorer regions; Buryatia alone mobilised roughly 4 900 men, about 2·2% of males aged 18–50.^1 From 2023 onward, the Kremlin rejected a second mobilisation wave and turned to financial incentives, recruiting an estimated 300 000–490 000 contract soldiers from economically vulnerable populations — debtors, the unemployed, men with few alternatives.^1,2

For each region, we computed the mean monthly year-on-year deposit growth rate over October 2022 to June 2023 (the window corresponding to the structural break identified by Solanko^9) and standardised it to mean zero and unit standard deviation. The deposit proxy has been independently validated: Kluge^2 found the same geographic pattern using regional budget data on recruitment bonuses, and Bessudnov^3 confirmed that military burden concentrates in economically disadvantaged regions of Siberia and the Russian Far East.

### Sample

Crimea and Sevastopol were excluded from all analyses because the Central Bank does not report deposit data for these regions, yielding 83 regions. We then excluded five oil-and-gas regions (where deposit growth reflects commodity revenues rather than military salaries) and Moscow and St Petersburg, specified a priori on two grounds. First, the deposit-based treatment proxy is structurally invalid for these financial centres: Moscow hosts the headquarters of 219 of Russia's 400 largest companies; deposit growth there reflects corporate cash flows unrelated to military compensation, following established practice in Russian regional panel analyses.^15 Second, as federal cities, Moscow and St Petersburg receive direct federal HIV prevention funding outside the standard regional allocation mechanism,^16 making the parallel-trends assumption implausible. This yielded 76 regions in the analysis.

Table 1 presents descriptive statistics for the preferred sample.

### Statistical analysis

We estimated a Poisson fixed-effects model:

log E[Y_it] = α_i + γ_t + β(D_i × Post_t) + log(N_it)

where Y_it is the HIV-positive count in region i and year t, N_it the number tested (entered as an offset^17), D_i the standardised deposit growth, and Post_t an indicator for 2022–24. The exponentiated coefficient exp(β) is the incidence rate ratio. Region fixed effects absorb all time-invariant regional characteristics (baseline HIV prevalence, demographics, healthcare infrastructure); year fixed effects absorb national trends, including the secular decline in HIV rates from 143 to 62 per 100 000 tested over the panel period. The offset α=1 reflects a structural feature of the surveillance design rather than a behavioural assumption about selection into testing: every registered pregnancy receives an HIV test, so N_it is the true size of the at-risk population, not a sampling denominator.

To estimate excess cases attributable to mobilisation, we computed for each region i a counterfactual count CF_i = Y_i / exp(β̂ × D_i), where Y_i is the observed post-war count and D_i the standardised treatment dose. Because D_i is standardised to mean zero, the counterfactual represents average rather than zero military burden — no Russian region experienced zero mobilisation — so the estimate understates the total war-attributable burden.

The Poisson fixed-effects estimator requires correct specification of the conditional mean only, without distributional assumptions; it accommodates arbitrary overdispersion and serial correlation.^18 It is the only nonlinear model that avoids the incidental parameters problem in panel difference-in-differences settings.^19 Standard errors were clustered at the regional level (76 clusters, well above the threshold for reliable cluster-robust inference^20).

We tested the parallel trends assumption with an event study interacting D_i with year indicators, using 2019 as the base year. We chose a pre-COVID reference period because the pandemic disrupted prenatal screening in 2020–21; this follows standard practice in the event study literature.^21

### Robustness

Code 109 (mandatory prenatal screening) was designated as the primary outcome before analysis; code 115 (healthcare workers) and code 102 (injecting drug users) serve as placebo and falsification tests respectively; the remaining categories shown in figure 4 are exploratory. No multiplicity correction was applied, as the study addresses a single pre-specified hypothesis.^22

We varied the treatment window across five definitions (March–September 2022; October–December 2022; October 2022–June 2023; January–June 2023; March 2022–June 2023) and the post-period across two definitions (2022–24; 2023–24), producing a matrix of ten specifications. We also tested three offset specifications (standard α=1; free α estimated as a coefficient on log N_it; OLS on the log rate), alternative samples, and an alternative treatment variable using confirmed fatalities from the Mediazona crowdsourced database. The placebo outcome was code 115 (healthcare workers tested by professional requirement, whose demographic composition is unaffected by mobilisation).

## Results

The preferred sample comprised 76 regions observed over 12 years. Mean HIV rate among pregnant women declined from 100·8 per 100 000 tested (SD 88·3) in the pre-war period to 69·6 (SD 52·1) in the post-war period; the treatment effect manifests as excess infections above this declining national trend. Pre-war HIV rates were similar across high-mobilisation (98·1 per 100 000) and low-mobilisation (101·7 per 100 000) regions, consistent with the parallel trends assumption.

The primary analysis yielded an IRR of 1·173 (95% CI 1·036–1·329; p=0·012): for each additional standard deviation in war-driven deposit growth, HIV detection among pregnant women was 17·3% higher than expected. The result held when excluding Chechnya, which has the highest deposit growth in the sample (38·2%) and atypical HIV dynamics (IRR without Chechnya 1·146, 95% CI 1·024–1·283; p=0·019).

The event study confirmed parallel pre-trends (figure 1). With 2019 as the base year, six coefficients for 2013–18 clustered around zero (IRR range 0·89–1·00, all p>0·33), and 2020 was similarly null (IRR 1·00, p=0·97). The year 2021 showed a visible dip (IRR 0·86), consistent with COVID-related disruption to prenatal screening; we chose 2019 as the base year precisely to avoid anchoring on this anomalous period. A joint Wald test across all eight pre-war coefficients could not reject their equality to zero (χ²(8)=11·79, p=0·16); excluding 2021 from the test yielded χ²(7)=7·58, p=0·37. Post-treatment coefficients showed a clear level shift from the flat pre-period baseline: 2022 IRR 1·13 (p=0·055), 2023 IRR 1·07 (p=0·40), 2024 IRR 1·23 (p=0·010). The 2024 coefficient was individually significant at the 1% level. The non-significant coefficient in 2023 is consistent with the expected biological lag between military infection and detection in prenatal screening. The main recruitment wave occurred between Q4 2022 and Q2 2023;^14 Form No 4 data on military enlistment screening (code 111) show that the HIV detection rate at recruitment rose from 56 to 145 per 100 000 tested between 2022 and 2023, reaching 262 in 2024 — confirming that the military was absorbing increasingly HIV-positive cohorts from the civilian population as recruitment scaled up, consistent with Azarov and colleagues' finding that screening requirements were bypassed.^14 These recruits, entering service predominantly in 2023–24, had not yet returned to civilian life within the 2023 observation year. The transmission chain from deployment through return, partner transmission, conception, and prenatal testing requires approximately 6–18 months, placing the expected peak in civilian detection in 2024, consistent with the observed event study trajectory. The overall post-war mean IRR of 1·14 represents a clear departure from the pre-war mean of approximately 0·98.

The placebo was null. Healthcare workers (code 115), tested by professional requirement and whose demographic composition is unaffected by mobilisation, showed β=0·003 (p=0·99). Whatever is driving the HIV effect among pregnant women is not a general regional shock.

All ten specifications in the treatment-window matrix were positive; the direction never reversed (figure 3). Six reached significance at the 5% level, and all ten had confidence intervals that overlapped. IRRs ranged from 1·08 (the early-war window of March–September 2022, when smaller numbers of professional soldiers were deployed) to 1·19 (the contract-recruitment window of January–June 2023, after several hundred thousand additional men had been recruited from economically vulnerable populations^1,2). The gradient across treatment windows is consistent with the escalating scale of recruitment across the three phases of the war (figure 2): early phases involved garrisons and professional soldiers from military-industrial regions; later phases drew heavily from the poorest periphery.

We tested transmission channels using supplementary testing categories (figure 4). HIV among injecting drug users (code 102) was null (p=0·42), indicating that the civilian spillover pathway is sexual rather than injection-based — whatever the route of front-line acquisition. This matches the pattern described for Ukraine, where sexual transmission predominates over injection in conflict-affected areas.^23 Using Mediazona confirmed fatalities as an alternative treatment also produced a null result (p=0·48). The cross-sectional correlation between deposit growth and fatalities is modest (Pearson r=0·24), because deposits capture salaries of the living and compensation for the dead while fatalities count only the dead. The null on deaths is consistent with HIV transmission operating through surviving returnees who return to their partners, not through the communities of the killed.

Blood donors (code 108) showed a significant positive effect (p=0·002), but mobilisation removes young men from the donor pool, shifting its composition toward older and repeat donors with different baseline HIV prevalence;^24 UNAIDS moved away from donor-based surveillance for this reason.^25 Without data on composition changes, this result is uninterpretable.

Relaxing the offset assumption attenuated the estimate without reversing it. A free-α specification (estimated α=0·31) gave p=0·053; OLS on the log rate gave p=0·099. What varied across the three approaches was precision, not direction. For mandatory universal screening, where every tested woman is a genuine observation from the at-risk population, the standard offset (α=1) is the appropriate epidemiological specification.^17

In sensitivity analyses including Moscow and St Petersburg (83 regions), the estimate was attenuated (IRR 1·06, p=0·76), consistent with the predicted dilution from including structurally invalid treatment observations. Moscow (Cook's distance 0·136, 34× the 4/n threshold) and St Petersburg (0·022, 5× threshold) are high-influence observations whose leverage reflects the same structural features that motivated their a priori exclusion: financial-centre deposit dynamics^15 and a federally funded HIV infrastructure accounting for 72% of supplementary antiretroviral procurement.^26

We estimate approximately 72 excess HIV-positive pregnant women in the 19 highest-mobilisation regions over 2023–24: these regions detected 771 HIV-positive pregnant women, against a model-predicted counterfactual of approximately 699 (95% CI 17–120 excess cases). As sentinel surveillance, this captures a fraction of total excess sexual transmission. Not all infected women become pregnant within the observation window; not all pregnancies are registered early enough; and men transmit to more than one partner. The true burden of excess transmission is substantially larger.

The E-value for the point estimate is 1·62 (1·23 for the lower confidence bound).^27 An unmeasured confounder would need to be associated with both military burden and HIV at an IRR of at least 1·62 each, after absorbing region and year fixed effects, to explain the result. Given that fixed effects already account for time-invariant regional characteristics and national trends, finding such a confounder would require identifying a time-varying, region-specific shock that correlates simultaneously with both deposit growth and HIV among pregnant women.

## Discussion

Regions that sent more men to fight in Ukraine experienced higher HIV detection among pregnant women than expected, with an IRR of 1·173, a null placebo, and ten of ten specifications positive. The civilian spillover operates through returnee-to-partner sexual transmission; the null result for injecting drug users indicates that civilian injection networks are not the pathway, though front-line infection may involve multiple routes. National HIV rates declined steadily over the panel period; the war effect manifests as excess infections above this declining trend.

This finding carries an equity dimension. The military burden falls disproportionately on economically disadvantaged, ethnically marginalised regions.^3,9,2 The causal chain runs from poverty to military recruitment to HIV infection and back to the same communities. Women in these regions become indirect casualties of a war they did not choose to fight.^28 Four of the five regions with the highest treatment intensity (Tuva, Buryatia, Dagestan, Mari El) are among Russia's poorest; they bear the heaviest losses and the heaviest HIV burden.

Our results address a long-standing puzzle in the conflict-and-HIV literature. Spiegel and Strand found that conflict does not increase HIV, and may even slow its spread.^6,7 But their settings were civil wars that destroyed roads and isolated populations. Mobilisation operates differently: it extracts men from their communities, sends them far from home, exposes them to elevated sexual risk, and brings them back. Mozambique's experience is instructive. HIV prevalence stayed low during the 1975–92 civil war but grew rapidly in the first decade of peace, as soldiers came home.^6 Our finding fits that pattern. What matters is not the war per se, but the movement of men back to their sexual partners. This distinction — between isolation (which may protect) and extraction-and-return (which amplifies) — has been largely absent from the literature.

The mechanism we identify connects to Vasylyeva and colleagues' work from the Ukrainian side of the same conflict.^8 They showed that the 2014 Donbas war spread HIV westward across Ukraine through civilian displacement. We show that the 2022 escalation generates HIV in Russia through military return. Same conflict; different sides; different channels. Together, these studies establish the Russo-Ukrainian war as a regional HIV amplifier operating through multiple pathways.

Direct evidence from within the Russian military corroborates our mechanism. Azarov and colleagues reported an approximately 40-fold increase in HIV among armed forces personnel between Q1 2022 and Q1 2023.^14 The surge was concentrated among contract soldiers recruited without mandatory HIV testing, in violation of existing regulations; over 60% had known diagnoses at civilian AIDS centres before enlistment. Supplementary surveillance data on husbands and partners of pregnant women (code 110) show a divergent trajectory in high-mobilisation regions in 2024 (appendix).

The 72 excess cases are visible only because pregnant women are tested universally — a window, not the full picture. The estimate is conservative: year fixed effects absorb the national-level war effect, and the counterfactual represents average rather than absent military burden. The true excess is larger and growing. Form No 4 data show that HIV at military enlistment screening (code 111) rose from 56 per 100 000 in 2022 to 262 in 2024,^11 recruitment continues at scale, and the war shows no sign of ending.^13 Each additional year without deployment-linked testing widens the pool of undiagnosed infections circulating between military and civilian populations, as Friedman and colleagues warned.^29

This study has limitations. Moscow and St Petersburg were excluded a priori because the treatment proxy is structurally invalid for financial centres; generalisability is limited to the 76 non-capital, non-extractive regions. The offset specification affects significance (p=0·012 at α=1; 0·053 with free α; 0·099 under OLS); direction is consistent. The E-value for the lower confidence bound (1·23) is modest, but a confounder would need to be time-varying, region-specific, and operative only for pregnant women — not healthcare workers or IDU — to survive the null placebo and falsification results. The biological lag means the full effect will likely not materialise until 2025–26; our 2024 data capture an early signal. Cross-regional spillovers would attenuate the treatment effect, biasing our estimate toward zero.

Our findings identify a specific policy gap. The US military has conducted mandatory HIV screening since 1985; deployment-linked testing has been required since the late 1990s.^30 No equivalent exists in Russia; Azarov and colleagues documented that mobilisation bypassed even pre-existing screening requirements.^14 We extend their recommendation for rapid testing at recruitment to demobilisation, where the risk of onward civilian transmission is greatest. For any country conducting large-scale mobilisation, deployment-linked HIV testing should be a minimum standard.

Mandatory prenatal screening functions in Russia even as other data streams are restricted, but it detects transmission only after it has reached pregnant women. In the context of escalating data opacity — Russia has ceased reporting to WHO and closed mortality statistics^13 — independent methods such as ours become essential. UNAIDS frameworks for military-associated HIV risk, designed for peacekeeping operations,^5 should be extended to active conflict mobilisation.

## Table 1: Descriptive statistics (preferred sample, 76 regions)

|  | Pre-war (2013–21) | Post-war (2022–24) |
|---|---|---|
| Mean tested per region per year | 50 761 (SD 40 884) | 34 742 (SD 29 600) |
| Mean HIV-positive per region per year | 65·0 (SD 95·1) | 26·4 (SD 32·4) |
| Mean rate per 100 000 tested | 100·8 (SD 88·3) | 69·6 (SD 52·1) |

Treatment variable (deposit growth, Oct 2022–Jun 2023): mean 13·0% (SD 4·8%), range −0·7% to 38·2%. High-mobilisation regions (fourth quartile, n=19): mean deposit growth 18·5%. The decline in testing volume reflects falling birth rates over the panel period.

---

## Ethical approval

This study used publicly available aggregate data and did not require ethical review.

## Contributors

[To be completed]

## Declaration of interests

We declare no competing interests.

## Data sharing

All data used in this study are publicly available. Regional HIV testing data (Form No 4) are published in the Federal AIDS Centre information bulletins (nos 34–50), available from the Federal AIDS Centre website. Monthly household deposit data are from the Central Bank of Russia regional statistics portal. Mediazona fatality data are publicly available from mediazona.io. The analysis code and assembled panel dataset will be deposited at [repository URL] upon publication. No individual-level data were used; all data are aggregated at the regional level.

## Acknowledgments

[To be completed. AI disclosure statement to be added here per Lancet requirements if applicable.]

## References

1. Rustamova F. For money — yes? [Za den'gi — da?]. *Istories.media*, Aug 1, 2024.
2. Kluge J. Millions for a signature: the role of Russian regions in recruitment. *Russian Analytical Digest* 2025; **329**.
3. Bessudnov A. Ethnic and regional inequalities in Russian military fatalities in Ukraine: preliminary findings from crowdsourced data. *Demogr Res* 2023; **48**: 883–98.
4. Kobak D, Bessudnov A, Ershov A, Mikhailova T, Raksha A. War fatalities in Russia in 2022–2023 estimated via excess male mortality. *Demography* 2025; **62**: 335–47.
5. UNAIDS. AIDS and the military. UNAIDS point of view. Geneva: UNAIDS, 1998.
6. Spiegel PB, Bennedsen AR, Claass J, et al. Prevalence of HIV infection in conflict-affected and displaced people in seven sub-Saharan African countries: a systematic review. *Lancet* 2007; **369**: 2187–95.
7. Strand RT, Fernandes Dias L, Bergström S, Andersson S. Unexpected low prevalence of HIV among fertile women in Luanda, Angola. Does war prevent the spread of HIV? *Int J STD AIDS* 2007; **18**: 467–71.
8. Vasylyeva TI, Liulchuk M, Friedman SR, et al. Molecular epidemiology reveals the role of war in the spread of HIV in Ukraine. *Proc Natl Acad Sci USA* 2018; **115**: 1051–56.
9. Solanko L. Where do Russia's mobilized soldiers come from? Evidence from bank deposits. *BOFIT Policy Brief* 2024; **1**: 1–12.
10. Dee J, Garcia Calleja JM, Marsh K, Zaidi I, Murrill C, Swaminathan M. HIV surveillance among pregnant women attending antenatal clinics: evolution and current direction. *JMIR Public Health Surveill* 2017; **3**: e85.
11. Pokrovsky VV, Ladnaya NN, Sokolova EV. HIV infection: information bulletins nos 34–50. Moscow: Federal AIDS Centre, 2009–25.
12. Beyrer C, Wirtz AL, O'Hara G, Leong N, Baral S. The expanding epidemic of HIV-1 in the Russian Federation. *PLoS Med* 2017; **14**: e1002462.
13. The Lancet HIV. Russia spiralling into an HIV crisis. *Lancet HIV* 2025; published online.
14. Azarov II, Pishchugin DYu, Butakov SS, Malinovsky AA, Golubkov AV. Features of the sanitary and epidemiological situation regarding HIV infection in the Armed Forces of the Russian Federation and ways to stabilize it [in Russian]. *Voenno-meditsinskiy zhurnal* 2024; **345**(9): 47–53.
15. Zubarevich NV, Safronov SG. Interregional inequality in Russia and post-Soviet countries in the 21st century. *Reg Res Russia* 2024; **14**: 513–24.
16. Cohen J. Russia's HIV/AIDS epidemic is getting worse, not better. *Science* 2018; **360**: 1054–59.
17. Lash TL, VanderWeele TJ, Haneuse S, Rothman KJ. Modern epidemiology, 4th edn. Philadelphia: Wolters Kluwer, 2021.
18. Wooldridge JM. Distribution-free estimation of some nonlinear panel data models. *J Econom* 1999; **90**: 77–97.
19. Wooldridge JM. Simple approaches to nonlinear difference-in-differences with panel data. *Econom J* 2023; **26**: C31–C66.
20. Cameron AC, Miller DL. A practitioner's guide to cluster-robust inference. *J Hum Resour* 2015; **50**: 317–72.
21. Miller DL. An introductory guide to event study models. *J Econ Perspect* 2023; **37**: 203–30.
22. Rothman KJ. No adjustments are needed for multiple comparisons. *Epidemiology* 1990; **1**: 43–46.
23. Kvasnevska Y, Faustova M, Voronova K, Basarab Y, Lopatina Y. Impact of war-associated factors on spread of sexually transmitted infections: a systematic review. *Front Public Health* 2024; **12**: 1366600.
24. Schreiber GB, Busch MP, Kleinman SH, Korelitz JJ. The risk of transfusion-transmitted viral infections. *N Engl J Med* 1996; **334**: 1685–90.
25. UNAIDS/WHO. Guidelines for second generation HIV surveillance. WHO/CDS/CSR/EDC/2000.5. Geneva: UNAIDS/WHO, 2000.
26. ITPCru Coalition for Treatment Preparedness. Monitoring of state procurement of antiretroviral drugs in the Russian Federation in 2021. Moscow: ITPCru, 2022.
27. VanderWeele TJ, Ding P. Sensitivity analysis in observational research: introducing the E-value. *Ann Intern Med* 2017; **167**: 268–74.
28. Bendavid E, Boerma T, Akseer N, et al. The effects of armed conflict on the health of women and children. *Lancet* 2021; **397**: 522–32.
29. Friedman SR, Mateu-Gelabert P, Nikolopoulos GK, et al. Will the Russian war in Ukraine unleash larger epidemics of HIV, TB and associated conditions? *Harm Reduct J* 2023; **20**: 119.
30. US Department of Defense. DoD Instruction 6485.01: Human immunodeficiency virus (HIV) in military service members. Washington, DC: US DoD, 2013 (updated 2022).

---

## Figure legends

**Figure 1:** Event study — HIV among pregnant women (code 109). Incidence rate ratios for the interaction of standardised deposit growth with year indicators, relative to 2019 (base year). Circles denote pre-treatment coefficients (2013–18, 2020); the triangle marks 2021 (COVID disruption to prenatal screening); diamonds denote post-treatment coefficients (2022–24). The square marks the omitted base year. Vertical bars are 95% CIs from cluster-robust standard errors. Joint Wald test for pre-treatment coefficients: χ²(8)=11·79, p=0·16.

**Figure 2:** Monthly year-on-year deposit growth across 76 regions. Grey lines show individual regions; coloured lines highlight Tuva, Buryatia, Chechnya (high mobilisation) and Sverdlovsk, Nizhny Novgorod (low mobilisation). Shaded bands mark three phases: professional soldiers (February–September 2022), formal mobilisation (September–December 2022), and mass contract recruitment (2023 onward).

**Figure 3:** Treatment-window robustness matrix. Incidence rate ratios from ten specifications (five treatment windows crossed with two post-period definitions), all estimated on the preferred sample of 76 regions. Filled circles denote p<0·05. Vertical bars are 95% CIs.

**Figure 4:** Effect by testing category. Incidence rate ratios for the preferred specification across HIV testing categories. Pregnant women (code 109, primary outcome) and blood donors (code 108, ambiguous due to composition changes) show positive effects; healthcare workers (code 115, placebo) and injecting drug users (code 102) are null.
