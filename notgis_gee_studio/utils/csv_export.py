"""CSV eksport utilitysi."""
import pandas as pd
import io
from utils.log_manager import add_log


def export_to_csv(df, filename="notGIS_export.csv"):
    """
    DataFrame ni CSV formatida eksport qiladi.

    Args:
        df: pd.DataFrame — eksport qilinadigan ma'lumot
        filename: str — fayl nomi

    Returns:
        bytes: CSV fayl mazmuni
    """
    if df is None or df.empty:
        add_log("Eksport uchun ma'lumot yo'q", "warning")
        return None

    try:
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False, encoding="utf-8-sig")
        content = buffer.getvalue()
        size_mb = len(content) / (1024 * 1024)
        add_log(f"CSV eksport: {filename} ({size_mb:.1f} MB)", "success")
        return content
    except Exception as e:
        add_log(f"CSV eksport xatosi: {str(e)}", "error")
        return None
