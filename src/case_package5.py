"""Case study: MoWT Clause 1229 EOT claim on a 3-year UNRA design-and-build road package (Masindi-Biiso and
Kabaale-Kiziranfumbi / Hohwa-Butole lots; commencement 25 Apr 2019, TfC 1,099 days).

Contractor's EOT No. 3 (assessed March 2021): 21 days for Sep 2019 - Nov 2020 under Clause 1229, using UNMA
Masindi station records 2005-2017/18; monthly V values with all non-positive months shown as 0.0. The Engineer
granted 21 days "in line with the Contractor's analysis". Clause 1229 requires the algebraic sum of monthly V
over the whole period for completion, with V >= -Nn.
Here the claim is recomputed with independent gridded data under the choices the clause leaves open.
Outputs: results/case_package5.csv, results/case_package5_monthly.csv
"""
import numpy as np
import pandas as pd

from common import site_series, write_csv

POINTS = {"Masindi (station)": (1.68, 31.72), "Masindi-Biiso road": (1.72, 31.52),  # approximate locations
          "Kabaale-Kiziranfumbi": (1.22, 31.05), "Hohwa-Butole": (1.10, 31.15)}
CLAIMED = {"2019-10": 1.1, "2019-11": 2.6, "2020-01": 2.3, "2020-02": 0.7, "2020-04": 1.1, "2020-05": 9.2,
           "2020-10": 0.8, "2020-11": 2.9}                  # all other months in Sep 2019 - Nov 2020: 0.0
WINDOWS = {"claim window Sep 2019-Nov 2020": ("2019-09-01", "2020-11-30"),
           "whole contract Apr 2019-Apr 2022": ("2019-05-01", "2022-04-30")}
BASELINES = {"2005-2017 (contractor)": (2005, 2017), "1989-2018 (30 yr pre-award)": (1989, 2018)}


def monthly_v(x, baseline, y=10.0, xdiv=20.0):
    m = pd.DataFrame({"R": x.resample("MS").sum(min_count=28),
                      "N": (x >= y).astype(float).where(x.notna()).resample("MS").sum(min_count=28)})
    b = m[(m.index.year >= baseline[0]) & (m.index.year <= baseline[1])]
    nn = b.N.groupby(b.index.month).mean()
    rn = b.R.groupby(b.index.month).mean()
    m["Nn"] = nn.reindex(m.index.month).values
    m["Rn"] = rn.reindex(m.index.month).values
    m["V"] = np.maximum((m.N - m.Nn) + (m.R - m.Rn) / xdiv, -m.Nn)
    return m


if __name__ == "__main__":
    rows, monthly_rows = [], []
    for pname, (lat, lon) in POINTS.items():
        for prod in ("CHIRPS", "CPC", "ARC2"):
            x = site_series(lat, lon, prod)
            for bname, base in BASELINES.items():
                m = monthly_v(x, base)
                for wname, (s, e) in WINDOWS.items():
                    w = m.loc[s:e]
                    complete = w.V.notna().all() and len(w) == len(pd.date_range(s, e, freq="MS"))
                    rows.append({"point": pname, "product": prod, "baseline": bname, "window": wname,
                                 "months": len(w), "complete": complete,
                                 "EOT algebraic (spec)": max(w.V.sum(), 0) if complete else np.nan,
                                 "EOT positive months only": w.V.clip(lower=0).sum() if complete else np.nan,
                                 "months V>0": int((w.V > 0).sum())})
                if pname == "Masindi (station)" and bname.startswith("2005"):
                    w = m.loc["2019-09-01":"2020-11-30", ["N", "Nn", "R", "Rn", "V"]].copy()
                    w["product"] = prod
                    w["claimed V"] = [CLAIMED.get(t.strftime("%Y-%m"), 0.0) for t in w.index]
                    monthly_rows.append(w)
    t = pd.DataFrame(rows)
    write_csv(t.round(1), "case_package5")
    mt = pd.concat(monthly_rows)
    mt.index.name = "month"
    write_csv(mt.round(2), "case_package5_monthly")
    pd.set_option("display.width", 220)
    print(t[t.complete].round(1).to_string(index=False))
    print("\nMasindi, 2005-2017 baseline, monthly V vs claimed:\n",
          mt.reset_index().pivot_table(index="month", columns="product", values="V").round(1)
          .assign(claimed=[CLAIMED.get(pd.Timestamp(i).strftime("%Y-%m"), 0.0) for i in
                           mt.reset_index().pivot_table(index="month", columns="product", values="V").index]).to_string())
