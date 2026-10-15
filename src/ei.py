"""Exceptionality Index (EI) for "exceptionally adverse climatic conditions" (FIDIC 2017 Sub-Clause 8.5(c)).

Method (concept note, WP1):
1. Compute weather indicators for the claim window at the site (e.g. lost working days, LWD).
2. Compute the same indicators for the same calendar window in every baseline year (years before award).
3. Convert the claim-window value to a return period (RP, years): empirical, stationary GEV and
   non-stationary GEV (location trending with year, evaluated at the claim year).
4. EI = RP / Time for Completion (years). FIDIC Contracts Guide (2000) rule of thumb: exceptional if EI >= 4-5.
5. NEC-style check: each calendar month against its baseline 1-in-10-year value (NEC4 cl. 60.1(13)).
"""
import warnings

import numpy as np
import pandas as pd
from scipy import optimize, stats

LWD_RULES = {"lwd10": 10.0, "lwd5": 5.0}   # earthworks (>= 10 mm/day), surfacing (>= 5 mm/day)
INDICATORS = ["total", "wet_days", "lwd10", "lwd5", "max_wet_spell", "rx1day", "rx5day"]
EI_RULE = (4.0, 5.0)                      # FIDIC Guide: RP of 4-5 x Time for Completion
MAX_MISSING = 0.05                        # windows with more missing days than this are not assessed


def _longest_run(mask):
    best = cur = 0
    for m in mask:
        cur = cur + 1 if m else 0
        best = max(best, cur)
    return best


def indicators(x):
    """Indicators for one window of daily rainfall (mm). Returns NaNs if the window has missing days."""
    x = np.asarray(x, float)
    miss = np.isnan(x)
    if len(x) == 0 or miss.mean() > MAX_MISSING:
        return {k: np.nan for k in INDICATORS}
    scale = len(x) / (~miss).sum()          # scale sums and counts to the full window when a few days are missing
    xf = np.where(miss, 0.0, x)
    rx5 = np.convolve(xf, np.ones(5), "valid").max() if len(x) >= 5 else xf.sum()
    out = {"total": xf.sum() * scale, "wet_days": round((xf >= 1).sum() * scale),
           "max_wet_spell": _longest_run(xf >= 1), "rx1day": xf.max(), "rx5day": rx5}
    out.update({k: round((xf >= thr).sum() * scale) for k, thr in LWD_RULES.items()})
    return {k: out[k] for k in INDICATORS}


def shift_window(start, end, year):
    """The [start, end] window moved to begin in `year` (same calendar days; 29 Feb -> 28 Feb)."""
    off = pd.DateOffset(years=year - start.year)
    return start + off, end + off


