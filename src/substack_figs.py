"""Single-panel, phone-sized figures for the Substack post (in addition to the substack_* panels in figs_extra.py).

  substack_contested        Finding 1: what makes an arguable claim season contested (from fig17's data)
  substack_three_contracts  Finding 3: share of 3-year contracts with weather relief under FIDIC, NEC4, 1-in-10
  substack_project_claim    Finding 4: Project A, total EOT under each defensible choice vs the 21 days granted
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap

from common import BLUE, CAT, GRID, INK2, MUTED, PROC, RED, RES, save
from wp1_map import draw


def contested():
    w = pd.read_csv(PROC / "rq2_window_flags.csv")
    a = w[w.any_exceptional]
    c = a[a.contested]
    p, b, t = c.flip_product, c.flip_baseline, c.flip_trend
    cats = {"The rainfall dataset alone": p & ~b & ~t,
            "Whether to allow for climate trend": t & ~p & ~b,
            "How many years count as 'normal'": b & ~p & ~t,
            "Two or more of these choices": (p.astype(int) + b.astype(int) + t.astype(int)) >= 2,
            "Only a combination of choices": ~(p | b | t)}
    shares = {k: v.mean() * len(c) / len(a) for k, v in cats.items()}
    shares["Not contested: every choice agrees"] = 1 - len(c) / len(a)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    keys = list(shares)[::-1]
    vals = [shares[k] * 100 for k in keys]
    cols = [GRID] + [CAT[0]] * 5
    ax.barh(range(len(keys)), vals, color=cols[::1], height=0.6)
    for i, v in enumerate(vals):
        ax.text(v + 0.8, i, f"{v:.0f}%", va="center", fontsize=10, fontweight="bold")
    ax.set_yticks(range(len(keys)), keys, fontsize=9)
    ax.set_xlim(0, max(vals) * 1.2)
    ax.set_xlabel("Share of arguable claim seasons (%)")
    ax.set_title(f"{len(c) / len(a):.0%} of arguable weather claims flip with the data choice", loc="left",
                 fontsize=11)
    ax.grid(axis="y", visible=False)
    save(fig, "substack_contested")
    plt.close(fig)


def three_contracts():
    g = pd.read_csv(RES / "rq3_forms_grid.csv")
    bounds = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0001]
    cmap = ListedColormap(["#f0efec", BLUE[0], BLUE[1], BLUE[3], BLUE[5], BLUE[6]])
    norm = BoundaryNorm(bounds, cmap.N)
    forms = [("FIDIC Guide", "FIDIC"), ("NEC4", "NEC4"), ("Monthly 1-in-10 (JCT practice)", "1-in-10 month")]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.4))
    for ax, (f, lab) in zip(axes, forms):
        draw(ax, g, f + " P(any)", cmap, norm, "")
        ax.set_title(f"{lab}\n{g[f + ' P(any)'].mean():.0%} of contracts", fontsize=10.5)
    cb = fig.colorbar(plt.cm.ScalarMappable(norm, cmap), ax=axes, orientation="horizontal", fraction=0.06,
                      pad=0.04, ticks=[0, 0.1, 0.25, 0.5, 0.75, 0.9, 1])
    cb.set_label("Share of 3-year contracts that get any weather extension", fontsize=9)
    fig.suptitle("Same rain, different contract", x=0.03, ha="left", fontweight="bold", fontsize=12)
    save(fig, "substack_three_contracts")
    plt.close(fig)


def project_claim():
    tot = pd.read_csv(RES / "case_package5.csv")
    tot = tot[tot.complete & (tot.point == "Masindi (station)")]
    rows = []
    for _, r in tot.iterrows():
        base = "2005-17" if r.baseline.startswith("2005") else "1989-2018"
        span = "claim period" if "claim" in r.window else "whole contract"
        rows.append((f"{r['product']}, {base} normal, {span}", r["EOT algebraic (spec)"], r["EOT positive months only"]))
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for i, (lab, a, p) in enumerate(rows):
        ax.plot([a, p], [i, i], color=GRID, lw=3, zorder=1)
        ax.scatter(a, i, color=CAT[3], s=55, zorder=2, label="As the clause is written" if i == 0 else None)
        ax.scatter(p, i, color=RED[4], s=55, zorder=2, label="Adding only the wet months" if i == 0 else None)
    ax.axvline(21, color=INK2, ls="--", lw=1.3)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=8.5)
    ax.set_ylim(len(rows) - 0.5, -1.1)
    ax.text(21.8, -0.75, "21 days granted", fontsize=9, color=INK2, va="center")
    ax.set_xlabel("Extension of time (days)")
    lo = min(min(a, p) for _, a, p in rows)
    hi = max(max(a, p) for _, a, p in rows)
    ax.set_title(f"One real claim: the same rain gives {lo:.0f} to {hi:.0f} days", loc="left", fontsize=11)
    ax.legend(fontsize=8.5, loc="upper center", bbox_to_anchor=(0.35, -0.13), ncol=2, frameon=False)
    ax.grid(axis="y", visible=False)
    save(fig, "substack_project_claim")
    plt.close(fig)


if __name__ == "__main__":
    contested()
    three_contracts()
    project_claim()
