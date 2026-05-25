"""Son, sana, koordinat formatlash utilitysi."""


def format_coordinate(lat, lon, precision=6):
    """
    Koordinatni formatlaydi.

    Args:
        lat: float — kenglik
        lon: float — uzunlik
        precision: int — kasr raqamlari soni

    Returns:
        str: formatlangan koordinat
    """
    lat_dir = "N" if lat >= 0 else "S"
    lon_dir = "E" if lon >= 0 else "W"
    return f"{abs(lat):.{precision}f}°{lat_dir}  {abs(lon):.{precision}f}°{lon_dir}"


def format_number(value, precision=4):
    """
    Sonni formatlaydi.

    Args:
        value: float yoki None
        precision: int — kasr raqamlari

    Returns:
        str: formatlangan son
    """
    if value is None:
        return "—"
    return f"{value:.{precision}f}"


def format_area(sqm):
    """
    Maydonni formatlaydi (m² → ha yoki km²).

    Args:
        sqm: float — kvadrat metr

    Returns:
        str: formatlangan maydon
    """
    if sqm is None:
        return "—"
    if sqm > 1e6:
        return f"{sqm / 1e6:.2f} km²"
    if sqm > 1e4:
        return f"{sqm / 1e4:.2f} ha"
    return f"{sqm:.0f} m²"


def format_trend_arrow(trend_info):
    """
    Trend ma'lumotlarini o'qli formatda ko'rsatadi.

    Args:
        trend_info: dict — {slope, r_squared, p_value, trend}

    Returns:
        str: formatlangan trend
    """
    if not trend_info:
        return "—"

    arrow = {"up": "↑", "down": "↓", "stable": "→"}.get(trend_info["trend"], "—")
    slope = trend_info["slope"]
    r2 = trend_info["r_squared"]

    result = f"{arrow} {slope:+.4f}/yil  (R²={r2:.2f}"
    if trend_info.get("p_value") is not None:
        result += f", p={trend_info['p_value']:.3f}"
    result += ")"

    return result
