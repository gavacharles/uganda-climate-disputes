import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import ei  # noqa: E402


def synthetic(seed=0, years=(1981, 2020), trend=0.0):
    rng = np.random.default_rng(seed)
    idx = pd.date_range(f"{years[0]}-01-01", f"{years[1]}-12-31")
    yr = (idx.year - years[0]).values
    wet = rng.random(len(idx)) < 0.35
    rain = np.where(wet, rng.gamma(0.8, 12, len(idx)) * (1 + trend * yr), 0.0)
    return pd.Series(rain, idx)


def test_indicators_basic():
    out = ei.indicators([0, 12, 12, 6, 0, 0.5, 1, 1, 1])
    assert out["total"] == 33.5
    assert out["lwd10"] == 2 and out["lwd5"] == 3
    assert out["wet_days"] == 6 and out["max_wet_spell"] == 3
    assert out["rx1day"] == 12 and out["rx5day"] == 30.5


def test_indicators_missing_gives_nan():
    assert np.isnan(ei.indicators([1, np.nan, 3])["total"])


def test_shift_window_leap_day():
    s, e = ei.shift_window(pd.Timestamp("2020-02-29"), pd.Timestamp("2020-03-31"), 2019)
    assert s == pd.Timestamp("2019-02-28") and e == pd.Timestamp("2019-03-31")


def test_window_crossing_year_end():
    x = synthetic()
    base = ei.window_values(x, "2019-12-01", "2020-01-31", range(1981, 2019))
    assert len(base) == 38                     # 1981/82 .. 2018/19, all complete


def test_rp_empirical_bounds():
    s = np.arange(1, 40)
    assert ei.rp_empirical(s, 100) == 40       # beats the record -> n + 1
    assert ei.rp_empirical(s, 0) == 1.0


def test_extreme_window_flagged_and_normal_not():
    x = synthetic()
    x.loc["2020-03-01":"2020-05-31"] = 25.0    # every day a lost day
    hi = ei.assess(x, "2020-03-01", "2020-05-31", tfc_years=2).set_index("indicator")
    assert hi.loc["lwd10", "verdict"] == "exceptional"
    lo = ei.assess(synthetic(1), "2020-03-01", "2020-05-31", tfc_years=2).set_index("indicator")
    assert lo.loc["lwd10", "ei_empirical"] < 4


def test_nonstationary_detects_trend():
    vals = 50 + 2.0 * np.arange(40) + np.random.default_rng(3).gumbel(0, 5, 40)
    p = ei.fit_gev_ns(vals, np.arange(1981, 2021))
    assert p is not None and p["mu1"] > 1 and p["trend_p"] < 0.01
    # under a rising trend the same value is less rare at the end of the record
    assert ei.rp_gev_ns(p, 120, 2021) < ei.rp_gev(vals, 120)


def test_nec_monthly_shape():
    x = synthetic()
    out = ei.nec_monthly(x, "2020-03-01", "2020-05-31")
    assert list(out["month"]) == ["2020-03", "2020-04", "2020-05"]
    assert (out["rain_1in10"] > 0).all()


def test_missing_claim_window_is_not_exceptional():
    x = synthetic()
    x.loc["2020-03-01":"2020-05-31"] = np.nan
    r = ei.assess(x, "2020-03-01", "2020-05-31", tfc_years=2).set_index("indicator")
    assert r.loc["lwd10", "verdict"] == "n/a" and np.isnan(r.loc["lwd10", "rp_empirical"])


def test_return_level_dry_baseline_not_zero():
    dry = np.array([0] * 27 + [1, 1, 2], float)          # 30 dry seasons, mostly no lost days
    thr = ei.return_level(dry, 15)
    assert thr > 1                                        # 1 lost day is not a 1-in-15-year event here
    assert ei.rp_empirical(dry, thr) >= 15
