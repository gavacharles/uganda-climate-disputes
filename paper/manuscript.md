# Quantifying "Exceptionally Adverse Climatic Conditions": Climate Data, Weather Provisions and Extension-of-Time Entitlement in Ugandan Road Contracts under Climate Change

Gavamukulya Charles

*Draft 0.4, 15 October 2026. Target: Journal of Legal Affairs and Dispute Resolution in Engineering and Construction (ASCE).*

## Abstract

**Introduction.** Construction contracts grant extensions of time (EOT) for "exceptionally adverse climatic conditions" but rarely fix the climatic variables, data, baseline period or assessment window that decide what is exceptional. Uganda's road contracts quantify only rainfall, through a monthly formula (Clause 1229 of the Ministry of Works General Specifications), and delegate its averages to tender documents. This study quantifies how far these open choices, rather than the weather, determine entitlement, and proposes a more determinate method.

**Methods.** Four contractual tests were applied consistently to 45 years of daily rainfall from three products (CHIRPS, ARC2, CPC) in all 268 grid cells covering Uganda:

- the FIDIC Contracts Guide return-period rule;
- NEC4's monthly 1-in-10-year test;
- JCT-style practice;
- Clause 1229.

The tests were run on hypothetical 3-year contracts starting monthly from 1991. Verdict sensitivity to data choices and claim-window selection was measured. Heat was assessed with a heat-stress index (simplified wet-bulb globe temperature) from NASA POWER. Bias-corrected CMIP6 projections (10 models, 2041–2070) tested climate-change effects. Contract and claim documents from four Ugandan road projects were reviewed.

**Results.**

- One claim season in four was arguable, and 87% of those were contested under alternative defensible choices.
- Selecting the claim window after the event raised the share of contracts with "exceptional" weather from 50% to 88%.
- Under the FIDIC rule, whether any relief arose depended on the rainfall product for 44% of contracts.
- Clause 1229 gave 13 days per contract as written, and 43 days when only positive months were summed, as in a reviewed claim.
- The rainfall tables printed in two signed contracts did not match the site climate. On one contract a tender addendum moved entitlement from about 219 days to none.
- By 2041–2070, keeping the tender-date baseline raised FIDIC relief by 40–80% (ensemble medians); updating it left 8–10 extra lost days per contract with the Contractor.
- Heat caused a third of weather-lost days nationally (over half in the North) yet is unquantified in Ugandan contracts. With a tender-date baseline, projected warming made heat "exceptional" in over 90% of contracts.

**Discussion.** Entitlement is largely set by unexamined data choices, which creates dispute risk at contract formation. A proposed Shared Weather Allowance names the dataset, tabulates monthly normal and 1-in-10-year lost working days at tender, and shares intermediate losses equally. It eliminated product-dependent verdicts while giving mean relief comparable to Clause 1229 as written. Its relief was also the most stable under projected climate (+25–31% with a stale baseline). The findings held across five East African countries.

## 1. Introduction

Weather is one of the most frequent causes of delay on construction projects in East Africa. In Uganda it ranks second among delay causes on road projects and is cited in a quarter of responses on public building projects (KIU 2025; Makerere). Uganda's public road works are let mainly on FIDIC-based conditions. Under FIDIC the contractor's protection against bad weather is an extension of time for "exceptionally adverse climatic conditions" (Sub-Clause 8.4(c) in the 1999 Red and Yellow Books; 8.5(c) in 2017). The term is undefined in 1999. The 2017 edition ties it to conditions that are Unforeseeable "having regard to climatic data" made available by the Employer or published for the Site, but it does not say which data, over what period, for which window, or by what comparison. The only numerical guidance is a rule of thumb in the FIDIC Contracts Guide (2000): an event is exceptional if its return period is four to five times the Time for Completion.

Uganda adds a further layer. The Ministry of Works General Specifications for Road and Bridge Works, incorporated in national road contracts, contain a monthly formula for "Extension of Time Arising from Abnormal Rainfall" (Clause 1229). The formula is numerical, but the rainfall source, the station and the averaging period are left to the Special Specifications "or as agreed to, in writing, by the Engineer".

Both regimes also narrow the hazard. "Climatic conditions" covers heat, wind and drought as well as rain, but Clause 1229 quantifies only abnormal rainfall. In Uganda's dry north, heat that halts heavy outdoor work therefore has no measurable test at all. Heat is also the hazard with the clearest warming trend.

Every one of these open choices is made after the event, by parties with opposite interests. Legal commentary calls the test subjective (Gowling WLG 2024; Vinson & Elkins). Dispute research, including the growing machine-learning literature, models dispute occurrence and outcomes from project and contract attributes rather than hazard data (Francis et al. 2025). Delay studies in sub-Saharan Africa rank weather as a cause through questionnaires but do not test contractual weather rules against measured climate. No study has measured how much the contractual test itself leaves open, or what each form of words actually delivers under a real climate record.

This paper holds the weather fixed and varies the test. It asks:

1. **RQ1.** Can "exceptionally adverse climatic conditions" be made into a reproducible, site- and season-specific test using gridded data in a data-sparse country?
2. **RQ2.** How often do defensible data choices (rainfall product, baseline length, trend treatment, claim window) reverse the verdict, and where?
3. **RQ3.** Under the same weather, how often and how much relief do the FIDIC Guide rule, NEC4, JCT-style practice and Uganda's Clause 1229 give a typical 3-year contract?
4. **RQ4.** How will climate change by mid-century shift that relief, and who bears the shift when the contractual baseline is fixed at award?
5. **RQ5.** Which clause design gives predictable, data-robust and fair risk sharing?
6. **RQ6.** How large is heat as a contractual climatic hazard in Uganda, and how do the same tests behave for it under warming?

Claim documents from four Ugandan road projects ground the analysis in practice. A short regional analysis tests whether the findings travel to Kenya, Tanzania, Rwanda and Burundi.

## 2. Contractual weather tests

