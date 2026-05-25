"""Excel eksport utilitysi."""
import pandas as pd
import io
from utils.log_manager import add_log


def export_to_excel(df, filename="notGIS_export.xlsx", sheet_name="Results"):
    """
    DataFrame ni Excel formatida eksport qiladi.

    Args:
        df: pd.DataFrame — eksport qilinadigan ma'lumot
        filename: str — fayl nomi
        sheet_name: str — varaq nomi

    Returns:
        bytes: Excel fayl mazmuni
    """
    if df is None or df.empty:
        add_log("Eksport uchun ma'lumot yo'q", "warning")
        return None

    try:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        content = buffer.getvalue()
        size_mb = len(content) / (1024 * 1024)
        add_log(f"Excel eksport: {filename} ({size_mb:.1f} MB)", "success")
        return content
    except Exception as e:
        add_log(f"Excel eksport xatosi: {str(e)}", "error")
        return None
