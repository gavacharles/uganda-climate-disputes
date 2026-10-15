# WP1 Exceptionality Index: first results (14 October 2026)

## What was built

- `src/ei.py` is the EI library. For a site and a claim window it computes rainfall indicators: lost working days (LWD) at ≥10 mm/day (earthworks) and ≥5 mm/day (surfacing), seasonal total, wet days, longest wet spell, Rx1day and Rx5day. It then:
  - computes the same indicators for the same calendar window in every pre-award baseline year;
  - converts the claim value to a return period three ways: empirical (Weibull rank, bounded at n+1), stationary GEV, and non-stationary GEV (location trending with year, evaluated at the claim year, with a likelihood-ratio test of the trend);
  - reports EI = RP / Time for Completion and a verdict: ≥5 exceptional, 4–5 borderline (FIDIC Contracts Guide band);
  - reports the value needed to count as exceptional (the RP = 4 × TfC return level) and the excess over the baseline mean;
  - runs an NEC-style monthly test: each month against its 1-in-10-year value, with the excess, because NEC compensates only the excess.
- `tests/test_ei.py`: 9 unit tests (indicators, leap-day and year-crossing windows, RP bounds, synthetic extreme vs normal windows, trend detection, missing data).
- `src/wp1_sites.py`: 8 illustrative road corridors × 3 claim windows, plus product and baseline-length sensitivity.
- `src/wp1_map.py`: national EI maps (CHIRPS 0.25°) and CHIRPS vs ARC2 verdict agreement.
- `src/claim_schema.py`: the WP2 extraction schema (see `docs/wp2_source_register.md`).

The scenario is illustrative, not claim data: a contract awarded in 2018 with a 2-year TfC and a 1981–2017 baseline. To count as exceptional, an event then needs a return period of about 8–10 years.

## Results

**1. The index behaves sensibly.** MAM 2019 is not exceptional at any site (EI 0.6–1.2). OND 2019, the record short rains during the strong positive Indian Ocean Dipole, is exceptional on CHIRPS in 72% of Ugandan cells and at 6 of 8 sites. MAM 2020 is exceptional only in the east and north-east (Mt Elgon, Karamoja), in 32% of cells. NEC-style monthly tests agree: 62% of site-months in OND 2019 exceed the 1-in-10 value, against 4% in MAM 2019 (`results/wp1_site_ei.csv`, `wp1_nec_monthly.csv`, `figures/wp1_sites_ond2019.png`, `wp1_map_ei.png`).

**2. Which rainfall product is used decides the verdict.** For OND 2019 with the full baseline, CHIRPS and ARC2 give different verdicts at 6 of 8 sites. Hoima has EI 84 on CHIRPS and 1.1 on ARC2; Kampala 347 vs 4.8 (borderline); Gulu 3.4 vs 5.8. Nationally the two products agree on the verdict in only 68% of cells. Same weather, same contract, different answer. This is direct evidence for the WP5 recommendation that particular conditions name the climatic baseline dataset (FIDIC 2017 already points to Employer-supplied or published data for the site), and it is a likely mechanism behind disputes (`results/wp1_sensitivity.csv`, `figures/wp1_sensitivity_ond2019.png`).

**3. Baseline length matters less than product, except for short records.** Twenty-, thirty-year and full baselines give the same verdict at almost every site. A 10-year baseline (roughly what a new site gauge or a short UNMA record gives) cannot resolve an 8-year event: the empirical RP is capped at 11 years. Verdicts there are unstable and GEV fitting is not possible.

**4. A public dataset can contain a silent break.** ARC2 runs 1.3–3.2× CHIRPS nationally from January 2020 to September 2023 (national annual totals of about 2,150–2,310 mm in 2020–2022, against about 1,300 mm normally). Used naively, ARC2 would have made **every** cell "exceptional" in MAM 2020. The period is now masked (`QC_MASK` in `src/common.py`). Point for the paper: any contractual baseline needs a homogeneity check, and clauses should say who carries that data risk.

**5. Trends.** The non-stationary GEV shows no consistent sign in OND LWD trends at the sample sites (Masaka −1.7 days/decade, p = 0.004; others not significant). The national trend map and the stationary vs non-stationary comparison, the core novel element, are the next step.

## Methodological decisions and caveats

- **GEV extrapolation.** For record-breaking events the GEV gives return periods of hundreds of years from 37-year samples (capped at 1,000). These are not credible as point values: report them as "> 2n years" and rely on the verdict. The verdict is well-determined because the 8-year threshold lies inside the record.
- **Count indicators.** GEV is fitted to discrete LWD counts. This is acceptable as a first pass; test a negative-binomial or beta-binomial alternative for LWD.
- **Window choice.** Claimants choose the worst window. A fair test should fix the window ex ante (e.g. calendar months, or the contractual programme period) or adjust for selection; compare month, season and "any 30-day" windows.
- **Grid vs point.** A 0.25° cell average smooths point extremes. UNMA station data (requested in WP1 data access) is needed for a bias check.
- **LWD rule.** The 10 mm / 5 mm thresholds are placeholders. Validate against site diaries or newspaper "rain stopped works" events, and add a drying-day rule (the day after ≥25 mm also lost).

## Next steps

1. WP1: stationary vs non-stationary threshold map; selection-adjusted window test; LWD distribution alternatives; add ERA5 as a third product.
2. WP4 (quick win): apply the CMIP6 monthly deltas (`cmip6_deltas_obsgrid.nc`) to the baseline to estimate how often today's 8-year LWD threshold is exceeded in 2030–2060. Monthly delta scaling understates changes in extremes, so treat it as a lower bound until daily CMIP6 is bias-corrected.
3. WP2: download Auditor General VFM reports, search ULII directly, and pilot the LLM extraction on 5 documents with `data/claim_schema.json`.
