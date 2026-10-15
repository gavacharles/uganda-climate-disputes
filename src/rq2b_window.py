"""RQ2b: how much does letting the claimant choose the window inflate the FIDIC Guide test?

For every Uganda CHIRPS cell: lost working days (>= 10 mm) in 90-day windows starting on 77 calendar days
(every 5th day of the year plus 1 Mar, 1 Jun, 1 Sep, 1 Dec). For each start day, the 15-year return level is
fitted (GEV) to the 1991-2020 values of the same calendar window. For 3-year contracts starting each month
1991-2023, compare
  fixed   any of the meteorological seasons (90-day windows from 1 Dec, 1 Mar, 1 Jun, 1 Sep) is exceptional
  chosen  any 90-day window inside the contract, at any of the 77 start days, is exceptional
Outputs: results/rq2b_window_grid.csv, results/rq2b_window_regions.csv, figures/rq2b_window_map.png
"""
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap

import ei
from common import BLUE, RED, load_product, save, write_csv
from regions import cells, region_summary
from wp1_map import draw

WIN, RP, BASELINE = 90, 15.0, (1991, 2020)
STARTS = pd.date_range("1991-01-01", "2023-01-01", freq="MS")
FIXED = {(12, 1), (3, 1), (6, 1), (9, 1)}
KEYS = sorted({(d.month, d.day) for d in pd.date_range("2001-01-01", "2001-12-31", freq="5D")} | FIXED)


def cell_run(args):
    lat, lon, region, x = args
    x = x.loc[:"2025-12-31"]
    lwd = (x >= 10).astype(float).where(x.notna())
    s = lwd.rolling(WIN, min_periods=int(WIN * 0.95)).sum().shift(-(WIN - 1))   # window starting on each day
    s = s.dropna()
    key = list(zip(s.index.month, s.index.day))
    df = pd.DataFrame({"v": s.values, "key": key}, index=s.index)
    df = df[df.key.isin(KEYS)]
    thr = {}
    for k, g in df[(df.index.year >= BASELINE[0]) & (df.index.year <= BASELINE[1])].groupby("key"):
        thr[k] = ei.return_level(g.v.values, RP)
    df["exc"] = df.v >= df.key.map(thr)
    df["fixed"] = df.key.isin(FIXED)
    fixed_any, chosen_any, n_fixed, n_chosen = [], [], [], []
    for st in STARTS:
        end = st + pd.DateOffset(months=36) - pd.Timedelta(days=WIN)      # window must end inside the contract
        w = df.loc[st:end]
        if w.empty or end > df.index[-1]:
            continue
        fixed_any.append(w.exc[w.fixed].any())
        chosen_any.append(w.exc.any())
        n_fixed.append(w.exc[w.fixed].sum())
        n_chosen.append(w.exc.sum())
    base = df[(df.index.year >= BASELINE[0]) & (df.index.year <= BASELINE[1])]
    return {"lat": lat, "lon": lon, "region": region,
            "P_fixed": np.mean(fixed_any), "P_chosen": np.mean(chosen_any),
            "windows_per_year_exc_rate": base.exc.mean(),
            "years_with_any_exc_window": base.groupby(base.index.year).exc.any().mean(),
            "years_with_fixed_exc": base[base.fixed].groupby(base[base.fixed].index.year).exc.any().mean()}


if __name__ == "__main__":
    da = load_product("CHIRPS")
    jobs = [(lat, lon, reg, da.sel(lat=lat, lon=lon).to_series().astype(float)) for lat, lon, reg in cells(da)]
    with Pool(8) as pool:
        g = pd.DataFrame(pool.map(cell_run, jobs, chunksize=4))
    g["inflation"] = g.P_chosen / g.P_fixed
    write_csv(g.round(3), "rq2b_window_grid")
    cols = ["P_fixed", "P_chosen", "inflation", "years_with_fixed_exc", "years_with_any_exc_window"]
    reg = region_summary(g, cols)
    write_csv(reg.round(3), "rq2b_window_regions")
    print(reg.round(3).to_string())

    b = [0, 0.25, 0.5, 0.75, 0.9, 0.97, 1.0001]
    cm = ListedColormap(["#f0efec", BLUE[0], BLUE[2], BLUE[4], BLUE[5], BLUE[6]])
    fig, ax = plt.subplots(1, 2, figsize=(7.5, 4))
    draw(ax[0], g, "P_fixed", cm, BoundaryNorm(b, cm.N), "Fixed calendar seasons")
    draw(ax[1], g, "P_chosen", cm, BoundaryNorm(b, cm.N), "Claimant picks any 90-day window")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(b, cm.N), cm), ax=ax, orientation="horizontal", fraction=0.05,
                 pad=0.04, label="Share of 3-year contracts with an 'exceptional' window (FIDIC Guide, RP >= 15 yr)")
    fig.suptitle("Choosing the window: the same rain, a stronger claim", x=0.06, ha="left", fontweight="bold",
                 fontsize=10)
    save(fig, "rq2b_window_map")
