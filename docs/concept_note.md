# Same rain, different verdict: climate data, contract forms and "exceptionally adverse climatic conditions" in Uganda

**Concept note (revised)** · Gavamukulya (Gava) Charles · 14 October 2026

*Revision: the paper no longer depends on claim records from Auditor General reports, PPDA or ULII. It studies how the contractual weather test itself, through the data it leaves unspecified, the form of contract and a changing climate, creates entitlement and dispute risk. Claim-outcome modelling moves to a follow-on paper if partner claim files become available (§12).*

## 1. Summary

**Working title:** *Same rain, different verdict: how data choices, contract forms and climate change decide "exceptionally adverse climatic conditions" in construction contracts. Evidence from Uganda.*

Construction contracts give contractors extra time when "exceptionally adverse climatic conditions" delay the works, but no contract says what "exceptional" means in numbers, or which data decides it. This study turns the FIDIC test into a reproducible, site-specific Exceptionality Index (EI) built from 45 years of gridded daily rainfall. It then asks three questions no study has answered:

1. How often do reasonable but different data choices (rainfall dataset, baseline length, claim window, trend-aware or fixed baseline) flip the verdict? The answer maps where disputes are built into the data.
2. Under the same weather, how much relief do FIDIC, NEC and JCT-style tests give a typical 3-year Ugandan contract?
3. How will climate change (CMIP6, to 2050) shift how often today's threshold is crossed?

The output is a set of evidence-based drafting recommendations and an open tool.

## 2. Background and problem

