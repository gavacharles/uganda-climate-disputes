"""Translate relief days and lost working days into money for Uganda's national road programme.

For a contract of price P and 3-year TfC, annual works spend is P/3, so a weather effect of D days per contract
is worth D x r x (annual programme spend) per year, where r is a daily rate as a share of contract price:
  delay damages avoided by the Contractor per day of EOT   r_ld = 0.05 % (KCCA addendum; FIDIC Contract Data norm)
  time-related (prolongation) cost per day                 r_tr = 0.02 / 0.03 / 0.05 % (low / central / high)
Annual programme spend: UNRA FY2025/26 framework projection UGX 3.13 trillion (GoU development + external).
FIDIC 8.5(c) gives time only: the Contractor's gain is avoided delay damages; the Employer bears later completion.
NEC4 compensates time and money: the Employer also pays time-related cost on compensated days.
Lost working days not relieved are the Contractor's risk, priced into tenders at time-related cost.
Inputs: results/rq3_forms_regions.csv, results/nex_uganda_summary.csv. Output: results/rq7_money.csv
"""
import pandas as pd

from common import RES, write_csv

SPEND = 3.13e12            # UGX per year
R_LD = 0.0005
R_TR = {"low": 0.0002, "central": 0.0003, "high": 0.0005}


def ugx_bn(days, rate):
    return days * rate * SPEND / 1e9


if __name__ == "__main__":
    forms = pd.read_csv(RES / "rq3_forms_regions.csv", index_col=0).loc["Uganda"]
    nex = pd.read_csv(RES / "nex_uganda_summary.csv", index_col=0, header=[0, 1])
    med = nex.xs("median", axis=1, level=0)["All"]
    rows = []
    for form in ("FIDIC Guide", "NEC4", "Monthly 1-in-10 (JCT practice)"):
        d_now = forms[f"{form} days"]
        rows.append({"item": f"{form}: relief days per contract today", "days": d_now,
                     "UGX bn/yr (delay damages avoided)": ugx_bn(d_now, R_LD),
                     **{f"UGX bn/yr time cost ({k})": ugx_bn(d_now, v) for k, v in R_TR.items()}})
        for scen in ("ssp245", "ssp585"):
            for b in ("stale", "updated"):
                d = med[f"d|{scen}|{b}|{form}|days"]
                rows.append({"item": f"{form}: change in relief days, {scen}, {b} baseline", "days": d,
                             "UGX bn/yr (delay damages avoided)": ugx_bn(d, R_LD),
                             **{f"UGX bn/yr time cost ({k})": ugx_bn(d, v) for k, v in R_TR.items()}})
    for scen in ("ssp245", "ssp585"):
        d = med[f"d|{scen}|lwd"]
        rows.append({"item": f"Extra lost working days per contract (all forms), {scen}", "days": d,
                     "UGX bn/yr (delay damages avoided)": ugx_bn(d, R_LD),
                     **{f"UGX bn/yr time cost ({k})": ugx_bn(d, v) for k, v in R_TR.items()}})
    t = pd.DataFrame(rows).set_index("item")
    write_csv(t.round(2), "rq7_money")
    pd.set_option("display.width", 250)
    print(t.round(1).to_string())
