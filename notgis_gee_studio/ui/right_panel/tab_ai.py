"""
AI sozlash, auto-config, chat tab.

AI provider sozlash, tabiiy tilda so'rov, chat.
"""
import streamlit as st
from config.settings import Settings, update_config, get_config
from ai.ai_router import AIRouter
from ai.dashboard_agent import DashboardAgent
from utils.log_manager import add_log


def render_ai_tab():
    """AI tabni ko'rsatadi."""

    # API Sozlash
    with st.expander("API SOZLASH", expanded=False):
        _render_ai_config()

    st.markdown("---")

    # Auto-Config
    _render_auto_config()

    st.markdown("---")

    # Chat
    _render_chat()


def _render_ai_config():
    """AI provider va API key sozlash."""

    providers = list(Settings.AI_PROVIDERS.keys())

    provider = st.selectbox(
        "Provider",
        providers,
        key="sel_ai_provider",
        label_visibility="collapsed",
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        key="inp_ai_api_key",
        label_visibility="collapsed",
        placeholder=f"{provider} API Key",
    )

    models = Settings.AI_PROVIDERS.get(provider, {}).get("models", [])
    model = st.selectbox(
        "Model",
        models,
        key="sel_ai_model",
        label_visibility="collapsed",
    )

    if st.button("Saqlash", key="btn_ai_save", use_container_width=True):
        if api_key:
            st.session_state["ai_provider"] = provider
            st.session_state["ai_api_key"] = api_key
            st.session_state["ai_model"] = model

            if "ai_router" not in st.session_state:
                st.session_state["ai_router"] = AIRouter()

            st.session_state["ai_router"].configure(provider, api_key, model)
            add_log(f"AI sozlandi: {provider} / {model}", "success")
            st.success(f"{provider} sozlandi")
        else:
            st.warning("API Key kiriting")


def _render_auto_config():
    """Auto-Config — tabiiy tilda so'rov."""

    st.markdown('<p style="font-size:10px;color:var(--text3);letter-spacing:1px;margin:4px 0 2px;font-weight:600;">AI AUTO-CONFIG</p>', unsafe_allow_html=True)

    prompt = st.text_area(
        "So'rov",
        placeholder="Masalan: Xorazm viloyatida 2020-2024 yillarda NDVI va NDWI o'zgarishini ko'rsat",
        height=80,
        key="ta_ai_prompt",
        label_visibility="collapsed",
    )

    # Tez misol tugmalari
    examples = [
        "Toshkent NDVI 5 yil",
        "Farg'ona suv indeksi",
        "Buxoro yong'in tahlili",
        "Samarqand shahar kengayishi",
    ]

    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(example, key=f"btn_ai_ex_{i}", use_container_width=True):
                st.session_state["ta_ai_prompt"] = example
                st.rerun()

    if st.button("AI SOZLA", key="btn_ai_config", use_container_width=True, type="primary"):
        provider = st.session_state.get("ai_provider")
        router = st.session_state.get("ai_router")

        if not provider or not router:
            st.warning("Avval AI providerni sozlang")
            return

        if not prompt:
            st.warning("So'rov kiriting")
            return

        with st.spinner("AI tahlil qilmoqda..."):
            config = st.session_state.get("config", {})
            result = DashboardAgent.analyze_and_configure(
                prompt, router, provider, config
            )

        if result.get("action") == "configure":
            # Konfiguratsiyani qo'llash
            if "satellite" in result:
                update_config("satellite", result["satellite"])
            if "selected_indices" in result:
                update_config("selected_indices", result["selected_indices"])
            if "aoi_name" in result:
                update_config("aoi_name", result["aoi_name"])
            if "start_date" in result:
                from datetime import date as d
                try:
                    update_config("start_date", d.fromisoformat(result["start_date"]))
                except (ValueError, TypeError):
                    pass
            if "end_date" in result:
                from datetime import date as d
                try:
                    update_config("end_date", d.fromisoformat(result["end_date"]))
                except (ValueError, TypeError):
                    pass
            if "cloud_pct" in result:
                update_config("cloud_pct", result["cloud_pct"])
            if "time_unit" in result:
                update_config("time_unit", result["time_unit"])

            explanation = result.get("explanation", "Sozlandi")
            st.success(f"Dashboard sozlandi!")
            st.caption(explanation)
            add_log(f"AI auto-config: {explanation}", "success")

        elif result.get("action") == "answer":
            st.info(result.get("answer", "Javob yo'q"))
        else:
            st.info(str(result))


def _render_chat():
    """AI chat bo'limi."""

    st.markdown('<p style="font-size:10px;color:var(--text3);letter-spacing:1px;margin:4px 0 2px;font-weight:600;">CHAT</p>', unsafe_allow_html=True)

    messages = st.session_state.get("ai_messages", [])

    # Xabarlar ko'rsatish
    chat_container = st.container(height=180)
    with chat_container:
        for msg in messages[-8:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "user":
                st.markdown(f'<div class="chat-msg user">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-msg assistant">{content}</div>', unsafe_allow_html=True)

    # Chat input
    question = st.chat_input("GEE haqida so'rang...", key="chat_input")

    if question:
        provider = st.session_state.get("ai_provider")
        router = st.session_state.get("ai_router")

        if not provider or not router:
            st.warning("Avval AI providerni sozlang")
            return

        messages.append({"role": "user", "content": question})

        answer = DashboardAgent.ask_gee_question(question, router, provider)
        messages.append({"role": "assistant", "content": answer})

        st.session_state["ai_messages"] = messages
        st.rerun()
