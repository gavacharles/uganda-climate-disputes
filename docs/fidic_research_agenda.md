# Determinable at tender: a data-driven research agenda on ambiguous FIDIC clauses

**Gavamukulya (Gava) Charles** · 15 October 2026 · scoping note (10 studies)

Clause numbers refer to FIDIC 2017 (Red Book unless stated), with 1999 equivalents in brackets. Check all clause wording against the primary texts before citing.

## The common thread

FIDIC allocates risk through tests that are decided *after the event*: "Unforeseeable", "exceptional", "should have become aware", "too slow", a cost index or rate chosen at tender and rarely checked. Each test depends on facts the contract does not fix: which data, which baseline, which date, which benchmark. The weather paper shows the pattern. A clause meant to allocate risk in advance becomes a source of dispute, and open data can make the test determinable at tender.

Each study below follows the same four-step design:

1. **Operationalise** the test with a reproducible, data-based index (the analogue of the Exceptionality Index).
2. **Measure the indeterminacy:** how often defensible choices of data or benchmark reverse the outcome.
3. **Ground it in practice:** contract and claim documents, anonymised.
4. **Propose a determinable rule:** drafting that fixes the data and benchmark at tender, tested on the same record.

**Shared assets.** Uganda as the main case; your OneDrive project files (Projects A–D and others) as evidence from practice; your existing data pipelines:

- CIPI: `Live-Tracker-Version-2-Uganda-Construction-Price-Intelligence-Platform`, `uganda-cipi-unsupervised-taxonomy`;
- remote sensing: `uganda-trade-corridors`;
- rainfall, floods and CMIP6: `uganda-rainfall-climate`;
- delay simulation: `uganda-seasons-construction-delay`.

**Shared outputs.** One paper each, an open "tender data pack" per clause (tables or tools an Employer can attach to tender documents), and a practitioner piece (Substack or LinkedIn).

---

## 1. Price adjustment: "same prices, different adjustment"

**Clause.** 13.7 Adjustments for Changes in Cost [1999: 13.8], with the Schedule of Cost Indexation (Contract Data).

**What it leaves open.** The formula Pn = a + b·Ln/Lo + c·En/Eo + … depends on:

- which indices are named;
- their weightings, including the fixed non-adjustable element *a*;
- the base date;
- the currency of each element;
- what happens when an index is revised, rebased, delayed or discontinued (provisional indices, later correction).

Disputes arise when the named index does not track what the Contractor actually paid, such as fuel or bitumen in 2022, or when a weighting was inherited from another contract.

**Research questions.**

1. How much does the adjustment on the same contract vary across defensible index and weighting choices?
2. How well does the contractual formula track actual input-cost movements (cost pass-through), and for whom does the error fall?
3. What does index revision, rebasing or discontinuation do to settled adjustments?
4. Which formula specification (index basket, weights from the BoQ, update rule) minimises tracking error and dispute exposure?

**Data and access.**

