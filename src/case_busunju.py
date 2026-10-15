"""Case study: the contractor's weather delay periods on a 145 km road rehabilitation (Busunju-Kiboga-Hoima).

The Contractor's Monthly Report No. 23 (July 2025) gives "adverse weather conditions experienced in the months
September 2023 to December 2023 and August 2024 to December 2024 due to the rainy season" as a major reason
for delay. Programme accepted July 2023, so the pre-award baseline is 1981-2022. TfC assumed 3 years
(to confirm from the Contract Data). Each window is tested at four points along the corridor, on three products.
Output: results/case_busunju.csv, results/case_busunju_nec.csv
"""
import pandas as pd

import ei
from common import site_series, write_csv

POINTS = {"Busunju": (0.64, 32.17), "Kiboga south": (0.80, 31.95), "Kiboga": (0.92, 31.77), "Hoima": (1.43, 31.35)}
WINDOWS = {"Sep-Dec 2023": ("2023-09-01", "2023-12-31"), "Aug-Dec 2024": ("2024-08-01", "2024-12-31")}
TFC, BASELINE = 3.0, (1983, 2022)          # common start for all three products

rows, nec = [], []
for pname, (lat, lon) in POINTS.items():
    for prod in ("CHIRPS", "ARC2", "CPC"):
        x = site_series(lat, lon, prod)
        for wname, (s, e) in WINDOWS.items():
            r = ei.assess(x, s, e, TFC, baseline=BASELINE, indicators_=("lwd10", "lwd5", "total"))
            rows.append(r.assign(point=pname, product=prod, window=wname))
            if prod == "CHIRPS":
                nec.append(ei.nec_monthly(x, s, e, baseline=BASELINE).assign(point=pname, window=wname))
t = pd.concat(rows, ignore_index=True)
cols = ["window", "point", "product", "indicator", "value", "baseline_mean", "threshold_value_rp4tfc",
        "rp_empirical", "rp_gev", "ei", "verdict"]
write_csv(t[cols].round(2), "case_busunju")
write_csv(pd.concat(nec).round(1), "case_busunju_nec")
pd.set_option("display.width", 200)
print(t[t.indicator == "lwd10"][cols].round(2).to_string(index=False))
n = pd.concat(nec)
print("\nNEC months over 1-in-10 (CHIRPS):\n", n.groupby(["window", "point"]).exceeds_1in10.sum())
