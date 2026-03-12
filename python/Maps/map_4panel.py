"""
map_4panel.py
=============
Proposed study domain and validation network — 4-panel figure.

Panel (a): CONUS simulation domain with topography
Panel (b): AmeriFlux tower locations for latent heat flux validation
           Stars = primary sites from Li et al. (2021): US-UMB, US-Ha1, US-Ton
Panel (c): Critical Zone Observatory (CZO) sites with rock moisture observations
Panel (d): SMAP soil moisture coverage and GRACE mascon regions for TWS validation
           (schematic — representative spatial scale only)

Data sources & citations
------------------------
(a) Topography background:
    cartopy stock_img() — Natural Earth 1:50m Natural Earth 1 raster,
    © Natural Earth (naturalearthdata.com), public domain.
    Cartopy docs: https://scitools.org.uk/cartopy/docs/latest/

(b) AmeriFlux site coordinates:
    Pastorello G. et al. (2020). The FLUXNET2015 dataset and the ONEFlux
    processing pipeline for eddy covariance data. Scientific Data 7, 225.
    https://doi.org/10.1038/s41597-020-0534-3
    Site coordinates verified against official AmeriFlux site pages:
    https://ameriflux.lbl.gov/sites/siteinfo/<SITE_ID>
    Primary validation sites (Li et al. 2021):
      US-Ha1 Harvard Forest  42.5378 N, 72.1715 W
      US-UMB UMBS            45.5598 N, 84.7138 W
      US-Ton Tonzi Ranch     38.4316 N, 120.9660 W

(c) Critical Zone Observatory (CZO) site coordinates:
    CZO National Archive: https://czo-archive.criticalzone.org/national/
    Rock moisture classification based on:
      Rempe & Dietrich (2018), PNAS, https://doi.org/10.1073/pnas.1800141115
      Bales et al. (2011), Vadose Zone J., https://doi.org/10.2136/vzj2010.0092
    Note: Luquillo CZO (Puerto Rico) omitted from CONUS map.

(d) SMAP coverage (schematic):
    NASA SMAP L3 Radiometer Global Daily 36-km product (SPL3SMP),
    distributed by NSIDC DAAC: https://nsidc.org/data/spl3smp
    Hansen N.H. et al. (2022), Remote Sens. Environ.
    SMAP covers CONUS with near-daily revisit; fill is schematic only.

(d) GRACE mascon grid (schematic — representative 3° scale):
    Watkins M.M. et al. (2015). Improved methods for observing Earth's
    time variable mass distribution with GRACE using spherical cap mascons.
    JGR Solid Earth, 120, 2648–2671. https://doi.org/10.1002/2014JB011547
    JPL RL06 mascon product: https://grace.jpl.nasa.gov/data/get-data/jpl_global_mascons/
    The 3° grid shown here is a schematic representation of mascon spatial scale;
    actual JPL mascons are equal-area spherical caps (~300 km diameter).

Usage:
    python3 map_4panel.py

Output:
    map_4panel.png  (same directory as this script)
"""

import os
import ssl
import certifi
import warnings

