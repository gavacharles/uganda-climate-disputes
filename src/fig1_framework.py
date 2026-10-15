"""Fig. 1: conceptual framework - the weather is held fixed and the contractual test varied."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from common import BLUE, CAT, INK, INK2, RED, save

fig, ax = plt.subplots(figsize=(10, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.2)
ax.axis("off")


def box(x, y, w, h, title, body, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08", fc=color, ec="none",
                                alpha=0.18))
    ax.text(x + w / 2, y + h - 0.22, title, ha="center", va="top", fontsize=9.5, fontweight="bold", color=INK)
    ax.text(x + w / 2, y + h - 0.55, body, ha="center", va="top", fontsize=8, color=INK2, linespacing=1.35)


def arrow(x0, x1, y):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=14, color=INK2, lw=1.2))


box(0.1, 1.2, 2.1, 2.6, "Climate record", "45 yr daily rainfall\n(CHIRPS, ARC2, CPC)\nheat stress (POWER)\nCMIP6 to 2041-2070\n\nheld fixed", BLUE[3])
box(2.7, 1.2, 2.6, 2.6, "Contractual test", "choices left open:\nhazard, dataset, baseline,\nwindow, trend, summation\n\nform: FIDIC Guide, NEC4,\nJCT practice, MoWT 1229\n\nvaried", CAT[1])
box(5.8, 1.2, 1.8, 2.6, "Entitlement", "relief yes / no\nEOT days\nwho carries\nthe excess", CAT[2])
box(8.1, 1.2, 1.8, 2.6, "Dispute risk", "verdict flips under\ndefensible choices\n\ncost of\nclimate drift", RED[3])
arrow(2.25, 2.65, 2.5)
arrow(5.35, 5.75, 2.5)
arrow(7.65, 8.05, 2.5)
ax.text(5.0, 0.55, "Evidence from practice: contract and claim documents, four Ugandan road projects (Projects A-D)",
        ha="center", fontsize=8.5, color=INK2, style="italic")
ax.text(5.0, 0.2, "Proposed remedy: Shared Weather Allowance - data, tables and shares fixed at tender",
        ha="center", fontsize=8.5, color=INK, fontweight="bold")
save(fig, "fig1_framework")
