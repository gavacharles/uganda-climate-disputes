# uganda-climate-disputes

Python code, results, figures and manuscript on how climate datasets and contract terms decide extension-of-time entitlement for "exceptionally adverse climatic conditions" in Ugandan road contracts (FIDIC, NEC4 and MoWT Clause 1229, plus a proposed Shared Weather Allowance).

Author: Gavamukulya (Gava) Charles.

## Contents

| Item | Where |
|---|---|
| Manuscript (Markdown and Word) | `paper/manuscript.md`, `paper/manuscript.docx` (build with `python src/build_docx.py`) |
| Concept note, work-package notes, source register | `docs/` |
| Figures | `figures/` |
| Result tables | `results/` |
| Claim schema | `data/claim_schema.json` |
| Code | `src/` |
| Tests | `tests/test_ei.py` |
| Post drafts | `outreach/` |

## Code map

| Script | Purpose |
|---|---|
| `ei.py` | Exceptionality Index library: indicators, return periods (empirical, GEV, non-stationary GEV), NEC test |
| `wp1_map.py` | National EI maps, CHIRPS vs ARC2 |
| `rq2_dispute_risk.py`, `rq2b_window.py` | Verdict sensitivity (product, baseline, trend) and claim-window selection |
| `rq3_forms.py` | FIDIC, NEC4 and JCT-style relief on 3-year contracts |
| `rq5_clauses.py` | Candidate clauses including Clause 1229 and the Shared Weather Allowance |
| `nex_proj.py`, `fetch_ea.py` | NEX-GDDP-CMIP6 download and projections; East Africa CHIRPS/CPC download |
| `rq6_heat.py` | Heat stress (sWBGT) |
| `rq7_money.py` | Cost translation |
| `ea_analysis.py` | East Africa regional outlook |
| `case_*.py` | Project case studies |
| `swa_outputs.py`, `figs_extra.py`, `fig1_framework.py`, `covers.py` | Tables and figures |

## Running

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
cd src && ../.venv/bin/python rq3_forms.py   # and so on for each script
```

`data/raw/` holds symlinks to the processed data of the `uganda-rainfall-climate` project. East Africa and NEX data are fetched by `src/fetch_ea.py` into `data/` (about 8 GB, not committed).

## Confidentiality

Contract and claim documents are not in this repository; the detailed contract review (`docs/contract_review.md`) is excluded from version control. The `case_*` scripts and their results refer to projects by name.
