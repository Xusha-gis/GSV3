"""
Jadval, trend tahlil tab.

Natijalar jadvali, trend xulosa, mini statistika kartochkalari.
"""
import streamlit as st
import pandas as pd
from config.settings import get_config
from utils.formatters import format_number, format_trend_arrow


def render_stats_tab():
    """Stats tabni ko'rsatadi."""

    df = st.session_state.get("results_df")

    if df is None or df.empty:
        st.markdown(
            '<div class="placeholder-box">'
            '<p style="color:var(--text3);text-align:center;padding:40px 0;">'
            'Hisoblash natijalarini kutmoqda'
            '</p></div>',
            unsafe_allow_html=True,
        )
        return

    indices = get_config("selected_indices", [])

    # Mini statistika kartochkalari
    _render_mini_stats(df, indices)

    # Asosiy jadval
    _render_data_table(df, indices)

    # Trend tahlil
    _render_trend_analysis(indices)


def _render_mini_stats(df, indices):
    """Mini statistika kartochkalari."""

    cols = st.columns(min(len(indices), 3))

    for i, idx_name in enumerate(indices[:3]):
        col_name = f"{idx_name}_mean"
        if col_name not in df.columns:
            continue

        values = df[col_name].dropna()
        if values.empty:
            continue

        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{idx_name}</div>
                <div class="stat-value">{values.iloc[-1]:.4f}</div>
                <div class="stat-range">
                    Min: {values.min():.3f} | Max: {values.max():.3f}
                </div>
            </div>
            """, unsafe_allow_html=True)


def _render_data_table(df, indices):
    """Natijalar jadvali."""

    st.markdown('<p style="font-size:10px;color:var(--text3);margin:8px 0 2px;">NATIJALAR JADVALI</p>', unsafe_allow_html=True)

    display_cols = []
    if "year" in df.columns:
        display_cols.append("year")
    if "month" in df.columns:
        display_cols.append("month")
    if "season" in df.columns:
        display_cols.append("season")

    for idx_name in indices:
        col = f"{idx_name}_mean"
        if col in df.columns:
            display_cols.append(col)

    if display_cols:
        display_df = df[display_cols].copy()

        for col in display_df.columns:
            if col not in ("year", "month", "season"):
                display_df[col] = display_df[col].apply(
                    lambda x: f"{x:.4f}" if pd.notna(x) else "—"
                )

        rename_map = {}
        for col in display_df.columns:
            if col.endswith("_mean"):
                rename_map[col] = col.replace("_mean", "")

        display_df = display_df.rename(columns=rename_map)

        st.dataframe(
            display_df,
            use_container_width=True,
            height=200,
            hide_index=True,
        )


def _render_trend_analysis(indices):
    """Trend tahlil xulosa."""

    trends = st.session_state.get("trend_results", {})
    if not trends:
        return

    st.markdown('<p style="font-size:10px;color:var(--text3);margin:12px 0 4px;">TREND TAHLIL</p>', unsafe_allow_html=True)

    for idx_name in indices:
        trend = trends.get(idx_name)
        if not trend:
            continue

        arrow_text = format_trend_arrow(trend)

        color_map = {"up": "var(--green)", "down": "var(--red)", "stable": "var(--text2)"}
        color = color_map.get(trend["trend"], "var(--text2)")

        st.markdown(
            f'<div style="font-family:monospace;font-size:11px;color:{color};margin:2px 0;">'
            f'{idx_name}  {arrow_text}'
            f'</div>',
            unsafe_allow_html=True,
        )
