"""
Xarita panel orchestrator.

Toolbar + Folium xarita + pastki info.
"""
import streamlit as st
from ui.center_panel.map_toolbar import render_map_toolbar
from ui.center_panel.map_widget import render_map
from config.settings import get_config


def render_center_panel():
    """Markaz panelni to'liq ko'rsatadi."""

    render_map_toolbar()
    render_map()

    # Pastki info chiziq
    crs = get_config("crs", "EPSG:32640")
    center = st.session_state.get("map_center", [41.3, 64.5])
    zoom = st.session_state.get("map_zoom", 6)

    st.markdown(
        f'<div class="map-info-bar">'
        f'<span>📍 {center[0]:.6f}°N  {center[1]:.6f}°E</span>'
        f'<span>Zoom: {zoom}</span>'
        f'<span>CRS: {crs}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
