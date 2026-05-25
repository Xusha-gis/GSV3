"""
Right panel orchestrator.

4 tab: Charts, Stats, Export, AI.
"""
import streamlit as st
from ui.right_panel.tab_charts import render_charts_tab
from ui.right_panel.tab_stats import render_stats_tab
from ui.right_panel.tab_export import render_export_tab
from ui.right_panel.tab_ai import render_ai_tab


def render_right_panel():
    """O'ng panelni to'liq ko'rsatadi."""

    tab_charts, tab_stats, tab_export, tab_ai = st.tabs([
        "Charts",
        "Stats",
        "Export",
        "AI",
    ])

    with tab_charts:
        render_charts_tab()

    with tab_stats:
        render_stats_tab()

    with tab_export:
        render_export_tab()

    with tab_ai:
        render_ai_tab()
