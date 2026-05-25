"""
Satellite va filtr bo'limi.

Satellite manba tanlash, bulut filtri, composite usuli.
"""
import streamlit as st
from config.settings import Settings, update_config, get_config


def render_satellite_section():
    """Satellite tanlash bo'limini ko'rsatadi."""

    satellite_names = list(Settings.SATELLITES.keys())
    current_sat = get_config("satellite", satellite_names[0])
    current_idx = satellite_names.index(current_sat) if current_sat in satellite_names else 0

    satellite = st.selectbox(
        "Satellite manba",
        satellite_names,
        index=current_idx,
        key="sel_satellite",
        label_visibility="collapsed",
    )
    update_config("satellite", satellite)

    sat_info = Settings.SATELLITES.get(satellite, {})
    scale = sat_info.get("scale", 30)
    st.caption(f"Scale: {scale}m | {sat_info.get('id', '')}")

    col1, col2 = st.columns(2)

    with col1:
        if sat_info.get("cloud_field"):
            cloud = st.slider(
                "Bulut %",
                0, 100,
                value=get_config("cloud_pct", 20),
                key="sld_cloud",
            )
            update_config("cloud_pct", cloud)
        else:
            st.caption("Bulut filtri yo'q")

    with col2:
        composite = st.selectbox(
            "Composite",
            Settings.COMPOSITES,
            index=Settings.COMPOSITES.index(get_config("composite", "median")),
            key="sel_composite",
        )
        update_config("composite", composite)
