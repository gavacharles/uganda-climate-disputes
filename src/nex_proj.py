"""RQ4 with bias-corrected daily CMIP6 (NEX-GDDP-CMIP6, 10 models, 0.25 deg).

For each model and cell: 3-year contracts starting each month in 1985-2012 (historical run, baseline 1985-2014)
and in 2041-2068 (SSP2-4.5 / SSP5-8.5, 2041-2070), evaluated
  hist     historical weather vs historical baseline
  stale    future weather vs the historical baseline (contract keeps the old normal)
  updated  future weather vs the future baseline
Metrics per form: P(any relief), relief days per contract; plus lost working days (>= 10 mm) per contract.
Changes are computed within each model (future minus its own historical) and summarised across models.
Usage: python nex_proj.py uganda|ea
Outputs: results/nex_<domain>_cells.csv (per model), nex_<domain>_summary.csv, figures/nex_<domain>_map.png
"""
import sys
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import BoundaryNorm, ListedColormap

from common import BLUE, PROC, RED, load_product, save, write_csv
from fetch_ea import MODELS
from regions import cells, ea_cells
from rq3_forms import FORMS, contracts, monthly, monthly_flags
from wp1_map import draw

HIST, FUT = (1985, 2014), (2041, 2070)
STARTS = {"hist": pd.date_range("1985-01-01", "2012-01-01", freq="MS"),
          "fut": pd.date_range("2041-01-01", "2068-01-01", freq="MS")}
SCENS = ("ssp245", "ssp585")


def to_series(da, lat, lon):
    s = da.sel(lat=lat, lon=lon).to_series().astype(float)
    return s[~s.index.duplicated()]


def lwd_per_contract(x, starts):
    m = monthly(x).lwd
    v = [m.loc[s: s + pd.DateOffset(months=35)].sum() for s in starts if s + pd.DateOffset(months=35) <= m.index[-1]]
    return float(np.mean(v))


def metrics(flags, starts, tag):
    c = contracts(flags, starts)
    out = {}
    for f in FORMS:
        out[f"{tag}|{f}|P(any)"] = c[f + "_any"].mean()
        out[f"{tag}|{f}|days"] = c[f + "_days"].mean()
    return out


def cell_run(args):
    lat, lon, region, model, h, futs = args
    r = {"lat": lat, "lon": lon, "region": region, "model": model}
    r.update(metrics(monthly_flags(h, baseline=HIST), STARTS["hist"], "hist"))
    r["hist|lwd"] = lwd_per_contract(h, STARTS["hist"])
    for scen, f in futs.items():
        r.update(metrics(monthly_flags(f, base=h, baseline=HIST), STARTS["fut"], f"{scen}|stale"))
        r.update(metrics(monthly_flags(f, baseline=FUT), STARTS["fut"], f"{scen}|updated"))
        r[f"{scen}|lwd"] = lwd_per_contract(f, STARTS["fut"])
    return r


def run(domain):
    ref = load_product("CHIRPS") if domain == "uganda" else load_product("CHIRPS_EA")
    cl = cells(ref) if domain == "uganda" else ea_cells(ref, stride=2)
    lats = sorted({c[0] for c in cl})
    lons = sorted({c[1] for c in cl})
    box = dict(lat=slice(min(lats) - 0.01, max(lats) + 0.01), lon=slice(min(lons) - 0.01, max(lons) + 0.01))
    rows = []
    for model in MODELS:
        files = {s: PROC / "nex" / f"{model}_{s}.nc" for s in ("historical",) + SCENS}
        if not all(f.exists() for f in files.values()):
            print("skip (not downloaded)", model, flush=True)
            continue
        da = {s: xr.open_dataset(f).precip.sel(**box).load() for s, f in files.items()}
        jobs = [(lat, lon, reg, model, to_series(da["historical"], lat, lon),
                 {s: to_series(da[s], lat, lon) for s in SCENS}) for lat, lon, reg in cl]
        with Pool(8) as pool:
            rows += pool.map(cell_run, jobs, chunksize=8)
        print("done", model, len(jobs), flush=True)
    return pd.DataFrame(rows)


