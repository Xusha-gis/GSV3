"""
Left panel orchestrator.

Barcha accordion bo'limlarni tartib bilan ko'rsatadi.
Pastda RUN tugmasi.
"""
import streamlit as st
from datetime import date
from config.settings import get_config, update_config
from utils.log_manager import add_log

from ui.left_panel.section_connection import render_connection_section
from ui.left_panel.section_satellite import render_satellite_section
from ui.left_panel.section_datetime import render_datetime_section
from ui.left_panel.section_aoi import render_aoi_section
from ui.left_panel.section_indices import render_indices_section
from ui.left_panel.section_legend import render_legend_section
from ui.left_panel.section_export_cfg import render_export_cfg_section


def render_left_panel():
    """Left panelni to'liq ko'rsatadi."""

    with st.expander("GEE ULANISH", expanded=st.session_state.get("panel_sections", {}).get("connection", True)):
        render_connection_section()

    with st.expander("SATELLITE", expanded=st.session_state.get("panel_sections", {}).get("satellite", True)):
        render_satellite_section()

    with st.expander("VAQT ORALIQ", expanded=st.session_state.get("panel_sections", {}).get("datetime", True)):
        render_datetime_section()

    with st.expander("HUDUD (AOI)", expanded=st.session_state.get("panel_sections", {}).get("aoi", True)):
        render_aoi_section()

    with st.expander("INDEKSLAR", expanded=st.session_state.get("panel_sections", {}).get("indices", True)):
        render_indices_section()

    with st.expander("LEGEND SOZLASH", expanded=st.session_state.get("panel_sections", {}).get("legend", False)):
        render_legend_section()

    with st.expander("EKSPORT SOZLASH", expanded=st.session_state.get("panel_sections", {}).get("export_cfg", False)):
        render_export_cfg_section()

    st.markdown("---")

    # RUN tugmasi
    _render_run_button()


def _render_run_button():
    """RUN tugmasini ko'rsatadi va tahlilni ishga tushiradi."""

    config = st.session_state.get("config", {})
    gee_connected = st.session_state.get("gee_connected", False)
    indices_selected = len(config.get("selected_indices", [])) > 0
    has_aoi = bool(config.get("aoi_name") or config.get("aoi_geojson"))

    can_run = indices_selected and has_aoi
    is_running = st.session_state.get("analysis_running", False)

    # Disabled sababi tooltip
    if not indices_selected:
        st.caption("Kamida 1 indeks tanlang")
    if not has_aoi:
        st.caption("Hudud tanlang")

    col1, col2 = st.columns([5, 1])

    with col1:
        run_label = "HISOBLASH (RUN)" if not is_running else "HISOBLANMOQDA..."
        if st.button(
            run_label,
            key="btn_run",
            use_container_width=True,
            type="primary",
            disabled=not can_run or is_running,
        ):
            _execute_analysis(config)

    with col2:
        if st.button("↺", key="btn_reset", help="Tozalash"):
            st.session_state["results_df"] = None
            st.session_state["map_layers"] = []
            st.session_state["last_stats"] = None
            st.session_state["trend_results"] = None
            add_log("Natijalar tozalandi", "info")
            st.rerun()


def _execute_analysis(config):
    """
    Tahlilni ishga tushiradi.

    Args:
        config: dict — barcha sozlamalar
    """
    from core.gee_analysis import TimeSeriesAnalyzer

    st.session_state["analysis_running"] = True

    time_unit = config.get("time_unit", "Yillik")
    add_log(f"Tahlil boshlandi: {time_unit}", "process")

    try:
        if time_unit == "Yillik":
            df = TimeSeriesAnalyzer.run_yearly(config)
        elif time_unit == "Oylik":
            df = TimeSeriesAnalyzer.run_monthly(config)
        else:
            df = TimeSeriesAnalyzer.run_seasonal(config)

        if df is not None and not df.empty:
            st.session_state["results_df"] = df

            # Trend hisoblash
            trends = {}
            for idx_name in config.get("selected_indices", []):
                col_name = f"{idx_name}_mean"
                if col_name in df.columns:
                    trend = TimeSeriesAnalyzer.compute_trend(df, col_name)
                    if trend:
                        trends[idx_name] = trend

            st.session_state["trend_results"] = trends
            add_log(f"Tahlil muvaffaqiyatli: {len(df)} qator", "success")
        else:
            add_log("Tahlil natija bermadi", "warning")

    except Exception as e:
        add_log(f"Tahlil xatosi: {str(e)}", "error")

    finally:
        st.session_state["analysis_running"] = False
        st.rerun()
