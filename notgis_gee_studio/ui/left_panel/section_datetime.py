"""
Vaqt oralig'i bo'limi.

Boshlanish/tugash sanasi, vaqt bo'limi, tez tanlash tugmalari.
"""
import streamlit as st
from datetime import date, timedelta
from config.settings import Settings, update_config, get_config


def render_datetime_section():
    """Vaqt oralig'i bo'limini ko'rsatadi."""

    col1, col2 = st.columns(2)
    today = date.today()

    with col1:
        start = st.date_input(
            "Boshlanish",
            value=get_config("start_date", today - timedelta(days=1825)),
            key="dt_start",
        )
        update_config("start_date", start)

    with col2:
        end = st.date_input(
            "Tugash",
            value=get_config("end_date", today),
            key="dt_end",
        )
        update_config("end_date", end)

    if start >= end:
        st.markdown('<p style="color:var(--red);font-size:11px;">Boshlanish sanasi tugash sanasidan oldin bo\'lishi kerak</p>', unsafe_allow_html=True)

    st.markdown('<p style="font-size:10px;color:var(--text3);margin:4px 0 2px;">TEZ TANLASH</p>', unsafe_allow_html=True)

    cols = st.columns(len(Settings.QUICK_DATE_OPTIONS))
    for i, (label, years) in enumerate(Settings.QUICK_DATE_OPTIONS.items()):
        with cols[i]:
            if st.button(label, key=f"btn_quick_{label}", use_container_width=True):
                new_start = today - timedelta(days=365 * years)
                update_config("start_date", new_start)
                update_config("end_date", today)
                st.rerun()

    time_units = Settings.TIME_UNITS
    current_unit = get_config("time_unit", "Yillik")
    current_idx = time_units.index(current_unit) if current_unit in time_units else 0

    time_unit = st.radio(
        "Vaqt bo'limi",
        time_units,
        index=current_idx,
        horizontal=True,
        key="radio_time_unit",
        label_visibility="collapsed",
    )
    update_config("time_unit", time_unit)