**FIDIC.** Under the 1999 Red and Yellow Books (8.4(c)), the Contractor is entitled to an extension of time for "exceptionally adverse climatic conditions", without definition. The 2017 Red and Yellow Books (8.5(c)) add: "which for the purpose of these Conditions shall mean adverse climatic conditions at the Site which are Unforeseeable having regard to climatic data made available by the Employer under Sub-Clause 2.5 and/or climatic data published in the Country for the geographical location of the Site". Relief is time only. The Silver Book (EPC) gives no weather relief. The FIDIC Contracts Guide (2000) suggests comparing the event with the frequency of similarly adverse events at or near the site. It treats as exceptional an event whose return period exceeds four to five times the Time for Completion. [Check exact Guide wording against the primary text.]

**NEC4.** Clause 60.1(13) makes weather a compensation event when a weather measurement recorded within a calendar month at a defined place is shown to occur on average less frequently than once in ten years. Only the difference between the measured weather and the 1-in-10-year weather is compensated, in time and money.

**JCT.** "Exceptionally adverse weather" is a Relevant Event without a numerical test. In practice, monthly records are compared with ten-year Met Office data, and the delay above an average month is claimed. [Cite practice sources.]

**Uganda: MoWT Clause 1229.** For each calendar month of the period for completion, including extensions:

> V = (N_w − N_n) + (R_w − R_n)/x, with V ≥ −N_n

Here N_w and R_w are the month's number of days with rainfall ≥ Y mm and its total rainfall. N_n and R_n are the corresponding averages "derived from the existing rainfall records of the Department of Meteorology provided in the Special Specifications, or as agreed to, in writing by the Engineer". Y = 10 mm and x = 20 unless the Special Specifications say otherwise. "The total extension of time shall be the algebraic sum of the monthly totals." Clause 1229 thus quantifies the weather relief but delegates the dataset and baseline.

**Which climatic conditions?** None of the FIDIC editions lists the climatic variables covered. Heat, wind, drought and humidity are as much "climatic conditions" as rain. NEC4 names four measurements (cumulative rainfall, days with rainfall over 5 mm, days with minimum air temperature below 0 °C, snow lying), and the parties may add others in the Contract Data. Clause 1229 covers rainfall only. The MoWT General Specifications refer to heat, cold and wind only as working limits, not as grounds for EOT: limits on placing concrete in hot and cold weather, no sprigging or sheeting in windy conditions, and occupational "prolonged stay in high temperatures".

*Table 1. Contractual weather tests compared.*

| | FIDIC 1999/2017 (8.4(c)/8.5(c)) + Contracts Guide | NEC4 60.1(13) | JCT (practice) | MoWT Clause 1229 |
|---|---|---|---|---|
| Hazard | Any "climatic conditions" (unspecified) | Four named measurements; others may be added | "Weather" (unspecified) | Rainfall only |
| Trigger | Return period ≥ 4–5 × TfC (Guide) | Monthly measurement rarer than 1 in 10 years | Exceptional vs ~10-year monthly record | None: every month computed |
| Window | Unspecified | Calendar month | Usually calendar month | Calendar month |
| Data | Employer's or published data (2017); unspecified (1999) | Measurements at a place stated in Contract Data | Usually Met Office records | Meteorological Department or "as agreed by the Engineer" |
| Baseline | Unspecified | Implicit in the 1-in-10 data | ~10 years | "Existing records" in Special Specifications or as agreed |
| Relief measure | Delay caused | Only the excess over 1-in-10 weather | Delay above an average month | V = (N_w − N_n) + (R_w − R_n)/20, summed algebraically |
| Relief type | Time | Time and money | Time | Time (time and money unless amended) |
| Left open | Variable, data, baseline, window, comparison | Additional measurements, baseline source | Data, threshold | Data source, baseline period, summation in practice |

## 3. Contract practice: four Ugandan road projects

The author reviewed the contract and claim documents of four national road projects (Table 2). They are anonymised as Projects A–D.

- **Project A** is a 97-km design-and-build upgrading package in western Uganda (FIDIC 1999 conditions; Time for Completion 1,099 days). Its Specification invokes Clause 1229. The Contractor's interim EOT claim No. 3 sought 21 days for September 2019 – November 2020. It applied Clause 1229 with averages from a single national meteorological station for 2005–2017/18, a 13-year record. In the monthly table, months with negative V appear as zero, so only positive months were summed, contrary to the specified algebraic sum. The Engineer granted 21 days "in line with the Contractor's analysis" without independent data. The days were later absorbed into a concurrent possession delay. Subsequent claims cite 4, 16 and 19 days of "exceptional rain" in 2021–2023.
- **Project B** is a 145-km rehabilitation in central-western Uganda under FIDIC 2017 conditions. The Contractor's monthly report attributes delay to "adverse weather conditions experienced in the months September 2023 to December 2023 and August 2024 to December 2024 due to the rainy season". The Engineer's reviewer asked whether it was "just rain or inclement weather" and whether "the rainfall data reflected this".
- **Projects C and D** (FIDIC conditions) contain the undefined 8.4(c) wording. Their delay disputes concern possession, suspension, payment and prolongation cost rather than weather.

**The tables in the contracts.** Two of the agreements, B and D, fill Clause 1229's gaps through a common Special Specification:

- N_w from site rain gauges read jointly each morning;
- the algebraic sum, with no reduction of time for a negative total;
- a monthly cap;
- time only, no money;
- a Table 1229/1 of monthly N_n and R_n.

The tables do not match the climate (Table 2b, Fig. 10).

- **Project D.** The original table is headed with the name of a station at the opposite end of the country. Its averages are 28 rain-days and 954 mm a year, against 38–63 days and 1,259–1,576 mm at the site in CPC and CHIRPS for 1991–2020. A tender addendum replaced it with a site-named table totalling 102 rain-days and 5,988 mm, four to five times the observed rainfall.
- **Project B.** The table lists 251 "rain-days ≥ 10 mm" and 128 mm a year, against about 33 days and 1,000–1,240 mm observed. The rows appear to be mislabelled.

Applied to 3-year contracts with gridded N_w and R_w:

