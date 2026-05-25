"""
GEE ulanish bo'limi.

4 xil ulanish usuli: Token, Service Account, ADC, API Key.
"""
import streamlit as st
import json
from core.gee_auth import GEEAuthManager
from utils.log_manager import add_log


def render_connection_section():
    """GEE ulanish bo'limini ko'rsatadi."""

    connected = st.session_state.get("gee_connected", False)

    if connected:
        project = st.session_state.get("gee_project", "")
        method = st.session_state.get("gee_auth_method", "")
        st.markdown(f"""
        <div class="connection-status connected">
            <span class="status-dot green"></span>
            <span>Ulangan: <b>{project}</b></span>
            <span class="conn-method">({method})</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Uzish", key="btn_disconnect", use_container_width=True):
            GEEAuthManager.disconnect()
            st.rerun()
        return

    auth_method = st.selectbox(
        "Ulanish usuli",
        ["Token Auth", "Service Account", "ADC", "API Key"],
        key="sel_auth_method",
        label_visibility="collapsed",
    )

    if auth_method == "Token Auth":
        project_id = st.text_input(
            "Project ID",
            placeholder="ee-your-project",
            key="inp_token_project",
        )
        if st.button("Ulaning", key="btn_token_connect", use_container_width=True, type="primary"):
            if project_id:
                with st.spinner("Ulanmoqda..."):
                    success = GEEAuthManager.connect_token(project_id)
                if success:
                    st.rerun()
            else:
                st.warning("Project ID kiriting")

    elif auth_method == "Service Account":
        uploaded = st.file_uploader(
            "JSON fayl",
            type=["json"],
            key="uploader_sa_json",
            label_visibility="collapsed",
        )
        project_id = st.text_input(
            "Project ID (ixtiyoriy)",
            key="inp_sa_project",
        )
        if st.button("Tekshir va Ulan", key="btn_sa_connect", use_container_width=True, type="primary"):
            if uploaded:
                json_content = uploaded.read().decode("utf-8")
                with st.spinner("Ulanmoqda..."):
                    success = GEEAuthManager.connect_service_account(json_content, project_id or None)
                if success:
                    st.rerun()
            else:
                st.warning("JSON fayl yuklang")

    elif auth_method == "ADC":
        project_id = st.text_input(
            "Project ID",
            placeholder="ee-your-project",
            key="inp_adc_project",
        )
        if st.button("ADC bilan Ulan", key="btn_adc_connect", use_container_width=True, type="primary"):
            if project_id:
                with st.spinner("Ulanmoqda..."):
                    success = GEEAuthManager.connect_adc(project_id)
                if success:
                    st.rerun()

    elif auth_method == "API Key":
        st.caption("Faqat public dataset lar uchun")
        api_key = st.text_input(
            "API Key",
            type="password",
            key="inp_api_key",
        )
        project_id = st.text_input(
            "Project ID",
            key="inp_apikey_project",
        )
        if st.button("API Key bilan Ulan", key="btn_api_connect", use_container_width=True, type="primary"):
            if api_key and project_id:
                with st.spinner("Ulanmoqda..."):
                    success = GEEAuthManager.connect_api_key(api_key, project_id)
                if success:
                    st.rerun()
