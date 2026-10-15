"""WP1 demonstration: Exceptionality Index for illustrative claim windows at sample project sites.

Scenario: contracts awarded in 2018 with a 3-year Time for Completion (typical for Ugandan public works), so the 1981-2017 record is the
pre-award climatic baseline. Claim windows are the two rainy seasons that fall in the contract period:
OND 2019 (record short rains, strong positive Indian Ocean Dipole) and MAM 2020 (very wet long rains).
MAM 2019 serves as a less extreme control.
Outputs: results/wp1_site_ei.csv, results/wp1_nec_monthly.csv, results/wp1_sensitivity.csv, figures.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ei
from common import BLUE, CAT, INK2, MUTED, RED, SITES, save, site_series, write_csv

TFC = 3.0
BASELINE = (1981, 2017)
WINDOWS = {"MAM 2019": ("2019-03-01", "2019-05-31"),
           "OND 2019": ("2019-10-01", "2019-12-31"),
           "MAM 2020": ("2020-03-01", "2020-05-31")}


def site_table():
    rows, nec = [], []
    for site, (lat, lon, kind) in SITES.items():
        x = site_series(lat, lon, "CHIRPS")
        for wname, (s, e) in WINDOWS.items():
            df = ei.assess(x, s, e, TFC, baseline=BASELINE)
            df.insert(0, "window", wname)
            df.insert(0, "site", site)
            rows.append(df)
            n = ei.nec_monthly(x, s, e, baseline=BASELINE)
            n.insert(0, "window", wname)
            n.insert(0, "site", site)
            nec.append(n)
    return pd.concat(rows, ignore_index=True), pd.concat(nec, ignore_index=True)


def sensitivity():
    """lwd10 EI for OND 2019 by product (CHIRPS vs ARC2) and baseline length (10, 20, 30 yrs, full)."""
    s, e = WINDOWS["OND 2019"]
    rows = []
    for site, (lat, lon, _) in SITES.items():
        for prod in ("CHIRPS", "ARC2"):
            x = site_series(lat, lon, prod)
            first = x.index.min().year
            for label, b0 in [("10 yr", 2008), ("20 yr", 1998), ("30 yr", 1988), ("full", first)]:
                r = ei.assess(x, s, e, TFC, baseline=(max(b0, first), 2017), indicators_=("lwd10",)).iloc[0]
                rows.append({"site": site, "product": prod, "baseline": label, "baseline_n": r["baseline_n"],
                             "lwd10": r["value"], "rp_empirical": r["rp_empirical"], "rp_gev": r["rp_gev"],
                             "ei": r["ei"], "ei_method": r["ei_method"], "verdict": r["verdict"]})
    return pd.DataFrame(rows)


def fig_sites(table):
    """Strip plot: baseline lwd10 for OND at each site, with the OND 2019 and the RP = 4 x TfC threshold."""
    s, e = WINDOWS["OND 2019"]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    names = list(SITES)
    for i, site in enumerate(names):
        lat, lon, _ = SITES[site]
        base = ei.window_values(site_series(lat, lon), s, e, range(*BASELINE[:1], BASELINE[1] + 1))["lwd10"]
        jitter = np.random.default_rng(i).uniform(-0.18, 0.18, len(base))
        ax.scatter(base.values, i + jitter, s=10, color=BLUE[2], alpha=0.8, lw=0,
                   label="OND in baseline years 1981-2017" if i == 0 else None)
        row = table[(table.site == site) & (table.window == "OND 2019") & (table.indicator == "lwd10")].iloc[0]
        ax.plot([row.threshold_value_rp4tfc] * 2, [i - 0.3, i + 0.3], color=INK2, lw=1.2,
                label="Exceptional threshold (RP = 4 x TfC = 12 yr)" if i == 0 else None)
        ax.scatter([row.value], [i], s=46, color=RED[3], zorder=3, label="OND 2019" if i == 0 else None)
        ax.text(row.value + 0.8, i, f"EI {row.ei:.1f}",
                va="center", fontsize=7.5, color=RED[4])
    ax.set_yticks(range(len(names)), names)
    ax.invert_yaxis()
    ax.set_xlabel("Lost working days (rain >= 10 mm/day) in October-December")
    ax.set_title("OND 2019 against each site's pre-award baseline (CHIRPS, TfC = 3 years)")
    ax.legend(loc="lower right", fontsize=7.5)
    ax.grid(axis="y", visible=False)
    save(fig, "wp1_sites_ond2019")
    plt.close(fig)


def fig_sensitivity(sens):
    piv = sens.pivot_table(index="site", columns=["product", "baseline"], values="ei")
    order = ["10 yr", "20 yr", "30 yr", "full"]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    names = list(SITES)
    width = 0.1
    for j, prod in enumerate(("CHIRPS", "ARC2")):
        for k, b in enumerate(order):
            off = (j * 4 + k - 3.5) * width
            ax.barh(np.arange(len(names)) + off, piv.loc[names, (prod, b)].values, height=width,
                    color=(BLUE if prod == "CHIRPS" else RED)[2 + k], label=f"{prod}, {b}")
    ax.axvline(4, color=INK2, lw=1, ls="--")
    ax.axvline(5, color=INK2, lw=1)
    ax.set_yticks(range(len(names)), names)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlabel("Exceptionality Index (return period / TfC; empirical for 10-yr baselines), log scale; FIDIC Guide band 4-5")
    ax.set_title("OND 2019, lost working days: sensitivity to rainfall product and baseline length")
    ax.legend(ncol=2, fontsize=7, loc="lower right")
    ax.grid(axis="y", visible=False)
    save(fig, "wp1_sensitivity_ond2019")
    plt.close(fig)


if __name__ == "__main__":
    table, nec = site_table()
    write_csv(table.round(3), "wp1_site_ei")
    write_csv(nec.round(2), "wp1_nec_monthly")
    sens = sensitivity()
    write_csv(sens.round(3), "wp1_sensitivity")
    fig_sites(table)
    fig_sensitivity(sens)
    show = table[table.indicator == "lwd10"].pivot(index="site", columns="window", values="ei").round(1)
    print("\nEI (lwd10, stationary GEV, TfC 3 yr):\n", show)
    print("\nVerdicts:\n", table[table.indicator == "lwd10"].pivot(index="site", columns="window", values="verdict"))
    print("\nNEC months exceeding 1-in-10:\n", nec.groupby(["window"])["exceeds_1in10"].mean().round(2))