| | EOT per contract | Contracts with EOT |
|---|---|---|
| D, original table | 219 days | every contract |
| D, addendum table | 0 days | none |
| D, data-based normals | 26.5 days | 73% |
| B, table in contract | 0 days | none |
| B, data-based normals | 12.7 days | 66% |

A single table, drafted at tender and rarely checked, decides the weather entitlement more than the weather does.

**Conditions of contract.**

- Project B uses FIDIC 2017 numbering, with delay damages of 0.05% of the Contract Price per day (Sub-Clause 8.8).
- Project C uses the FIDIC 1999 First Edition, with a Time for Completion of at most 1,095 days.
- Project D uses the FIDIC MDB Harmonised Edition (2010).

In Project D's rate breakdown, head-office overheads are 10% of the contract price.

*Table 2. Contract regimes and weather claims in Projects A–D.*

## 4. Data and methods

### 4.1 Data

- **Rainfall.** Three products:
  - CHIRPS v2.0 daily, 0.25°, 1981–2026 (Funk et al. 2015);
  - ARC2 daily, 0.1°, 1983–2025 (Novella and Thiaw 2013);
  - CPC Unified gauge-based daily, 0.5°, 1981–2025.

  A homogeneity screen found a step increase in ARC2 from January 2020 to September 2023. Over that period ARC2 national monthly totals are 1.3–3.2 times CHIRPS, and annual totals are about 2,150–2,310 mm against about 1,300 mm in other years. Those months are masked (Fig. S1). Windows missing more than 5% of days are not assessed, and smaller gaps are scaled.
- **Grid.** All 268 CHIRPS cells with centres in Uganda's four regions, excluding open water.
- **Heat.** NASA POWER daily maximum temperature and dewpoint, 1981–2025, at 52 grid points (about 0.5°) in Uganda. Projected warming uses the CMIP6 ensemble-median monthly temperature change for 2041–2070 (1.3 °C under SSP2-4.5, 1.8 °C under SSP5-8.5).
- **Projections.** NEX-GDDP-CMIP6 (Thrasher et al. 2022): daily, 0.25°, bias-corrected precipitation from 10 models (ACCESS-CM2, CanESM5, EC-Earth3, GFDL-ESM4, INM-CM5-0, IPSL-CM6A-LR, MIROC6, MPI-ESM1-2-HR, MRI-ESM2-0, NorESM2-MM). Periods: historical 1985–2014; SSP2-4.5 and SSP5-8.5 for 2041–2070.

### 4.2 Lost working days and the Exceptionality Index (RQ1)

A lost working day (LWD) is a day with rainfall ≥ 10 mm. This is the Clause 1229 default and a common earthworks threshold; ≥ 5 mm is a sensitivity case. For a claim window, the LWD count is compared with the same calendar window in each baseline year. The return period is estimated three ways:

- empirically, as (n+1)/(m+1), where m is the number of baseline values ≥ the claim value;
- from a stationary GEV distribution;
- from a non-stationary GEV with a linear trend in location, evaluated at the claim year.

The Exceptionality Index is EI = RP / TfC. Following the Guide, a window is exceptional when EI ≥ 5 (RP ≥ 15 years for a 3-year contract) and borderline when 4 ≤ EI < 5.

### 4.3 Verdict sensitivity (RQ2)

Claim windows are every meteorological season from DJF 2001 to SON 2019 in every cell. Each is judged on data before it under 2 × 2 × 2 defensible choices:

- rainfall product: CHIRPS, or the nearest ARC2 cell;
- baseline: previous 20 years, or full prior record;
- statistics: stationary or trend-aware GEV.

A window is *arguable* if at least one choice finds it exceptional, and *contested* if the choices disagree. Pairwise flip rates isolate each choice.

Window selection is tested separately. For each of 77 calendar start days, the 15-year return level of 90-day LWD is fitted on 1991–2020 data. For each 3-year contract, two cases are compared: fixed meteorological seasons, and any 90-day window the claimant might choose.

### 4.4 Contract forms and candidate clauses (RQ3, RQ5)

For each cell, 3-year contracts start on the first of every month (1991–2023 for the forms; 1991–2018 for the clauses). They are evaluated against the 1991–2020 normal:

- **FIDIC Guide.** A season with LWD at or above the 15-year return level. Relief = LWD minus the seasonal mean.
- **NEC4.** A month with rainfall or days ≥ 5 mm above the calendar month's 90th percentile. Relief = LWD minus the month's 1-in-10-year LWD, floored at zero.
- **JCT-style practice.** The NEC4 trigger. Relief = LWD minus the monthly mean.
- **Clause 1229.** V per month. Relief = max(ΣV, 0) over the contract, as written; and ΣV⁺, positive months only, as practised.
- **Candidate clauses**, all using lost-day thresholds in the Contract Data from a named dataset and cell:
  - *1-in-10 table:* relief = (L − q90)⁺;
  - *mean table:* relief = (L − mean)⁺;
  - *shared band:* relief = ½·min((L − mean)⁺, q90 − mean) + (L − q90)⁺.

Here L is the month's LWD and q90 its 1-in-10-year value. The Employer carries half of above-normal lost days up to the 1-in-10 level and all of them beyond.

Metrics are:

- probability of any relief per contract;
- mean relief days;
- coefficient of variation across contracts (predictability);
- share of above-normal lost days relieved (risk sharing);
- product sensitivity: mean |relief(CHIRPS) − relief(CPC)| / mean relief, and the share of contracts whose any-relief verdict differs between products.

### 4.5 Climate change (RQ4)

For each NEX model and cell, contracts are evaluated three ways:

- in the historical run against its 1985–2014 baseline;
- in 2041–2070 against the same historical baseline (*stale*, as when climatic data are fixed at award);
- in 2041–2070 against a 2041–2070 baseline (*updated*).

Changes are computed within each model, and the ensemble median and 10–90% range are reported. Total LWD per contract measures the weather the Contractor must either price or be relieved of. A delta-change version using monthly CMIP6 change factors, with and without heavy-rain (Clausius–Clapeyron) scaling, is reported as a sensitivity.

### 4.6 Cost translation

Relief days and lost days are converted to Uganda shillings using two rates per day, as shares of contract price:

