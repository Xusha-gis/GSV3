"""
Indekslar bo'limi.

Kategoriya bo'yicha guruhlangan compact checkbox list.
Maksimum 7 ta bir vaqtda tanlash mumkin.
"""
import streamlit as st
from config.settings import Settings, update_config, get_config
from core.indices import get_indices_by_category, get_available_indices_for_satellite, INDICES


def render_indices_section():
    """Indekslar bo'limini ko'rsatadi."""

    selected = list(get_config("selected_indices", []))
    satellite_key = get_config("satellite", "Sentinel-2 SR Harmonized")
    sat_info = Settings.SATELLITES.get(satellite_key, {})
    sat_id = sat_info.get("id", "sentinel2")

    available = get_available_indices_for_satellite(sat_id)

    max_indices = Settings.MAX_INDICES
    count = len(selected)

    st.markdown(
        f'<p style="font-size:10px;color:var(--text3);margin:0;">TANLANGAN: {count}/{max_indices}</p>',
        unsafe_allow_html=True,
    )

    categories = get_indices_by_category()

    for cat_name, indices_list in categories.items():
        cat_available = [idx for idx in indices_list if idx["name"] in available]
        if not cat_available:
            continue

        st.markdown(
            f'<p style="font-size:9px;color:var(--text3);letter-spacing:1px;margin:8px 0 2px;font-weight:600;">{cat_name}</p>',
            unsafe_allow_html=True,
        )

        for idx in cat_available:
            name = idx["name"]
            full = idx["full_name"]
            is_selected = name in selected
            at_limit = count >= max_indices and not is_selected

            checked = st.checkbox(
                f"{name} — {full}",
                value=is_selected,
                key=f"chk_idx_{name}",
                disabled=at_limit,
                help=idx.get("tooltip", idx.get("formula", "")),
            )

            if checked and name not in selected:
                selected.append(name)
            elif not checked and name in selected:
                selected.remove(name)

    update_config("selected_indices", selected)
