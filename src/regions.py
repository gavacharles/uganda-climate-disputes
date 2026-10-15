"""National grid helpers: Uganda CHIRPS cells with their region, and regional summaries."""
from functools import lru_cache

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from common import RAW


@lru_cache(maxsize=None)
def regions():
    g = gpd.read_file(RAW / "uganda_adm1.geojson")
    return [(r.shapeName.replace(" Region", ""), r.geometry) for r in g.itertuples()]


def region_of(lat, lon):
    p = Point(float(lon), float(lat))
    for name, geom in regions():
        if geom.contains(p):
            return name
    return None


def cells(da):
    """(lat, lon, region) for every grid cell of `da` whose centre lies in Uganda."""
    out = []
    for lat in da.lat.values:
        for lon in da.lon.values:
            r = region_of(lat, lon)
            if r is not None:
                out.append((float(lat), float(lon), r))
    return out


def region_summary(df, cols, by=("region",)):
    """Mean of `cols` by region (and optional extra keys), plus a Uganda row."""
    by = list(by)
    reg = df.groupby(by)[cols].mean()
    nat = df[cols].mean().to_frame("Uganda").T
    nat.index.name = by[0]
    if len(by) > 1:
        nat = df.groupby(by[1:])[cols].mean().assign(**{by[0]: "Uganda"}).reset_index().set_index(by)
    return pd.concat([reg, nat])


EA = {"UGA": "Uganda", "KEN": "Kenya", "TZA": "Tanzania", "RWA": "Rwanda", "BDI": "Burundi"}
NE = __import__("pathlib").Path.home() / "uganda-concrete-climate" / "data" / "raw" / "naturalearth"


@lru_cache(maxsize=None)
def countries():
    g = gpd.read_file(NE / "ne_10m_admin_0_countries.geojson")
    g = g[g.ADM0_A3.isin(list(EA))]
    return [(EA[r.ADM0_A3], r.geometry) for r in g.itertuples()]


@lru_cache(maxsize=None)
def lakes():
    g = gpd.read_file(NE / "ne_10m_lakes.geojson")
    return g[g.geometry.intersects(gpd.GeoSeries.from_xy([28, 42], [-12, 6]).unary_union.envelope)].unary_union


def ea_cells(da, stride=1):
    """(lat, lon, country) for East African land cells (open water excluded), every `stride`-th cell."""
    out = []
    lk = lakes()
    for lat in da.lat.values[::stride]:
        for lon in da.lon.values[::stride]:
            p = Point(float(lon), float(lat))
            if lk.contains(p):
                continue
            for name, geom in countries():
                if geom.contains(p):
                    out.append((float(lat), float(lon), name))
                    break
    return out


@lru_cache(maxsize=None)
def uganda_shape():
    from shapely.ops import unary_union
    return unary_union([g for _, g in regions()])