- delay damages: 0.05% per day, a common Contract Data value (e.g. KCCA 2023);
- time-related cost: 0.02–0.05% per day.

The programme is UNRA's FY2025/26 budget, about UGX 3.13 trillion. The delay-damages rate matches Project B's Contract Data. The time-related range is consistent with Project D's 10% head-office overhead over a 3-year period (about 0.01% per day) plus site time-related costs.

### 4.7 Heat (RQ6)

Heat stress is measured with the simplified wet-bulb globe temperature:

> sWBGT = 0.567·T_max + 0.393·e + 3.94, with e = 6.105·exp(17.27·T_d / (237.7 + T_d))

This is computed daily from maximum temperature and dewpoint. A heat-lost day is a day with sWBGT ≥ 30 °C, a level at which heavy outdoor work by acclimatised workers must be substantially curtailed. Thresholds of 29 and 31 °C are sensitivities. [Verify against ISO 7243 and ACGIH reference values.]

The analysis then repeats the rainfall tests on monthly and seasonal heat-lost-day counts:

- the observed trend (Theil–Sen);
- the FIDIC Guide test on seasons (15-year return level, 1991–2020 normal);
- stationary vs trend-aware verdicts for 2001–2025;
- an SWA heat row;
- heat's share of all weather-lost days, with rain lost days taken from the nearest CHIRPS cell.

Projections add the monthly warming to both T_max and T_d, which keeps relative humidity roughly constant. They are evaluated against stale and updated baselines. This delta method is a first approximation; daily NEX temperature fields would refine it.

### 4.8 Case studies

- **Project A:** the Clause 1229 claim is recomputed for the claim window and the whole contract period, under CHIRPS, CPC and ARC2, the Contractor's 2005–2017 baseline and a 30-year pre-award baseline, and algebraic vs positive-month summation.
- **Project B:** the two delay periods are tested with the EI at four points along the corridor, on three products.

## 5. Results

### 5.1 The index behaves sensibly (RQ1)

For contracts awarded in 2018 with a 3-year TfC:

- **OND 2019** (the record short rains of the 2019 positive Indian Ocean Dipole) is exceptional in 64% of Uganda's cells on CHIRPS, concentrated in the centre, north and east (Fig. 2).
- **MAM 2020** is exceptional in 28% of cells, mainly the east and north-east.
- **MAM 2019** is exceptional nowhere.

NEC-style monthly tests agree: 62% of site-months in OND 2019 exceed the 1-in-10-year value, against 4% in MAM 2019.

For OND 2019, CHIRPS and ARC2 agree on the verdict in only 60% of cells. With a 10-year baseline, about the length of many station records, an 8- to 15-year event cannot be resolved at all.

### 5.2 One arguable claim in four, and most are contested (RQ2)

- Across Uganda, 24.5% of claim seasons in 2001–2019 are arguable. Of these, **87% are contested** (Fig. 3).
- The rainfall product causes most of the flips (10.4% of all seasons), then trend treatment (4.2%), then baseline length (2.7%). Of arguable seasons, 36% are contested by the dataset choice alone, 9% by trend treatment alone and 3% by baseline length alone. A further 10% are contested by two or more choices, and 28% only by combinations of choices (Fig. 17).
- Dispute risk is highest in the north and east, along the Elgon border and in Karamoja.

**Window selection.** Letting the claimant choose any 90-day window raises the share of 3-year contracts with an "exceptional" window from 50% to 88%. Even within the 1991–2020 baseline, 60% of years contain a "1-in-15-year" 90-day window, against 24% for fixed seasons (Fig. 4).

### 5.3 Same weather, different entitlement (RQ3)

Nationally (Table 4, Fig. 5):

| Form | Contracts with relief | Mean relief per contract |
|---|---|---|
| FIDIC Guide | 51% | 5.6 days |
| NEC4 | 98% | 3.8 days |
| JCT-style practice | 98% | 11.5 days |

NEC4's near-certain trigger follows from monthly testing. Each month triggers 12.7% of the time, and over 36 months 1 − (1 − 0.127)³⁶ ≈ 0.99. NEC4 is frequent-small, FIDIC rare-large. The JCT-style average-excess measure gives about twice FIDIC's relief.

Across all contracts and cells, the FIDIC Guide and Clause 1229 as written give no EOT at all to 49% and 45% of contracts respectively (Fig. 15). Clause 1229 as written relieves 59% of contracts with 13.4 days on average. As practised (positive months only) it relieves every contract with 42.6 days. That is about three times as much, and 174% of the above-normal lost days actually experienced, so ordinary month-to-month variation is converted into extension of time (Table 5).

### 5.4 Case studies

**Project A.** The same clause, applied to the same contract, gives anywhere from 0 to 42 days, depending on product, baseline and window, when summed algebraically as specified. Positive-month summation gives 19 to 67 days. The Contractor's station-based 21 days falls inside this range. However, the months identified as abnormal differ between station and gridded data: for May 2020 the claim shows +9.2 days, CHIRPS −0.3 and CPC +4.8. Without a named dataset and summation rule, the clause does not determine the entitlement (Table 3, Fig. 11).

**Project B.** Neither delay period comes near exceptional on CHIRPS or CPC (EI 0.4–1.6 at all four points), which is consistent with an ordinary rainy season. On ARC2, however, Aug–Dec 2024 is exceptional at the northern end of the corridor (EI 5.8). A claimant searching across public datasets would find support in one product out of three.

### 5.5 Climate change moves the line (RQ4)

The 10 NEX-GDDP-CMIP6 models were compared with their own 1985–2014 runs for 2041–2070. Their historical simulations reproduce annual rainfall within about 10–20% of CHIRPS. They give fewer heavy-rain days in the dry south-west, which is why all changes are computed within each model. Results are ensemble medians for Uganda, with 10–90% model ranges in brackets (Table 6, Fig. 7).