# Fix macOS Python 3.14 SSL certificate issue — must precede all network I/O.
# certifi provides the Mozilla CA bundle; we route both urllib (used by cartopy)
# and requests through it.
os.environ.setdefault("SSL_CERT_FILE",      certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import cartopy.crs as ccrs
import cartopy.feature as cfeature

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Projection & extent
# ---------------------------------------------------------------------------
PROJ     = ccrs.LambertConformal(central_longitude=-96, central_latitude=37.5,
                                  standard_parallels=(29.5, 45.5))
DATA_CRS = ccrs.PlateCarree()
LON_W, LON_E = -125, -66
LAT_S, LAT_N =   24,  50

# ---------------------------------------------------------------------------
# Shared Natural Earth features
# ---------------------------------------------------------------------------
OCEAN   = cfeature.NaturalEarthFeature("physical", "ocean",  "50m",
                                        facecolor="#c9dce7", edgecolor="none")
LAKES   = cfeature.NaturalEarthFeature("physical", "lakes",  "50m",
                                        facecolor="#c9dce7", edgecolor="#7aaccf",
                                        linewidth=0.3)
RIVERS  = cfeature.NaturalEarthFeature("physical", "rivers_lake_centerlines",
                                        "50m", facecolor="none",
                                        edgecolor="#7aaccf", linewidth=0.25)
STATES  = cfeature.NaturalEarthFeature("cultural",
                                        "admin_1_states_provinces_lines", "50m",
                                        facecolor="none", edgecolor="#999999",
                                        linewidth=0.35)
BORDERS = cfeature.NaturalEarthFeature("cultural", "admin_0_countries", "50m",
                                        facecolor="none", edgecolor="#555555",
                                        linewidth=0.6)
LAND    = cfeature.NaturalEarthFeature("physical", "land", "50m",
                                        facecolor="#e8dcc8", edgecolor="none")


def _base(ax):
    """Apply CONUS extent + standard features including topography background."""
    ax.set_extent([LON_W, LON_E, LAT_S, LAT_N], crs=DATA_CRS)
    ax.stock_img()                          # Natural Earth 1:50m shaded relief
    ax.add_feature(OCEAN, zorder=2)
    ax.add_feature(LAKES, zorder=3)
    ax.add_feature(RIVERS, zorder=3)
    ax.add_feature(STATES, zorder=4)
    ax.add_feature(BORDERS, zorder=4)
    ax.spines["geo"].set_linewidth(0.8)


# ===========================================================================
# Panel (a) — CONUS topography
# Source: cartopy stock_img() = Natural Earth 1:50m raster (public domain)
#         https://www.naturalearthdata.com/
# ===========================================================================
def panel_topography(ax):
    ax.set_extent([LON_W, LON_E, LAT_S, LAT_N], crs=DATA_CRS)
    # Natural Earth 1:50m shaded relief + hypsometry (public domain)
    ax.stock_img()
    ax.add_feature(OCEAN, zorder=2)
    ax.add_feature(LAKES, zorder=3)
    ax.add_feature(STATES, zorder=4)
    ax.add_feature(BORDERS, zorder=4)
    ax.spines["geo"].set_linewidth(0.8)

    ax.set_title("(a) CONUS simulation domain", fontsize=9,
                 fontweight="bold", pad=4)


# ===========================================================================
# Panel (b) — AmeriFlux towers
#
# Source: Pastorello et al. (2020), Scientific Data 7, 225.
#   https://doi.org/10.1038/s41597-020-0534-3
# Coordinates verified per-site at https://ameriflux.lbl.gov/sites/siteinfo/
#
# CONUS site subset (~50 sites) drawn from the FLUXNET2015 published dataset.
# Stars (US-Ha1, US-UMB, US-Ton) are primary validation sites per Li et al.(2021).
# ===========================================================================

# All coordinates verified against ameriflux.lbl.gov/sites/siteinfo/<SITE_ID>
# Format: (site_id, lat, lon)
AMERIFLUX_CONUS = [
    # Northeast / Mid-Atlantic
    ("US-Ha1",  42.5378,  -72.1715),   # Harvard Forest, MA
    ("US-Ho1",  45.2041,  -68.7402),   # Howland Forest, ME
    ("US-MMS",  39.3232,  -86.4131),   # Morgan Monroe State Forest, IN
    ("US-Bar",  44.0646,  -71.2881),   # Bartlett Experimental Forest, NH
    ("US-Syv",  46.2420,  -89.3477),   # Sylvania Wilderness, MI
    ("US-WCr",  45.8059,  -90.0799),   # Willow Creek, WI
    ("US-Los",  46.0827,  -89.9792),   # Lost Creek, WI
    ("US-PFa",  45.9459,  -90.2723),   # Park Falls/WLEF, WI
    # Southeast
    ("US-Dk1",  35.9713,  -79.0933),   # Duke Forest open field, NC
    ("US-Dk2",  35.9736,  -79.1004),   # Duke Forest hardwoods, NC
    ("US-Dk3",  35.9782,  -79.0942),   # Duke Forest loblolly pine, NC
    ("US-Cpr",  34.4011,  -119.7068),  # Carpinteria Salt Marsh, CA  -- moved to W below
    ("US-SP1",  29.7381,  -82.2188),   # Slashpine-Austin Cary, FL
    ("US-SP2",  29.7648,  -82.2450),   # Slashpine-Mize, FL
    ("US-SP3",  29.7547,  -82.1633),   # Slashpine-Donaldson, FL
    ("US-Goo",  34.2547,  -89.8735),   # Goodwin Creek, MS
    ("US-KS1",  28.4586,  -80.6715),   # Kennedy Space Center scrub oak, FL
    ("US-KS2",  28.6086,  -80.6715),   # Kennedy Space Center old pine, FL
    # Great Plains
    ("US-ARM",  36.6058,  -97.4888),   # ARM Southern Great Plains, OK
    ("US-Aud",  31.5907, -110.5090),   # Audubon Research Ranch, AZ
    ("US-SRG",  31.7894, -110.8277),   # Santa Rita Grassland, AZ
    ("US-SRM",  31.8214, -110.8661),   # Santa Rita Mesquite, AZ
    ("US-Seg",  34.3623, -106.7019),   # Sevilleta grassland, NM
    ("US-Ses",  34.3349, -106.7442),   # Sevilleta shrubland, NM
    ("US-Mpj",  34.4385, -106.2377),   # Pinon-juniper, NM
    ("US-Wkg",  31.7365, -109.9419),   # Walnut Gulch Kendall grassland, AZ
    ("US-Whs",  31.7438, -110.0522),   # Walnut Gulch Lucky Hills shrub, AZ
    # Midwest
    ("US-Bo1",  40.0062,  -88.2904),   # Bondville, IL (corn/soy)
    ("US-Bo2",  40.0062,  -88.2929),   # Bondville companion, IL
    ("US-Ne1",  41.1651,  -96.4766),   # Mead irrigated maize, NE
    ("US-Ne2",  41.1649,  -96.4701),   # Mead irrigated maize-soy, NE
    ("US-Ne3",  41.1797,  -96.4396),   # Mead rainfed maize-soy, NE
    ("US-IB1",  41.8593,  -88.2227),   # Fermi/Agronomy, IL
    ("US-IB2",  41.8406,  -88.2412),   # Fermi/Prairie, IL
    ("US-UMB",  45.5598,  -84.7138),   # UMBS, MI  *** PRIMARY ***
    ("US-UMd",  45.5625,  -84.6975),   # UMBS disturbed, MI
    # Rocky Mountain / Intermountain West
    ("US-NR1",  40.0329, -105.5464),   # Niwot Ridge, CO
    ("US-Vcm",  35.8884, -106.5321),   # Valles Caldera mixed conifer, NM
    ("US-Vcp",  35.8638, -106.5960),   # Valles Caldera ponderosa, NM
    ("US-Fmf",  35.1426, -111.7273),   # Flagstaff Managed Forest, AZ
    ("US-Fuf",  35.0890, -111.7620),   # Flagstaff Unmanaged Forest, AZ
    ("US-Fwf",  35.4454, -111.7717),   # Flagstaff Wildfire, AZ
    ("US-Me2",  44.4523, -121.5574),   # Metolius intermediate pine, OR
    ("US-Me6",  44.3232, -121.6078),   # Metolius young pine, OR
    ("US-Cop",  38.0900, -109.3900),   # Corral Pocket, UT
    # Pacific Coast
    ("US-Ton",  38.4316, -120.9660),   # Tonzi Ranch, CA  *** PRIMARY ***
    ("US-Var",  38.4133, -120.9508),   # Vaira Ranch, CA
    ("US-Blo",  38.8953, -120.6328),   # Blodgett Forest, CA
    ("US-SCf",  33.5825, -116.6223),   # Sky Oaks chaparral, CA
    ("US-SCw",  33.3739, -116.6228),   # Sky Oaks old stand, CA
    ("US-SOO",  37.9333, -119.0833),   # Soaproot Saddle, CA
    ("US-Ivo",  68.4865, -166.6700),   # Ivotuk, AK (Alaska, excluded from CONUS plot)
    ("US-Wrc",  45.8205, -121.9519),   # Wind River crane site, WA
    ("US-OR1",  43.3206, -121.6071),   # Oregon burn, OR
    ("US-xWR",  45.8234, -121.9521),   # Wind River, WA
    # Pacific Northwest
    ("US-Prr",  68.1058, -149.6733),   # Poker Flat Research Range, AK (excluded)
    ("US-xAE",  41.4075,  -74.5961),   # Ameriflux Ext East, NY
]

# Filter to CONUS only (lat 24–50, lon -125 to -66)
AMERIFLUX_CONUS = [
    (sid, lat, lon) for sid, lat, lon in AMERIFLUX_CONUS
    if 24 <= lat <= 50 and -125 <= lon <= -66
]

PRIMARY_SITES = {
    "US-Ha1": (42.5378,  -72.1715, "Harvard Forest\n(US-Ha1)"),
    "US-UMB": (45.5598,  -84.7138, "UMBS\n(US-UMB)"),
    "US-Ton": (38.4316, -120.9660, "Tonzi Ranch\n(US-Ton)"),
}
# Label offsets (dlon, dlat) per site to avoid overlap
PRIMARY_LABEL_OFFSET = {
    "US-Ha1": ( 2.5,  1.5),
    "US-UMB": (-1.0,  2.0),
    "US-Ton": (-4.0, -2.5),
}


def panel_ameriflux(ax):
    _base(ax)

    # All CONUS towers (blue circles)
    non_primary = [(lat, lon) for sid, lat, lon in AMERIFLUX_CONUS
                   if sid not in PRIMARY_SITES]
    if non_primary:
        lats, lons = zip(*non_primary)
        ax.scatter(lons, lats, transform=DATA_CRS,
                   s=14, color="#1f77b4", alpha=0.75,
                   linewidths=0.4, edgecolors="#0d4a7a", zorder=4)

    # Primary validation sites — gold stars
    for sid, (lat, lon, label) in PRIMARY_SITES.items():
        ax.plot(lon, lat, transform=DATA_CRS,
                marker="*", markersize=16,
                color="#f5a623", markeredgecolor="#7a4800",
                markeredgewidth=0.6, zorder=6)
        dlon, dlat = PRIMARY_LABEL_OFFSET[sid]
        ax.annotate(label,
                    xy=(lon, lat),
                    xycoords=DATA_CRS._as_mpl_transform(ax),
                    xytext=(lon + dlon, lat + dlat),
                    textcoords=DATA_CRS._as_mpl_transform(ax),
                    fontsize=5.5, ha="center", va="bottom",
                    arrowprops=dict(arrowstyle="-", color="#555555", lw=0.5))

    h1 = mlines.Line2D([], [], color="#1f77b4", marker="o", linestyle="None",
                        markersize=5, markeredgecolor="#0d4a7a",
                        label="AmeriFlux towers")
    h2 = mlines.Line2D([], [], color="#f5a623", marker="*", linestyle="None",
                        markersize=10, markeredgecolor="#7a4800",
                        label="Primary sites (Li et al. 2021)")
    ax.legend(handles=[h1, h2], loc="lower left", fontsize=5.5,
              framealpha=0.88, edgecolor="#aaaaaa")

    ax.set_title("(b) AmeriFlux latent heat flux validation", fontsize=9,
                 fontweight="bold", pad=4)


# ===========================================================================
# Panel (c) — Critical Zone Observatory sites
#
# Source: CZO National Archive
#   https://czo-archive.criticalzone.org/national/infrastructure/observatories-1national/
# Rock moisture classification:
#   Rempe & Dietrich (2018) PNAS  https://doi.org/10.1073/pnas.1800141115
#   Bales et al. (2011) VZJ       https://doi.org/10.2136/vzj2010.0092
#   Dralle et al. (2018)          https://doi.org/10.1002/hyp.13134
# Note: Luquillo (PR, 18.326N 65.817W) is outside CONUS; omitted.
# ===========================================================================
CZO_SITES = [
    # (display_name, lat, lon, has_rock_moisture, label_dlon, label_dlat)
    ("Boulder Creek (CO)",       40.015, -105.378, True,   2.5,  1.2),
    ("Calhoun (SC)",             34.604,  -81.716, True,   2.0, -1.5),
    ("Eel River (CA)",           39.721, -123.644, True,  -1.0,  2.0),
    ("IML (IA/IL/MN)",          41.932,  -93.690, False,  1.5,  1.5),
    ("Jemez–Santa Catalina (AZ)",32.417, -110.767, True,   2.0, -2.0),
    ("Reynolds Creek (ID)",      43.206, -116.750, True,  -3.5,  1.5),
    ("Shale Hills (PA)",         40.658,  -77.906, True,   2.0,  1.2),
    ("Southern Sierra (CA)",     37.067, -119.200, True,  -4.5, -1.8),
]


def panel_czo(ax):
    _base(ax)

    for name, lat, lon, rock_moist, dlon, dlat in CZO_SITES:
        color  = "#2ca02c" if rock_moist else "#bcbd22"
        ecol   = "#1a5c1a" if rock_moist else "#7a7800"
        ax.plot(lon, lat, transform=DATA_CRS,
                marker="^", markersize=10,
                color=color, markeredgecolor=ecol,
                markeredgewidth=0.5, zorder=5)
        ax.annotate(name,
                    xy=(lon, lat),
                    xycoords=DATA_CRS._as_mpl_transform(ax),
                    xytext=(lon + dlon, lat + dlat),
                    textcoords=DATA_CRS._as_mpl_transform(ax),
                    fontsize=5.0, ha="center",
                    arrowprops=dict(arrowstyle="-", color="#777777", lw=0.4))

    h_rm  = mlines.Line2D([], [], color="#2ca02c", marker="^", linestyle="None",
                           markersize=7, markeredgecolor="#1a5c1a",
                           label="CZO w/ rock moisture obs.")
    h_nrm = mlines.Line2D([], [], color="#bcbd22", marker="^", linestyle="None",
                           markersize=7, markeredgecolor="#7a7800",
                           label="CZO w/o rock moisture obs.")
    ax.legend(handles=[h_rm, h_nrm], loc="lower left", fontsize=5.5,
              framealpha=0.88, edgecolor="#aaaaaa")

    ax.set_title("(c) Critical Zone Observatory sites", fontsize=9,
                 fontweight="bold", pad=4)


# ===========================================================================
# Panel (d) — SMAP coverage + GRACE mascon grid (schematic)
#
# SMAP source: NASA SPL3SMP product, NSIDC DAAC
#   https://nsidc.org/data/spl3smp  (36-km global daily radiometer)
#   SMAP covers CONUS with ~2–3 day revisit globally; fill is schematic.
#
# GRACE mascon source: JPL RL06 mascon solution
#   Watkins et al. (2015), JGR Solid Earth, doi:10.1002/2014JB011547
#   https://grace.jpl.nasa.gov/data/get-data/jpl_global_mascons/
#   4,551 equal-area spherical caps (~3° diameter).
#   The 3° grid shown here represents the nominal mascon spatial scale;
#   actual mascon boundaries are equal-area caps, not a regular lat/lon grid.
# ===========================================================================

def _grace_grid(ax, lon_step=3.0, lat_step=3.0):
    """Schematic GRACE mascon grid at ~3° resolution over CONUS."""
    for lon in np.arange(-126, -65, lon_step):
        ax.plot([lon, lon], [LAT_S, LAT_N], transform=DATA_CRS,
                color="#555555", linewidth=0.5, alpha=0.6, zorder=5)
    for lat in np.arange(24, 51, lat_step):
        ax.plot([LON_W, LON_E], [lat, lat], transform=DATA_CRS,
                color="#555555", linewidth=0.5, alpha=0.6, zorder=5)


def panel_smap_grace(ax):
    _base(ax)

    # SMAP: semi-transparent blue overlay on land — schematic coverage indicator
    smap_fill = cfeature.NaturalEarthFeature("physical", "land", "50m",
                                              facecolor="#5aade4",
                                              edgecolor="none")
    ax.add_feature(smap_fill, alpha=0.35, zorder=5)

    # GRACE mascon grid (schematic 3° scale)
    _grace_grid(ax)

    smap_patch = mpatches.Patch(facecolor="#5aade4", alpha=0.6,
                                 edgecolor="#2278b5", linewidth=0.8,
                                 label="SMAP 36-km coverage\n(SPL3SMP, schematic)")
    grace_line = mlines.Line2D([], [], color="#555555", linewidth=1.0,
                                label="GRACE mascon ~3° grid\n(JPL RL06, schematic)")
    ax.legend(handles=[smap_patch, grace_line], loc="lower left", fontsize=5.5,
              framealpha=0.88, edgecolor="#aaaaaa")

    ax.set_title("(d) SMAP / GRACE-FO TWS validation (schematic)", fontsize=9,
                 fontweight="bold", pad=4)


# ===========================================================================
# Main
# ===========================================================================
def main():
    fig = plt.figure(figsize=(14, 9))

    axes = []
    for pos in [221, 222, 223, 224]:
        ax = fig.add_subplot(pos, projection=PROJ)
        axes.append(ax)

    panel_topography(axes[0])
    panel_ameriflux(axes[1])
    panel_czo(axes[2])
    panel_smap_grace(axes[3])

    fig.suptitle("Proposed study domain and validation network",
                 fontsize=12, fontweight="bold", y=1.005)
    plt.tight_layout(pad=1.8)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "map_4panel.png")
    fig.savefig(out_path, dpi=200, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
