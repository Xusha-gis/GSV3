"""
Log tizimi — session_state asosida.

Barcha muhim operatsiyalar logga yoziladi.
Log xabarlari status strip da ko'rsatiladi.
"""
import streamlit as st
from datetime import datetime


def _ensure_logs():
    """Log ro'yxati mavjudligini tekshiradi."""
    if "logs" not in st.session_state:
        st.session_state["logs"] = []


def add_log(message, level="info"):
    """
    Yangi log xabari qo'shadi.

    Args:
        message: str — log xabari matni
        level: str — info, process, success, warning, error
    """
    _ensure_logs()

    log_entry = {
        "id": len(st.session_state["logs"]) + 1,
        "time": datetime.now().strftime("%H:%M:%S"),
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
    }

    st.session_state["logs"].append(log_entry)


def get_logs(last_n=None, level_filter=None):
    """
    Log xabarlarini qaytaradi.

    Args:
        last_n: int yoki None — oxirgi N ta log (None = hammasi)
        level_filter: str yoki None — faqat belgilangan daraja

    Returns:
        list: log yozuvlari
    """
    _ensure_logs()

    logs = st.session_state["logs"]

    if level_filter:
        if level_filter == "errors":
            logs = [l for l in logs if l["level"] in ("error", "warning")]
        else:
            logs = [l for l in logs if l["level"] == level_filter]

    if last_n:
        logs = logs[-last_n:]

    return logs


def get_log_count():
    """
    Jami log soni.

    Returns:
        int: log yozuvlari soni
    """
    _ensure_logs()
    return len(st.session_state["logs"])


def get_error_count():
    """
    Xato va ogohlantirish soni.

    Returns:
        int: xato/warning soni
    """
    _ensure_logs()
    return len([l for l in st.session_state["logs"] if l["level"] in ("error", "warning")])


def export_logs(filter_type="all"):
    """
    Log yozuvlarini TXT formatida eksport qiladi.

    Args:
        filter_type: str — all, errors

    Returns:
        str: TXT formatida log mazmuni
    """
    _ensure_logs()

    project = st.session_state.get("gee_project", "noma'lum")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "notGIS GEE Studio — Session Log",
        f"Generated: {now}",
        f"Project: {project}",
        "=" * 50,
        "",
    ]

    logs = get_logs(level_filter="errors" if filter_type == "errors" else None)
    level_map = {
        "info": "INFO    ",
        "process": "PROCESS ",
        "success": "SUCCESS ",
        "warning": "WARNING ",
        "error": "ERROR   ",
    }

    for log in logs:
        level_str = level_map.get(log["level"], "INFO    ")
        lines.append(f"[{log['time']}] {level_str} {log['message']}")

    return "\n".join(lines)


def clear_logs():
    """Barcha loglarni tozalaydi."""
    st.session_state["logs"] = []


def format_log_for_ticker(log_entry):
    """
    Log yozuvini ticker strip uchun formatlaydi.

    Args:
        log_entry: dict — log yozuvi

    Returns:
        str: formatlangan matn
    """
    icons = {
        "info": "●",
        "process": "⏳",
        "success": "✓",
        "warning": "⚠",
        "error": "✗",
    }
    icon = icons.get(log_entry["level"], "●")
    return f"[ {log_entry['time']} ] {icon} {log_entry['message']}"
