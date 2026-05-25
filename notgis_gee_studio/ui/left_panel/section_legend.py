"""
Legend va rang sozlash bo'limi.

Palitra tanlash, min/max, klassifikatsiya usuli.
"""
import streamlit as st
from config.settings import Settings, update_config, get_config


def render_legend_section():
    """Legend sozlash bo'limini ko'rsatadi."""

    palette_names = list(Settings.PALETTES.keys())
    current = get_config("palette", "RdYlGn")
    current_idx = palette_names.index(current) if current in palette_names else 0

    # Palitra tanlash — har birining rangli ko'rinishi
    for pname in palette_names:
        colors = Settings.PALETTES[pname]
        gradient = ", ".join(colors)
        is_selected = pname == current

        border_style = "2px solid var(--primary)" if is_selected else "1px solid var(--border)"
        bg = "var(--surface3)" if is_selected else "transparent"

        if st.button(
            pname,
            key=f"btn_pal_{pname}",
            use_container_width=True,
        ):
            update_config("palette", pname)
            st.rerun()

    # Min / Max
    st.markdown('<p style="font-size:10px;color:var(--text3);margin:8px 0 2px;">QIYMAT ORALIQ</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        vmin = st.number_input(
            "Min",
            value=float(get_config("value_min", -0.2)),
            step=0.1,
            key="inp_vmin",
        )
        update_config("value_min", vmin)

    with col2:
        vmax = st.number_input(
            "Max",
            value=float(get_config("value_max", 0.8)),
            step=0.1,
            key="inp_vmax",
        )
        update_config("value_max", vmax)

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Auto", key="btn_auto_range"):
            update_config("value_min", -0.2)
            update_config("value_max", 0.8)
            st.rerun()

    # Klassifikatsiya usuli
    methods = Settings.CLASSIFICATION_METHODS
    current_method = get_config("classification", methods[0])
    method_idx = methods.index(current_method) if current_method in methods else 0

    classification = st.selectbox(
        "Klassifikatsiya",
        methods,
        index=method_idx,
        key="sel_classification",
    )
    update_config("classification", classification)

    # Klass soni
    class_count = st.slider(
        "Klass soni",
        3, 10,
        value=get_config("class_count", 5),
        key="sld_class_count",
    )
    update_config("class_count", class_count)
