"""Shared Weather Allowance deliverables:
  1. National SWA tables: monthly mean and 1-in-10-year lost working days (>= 10 mm) for every Uganda CHIRPS
     cell, 1991-2020 (results/swa_tables_uganda.csv) - the values that would go into the Contract Data.
  2. Worked example: Project A claim period (Sep 2019 - Nov 2020) and whole contract, SWA vs Clause 1229
     (results/swa_worked_example.csv).
  3. Fig. 6: clause comparison (figures/fig6_clauses.png).
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from case_package5 import POINTS, WINDOWS, monthly_v
from common import CAT, GRID, INK2, RES, load_product, save, site_series, write_csv
from regions import cells

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def lwd_monthly(x):
    return (x >= 10).astype(float).where(x.notna()).resample("MS").sum(min_count=28).dropna()


def swa_table(x, base=(1991, 2020)):
    m = lwd_monthly(x)
    b = m[(m.index.year >= base[0]) & (m.index.year <= base[1])]
    g = b.groupby(b.index.month)
    return g.mean(), g.quantile(0.9)


def swa_eot(x, s, e, base):
    m = lwd_monthly(x).loc[s:e]
    mean, q90 = swa_table(x, base)
    mu, q = mean.reindex(m.index.month).values, q90.reindex(m.index.month).values
    return float((0.5 * np.clip(m.values - mu, 0, np.maximum(q - mu, 0)) + np.maximum(m.values - q, 0)).sum())


if __name__ == "__main__":
    # 1. national tables
    da = load_product("CHIRPS")
    rows = []
    for lat, lon, reg in cells(da):
        mean, q90 = swa_table(da.sel(lat=lat, lon=lon).to_series().astype(float))
        rows.append({"lat": lat, "lon": lon, "region": reg,
                     **{f"normal_{MONTHS[i - 1]}": round(mean[i], 1) for i in range(1, 13)},
                     **{f"1in10_{MONTHS[i - 1]}": round(q90[i], 1) for i in range(1, 13)}})
    write_csv(pd.DataFrame(rows), "swa_tables_uganda")

    # 2. worked example, Project A (Masindi cell)
    lat, lon = POINTS["Masindi (station)"]
    ex = []
    for prod in ("CHIRPS", "CPC"):
        x = site_series(lat, lon, prod)
        for wname, (s, e) in WINDOWS.items():
            mv = monthly_v(x, (1989, 2018)).loc[s:e]
            ex.append({"product": prod, "window": wname, "baseline": "1989-2018 (30 yr pre-award)",
                       "SWA EOT (days)": round(swa_eot(x, s, e, (1989, 2018)), 1),
                       "Clause 1229 algebraic (days)": round(max(mv.V.sum(), 0), 1),
                       "Clause 1229 positive months (days)": round(mv.V.clip(lower=0).sum(), 1)})
    exd = pd.DataFrame(ex)
    write_csv(exd, "swa_worked_example")
    print(exd.to_string(index=False))

    # 3. Fig. 6
    t = pd.read_csv(RES / "rq5_clauses_present.csv", index_col=0)
    order = ["FIDIC Guide (status quo)", "NEC4", "MoWT 1229 (algebraic sum)", "MoWT 1229 (positive months only)",
             "Shared band"]
    labels = ["FIDIC Guide", "NEC4", "Clause 1229\n(as written)", "Clause 1229\n(positive months)",
              "Shared Weather\nAllowance"]
    t = t.loc[order]
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    cols = [CAT[0], CAT[1], CAT[3], CAT[7], CAT[2]]
    y = np.arange(len(order))
    for a, (col, title, fmt) in zip(ax, [("relief_days", "Mean EOT per 3-year contract (days)", "{:.1f}"),
                                         ("product_verdict_flip", "Verdict differs CHIRPS vs CPC\n(share of contracts)", "{:.0%}"),
                                         ("cv", "Unpredictability\n(CV of EOT across contracts)", "{:.2f}")]):
        a.barh(y, t[col].values, color=cols, height=0.62)
        for yi, v in zip(y, t[col].values):
            a.text(v, yi, " " + fmt.format(v), va="center", fontsize=8, color=INK2)
        a.set_title(title, fontsize=9)
        a.grid(axis="y", visible=False)
        a.set_xlim(0, t[col].max() * 1.3)
    ax[0].set_yticks(y, labels)
    ax[0].invert_yaxis()
    fig.suptitle("Candidate weather rules on the same 45-year record (all Uganda, 3-year contracts, 1991-2020 normal)",
                 x=0.06, y=1.06, ha="left", fontweight="bold", fontsize=10)
    fig.subplots_adjust(wspace=0.35)
    save(fig, "fig6_clauses")
