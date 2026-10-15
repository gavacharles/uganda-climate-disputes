"""Download daily rainfall for the East Africa box (Uganda, Kenya, Tanzania, Rwanda, Burundi).

  chirps_ea_daily.nc   CHIRPS v2.0 daily 0.25 deg, 1981-2025 (IRI Data Library subset)
  cpc_ea_daily.nc      CPC Unified gauge-based daily 0.5 deg, 1981-2025 (NOAA PSL THREDDS subset)
  nex/<model>_<scen>.nc  NEX-GDDP-CMIP6 daily pr 0.25 deg (bias-corrected), historical 1985-2014 and
                       SSP2-4.5 / SSP5-8.5 2041-2070 (NASA NCCS THREDDS subset), mm/day
Usage: python fetch_ea.py [chirps|cpc|nex|all]
"""
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import requests
import xarray as xr

from common import PROC, RAW

BOX = dict(south=-12, north=6, west=28, east=42)
DL = RAW / "ea"
NEX_DIR = PROC / "nex"
for d in (DL, NEX_DIR):
    d.mkdir(parents=True, exist_ok=True)

NEX = "https://ds.nccs.nasa.gov/thredds"
MODELS = {"ACCESS-CM2": "r1i1p1f1", "CanESM5": "r1i1p1f1", "EC-Earth3": "r1i1p1f1", "GFDL-ESM4": "r1i1p1f1",
          "INM-CM5-0": "r1i1p1f1", "IPSL-CM6A-LR": "r1i1p1f1", "MIROC6": "r1i1p1f1", "MPI-ESM1-2-HR": "r1i1p1f1",
          "MRI-ESM2-0": "r1i1p1f1", "NorESM2-MM": "r1i1p1f1"}
PERIODS = {"historical": range(1985, 2015), "ssp245": range(2041, 2071), "ssp585": range(2041, 2071)}


def get(url, out, tries=4, timeout=300):
    for k in range(tries):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200 and len(r.content) > 1000:
                out.write_bytes(r.content)
                return True
            print("bad", r.status_code, url[:120], flush=True)
        except requests.RequestException as e:
            print("err", e.__class__.__name__, url[:120], flush=True)
        time.sleep(5 * (k + 1))
    return False


# ---------------------------------------------------------------- CHIRPS via IRI
def chirps_year(y):
    out = DL / f"chirps_{y}.nc"
    if out.exists():
        return
    url = ("https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.daily-improved/.global/.0p25/.prcp/"
           f"T/(1%20Jan%20{y})/(31%20Dec%20{y})/RANGEEDGES/X/{BOX['west']}/{BOX['east']}/RANGEEDGES/"
           f"Y/{BOX['south']}/{BOX['north']}/RANGEEDGES/data.nc")
    if get(url, out):
        print("chirps", y, flush=True)


def chirps():
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(chirps_year, range(1981, 2026)))
    parts = []
    for y in range(1981, 2026):
        ds = xr.open_dataset(DL / f"chirps_{y}.nc", decode_times=False)
        da = ds.prcp.rename(T="time", X="lon", Y="lat")
        da["time"] = pd.date_range(f"{y}-01-01", periods=da.sizes["time"], freq="D")
        parts.append(da.load())
    da = xr.concat(parts, "time").rename("precip").astype("float32").sortby("lat")
    da = da.where(da >= 0)
    da.to_dataset().to_netcdf(PROC / "chirps_ea_daily.nc")
    print("wrote chirps_ea_daily.nc", da.shape, flush=True)


# ---------------------------------------------------------------- CPC via PSL
def cpc_year(y):
    out = DL / f"cpc_{y}.nc"
    if out.exists():
        return
    url = (f"https://psl.noaa.gov/thredds/ncss/grid/Datasets/cpc_global_precip/precip.{y}.nc?var=precip"
           f"&north={BOX['north']}&west={BOX['west']}&east={BOX['east']}&south={BOX['south']}"
           f"&time_start={y}-01-01T00:00:00Z&time_end={y}-12-31T23:59:59Z&accept=netcdf4")
    if get(url, out):
        print("cpc", y, flush=True)


