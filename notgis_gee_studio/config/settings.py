"""
Global konstantlar, default qiymatlar va session state boshqaruvi.

Bu modul butun ilova uchun yagona manba bo'lib xizmat qiladi.
Barcha default konfiguratsiyalar shu yerda belgilanadi.
"""
import streamlit as st
from datetime import date, timedelta


class Settings:
    """Ilova uchun global konstantlar."""

    APP_NAME = "notGIS GEE Studio"
    APP_VERSION = "1.0.0"
    APP_ICON = "🛰"

    # Layout o'lchamlari
    NAVBAR_HEIGHT = 52
    STATUS_HEIGHT = 28
    LEFT_PANEL_WIDTH = 280
    RIGHT_PANEL_WIDTH = 300
    PANEL_GAP = 1

    # Indeks limiti
    MAX_INDICES = 7

    # Vaqt tez tanlash (yillar)
    QUICK_DATE_OPTIONS = {
        "1Y": 1,
        "3Y": 3,
        "5Y": 5,
        "10Y": 10,
        "Max": 40,
    }

    # Satellite manbalari
    SATELLITES = {
        "Sentinel-2 SR Harmonized": {
            "id": "sentinel2",
            "collection": "COPERNICUS/S2_SR_HARMONIZED",
            "scale": 10,
            "cloud_field": "CLOUDY_PIXEL_PERCENTAGE",
            "bands_rgb": ["B4", "B3", "B2"],
        },
        "Sentinel-1 SAR GRD": {
            "id": "sentinel1",
            "collection": "COPERNICUS/S1_GRD",
            "scale": 10,
            "cloud_field": None,
            "bands_rgb": ["VV", "VH", "VV"],
        },
        "Landsat 8/9 SR C2": {
            "id": "landsat89",
            "collection": "LANDSAT/LC08/C02/T1_L2",
            "scale": 30,
            "cloud_field": "CLOUD_COVER",
            "bands_rgb": ["SR_B4", "SR_B3", "SR_B2"],
        },
        "Landsat 5/7 SR C2": {
            "id": "landsat57",
            "collection": "LANDSAT/LE07/C02/T1_L2",
            "scale": 30,
            "cloud_field": "CLOUD_COVER",
            "bands_rgb": ["SR_B3", "SR_B2", "SR_B1"],
        },
        "MODIS Terra Daily": {
            "id": "modis",
            "collection": "MODIS/061/MOD09GA",
            "scale": 500,
            "cloud_field": None,
            "bands_rgb": ["sur_refl_b01", "sur_refl_b04", "sur_refl_b03"],
        },
        "ERA5 Climate Daily": {
            "id": "era5",
            "collection": "ECMWF/ERA5_LAND/DAILY_AGGR",
            "scale": 11132,
            "cloud_field": None,
            "bands_rgb": None,
        },
    }

    # Composite usullari
    COMPOSITES = ["median", "mean", "min", "max", "mosaic"]

    # Vaqt bo'limlari
    TIME_UNITS = ["Yillik", "Oylik", "Mavsumiy"]

    # CRS variantlari
    CRS_OPTIONS = {
        "EPSG:32640": "WGS 84 / UTM zone 40N",
        "EPSG:32641": "WGS 84 / UTM zone 41N",
        "EPSG:32642": "WGS 84 / UTM zone 42N",
        "EPSG:4326": "WGS 84 (Geographic)",
    }

    # Eksport scale variantlari
    EXPORT_SCALES = [10, 30, 100, 250, 500, 1000]

    # Klassifikatsiya usullari
    CLASSIFICATION_METHODS = [
        "Natural Breaks (Jenks)",
        "Equal Interval",
        "Quantile",
        "Standard Deviation",
    ]

    # Palitra nomlari
    PALETTES = {
        "RdYlGn": ["#d73027", "#fc8d59", "#fee08b", "#d9ef8b", "#91cf60", "#1a9850"],
        "Viridis": ["#440154", "#414487", "#2a788e", "#22a884", "#7ad151", "#fde725"],
        "Plasma": ["#0d0887", "#6a00a8", "#b12a90", "#e16462", "#fca636", "#f0f921"],
        "Spectral": ["#9e0142", "#d53e4f", "#f46d43", "#fdae61", "#abdda4", "#66c2a5", "#3288bd", "#5e4fa2"],
        "YlOrRd": ["#ffffb2", "#fed976", "#feb24c", "#fd8d3c", "#fc4e2a", "#e31a1c", "#b10026"],
        "RdBu": ["#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#d1e5f0", "#92c5de", "#4393c3", "#2166ac"],
        "Blues": ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#084594"],
        "Greens": ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#005a32"],
    }

    # AI providerlar
    AI_PROVIDERS = {
        "Gemini": {
            "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
            "default_model": "gemini-2.0-flash",
        },
        "Groq": {
            "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            "default_model": "llama-3.3-70b-versatile",
        },
        "OpenRouter": {
            "models": ["meta-llama/llama-3.3-70b-instruct", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5"],
            "default_model": "meta-llama/llama-3.3-70b-instruct",
        },
        "RouterWay": {
            "models": ["gpt-4o", "claude-3.5-sonnet", "gemini-pro"],
            "default_model": "gpt-4o",
        },
    }


def get_default_config():
    """
    Standart konfiguratsiya dict qaytaradi.

    Returns:
        dict: Barcha sozlamalar uchun default qiymatlar
    """
    today = date.today()
    return {
        "satellite": "Sentinel-2 SR Harmonized",
        "start_date": today - timedelta(days=365 * 5),
        "end_date": today,
        "cloud_pct": 20,
        "composite": "median",
        "time_unit": "Yillik",
        "selected_indices": [],
        "aoi_type": "predefined",
        "aoi_geometry": None,
        "aoi_name": "",
        "aoi_geojson": None,
        "buffer_km": 0,
        "class_count": 5,
        "classification": "Natural Breaks (Jenks)",
        "palette": "RdYlGn",
        "custom_colors": [],
        "value_min": -0.2,
        "value_max": 0.8,
        "scale": 30,
        "crs": "EPSG:32640",
        "max_pixels": 1e13,
        "drive_folder": "notGIS_exports",
    }


def init_session_state():
    """
    Session state ni boshlang'ich qiymatlar bilan to'ldiradi.
    Faqat app.py da bir marta chaqiriladi.
    """
    defaults = {
        # GEE
        "gee_connected": False,
        "gee_project": None,
        "gee_auth_method": None,
        "gee_quota": None,

        # Konfiguratsiya
        "config": get_default_config(),

        # Natijalar
        "results_df": None,
        "map_layers": [],
        "last_stats": None,
        "trend_results": None,

        # Log
        "logs": [],

        # AI
        "ai_messages": [],
        "ai_provider": None,
        "ai_api_key": None,
        "ai_model": None,

        # UI holat
        "panel_sections": {
            "connection": True,
            "satellite": True,
            "datetime": True,
            "aoi": True,
            "indices": True,
            "legend": False,
            "export_cfg": False,
        },
        "right_tab": "charts",
        "analysis_running": False,
        "dark_mode": True,
        "map_center": [41.3, 64.5],
        "map_zoom": 6,
        "drawn_geometry": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def update_config(key, value):
    """
    Konfiguratsiya qiymatini xavfsiz yangilaydi.

    Args:
        key: str — config kalit nomi
        value: any — yangi qiymat
    """
    if "config" not in st.session_state:
        st.session_state["config"] = get_default_config()
    st.session_state["config"][key] = value


def get_config(key, default=None):
    """
    Konfiguratsiya qiymatini o'qiydi.

    Args:
        key: str — config kalit nomi
        default: any — topilmasa qaytariladigan qiymat

    Returns:
        any: config qiymati yoki default
    """
    if "config" not in st.session_state:
        return default
    return st.session_state["config"].get(key, default)
