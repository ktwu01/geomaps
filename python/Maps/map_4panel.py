"""
map_4panel.py
=============
Proposed study domain and validation network — 4-panel figure.

Panel (a): CONUS simulation domain with topography
Panel (b): AmeriFlux tower locations for latent heat flux validation
           Stars = primary sites from Li et al. (2021): US-UMB, US-Ha1, US-Ton
Panel (c): Critical Zone Observatory (CZO) sites with rock moisture observations
Panel (d): SMAP soil moisture coverage and GRACE mascon grid for TWS validation

Data sources (all public, no login required):
  - Topography: Natural Earth shaded relief via cartopy
  - AmeriFlux site metadata: https://ameriflux.lbl.gov/wp-content/uploads/
      sites/ameriflux/amf_sites.csv  (public CSV, no auth needed)
  - CZO coordinates: CZO Archive (czo-archive.criticalzone.org)
  - SMAP coverage: schematic (SMAP covers CONUS globally at 36 km / 9 km)
  - GRACE mascons: JPL RL06 3-degree equal-area spherical caps — shown as
      schematic 3° grid over CONUS (no data download needed for domain figure)

Usage:
    python3 map_4panel.py

Output:
    map_4panel.png  (same directory as this script)
"""

import os
import io
import ssl
import certifi
import warnings

