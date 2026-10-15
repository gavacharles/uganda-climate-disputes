"""RQ2: how often do defensible data choices flip the FIDIC 8.5(c) verdict? National dispute-risk map.

Claim windows: every meteorological season (DJF, MAM, JJA, SON) from 2001 to 2019 (both products clean),
in every CHIRPS cell in Uganda. Indicator: lost working days (>= 10 mm/day). Test: season value >= the
return level for RP = 5 x TfC = 15 years, using only data before the claim season.
Choices varied (2 x 2 x 2 = 8 verdicts per claim window):
  product   CHIRPS (0.25 deg cell) | ARC2 (nearest 0.1 deg cell)
  baseline  previous 20 years      | full record before the claim
  method    stationary GEV         | non-stationary GEV (location trend, evaluated at the claim year)
A claim window is "contested" when the valid verdicts are not unanimous.
Outputs: results/rq2_dispute_risk_grid.csv, results/rq2_dispute_risk_regions.csv, figures/rq2_dispute_risk_map.png.
"""
import itertools
import warnings
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap
from scipy import stats

import ei
from common import BLUE, RED, load_product, save, write_csv
from regions import cells, region_summary
from rq3_forms import monthly
from wp1_map import draw

RP = 15.0
CLAIMS = ("2000-12-01", "2019-09-01")     # quarter start dates of claim seasons (DJF 2001 .. SON 2019)
PRODUCTS, BASELINES, METHODS = ("CHIRPS", "ARC2"), ("20 yr", "full"), ("stationary", "trend")
COMBOS = list(itertools.product(PRODUCTS, BASELINES, METHODS))


def seasonal(x):
    m = monthly(x).lwd
    q = m.resample("QS-DEC").agg(["sum", "count"])
    return q["sum"][q["count"] == 3]


def threshold(base, years, method, year):
    if method == "stationary":
        return ei.return_level(base, RP) if ei._usable(base) else np.nan
    p = ei.fit_gev_ns(base, years)
    if p is None:
        return np.nan
    loc = p["mu0"] + p["mu1"] * (year - p["t0"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return float(stats.genextreme.isf(1 / RP, p["c"], loc, p["scale"]))


def cell_verdicts(args):
    lat, lon, region, xc, xa = args
    qs = {"CHIRPS": seasonal(xc), "ARC2": seasonal(xa)}
    rows = []
    for t in qs["CHIRPS"].loc[CLAIMS[0]:CLAIMS[1]].index:
        r = {"lat": lat, "lon": lon, "region": region, "season": t}
        for prod, bl, meth in COMBOS:
            q = qs[prod]
            if t not in q.index:
                r[(prod, bl, meth)] = np.nan
                continue
            hist = q[(q.index.month == t.month) & (q.index < t)]
            if bl == "20 yr":
                hist = hist.iloc[-20:]
            thr = threshold(hist.values, hist.index.year.values, meth, t.year)
            r[(prod, bl, meth)] = np.nan if not np.isfinite(thr) else float(q[t] >= thr)
        rows.append(r)
    return rows


def summarise(v):
    """Per-window flags -> shares. v has one column per combo (1/0/NaN)."""
    combo = v[COMBOS]
    anyx = combo.max(axis=1) == 1
    contested = (combo.min(axis=1) == 0) & anyx
    pair = lambda a, b: ((v[a] != v[b]) & v[a].notna() & v[b].notna())  # noqa: E731
    return pd.DataFrame({
        "any_exceptional": anyx, "contested": contested,
        "flip_product": pair(("CHIRPS", "full", "stationary"), ("ARC2", "full", "stationary")),
        "flip_baseline": pair(("CHIRPS", "20 yr", "stationary"), ("CHIRPS", "full", "stationary")),
        "flip_trend": pair(("CHIRPS", "full", "stationary"), ("CHIRPS", "full", "trend")),
    })


if __name__ == "__main__":
    chirps, arc2 = load_product("CHIRPS"), load_product("ARC2")
    jobs = []
    for lat, lon, region in cells(chirps):
        xc = chirps.sel(lat=lat, lon=lon).to_series().astype(float)
        xa = arc2.sel(lat=lat, lon=lon, method="nearest").to_series().astype(float)
        jobs.append((lat, lon, region, xc, xa))
    with Pool(8) as pool:
        rows = [r for cell in pool.imap_unordered(cell_verdicts, jobs, chunksize=4) for r in cell]
    v = pd.DataFrame(rows)
    flags = pd.concat([v[["lat", "lon", "region", "season"]], summarise(v)], axis=1)
    flags.to_csv("../data/processed/rq2_window_flags.csv", index=False)

    g = flags.groupby(["lat", "lon", "region"]).agg(
        windows=("contested", "size"), any_exceptional=("any_exceptional", "mean"),
        contested=("contested", "mean"), flip_product=("flip_product", "mean"),
        flip_baseline=("flip_baseline", "mean"), flip_trend=("flip_trend", "mean")).reset_index()
    arguable = flags[flags.any_exceptional].groupby(["lat", "lon"]).contested.mean().rename("contested_if_arguable")
    g = g.merge(arguable.reset_index(), on=["lat", "lon"], how="left")
    write_csv(g.round(3), "rq2_dispute_risk_grid")
    reg = region_summary(flags.assign(season_name=flags.season.dt.month.map({12: "DJF", 3: "MAM", 6: "JJA", 9: "SON"})),
                         ["any_exceptional", "contested", "flip_product", "flip_baseline", "flip_trend"])
    write_csv(reg.round(3), "rq2_dispute_risk_regions")
    print(reg.round(3).to_string())
    a = flags[flags.any_exceptional]
    print(f"\nNational: {flags.any_exceptional.mean():.3f} of claim windows arguable (>= 1 choice says exceptional); "
          f"{a.contested.mean():.3f} of those contested (choices disagree)")

    bounds = [0, 0.05, 0.1, 0.2, 0.3, 0.4, 1.0001]
    cmap = ListedColormap(["#f0efec", RED[0], RED[1], RED[3], RED[4], RED[6]])
    norm = BoundaryNorm(bounds, cmap.N)
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.9))
    for ax, (col, title) in zip(axes, [("contested", "Any choice flips the verdict"),
                                       ("flip_product", "CHIRPS vs ARC2"),
                                       ("flip_baseline", "20-yr vs full baseline"),
                                       ("flip_trend", "Stationary vs trend-aware")]):
        draw(ax, g, col, cmap, norm, title)
    cb = fig.colorbar(plt.cm.ScalarMappable(norm, cmap), ax=axes, orientation="horizontal", fraction=0.05,
                      pad=0.04, ticks=bounds[:-1] + [1])
    cb.set_label("Share of claim seasons 2001-2019 whose FIDIC Guide verdict depends on the choice "
                 "(3-year contract, RP >= 15 yr)", fontsize=8)
    fig.suptitle("Dispute risk built into the data: where defensible choices give opposite verdicts",
                 x=0.06, y=0.98, ha="left", fontweight="bold", fontsize=10)
    save(fig, "rq2_dispute_risk_map")