| Change per 3-year contract, 2041–2070 vs 1985–2014 | SSP2-4.5 | SSP5-8.5 |
|---|---|---|
| Lost working days (≥ 10 mm) | +7.9 (+0.9 to +31) | +9.6 (−1.1 to +60) |
| FIDIC Guide, share of contracts relieved, stale baseline | +13 points (+7 to +28) | +22 points (+8 to +36) |
| FIDIC Guide, relief days, stale baseline | +2.9 (+0.6 to +17) | +5.3 (+0.4 to +40) |
| FIDIC Guide, relief days, updated baseline | +0.3 (−0.6 to +1.3) | +1.1 (−0.5 to +3.0) |
| NEC4, relief days, stale baseline | +3.3 (+1.3 to +11) | +3.6 (+2.0 to +23) |
| NEC4, relief days, updated baseline | +0.4 | +0.4 |

Against historical model values of 6.8 FIDIC and 4.7 NEC4 relief days per contract:

- **With a stale baseline**, FIDIC relief rises by about 40% (SSP2-4.5) to 80% (SSP5-8.5), and NEC4 relief by about 70–75%. The extra lost days are converted into extension of time, a cost the Employer carries.
- **With an updated baseline**, relief barely changes, and the 8–10 extra lost days per contract stay with the Contractor, who will price them into tenders.
- **Regionally**, the increase in relief probability is largest in the Western (+27 points, SSP5-8.5) and Central regions. The increase in lost days is largest in the Central and Eastern regions.

The model spread is wide and skewed: a minority of wetter models gives much larger increases. Even the 10th-percentile model raises stale-baseline relief under both forms.

A delta-change sensitivity (CMIP6 ensemble-median monthly factors applied to CHIRPS, with and without heavy-rain scaling) gives the same direction and somewhat larger medians. Under SSP5-8.5 it gives +17 lost days per contract and FIDIC relief rising from 54% to 84% of contracts with a stale baseline.

**Cost.** At 0.05% of contract price per day of delay damages and a UGX 3.13 trillion annual programme, today's FIDIC weather relief is worth about UGX 9 billion a year in delay damages avoided by contractors. Under SSP5-8.5 with a stale baseline, a further UGX 8 billion a year moves to the Employer. With an updated baseline, the 8–10 extra lost days per contract instead cost contractors about UGX 5–15 billion a year in time-related costs (0.02–0.05% per day), which will be priced into tenders. These are modest sums against the programme, but they recur every year and grow with the climate signal. What matters is that no contract states who bears them (results/rq7_money.csv).

### 5.6 Clause design (RQ5)

Nationally, under the present climate (Table 5):

- **FIDIC Guide (status quo):** worst on predictability (CV 1.27) and data robustness. The any-relief verdict differs between CHIRPS and CPC for 44% of contracts, and it relieves only 22% of above-normal lost days.
- **Clause 1229 as written:** a 37% verdict-flip rate.
- **Shared band:** about the same mean relief as Clause 1229 as written (14.3 vs 13.4 days). It eliminates verdict flips, roughly halves the relief gap between products, cuts variability to a third (CV 0.43), and gives the Employer 59% of above-normal lost days.

Under projected climate with stale tables, SWA relief rises least of all rules (+25–31%, against +42–78% for the FIDIC Guide and +56–72% for Clause 1229 as written; Section 6).

### 5.7 Regional outlook

To test whether the findings depend on Uganda's climate, the present-climate analysis was repeated for all 2,243 CHIRPS land cells in Uganda, Kenya, Tanzania, Rwanda and Burundi. These range from bimodal equatorial to unimodal southern regimes (Table 7, Fig. 8).

The pattern is the same in every country:

- The FIDIC Guide relieves 42–62% of 3-year contracts. Whether any relief arises depends on the rainfall product (CHIRPS vs CPC) for 33–46% of them.
- NEC4 relieves 95–98% of contracts with 2.9–3.4 days each.
- Clause 1229 summed over positive months only gives 2.6–4.1 times the algebraic-sum entitlement.
- The Shared Weather Allowance gives 10–14 days per contract with no product-dependent verdicts, and a coefficient of variation of 0.38–0.60 against 1.05–1.51 for the FIDIC Guide.

*Table 7. East Africa, 3-year contracts, 1991–2020 normals.*

| Country | FIDIC: P(relief) | FIDIC: verdict differs CHIRPS vs CPC | NEC4: days | 1229 algebraic: days | 1229 positive-only: days | SWA: days | SWA: verdict differs |
|---|---|---|---|---|---|---|---|
| Uganda | 0.53 | 0.44 | 3.3 | 13.3 | 42.6 | 14.3 | 0.00 |
| Kenya | 0.44 | 0.33 | 3.2 | 13.3 | 34.5 | 10.1 | 0.00 |
| Tanzania | 0.42 | 0.38 | 2.9 | 11.5 | 40.9 | 12.0 | 0.00 |
| Rwanda | 0.62 | 0.46 | 3.3 | 9.7 | 39.8 | 13.3 | 0.00 |
| Burundi | 0.52 | 0.46 | 3.4 | 13.0 | 42.0 | 13.8 | 0.00 |
| East Africa | 0.45 | 0.37 | 3.1 | 12.3 | 39.0 | 11.7 | 0.00 |

The indeterminacy of the contractual test is therefore not a feature of one climate or one dataset pair. A cross-country comparison of the standard specifications and projected changes is left to a separate study.

### 5.8 Heat: the unquantified hazard (RQ6)

Heat stress is already a material cause of lost working time (Table 8, Fig. 9).

- **Today.** Over 1991–2020, the national mean is 38 heat-lost days a year (sWBGT ≥ 30 °C). The Northern region has 69 and the Central region 8. Per 3-year contract, heat accounts for 34% of all weather-lost days nationally and 53% in the North, where it now rivals rain.
- **Trend.** Heat-lost days rose by about 6 days per decade over 1981–2025: 9 per decade in the North (Kendall p = 0.01) and 5 in the East (p = 0.02).
- **Seasonality.** Heat-lost days peak in February–April, the hot and humid months before and at the start of the long rains, and are concentrated in the North and East (Fig. 14).
- **Sensitivity to threshold.** The count is highly sensitive to the threshold chosen: 91, 38 and 12 days a year at 29, 30 and 31 °C. This is the same indeterminacy as for rainfall data, in another variable.

