# Climate data, contract forms and "exceptionally adverse climatic conditions" in Uganda

**Author:** Gavamukulya (Gava) Charles · started 14 October 2026 · **private repository**

How far do the choices a construction contract leaves open, rather than the weather, decide entitlement to extension of time for "exceptionally adverse climatic conditions"? Those choices are the climatic variable, dataset, baseline, assessment window and summation rule. The study applies the FIDIC Contracts Guide rule, NEC4, JCT-style practice and Uganda's MoWT Clause 1229 to 45 years of daily rainfall (CHIRPS, ARC2, CPC) and heat stress (NASA POWER) for every cell in Uganda, with NEX-GDDP-CMIP6 projections to 2041–2070. It proposes the **Shared Weather Allowance**.

| Item | Where |
|---|---|
| Manuscript (Markdown / Word) | [`paper/manuscript.md`](paper/manuscript.md), `paper/manuscript.docx` (build: `python src/build_docx.py`) |
| Concept note, WP notes, source register | [`docs/`](docs/) |
| Outreach (Substack, LinkedIn) | [`outreach/`](outreach/) |
| Figures | [`figures/`](figures/) (Fig. 1–17, S1–S2, `substack_*`) |
| Result tables | [`results/`](results/), including the national SWA tables `swa_tables_uganda.csv` |
| Code | [`src/`](src/) |

## Code map

| Script | Purpose |
|---|---|
| `ei.py` | Exceptionality Index library: indicators, return periods (empirical, GEV, non-stationary GEV), NEC test |
| `wp1_map.py` | National EI maps (OND 2019, MAM 2020), CHIRPS vs ARC2 |
| `rq2_dispute_risk.py`, `rq2b_window.py` | Verdict sensitivity (product, baseline, trend) and claim-window selection |
| `rq3_forms.py` | FIDIC Guide, NEC4 and JCT-style relief on 3-year contracts |
| `rq5_clauses.py` | Candidate clauses incl. Clause 1229 and the Shared Weather Allowance; present and NEX future |
| `nex_proj.py`, `fetch_ea.py` | NEX-GDDP-CMIP6 download and projections; East Africa CHIRPS/CPC download |
| `rq6_heat.py` | Heat stress (sWBGT) as a climatic condition |
| `rq7_money.py` | Cost translation (UGX) |
| `ea_analysis.py` | East Africa regional outlook |
| `case_*.py` | Project case studies (contract documents are confidential and not in this repository) |
| `swa_outputs.py`, `figs_extra.py`, `fig1_framework.py` | SWA tables, worked example and figures |

## Run

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
cd src && ../.venv/bin/python rq3_forms.py   # etc.
```

`data/raw/` holds symlinks to `~/uganda-rainfall-climate/data/processed`. East Africa and NEX data are fetched by `src/fetch_ea.py` into `data/` (about 8 GB, not committed).

## Confidentiality

Project contract and claim documents were reviewed locally and are reported only in anonymised form (Projects A–D). The detailed review (`docs/contract_review.md`) is excluded from version control. The `case_*` scripts and results carry project names; anonymise them before making this repository public.
