"""Build paper/manuscript.docx from paper/manuscript.md with pandoc.

The working "Figures and tables (current files)" section is replaced by embedded figures with captions,
placed after the references (journal convention). Run from the project root or src/.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANDOC = Path.home() / "uganda-rainfall-climate/.venv/lib/python3.9/site-packages/pypandoc/files/pandoc"

FIGURES = [
    ("fig1_framework.png", "Conceptual framework: the climate record is held fixed and the contractual test is varied."),
    ("wp1_map_ei.png", "Exceptionality Index for OND 2019 and MAM 2020 on CHIRPS (3-year contract awarded 2018), and verdict agreement between CHIRPS and ARC2 (ARC2 masked for 2020-2023)."),
    ("rq2_dispute_risk_map.png", "Share of claim seasons (2001-2019) whose FIDIC Guide verdict depends on the choice of rainfall product, baseline length or trend treatment."),
    ("rq2b_window_map.png", "Share of 3-year contracts with an 'exceptional' window when assessed on fixed calendar seasons versus any 90-day window chosen by the claimant."),
    ("rq3_forms_map.png", "Weather relief on 3-year contracts under the FIDIC Guide rule, NEC4 and JCT-style practice: share of contracts with any relief (top) and mean relief days (bottom), 1991-2025."),
    ("fig6_clauses.png", "Candidate weather rules compared on the same record: mean EOT, CHIRPS-CPC verdict disagreement and unpredictability (coefficient of variation)."),
    ("nex_uganda_map.png", "Projected change (2041-2070 vs 1985-2014, NEX-GDDP-CMIP6 ensemble median) in the share of contracts with FIDIC relief under a stale baseline, and in lost working days per contract."),
    ("ea_forms_map.png", "East Africa: FIDIC Guide and NEC4 relief, FIDIC relief days, and FIDIC verdict disagreement between CHIRPS and CPC, 1991-2020."),
    ("rq6_heat_map.png", "Heat as a contractual climatic condition: heat-lost days per year (sWBGT >= 30 C), observed trend, projected change under SSP5-8.5, and change in the share of contracts with 'exceptional' heat under a stale baseline."),
    ("fig10_contract_tables.png", "Clause 1229 average tables (N_n, R_n) printed in two signed contracts compared with 1991-2020 site normals from CHIRPS and CPC, and the resulting EOT per 3-year contract."),
    ("fig11_projectA.png", "Project A: monthly Clause 1229 values claimed versus recomputed with CHIRPS and CPC (a), and total EOT under each combination of dataset, baseline, period and summation (b)."),
    ("fig12_swa_schematic.png", "How the Shared Weather Allowance converts a month's lost working days into extension of time, compared with NEC4 and Clause 1229 (illustrative)."),
    ("fig13_risk_split.png", "Who carries above-normal rain lost days under each rule today (a) and the extra lost days projected for 2041-2070 under stale and updated baselines (b)."),
    ("fig14_rain_heat_calendar.png", "Mean monthly rain lost days and heat-lost days by region, 1991-2020. A day may count in both categories; such overlap is rare."),
    ("fig15_eot_distribution.png", "Distribution of EOT per 3-year contract across all contracts and cells, by rule."),
    ("fig16_climate_stability.png", "Relief per contract in 1985-2014 and in 2041-2070 under stale and updated baselines, by rule (10-model ensemble; bars show the 10-90% model range for the stale case)."),
    ("fig17_contested_sources.png", "Sources of disagreement among arguable claim seasons (FIDIC Guide, 3-year contracts, Uganda 2001-2019)."),
]
SUPPLEMENT = [
    ("figS1_arc2_break.png", "Homogeneity screen: ratio of ARC2 to CHIRPS national monthly rainfall, 1983-2025, with the masked period shaded."),
    ("figS2_gauge_vs_grid.png", "Project A: site-gauge versus gridded days >= 10 mm and monthly rainfall for the six claimed months (2022-2023)."),
]


def main():
    md = (ROOT / "paper" / "manuscript.md").read_text()
    md = re.sub(r"## Figures and tables \(current files\).*?(?=## References)", "", md, flags=re.S)
    md = md.replace("\n*Draft", "\n\n*Draft", 1)
    parts = ["\n\n## Figures\n"]
    for i, (f, cap) in enumerate(FIGURES, 1):
        parts.append(f"\n![**Fig. {i}.** {cap}](figures/{f}){{width=6.5in}}\n")
    parts.append("\n## Supplementary figures\n")
    for i, (f, cap) in enumerate(SUPPLEMENT, 1):
        parts.append(f"\n![**Fig. S{i}.** {cap}](figures/{f}){{width=6.5in}}\n")
    tmp = ROOT / "paper" / "_manuscript_build.md"
    tmp.write_text(md + "".join(parts))
    out = ROOT / "paper" / "manuscript.docx"
    subprocess.run([str(PANDOC), str(tmp), "-f", "markdown+pipe_tables+implicit_figures", "-t", "docx",
                    "-o", str(out), "--resource-path", str(ROOT)], check=True)
    tmp.unlink()
    print("wrote", out)


if __name__ == "__main__":
    main()
