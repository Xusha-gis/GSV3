"""
Hudud tanlash bo'limi.

Oldindan belgilangan hududlar, GeoJSON yuklash, GEE Asset, bufer.
"""
import json
import streamlit as st
from config.settings import update_config, get_config
from config.aoi_registry import AOIRegistry
from utils.log_manager import add_log


def render_aoi_section():
    """Hudud tanlash bo'limini ko'rsatadi."""

    aoi_type = st.radio(
        "AOI turi",
        ["Hudud", "GeoJSON/KML", "GEE Asset", "Chizish"],
        horizontal=True,
        key="radio_aoi_type",
        label_visibility="collapsed",
    )
    update_config("aoi_type", aoi_type)

    if aoi_type == "Hudud":
        regions = AOIRegistry.get_region_names()
        current_aoi = get_config("aoi_name", "")
        idx = regions.index(current_aoi) if current_aoi in regions else 0

        selected = st.selectbox(
            "Viloyat",
            regions,
            index=idx,
            key="sel_aoi_region",
            label_visibility="collapsed",
        )
        update_config("aoi_name", selected)

        region_info = AOIRegistry.get_region(selected)
        if region_info:
            bbox = region_info.get("bbox", [])
            if bbox:
                st.caption(f"Bbox: {bbox[0]:.1f}°N, {bbox[1]:.1f}°E — {bbox[2]:.1f}°N, {bbox[3]:.1f}°E")
                geojson = {
                    "type": "Polygon",
                    "coordinates": [[
                        [bbox[1], bbox[0]],
                        [bbox[3], bbox[0]],
                        [bbox[3], bbox[2]],
                        [bbox[1], bbox[2]],
                        [bbox[1], bbox[0]],
                    ]]
                }
                update_config("aoi_geojson", geojson)
            st.session_state["map_center"] = region_info.get("center", [41.3, 64.5])
            st.session_state["map_zoom"] = region_info.get("zoom", 6)

    elif aoi_type == "GeoJSON/KML":
        uploaded = st.file_uploader(
            "GeoJSON/KML yuklash",
            type=["geojson", "json", "kml"],
            key="uploader_geojson",
            label_visibility="collapsed",
        )
        if uploaded:
            try:
                content = uploaded.read().decode("utf-8")
                geojson_data = json.loads(content)

                if geojson_data.get("type") == "FeatureCollection":
                    geom = geojson_data["features"][0]["geometry"]
                elif geojson_data.get("type") == "Feature":
                    geom = geojson_data["geometry"]
                else:
                    geom = geojson_data

                update_config("aoi_geojson", geom)
                update_config("aoi_name", uploaded.name)
                add_log(f"GeoJSON yuklandi: {uploaded.name}", "success")
                st.success(f"Yuklandi: {uploaded.name}")

            except Exception as e:
                add_log(f"GeoJSON yuklash xatosi: {str(e)}", "error")
                st.error("Fayl formati noto'g'ri")

    elif aoi_type == "GEE Asset":
        asset_id = st.text_input(
            "GEE Asset ID",
            placeholder="projects/.../assets/my_aoi",
            key="inp_asset_id",
        )
        if asset_id:
            update_config("aoi_name", asset_id.split("/")[-1])
            st.caption("GEE ulanganida geometriya yuklanadi")

    elif aoi_type == "Chizish":
        st.info("Xaritada polygon yoki to'rtburchak chizing")
        drawn = st.session_state.get("drawn_geometry")
        if drawn:
            st.success("Geometriya chizildi")
            update_config("aoi_geojson", drawn)

    # Bufer
    buffer = st.slider(
        "Bufer (km)",
        0, 100,
        value=get_config("buffer_km", 0),
        key="sld_buffer",
    )
    update_config("buffer_km", buffer)
