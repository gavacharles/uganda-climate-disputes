"""Additional figures (main text, supplement, Substack).

  fig10_contract_tables      Clause 1229 tables in contracts vs site climate, and EOT per contract
  fig11_projectA             Project A claim: monthly V (claimed vs CHIRPS vs CPC) and totals under all choices
  fig12_swa_schematic        How the Shared Weather Allowance works, vs Clause 1229, NEC4 and the FIDIC Guide
  fig13_risk_split           Who carries above-normal lost days, today and 2041-2070 (stale / updated)
  fig14_rain_heat_calendar   Monthly rain and heat lost days by region
  fig15_eot_distribution     EOT per contract across all contracts and cells, by rule
  fig16_climate_stability    Relief today, stale and updated baseline, by rule (NEX ensemble)
  fig17_contested_sources    What makes a claim season contested
  figS1_arc2_break           ARC2 / CHIRPS national monthly ratio, masked period shaded
  figS2_gauge_vs_grid        Project A site gauge vs gridded days >= 10 mm and monthly rainfall
  substack_*                 single-panel versions of 10, 12 and 14
"""
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from common import BLUE, CAT, GRID, INK, INK2, MUTED, PROC, RAW, RED, RES, load_product, save
from regions import cells

MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
MON3 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
RULE_LABEL = {"FIDIC Guide (status quo)": "FIDIC Guide", "NEC4": "NEC4",
              "MoWT 1229 (algebraic sum)": "Clause 1229\n(as written)",
              "MoWT 1229 (positive months only)": "Clause 1229\n(positive months)",
              "LWD table 1-in-10": "1-in-10 table", "LWD table mean": "Mean table",
              "Shared band": "Shared Weather\nAllowance", "Shared band (netted)": "SWA (netted)"}
MAIN_RULES = ["FIDIC Guide (status quo)", "NEC4", "MoWT 1229 (algebraic sum)", "MoWT 1229 (positive months only)",
              "Shared band"]
RULE_COLOR = dict(zip(MAIN_RULES, [CAT[0], CAT[1], CAT[3], CAT[7], CAT[2]]))


def tidy(ax, ygrid=True):
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", visible=ygrid)


# ---------------------------------------------------------------- 10
def fig10(substack=False):
    t = pd.read_csv(RES / "case_tables.csv")
    e = pd.read_csv(RES / "case_tables_eot.csv")
    names = list(dict.fromkeys(t.table))
    short = {names[0]: "Project D\noriginal table", names[1]: "Project D\naddendum table",
             names[2]: "Project B\ntable"}
    if substack:
        fig, ax = plt.subplots(figsize=(6.4, 3.6))
        rows = [(short[names[0]], e.iloc[0]), ("Project D\nreplacement table", e.iloc[2]),
                ("Built from\nactual rainfall", e.iloc[1])]
        vals = [r["EOT per contract (algebraic)"] for _, r in rows]
        ax.bar(range(3), vals, color=[RED[3], RED[5], BLUE[3]], width=0.6)
        for i, v in enumerate(vals):
            ax.text(i, v + 4, f"{v:.0f} days", ha="center", fontsize=10, fontweight="bold")
        ax.set_ylim(0, max(vals) * 1.18)
        ax.set_xticks(range(3), [r[0] for r in rows])
        ax.set_ylabel("Weather extension per 3-year contract")
        ax.set_title("Same contract, same rain: the rainfall table decides", loc="left")
        tidy(ax)
        save(fig, "substack_contract_tables")
        plt.close(fig)
        return
    fig = plt.figure(figsize=(12, 6.6))
    gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 1, 0.95], hspace=0.45, wspace=0.55)
    x = np.arange(12)
    for j, n in enumerate(names):
        for i, var in enumerate(("Rn", "Nn")):
            ax = fig.add_subplot(gs[i, j])
            row = lambda src: t[(t.table == n) & (t.source == src) & (t["var"] == var)][MON3].values.ravel()  # noqa
            ax.bar(x, row("contract"), color=RED[3], width=0.7, label="Table in contract")
            ax.plot(x, row("CHIRPS 1991-2020"), "o-", color=BLUE[4], ms=3, lw=1.5, label="CHIRPS 1991-2020")
            ax.plot(x, row("CPC 1991-2020"), "s--", color=BLUE[2], ms=3, lw=1.2, label="CPC 1991-2020")
            ax.set_xticks(x, MONTHS, fontsize=7)
            if i == 0:
                ax.set_title(short[n].replace("\n", " "), fontsize=9)
            ax.set_ylabel("R_n, mean monthly rain (mm)" if var == "Rn" else "N_n, mean days >= 10 mm", fontsize=8)
            tidy(ax)
            if i == 0 and j == 0:
                handles, labels = ax.get_legend_handles_labels()
    ax = fig.add_subplot(gs[:, 3])
    ev = e["EOT per contract (algebraic)"].values
    lab = ["D, original\ntable", "D, addendum\ntable", "D, normals\nfrom data", "B, table", "B, normals\nfrom data"]
    vals = [ev[0], ev[2], ev[1], ev[4], ev[5]]
    cols = [RED[3], RED[5], BLUE[3], RED[4], BLUE[3]]
    ax.barh(range(len(vals)), vals, color=cols, height=0.6)
    for i, v in enumerate(vals):
        ax.text(v + 3, i, f"{v:.0f}", va="center", fontsize=8)
    ax.set_yticks(range(len(vals)), lab, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("EOT per 3-year contract (days)")
    ax.set_xlim(0, max(vals) * 1.25)
    ax.set_title("Clause 1229 EOT, 2001-2022 starts", fontsize=9)
    ax.grid(axis="y", visible=False)
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.42, 0.985), ncol=3, fontsize=8, frameon=False)
    fig.suptitle("Clause 1229 average tables in two signed contracts vs the site climate", x=0.06, y=1.02, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "fig10_contract_tables")
    plt.close(fig)