def summarise(df):
    """Ensemble statistics of regional means of each metric (and of future-minus-historical changes)."""
    metric_cols = [c for c in df.columns if "|" in c]
    reg = df.groupby(["model", "region"])[metric_cols].mean()
    nat = df.groupby("model")[metric_cols].mean().assign(region="All").set_index("region", append=True)
    reg = pd.concat([reg, nat])
    for scen in SCENS:                       # changes vs each model's own historical
        for f in FORMS:
            for stat in ("P(any)", "days"):
                for b in ("stale", "updated"):
                    reg[f"d|{scen}|{b}|{f}|{stat}"] = reg[f"{scen}|{b}|{f}|{stat}"] - reg[f"hist|{f}|{stat}"]
        reg[f"d|{scen}|lwd"] = reg[f"{scen}|lwd"] - reg["hist|lwd"]
    g = reg.groupby(level="region")
    out = pd.concat({"median": g.median(), "p10": g.quantile(0.1), "p90": g.quantile(0.9),
                     "n_models": g.size().to_frame("n").reindex(columns=reg.columns, fill_value=np.nan)
                     .fillna(g.size().iloc[0])}, axis=0)
    return out.T


def fig(df, domain):
    med = df.groupby(["lat", "lon"]).median(numeric_only=True).reset_index()
    for scen in SCENS:
        med[f"dP_{scen}"] = med[f"{scen}|stale|FIDIC Guide|P(any)"] - med["hist|FIDIC Guide|P(any)"]
        med[f"dL_{scen}"] = med[f"{scen}|lwd"] - med["hist|lwd"]
    b = [-0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3, 1]
    cm = ListedColormap([BLUE[4], BLUE[2], "#f0efec", RED[0], RED[1], RED[3], RED[5]])
    db = [-15, -6, -2, 2, 6, 10, 20, 100]
    step = 0.25 if domain == "uganda" else 0.5
    fig, ax = plt.subplots(1, 4, figsize=(13, 4))
    for i, scen in enumerate(SCENS):
        _draw(ax[i], med, f"dP_{scen}", cm, BoundaryNorm(b, cm.N), f"FIDIC relief probability\n{scen.upper()}, stale baseline", domain, step)
        _draw(ax[2 + i], med, f"dL_{scen}", cm, BoundaryNorm(db, cm.N), f"Lost working days per contract\n{scen.upper()}", domain, step)
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(b, cm.N), cm), ax=ax[:2], orientation="horizontal", fraction=0.05,
                 pad=0.03, label="Change in share of 3-year contracts with FIDIC relief")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(db, cm.N), cm), ax=ax[2:], orientation="horizontal", fraction=0.05,
                 pad=0.03, label="Change in lost working days per 3-year contract")
    fig.suptitle("2041-2070 vs 1985-2014, NEX-GDDP-CMIP6 ensemble median (10 models)", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, f"nex_{domain}_map")


def _draw(ax, df, col, cmap, norm, title, domain, step):
    if domain == "uganda":
        draw(ax, df, col, cmap, norm, title)
        return
    from regions import countries
    for _, r in df.iterrows():
        if np.isfinite(r[col]):
            ax.add_patch(plt.Rectangle((r.lon - step / 2, r.lat - step / 2), step, step, color=cmap(norm(r[col])), lw=0))
    for _, g in countries():
        for poly in getattr(g, "geoms", [g]):
            ax.plot(*poly.exterior.xy, color="#52514e", lw=0.5)
    ax.set_xlim(28.5, 42)
    ax.set_ylim(-12, 5.5)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "uganda"
    df = run(domain)
    df.round(3).to_csv(PROC / f"nex_{domain}_cells.csv", index=False)
    s = summarise(df)
    s.index.name = "metric"
    write_csv(s.round(3), f"nex_{domain}_summary")
    keys = [k for k in s.index if k.startswith("d|") and ("FIDIC" in k or "lwd" in k or "NEC4|days" in k)]
    pd.set_option("display.width", 250)
    print(s.loc[keys].xs("median", axis=1, level=0).round(2).to_string())
    fig(df, domain)
