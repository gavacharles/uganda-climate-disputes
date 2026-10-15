"""Cover images for LinkedIn (1200x1200) and Substack (1456x816).

Motif: monthly heavy-rain days (>= 10 mm, CHIRPS) at one cell in central Uganda through the record 2019-2020
rains, with the 1-in-10-year monthly threshold from two datasets (CHIRPS and CPC, 1991-2018). Months between the
lines are "exceptional" on one dataset and not on the other: same rain, different verdict.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import FIG, site_series

plt.rcParams["savefig.bbox"] = "standard"   # keep exact canvas size (project default crops tightly)

BG, INK, MUTED = "#0f1b2d", "#f4f1ea", "#9fb0c5"
RAIN, HI, LO = "#3d8fe0", "#f2a541", "#e2574c"
LAT, LON = 0.375, 32.625
WIN = ("2019-01-01", "2020-12-31")


def data():
    out = {}
    for prod in ("CHIRPS", "CPC"):
        x = site_series(LAT, LON, prod)
        m = (x >= 10).astype(float).where(x.notna()).resample("MS").sum(min_count=28)
        base = m.loc["1991":"2018"]
        q90 = base.groupby(base.index.month).quantile(0.9)
        out[prod] = (m, q90)
    m = out["CHIRPS"][0].loc[WIN[0]:WIN[1]]
    thr_c = out["CHIRPS"][1].reindex(m.index.month).values
    thr_p = out["CPC"][1].reindex(m.index.month).values
    return m, thr_c, thr_p


def draw_chart(ax, m, thr_c, thr_p, fs=1.0):
    x = np.arange(len(m))
    lo, hi = np.minimum(thr_c, thr_p), np.maximum(thr_c, thr_p)
    contested = (m.values > lo) & (m.values <= hi)
    above = m.values > hi
    cols = [HI if c else (LO if a else RAIN) for c, a in zip(contested, above)]
    ax.bar(x, m.values, color=cols, width=0.72, zorder=2)
    ax.step(np.r_[x - 0.5, x[-1] + 0.5], np.r_[thr_c, thr_c[-1]], where="post", color=INK, lw=1.6 * fs, zorder=3)
    ax.step(np.r_[x - 0.5, x[-1] + 0.5], np.r_[thr_p, thr_p[-1]], where="post", color=MUTED, lw=1.6 * fs, ls=(0, (3, 2)),
            zorder=3)
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_yticks([])
    ticks = [i for i, t in enumerate(m.index) if t.month in (1, 7)]
    ax.set_xticks(ticks, [m.index[i].strftime("%b %Y") for i in ticks], color=MUTED, fontsize=10 * fs)
    ax.tick_params(length=0)
    ax.grid(False)
    ax.set_xlim(-0.8, len(m) - 0.2)
    return contested.sum()


def key(fig, x, y, fs=1.0, step=0.035):
    items = [(INK, "-", "1-in-10-year month, dataset A"), (MUTED, "--", "1-in-10-year month, dataset B")]
    for i, (c, ls, lab) in enumerate(items):
        fig.lines.append(plt.Line2D([x, x + 0.04], [y - i * step] * 2, color=c, ls=ls, lw=2, transform=fig.transFigure))
        fig.text(x + 0.05, y - i * step, lab, color=MUTED, fontsize=11 * fs, va="center")
    for i, (c, lab) in enumerate([(HI, "'Exceptional' on one dataset only"), (LO, "'Exceptional' on both")]):
        yy = y - (i + 2) * step
        fig.patches.append(plt.Rectangle((x + 0.008, yy - 0.008), 0.024, 0.016, color=c, transform=fig.transFigure))
        fig.text(x + 0.05, yy, lab, color=MUTED, fontsize=11 * fs, va="center")


def linkedin(m, thr_c, thr_p):
    fig = plt.figure(figsize=(12, 12), dpi=100, facecolor=BG)
    fig.text(0.07, 0.90, "CONSTRUCTION LAW  ·  CLIMATE RISK", color=HI, fontsize=17, fontweight="bold")
    fig.text(0.07, 0.86, "When a risk-allocation clause\nbecomes a dispute generator", color=INK, fontsize=46,
             fontweight="bold", va="top", linespacing=1.15)
    fig.text(0.07, 0.665, "“Exceptionally adverse climatic conditions” in Uganda’s road contracts:\n"
             "who decides what is exceptional, and with which data?", color=MUTED, fontsize=19, va="top",
             linespacing=1.4)
    ax = fig.add_axes([0.07, 0.17, 0.86, 0.36])
    draw_chart(ax, m, thr_c, thr_p, fs=1.2)
    fig.text(0.07, 0.555, "Heavy-rain days per month, central Uganda, 2019–2020", color=INK, fontsize=15)
    key(fig, 0.07, 0.115, fs=1.15, step=0.026)
    fig.text(0.93, 0.04, "Gava Charles", color=MUTED, fontsize=15, ha="right")
    fig.savefig(FIG / "cover_linkedin.png", facecolor=BG, dpi=100)
    plt.close(fig)
    print("wrote", FIG / "cover_linkedin.png")


def substack(m, thr_c, thr_p):
    fig = plt.figure(figsize=(14.56, 8.16), dpi=100, facecolor=BG)
    fig.text(0.05, 0.86, "Same rain,\ndifferent verdict", color=INK, fontsize=46, fontweight="bold", va="top",
             linespacing=1.05)
    fig.text(0.05, 0.53, "Why \u201cexceptionally adverse weather\u201d\nis one of the most argued\n"
             "sentences in Ugandan construction", color=MUTED, fontsize=18, va="top", linespacing=1.4)
    ax = fig.add_axes([0.54, 0.33, 0.42, 0.50])
    draw_chart(ax, m, thr_c, thr_p, fs=1.0)
    fig.text(0.54, 0.87, "Heavy-rain days per month, central Uganda, 2019\u20132020", color=INK, fontsize=13)
    key(fig, 0.54, 0.23, fs=1.0, step=0.042)
    fig.text(0.05, 0.07, "Gava Charles", color=HI, fontsize=16, fontweight="bold")
    fig.savefig(FIG / "cover_substack.png", facecolor=BG, dpi=100)
    plt.close(fig)
    print("wrote", FIG / "cover_substack.png")


if __name__ == "__main__":
    m, thr_c, thr_p = data()
    linkedin(m, thr_c, thr_p)
    substack(m, thr_c, thr_p)
