"""
Folium xarita + layer boshqaruv.

Xaritani yaratadi, GEE layer'larini qo'shadi, AOI polygon ko'rsatadi.
"""
import streamlit as st
import folium
from folium import plugins

try:
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

from config.settings import get_config, Settings
from config.aoi_registry import AOIRegistry


def create_map():
    """
    Folium xarita yaratadi.

    Returns:
        folium.Map — sozlangan xarita
    """
    center = st.session_state.get("map_center", [41.3, 64.5])
    zoom = st.session_state.get("map_zoom", 6)

    basemap_sel = st.session_state.get("sel_basemap", "Dark")
    tiles_map = {
        "Dark": "cartodbdark_matter",
        "Satellite": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        "OSM": "OpenStreetMap",
        "Topo": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
    }

    tile_source = tiles_map.get(basemap_sel, "cartodbdark_matter")

    if tile_source.startswith("http"):
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles=tile_source,
            attr="Google",
            control_scale=True,
        )
    else:
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles=tile_source,
            control_scale=True,
        )

    # AOI polygon qo'shish
    _add_aoi_to_map(m)

    # GEE layer'lar qo'shish
    _add_gee_layers(m)

    # Chizish asboblari
    draw = plugins.Draw(
        export=False,
        draw_options={
            "polyline": False,
            "circle": True,
            "rectangle": True,
            "polygon": True,
            "marker": False,
            "circlemarker": False,
        },
        edit_options={"edit": True, "remove": True},
    )
    draw.add_to(m)

    # O'lchash asbobi
    plugins.MeasureControl(
        position="topright",
        primary_length_unit="kilometers",
        primary_area_unit="hectares",
    ).add_to(m)

    # Minimap
    plugins.MiniMap(toggle_display=True).add_to(m)

    # Mouse koordinatlari
    plugins.MousePosition(
        position="bottomleft",
        separator=" | ",
        prefix="Koordinat:",
        num_digits=6,
    ).add_to(m)

    # Fullscreen
    plugins.Fullscreen().add_to(m)

    # Layer boshqaruv
    folium.LayerControl(collapsed=True).add_to(m)

    return m


def _add_aoi_to_map(m):
    """
    AOI polygon ni xaritaga qo'shadi.

    Args:
        m: folium.Map
    """
    geojson = get_config("aoi_geojson")
    if geojson:
        try:
            folium.GeoJson(
                geojson,
                name="AOI",
                style_function=lambda x: {
                    "fillColor": "transparent",
                    "color": "#F5C518",
                    "weight": 2,
                    "dashArray": "5, 5",
                    "fillOpacity": 0.05,
                },
            ).add_to(m)
        except Exception:
            pass

    aoi_name = get_config("aoi_name", "")
    if aoi_name and not geojson:
        bbox = AOIRegistry.get_bbox_as_ee_geometry(aoi_name)
        if bbox:
            bounds = [[bbox[1], bbox[0]], [bbox[3], bbox[2]]]
            folium.Rectangle(
                bounds=bounds,
                color="#F5C518",
                weight=2,
                dash_array="5, 5",
                fill=True,
                fill_opacity=0.05,
                popup=aoi_name,
            ).add_to(m)


def _add_gee_layers(m):
    """
    GEE tile layer'larni xaritaga qo'shadi.

    Args:
        m: folium.Map
    """
    layers = st.session_state.get("map_layers", [])

    for layer in layers:
        if not layer.get("visible", True):
            continue

        url = layer.get("url")
        name = layer.get("name", "Layer")

        if url:
            folium.TileLayer(
                tiles=url,
                attr="Google Earth Engine",
                name=name,
                overlay=True,
                control=True,
                opacity=0.8,
            ).add_to(m)


def render_map():
    """Xaritani Streamlit da ko'rsatadi."""

    if not FOLIUM_AVAILABLE:
        st.warning("streamlit-folium o'rnatilmagan")
        st.code("pip install streamlit-folium")
        return

    m = create_map()

    map_data = st_folium(
        m,
        width=None,
        height=600,
        key="main_map",
        returned_objects=["all_drawings"],
    )

    # Chizilgan geometriyani saqlash
    if map_data and map_data.get("all_drawings"):
        drawings = map_data["all_drawings"]
        if drawings:
            last_drawing = drawings[-1]
            geom = last_drawing.get("geometry")
            if geom:
                st.session_state["drawn_geometry"] = geom
