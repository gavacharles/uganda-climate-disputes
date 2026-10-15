"""RQ5: calibrate candidate weather clauses on the national record and under climate change.

Rules (all assume a named dataset and grid cell; LWD = days >= 10 mm; L = month's LWD; mean, q90 = that calendar
month's baseline mean and 1-in-10-year LWD):
  FIDIC Guide (status quo)   season LWD with RP >= 15 yr -> relief = season LWD - mean      (binary trigger)
  NEC4                       month rain or days>=5mm > 1-in-10 -> relief = (L - q90)+       (binary trigger)
  LWD table 1-in-10          Contract Data table of monthly 1-in-10 LWD -> relief = (L - q90)+ every month
  LWD table mean             relief = (L - mean)+ every month (Employer carries all above-normal lost days)
  Shared band                relief = 0.5 x (L - mean)+ capped at (q90 - mean), plus (L - q90)+
  MoWT 1229                  Uganda MoWT General Specifications for Road and Bridge Works, Clause 1229:
                             V = (Nw - Nn) + (Rw - Rn)/20 per month (Nw, Nn = days >= 10 mm; Rw, Rn = rainfall),
                             V >= -Nn; the specification sums V algebraically over the contract period
                             ("algebraic sum"); practice seen in claims adds only positive months
Present (CHIRPS, 1991-2020 normal, contracts starting 1991-2018) per Uganda cell:
  P(any relief), mean relief days, CV of relief across contracts (predictability),
  share of above-normal lost days relieved (risk sharing), and product sensitivity: mean |relief(CHIRPS) -
  relief(CPC)| / mean relief, and the share of contracts whose any-relief verdict differs between products.
Future (NEX-GDDP-CMIP6, within-model change 2041-2070 vs 1985-2014, stale and updated baselines).
Outputs: results/rq5_clauses_present.csv, results/rq5_clauses_future.csv, figures/rq5_clauses.png
"""
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from common import CAT, PROC, load_product, save, write_csv
from fetch_ea import MODELS
from regions import cells
from rq3_forms import monthly, monthly_flags

RULES = ["FIDIC Guide (status quo)", "NEC4", "MoWT 1229 (algebraic sum)", "MoWT 1229 (positive months only)",
         "LWD table 1-in-10", "LWD table mean", "Shared band", "Shared band (netted)"]
CONTRACT_LEVEL = {"MoWT 1229 (algebraic sum)", "Shared band (netted)"}     # relief = max(sum of monthly V over the contract, 0)
BASELINE = (1991, 2020)
STARTS = pd.date_range("1991-01-01", "2018-01-01", freq="MS")
HIST, FUT = (1985, 2014), (2041, 2070)
STARTS_H = pd.date_range("1985-01-01", "2012-01-01", freq="MS")
STARTS_F = pd.date_range("2041-01-01", "2068-01-01", freq="MS")


def rule_months(x, base=None, baseline=BASELINE):
    """Monthly relief under each rule, plus the month's above-normal lost days."""
    fl = monthly_flags(x, base=base, baseline=baseline)
    m = monthly(x).reindex(fl.index)
    mb = monthly(x if base is None else base)
    b = mb[(mb.index.year >= baseline[0]) & (mb.index.year <= baseline[1])]
    mon = m.index.month
    mean = b.lwd.groupby(b.index.month).mean().reindex(mon).values
    q90 = b.lwd.groupby(b.index.month).quantile(0.9).reindex(mon).values
    L = m.lwd.values
    out = pd.DataFrame(index=fl.index)
    out["FIDIC Guide (status quo)"] = fl["FIDIC Guide"]
    out["NEC4"] = fl["NEC4"]
    out["LWD table 1-in-10"] = np.maximum(L - q90, 0)
    out["LWD table mean"] = np.maximum(L - mean, 0)
    out["Shared band"] = 0.5 * np.clip(L - mean, 0, np.maximum(q90 - mean, 0)) + np.maximum(L - q90, 0)
    # netted variant: half of any below-normal deficit offsets relief elsewhere in the contract (total floored at 0)
    out["Shared band (netted)"] = 0.5 * np.minimum(L - mean, np.maximum(q90 - mean, 0)) + np.maximum(L - q90, 0)
    # MoWT General Specifications for Road and Bridge Works, Clause 1229 (Y = 10 mm, x = 20)
    rn = b.rain.groupby(b.index.month).mean().reindex(mon).values
    v = np.maximum((L - mean) + (m.rain.values - rn) / 20.0, -mean)
    out["MoWT 1229 (algebraic sum)"] = v
    out["MoWT 1229 (positive months only)"] = np.maximum(v, 0)
    out["_trig_FIDIC Guide (status quo)"] = fl["FIDIC Guide_trig"]
    out["_trig_NEC4"] = fl["NEC4_trig"]
    for r in RULES[2:]:
        out["_trig_" + r] = out[r] > 0          # (contract-level rules recompute the trigger from the total)
    out["_abnormal"] = np.maximum(L - mean, 0)
    return out