Applied to heat, the FIDIC Guide test behaves much as it does for rain under the present climate: 45% of contracts have an "exceptional" heat season, with 7 relief days each. Under warming, the tender-date baseline fails completely:

| Heat, 3-year contracts | 1991–2020 | SSP2-4.5 (+1.3 °C) | SSP5-8.5 (+1.8 °C) |
|---|---|---|---|
| Heat-lost days per contract | 117 | 353 | 474 |
| FIDIC "exceptional", stale baseline: contracts | 45% | 92% | 96% |
| FIDIC relief days, stale baseline | 7 | 179 | 280 |
| FIDIC, updated baseline | 45%, 7 days | 51%, 13 days | 60%, 14 days |
| SWA heat row, stale tables | 18 days | 199 days | 317 days |
| SWA heat row, updated tables | 18 days | 32 days | 33 days |

Even under updated baselines, about 240–360 more heat-lost days per contract must be priced by the Contractor. That is larger than the projected change in rain lost days by more than an order of magnitude.

The observed record shows few verdict flips between stationary and trend-aware heat baselines yet (3%). The projected shift, however, is far outside the historical distribution. For heat, a baseline fixed at award stops being a test of exceptionality and becomes a transfer of the warming trend to the Employer.

*Table 8. Heat by region (results/rq6_heat_regions.csv).*

| Region | Heat-lost days/yr | Trend (days/decade) | Heat share of weather-lost days | Heat days per contract: today / SSP2-4.5 / SSP5-8.5 |
|---|---|---|---|---|
| Central | 8 | +2.5 | 14% | 25 / 135 / 228 |
| Eastern | 29 | +5.2 | 32% | 89 / 335 / 464 |
| Northern | 69 | +8.9 | 53% | 211 / 563 / 716 |
| Western | 17 | +4.0 | 21% | 50 / 191 / 281 |
| Uganda | 38 | +5.9 | 34% | 117 / 353 / 474 |

## 6. A proposed method: the Shared Weather Allowance (SWA)

The results point to a design that fixes every open choice at tender, uses a continuous rather than binary measure, and splits intermediate weather between the parties. We call it the Shared Weather Allowance.

### 6.1 Procedure

1. **Name the data.** For each section of the works, the Contract Data names one dataset and one location (grid cell or station). That dataset supplies both the monthly counts and the normals. It is screened for homogeneity before tender, and the contract allocates the risk of data error.
2. **Name the hazards.** Rain lost working days (days with ≥ 10 mm) and, where relevant, heat-lost days (days with sWBGT ≥ 30 °C, or a stated index and threshold).
3. **Tabulate at tender.** For each calendar month m and each hazard, the Contract Data gives the 30-year pre-award mean (normal_m) and the 1-in-10-year value (q90_m). The Contractor prices the normal days into the programme.
4. **Assess calendar months.** During the works, the named data give the month's lost days, L_m.
5. **Share the excess:**

   > EOT_m = ½ · min((L_m − normal_m)⁺, q90_m − normal_m) + (L_m − q90_m)⁺

   The Contractor carries weather up to the normal (Fig. 12). The parties share equally between the normal and the 1-in-10-year level. The Employer carries everything beyond.
6. **Total and analyse.** Monthly EOT is summed over the period. Concurrency with other delay events is then treated by the contract's ordinary delay analysis.
7. **State the baseline rule.** Tables are fixed at award for contracts of up to three years. For longer contracts, they are recomputed from the latest 30 years at a stated interval. Where 8.5(c) wording is retained, the Exceptionality Index (Section 4.2) provides the reproducible "exceptional" test.

### 6.2 Performance

**Present climate (Uganda, Table 5, Fig. 6).** The SWA gives a mean of 14.3 days per 3-year contract, close to Clause 1229 as written (13.4) and a third of its positive-month practice (42.6). Compared with the alternatives it:

- never changes its any-relief verdict between CHIRPS and CPC, against 44% for the FIDIC Guide and 37% for Clause 1229;
- is about three times more predictable (CV 0.43 against 1.27–1.28);
- assigns 59% of above-normal lost days to the Employer.

A netted variant, in which half of any below-normal deficit offsets relief elsewhere, reintroduces data sensitivity (41% verdict flips; CV 1.31) and is rejected. Across East Africa the SWA gives 10–14 days per contract with no product-dependent verdicts (Table 7).

**Projected climate.** With tables fixed at award, rain-based SWA relief rises by 25–31% (Fig. 16) by 2041–2070 (NEX ensemble median). That is the smallest increase of any rule (FIDIC Guide +42–78%, Clause 1229 +56–72%, NEC4 +71–76%). With updated tables it changes by 6–8%. For heat, fixed tables are untenable under warming (Section 5.8), so the baseline rule in step 7 is essential.

**Worked example (Project A).** For the 2019–2020 claim window, the SWA gives 20 days on CHIRPS and 9 on CPC, using a 1989–2018 baseline. Clause 1229 as written gives 42 and 20 days. Over the whole contract, the SWA gives 25 and 18 days, while Clause 1229 gives 36 and 0. The SWA's spread between datasets is markedly narrower. With the dataset named, as step 1 requires, the answer would be a single number.

**Validation.** On six claimed months with site records (Project A), gridded counts correlate with site counts at 0.85–0.95 (Fig. S2). A point gauge records about twice the days ≥ 10 mm of a 0.25–0.5° cell. Counts and normals must therefore come from the same dataset. Mixing a site gauge for L_m with station or gridded normals, as the Clause 1229 template in Projects B and D does, inflates entitlement.

**Deliverable.** The monthly normal and 1-in-10-year rain lost-day tables for every Uganda cell are provided as supplementary data (results/swa_tables_uganda.csv), ready for insertion in Contract Data.

## 7. Discussion

