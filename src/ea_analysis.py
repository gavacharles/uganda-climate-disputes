"""East Africa extension: contract forms, candidate clauses and product sensitivity in Uganda, Kenya, Tanzania,
Rwanda and Burundi (every CHIRPS 0.25 deg land cell; CPC nearest 0.5 deg cell as the second product).

Per cell, 3-year contracts starting each month 1991-2018 against the 1991-2020 normal (as rq5_clauses.present):
P(any relief), relief days, CV, share of above-normal lost days relieved, CHIRPS-CPC relief gap and verdict flips,
for the FIDIC Guide, NEC4 and the candidate clauses; plus the JCT-style monthly rule from rq3_forms.
Outputs: results/ea_clauses_countries.csv, results/ea_forms_countries.csv, figures/ea_forms_map.png
"""
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap

from common import BLUE, PROC, RED, load_product, save, write_csv
from regions import countries, ea_cells
from rq3_forms import FORMS, contracts, monthly_flags
from rq5_clauses import RULES, STARTS, present_cell

COUNTRY_ORDER = ["Uganda", "Kenya", "Tanzania", "Rwanda", "Burundi", "All"]


def cell(args):
    lat, lon, country, xc, xp = args
    rows = present_cell((lat, lon, country, xc, xp))
    c = contracts(monthly_flags(xc), STARTS)
    forms = {"lat": lat, "lon": lon, "country": country}
    for f in FORMS:
        forms[f + " P(any)"] = c[f + "_any"].mean()
        forms[f + " days"] = c[f + "_days"].mean()
    return rows, forms


def by_country(df, cols, key="country"):
    t = df.groupby(key)[cols].mean()
    t.loc["All"] = df[cols].mean()
    return t.reindex([c for c in COUNTRY_ORDER if c in t.index])


def ea_map(ax, df, col, cmap, norm, title, step=0.25):
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


def plot(forms, clauses):
    b = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0001]
    cm = ListedColormap(["#f0efec", BLUE[0], BLUE[1], BLUE[3], BLUE[5], BLUE[6]])
    db = [0, 2, 4, 6, 8, 12, 20]
    dcm = ListedColormap(["#f0efec", RED[0], RED[1], RED[2], RED[3], RED[4], RED[6]])
    fb = [0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
    fcm = ListedColormap(["#f0efec", RED[0], RED[1], RED[3], RED[4], RED[6]])
    flip = clauses[clauses.rule == RULES[0]][["lat", "lon", "product_verdict_flip"]]
    fig, ax = plt.subplots(1, 4, figsize=(13, 4.6))
    ea_map(ax[0], forms, "FIDIC Guide P(any)", cm, BoundaryNorm(b, cm.N), "FIDIC Guide:\ncontracts with relief")
    ea_map(ax[1], forms, "NEC4 P(any)", cm, BoundaryNorm(b, cm.N), "NEC4:\ncontracts with relief")
    ea_map(ax[2], forms, "FIDIC Guide days", dcm, BoundaryNorm(db, dcm.N, extend="max"), "FIDIC Guide:\nrelief days per contract")
    ea_map(ax[3], flip, "product_verdict_flip", fcm, BoundaryNorm(fb, fcm.N), "FIDIC verdict differs,\nCHIRPS vs CPC")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(b, cm.N), cm), ax=ax[:2], orientation="horizontal",
                 fraction=0.05, pad=0.03, ticks=[0, 0.1, 0.25, 0.5, 0.75, 0.9, 1],
                 label="Share of 3-year contracts with any relief")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(db, dcm.N, extend="max"), dcm), ax=ax[2], orientation="horizontal",
                 fraction=0.05, pad=0.03, ticks=db, extend="max", label="Relief days per contract")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(fb, fcm.N), fcm), ax=ax[3], orientation="horizontal",
                 fraction=0.05, pad=0.03, ticks=fb, label="Share of contracts")
    fig.suptitle("East Africa: weather relief on 3-year contracts, 1991-2020 (CHIRPS)", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "ea_forms_map")


if __name__ == "__main__" and __import__("sys").argv[1:] == ["plot"]:
    plot(pd.read_csv(PROC / "ea_forms_cells.csv"), pd.read_csv(PROC / "ea_clauses_cells.csv"))
elif __name__ == "__main__":
    chirps, cpc = load_product("CHIRPS_EA"), load_product("CPC")
    jobs = [(lat, lon, ctry, chirps.sel(lat=lat, lon=lon).to_series().astype(float).loc[:"2020-12-31"],
             cpc.sel(lat=lat, lon=lon, method="nearest").to_series().astype(float).loc[:"2020-12-31"])
            for lat, lon, ctry in ea_cells(chirps)]
    print("cells", len(jobs), flush=True)
    with Pool(8) as pool:
        out = pool.map(cell, jobs, chunksize=8)
    clauses = pd.DataFrame([r for rows, _ in out for r in rows]).rename(columns={"region": "country"})
    forms = pd.DataFrame([f for _, f in out])
    clauses.round(4).to_csv(PROC / "ea_clauses_cells.csv", index=False)
    forms.round(4).to_csv(PROC / "ea_forms_cells.csv", index=False)

    ccols = ["P(any)", "relief_days", "cv", "share_abnormal_relieved", "product_gap", "product_verdict_flip"]
    ctab = clauses.groupby(["rule", "country"])[ccols].mean().unstack("rule")
    ctab = pd.concat([ctab, clauses.groupby("rule")[ccols].mean().unstack().to_frame("All").T])
    write_csv(ctab.round(3), "ea_clauses_countries")
    ftab = by_country(forms, [c for c in forms.columns if c not in ("lat", "lon", "country")])
    write_csv(ftab.round(3), "ea_forms_countries")
    pd.set_option("display.width", 250)
    print(ftab.round(2).to_string())
    print(clauses.groupby(["rule"])[ccols].mean().reindex(RULES).round(3).to_string())

    plot(forms, clauses)
    raise SystemExit
    fig, ax = plt.subplots(1, 4, figsize=(13, 4.4))
    ea_map(ax[0], forms, "FIDIC Guide P(any)", cm, BoundaryNorm(b, cm.N), "FIDIC Guide:\ncontracts with relief")
    ea_map(ax[1], forms, "NEC4 P(any)", cm, BoundaryNorm(b, cm.N), "NEC4:\ncontracts with relief")
    ea_map(ax[2], forms, "FIDIC Guide days", dcm, BoundaryNorm(db, dcm.N), "FIDIC Guide:\nrelief days per contract")
    fb = [0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0001]
    fcm = ListedColormap(["#f0efec", RED[0], RED[1], RED[3], RED[4], RED[6]])
    ea_map(ax[3], flip, "product_verdict_flip", fcm, BoundaryNorm(fb, fcm.N), "FIDIC verdict differs,\nCHIRPS vs CPC")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(b, cm.N), cm), ax=ax[:2], orientation="horizontal",
                 fraction=0.05, pad=0.03, label="Share of 3-year contracts")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(db, dcm.N), dcm), ax=ax[2], orientation="horizontal",
                 fraction=0.05, pad=0.03, label="Lost working days")
    fig.colorbar(plt.cm.ScalarMappable(BoundaryNorm(fb, fcm.N), fcm), ax=ax[3], orientation="horizontal",
                 fraction=0.05, pad=0.03, label="Share of contracts")
    fig.suptitle("East Africa: weather relief on 3-year contracts, 1991-2020 (CHIRPS)", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "ea_forms_map")
