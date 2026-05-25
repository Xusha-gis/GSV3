"""
Eksport sozlamalari bo'limi.

Scale, CRS, Drive papka, maxPixels.
"""
import streamlit as st
from config.settings import Settings, update_config, get_config


def render_export_cfg_section():
    """Eksport sozlamalari bo'limini ko'rsatadi."""

    col1, col2 = st.columns(2)

    with col1:
        scales = Settings.EXPORT_SCALES
        current_scale = get_config("scale", 30)
        scale_idx = scales.index(current_scale) if current_scale in scales else 1

        scale = st.selectbox(
            "Scale (m)",
            scales,
            index=scale_idx,
            key="sel_export_scale",
        )
        update_config("scale", scale)

    with col2:
        crs_options = list(Settings.CRS_OPTIONS.keys())
        current_crs = get_config("crs", "EPSG:32640")
        crs_idx = crs_options.index(current_crs) if current_crs in crs_options else 0

        crs = st.selectbox(
            "CRS",
            crs_options,
            index=crs_idx,
            key="sel_export_crs",
            format_func=lambda x: f"{x} ({Settings.CRS_OPTIONS[x][:12]})",
        )
        update_config("crs", crs)

    folder = st.text_input(
        "Drive papka",
        value=get_config("drive_folder", "notGIS_exports"),
        key="inp_drive_folder",
    )
    update_config("drive_folder", folder)

    max_px = st.text_input(
        "maxPixels",
        value=str(int(get_config("max_pixels", 1e13))),
        key="inp_max_pixels",
    )
    try:
        update_config("max_pixels", float(max_px))
    except ValueError:
        pass