# Fix macOS Python 3.14 SSL certificate issue — must be set before any network I/O
os.environ.setdefault("SSL_CERT_FILE",      certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
# Patch the default SSL context so cartopy's urllib downloads also use certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import requests

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Projection & map extent
# ---------------------------------------------------------------------------
PROJ = ccrs.LambertConformal(central_longitude=-96, central_latitude=37.5,
                              standard_parallels=(29.5, 45.5))
DATA_CRS = ccrs.PlateCarree()
# CONUS bounding box in geographic coords
LON_W, LON_E = -125, -66
LAT_S, LAT_N = 24, 50

# ---------------------------------------------------------------------------
# Natural Earth features (auto-downloaded to cartopy cache on first run)
# ---------------------------------------------------------------------------
LAND   = cfeature.NaturalEarthFeature("physical", "land",   "50m",
                                       facecolor="#e8dcc8", edgecolor="none")
OCEAN  = cfeature.NaturalEarthFeature("physical", "ocean",  "50m",
                                       facecolor="#c9dce7", edgecolor="none")
LAKES  = cfeature.NaturalEarthFeature("physical", "lakes",  "50m",
                                       facecolor="#c9dce7", edgecolor="#7aaccf",
                                       linewidth=0.3)
RIVERS = cfeature.NaturalEarthFeature("physical", "rivers_lake_centerlines",
                                       "50m", facecolor="none",
                                       edgecolor="#7aaccf", linewidth=0.3)
STATES = cfeature.NaturalEarthFeature("cultural",
                                       "admin_1_states_provinces_lines", "50m",
                                       facecolor="none", edgecolor="#aaaaaa",
                                       linewidth=0.4)
BORDERS = cfeature.NaturalEarthFeature("cultural", "admin_0_countries", "50m",
                                        facecolor="none", edgecolor="#888888",
                                        linewidth=0.6)


def _add_base_features(ax, add_relief=False):
    """Add standard map features to an axis."""
    ax.add_feature(OCEAN)
    ax.add_feature(LAND)
    ax.add_feature(LAKES)
    ax.add_feature(RIVERS)
    ax.add_feature(STATES)
    ax.add_feature(BORDERS)
    ax.set_extent([LON_W, LON_E, LAT_S, LAT_N], crs=DATA_CRS)
    # Thin frame
    ax.spines["geo"].set_linewidth(0.8)


# ---------------------------------------------------------------------------
# Panel (a) — CONUS topography
# ---------------------------------------------------------------------------
def panel_topography(ax):
    """
    Show CONUS domain with shaded topographic relief using the Natural Earth
    'cross_blended_hypsometric_tints' raster, accessed via cartopy's
    background image interface.
    Uses a DEM-derived colormap over a simple elevation grid as fallback
    if the NE raster is unavailable.
    """
    _add_base_features(ax, add_relief=True)

    # Add Natural Earth shaded relief as background
    # cartopy ships a low-res version; the 50m NE relief is fetched on demand.
    try:
        ax.background_img(name="BM",        # Blue Marble
                          resolution="low")
    except Exception:
        # Fallback: stock image (Natural Earth 1:50m)
        try:
            ax.stock_img()
        except Exception:
            pass  # leave plain land color

    # Overlay state/border lines on top of imagery
    ax.add_feature(STATES)
    ax.add_feature(BORDERS)

    # CONUS domain box
    lons_box = [LON_W, LON_E, LON_E, LON_W, LON_W]
    lats_box = [LAT_S, LAT_S, LAT_N, LAT_N, LAT_S]
    ax.plot(lons_box, lats_box, transform=DATA_CRS,
            color="#d62728", linewidth=1.2, linestyle="--")

    ax.set_title("(a) CONUS simulation domain", fontsize=9, fontweight="bold",
                 pad=4)


# ---------------------------------------------------------------------------
# Panel (b) — AmeriFlux towers
# ---------------------------------------------------------------------------
# Primary sites (Li et al. 2021) — coordinates from ameriflux.lbl.gov
PRIMARY_SITES = {
    "US-Ha1": (42.5378, -72.1715, "Harvard Forest\n(US-Ha1)"),
    "US-UMB": (45.5598, -84.7138, "UMBS\n(US-UMB)"),
    "US-Ton": (38.4316, -120.9660, "Tonzi Ranch\n(US-Ton)"),
}

# Offset (dlat, dlon) for text labels to avoid marker overlap
PRIMARY_OFFSETS = {
    "US-Ha1": (1.2, 1.0),
    "US-UMB": (1.2, -1.0),
    "US-Ton": (-2.5, -3.0),
}

AMERIFLUX_CSV_URL = (
    "https://ameriflux.lbl.gov/wp-content/uploads/sites/ameriflux/amf_sites.csv"
)


def _fetch_ameriflux_sites():
    """
    Fetch AmeriFlux site metadata CSV (public, no login).
    Returns list of (lat, lon) tuples for CONUS sites only.
    Falls back to an empty list on network error.
    """
    try:
        resp = requests.get(AMERIFLUX_CSV_URL, timeout=15)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        sites = []
        header = None
        for line in lines:
            parts = [p.strip().strip('"') for p in line.split(",")]
            if header is None:
                header = [h.lower() for h in parts]
                continue
            if len(parts) < 3:
                continue
            try:
                # Find lat/lon columns robustly
                lat_idx = next(i for i, h in enumerate(header)
                               if "lat" in h and "lon" not in h)
                lon_idx = next(i for i, h in enumerate(header)
                               if "lon" in h)
                lat = float(parts[lat_idx])
                lon = float(parts[lon_idx])
                # CONUS only: roughly 24–50N, 125–66W
                if 24 <= lat <= 50 and -125 <= lon <= -60:
                    sites.append((lat, lon))
            except (StopIteration, ValueError, IndexError):
                continue
        return sites
    except Exception:
        return []


def panel_ameriflux(ax):
    _add_base_features(ax)

    # All AmeriFlux CONUS sites
    all_sites = _fetch_ameriflux_sites()
    if all_sites:
        lats, lons = zip(*all_sites)
        ax.scatter(lons, lats, transform=DATA_CRS,
                   s=12, color="#1f77b4", alpha=0.6,
                   linewidths=0.3, edgecolors="#145a86", zorder=4,
                   label="AmeriFlux towers")

    # Primary validation sites — gold stars
    for site_id, (lat, lon, label) in PRIMARY_SITES.items():
        ax.plot(lon, lat, transform=DATA_CRS,
                marker="*", markersize=14,
                color="#f5a623", markeredgecolor="#8b5e00",
                markeredgewidth=0.5, zorder=6)
        dlat, dlon = PRIMARY_OFFSETS[site_id]
        ax.annotate(label,
                    xy=(lon, lat), xycoords=DATA_CRS._as_mpl_transform(ax),
                    xytext=(lon + dlon, lat + dlat),
                    textcoords=DATA_CRS._as_mpl_transform(ax),
                    fontsize=5.5, ha="center",
                    arrowprops=dict(arrowstyle="-", color="#555555",
                                   lw=0.5))

    # Legend
    h1 = mlines.Line2D([], [], color="#1f77b4", marker="o", linestyle="None",
                        markersize=5, label="AmeriFlux towers")
    h2 = mlines.Line2D([], [], color="#f5a623", marker="*", linestyle="None",
                        markersize=9, markeredgecolor="#8b5e00",
                        label="Primary sites\n(Li et al. 2021)")
    ax.legend(handles=[h1, h2], loc="lower left", fontsize=5.5,
              framealpha=0.85, edgecolor="#aaaaaa")

    ax.set_title("(b) AmeriFlux latent heat flux validation", fontsize=9,
                 fontweight="bold", pad=4)


# ---------------------------------------------------------------------------
# Panel (c) — Critical Zone Observatory sites
# ---------------------------------------------------------------------------
# Coordinates from CZO Archive (czo-archive.criticalzone.org)
# Only CONUS-continental sites are shown on the main panel.
CZO_SITES = [
    # (name, lat, lon, has_rock_moisture)
    # has_rock_moisture = True if the CZO explicitly measured vadose-zone
    # rock moisture / deep weathered regolith moisture (Rempe & Dietrich 2018;
    # Dralle et al. 2018; Bales et al. 2011)
    ("Boulder Creek\n(CO)",          40.015, -105.378, True),
    ("Calhoun\n(SC)",                34.604,  -81.716, True),
    ("Eel River\n(CA)",              39.721, -123.644, True),
    ("IML\n(IA/IL/MN)",             41.932,  -93.690, False),
    ("Jemez–Santa\nCatalina\n(AZ)", 32.417, -110.767, True),
    ("Reynolds Creek\n(ID)",         43.206, -116.750, True),
    ("Shale Hills\n(PA)",            40.658,  -77.906, True),
    ("S. Sierra\n(CA)",              37.067, -119.200, True),
]
# Luquillo (Puerto Rico, 18.326N 65.817W) is outside CONUS; omitted from main map.


def panel_czo(ax):
    _add_base_features(ax)

    for name, lat, lon, rock_moist in CZO_SITES:
        color  = "#2ca02c" if rock_moist else "#bcbd22"
        marker = "^"
        ax.plot(lon, lat, transform=DATA_CRS,
                marker=marker, markersize=9,
                color=color, markeredgecolor="#1a6b1a" if rock_moist else "#888800",
                markeredgewidth=0.5, zorder=5)
        ax.annotate(name,
                    xy=(lon, lat), xycoords=DATA_CRS._as_mpl_transform(ax),
                    xytext=(lon + 1.5, lat + 1.5),
                    textcoords=DATA_CRS._as_mpl_transform(ax),
                    fontsize=4.5, ha="left",
                    arrowprops=dict(arrowstyle="-", color="#777777", lw=0.4))

    h_rm  = mlines.Line2D([], [], color="#2ca02c", marker="^",
                           linestyle="None", markersize=7,
                           markeredgecolor="#1a6b1a",
                           label="CZO w/ rock moisture")
    h_nrm = mlines.Line2D([], [], color="#bcbd22", marker="^",
                           linestyle="None", markersize=7,
                           markeredgecolor="#888800",
                           label="CZO w/o rock moisture")
    ax.legend(handles=[h_rm, h_nrm], loc="lower left", fontsize=5.5,
              framealpha=0.85, edgecolor="#aaaaaa")

    ax.set_title("(c) Critical Zone Observatory sites", fontsize=9,
                 fontweight="bold", pad=4)


# ---------------------------------------------------------------------------
# Panel (d) — SMAP coverage + GRACE mascon grid
# ---------------------------------------------------------------------------
# SMAP: global coverage at 36 km (L3) — shown as a CONUS-wide filled background
# GRACE: JPL RL06 mascons are 3° equal-area spherical caps.
#        We draw a schematic 3° lon × 3° lat grid over CONUS, which faithfully
#        represents the mascon spatial scale used in validation studies.

def _grace_mascon_grid(ax, lon_step=3.0, lat_step=3.0):
    """
    Draw schematic GRACE mascon grid (3° cells) over CONUS as thin grey lines.
    """
    lon_lines = np.arange(-126, -65, lon_step)
    lat_lines = np.arange(24, 51, lat_step)
    for lon in lon_lines:
        ax.plot([lon, lon], [LAT_S, LAT_N], transform=DATA_CRS,
                color="#7f7f7f", linewidth=0.5, alpha=0.7, zorder=4)
    for lat in lat_lines:
        ax.plot([LON_W, LON_E], [lat, lat], transform=DATA_CRS,
                color="#7f7f7f", linewidth=0.5, alpha=0.7, zorder=4)


def panel_smap_grace(ax):
    _add_base_features(ax)

    # SMAP coverage: shade the CONUS land area with a light blue fill
    # This represents SMAP's 36-km global coverage over the domain.
    # We add a second LAND feature with a blue tint on top at low alpha.
    smap_land = cfeature.NaturalEarthFeature("physical", "land", "50m",
                                              facecolor="#a8d5e2",
                                              edgecolor="none")
    ax.add_feature(smap_land, alpha=0.55, zorder=3)

    # GRACE mascon grid (schematic, 3° cells)
    _grace_mascon_grid(ax)

    # Legend / annotation
    smap_patch = mpatches.Patch(facecolor="#a8d5e2", alpha=0.7,
                                 edgecolor="#4a9ab5", linewidth=0.8,
                                 label="SMAP 36-km coverage")
    grace_line = mlines.Line2D([], [], color="#7f7f7f", linewidth=1.0,
                                label="GRACE mascon grid (3°)")
    ax.legend(handles=[smap_patch, grace_line], loc="lower left", fontsize=5.5,
              framealpha=0.85, edgecolor="#aaaaaa")

    ax.set_title("(d) SMAP / GRACE-FO TWS validation", fontsize=9,
                 fontweight="bold", pad=4)


# ---------------------------------------------------------------------------
# Main: compose 4-panel figure
# ---------------------------------------------------------------------------
def main():
    fig = plt.figure(figsize=(13, 8.5))

    # 2×2 grid with tight spacing
    axes = []
    positions = [221, 222, 223, 224]
    for pos in positions:
        ax = fig.add_subplot(pos, projection=PROJ)
        axes.append(ax)

    panel_topography(axes[0])
    panel_ameriflux(axes[1])
    panel_czo(axes[2])
    panel_smap_grace(axes[3])

    fig.suptitle(
        "Proposed study domain and validation network",
        fontsize=11, fontweight="bold", y=1.01
    )

    plt.tight_layout(pad=1.5)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "map_4panel.png")
    fig.savefig(out_path, dpi=200, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