def window_values(series, start, end, years):
    """DataFrame (index year) of indicators for the same calendar window in each of `years`."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    rows = {}
    for y in years:
        s, e = shift_window(start, end, y)
        w = series.loc[s:e]
        if len(w) < (e - s).days + 1:      # incomplete coverage at the record edges
            continue
        rows[y] = indicators(w.values)
    return pd.DataFrame.from_dict(rows, orient="index").rename_axis("year").dropna()


# ---------------------------------------------------------------- return periods

def rp_empirical(sample, x):
    """Rank the event among the baseline + itself (Weibull): RP = (n+1)/(m+1), m = baseline values >= x.
    Bounded at n+1 when the event beats the whole record."""
    sample = np.asarray(sample, float)
    if not np.isfinite(x) or len(sample) == 0:
        return np.nan
    m = int((sample >= x).sum())
    return (len(sample) + 1) / (m + 1)


def _usable(sample):
    return len(sample) >= 15 and len(np.unique(sample)) >= 6 and np.std(sample) > 0


def rp_gev(sample, x, max_rp=1000.0):
    """Stationary GEV return period of exceeding x (scipy shape c = -xi)."""
    sample = np.asarray(sample, float)
    if not np.isfinite(x) or not _usable(sample):
        return np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c, loc, scale = stats.genextreme.fit(sample)
    p = stats.genextreme.sf(x, c, loc, scale)
    return float(np.clip(1 / max(p, 1e-12), 1, max_rp))


def fit_gev_ns(sample, years):
    """Non-stationary GEV, location = mu0 + mu1 * (year - mean year). Returns params dict or None."""
    sample, years = np.asarray(sample, float), np.asarray(years, float)
    if not _usable(sample):
        return None
    t0 = years.mean()
    t = years - t0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c0, loc0, sc0 = stats.genextreme.fit(sample)

        def nll(p):
            c, mu0, mu1, lsc = p
            ll = stats.genextreme.logpdf(sample, c, mu0 + mu1 * t, np.exp(lsc))
            return 1e10 if not np.all(np.isfinite(ll)) else -ll.sum()

        res = optimize.minimize(nll, [c0, loc0, 0.0, np.log(sc0)], method="Nelder-Mead",
                                options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-6})
        nll_stat = nll([c0, loc0, 0.0, np.log(sc0)])
    if not res.success and res.fun > nll_stat:
        return None
    c, mu0, mu1, lsc = res.x
    # likelihood-ratio test of the trend term (1 df)
    lr = 2 * max(nll_stat - res.fun, 0.0)
    return {"c": c, "mu0": mu0, "mu1": mu1, "scale": np.exp(lsc), "t0": t0,
            "trend_p": float(stats.chi2.sf(lr, 1))}


def rp_gev_ns(params, x, year, max_rp=1000.0):
    """Return period of exceeding x in `year` under a fitted non-stationary GEV."""
    if params is None or not np.isfinite(x):
        return np.nan
    loc = params["mu0"] + params["mu1"] * (year - params["t0"])
    p = stats.genextreme.sf(x, params["c"], loc, params["scale"])
    return float(np.clip(1 / max(p, 1e-12), 1, max_rp))


# ---------------------------------------------------------------- the claim test

def verdict(ei):
    if not np.isfinite(ei):
        return "n/a"
    lo, hi = EI_RULE
    return "exceptional" if ei >= hi else ("borderline" if ei >= lo else "not exceptional")


def assess(series, start, end, tfc_years, baseline=None, indicators_=("lwd10", "lwd5", "total")):
    """Assess one claim window at one site.

    series     daily rainfall at the site (pd.Series indexed by date)
    start, end claim window (inclusive)
    tfc_years  Time for Completion in years
    baseline   (first, last) baseline years; default = record start .. year before the window starts
    Returns a DataFrame, one row per indicator.
    """
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    b0 = series.index.min().year if baseline is None else baseline[0]
    b1 = start.year - 1 if baseline is None else baseline[1]
    obs = indicators(series.loc[start:end].values)
    base = window_values(series, start, end, range(b0, b1 + 1))
    rows = []
    for ind in indicators_:
        x, s = obs[ind], base[ind].values
        ns = fit_gev_ns(s, base.index.values)
        r = {"indicator": ind, "value": x, "baseline_n": len(s), "baseline_mean": s.mean(),
             "excess_over_mean": x - s.mean(), "rp_empirical": rp_empirical(s, x), "rp_gev": rp_gev(s, x),
             "rp_gev_ns": rp_gev_ns(ns, x, start.year),
             "trend_per_decade": np.nan if ns is None else 10 * ns["mu1"],
             "trend_p": np.nan if ns is None else ns["trend_p"]}
        # value needed to count as exceptional (RP = 4 x TfC) under the stationary GEV
        r["threshold_value_rp4tfc"] = return_level(s, EI_RULE[0] * tfc_years)
        for k in ("rp_empirical", "rp_gev", "rp_gev_ns"):
            r["ei" + k[2:]] = r[k] / tfc_years
        use_gev = np.isfinite(r["ei_gev"])
        r["ei"] = r["ei_gev"] if use_gev else r["ei_empirical"]          # headline EI
        r["ei_method"] = "gev" if use_gev else "empirical"
        r["verdict"] = verdict(r["ei"])
        rows.append(r)
    return pd.DataFrame(rows)


def return_level(sample, rp):
    """Stationary GEV value with return period `rp` years (empirical quantile if GEV unusable)."""
    sample = np.asarray(sample, float)
    if len(sample) == 0:
        return np.nan
    if not _usable(sample):
        # smallest positive value c with empirical exceedance (m(c)+1)/(n+1) <= 1/rp, so a dry-season baseline of
        # mostly zeros does not give a threshold of 0 (which would make every season "exceptional")
        n = len(sample)
        for c in np.unique(np.concatenate([sample[sample > 0], [sample.max() + 1, 1.0]])):
            if c > 0 and ((sample >= c).sum() + 1) / (n + 1) <= 1 / rp:
                return float(c)
        return float(sample.max() + 1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        c, loc, scale = stats.genextreme.fit(sample)
    return float(stats.genextreme.isf(1 / rp, c, loc, scale))


def nec_monthly(series, start, end, baseline=None):
    """NEC-style test: for each calendar month in the window, compare monthly rainfall and days >= 5 mm
    with the 1-in-10-year values (empirical 90th percentile) of that month in the baseline years.
    NEC compensates only the excess over the 1-in-10-year weather, so the excess is reported too."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    b0 = series.index.min().year if baseline is None else baseline[0]
    b1 = start.year - 1 if baseline is None else baseline[1]
    monthly = pd.DataFrame({"rain": series.resample("MS").sum(min_count=28),
                            "days5": (series >= 5).astype(float).where(series.notna()).resample("MS").sum(min_count=28)})
    rows = []
    for m in pd.date_range(start.to_period("M").to_timestamp(), end, freq="MS"):
        base = monthly[(monthly.index.month == m.month) & (monthly.index.year.isin(range(b0, b1 + 1)))].dropna()
        r = {"month": m.strftime("%Y-%m")}
        for v in ("rain", "days5"):
            q10 = float(np.quantile(base[v], 0.9))
            r[v] = monthly.loc[m, v]
            r[v + "_1in10"] = q10
            r[v + "_excess"] = max(r[v] - q10, 0.0)
        r["exceeds_1in10"] = bool(r["rain_excess"] > 0 or r["days5_excess"] > 0)
        rows.append(r)
    return pd.DataFrame(rows)
