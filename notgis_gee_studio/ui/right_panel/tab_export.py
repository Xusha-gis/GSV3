"""
Eksport va import tab.

CSV, Excel, GeoTIFF eksport. GEE JS va Python kod generatsiya.
"""
import streamlit as st
from config.settings import get_config
from utils.csv_export import export_to_csv
from utils.excel_export import export_to_excel
from utils.code_generator import generate_js_code, generate_python_code
from utils.log_manager import add_log


def render_export_tab():
    """Export tabni ko'rsatadi."""

    df = st.session_state.get("results_df")
    config = st.session_state.get("config", {})
    has_data = df is not None and not df.empty

    # Import bo'limi
    st.markdown('<p style="font-size:10px;color:var(--text3);letter-spacing:1px;margin:4px 0 2px;font-weight:600;">IMPORT</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "GeoJSON/KML",
        type=["geojson", "json", "kml"],
        key="export_tab_import",
        label_visibility="collapsed",
    )

    asset_id = st.text_input(
        "GEE Asset ID",
        placeholder="projects/.../assets/...",
        key="export_tab_asset",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Eksport bo'limi
    st.markdown('<p style="font-size:10px;color:var(--text3);letter-spacing:1px;margin:4px 0 2px;font-weight:600;">EKSPORT</p>', unsafe_allow_html=True)

    if has_data:
        col1, col2 = st.columns(2)

        with col1:
            csv_data = export_to_csv(df, "notGIS_export.csv")
            if csv_data:
                st.download_button(
                    "CSV",
                    data=csv_data,
                    file_name="notGIS_export.csv",
                    mime="text/csv",
                    key="dl_csv",
                    use_container_width=True,
                )

        with col2:
            excel_data = export_to_excel(df, "notGIS_export.xlsx")
            if excel_data:
                st.download_button(
                    "Excel",
                    data=excel_data,
                    file_name="notGIS_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_excel",
                    use_container_width=True,
                )

        col3, col4 = st.columns(2)

        with col3:
            if st.button("GeoTIFF (Drive)", key="btn_geotiff", use_container_width=True):
                if st.session_state.get("gee_connected"):
                    add_log("GeoTIFF eksport — GEE ulanish kerak", "info")
                else:
                    st.warning("GEE ulangan bo'lishi kerak")

        with col4:
            if st.button("GEE Asset", key="btn_gee_asset", use_container_width=True):
                if st.session_state.get("gee_connected"):
                    add_log("GEE Asset eksport — GEE ulanish kerak", "info")
                else:
                    st.warning("GEE ulangan bo'lishi kerak")
    else:
        st.caption("Hisoblash natijasi kerak")

    st.markdown("---")

    # Kod generatsiya
    st.markdown('<p style="font-size:10px;color:var(--text3);letter-spacing:1px;margin:4px 0 2px;font-weight:600;">KOD GENERATSIYA</p>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        if st.button("GEE JavaScript", key="btn_gen_js", use_container_width=True):
            js_code = generate_js_code(config)
            st.session_state["generated_code"] = js_code
            st.session_state["code_lang"] = "javascript"
            add_log("GEE JavaScript kod generatsiya qilindi", "success")

    with col6:
        if st.button("Python", key="btn_gen_py", use_container_width=True):
            py_code = generate_python_code(config)
            st.session_state["generated_code"] = py_code
            st.session_state["code_lang"] = "python"
            add_log("Python kod generatsiya qilindi", "success")

    # Generatsiya qilingan kodni ko'rsatish
    code = st.session_state.get("generated_code")
    if code:
        lang = st.session_state.get("code_lang", "python")
        st.code(code, language=lang)

        st.download_button(
            f"Yuklab olish (.{'js' if lang == 'javascript' else 'py'})",
            data=code,
            file_name=f"notGIS_code.{'js' if lang == 'javascript' else 'py'}",
            mime="text/plain",
            key="dl_code",
            use_container_width=True,
        )