def per_contract(rm, starts):
    rows = []
    for s in starts:
        w = rm.loc[s: s + pd.DateOffset(months=35)]
        if len(w) < 36:
            continue
        r = {"start": s, "_abnormal": w["_abnormal"].sum()}
        for k in RULES:
            r[k] = max(w[k].sum(), 0.0) if k in CONTRACT_LEVEL else w[k].sum()
            r["any_" + k] = r[k] > 0 if k in CONTRACT_LEVEL else bool(w["_trig_" + k].any())
        rows.append(r)
    return pd.DataFrame(rows).set_index("start")


def present_cell(args):
    lat, lon, region, xc, xp = args
    c = per_contract(rule_months(xc), STARTS)
    p = per_contract(rule_months(xp), STARTS)
    common = c.index.intersection(p.index)       # CPC drops months with missing days
    c, p = c.loc[common], p.loc[common]
    rows = []
    for k in RULES:
        mu = c[k].mean()
        rows.append({"lat": lat, "lon": lon, "region": region, "rule": k, "P(any)": c["any_" + k].mean(),
                     "relief_days": mu, "cv": c[k].std() / mu if mu > 0 else np.nan,
                     "share_abnormal_relieved": c[k].sum() / c["_abnormal"].sum(),
                     "product_gap": (c[k] - p[k]).abs().mean() / mu if mu > 0 else np.nan,
                     "product_verdict_flip": (c["any_" + k] != p["any_" + k]).mean()})
    return rows


def future_cell(args):
    lat, lon, region, model, h, futs = args
    hist = per_contract(rule_months(h, baseline=HIST), STARTS_H)
    rows = []
    for scen, f in futs.items():
        stale = per_contract(rule_months(f, base=h, baseline=HIST), STARTS_F)
        upd = per_contract(rule_months(f, baseline=FUT), STARTS_F)
        for k in RULES:
            rows.append({"lat": lat, "lon": lon, "region": region, "model": model, "scenario": scen, "rule": k,
                         "hist_days": hist[k].mean(), "stale_days": stale[k].mean(), "updated_days": upd[k].mean(),
                         "hist_P": hist["any_" + k].mean(), "stale_P": stale["any_" + k].mean(),
                         "updated_P": upd["any_" + k].mean()})
    return rows


def present():
    chirps, cpc = load_product("CHIRPS"), load_product("CPC")
    jobs = [(lat, lon, reg, chirps.sel(lat=lat, lon=lon).to_series().astype(float).loc[:"2020-12-31"],
             cpc.sel(lat=lat, lon=lon, method="nearest").to_series().astype(float).loc[:"2020-12-31"])
            for lat, lon, reg in cells(chirps)]
    with Pool(8) as pool:
        rows = [r for cell in pool.map(present_cell, jobs, chunksize=4) for r in cell]
    return pd.DataFrame(rows)


def future():
    ref = load_product("CHIRPS")
    cl = cells(ref)
    box = dict(lat=slice(-1.6, 4.5), lon=slice(29.4, 35.2))
    rows = []
    for model in MODELS:
        files = {s: PROC / "nex" / f"{model}_{s}.nc" for s in ("historical", "ssp245", "ssp585")}
        if not all(f.exists() for f in files.values()):
            continue
        da = {s: xr.open_dataset(f).precip.sel(**box).load() for s, f in files.items()}
        ser = lambda s, lat, lon: da[s].sel(lat=lat, lon=lon).to_series().astype(float)  # noqa: E731
        jobs = [(lat, lon, reg, model, ser("historical", lat, lon),
                 {s: ser(s, lat, lon) for s in ("ssp245", "ssp585")}) for lat, lon, reg in cl]
        with Pool(8) as pool:
            rows += [r for cell in pool.map(future_cell, jobs, chunksize=8) for r in cell]
        print("future done", model, flush=True)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import sys
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    if part in ("present", "all"):
        p = present()
        p.round(4).to_csv(PROC / "rq5_present_cells.csv", index=False)
        tab = p.groupby("rule")[["P(any)", "relief_days", "cv", "share_abnormal_relieved", "product_gap",
                                 "product_verdict_flip"]].mean().reindex(RULES)
        write_csv(tab.round(3), "rq5_clauses_present")
        print(tab.round(3).to_string())
    if part in ("future", "all"):
        f = future()
        f.round(4).to_csv(PROC / "rq5_future_cells.csv", index=False)
        nat = f.groupby(["scenario", "rule", "model"])[["hist_days", "stale_days", "updated_days", "hist_P",
                                                        "stale_P", "updated_P"]].mean()
        nat["d_stale_days"] = nat.stale_days - nat.hist_days
        nat["d_updated_days"] = nat.updated_days - nat.hist_days
        nat["d_stale_P"] = nat.stale_P - nat.hist_P
        nat["d_updated_P"] = nat.updated_P - nat.hist_P
        g = nat.groupby(level=["scenario", "rule"])
        tab = pd.concat({"median": g.median(), "p10": g.quantile(0.1), "p90": g.quantile(0.9)}, axis=1)
        write_csv(tab.round(3), "rq5_clauses_future")
        print(tab.xs("median", axis=1, level=0).round(2).to_string())
