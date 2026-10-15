"""RQ6: heat as an "exceptionally adverse climatic condition" in Uganda.

Heat-stress index: simplified wet-bulb globe temperature (sWBGT, Australian Bureau of Meteorology form)
  sWBGT = 0.567 Tmax + 0.393 e + 3.94,  e = 6.105 exp(17.27 Td / (237.7 + Td))   [degC, hPa]
from NASA POWER daily maximum temperature and dewpoint (1981-2025) at POWER grid points in Uganda.
A heat-lost day is a day with sWBGT >= 30 degC (sensitivities 29 and 31 degC): heavy outdoor work by acclimatised
workers must be substantially curtailed (check against ISO 7243 / ACGIH reference values before citing).

Per point:
  observed trend in annual heat days (Theil-Sen, Kendall p);
  FIDIC Guide test on seasonal heat days (RP >= 15 yr, 1991-2020 normal) for 3-year contracts starting 1991-2018;
  stationary vs trend-aware verdicts for claim seasons 2001-2025 (as rq2 for rain);
  Shared Weather Allowance heat row (monthly mean and 1-in-10 heat days; shared band);
  projected 2041-2070: monthly CMIP6 ensemble-median warming added to Tmax and Td (constant dewpoint depression),
  stale vs updated baselines;
  heat days vs rain lost days (CHIRPS, >= 10 mm) per contract.
Outputs: results/rq6_heat_points.csv, results/rq6_heat_regions.csv, figures/rq6_heat_map.png
"""
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import BoundaryNorm, ListedColormap
from scipy import stats

import ei
from common import BLUE, RAW, RED, load_product, save, write_csv
from regions import region_of, region_summary, uganda_shape

THR, SENS = 30.0, (29.0, 31.0)
BASELINE = (1991, 2020)
STARTS = pd.date_range("1991-01-01", "2018-01-01", freq="MS")
RP = 15.0


def swbgt(tmax, td):
    e = 6.105 * np.exp(17.27 * td / (237.7 + td))
    return 0.567 * tmax + 0.393 * e + 3.94


def monthly_count(flag):
    return flag.astype(float).where(flag.notna()).resample("MS").sum(min_count=28)


def season_sums(mc):
    q = mc.resample("QS-DEC").agg(["sum", "count"])
    return q["sum"][q["count"] == 3]


def fidic(mc, base_mc, starts=STARTS):
    """Per contract: any season with heat days >= 15-yr return level (baseline from base_mc), relief = excess over mean."""
    q, qb_all = season_sums(mc), season_sums(base_mc)
    qb = qb_all[(qb_all.index.year >= BASELINE[0]) & (qb_all.index.year <= BASELINE[1])]
    exc = pd.Series(0.0, index=q.index)
    trig = pd.Series(False, index=q.index)
    for m in (12, 3, 6, 9):
        b = qb[qb.index.month == m].values
        thr, mu = ei.return_level(b, RP), b.mean()
        s = q[q.index.month == m]
        hit = (s >= thr) & (s > 0)
        trig[s.index] = hit
        exc[s.index] = np.where(hit, np.maximum(s - mu, 0), 0)
    anyx, days = [], []
    for st in starts:
        end = st + pd.DateOffset(months=36)
        sel = (q.index >= st) & (q.index + pd.DateOffset(months=2) < end)
        anyx.append(trig[sel].any())
        days.append(exc[sel].sum())
    return np.mean(anyx), np.mean(days)


def swa(mc, base_mc, starts=STARTS):
    b = base_mc[(base_mc.index.year >= BASELINE[0]) & (base_mc.index.year <= BASELINE[1])]
    mean = b.groupby(b.index.month).mean().reindex(mc.index.month).values
    q90 = b.groupby(b.index.month).quantile(0.9).reindex(mc.index.month).values
    L = mc.values
    rel = pd.Series(0.5 * np.clip(L - mean, 0, np.maximum(q90 - mean, 0)) + np.maximum(L - q90, 0), index=mc.index)
    return np.mean([rel.loc[s: s + pd.DateOffset(months=35)].sum() for s in starts])