- UBOS CIPI and its components (in hand from your PhD pipeline).
- UBOS CPI, fuel pump prices, bitumen import prices, cement and steel prices, BoU exchange rates (open).
- BoQs and price-adjustment schedules from contracts (in your files; Projects A–D's Contract Data).

**Method.** Recompute Pn for many contracts (real schedules plus synthetic contracts built from BoQ cost shares) under alternative index sets and weights. Benchmark against a "true cost" series built from BoQ quantities × input prices. Measure tracking error, the share of cost shocks passed through, and the verdict dispersion across choices. Run event studies around the 2022 fuel/bitumen shock and the CIPI rebasing.

**Novelty.** Price-adjustment literature is mostly econometric (escalation forecasting) or doctrinal. No study measures the indeterminacy of the FIDIC formula against actual cost paths in an African market.

**Evidence from practice.** Price-adjustment disputes appear in your claims folders (e.g. variation-of-price items in the Mubende–Mityana Employer's comments). Check the Contract Data of Projects A–D for index schedules.

**Outputs.** Paper. An open "tender index pack" (recommended index basket and BoQ-derived weights by work type) for Uganda.

**Journals.** J. Construction Engineering and Management (ASCE); Construction Management and Economics; J. Legal Affairs & Dispute Resolution.

**Feasibility.** High: data largely in hand. **4–6 months.** **Risks:** limited actual-cost data; mitigate with BoQ-based synthetic cost paths.

---

## 2. Access to the Site: when was possession really given?

**Clause.** 2.1 Right of Access to the Site [1999: 2.1]; Contract Data milestones for handover of sections. Linked to 8.5 (EOT) and 20.

**What it leaves open.**

- The date access was actually given, section by section.
- Whether partial or encumbered access counts.
- How much of the delay was caused by the Contractor's own document delays (the 2.1 proviso).

Land acquisition and right-of-way encumbrances are the dominant delay cause on Ugandan roads. In Project A, the possession heads (158 days and more) dwarf weather.

**Research questions.**

1. Can satellite imagery establish an objective, section-level date of clearance and possession?
2. How do Engineer-determined possession delays compare with the remotely sensed record?
3. How should contracts define "access" (clearance thresholds, minimum continuous length) to make it verifiable?

**Data and access.**

- Sentinel-2 (10 m, five-day revisit), Planet (research access), Google Open Buildings temporal, the GHSL built-up layer.
- OpenStreetMap; corridor alignments from contract drawings.
- RAP compensation status reports (Project A's "ROW Acquisition Status" appendix is in your files).

**Method.**

- Detect building removal and vegetation clearing along the corridor buffer with change detection (NDVI and built-up indices, time-series breakpoints).
- Derive "cleared length" per 1 km section and month, and compare with handover milestones and EOT determinations.
- Validate against site photographs and handover certificates.

**Novelty.** Remote sensing has been used for progress monitoring, but not to adjudicate *Employer* possession obligations or to quantify encumbrance as a contractual fact.

**Evidence from practice.**

- Project A: EOTs 3, 5 and 7, with possession delays of 472, 765 and 849 days, and the DAB referral on possession and design overlap.
- Other projects: KKAT–CRSG correspondence.

**Outputs.** Paper. A reproducible "corridor clearance tracker" that Engineers could use monthly.

**Journals.** Automation in Construction; J. Legal Affairs & Dispute Resolution; J. Construction Engineering and Management.

**Feasibility.** Medium–high: method from `uganda-trade-corridors`. **6–8 months.** **Risks:** cloud cover (use Sentinel-1 radar); small structures below 10 m resolution (use Planet or Open Buildings).

---

## 3. Unforeseeable Physical Conditions: a "foreseeability index"

**Clause.** 4.12 Unforeseeable Physical Conditions [1999: 4.12], with 4.10 Use of Site Data and 4.11 Sufficiency of the Accepted Contract Amount. "Unforeseeable" (1.1.87) means not reasonably foreseeable by an experienced contractor by the Base Date. Climatic conditions are excluded.

**What it leaves open.**

- What an experienced contractor should have inferred from the site data and other available information.
- How much investigation was reasonable.
- The boundary with weather: groundwater raised by rain.

**Research questions.**

1. Given data available at the Base Date, how probable was the encountered condition? Build a foreseeability index.
2. How does site-investigation density (boreholes per km, test pits) change foreseeability, and therefore who bears the risk?
3. Can data separate 4.12 physical conditions from 8.5(c) climatic conditions (e.g. groundwater response to rainfall)?

**Data and access.**

- Geological survey maps (Uganda DGSM); ISRIC SoilGrids (250 m; clay, bulk density, depth to bedrock); groundwater (Ministry of Water and Environment); expansive-soil maps.
- Site-investigation reports in contract documents (Projects A–D annexes).
- Claimed conditions from claim files.

**Method.** Spatial prediction of ground properties from Base-Date data (kriging or random-forest on SoilGrids and boreholes). Compute the probability of the encountered condition (e.g. rock at depth, black cotton soil thickness) at the claimed location. Study how probability falls with investigation density. Test the rain–groundwater link with CHIRPS and water-table records.

**Novelty.** 4.12 is the most litigated FIDIC clause, but the doctrinal test has never been operationalised probabilistically. This is a direct twin of the weather paper.

**Evidence from practice.** Search claims folders for 4.12 claims (rock, unsuitable material, groundwater). Project D's addendum notes that "the available [geology] data is out of date". That is itself evidence of the Base-Date problem.

**Outputs.** Paper. A "ground-risk register at tender" template with probability bands.

**Journals.** J. Legal Affairs & Dispute Resolution; Construction Management and Economics; Engineering Geology (for the method).

**Feasibility.** Medium: needs borehole data from projects. **6–9 months.** **Risks:** few georeferenced boreholes; mitigate with project site-investigation annexes and the national borehole database.

---

## 4. Defects, design and overloading: who broke the road?

**Clause.** 11 Defects after Taking Over (11.1–11.4), 4.1 (Yellow Book, fitness for purpose), and the Employer's risks relating to use and occupation. In practice the question is whether early pavement failure is a design, workmanship or overloading problem.

**What it leaves open.** Causation of defects within the Defects Notification Period: actual traffic loading against design loading, maintenance, drainage.

**Research questions.**

1. How much did actual cumulative axle loading (ESALs) exceed design loading on Ugandan national roads?
2. Can loading data apportion responsibility for early failures?
3. What contract mechanism (load-adjusted defects liability, axle-load monitoring obligation) would make causation determinable?

**Data and access.**

- UNRA axle-load control and weighbridge statistics, traffic counts (request; some published in annual reports).
- Pavement roughness (IRI) and condition surveys (UNRA; World Bank RONET).
- Design traffic from pavement design reports (in contract documents).

**Method.** Compare design ESALs with observed ESALs from traffic and axle-load surveys. Estimate the expected service life under observed loading with mechanistic-empirical models. Relate condition deterioration to loading, and build a causation-apportionment model for defects claims.

**Novelty.** Engineering literature studies overloading and deterioration. Nobody has connected this to contractual defect liability and dispute allocation.

**Evidence from practice.** Defects and guardrail or road-sign claims in UNRA folders. Look for DNP disputes in your files.

**Outputs.** Paper. A proposed "load-adjusted defects" clause and monitoring protocol.

**Journals.** J. Infrastructure Systems (ASCE); International Journal of Pavement Engineering; J. Legal Affairs & Dispute Resolution.

**Feasibility.** Medium–low: depends on UNRA data access. **8–12 months.** **Risks:** data access; mitigate through partnership with UNRA or the Ministry of Works.

---

## 5. Delay Damages: penalty or pre-estimate?

**Clause.** 8.8 Delay Damages [1999: 8.7]; Contract Data rate (often 0.05% of the Contract Price per day, capped at 10%).

**What it leaves open.** Whether the rate is enforceable: a genuine pre-estimate, or proportionate to a legitimate interest (*Cavendish v Makdessi*; Ugandan courts apply common-law principles). The same percentage is applied to rural and urban roads alike.

**Research questions.**

1. What does a day of late completion actually cost the public (road-user costs: vehicle operating costs, travel time) on Ugandan roads?
2. How does the standard 0.05%/day compare with that loss across the network?
3. What rate rule (traffic-based) would be proportionate and defensible?

**Data and access.**

- Traffic counts (UNRA; the OSM-derived models from `uganda-trade-corridors`).
- Vehicle operating cost models (HDM-4 parameters, World Bank RONET).
- Contract prices and delay-damages rates from tender documents.

**Method.** For each road, compute the daily benefit forgone by comparing the improved and existing road, using HDM-4/RONET unit costs and traffic. Compare with the delay-damages rate × contract price, then map ratios across the network.

**Novelty.** Delay-damages enforceability is doctrinal. An empirical proportionality test across a national network has not been done.

**Evidence from practice.** Project B Contract Data (0.05%/day). "Appraising the Possibility of Levying Delay Damages" (UNRA claims folder) is a ready vignette.

**Outputs.** Paper. A rate calculator for Contract Data.

**Journals.** J. Legal Affairs & Dispute Resolution; Transport Policy; J. Construction Engineering and Management.

**Feasibility.** High. **3–5 months.** **Risks:** traffic data gaps; mitigate with modelled traffic.

---

## 6. Notice time bar: when "should" the Contractor have known?

**Clause.** 20.2.1 Notice of Claim [1999: 20.1]. Notice is due within 28 days after the claiming Party "became aware, or should have become aware" of the event. Failure is a time bar, subject in 2017 to 20.2.5 (the DAAB may consider late notice).

**What it leaves open.** The constructive-awareness date. Time-bar disputes are common and decisive.

**Research questions.**

1. For data-observable events (rainfall thresholds, index publications, possession status, exchange-rate shocks), what is the objective date a reasonable contractor could have known?
2. How often would claims in practice be time-barred under an objective date versus the dates the parties used?
3. Can contracts define awareness dates by reference to named data releases?

**Data and access.** As for studies 1–3 and 7, plus notice letters and claim submission dates (in your files: Project A EOT notices, Project D notices).

**Method.** For each event type, define a detection rule (e.g. the first day the monthly lost-working-day count exceeds the 1-in-10 value, or the index publication date). Compute the constructive-awareness date and compare it with notice dates in claim files.

**Novelty.** Time-bar scholarship is doctrinal. This is the first attempt to define "should have become aware" empirically.

**Evidence from practice.** Your files contain dated notices and determinations, enough for a pilot on 20–40 events.

**Outputs.** Paper. A "notice clock" specification for Particular Conditions.

**Journals.** J. Legal Affairs & Dispute Resolution; Construction Law Journal; International Construction Law Review.

**Feasibility.** High, as an extension of the weather paper. **3–4 months.** **Risks:** small n; frame as a methods paper with case vignettes.

---

## 7. Exceptional Events: how exceptional was it?

**Clause.** 18 Exceptional Events [1999: 19 Force Majeure]: an event beyond a Party's control, which could not reasonably have been provided against, could not reasonably have been avoided once it arose, and is not substantially attributable to the other Party. Listed examples include riot, commotion and natural catastrophes.

**What it leaves open.** Whether unrest, election violence, epidemics or floods meet the test, and the extent of the effect on the works.

**Research questions.**

1. How unusual, for place and time, were the events claimed (unrest, COVID-19 restrictions, floods), measured against historical event data?
2. Do claimed durations match the measured duration and intensity of the event?
3. What objective trigger (event density thresholds, government-order dates) could Particular Conditions adopt?

**Data and access.**

- ACLED (conflict and unrest events, geolocated, dated; free registration).
- Oxford COVID-19 Government Response Tracker; Google mobility (archived).
- Flood return periods from the rainfall project.
- Gazette dates of government orders.

**Method.** Event-density anomalies within a radius of the site against a 10-year baseline, using a return-period approach as in the weather paper. Restriction stringency timelines are compared with claimed periods.

**Novelty.** No empirical treatment of force-majeure or Exceptional Event claims exists. COVID-19 claims make this timely.

**Evidence from practice.** Project A: 230 days claimed for COVID-19 (10 Mar – 20 Sep 2020), 194 granted, overlapping possession delay. Ideal for comparing the stringency timeline with the claim.

**Outputs.** Paper. An "exceptional event trigger" annex.

**Journals.** J. Legal Affairs & Dispute Resolution; International Journal of Disaster Risk Reduction; Construction Management and Economics.

**Feasibility.** High. **4–6 months.** **Risks:** attribution of delay to the event; use the case-file programme evidence.

---

## 8. Forces of nature and care of the Works: whose flood?

**Clause.** 17.2 Liability for Care of the Works with Employer's risks in 17.2(d) [1999: 17.3(h)], which covers forces of nature that are Unforeseeable or against which an experienced contractor could not reasonably have taken adequate preventive precautions.

**What it leaves open.** Whether flood, landslide or storm damage to temporary or permanent works was Unforeseeable, and what precautions were reasonable, including temporary works designed to what return period.

**Research questions.**

1. What return period did damaging events have at the site, from rainfall, river-flow and flood models?
2. What return period should temporary works (diversions, culverts, cofferdams) be designed for, given a contract duration?
3. Can a design-standard reference (e.g. temporary works to a 1-in-10-year event over the contract period) make the test determinable?

**Data and access.** CHIRPS and IMERG rainfall; river gauges (Ministry of Water and Environment); flood models and DEMs from `uganda-rainfall-climate` (the Kampala flood work); damage reports in claim files.

**Method.** Rainfall-runoff or flood-frequency analysis at damaged structures; event return periods; the probability of exceedance during the contract (1 − (1 − 1/T)^n) for different temporary-works standards.

**Novelty.** Links hydrological design standards to contractual risk allocation, which is absent from the literature. A sister paper to the weather study, with a different clause.

**Evidence from practice.** Search for washout or damage claims in your files (Projects A–D monthly reports).

**Outputs.** Paper. A temporary-works design-standard clause.

**Journals.** J. Legal Affairs & Dispute Resolution; J. Flood Risk Management; Natural Hazards Review (ASCE).

**Feasibility.** Medium–high. **4–6 months.** **Risks:** few damage events with locations; use case vignettes plus national hazard maps.

---

## 9. Delayed Payment: does the financing charge compensate?

**Clause.** 14.8 Delayed Payment [1999: 14.8]: financing charges at the rate stated in the Contract Data, by default 3 percentage points above the central bank discount rate in the currency of payment, compounded monthly.

**What it leaves open.**

- Which reference rate (BoU Central Bank Rate vs rediscount rate; foreign-currency portions).
- Whether the charge compensates actual financing costs.
- When "due" starts.

Late payment is endemic on Ugandan public works and drives other claims (suspension in Project C).

**Research questions.**

1. How long are payment delays on Ugandan public works, and how do they vary by Employer and budget cycle?
2. How does the contractual financing charge compare with contractors' actual borrowing costs (commercial lending rates)?
3. How do payment delays propagate into suspension, slowdown and other claims?

**Data and access.**

- Interim payment certificate dates and payment dates from project files and Auditor General reports.
- BoU policy, rediscount and commercial lending rates (open).
- Ministry of Finance budget-release calendars.

**Method.** Survival analysis of payment delays; the gap between the financing charge and the cost of funds; regression or event analysis linking delays to subsequent claims.

**Novelty.** Payment-delay studies are survey-based. This would measure the adequacy of the contractual remedy with actual rates and delays.

**Evidence from practice.** Project C (suspension after non-payment); the "Govt losing Shs342 million per day to unpaid road contractors" reporting (2022).

**Outputs.** Paper. Recommended Contract Data rates by currency.

**Journals.** Construction Management and Economics; J. Legal Affairs & Dispute Resolution; Engineering, Construction and Architectural Management.

**Feasibility.** Medium: needs payment-date data. **5–7 months.** **Risks:** data access; use Auditor General reports and project files.

---

## 10. Rate of progress and termination: how slow is "too slow"?

**Clause.** 8.7 Rate of Progress [1999: 8.6]; 15.1 Notice to Correct; 15.2 Termination for Contractor's Default (failing to proceed in accordance with Clause 8). 1999 15.2(c): "fails without reasonable excuse… to proceed with the Works in accordance with Clause 8".

**What it leaves open.** "Too slow to complete by the due date" and "proceed with due expedition and without delay" have no benchmark. Termination for slow progress is high-stakes and often disputed (e.g. the terminated contracts in your client and referral folders).

**Research questions.**

1. What do progress curves (S-curves) of completed Ugandan road contracts look like, and what share of contracts behind at month *t* still finished on time (recovery probability)?
2. Can satellite-measured progress (earthworks and surfacing extent) reproduce reported progress?
3. What objective threshold (e.g. a recovery probability below *p* at time *t*) could define "too slow"?

**Data and access.** Monthly progress reports (in your files for several projects); Auditor General physical-progress data; Sentinel-2 or Planet imagery for surfacing progress along alignments.

**Method.** Build an empirical S-curve library; estimate recovery probabilities conditional on the progress gap; validate reported progress with remote sensing.

**Novelty.** No empirical benchmark for the contractual "too slow" test exists. Remote-sensing verification of progress for termination decisions is new.

**Evidence from practice.** Termination determinations and referrals in your files (e.g. "Supervisor's Final Determination of Termination Claim No. 3"); slow-progress comments in Project B's monthly report.

**Outputs.** Paper. A progress-threshold annex for Particular Conditions.

**Journals.** J. Construction Engineering and Management; Automation in Construction; J. Legal Affairs & Dispute Resolution.

**Feasibility.** Medium. **6–9 months.** **Risks:** few complete progress histories; pool Auditor General data.

---

## Prioritisation and roadmap

| # | Study | Data in hand | Novelty | Effort | Priority |
|---|---|---|---|---|---|
| 1 | Price adjustment (13.7) | High (CIPI) | High | 4–6 mo | **1** |
| 6 | Notice time bar (20.2.1) | High (extends weather) | High | 3–4 mo | **2** |
| 5 | Delay damages (8.8) | High | Medium–high | 3–5 mo | **3** |
| 7 | Exceptional Events (18) | High | High (COVID) | 4–6 mo | **4** |
| 2 | Site access (2.1) | Medium (method ready) | High | 6–8 mo | **5** |
| 8 | Forces of nature (17.2) | Medium–high | Medium–high | 4–6 mo | 6 |
| 3 | Unforeseeable ground (4.12) | Medium | Very high | 6–9 mo | 7 |
| 10 | Rate of progress (8.7/15.2) | Medium | High | 6–9 mo | 8 |
| 9 | Delayed payment (14.8) | Medium–low | Medium | 5–7 mo | 9 |
| 4 | Defects and overloading (11) | Low (UNRA data) | High | 8–12 mo | 10 |

**Suggested sequence (2027–2028).**

- **First half of 2027:** studies 1 and 6. One uses data already in hand; the other extends the weather paper.
- **Second half of 2027:** studies 5 and 7.
- **2028:** studies 2 and 8 (remote sensing and hydrology), then 3 and 10.
- **Running throughout:** request the data for studies 4 and 9 (UNRA, MoFPED) so they are ready later.

**As a programme.** The ten studies form a coherent research agenda, *Determinable at tender: open data for construction contract risk allocation*, suitable for:

- a postdoctoral fellowship proposal (e.g. AfDB, Leverhulme, Marie Skłodowska-Curie Global, African Academy of Sciences);
- a FIDIC or ICC research grant;
- a monograph or edited volume;
- an open "tender data pack" platform for Ugandan public procurement (PPDA/UNRA), a practical output with policy reach.

**Synthesis paper (after 4–5 studies).** "When risk allocation creates disputes: the post-event determination problem in FIDIC contracts", a cross-clause review using the measured indeterminacies, targeted at the International Construction Law Review or the J. Legal Affairs & Dispute Resolution.

**Ethics and confidentiality.** All project documents remain confidential and are reported anonymised. A data-access agreement with UNRA or the Ministry of Works would widen the evidence base and strengthen every study.
