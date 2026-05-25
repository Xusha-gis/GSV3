"""
Plotly grafiklar tab.

Time series grafik va bar chart.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config.settings import get_config


def render_charts_tab():
    """Charts tabni ko'rsatadi."""

    df = st.session_state.get("results_df")

    if df is None or df.empty:
        st.markdown(
            '<div class="placeholder-box">'
            '<p style="color:var(--text3);text-align:center;padding:40px 0;">'
            'Hisoblash tugagandan so\'ng grafik ko\'rinadi'
            '</p></div>',
            unsafe_allow_html=True,
        )
        return

    indices = get_config("selected_indices", [])

    # Time Series grafik
    _render_time_series(df, indices)

    # Bar chart
    _render_bar_chart(df, indices)


def _render_time_series(df, indices):
    """
    Time series chiziq grafik.

    Args:
        df: pd.DataFrame
        indices: list — indeks nomlari
    """
    fig = go.Figure()

    colors = ["#F5C518", "#22c55e", "#60a5fa", "#ef4444", "#a855f7", "#f59e0b", "#06b6d4"]
    time_col = "year" if "year" in df.columns else df.columns[0]

    for i, idx_name in enumerate(indices):
        col_name = f"{idx_name}_mean"
        if col_name not in df.columns:
            continue

        color = colors[i % len(colors)]

        fig.add_trace(go.Scatter(
            x=df[time_col],
            y=df[col_name],
            mode="lines+markers",
            name=idx_name,
            line=dict(color=color, width=2),
            marker=dict(size=5, color=color),
            hovertemplate=f"{idx_name}: %{{y:.4f}}<extra></extra>",
        ))

        # Trend chizig'i
        trends = st.session_state.get("trend_results", {})
        trend = trends.get(idx_name)
        if trend:
            import numpy as np
            x_vals = df[time_col].values
            y_trend = trend["slope"] * np.arange(len(x_vals)) + trend["intercept"]
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_trend,
                mode="lines",
                name=f"{idx_name} trend",
                line=dict(color=color, width=1, dash="dot"),
                showlegend=False,
                hoverinfo="skip",
            ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            title=None,
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            title=None,
        ),
        font=dict(size=10),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_bar_chart(df, indices):
    """
    So'nggi yil bar chart.

    Args:
        df: pd.DataFrame
        indices: list
    """
    if df.empty:
        return

    last_row = df.iloc[-1]
    bar_data = []

    for idx_name in indices:
        col_name = f"{idx_name}_mean"
        if col_name in last_row:
            val = last_row[col_name]
            if val is not None:
                bar_data.append({"Index": idx_name, "Value": val})

    if not bar_data:
        return

    bar_df = pd.DataFrame(bar_data)

    fig = go.Figure(go.Bar(
        x=bar_df["Value"],
        y=bar_df["Index"],
        orientation="h",
        marker_color="#F5C518",
        text=[f"{v:.4f}" for v in bar_df["Value"]],
        textposition="outside",
        textfont=dict(size=10, color="#e8e8e8"),
    ))

    time_col = "year" if "year" in df.columns else ""
    period = last_row.get(time_col, "So'nggi")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=160,
        margin=dict(l=10, r=40, t=25, b=10),
        title=dict(text=f"So'nggi davr: {period}", font=dict(size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=None),
        yaxis=dict(title=None),
        font=dict(size=10),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