**The dispute is in the data.** Nearly nine in ten arguable claim seasons can be argued either way by a defensible choice of dataset, baseline or statistic. The single largest source is the rainfall product, not the baseline length that commentary usually emphasises. Two widely used satellite products disagree on whether the record 2019 short rains were exceptional in two-fifths of Uganda. One of them carried an undetected three-year wet bias that would have made every 2020 claim exceptional. A test that leaves the data open converts genuine scientific uncertainty into contractual entitlement, and so into dispute. This is predictable at contract formation, not only after the event.

**Numbers alone do not settle it.** Uganda is unusual in already having a numerical rule, but Clause 1229 shows that a formula without a named data source moves the argument rather than ending it. In practice, the averages are a page of the Special Specifications. In the contracts reviewed, that page named the wrong station, was replaced by an addendum with values four to five times the site climate, or had its rows transposed. Depending on which page applied, the same contract was entitled to about 219 days of weather EOT or to none. The formula's arithmetic is also not followed: summing positive months only, as in the claims reviewed, triples entitlement and turns ordinary month-to-month variation into extension of time. Engineers accepted contractor calculations without independent data. Recomputing one claim with open data gave 0–42 days for the same clause.

**The claimant chooses the window.** Because no form fixes the assessment window, the claimant can select the worst period after the event. That alone lifts the share of contracts with an "exceptional" window from half to nearly nine in ten. Calendar-month assessment, as in NEC4 and Clause 1229, removes this advantage.

**Form is risk allocation (Fig. 13).** Under the same weather, NEC4 compensates almost every contract a little, in time and money. The FIDIC Guide relieves half of contracts, in time only, through a binary test whose outcome depends on the dataset for almost half of them. JCT-style practice gives about twice FIDIC's relief. These are allocations of the same climatic risk, not interpretations of it, and could be chosen deliberately.

**Climate change and the baseline.** A baseline fixed at award passes the warming trend to the Employer as extension of time. For rain the effect is moderate by mid-century (FIDIC relief up 40–80%). For heat it is overwhelming (over 90% of contracts "exceptional"). An updated baseline instead leaves the trend with the Contractor, who must price 8–10 extra rain lost days and hundreds of extra heat-lost days per 3-year contract by mid-century. Neither allocation is wrong, but at present no Ugandan contract states which applies. The annual sums involved are modest against the national road programme (UGX 5–15 billion), but they recur and grow.

**Heat is the missing hazard.** "Climatic conditions" includes heat. In northern Uganda, heat already accounts for over half of weather-lost working days, yet Ugandan specifications treat it only as a technical or occupational limit. Contractors who stop work for heat have no measurable test, and employers have no defined exposure. As warming continues, heat will become the dominant contractual climatic risk in the north. The SWA can carry a heat row in the same banded form, with the index and threshold named, since the heat count is as threshold-sensitive as the rain count is dataset-sensitive.

**Implications for practice in Uganda.** The MoWT General Specifications and the PPDA standard bidding documents could incorporate the SWA directly. That means replacing Table 1229/1 with tables generated from a named gridded or station dataset, enforcing algebraic summation if Clause 1229 is retained, and adding a heat row for northern and eastern contracts. UNRA could publish the national tables with each tender, as this study does for rainfall.

**Limitations.**

- The contracts analysed nationally are hypothetical. Lost working days are a proxy for site disruption and do not capture drainage, soils or programme sequencing.
- Gridded cells smooth point extremes. The 10 mm and 30 °C thresholds are conventions, and the heat index is a simplified form.
- Extreme-value fits on counts are approximate, though the verdicts rest on return levels within the record.
- 1991–2020 contracts are evaluated against an in-sample normal.
- The heat projections use a delta method, and the rain projections show wide model spread.
- The document review covers four projects, not a sample, and is reported in anonymised form.

None of these limitations affects the central finding, which concerns the sensitivity of the contractual verdict to choices the contracts leave open.

## 8. Recommendations for drafting

1. **Name the climatic data in the Contract Data:** one dataset and one location per section, used for both monthly counts and normals. Attach the monthly normal and 1-in-10-year tables at tender, generated from at least 30 years of record.
2. **Screen the data and allocate the risk.** Require a homogeneity check before tender, and state who bears the consequences of later-discovered data errors.
3. **Fix the window:** calendar months.
4. **If Clause 1229 is kept, apply it as written**, with algebraic summation over the whole period for completion, and audit Table 1229/1 against the site climate before tender.
5. **Prefer the Shared Weather Allowance:** a continuous, banded measure with the Contractor carrying normal weather, the parties sharing up to the 1-in-10-year level, and the Employer carrying the rest.
6. **Name the hazards.** Include heat (index and threshold) where it is material, particularly in northern and eastern Uganda.
7. **State the baseline rule:** fixed at award for short contracts; periodically updated for long contracts and for heat.
8. **For Engineers: determine weather claims on the named data, not on the claimant's calculation.**

## 9. Conclusions

Whether weather is "exceptionally adverse" under a construction contract depends less on the weather than on choices the contract leaves open: which variable, which data, which baseline, which window, and how the result is summed. Applied consistently to 45 years of Ugandan rainfall, the tests in current use give opposite verdicts for most arguable claims. They reward choosing the window after the event, and differ by form in ways that reflect risk allocation rather than interpretation. Uganda's own numerical rule is undermined in practice by unchecked tables and selective arithmetic. Heat, already a third of weather-lost days and rising, is not quantified at all. Climate change will widen every one of these gaps unless contracts say how the baseline moves.

The Shared Weather Allowance removes most of this indeterminacy at contract formation. It names the data, tabulates normal and 1-in-10-year lost days at tender, and shares the excess in bands. It also proves stable across datasets, countries and projected climate.

## Acknowledgements and use of generative AI

[Funding and data acknowledgements.] Generative AI (Claude, Anthropic) assisted with analysis code, document text extraction and drafting. The author designed the study, verified all analyses, results and text, and takes responsibility for the content.

## Data and code availability

Code: project repository (`src/`). Data: CHIRPS, ARC2, CPC Unified and NEX-GDDP-CMIP6 are open. Project documents are confidential and reported in anonymised form.

## Figures and tables (current files)

