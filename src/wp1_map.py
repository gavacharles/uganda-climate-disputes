"""WP1 national maps: where would a 3-year contract's weather claim have passed the FIDIC Guide test?

For every CHIRPS cell in Uganda: lost working days (>= 10 mm/day) in OND 2019 and MAM 2020 versus the
1981-2017 baseline of the same window; EI = GEV return period / 3 years. ARC2 (regridded to the CHIRPS
cells by averaging verdicts of the 0.1 deg cells inside each 0.25 deg cell) gives the product-agreement map.
Outputs: results/wp1_grid_ei.csv, figures/wp1_map_ei.png.
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap
from shapely.geometry import Point

import ei
from common import BLUE, GRID, INK2, MUTED, RAW, RED, SITES, load_product, save, write_csv

TFC, BASELINE = 3.0, (1981, 2017)
WINDOWS = {"OND 2019": ("2019-10-01", "2019-12-31"), "MAM 2020": ("2020-03-01", "2020-05-31")}


def uganda():
    return gpd.read_file(RAW / "uganda_adm1.geojson").dissolve()


def grid_ei(product, s, e):
    da = load_product(product)
    shape = uganda().geometry.iloc[0]
    rows = []
    for lat in da.lat.values:
        for lon in da.lon.values:
            if not shape.contains(Point(float(lon), float(lat))):
                continue
            x = da.sel(lat=lat, lon=lon).to_series().astype(float)
            r = ei.assess(x, s, e, TFC, baseline=BASELINE, indicators_=("lwd10",)).iloc[0]
            rows.append({"lat": float(lat), "lon": float(lon), "value": r["value"],
                         "threshold": r["threshold_value_rp4tfc"], "rp_empirical": r["rp_empirical"],
                         "rp_gev": r["rp_gev"], "ei": r["ei"], "verdict": r["verdict"]})
    return pd.DataFrame(rows)


def agreement(chirps, arc2):
    """Share of ARC2 cells inside each CHIRPS cell that are 'exceptional', vs the CHIRPS verdict."""
    a = arc2.copy()
    a["clat"] = (np.floor(a.lat / 0.25) * 0.25 + 0.125).round(3)
    a["clon"] = (np.floor(a.lon / 0.25) * 0.25 + 0.125).round(3)
    a = a[a.verdict != "n/a"]                  # masked / missing ARC2 cells do not vote
    share = (a.assign(exc=a.verdict == "exceptional").groupby(["clat", "clon"]).exc.mean()
             .rename("arc2_share_exceptional"))
    c = chirps.assign(clat=chirps.lat.round(3), clon=chirps.lon.round(3))
    return c.merge(share.reset_index(), on=["clat", "clon"], how="left").drop(columns=["clat", "clon"])


def draw(ax, df, col, cmap, norm, title, sites=False):
    step = 0.25
    for _, r in df.iterrows():
        v = r[col]
        if not np.isfinite(v):
            continue
        ax.add_patch(plt.Rectangle((r.lon - step / 2, r.lat - step / 2), step, step,
                                   color=cmap(norm(v)), lw=0))
    uganda().boundary.plot(ax=ax, color=INK2, lw=0.6)
    for name, (lat, lon, _) in (SITES.items() if sites else []):
        ax.plot(lon, lat, "o", ms=3.5, mfc="white", mec="black", mew=0.7)
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
    out = []
    for wname, (s, e) in WINDOWS.items():
        c = grid_ei("CHIRPS", s, e)
        a = grid_ei("ARC2", s, e)
        g = agreement(c, a).assign(window=wname)
        out.append(g)
        print(wname, "CHIRPS exceptional share:", round((c.verdict == "exceptional").mean(), 2),
              "| ARC2:", round((a.verdict == "exceptional").mean(), 2),
              "| verdicts agree (ARC2 majority vs CHIRPS):",
              round(((g.arc2_share_exceptional >= 0.5) == (g.verdict == "exceptional"))
                    [g.arc2_share_exceptional.notna()].mean(), 2) if g.arc2_share_exceptional.notna().any()
              else "n/a (ARC2 masked)")
    grid = pd.concat(out, ignore_index=True)
    write_csv(grid.round(3), "wp1_grid_ei")

    bounds = [0, 1, 2, 4, 5, 10, 25, 1e9]
    cmap_ei = ListedColormap(["#f0efec", BLUE[0], BLUE[2], RED[1], RED[3], RED[4], RED[6]])
    norm_ei = BoundaryNorm(bounds, cmap_ei.N)
    cmap_ag = ListedColormap([BLUE[3], BLUE[1], "#f0efec", RED[1], RED[3]])
    norm_ag = BoundaryNorm([-1.01, -0.5, -0.01, 0.01, 0.5, 1.01], cmap_ag.N)

    fig, axes = plt.subplots(1, 4, figsize=(11, 3.6))
    for i, w in enumerate(WINDOWS):
        g = grid[grid.window == w]
        draw(axes[i], g, "ei", cmap_ei, norm_ei, f"{w}: EI (CHIRPS)")
        g = g.assign(diff=(g.verdict == "exceptional").astype(float) - g.arc2_share_exceptional)
        draw(axes[2 + i], g, "diff", cmap_ag, norm_ag, f"{w}: CHIRPS vs ARC2")
        if g["diff"].isna().all():
            axes[2 + i].text(32.3, 1.4, "ARC2 masked\n(inhomogeneous\n2020-2023)", ha="center", va="center",
                             fontsize=8, color=MUTED)
    cb = fig.colorbar(plt.cm.ScalarMappable(norm_ei, cmap_ei), ax=axes[:2], orientation="horizontal",
                      fraction=0.05, pad=0.03, ticks=bounds[:-1] + [50])
    cb.ax.set_xticklabels(["0", "1", "2", "4", "5", "10", "25", ""])
    cb.set_label("Exceptionality Index, lost working days (>= 4-5 = exceptional under FIDIC Guide)", fontsize=8)
    cb2 = fig.colorbar(plt.cm.ScalarMappable(norm_ag, cmap_ag), ax=axes[2:], orientation="horizontal",
                       fraction=0.05, pad=0.03, ticks=[-1, 0, 1])
    cb2.ax.set_xticklabels(["only ARC2 says exceptional", "agree", "only CHIRPS says exceptional"], fontsize=7)
    cb2.set_label("Verdict disagreement between products", fontsize=8)
    fig.suptitle("Would a weather claim on a 3-year contract (awarded 2018) have been 'exceptional'?",
                 x=0.06, y=0.9, ha="left", fontweight="bold", fontsize=10)
    save(fig, "wp1_map_ei")
