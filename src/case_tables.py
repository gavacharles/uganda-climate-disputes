"""Clause 1229 average tables in signed contracts vs the rainfall record (1991-2020 normals).

Table 1229/1 as printed in the Special Specifications / addenda of two MoWT road contracts, compared with Nn
(mean days >= 10 mm) and Rn (mean monthly rainfall, mm) from CHIRPS and CPC at the project location.
Output: results/case_tables.csv
"""
import pandas as pd

from common import site_series, write_csv

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TABLES = {
    "Project D (Kapchorwa-Suam), original table 'Kihihi'": {
        "loc": (1.40, 34.45),
        "Nn": [1, 1, 4, 3, 2, 1, 0, 3, 3, 4, 4, 2],
        "Rn": [50, 52, 109, 97, 86, 24, 22, 73, 120, 144, 119, 58]},
    "Project D (Kapchorwa-Suam), addendum table 'Kapchorwa'": {
        "loc": (1.40, 34.45),
        "Nn": [3, 6, 8, 9, 10, 10, 10, 10, 10, 10, 10, 6],
        "Rn": [164.5, 259, 583, 666.9, 1026.6, 444.8, 532.3, 628.77, 733.9, 511.9, 220.2, 215.8]},
    "Project B (Busunju-Kiboga-Hoima), table 'Hoima station'": {
        "loc": (1.43, 31.35),
        "Nn": [26, 23, 21, 18, 21, 22, 23, 21, 18, 17, 18, 23],
        "Rn": [7, 7, 11, 13, 11, 9, 9, 11, 13, 15, 13, 9]},
}


def normals(lat, lon, prod):
    x = site_series(lat, lon, prod).loc["1991":"2020"]
    m = pd.DataFrame({"Rn": x.resample("MS").sum(min_count=28),
                      "Nn": (x >= 10).astype(float).where(x.notna()).resample("MS").sum(min_count=28)})
    return m.groupby(m.index.month).mean()


rows = []
for name, t in TABLES.items():
    rows.append({"table": name, "source": "contract", "var": "Nn", **dict(zip(MONTHS, t["Nn"])), "annual": sum(t["Nn"])})
    rows.append({"table": name, "source": "contract", "var": "Rn", **dict(zip(MONTHS, t["Rn"])), "annual": sum(t["Rn"])})
    for prod in ("CHIRPS", "CPC"):
        n = normals(*t["loc"], prod)
        for v in ("Nn", "Rn"):
            vals = list(n[v].round(1))
            rows.append({"table": name, "source": f"{prod} 1991-2020", "var": v, **dict(zip(MONTHS, vals)),
                         "annual": round(sum(vals), 1)})
out = pd.DataFrame(rows)
write_csv(out, "case_tables")
pd.set_option("display.width", 250)
print(out.to_string(index=False))


# ---- EOT per 3-year contract under each table (Clause 1229 as amended in these contracts: algebraic sum, a
# negative grand total does not reduce time, monthly V capped at Nc - Nn and floored at -Nn); Nw, Rw from CHIRPS
def eot_contracts(x, nn, rn, starts):
    m = pd.DataFrame({"R": x.resample("MS").sum(min_count=28),
                      "N": (x >= 10).astype(float).where(x.notna()).resample("MS").sum(min_count=28)}).dropna()
    mon = m.index.month - 1
    nn_m = pd.Series(nn).iloc[mon].values
    rn_m = pd.Series(rn).iloc[mon].values
    days = m.index.days_in_month.values
    v = (m.N.values - nn_m) + (m.R.values - rn_m) / 20
    v = pd.Series(pd.Series(v).clip(lower=-nn_m, upper=days - nn_m).values, index=m.index)
    tot = [max(v.loc[s: s + pd.DateOffset(months=35)].sum(), 0) for s in starts]
    pos = [v.loc[s: s + pd.DateOffset(months=35)].clip(lower=0).sum() for s in starts]
    return sum(tot) / len(tot), sum(t > 0 for t in tot) / len(tot), sum(pos) / len(pos)


starts = pd.date_range("2001-01-01", "2022-12-01", freq="MS")
erows = []
for name, t in TABLES.items():
    x = site_series(*t["loc"], "CHIRPS").loc[:"2025-12-31"]
    own = normals(*t["loc"], "CHIRPS")
    for label, nn, rn in [("table in contract", t["Nn"], t["Rn"]),
                          ("CHIRPS 1991-2020 normals", list(own.Nn), list(own.Rn))]:
        mean, p, pos = eot_contracts(x, nn, rn, starts)
        erows.append({"table": name, "averages used": label, "EOT per contract (algebraic)": round(mean, 1),
                      "share of contracts with EOT": round(p, 2), "EOT positive months only": round(pos, 1)})
e = pd.DataFrame(erows)
write_csv(e, "case_tables_eot")
print(e.to_string(index=False))
