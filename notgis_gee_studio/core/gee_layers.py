"""
Xaritaga layer qo'shish (Tile URL).

GEE obrazlarini Folium xaritasiga tile layer sifatida qo'shadi.
"""
import streamlit as st

try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False

from core.indices import get_index
from config.settings import Settings
from utils.log_manager import add_log


class GEELayerManager:
    """GEE layer boshqaruvi."""

    @staticmethod
    def add_index_layer(index_name, image, vis_params=None):
        """
        Indeks obrazini xarita layeriga qo'shadi.

        Args:
            index_name: str — indeks nomi
            image: ee.Image — indeks obrazi
            vis_params: dict yoki None — vizualizatsiya parametrlari

        Returns:
            dict: {name, url, vis_params} yoki None
        """
        if not EE_AVAILABLE or image is None:
            return None

        idx_info = get_index(index_name)
        if not idx_info:
            return None

        if vis_params is None:
            palette_name = idx_info.get("default_palette", "RdYlGn")
            palette = Settings.PALETTES.get(palette_name, Settings.PALETTES["RdYlGn"])
            display_range = idx_info.get("display_range", {"min": -1, "max": 1})

            vis_params = {
                "min": display_range["min"],
                "max": display_range["max"],
                "palette": palette,
            }

        try:
            map_id = image.getMapId(vis_params)
            tile_url = map_id["tile_fetcher"].url_format

            layer_info = {
                "name": index_name,
                "url": tile_url,
                "vis_params": vis_params,
                "visible": True,
            }

            if "map_layers" not in st.session_state:
                st.session_state["map_layers"] = []

            existing = [l for l in st.session_state["map_layers"] if l["name"] != index_name]
            existing.append(layer_info)
            st.session_state["map_layers"] = existing

            add_log(f"Layer qo'shildi: {index_name}", "success")
            return layer_info

        except Exception as e:
            add_log(f"Layer qo'shish xatosi ({index_name}): {str(e)}", "error")
            return None

    @staticmethod
    def remove_layer(index_name):
        """
        Layerni xaritadan olib tashlaydi.

        Args:
            index_name: str — olib tashlanadigan layer nomi
        """
        if "map_layers" in st.session_state:
            st.session_state["map_layers"] = [
                l for l in st.session_state["map_layers"] if l["name"] != index_name
            ]
            add_log(f"Layer olib tashlandi: {index_name}", "info")

    @staticmethod
    def clear_layers():
        """Barcha layerlarni tozalaydi."""
        st.session_state["map_layers"] = []
        add_log("Barcha layerlar tozalandi", "info")

    @staticmethod
    def toggle_layer_visibility(index_name, visible=None):
        """
        Layer ko'rinishini almashtiradi.

        Args:
            index_name: str — layer nomi
            visible: bool yoki None — None bo'lsa toggle qiladi
        """
        if "map_layers" not in st.session_state:
            return

        for layer in st.session_state["map_layers"]:
            if layer["name"] == index_name:
                if visible is None:
                    layer["visible"] = not layer["visible"]
                else:
                    layer["visible"] = visible
                break