# ---------------------------------------------------------------- 11
def fig11():
    m = pd.read_csv(RES / "case_package5_monthly.csv", parse_dates=["month"])
    tot = pd.read_csv(RES / "case_package5.csv")
    tot = tot[tot.complete & (tot.point == "Masindi (station)")]
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw={"width_ratios": [1.5, 1], "wspace": 0.55})
    months = sorted(m.month.unique())
    x = np.arange(len(months))
    claimed = m[m["product"] == "CHIRPS"].set_index("month")["claimed V"].reindex(months).values
    w = 0.27
    ax[0].bar(x - w, claimed, w, color=RED[3], label="Contractor (station, positive months only)")
    for k, (prod, c) in enumerate([("CHIRPS", BLUE[4]), ("CPC", BLUE[2])]):
        v = m[m["product"] == prod].set_index("month").V.reindex(months).values
        ax[0].bar(x + k * w, v, w, color=c, label=f"{prod}, same 2005-2017 baseline")
    ax[0].axhline(0, color=INK2, lw=0.8)
    ax[0].set_xticks(x, [pd.Timestamp(t).strftime("%b\n%y") for t in months], fontsize=7)
    ax[0].set_ylabel("Clause 1229 monthly V (days)")
    ax[0].set_title("a  Which months were abnormal? Claim vs gridded data", fontsize=9)
    ax[0].legend(fontsize=7)
    tidy(ax[0])
    rows = []
    for _, r in tot.iterrows():
        for meth in ("EOT algebraic (spec)", "EOT positive months only"):
            rows.append({"label": f"{r['product']} {r.baseline.split(' ')[0]}, "
                                  f"{'claim' if 'claim' in r.window else 'contract'}",
                         "method": meth, "v": r[meth]})
    d = pd.DataFrame(rows)
    labels = list(dict.fromkeys(d.label))
    for i, lab in enumerate(labels):
        a = d[(d.label == lab) & (d.method == "EOT algebraic (spec)")].v.values[0]
        p = d[(d.label == lab) & (d.method == "EOT positive months only")].v.values[0]
        ax[1].plot([a, p], [i, i], color=GRID, lw=2, zorder=1)
        ax[1].scatter(a, i, color=CAT[3], s=30, zorder=2, label="Algebraic sum (as specified)" if i == 0 else None)
        ax[1].scatter(p, i, color=CAT[7], s=30, zorder=2, label="Positive months only" if i == 0 else None)
    ax[1].axvline(21, color=RED[4], ls="--", lw=1.2)
    ax[1].text(21.8, -0.45, "21 days claimed and granted", color=RED[4], fontsize=7.5, va="bottom")
    ax[1].set_yticks(range(len(labels)), labels, fontsize=7)
    ax[1].invert_yaxis()
    ax[1].set_xlabel("Total EOT (days)")
    ax[1].set_title("b  Same clause, same contract: total EOT by choice", fontsize=9)
    ax[1].legend(fontsize=7, loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=2, frameon=False)
    ax[1].set_ylim(len(labels) - 0.5, -1)
    ax[1].grid(axis="y", visible=False)
    fig.suptitle("Project A: Clause 1229 EOT claim recomputed with independent data", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "fig11_projectA")
    plt.close(fig)


