# WP2 source register

First scan, 14 October 2026. Status of each planned claim source and what it can realistically give.

| Source | Expected yield | Status | Notes |
|---|---|---|---|
| Auditor General VFM / annual audits (auditorgeneral.go.ug) | EOTs granted per project; causes listed in general terms | To download | Reports give EOT counts and durations (e.g. Kitale–Gerenge, three EOTs; Kampala Northern Bypass, 3 → 7.5 years) and cite "heavy rains" as a reason for incomplete LG roads. A first search found no claim-level weather EOT detail. Need the full PDFs; extract per-project EOT tables. |
| PPDA Appeals Tribunal (ulii.org/judgments/UGPPDPAAT) | **Low** for this study | Checked | Decisions found are procurement reviews (bid challenges, filing deadlines), not disputes over how contracts were carried out. Keep only for contract-form and time-bar context. **The concept note should be revised: this is not a main source of claim outcomes.** |
| ULII Commercial Division / High Court / Court of Appeal | Litigated EOT and delay disputes; high-quality labels, small n | To search on ulii.org directly | Web search returned no indexed weather-EOT judgment; search ULII with "extension of time", "inclement weather", "adverse climatic", "rain", "FIDIC". |
| UNRA annual / performance reports; Uganda Road Fund | EOT days per contract | To download | |
| World Bank ICRs / AfDB PCRs for Ugandan roads | Delay causes, EOTs, contract forms; often name weather explicitly | To search | Good coverage of large FIDIC MDB contracts. |
| CoST Uganda Infrastructure Transparency Index; OAG project disclosures | Contract dates, TfC, EOTs | To search | Gives award dates and TfC needed for EI linkage. |
| Newspaper corpus (`~/Projects/uganda-urban-headlines`) | "Rains halt works" events with dates and places | To query | Event-level, not claim-level; use as weak labels / validation. |
| ClaimsExpertData `kb.sqlite` | International adverse-weather case law | **Blocked**: reading it needs your permission | For the legal-standard review (WP1 baseline choice, NEC/JCT comparators). |
| Consultant/contractor claim files (partner MoU) | Notices, EOT assessments, days claimed vs granted | Not started | Given the thin public record above, this probably becomes **essential** for RQ2–RQ3 sample size, not optional. |

Other useful context found: KTA Advocates paper on delays in Ugandan road projects and the case for DAABs: https://www.ktaadvocates.com/wp-content/uploads/2023/01/EFFECTS-OF-DELAYS-IN-UGANDAS-ROAD-CONSTRUCTION-PROJECTS-A-CASE-FOR-DISPUTE-ADJUDICATION-ADD-ARBITRATION-BOARDS-DAABS.pdf

Extraction schema: `src/claim_schema.py` → `data/claim_schema.json`.
