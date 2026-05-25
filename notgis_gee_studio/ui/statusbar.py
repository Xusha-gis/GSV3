"""
Pastki status chiziq (log strip) — 28px sabit.

AutoCAD buyruq satriga o'xshash gorizontal scrolllovchi lenta.
"""
import streamlit as st
from utils.log_manager import get_logs, get_log_count, get_error_count, export_logs, format_log_for_ticker


def render_statusbar():
    """Status strip ni ko'rsatadi."""

    logs = get_logs(last_n=15)
    log_count = get_log_count()
    error_count = get_error_count()

    ticker_items = []
    for log in logs:
        level = log["level"]
        color_map = {
            "info": "var(--text3)",
            "process": "var(--blue)",
            "success": "var(--green)",
            "warning": "var(--yellow)",
            "error": "var(--red)",
        }
        color = color_map.get(level, "var(--text3)")
        text = format_log_for_ticker(log)
        ticker_items.append(f'<span style="color:{color};margin-right:32px;">{text}</span>')

    ticker_html = "  ——  ".join([format_log_for_ticker(l) for l in logs]) if logs else "notGIS GEE Studio tayyor"
    ticker_spans = " ".join(ticker_items) if ticker_items else '<span style="color:var(--text3);">notGIS GEE Studio tayyor</span>'

    error_badge = f'<span class="status-badge status-badge-error">{error_count}</span>' if error_count > 0 else ""

    st.markdown(f"""
    <div class="notgis-statusbar">
        <div class="log-ticker">
            <div class="log-ticker-inner">
                {ticker_spans}
            </div>
        </div>
        <div class="status-actions">
            <span class="status-count">{log_count} log</span>
            {error_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_log, col_err = st.columns([1, 1])
    with col_log:
        log_txt = export_logs("all")
        st.download_button(
            label="Log.txt",
            data=log_txt,
            file_name="notgis_session_log.txt",
            mime="text/plain",
            key="dl_all_logs",
            use_container_width=True,
        )
    with col_err:
        err_txt = export_logs("errors")
        st.download_button(
            label="Xatolar.txt",
            data=err_txt,
            file_name="notgis_errors_log.txt",
            mime="text/plain",
            key="dl_err_logs",
            use_container_width=True,
        )