*Seventeen main figures exceed most journal limits. Suggested main-text set: Figs. 1, 2, 3, 5, 6 (or 15), 10, 11, 12, 13, 9 or 14, 16. The rest go to the supplement.*

| Item | Content | File |
|---|---|---|
| Fig. 1 | Conceptual framework | figures/fig1_framework.png |
| Fig. 2 | EI maps OND 2019, MAM 2020 and CHIRPS–ARC2 agreement | figures/wp1_map_ei.png |
| Fig. 3 | Dispute-risk map | figures/rq2_dispute_risk_map.png (add CPC and arguable-share panel) |
| Fig. 4 | Window selection | figures/rq2b_window_map.png |
| Fig. 5 | Contract forms | figures/rq3_forms_map.png, rq3_forms_regions.png |
| Fig. 6 | Clause comparison | figures/fig6_clauses.png |
| Fig. 7 | Projections | figures/nex_uganda_map.png |
| Fig. 8 | Regional outlook | figures/ea_forms_map.png |
| Fig. 9 | Heat | figures/rq6_heat_map.png |
| Fig. 10 | Clause 1229 tables in contracts vs site climate; EOT per contract | figures/fig10_contract_tables.png |
| Fig. 11 | Project A claim recomputed | figures/fig11_projectA.png |
| Fig. 12 | How the SWA works | figures/fig12_swa_schematic.png |
| Fig. 13 | Who carries the weather, today and 2041–2070 | figures/fig13_risk_split.png |
| Fig. 14 | Rain and heat lost days through the year | figures/fig14_rain_heat_calendar.png |
| Fig. 15 | EOT across all contracts, by rule | figures/fig15_eot_distribution.png |
| Fig. 16 | Climate stability of each rule | figures/fig16_climate_stability.png |
| Fig. 17 | Sources of contested verdicts | figures/fig17_contested_sources.png |
| Fig. S1 | ARC2 homogeneity break | figures/figS1_arc2_break.png |
| Fig. S2 | Site gauge vs gridded data (Project A) | figures/figS2_gauge_vs_grid.png |
| Substack | Single-panel versions | figures/substack_contract_tables.png, substack_swa_schematic.png, substack_rain_heat.png |
| Table 1 | Contractual tests compared | Section 2 |
| Table 2 | Projects A–D | docs/contract_review.md |
| Table 2b | Clause 1229 tables in contracts vs data; EOT per contract | results/case_tables.csv, case_tables_eot.csv |
| Table 3 | Project A recomputation | results/case_package5.csv |
| Table 4 | Forms by region | results/rq3_forms_regions.csv |
| Table 5 | Clauses | results/rq5_clauses_present.csv |
| Table 6 | Projections and costs | results/nex_uganda_summary.csv, rq7_money.csv, rq5_clauses_future.csv |
| Table 7 | Regional | results/ea_*_countries.csv |
| Table 8 | Heat by region | results/rq6_heat_regions.csv |
| Supplementary | National SWA tables | results/swa_tables_uganda.csv |

## References

*Verify all entries against primary sources before submission.*

- ACGIH (2023). *TLVs and BEIs: Threshold Limit Values for Chemical Substances and Physical Agents.* American Conference of Governmental Industrial Hygienists, Cincinnati.
- Australian Bureau of Meteorology. About the WBGT and apparent temperature indices (simplified WBGT formula).
- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values.* Springer, London.
- FIDIC (1999). *Conditions of Contract for Construction* (Red Book) and *Conditions of Contract for Plant and Design-Build* (Yellow Book), 1st ed. FIDIC, Geneva.
- FIDIC (2000). *The FIDIC Contracts Guide.* FIDIC, Geneva.
- FIDIC (2010). *Conditions of Contract for Construction, Multilateral Development Bank Harmonised Edition.* FIDIC, Geneva.
- FIDIC (2017). *Conditions of Contract for Construction* (Red Book), 2nd ed. FIDIC, Geneva.
- Francis, M., Perera, S., Zhou, W., and Nanayakkara, S. (2025). Artificial intelligence applications for proactive dispute management in the construction industry: a systematic literature review. *Journal of Information Technology in Construction*, 30, 711–730.
- Funk, C., et al. (2015). The climate hazards infrared precipitation with stations: a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066.
- Gowling WLG (2024). Adverse weather claims. https://gowlingwlg.com/en/insights-resources/articles/2024/adverse-weather-claims
- ISO (2017). *ISO 7243:2017 Ergonomics of the thermal environment: Assessment of heat stress using the WBGT index.* ISO, Geneva.
- JCT (2024). *Design and Build Contract.* Joint Contracts Tribunal, London.
- Kampala Capital City Authority (2023). Addendum No. 1, Kampala City Roads Rehabilitation Project bidding documents.
- KIU Journal of Science, Engineering and Technology (2025). Investigating the dynamics of delays in public building projects in Uganda.
- Ministry of Finance, Planning and Economic Development (BMAU). Briefing Paper 7/13: Delays and cost overruns in the construction of roads.
- Ministry of Works and Transport, Uganda. *General Specifications for Road and Bridge Works*, Series 1000, Clause 1229.
- NASA POWER Project. Prediction of Worldwide Energy Resources, daily meteorological data. https://power.larc.nasa.gov
- NEC (2017). *NEC4 Engineering and Construction Contract.* Thomas Telford, London.
- Novella, N. S., and Thiaw, W. M. (2013). African Rainfall Climatology Version 2 for famine early warning systems. *Journal of Applied Meteorology and Climatology*, 52, 588–606.
- Thrasher, B., et al. (2022). NASA Global Daily Downscaled Projections, CMIP6. *Scientific Data*, 9, 262.
- Uganda National Roads Authority (2025). Budget framework paper, FY2025/26.
- Vinson & Elkins. When you walk through a storm: legal implications of adverse weather on construction contracts.
- Xie, P., et al. (2007). A gauge-based analysis of daily precipitation over East Asia. *Journal of Hydrometeorology*, 8, 607–626. [CPC Unified methodology; confirm global product citation.]
- [Makerere University dissertation on road project delays in Uganda; KTA Advocates (2023) on delays and DAABs.]