# ---------------------------------------------------------------- 12
def fig12(substack=False):
    normal, q90 = 6.0, 10.0
    L = np.linspace(0, 16, 321)
    swa = 0.5 * np.clip(L - normal, 0, q90 - normal) + np.clip(L - q90, 0, None)
    nec = np.clip(L - q90, 0, None)
    c1229 = np.maximum((L - normal) * (1 + 20 / 20), -normal)      # assumes ~20 mm extra rain per extra rain day
    fig, ax = plt.subplots(figsize=(6.8, 4.4) if substack else (7.6, 4.8))
    ax.axvspan(0, normal, color=BLUE[0], alpha=0.5, lw=0)
    ax.axvspan(normal, q90, color=CAT[3], alpha=0.12, lw=0)
    ax.axvspan(q90, 16, color=RED[0], alpha=0.5, lw=0)
    ax.text(normal / 2, 9.3, "Contractor\ncarries\n(priced in)", ha="center", fontsize=8.5, color=INK2)
    ax.text((normal + q90) / 2, 9.3, "Shared\n50 : 50", ha="center", fontsize=8.5, color=INK2)
    ax.text((q90 + 16) / 2, 9.3, "Employer\ncarries", ha="center", fontsize=8.5, color=INK2)
    ax.plot(L, swa, color=CAT[2], lw=3, label="Shared Weather Allowance")
    if not substack:
        ax.plot(L, nec, color=CAT[1], lw=1.6, ls="--", label="NEC4 (once triggered)")
        ax.plot(L, np.maximum(c1229, 0), color=CAT[7], lw=1.4, ls=":",
                label="Clause 1229, positive month (illustrative)")
        ax.plot(L, c1229, color=CAT[3], lw=1.2, ls="-.", label="Clause 1229 monthly V, can be negative (illustrative)")
    ax.scatter([13], [5], color=INK, zorder=5)
    ax.annotate("Worked example: 13 lost days\n= 2 shared + 3 beyond = 5 days EOT", (13, 5), (12.2, 1.2),
                fontsize=8, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.set_xlim(0, 16)
    ax.set_ylim(-2.5 if not substack else -0.5, 11)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks([0, normal, q90, 16], ["0", "normal\n(30-yr mean)", "1-in-10-year\nmonth", "16"])
    ax.set_xlabel("Lost working days in the month (rain >= 10 mm), from the named dataset")
    ax.set_ylabel("Extension of time for the month (days)")
    ax.set_title("How the Shared Weather Allowance works (example: normal 6, 1-in-10 = 10)", loc="left", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False)
    tidy(ax)
    save(fig, "substack_swa_schematic" if substack else "fig12_swa_schematic")
    plt.close(fig)


# ---------------------------------------------------------------- 13
def fig13():
    p = pd.read_csv(RES / "rq5_clauses_present.csv", index_col=0)
    f = pd.read_csv(RES / "rq5_clauses_future.csv", index_col=[0, 1], header=[0, 1])
    nex = pd.read_csv(RES / "nex_uganda_summary.csv", index_col=0, header=[0, 1])
    d_lwd = nex.loc["d|ssp585|lwd", ("median", "All")]
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
    rules = MAIN_RULES
    emp = np.array([p.loc[r, "share_abnormal_relieved"] for r in rules])
    y = np.arange(len(rules))
    ax[0].barh(y, np.minimum(emp, 1) * 100, color=CAT[2], height=0.6, label="Employer (EOT)")
    ax[0].barh(y, np.maximum(1 - emp, 0) * 100, left=np.minimum(emp, 1) * 100, color=MUTED, height=0.6,
               label="Contractor")
    for i, v in enumerate(emp):
        if v > 1:
            ax[0].barh(i, (v - 1) * 100, left=100, color=RED[3], height=0.6,
                       label="EOT beyond the abnormal days" if v == emp.max() else None)
        ax[0].text(min(v, 1) * 100 / 2, i, f"{v:.0%}", ha="center", va="center", fontsize=8, color="white")
    ax[0].set_yticks(y, [RULE_LABEL[r] for r in rules], fontsize=8)
    ax[0].invert_yaxis()
    ax[0].set_xlabel("Share of above-normal lost days (%)")
    ax[0].set_title("a  Today: who carries above-normal rain lost days", fontsize=9)
    ax[0].legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
    ax[0].grid(axis="y", visible=False)
    w = 0.38
    for k, (b, lab) in enumerate([("d_stale_days", "Stale baseline"), ("d_updated_days", "Updated baseline")]):
        emp_d = np.array([f.loc[("ssp585", r), ("median", b)] for r in rules])
        con_d = np.maximum(d_lwd - emp_d, 0)
        ax[1].barh(y + (k - 0.5) * w, emp_d, w, color=CAT[2] if k == 0 else BLUE[2],
                   label=f"Employer, {lab.lower()}")
        ax[1].barh(y + (k - 0.5) * w, con_d, w, left=emp_d, color=MUTED, alpha=0.6 if k else 1,
                   label="Contractor" if k == 0 else None)
    ax[1].axvline(d_lwd, color=INK2, ls=":", lw=1)
    ax[1].text(d_lwd + 0.2, -0.55, f"+{d_lwd:.1f} extra lost days (all rules)", fontsize=7.5, color=INK2, va="center")
    ax[1].set_ylim(-0.9, len(rules) - 0.5)
    ax[1].set_yticks(y, [RULE_LABEL[r] for r in rules], fontsize=8)
    ax[1].invert_yaxis()
    ax[1].set_xlabel("Extra rain lost days per 3-year contract, 2041-2070 SSP5-8.5 (days)")
    ax[1].set_title("b  Climate change: who carries the extra days", fontsize=9)
    ax[1].legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
    ax[1].grid(axis="y", visible=False)
    fig.suptitle("Risk allocation of weather under each rule (Uganda, NEX ensemble median)", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "fig13_risk_split")
    plt.close(fig)


# ---------------------------------------------------------------- 14
def calendar_data():
    chirps = load_product("CHIRPS")
    rows = []
    for lat, lon, reg in cells(chirps):
        x = chirps.sel(lat=lat, lon=lon).to_series().loc["1991":"2020"]
        m = (x >= 10).groupby(x.index.month).sum() / 30
        rows.append(pd.DataFrame({"region": reg, "month": m.index, "rain": m.values}))
    rain = pd.concat(rows).groupby(["region", "month"]).rain.mean().unstack(0)
    d = xr.open_dataset(RAW / "power_daily.nc")[["T2M_MAX", "T2MDEW"]].load()
    e = 6.105 * np.exp(17.27 * d.T2MDEW / (237.7 + d.T2MDEW))
    w = (0.567 * d.T2M_MAX + 0.393 * e + 3.94).sel(time=slice("1991", "2020"))
    from regions import region_of
    rows = []
    for lat in w.lat.values:
        for lon in w.lon.values:
            s = w.sel(lat=lat, lon=lon).to_series()
            reg = region_of(lat, lon)
            if s.isna().all() or reg is None:
                continue
            hm = (s >= 30).groupby(s.index.month).sum() / 30
            rows.append(pd.DataFrame({"region": reg, "month": hm.index, "heat": hm.values}))
    heat = pd.concat(rows).groupby(["region", "month"]).heat.mean().unstack(0)
    return rain, heat


def fig14(rain, heat, substack=False):
    regs = ["Northern"] if substack else ["Northern", "Eastern", "Central", "Western"]
    fig, axes = plt.subplots(1, len(regs), figsize=(6.4, 3.8) if substack else (12, 3.6), sharey=True,
                             squeeze=False)
    x = np.arange(12)
    for ax, r in zip(axes[0], regs):
        ax.bar(x, rain[r].values, color=BLUE[3], width=0.75, label="Rain lost days (>= 10 mm)")
        ax.bar(x, heat[r].values, bottom=rain[r].values, color=RED[3], width=0.75,
               label="Heat-lost days (sWBGT >= 30 C)")
        ax.set_xticks(x, MONTHS)
        ax.set_title(r if not substack else "Northern Uganda: lost working days by month", fontsize=9)
        tidy(ax)
    axes[0][0].set_ylabel("Days per month, 1991-2020 mean")
    axes[0][0].legend(fontsize=7, loc="upper right" if substack else "upper center",
                      bbox_to_anchor=None if substack else (2.3, 1.22), ncol=1 if substack else 2, frameon=False)
    if not substack:
        fig.suptitle("Rain and heat lost working days through the year: heat peaks in the hot, humid months "
                     "before and at the start of the long rains", x=0.06, y=1.08, ha="left", fontweight="bold",
                     fontsize=10)
    save(fig, "substack_rain_heat" if substack else "fig14_rain_heat_calendar")
    plt.close(fig)


# ---------------------------------------------------------------- 15
def _contract_dist(args):
    from rq5_clauses import STARTS, per_contract, rule_months
    lat, lon, x = args
    c = per_contract(rule_months(x), STARTS)
    return c[MAIN_RULES]


def fig15():
    chirps = load_product("CHIRPS")
    jobs = [(lat, lon, chirps.sel(lat=lat, lon=lon).to_series().astype(float).loc[:"2020-12-31"])
            for lat, lon, _ in cells(chirps)]
    with Pool(8) as pool:
        c = pd.concat(pool.map(_contract_dist, jobs, chunksize=8))
    fig, ax = plt.subplots(figsize=(9, 4.2))
    data = [c[r].values for r in MAIN_RULES]
    bp = ax.boxplot(data, positions=range(len(data)), whis=(5, 95), showfliers=False, widths=0.5,
                    patch_artist=True, medianprops=dict(color=INK, lw=1.5))
    for box_, r in zip(bp["boxes"], MAIN_RULES):
        box_.set_facecolor(RULE_COLOR[r])
        box_.set_alpha(0.6)
        box_.set_edgecolor(INK2)
    for i, v in enumerate(data):
        ax.scatter(i, v.mean(), color="white", edgecolor=INK, s=22, zorder=3)
        ax.text(i + 0.3, np.percentile(v, 75), f"mean {v.mean():.0f}\nzero EOT {np.mean(v == 0):.0%}",
                fontsize=7, va="bottom")
    ax.set_xticks(range(len(data)), [RULE_LABEL[r] for r in MAIN_RULES], fontsize=8)
    ax.set_ylabel("EOT per 3-year contract (days)")
    ax.set_title("EOT for every 3-year contract (1991-2018 starts) in every cell; box = 25-75%, whiskers = 5-95%",
                 loc="left", fontsize=9.5)
    tidy(ax)
    save(fig, "fig15_eot_distribution")
    plt.close(fig)


# ---------------------------------------------------------------- 16
def fig16():
    f = pd.read_csv(RES / "rq5_clauses_future.csv", index_col=[0, 1], header=[0, 1])
    fig, ax = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    y = np.arange(len(MAIN_RULES))
    for a, scen in zip(ax, ("ssp245", "ssp585")):
        for i, r in enumerate(MAIN_RULES):
            h = f.loc[(scen, r), ("median", "hist_days")]
            st, up = f.loc[(scen, r), ("median", "stale_days")], f.loc[(scen, r), ("median", "updated_days")]
            lo = h + f.loc[(scen, r), ("p10", "d_stale_days")]
            hi = h + f.loc[(scen, r), ("p90", "d_stale_days")]
            a.plot([lo, hi], [i, i], color=RED[1], lw=6, alpha=0.6, solid_capstyle="butt",
                   label="Stale, 10-90% of models" if i == 0 else None)
            a.plot([h, st], [i, i], color=GRID, lw=2)
            a.scatter(h, i, color=INK, s=28, zorder=3, label="1985-2014" if i == 0 else None)
            a.scatter(up, i, color=BLUE[3], s=28, zorder=3, marker="s", label="2041-70, updated baseline" if i == 0 else None)
            a.scatter(st, i, color=RED[4], s=34, zorder=3, marker="D", label="2041-70, stale baseline" if i == 0 else None)
            dmed = f.loc[(scen, r), ("median", "d_stale_days")]
            a.text(max(hi, st) + 1, i, f"+{dmed / h:.0%}", va="center", fontsize=7.5, color=RED[5])
        a.set_title(scen.upper().replace("SSP", "SSP").replace("245", "2-4.5").replace("585", "5-8.5"), fontsize=9)
        a.set_xlabel("EOT per 3-year contract (days, NEX model space)")
        a.grid(axis="y", visible=False)
    ax[0].set_yticks(y, [RULE_LABEL[r] for r in MAIN_RULES], fontsize=8)
    ax[0].invert_yaxis()
    ax[0].legend(fontsize=7, loc="lower right")
    fig.suptitle("Climate stability of each rule: relief now and in 2041-2070 (10 models; % = median stale change)",
                 x=0.06, ha="left", fontweight="bold", fontsize=10)
    save(fig, "fig16_climate_stability")
    plt.close(fig)


# ---------------------------------------------------------------- 17
def fig17():
    w = pd.read_csv(PROC / "rq2_window_flags.csv")
    a = w[w.any_exceptional]
    c = a[a.contested]
    p, b, t = c.flip_product, c.flip_baseline, c.flip_trend
    cats = {"Dataset only": p & ~b & ~t, "Trend treatment only": t & ~p & ~b, "Baseline length only": b & ~p & ~t,
            "Two or more choices": (p.astype(int) + b.astype(int) + t.astype(int)) >= 2,
            "Combinations only\n(no single choice)": ~(p | b | t)}
    shares = {k: v.mean() * len(c) / len(a) for k, v in cats.items()}
    fig, ax = plt.subplots(figsize=(9, 2.4))
    left = 0
    cols = [CAT[0], CAT[3], CAT[4], CAT[6], MUTED]
    for (k, v), col in zip(shares.items(), cols):
        ax.barh(0, v * 100, left=left, color=col, height=0.5, label=f"{k}: {v:.0%}")
        if v > 0.04:
            ax.text(left + v * 50, 0, f"{v:.0%}", ha="center", va="center", color="white", fontsize=9)
        left += v * 100
    unc = 1 - len(c) / len(a)
    ax.barh(0, unc * 100, left=left, color=GRID, height=0.5, label=f"Not contested: {unc:.0%}")
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("Share of arguable claim seasons, Uganda 2001-2019 (%)")
    ax.set_title("What makes an arguable claim season contested (FIDIC Guide, 3-year contracts)", loc="left",
                 fontsize=9.5)
    ax.legend(fontsize=7.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.5), frameon=False)
    ax.grid(False)
    save(fig, "fig17_contested_sources")
    plt.close(fig)


