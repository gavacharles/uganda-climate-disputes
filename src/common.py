"""Shared paths, data loaders, sample sites and plotting style."""
from functools import lru_cache
from pathlib import Path

import matplotlib as mpl
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC = ROOT / "data" / "raw", ROOT / "data" / "processed"
FIG, RES = ROOT / "figures", ROOT / "results"
for d in (PROC, FIG, RES):
    d.mkdir(parents=True, exist_ok=True)

# Daily rainfall products (symlinked from ~/uganda-rainfall-climate/data/processed)
PRODUCTS = {
    "CHIRPS": RAW / "chirps_uganda_daily.nc",   # 0.25 deg, 1981-
    "ARC2": RAW / "arc2_uganda_daily.nc",       # 0.1 deg, 1983-2025
    "CPC": PROC / "cpc_ea_daily.nc",            # 0.5 deg gauge-only, 1981-2025, East Africa box
    "CHIRPS_EA": PROC / "chirps_ea_daily.nc",   # 0.25 deg, 1981-2025, East Africa box
}

# Periods screened out as inhomogeneous. ARC2 runs 1.3-3.2x CHIRPS nationally from Jan 2020 to Sep 2023
# (national annual totals ~2,200 mm vs ~1,300 mm in other years); see docs/wp1_notes.md.
QC_MASK = {"ARC2": [("2020-01-01", "2023-09-30")]}

# Illustrative project sites (approximate mid-points of real corridors; not claim data).
SITES = {  # name: (lat, lon, project type)
    "Kampala-Entebbe Expressway": (0.17, 32.53, "road"),
    "Masaka-Mbarara": (-0.45, 31.20, "road"),
    "Kabale-Kisoro": (-1.27, 29.85, "road"),
    "Hoima-Butiaba-Wanseko": (1.85, 31.30, "road"),
    "Gulu-Atiak": (3.00, 32.20, "road"),
    "Mbale-Lwakhakha": (0.95, 34.35, "road"),
    "Kapchorwa-Suam": (1.35, 34.55, "road"),
    "Moroto-Nakapiripirit": (2.30, 34.65, "road"),
}


@lru_cache(maxsize=None)
def load_product(name):
    """Daily precipitation DataArray (time, lat, lon) in mm/day, loaded into memory."""
    da = xr.open_dataset(PRODUCTS[name])["precip"].load()
    for a, b in QC_MASK.get(name, []):
        da.loc[dict(time=slice(a, b))] = float("nan")
    return da


def site_series(lat, lon, product="CHIRPS"):
    """Daily rainfall (mm) at the grid cell nearest to (lat, lon)."""
    da = load_product(product).sel(lat=lat, lon=lon, method="nearest")
    return da.to_series().astype(float)


# ---- style (validated reference palette, as in the rainfall project) ----
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
RED = ["#fbd5cf", "#f4aa9f", "#ec7f70", "#e34948", "#c13332", "#982524", "#6e1a1a"]

mpl.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "figure.dpi": 110,
    "savefig.dpi": 200, "savefig.bbox": "tight", "font.size": 9, "axes.titlesize": 10,
    "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2,
    "legend.frameon": False, "axes.prop_cycle": mpl.cycler(color=CAT),
})


def save(fig, name):
    fig.savefig(FIG / f"{name}.png")
    print("wrote", FIG / f"{name}.png")


def write_csv(df, name):
    path = RES / f"{name}.csv"
    df.to_csv(path, index=isinstance(df.index, pd.MultiIndex) or df.index.name is not None)
    print("wrote", path)
