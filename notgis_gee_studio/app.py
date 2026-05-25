"""
notGIS GEE Studio — Streamlit entry point, layout orchestrator.

ArcGIS Pro / QGIS darajasidagi professional desktop-like veb interfeys.
GIS mutaxassislari, tadqiqotchilar va universitetlar uchun.
"""
import streamlit as st
import os
import sys

# Loyiha ildiz papkasini sys.path ga qo'shish
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings, init_session_state
from config.themes import ThemeManager
from ui.navbar import render_navbar
from ui.statusbar import render_statusbar
from ui.layout import render_main_layout
from utils.log_manager import add_log


def configure_page():
    """Streamlit sahifa sozlamalarini belgilaydi."""
    st.set_page_config(
        page_title=Settings.APP_NAME,
        page_icon=Settings.APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "About": f"# {Settings.APP_NAME} v{Settings.APP_VERSION}\n"
                     "Professional GIS va masofadan zondlash platformasi.",
        },
    )


def load_css():
    """Global CSS ni yuklaydi."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

    # Qo'shimcha dinamik CSS (tema asosida)
    dark_mode = st.session_state.get("dark_mode", True)
    theme_css = ThemeManager.get_css_variables(dark_mode)
    st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

    # Sidebar ni butunlay yashirish
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none; }
        .stApp > header { background: transparent; }
        .block-container { padding-top: 0; padding-bottom: 0; }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Asosiy ilova funksiyasi."""

    # Sahifa sozlash
    configure_page()

    # Session state boshlash
    init_session_state()

    # CSS yuklash
    load_css()

    # Boshlang'ich log
    if len(st.session_state.get("logs", [])) == 0:
        add_log("notGIS GEE Studio ishga tushdi", "info")
        add_log("GEE ulanishini sozlang — chap panelda", "info")

    # NAVBAR
    render_navbar()

    # ASOSIY 3-PANEL LAYOUT
    render_main_layout()

    # STATUS STRIP
    st.markdown("---")
    render_statusbar()


if __name__ == "__main__":
    main()
