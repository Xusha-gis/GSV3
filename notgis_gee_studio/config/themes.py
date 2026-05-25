"""
CSS o'zgaruvchilar va rang sistemasi.

Dark va Light mode uchun barcha rang va o'lcham o'zgaruvchilari.
"""


class ThemeManager:
    """Ilova temasini boshqaradi."""

    DARK = {
        "bg": "#090909",
        "surface": "#111111",
        "surface2": "#161616",
        "surface3": "#1c1c1c",
        "border": "#1e1e1e",
        "border2": "#2a2a2a",
        "primary": "#F5C518",
        "primary_d": "#c9a010",
        "primary_g": "rgba(245,197,24,0.08)",
        "text": "#e8e8e8",
        "text2": "#888888",
        "text3": "#444444",
        "green": "#22c55e",
        "red": "#ef4444",
        "yellow": "#f59e0b",
        "blue": "#60a5fa",
    }

    LIGHT = {
        "bg": "#f5f5f5",
        "surface": "#ffffff",
        "surface2": "#fafafa",
        "surface3": "#f0f0f0",
        "border": "#e0e0e0",
        "border2": "#d0d0d0",
        "primary": "#c9a010",
        "primary_d": "#a88500",
        "primary_g": "rgba(201,160,16,0.08)",
        "text": "#1a1a1a",
        "text2": "#666666",
        "text3": "#999999",
        "green": "#16a34a",
        "red": "#dc2626",
        "yellow": "#d97706",
        "blue": "#3b82f6",
    }

    @staticmethod
    def get_theme(dark_mode=True):
        """
        Joriy tema ranglarini qaytaradi.

        Args:
            dark_mode: bool — True = dark, False = light

        Returns:
            dict: rang o'zgaruvchilari
        """
        return ThemeManager.DARK if dark_mode else ThemeManager.LIGHT

    @staticmethod
    def get_css_variables(dark_mode=True):
        """
        CSS :root o'zgaruvchilari string ko'rinishida.

        Args:
            dark_mode: bool

        Returns:
            str: CSS o'zgaruvchilar bloki
        """
        theme = ThemeManager.get_theme(dark_mode)
        variables = []
        for key, value in theme.items():
            css_key = key.replace("_", "-")
            variables.append(f"--{css_key}: {value};")
        return ":root {\n  " + "\n  ".join(variables) + "\n}"