- **The clause.** FIDIC Red/Yellow Book 2017 Sub-Clause 8.5(c) gives an extension of time (not money) for "exceptionally adverse climatic conditions". The 2017 edition ties these conditions to the Site and to climatic data: conditions "which are Unforeseeable having regard to climatic data" provided by the Employer or published for the site's location. It does not say which data, over what period, or how to compare. The 1987 and 1999 editions did not define the term. The 2017 Silver Book (EPC) gives no relief. [Gowling WLG](https://gowlingwlg.com/en/insights-resources/articles/2024/adverse-weather-claims); [Vinson & Elkins](https://www.velaw.com/insights/when-you-walk-through-a-storm-legal-implications-of-adverse-weather-on-construction-contracts)
- **The only numerical guidance is a rule of thumb.** The FIDIC Contracts Guide (2000) treats as exceptional an event whose return period is 4 to 5 times the Time for Completion. A typical 3-year Ugandan public works contract therefore needs roughly a 1-in-12 to 1-in-15-year event. [Vinson & Elkins](https://www.velaw.com/insights/when-you-walk-through-a-storm-legal-implications-of-adverse-weather-on-construction-contracts)
- **Other forms use a different test.** NEC4 (cl. 60.1(13)) compares each calendar month with its 1-in-10-year weather and compensates only the excess. In the UK, JCT practice compares months with Met Office 10-year records. [Gowling WLG](https://gowlingwlg.com/en/insights-resources/articles/2024/adverse-weather-claims)
- **Why it is disputed.** There is little case law. The test is applied after the event, and the parties choose the data, the period and the comparison. Practitioners note that climate change may shift what counts as "unforeseeable". [Gowling WLG](https://gowlingwlg.com/en/insights-resources/articles/2024/adverse-weather-claims)
- **Why Uganda.** Weather ranks among the top causes of delay on Ugandan projects: second on roads in a Makerere study, and 25% of responses for public buildings (KIU, 2025). Most public works use FIDIC-based or PPDA standard contracts. Uganda has two rainy seasons, sparse and short station records, and several competing satellite rainfall products. The parties rarely share a baseline. [KIU 2025](https://kjset.kiu.ac.ug/assets/articles/1751038549_investigating-the-dynamics-of-delays-in-public-building-projects-in-uganda.pdf); [Makerere](https://dissertations.mak.ac.ug/handle/20.500.12281/15496); [MoFPED BMAU](https://archive.finance.go.ug/sites/default/files/Publications/BMAU%20Briefing%20Paper%207-13%20-Delays%20and%20cost%20overruns%20in%20the%20construction%20of%20roads.%20Can%20the%20causes%20be%20mitigated.pdf)

## 3. Research gap

1. **No operational definition of "exceptional".** The legal commentary gives no reproducible, location-specific method for FIDIC 8.5(c), especially where station data is sparse.
2. **Nobody has measured how much the test leaves open.** Commentary says the test is subjective. No study quantifies how often defensible data choices reverse the verdict, or where.
3. **Contract forms have never been compared on the same weather.** FIDIC, NEC and JCT allocate weather risk differently in principle. No study has computed what each actually gives under a real climate record, let alone in a tropical climate with two rainy seasons.
4. **There is no forward view.** No study estimates how a warming climate changes how often the contractual threshold is crossed, or who carries the drift of a baseline fixed at award.
5. **The dispute literature ignores climate.** A 2025 review of 19 AI-for-construction-disputes studies found none using external hazard data. [Francis et al., 2025, ITcon](https://itcon.org/paper/2025/29) This paper supplies the hazard side; linking it to outcomes is the follow-on (§12).

## 4. Aim, objectives and research questions

**Aim:** a transparent, data-based method for deciding when weather is contractually exceptional; evidence of how much the current test leaves open; and a measure of how contract form and climate change move the line, in Uganda.

| # | Research question | Output |
|---|---|---|
| RQ1 | How can "exceptionally adverse climatic conditions" be turned into a reproducible, site- and season-specific test using gridded climate data? | Exceptionality Index (EI) + open tool |
| RQ2 | How sensitive is the verdict to the choices the contract leaves open: rainfall dataset, baseline length, claim window, stationary vs trend-aware baseline? | Verdict-sensitivity statistics; **dispute-risk map** |
| RQ3 | Under the same weather, how often and how much relief do FIDIC (Guide rule), NEC4 and JCT-style monthly tests give a 3-year contract? | Relief probability and expected relief days per contract, by form and location |
| RQ4 | How will the frequency of threshold-crossing events change by 2050 under SSP2-4.5 and SSP5-8.5? | Projected exceedances and expected relief by region and season |
| RQ5 | What should contracts say about climatic data, baselines and risk sharing? | Drafting recommendations, tested with experts |

## 5. Conceptual framework

```
Climate record ──► Contractual test ──────────────────► Entitlement ──► Dispute risk
(45 yr daily rain,  (choices: dataset, baseline,         (relief yes/no,  (verdict flips under
 CMIP6 to 2050)      window, trend; form: FIDIC/NEC/JCT)   relief days)     defensible choices)
       ▲                        ▲
 Exceptionality Index (RQ1)   Sensitivity (RQ2), forms (RQ3), climate change (RQ4)
```

The study holds the weather fixed and varies the contractual test. Where defensible choices give opposite answers, a dispute is likely whatever the facts on site.

## 6. Data sources

| Data | What it gives | Access | Status |
|---|---|---|---|
| CHIRPS v2 daily (0.25°, 1981–) | Primary rainfall product | Open | In hand |
| ARC2 daily (0.1°, 1983–) | Second product for RQ2 | Open | In hand; inhomogeneous Jan 2020–Sep 2023 (masked) |
| ERA5 / ERA5-Land | Third product; temperature and wind for multi-hazard EI | Open (CDS) | To fetch |
| NASA POWER | Temperature, wind, humidity | Open | In hand |
| UNMA station records | Bias check of gridded products | Request | Ask for 10–15 synoptic stations |
| CMIP6 (16-model ensemble) | 2030–2060 projections | Open | Monthly deltas in hand; daily to fetch |
| Newspaper corpus (`~/Projects/uganda-urban-headlines`) | Dated "rains halt works" events | Own | Validation of the lost-working-day rule |
| ClaimsExpertData `kb.sqlite` | Adverse-weather case law (739 chunks) | Own | For the legal review (permission pending) |
| Expert interviews (8–12) | Practice on baselines and datasets; ranking of drafting options | Primary | To schedule |

**Unit of analysis:** a hypothetical contract defined by site, start month and Time for Completion (default 3 years), evaluated over every start month 1991–2023 and every CHIRPS cell in Uganda (about 375 cells × 385 starts).

## 7. Methods

**WP1. Exceptionality Index (RQ1).** *Built: `src/ei.py`.*
- For a site and window, compute lost working days (LWD; ≥ 10 mm/day earthworks, ≥ 5 mm/day surfacing), totals, wet spells, Rx1day and Rx5day.
- Compare with the same calendar window in each baseline year. Return period by three methods: empirical, stationary GEV, and non-stationary GEV (trend in location).
- EI = return period ÷ Time for Completion; exceptional at EI ≥ 5, borderline 4–5 (FIDIC Guide). Plus the NEC monthly 1-in-10 test.

**WP2. Verdict sensitivity and dispute-risk map (RQ2).**
- For each cell and season, recompute the verdict under each defensible choice: product (CHIRPS, ARC2, ERA5), baseline (10/20/30 years, full record), window (calendar season, calendar months, worst 30/60/90 days), and stationary vs trend-aware.
- Dispute risk = share of choice combinations that disagree with the majority verdict. Map it, and test whether it is higher where products disagree on extremes or where trends are strong.
- Data-quality screen: homogeneity tests on every product (the ARC2 2020–2023 break is a case study).

**WP3. Contract forms on the same weather (RQ3).** *First version built: `src/rq3_forms.py`.*
- For every 3-year contract (each start month 1991–2023) in every cell, apply the FIDIC Guide test (season LWD with return period ≥ 15 years), the NEC4 monthly test (1-in-10 rainfall or days ≥ 5 mm; relief = excess over 1-in-10 weather), and a JCT-style monthly test (same trigger; relief = excess over average). FIDIC Silver gives none.
- Outputs: probability of at least one relief event, and expected relief days, per contract.
- Robustness: out-of-sample baselines, Time for Completion of 1–5 years, the 4× vs 5× rule.

**WP4. Climate projections (RQ4).**
- First pass: apply CMIP6 monthly delta factors to the observed daily series. This is a lower bound for changes in extremes.
- Main analysis: bias-correct daily CMIP6 precipitation (quantile mapping to CHIRPS) and recompute the WP3 metrics for 2030–2060 under SSP2-4.5 and SSP5-8.5.
- Quantify baseline drift: how a baseline fixed at award under- or over-states risk over a 3-year contract and over a 30-year asset programme.

**WP5. Validation and synthesis (RQ5).**
- Validate the LWD rule and EI against dated newspaper reports of work stoppages (event-level, not claim-level).
- Draft model particular conditions: a named climatic dataset with a homogeneity check, a defined window, a trend-aware or periodically updated threshold, and a shared-risk band. Test them in 8–12 expert interviews (PPDA, UNRA, FIDIC-accredited adjudicators, contractors).

## 8. Expected contributions and novelty

1. The first reproducible, open method to quantify FIDIC 8.5(c) from gridded data, usable where station data is sparse.
2. The first measure of how much the "exceptional" test leaves open, with a dispute-risk map: places where the verdict depends on the dataset rather than the weather.
3. The first like-for-like comparison of FIDIC, NEC and JCT-style weather relief under a real climate record, showing how much weather risk each form moves to the employer.
4. Expected weather relief per contract, a contingency figure that estimators and employers can use.
5. A forward-looking estimate of climate-driven change in contractual weather risk in sub-Saharan Africa.
6. An open tool: enter site, dates and Time for Completion; get EI, return periods and the verdict under each form.

**First results (WP1, illustrative 2018 award, 3-year Time for Completion):**
- OND 2019 is exceptional at 5 of 8 sample corridors and MAM 2019 at none.
- CHIRPS and ARC2 give opposite verdicts in about a third of Uganda for OND 2019.
- ARC2 contains a silent wet bias from 2020 to 2023 that would make every MAM 2020 claim "exceptional".

See `docs/wp1_notes.md`.

## 9. Risks, limitations and ethics

| Risk | Mitigation |
|---|---|
| Reviewers ask "where are the real claims?" | Frame as entitlement and dispute *risk*, not outcomes; validate against dated stoppage events; expert interviews; partner case vignettes where available |
| Gridded products miss point extremes | Three products plus UNMA stations; report product uncertainty (it is itself a finding) |
| GEV extrapolation for record events | Report verdicts, not point return periods, beyond 2× the record length |
| LWD thresholds are stylised | Sensitivity to 5/10/15 mm rules and a drying-day rule; validate with news events |
| Hypothetical contracts are not real programmes | Use all start months, multiple Time for Completion values; season-specific results show programming effects |
| Legal interpretation | Frame as quantitative analysis of tests, not legal advice; check primary FIDIC/NEC texts before citing |

## 10. Work plan (12 months)

| Months | Work |
|---|---|
| 1–2 | Legal review (FIDIC, NEC, JCT texts; case law); ERA5 and daily CMIP6 downloads; UNMA request |
| 1–3 | WP1 complete (done in prototype); WP3 forms comparison (first version done) |
| 3–5 | WP2 sensitivity and dispute-risk map |
| 5–7 | WP4 projections |
| 6–8 | WP5 news validation; tool release |
| 8–10 | Expert interviews; drafting recommendations |
| 9–12 | Paper A drafting and submission; outreach brief |

**Paper A** (this note): RQ1–RQ5. **Paper B** (§12): claim outcomes, if partner data allows.

## 11. Target journals

| Journal | Fit |
|---|---|
| Journal of Legal Affairs and Dispute Resolution in Engineering and Construction (ASCE) | **First choice**: contract test, dispute risk, drafting |
| Climate Risk Management | Climate-risk allocation framing, projections |
| Journal of Construction Engineering and Management (ASCE) | Quantitative contract-risk analysis |
| Engineering, Construction and Architectural Management | Developing-country construction management |

## 12. Follow-on: claim outcomes (Paper B)

If partner claim files (consultants, contractors, UNRA) become available, link EI to claimed vs granted days and outcomes, and model the drivers (records, form, baseline cited) with interpretable ML. The extraction schema is ready (`src/claim_schema.py`). The public-record scan (`docs/wp2_source_register.md`) found Auditor General reports too general and PPDA Tribunal decisions out of scope, so partner data is required.

## 13. Key references

- Francis, M., Perera, S., Zhou, W., Nanayakkara, S. (2025). Artificial intelligence applications for proactive dispute management in the construction industry: a systematic literature review. *ITcon* 30, 711–730. https://itcon.org/paper/2025/29
- Gowling WLG (2024). Adverse weather claims. https://gowlingwlg.com/en/insights-resources/articles/2024/adverse-weather-claims
- Vinson & Elkins. When you walk through a storm: legal implications of adverse weather on construction contracts. https://www.velaw.com/insights/when-you-walk-through-a-storm-legal-implications-of-adverse-weather-on-construction-contracts
- FIDIC (2000). *The FIDIC Contracts Guide*; FIDIC (2017). Conditions of Contract for Construction (Red Book), Sub-Clause 8.5. NEC4 Engineering and Construction Contract, cl. 60.1(13). Check primary texts before citing.
- KIU Journal of Science, Engineering and Technology (2025). Investigating the dynamics of delays in public building projects in Uganda. https://kjset.kiu.ac.ug/assets/articles/1751038549_investigating-the-dynamics-of-delays-in-public-building-projects-in-uganda.pdf
- Makerere University dissertation. Effect of excessive variations on time performance of road projects in Uganda. https://dissertations.mak.ac.ug/handle/20.500.12281/15496
- MoFPED BMAU Briefing Paper 7/13. Delays and cost overruns in the construction of roads. https://archive.finance.go.ug/sites/default/files/Publications/BMAU%20Briefing%20Paper%207-13%20-Delays%20and%20cost%20overruns%20in%20the%20construction%20of%20roads.%20Can%20the%20causes%20be%20mitigated.pdf
- KTA Advocates (2023). Effects of delays in Uganda's road construction projects: a case for DAABs. https://www.ktaadvocates.com/wp-content/uploads/2023/01/EFFECTS-OF-DELAYS-IN-UGANDAS-ROAD-CONSTRUCTION-PROJECTS-A-CASE-FOR-DISPUTE-ADJUDICATION-ADD-ARBITRATION-BOARDS-DAABS.pdf
- Funk, C. et al. (2015). The climate hazards infrared precipitation with stations (CHIRPS). *Scientific Data* 2, 150066.
- Novella, N.S., Thiaw, W.M. (2013). African Rainfall Climatology Version 2 (ARC2). *J. Appl. Meteor. Climatol.* 52, 588–606.