def per_contract(mc, starts=STARTS):
    return np.mean([mc.loc[s: s + pd.DateOffset(months=35)].sum() for s in starts])


def trend_flips(mc):
    """Claim seasons 2001-2025: share where stationary and trend-aware GEV verdicts differ (prior data only)."""
    q = season_sums(mc)
    flips, arguable = [], []
    for t in q.loc["2000-12-01":"2025-09-01"].index:
        hist = q[(q.index.month == t.month) & (q.index < t)]
        if len(hist) < 15:
            continue
        thr_s = ei.return_level(hist.values, RP)
        p = ei.fit_gev_ns(hist.values, hist.index.year.values)
        if p is None or not np.isfinite(thr_s):
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            thr_t = float(stats.genextreme.isf(1 / RP, p["c"], p["mu0"] + p["mu1"] * (t.year - p["t0"]), p["scale"]))
        v = q[t]
        a, b = v >= thr_s and v > 0, v >= thr_t and v > 0
        flips.append(a != b)
        arguable.append(a or b)
    return float(np.mean(flips)) if flips else np.nan, float(np.mean(arguable)) if arguable else np.nan


def main():
    d = xr.open_dataset(RAW / "power_daily.nc")[["T2M_MAX", "T2MDEW"]].load()
    dT = xr.open_dataset(RAW / "cmip6_deltas_obsgrid.nc").dT
    chirps = load_product("CHIRPS")
    shape = uganda_shape()
    rows = []
    for lat in d.lat.values:
        for lon in d.lon.values:
            tx = d.T2M_MAX.sel(lat=lat, lon=lon).to_series()
            td = d.T2MDEW.sel(lat=lat, lon=lon).to_series()
            if tx.isna().all() or not shape.contains(__import__("shapely.geometry", fromlist=["Point"]).Point(lon, lat)):
                continue
            reg = region_of(lat, lon) or "Uganda"
            w = swbgt(tx, td).loc[:"2025-12-31"]
            r = {"lat": float(lat), "lon": float(lon), "region": reg,
                 "sWBGT_median": w.median(), "sWBGT_p95": w.quantile(0.95)}
            for thr in (THR,) + SENS:
                ann = (w >= thr).groupby(w.index.year).sum().loc[1981:2025]
                r[f"heat_days_yr_{thr:g}"] = ann.loc[BASELINE[0]:BASELINE[1]].mean()
            ann = (w >= THR).groupby(w.index.year).sum().loc[1981:2025].astype(float)
            sl = stats.theilslopes(ann.values, ann.index.values)
            r["trend_days_per_decade"] = 10 * sl[0]
            r["trend_p"] = stats.kendalltau(ann.index.values, ann.values).pvalue
            mc = monthly_count(w >= THR)
            mc_p = mc.loc["1991":"2020"]
            r["heat_days_per_contract"] = per_contract(mc_p)
            r["fidic_P"], r["fidic_days"] = fidic(mc_p, mc_p)
            r["swa_days"] = swa(mc_p, mc_p)
            r["trend_flip"], r["trend_arguable"] = trend_flips(mc)
            # rain lost days at the nearest CHIRPS cell, same contracts
            rain = chirps.sel(lat=lat, lon=lon, method="nearest").to_series().loc["1991":"2020"]
            r["rain_lwd_per_contract"] = per_contract(monthly_count(rain >= 10))
            # projected warming (monthly ensemble median), added to Tmax and Td
            for scen in ("ssp245", "ssp585"):
                dt = dT.sel(scenario=scen).sel(lat=lat, lon=lon, method="nearest").values   # 12 months
                add = dt[w.loc["1991":"2020"].index.month - 1]
                wf = swbgt(tx.loc["1991":"2020"] + add, td.loc["1991":"2020"] + add)
                mf = monthly_count(wf >= THR)
                r[f"{scen}_dT"] = float(np.mean(dt))
                r[f"{scen}_heat_days_per_contract"] = per_contract(mf)
                r[f"{scen}_stale_fidic_P"], r[f"{scen}_stale_fidic_days"] = fidic(mf, mc_p)
                r[f"{scen}_updated_fidic_P"], r[f"{scen}_updated_fidic_days"] = fidic(mf, mf)
                r[f"{scen}_stale_swa_days"] = swa(mf, mc_p)
                r[f"{scen}_updated_swa_days"] = swa(mf, mf)
            rows.append(r)
    g = pd.DataFrame(rows)
    g["heat_share_of_lost_days"] = g.heat_days_per_contract / (g.heat_days_per_contract + g.rain_lwd_per_contract)
    write_csv(g.round(3), "rq6_heat_points")
    cols = [c for c in g.columns if c not in ("lat", "lon", "region")]
    reg = region_summary(g, cols)
    write_csv(reg.round(3), "rq6_heat_regions")
    pd.set_option("display.width", 250)
    print(reg.T.round(2).to_string())
    print("points:", len(g), " with heat days >= 1/yr:", int((g[f"heat_days_yr_{THR:g}"] >= 1).sum()))

    fig, ax = plt.subplots(1, 4, figsize=(13, 4))
    step = 0.5
    labels = {"heat_days_yr_30": "Days per year", "trend_days_per_decade": "Days per decade",
              "d585": "Extra heat-lost days per contract", "dP585": "Change in share of contracts"}
    panels = [("heat_days_yr_30", "Heat-lost days per year\n(sWBGT >= 30 C), 1991-2020",
               [0, 1, 5, 15, 30, 60, 120, 400], ListedColormap(["#f0efec", RED[0], RED[1], RED[2], RED[3], RED[4], RED[6]])),
              ("trend_days_per_decade", "Observed trend 1981-2025\n(days per decade)",
               [-20, -5, -1, 1, 5, 10, 20, 100], ListedColormap([BLUE[3], BLUE[1], "#f0efec", RED[0], RED[1], RED[3], RED[5]])),
              ("d585", "Change in heat days per 3-yr\ncontract, SSP5-8.5 2041-2070",
               [-1, 1, 10, 30, 60, 120, 240, 2000], ListedColormap(["#f0efec", RED[0], RED[1], RED[2], RED[3], RED[4], RED[6]])),
              ("dP585", "FIDIC 'exceptional' heat: change in\nshare of contracts, stale baseline",
               [0, 0.2, 0.4, 0.6, 0.8, 1.0], ListedColormap(["#f0efec", RED[1], RED[2], RED[4], RED[6]]))]
    g["d585"] = g.ssp585_heat_days_per_contract - g.heat_days_per_contract
    g["dP585"] = g.ssp585_stale_fidic_P - g.fidic_P
    from wp1_map import draw
    for a, (col, title, b, cm) in zip(ax, panels):
        _tiles(a, g, col, cm, BoundaryNorm(b, cm.N), title, step)
        cb = fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(b, cm.N), cm), ax=a, orientation="horizontal",
                          fraction=0.05, pad=0.03, ticks=b)
        cb.set_label(labels[col], fontsize=8)
        cb.ax.tick_params(labelsize=7, rotation=45 if len(b) > 6 else 0)
    fig.suptitle("Heat as a contractual climatic condition in Uganda (NASA POWER; CMIP6 ensemble-median warming)",
                 x=0.06, ha="left", fontweight="bold", fontsize=10)
    save(fig, "rq6_heat_map")


def _tiles(ax, df, col, cmap, norm, title, step):
    from regions import regions
    for _, r in df.iterrows():
        if np.isfinite(r[col]):
            ax.add_patch(plt.Rectangle((r.lon - step / 2, r.lat - step / 2), step, step, color=cmap(norm(r[col])), lw=0))
    for _, geom in regions():
        for poly in getattr(geom, "geoms", [geom]):
            ax.plot(*poly.exterior.xy, color="#52514e", lw=0.5)
    ax.set_xlim(29.4, 35.2)
    ax.set_ylim(-1.6, 4.4)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)


if __name__ == "__main__":
    main()
