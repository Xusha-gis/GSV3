"""
Barcha hudud geometriyalari ro'yxati.

O'zbekiston viloyatlari va boshqa oldindan belgilangan hududlar.
Har bir yozuv nomi, markazi va geometriya turini o'z ichiga oladi.
"""


class AOIRegistry:
    """Oldindan belgilangan AOI hududlari."""

    REGIONS = {
        "O'zbekiston (butun)": {
            "center": [41.3, 64.5],
            "zoom": 6,
            "bbox": [37.17, 56.0, 45.59, 73.15],
        },
        "Toshkent viloyati": {
            "center": [41.26, 69.22],
            "zoom": 9,
            "bbox": [40.5, 68.5, 42.0, 70.5],
        },
        "Toshkent shahri": {
            "center": [41.30, 69.28],
            "zoom": 11,
            "bbox": [41.18, 69.10, 41.42, 69.45],
        },
        "Samarqand viloyati": {
            "center": [39.65, 66.96],
            "zoom": 9,
            "bbox": [38.8, 65.5, 40.5, 68.5],
        },
        "Buxoro viloyati": {
            "center": [40.25, 63.60],
            "zoom": 8,
            "bbox": [38.5, 61.0, 42.0, 66.0],
        },
        "Farg'ona viloyati": {
            "center": [40.38, 71.79],
            "zoom": 9,
            "bbox": [39.8, 70.5, 41.0, 72.5],
        },
        "Andijon viloyati": {
            "center": [40.78, 72.34],
            "zoom": 9,
            "bbox": [40.3, 71.5, 41.3, 73.2],
        },
        "Namangan viloyati": {
            "center": [41.0, 71.67],
            "zoom": 9,
            "bbox": [40.3, 70.5, 41.6, 72.5],
        },
        "Xorazm viloyati": {
            "center": [41.55, 60.63],
            "zoom": 9,
            "bbox": [40.8, 60.0, 42.1, 61.5],
        },
        "Navoiy viloyati": {
            "center": [42.17, 65.37],
            "zoom": 8,
            "bbox": [40.0, 62.0, 44.5, 68.0],
        },
        "Qashqadaryo viloyati": {
            "center": [38.86, 66.01],
            "zoom": 9,
            "bbox": [37.7, 64.5, 39.8, 67.5],
        },
        "Surxondaryo viloyati": {
            "center": [38.20, 67.57],
            "zoom": 9,
            "bbox": [37.2, 66.5, 39.3, 68.5],
        },
        "Jizzax viloyati": {
            "center": [40.46, 67.84],
            "zoom": 9,
            "bbox": [39.5, 66.5, 41.5, 69.0],
        },
        "Sirdaryo viloyati": {
            "center": [40.84, 68.66],
            "zoom": 9,
            "bbox": [40.2, 67.8, 41.5, 69.5],
        },
        "Qoraqalpog'iston": {
            "center": [43.0, 58.5],
            "zoom": 7,
            "bbox": [41.0, 55.5, 46.0, 62.0],
        },
    }

    @staticmethod
    def get_region_names():
        """
        Barcha hudud nomlarini qaytaradi.

        Returns:
            list: hudud nomlari
        """
        return list(AOIRegistry.REGIONS.keys())

    @staticmethod
    def get_region(name):
        """
        Berilgan hudud ma'lumotlarini qaytaradi.

        Args:
            name: str — hudud nomi

        Returns:
            dict yoki None: hudud ma'lumotlari
        """
        return AOIRegistry.REGIONS.get(name)

    @staticmethod
    def get_bbox_as_ee_geometry(name):
        """
        Hududni GEE ee.Geometry.Rectangle formatida qaytarish uchun bbox.

        Args:
            name: str — hudud nomi

        Returns:
            list: [west, south, east, north] yoki None
        """
        region = AOIRegistry.REGIONS.get(name)
        if region and "bbox" in region:
            bbox = region["bbox"]
            return [bbox[1], bbox[0], bbox[3], bbox[2]]
        return None
