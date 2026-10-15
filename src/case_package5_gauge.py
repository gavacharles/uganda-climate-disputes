"""Validate gridded lost-working-day counts against Project A's site/station rainfall used in its EOT-7 claim.

The EOT-7 report gives, for each claimed month, the recorded Nw (days >= 10 mm), Rw (monthly mm), and the
Nn, Rn averages with the resulting V. Here those are compared with CHIRPS and CPC at the project cell.
Input: text extracted from the report (path in argv[1]). Output: results/case_package5_gauge.csv
"""
import re
import sys

import pandas as pd

from case_package5 import POINTS
from common import site_series, write_csv

txt = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
blocks = re.split(r"COMPUTATION FOR EXTENSION OF TIME FOR THE MONTH OF", txt)[1:]
rows = []
for b in blocks:
    m = re.match(r"\s*([A-Za-z]+)[ .\-]*(\d{4})", b)
    vals = {}
    for k in ("Nn", "Rn", "Rw", "Nw"):
        g = re.search(rf"\n\s*{k}\s+(-?[\d.]+)", b)
        vals[k] = float(g.group(1)) if g else None
    v = re.search(r"V=Extension of time \(Days\)\s+(-?[\d.]+)", b)
    if m:
        rows.append({"month": pd.Timestamp(f"1 {m.group(1)[:3]} {m.group(2)}"), **vals,
                     "V_claimed": float(v.group(1)) if v else None})
claims = pd.DataFrame(rows).drop_duplicates("month").set_index("month").sort_index()

lat, lon = POINTS["Masindi (station)"]
for prod in ("CHIRPS", "CPC"):
    x = site_series(lat, lon, prod)
    mm = x.resample("MS").sum(min_count=28)
    n10 = (x >= 10).astype(float).where(x.notna()).resample("MS").sum(min_count=28)
    claims[f"Rw_{prod}"] = mm.reindex(claims.index).round(1)
    claims[f"Nw_{prod}"] = n10.reindex(claims.index)
write_csv(claims, "case_package5_gauge")
pd.set_option("display.width", 200)
print(claims.to_string())
ok = claims.dropna(subset=["Nw", "Nw_CHIRPS"])
for prod in ("CHIRPS", "CPC"):
    o = ok.dropna(subset=[f"Nw_{prod}"])
    if len(o) > 2:
        print(f"{prod}: n={len(o)}  corr(Nw)={o.Nw.corr(o[f'Nw_{prod}']):.2f}  corr(Rw)={o.Rw.corr(o[f'Rw_{prod}']):.2f}  "
              f"mean Nw site {o.Nw.mean():.1f} vs {o[f'Nw_{prod}'].mean():.1f}; mean Rw site {o.Rw.mean():.0f} vs {o[f'Rw_{prod}'].mean():.0f}")