def cpc():
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(cpc_year, range(1981, 2026)))
    da = xr.concat([xr.open_dataset(DL / f"cpc_{y}.nc").precip.load() for y in range(1981, 2026)], "time")
    da = da.sortby("lat").astype("float32")
    da.to_dataset().to_netcdf(PROC / "cpc_ea_daily.nc")
    print("wrote cpc_ea_daily.nc", da.shape, flush=True)


# ---------------------------------------------------------------- NEX-GDDP-CMIP6 via NCCS
def nex_files(model, scen, variant):
    url = f"{NEX}/catalog/AMES/NEX/GDDP-CMIP6/{model}/{scen}/{variant}/pr/catalog.html"
    html = requests.get(url, timeout=120).text
    names = sorted(set(re.findall(rf"pr_day_{re.escape(model)}_{scen}_{variant}_\w+?_(\d{{4}})(_v\d\.\d)?\.nc", html)))
    best = {}
    for y, v in names:                       # keep the latest version for each year
        best[int(y)] = max(best.get(int(y), ""), v)
    grid = re.search(rf"pr_day_{re.escape(model)}_{scen}_{variant}_(\w+?)_\d{{4}}", html)
    return best, (grid.group(1) if grid else "gn")


def nex_one(args):
    model, scen, variant, grid, y, v = args
    out = DL / f"nex_{model}_{scen}_{y}.nc"
    if out.exists():
        return True
    fn = f"pr_day_{model}_{scen}_{variant}_{grid}_{y}{v}.nc"
    url = (f"{NEX}/ncss/grid/AMES/NEX/GDDP-CMIP6/{model}/{scen}/{variant}/pr/{fn}?var=pr"
           f"&north={BOX['north']}&west={BOX['west']}&east={BOX['east']}&south={BOX['south']}"
           "&horizStride=1&temporal=all&accept=netcdf4")
    return get(url, out)


def nex():
    jobs = []
    for model, variant in MODELS.items():
        for scen, years in PERIODS.items():
            try:
                best, grid = nex_files(model, scen, variant)
            except requests.RequestException as e:
                print("catalog failed", model, scen, e, flush=True)
                continue
            missing = [y for y in years if y not in best]
            if missing:
                print("missing years", model, scen, missing[:5], flush=True)
            jobs += [(model, scen, variant, grid, y, best[y]) for y in years if y in best]
    print("nex files to fetch:", len(jobs), flush=True)
    with ThreadPoolExecutor(6) as ex:
        ok = list(ex.map(nex_one, jobs))
    print("nex fetched", sum(ok), "of", len(jobs), flush=True)
    for model in MODELS:
        for scen, years in PERIODS.items():
            out = NEX_DIR / f"{model}_{scen}.nc"
            files = [DL / f"nex_{model}_{scen}_{y}.nc" for y in years]
            if out.exists() or not all(f.exists() for f in files):
                continue
            da = xr.concat([xr.open_dataset(f).pr.load() for f in files], "time")
            da = (da * 86400).astype("float32")          # kg m-2 s-1 -> mm/day
            if float(da.lon.max()) > 180:
                da = da.assign_coords(lon=((da.lon + 180) % 360) - 180)
            da = da.sortby("lat").rename("precip")
            da["time"] = pd.to_datetime([f"{t.year:04d}-{t.month:02d}-{t.day:02d}" for t in da.indexes["time"]],
                                        errors="coerce") if not np.issubdtype(da.time.dtype, np.datetime64) else da.time
            da = da.sel(time=da.time.notnull())
            da.to_dataset().to_netcdf(out)
            print("wrote", out.name, da.shape, flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("cpc", "all"):
        cpc()
    if what in ("chirps", "all"):
        chirps()
    if what in ("nex", "all"):
        nex()
