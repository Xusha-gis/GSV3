"""
3-panel asosiy layout boshqaruvchi.

Left (280px) | Center (flex) | Right (300px)
"""
import streamlit as st
from ui.left_panel.panel import render_left_panel
from ui.center_panel.panel import render_center_panel
from ui.right_panel.panel import render_right_panel


def render_main_layout():
    """
    Asosiy 3-panel layoutni ko'rsatadi.

    Streamlit columns yordamida 3 panel yaratiladi.
    """
    left_col, center_col, right_col = st.columns([1.2, 3, 1.3])

    with left_col:
        render_left_panel()

    with center_col:
        render_center_panel()

    with right_col:
        render_right_panel()
