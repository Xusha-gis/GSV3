"""
Yuqori navbar — 52px sabit balandlik.

Chapda: logotip
Markazda: loyiha nomi + GEE holati
O'ngda: CRS, mode toggle
"""
import streamlit as st
from config.settings import get_config


def render_navbar():
    """Navbar'ni ko'rsatadi."""

    gee_connected = st.session_state.get("gee_connected", False)
    gee_project = st.session_state.get("gee_project", "")
    crs = get_config("crs", "EPSG:32640")
    dark_mode = st.session_state.get("dark_mode", True)

    status_dot = "🟢" if gee_connected else "🔴"
    status_text = gee_project if gee_connected else "Ulanmagan"

    st.markdown(f"""
    <div class="notgis-navbar">
        <div class="navbar-left">
            <span class="navbar-brand">notGIS</span>
            <span class="navbar-subtitle">GEE Studio</span>
        </div>
        <div class="navbar-center">
            <span class="navbar-status">{status_dot} {status_text}</span>
        </div>
        <div class="navbar-right">
            <span class="navbar-crs">{crs}</span>
            <span class="navbar-separator">|</span>
            <span class="navbar-crs">WGS84 / UTM</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
