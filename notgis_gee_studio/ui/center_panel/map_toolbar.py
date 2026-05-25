"""
Xarita ustidagi toolbar.

Basemap tanlash, chizish asboblari, to'liq ekran.
"""
import streamlit as st


def render_map_toolbar():
    """Xarita toolbar ni ko'rsatadi."""

    cols = st.columns([1, 1, 1, 1, 1])

    with cols[0]:
        basemap = st.selectbox(
            "Basemap",
            ["Dark", "Satellite", "OSM", "Topo"],
            index=0,
            key="sel_basemap",
            label_visibility="collapsed",
        )

    with cols[1]:
        st.caption("Draw: Xaritada chizing")

    with cols[2]:
        st.caption("Layers: " + str(len(st.session_state.get("map_layers", []))))

    with cols[3]:
        zoom = st.session_state.get("map_zoom", 6)
        st.caption(f"Zoom: {zoom}")

    with cols[4]:
        center = st.session_state.get("map_center", [41.3, 64.5])
        st.caption(f"{center[0]:.2f}°N {center[1]:.2f}°E")