# ---------------------------------------------------------------- S1
def figS1():
    a = xr.open_dataset(RAW / "arc2_uganda_daily.nc").precip.mean(["lat", "lon"]).to_series()
    c = load_product("CHIRPS").mean(["lat", "lon"]).to_series()
    r = (a.resample("MS").sum() / c.resample("MS").sum()).loc["1983":"2025"]
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2023-09-30"), color=RED[0], alpha=0.7, lw=0,
               label="Masked: Jan 2020 - Sep 2023")
    ax.plot(r.index, r.values, color=MUTED, lw=0.8)
    ax.plot(r.rolling(12, center=True).median(), color=INK, lw=1.8, label="12-month running median")
    ax.axhline(1, color=BLUE[3], lw=1, ls="--")
    ax.set_ylabel("ARC2 / CHIRPS\nnational monthly rainfall")
    ax.set_title("Homogeneity screen: a step change in ARC2 from 2020", loc="left", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper left")
    tidy(ax)
    save(fig, "figS1_arc2_break")
    plt.close(fig)


# ---------------------------------------------------------------- S2
def figS2():
    g = pd.read_csv(RES / "case_package5_gauge.csv")
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    for a, var, lab in [(ax[0], "Nw", "days >= 10 mm"), (ax[1], "Rw", "monthly rainfall (mm)")]:
        for prod, col, mk in [("CHIRPS", BLUE[4], "o"), ("CPC", BLUE[2], "s")]:
            a.scatter(g[var], g[f"{var}_{prod}"], color=col, marker=mk, s=40, label=prod)
        lim = max(g[var].max(), g[[f"{var}_CHIRPS", f"{var}_CPC"]].max().max()) * 1.1
        a.plot([0, lim], [0, lim], color=INK2, ls="--", lw=1, label="1:1")
        a.set_xlim(0, lim)
        a.set_ylim(0, lim)
        a.set_xlabel(f"Site record, {lab}")
        a.set_ylabel(f"Gridded, {lab}")
        a.legend(fontsize=7.5)
    fig.suptitle("Project A: site gauge vs gridded data for the six claimed months (2022-2023)", x=0.06, ha="left",
                 fontweight="bold", fontsize=10)
    save(fig, "figS2_gauge_vs_grid")
    plt.close(fig)


if __name__ == "__main__":
    fig10()
    fig10(substack=True)
    fig11()
    fig12()
    fig12(substack=True)
    fig13()
    rain, heat = calendar_data()
    fig14(rain, heat)
    fig14(rain, heat, substack=True)
    fig15()
    fig16()
    fig17()
    figS1()
    figS2()
