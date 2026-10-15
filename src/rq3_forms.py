"""RQ3: same weather, different contract form. How often does a 3-year contract get weather relief, and how much?

For every CHIRPS cell in Uganda and every 3-year contract starting in each month 1991-01 .. 2023-01, apply:
  FIDIC Guide  season (DJF/MAM/JJA/SON) lost working days (>= 10 mm/day) with RP >= 5 x TfC (15 yr, GEV);
               relief = lost days above the seasonal baseline mean.
  NEC4         month whose rainfall or days >= 5 mm exceed the 1-in-10-year value (cl. 60.1(13));
               relief = only the lost days above the 1-in-10-year month (NEC prices the excess only).
  Monthly 1-in-10, average relief (common JCT practice)
               same monthly trigger; relief = lost days above the monthly mean.
  FIDIC Silver no relief (shown as zero for reference).
Baseline: the 1991-2020 WMO normal for all forms (in-sample for 1991-2020 contracts; see notes).
Outputs: results/rq3_forms_grid.csv, results/rq3_forms_sites.csv, figures/rq3_forms_map.png, rq3_forms_sites.png.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap

import ei
from common import BLUE, CAT, RED, load_product, save, write_csv
from regions import cells, region_summary
from wp1_map import draw

TFC_MONTHS = 36
BASELINE = (1991, 2020)
FIDIC_RP = 5 * TFC_MONTHS / 12           # 15 years (upper end of the Guide's 4-5 x TfC band)
STARTS = pd.date_range("1991-01-01", "2023-01-01", freq="MS")
FORMS = ["FIDIC Guide", "NEC4", "Monthly 1-in-10 (JCT practice)"]


def monthly(x):
    """Monthly rainfall, days >= 5 mm and lost working days (>= 10 mm) from a daily series."""
    ok = x.notna()
    return pd.DataFrame({"rain": x.resample("MS").sum(min_count=28),
                         "d5": (x >= 5).astype(float).where(ok).resample("MS").sum(min_count=28),
                         "lwd": (x >= 10).astype(float).where(ok).resample("MS").sum(min_count=28)}).dropna()


def monthly_flags(x, base=None, baseline=BASELINE):
    """Per month: trigger and relief days under each form. Thresholds come from `base` (daily series) over the
    `baseline` years; default is x itself. Passing a different `base` evaluates x against a fixed (e.g. stale) baseline."""
    m = monthly(x)
    mb = m if base is None else monthly(base)
    b = mb[(mb.index.year >= baseline[0]) & (mb.index.year <= baseline[1])]
    mon = m.index.month
    q90 = b.groupby(b.index.month).quantile(0.9)
    mean = b.groupby(b.index.month).mean()
    trig = (m.rain.values > q90.rain.reindex(mon).values) | (m.d5.values > q90.d5.reindex(mon).values)
    out = pd.DataFrame(index=m.index)
    out["NEC4"] = np.where(trig, np.maximum(m.lwd.values - q90.lwd.reindex(mon).values, 0), 0.0)
    out["NEC4_trig"] = trig
    out["Monthly 1-in-10 (JCT practice)"] = np.where(trig, np.maximum(m.lwd.values - mean.lwd.reindex(mon).values, 0), 0.0)
    out["Monthly 1-in-10 (JCT practice)_trig"] = trig

    # FIDIC Guide on meteorological seasons; quarter result is booked to the quarter's last month
    q = m.lwd.resample("QS-DEC").sum(min_count=3).dropna()
    qa = q if base is None else mb.lwd.resample("QS-DEC").sum(min_count=3).dropna()
    qb = qa[(qa.index.year >= baseline[0]) & (qa.index.year <= baseline[1])]
    fid = pd.Series(0.0, index=m.index)
    fid_trig = pd.Series(False, index=m.index)
    for qm in (12, 3, 6, 9):
        s = q[q.index.month == qm]
        base = qb[qb.index.month == qm].values
        thr, mu = ei.return_level(base, FIDIC_RP), base.mean()
        for t, v in s.items():
            last = t + pd.DateOffset(months=2)
            if last in fid.index and v >= thr:
                fid[last] = max(v - mu, 0.0)
                fid_trig[last] = True
    out["FIDIC Guide"] = fid
    out["FIDIC Guide_trig"] = fid_trig
    return out


def contracts(flags, starts=STARTS):
    """Per contract start: any trigger (bool) and total relief days, for each form."""
    rows = []
    for s in starts:
        w = flags.loc[s: s + pd.DateOffset(months=TFC_MONTHS - 1)]
        if len(w) < TFC_MONTHS:
            continue
        r = {"start": s}
        for f in FORMS:
            r[f + "_any"] = bool(w[f + "_trig"].any())
            r[f + "_days"] = float(w[f].sum())
        rows.append(r)
    return pd.DataFrame(rows)


def summarise(c):
    out = {}
    for f in FORMS:
        out[f + " P(any)"] = c[f + "_any"].mean()
        out[f + " days"] = c[f + "_days"].mean()
    return out


def grid():
    da = load_product("CHIRPS")
    rows = []
    for lat, lon, region in cells(da):
        f = monthly_flags(da.sel(lat=lat, lon=lon).to_series().astype(float).loc[:"2025-12-31"])
        r = summarise(contracts(f))
        r["NEC4 monthly trigger rate"] = f["NEC4_trig"].mean()
        rows.append({"lat": lat, "lon": lon, "region": region, **r})
    return pd.DataFrame(rows)


def fig_map(g):
    bounds = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0001]
    cmap = ListedColormap(["#f0efec", BLUE[0], BLUE[1], BLUE[3], BLUE[5], BLUE[6]])
    norm = BoundaryNorm(bounds, cmap.N)
    dbounds = [0, 2, 5, 10, 20, 40, 1e9]
    dcmap = ListedColormap(["#f0efec", RED[0], RED[1], RED[3], RED[4], RED[6]])
    dnorm = BoundaryNorm(dbounds, dcmap.N)
    fig, axes = plt.subplots(2, 3, figsize=(10, 7.4))
    for j, f in enumerate(FORMS):
        draw(axes[0, j], g, f + " P(any)", cmap, norm, f)
        draw(axes[1, j], g, f + " days", dcmap, dnorm, "")
    cb = fig.colorbar(plt.cm.ScalarMappable(norm, cmap), ax=axes[0], fraction=0.04, pad=0.02,
                      ticks=bounds[:-1] + [1])
    cb.set_label("Share of 3-year contracts with\nat least one relief event", fontsize=8)
    cb2 = fig.colorbar(plt.cm.ScalarMappable(dnorm, dcmap), ax=axes[1], fraction=0.04, pad=0.02,
                       ticks=dbounds[:-1])
    cb2.set_label("Mean relief (lost working days)\nper 3-year contract", fontsize=8)
    fig.suptitle("Same weather, different contract: weather relief on 3-year contracts in Uganda, 1991-2025 (CHIRPS)",
                 x=0.06, ha="left", fontweight="bold", fontsize=10)
    save(fig, "rq3_forms_map")
    plt.close(fig)


def fig_regions(reg):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
    y = np.arange(len(reg))
    h = 0.26
    for j, f in enumerate(FORMS):
        axes[0].barh(y + (j - 1) * h, reg[f + " P(any)"] * 100, height=h, color=CAT[j], label=f)
        axes[1].barh(y + (j - 1) * h, reg[f + " days"], height=h, color=CAT[j])
    axes[0].set_yticks(y, reg.index)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("% of 3-year contracts with any relief event")
    axes[1].set_xlabel("Mean relief per contract (lost working days)")
    axes[0].legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(1.1, -0.2), ncol=3, frameon=False)
    axes[0].set_title("How often relief is triggered")
    axes[1].set_title("How much time is granted")
    for ax in axes:
        ax.grid(axis="y", visible=False)
    save(fig, "rq3_forms_regions")
    plt.close(fig)


if __name__ == "__main__":
    g = grid()
    write_csv(g.round(3), "rq3_forms_grid")
    cols = [c for c in g.columns if c not in ("lat", "lon", "region")]
    reg = region_summary(g, cols)
    write_csv(reg.round(3), "rq3_forms_regions")
    print(reg.round(3).to_string())
    fig_map(g)
    fig_regions(reg)
    print("\nNational medians across cells:\n", g.drop(columns=["lat", "lon", "region"]).median().round(3))
    r = g["NEC4 monthly trigger rate"].median()
    print(f"Independence benchmark 1-(1-p)^36 with median monthly trigger rate {r:.3f}: {1 - (1 - r) ** 36:.3f}")
