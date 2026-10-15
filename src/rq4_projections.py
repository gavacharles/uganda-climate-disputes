"""RQ4: how does climate change (2041-2070, CMIP6 ensemble median) shift contractual weather relief in Uganda?

Pseudo-future daily rainfall for every CHIRPS cell: the 1991-2020 series scaled by CMIP6 monthly change
factors (cmip6_deltas_obsgrid.nc, 2041-2070 vs 1991-2020, SSP2-4.5 and SSP5-8.5). Two variants:
  uniform  every day x (1 + dP[month])                                   (lower bound for extremes)
  CC       days >= the cell's wet-day 90th percentile get an extra (1 + 0.07 dT) (Clausius-Clapeyron),
           other wet days are scaled down so each month's change still equals dP
For 3-year contracts (start each month, 1991-2018 pseudo-calendar), compare:
  present         1991-2020 weather vs 1991-2020 baseline
  stale baseline  future weather vs the 1991-2020 baseline (contract keeps the old normal)
  updated         future weather vs a future baseline (contract uses an up-to-date normal)
Metrics: P(any relief), relief days per form, and total lost working days per contract (the contractor's
exposure, priced or relieved).
Outputs: results/rq4_projections_grid.csv, results/rq4_projections_regions.csv, figures/rq4_projections_map.png.
"""
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import BoundaryNorm, ListedColormap

from common import BLUE, RAW, RED, load_product, save, write_csv
from regions import cells, region_summary
from rq3_forms import FORMS, contracts, monthly, monthly_flags
from wp1_map import draw

PERIOD = ("1991-01-01", "2020-12-31")
CC = 0.07


def future(x, dP, dT, variant):
    """Scale a daily series by monthly change factors dP (fraction, 12 values) and warming dT (degC)."""
    f = 1 + dP[x.index.month - 1]
    if variant == "uniform":
        return x * f
    wet = x >= 1
    p90 = x[wet].quantile(0.9)
    heavy = x >= p90
    out = x * (1 + CC * dT[x.index.month - 1]) * heavy
    # rescale the remaining wet days so each calendar month's total change equals dP
    month = x.index.to_period("M")
    tot_target = (x * f).groupby(month).transform("sum")
    tot_heavy = out.groupby(month).transform("sum")
    rest = x.where(~heavy, 0.0)
    tot_rest = rest.groupby(month).transform("sum")
    k = ((tot_target - tot_heavy) / tot_rest.replace(0, np.nan)).clip(lower=0).fillna(1.0)
    return out + rest * k


def exposure(x):
    m = monthly(x)
    rows = []
    for c in contracts_index(m):
        rows.append(m.lwd.loc[c: c + pd.DateOffset(months=35)].sum())
    return float(np.mean(rows))


def contracts_index(m):
    return [s for s in pd.date_range(PERIOD[0], "2018-01-01", freq="MS") if s + pd.DateOffset(months=35) <= m.index[-1]]


def summarise(flags, tag):
    c = contracts(flags)
    out = {}
    for f in FORMS:
        out[f"{tag}|{f}|P(any)"] = c[f + "_any"].mean()
        out[f"{tag}|{f}|days"] = c[f + "_days"].mean()
    return out


def cell_run(args):
    lat, lon, region, x, deltas = args
    x = x.loc[PERIOD[0]:PERIOD[1]]
    r = {"lat": lat, "lon": lon, "region": region}
    r.update(summarise(monthly_flags(x), "present"))
    r["present|lwd per contract"] = exposure(x)
    for scen, (dP, dT) in deltas.items():
        for variant in ("uniform", "CC"):
            fx = future(x, dP, dT, variant)
            tag = f"{scen}|{variant}"
            r.update(summarise(monthly_flags(fx, base=x), tag + "|stale"))
            r.update(summarise(monthly_flags(fx), tag + "|updated"))
            r[f"{tag}|lwd per contract"] = exposure(fx)
    return r


if __name__ == "__main__":
    chirps = load_product("CHIRPS")
    d = xr.open_dataset(RAW / "cmip6_deltas_obsgrid.nc")
    jobs = []
    for lat, lon, region in cells(chirps):
        deltas = {s: (d.dP.sel(scenario=s).sel(lat=lat, lon=lon, method="nearest").values,
                      d.dT.sel(scenario=s).sel(lat=lat, lon=lon, method="nearest").values) for s in ("ssp245", "ssp585")}
        jobs.append((lat, lon, region, chirps.sel(lat=lat, lon=lon).to_series().astype(float), deltas))
    with Pool(8) as pool:
        g = pd.DataFrame(pool.map(cell_run, jobs, chunksize=4))
    write_csv(g.round(3), "rq4_projections_grid")

    # long format summary: scenario x variant x baseline x form, national and by region
    long = []
    for col in g.columns[3:]:
        parts = col.split("|")
        long.append(g[["region"]].assign(key=col, value=g[col]))
    L = pd.concat(long)
    reg = L.groupby(["key", "region"]).value.mean().unstack()
    reg["Uganda"] = L.groupby("key").value.mean()
    write_csv(reg.round(3), "rq4_projections_regions")
    print(reg.round(2).to_string())

    # map: change in FIDIC Guide P(any) and lost days per contract, SSP5-8.5 CC, stale baseline
    s = "ssp585|CC"
    g["dP_fidic"] = g[f"{s}|stale|FIDIC Guide|P(any)"] - g["present|FIDIC Guide|P(any)"]
    g["dP_nec_days"] = g[f"{s}|stale|NEC4|days"] - g["present|NEC4|days"]
    g["d_lwd"] = g[f"{s}|lwd per contract"] - g["present|lwd per contract"]
    g["d_lwd_245"] = g["ssp245|CC|lwd per contract"] - g["present|lwd per contract"]
    b = [-0.1, -0.05, 0, 0.05, 0.1, 0.2, 0.3, 1]
    cm = ListedColormap([BLUE[3], BLUE[1], "#f0efec", RED[0], RED[1], RED[3], RED[5]])
    db = [-6, -3, -1, 1, 3, 6, 10, 100]
    fig, ax = plt.subplots(1, 3, figsize=(11, 4))
    draw(ax[0], g, "dP_fidic", cm, BoundaryNorm(b, cm.N), "FIDIC Guide: change in share of\ncontracts with relief (stale baseline)")
    draw(ax[1], g, "d_lwd_245", cm, BoundaryNorm(db, cm.N), "Lost working days per contract:\nchange, SSP2-4.5")
    draw(ax[2], g, "d_lwd", cm, BoundaryNorm(db, cm.N), "Lost working days per contract:\nchange, SSP5-8.5")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(b, cm.N), cm), ax=ax[0], orientation="horizontal", fraction=0.05,
                 pad=0.03, label="Change in probability")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(db, cm.N), cm), ax=ax[1:], orientation="horizontal", fraction=0.05,
                 pad=0.03, label="Change in lost working days per 3-year contract")
    fig.suptitle("2041-2070 vs 1991-2020 (CMIP6 ensemble median, heavy-rain scaling)", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "rq4_projections_map")
