"""
20+ indeks metadata va formulalar.

Har bir indeks uchun nomi, formulasi, satellite bandlari,
qiymat oralig'i va vizualizatsiya sozlamalari.
"""

INDICES = {
    # ==================== VEGETATSIYA ====================
    "NDVI": {
        "name": "NDVI",
        "full_name": "Normalized Difference Vegetation Index",
        "category": "vegetation",
        "formula": "(NIR - Red) / (NIR + Red)",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "red": "B4"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "red": "SR_B4"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "red": "SR_B3"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.2, "max": 0.8},
        "default_palette": "RdYlGn",
        "description": "O'simlik zichligi va sog'lig'ini o'lchaydi",
        "unit": "",
        "tooltip": "Yaxshi vegetatsiya: 0.6-0.9. Quruq tuproq: 0-0.1. Suv: <0",
    },
    "EVI": {
        "name": "EVI",
        "full_name": "Enhanced Vegetation Index",
        "category": "vegetation",
        "formula": "2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "red": "B4", "blue": "B2"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "red": "SR_B4", "blue": "SR_B2"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "red": "SR_B3", "blue": "SR_B1"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.2, "max": 0.8},
        "default_palette": "RdYlGn",
        "description": "Yaxshilangan vegetatsiya indeksi, atmosfera ta'sirini kamaytiradi",
        "unit": "",
        "tooltip": "NDVI ga o'xshash, lekin atmosfera va tuproq ta'sirini kamroq sezadi",
    },
    "SAVI": {
        "name": "SAVI",
        "full_name": "Soil Adjusted Vegetation Index",
        "category": "vegetation",
        "formula": "1.5 * (NIR - Red) / (NIR + Red + 0.5)",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "red": "B4"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "red": "SR_B4"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "red": "SR_B3"}, "scale": 30},
        },
        "value_range": {"min": -1.5, "max": 1.5},
        "display_range": {"min": -0.2, "max": 0.8},
        "default_palette": "RdYlGn",
        "description": "Tuproq ta'sirini hisobga oladigan vegetatsiya indeksi",
        "unit": "",
        "tooltip": "Kam vegetatsiyali hududlarda NDVI dan aniqroq natija beradi",
    },
    "GNDVI": {
        "name": "GNDVI",
        "full_name": "Green Normalized Difference Vegetation Index",
        "category": "vegetation",
        "formula": "(NIR - Green) / (NIR + Green)",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "green": "B3"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "green": "SR_B3"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "green": "SR_B2"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.2, "max": 0.8},
        "default_palette": "Greens",
        "description": "Xlorofil konsentratsiyasini o'lchaydi",
        "unit": "",
        "tooltip": "Xlorofil darajasini baholashda NDVI dan yaxshiroq",
    },
    "MSAVI": {
        "name": "MSAVI",
        "full_name": "Modified Soil Adjusted Vegetation Index",
        "category": "vegetation",
        "formula": "(2*NIR + 1 - sqrt((2*NIR+1)^2 - 8*(NIR-Red))) / 2",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "red": "B4"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "red": "SR_B4"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "red": "SR_B3"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.2, "max": 0.8},
        "default_palette": "RdYlGn",
        "description": "SAVI ning yaxshilangan versiyasi",
        "unit": "",
        "tooltip": "Tuproq yorqinligi avtomatik hisobga olinadi",
    },
    "ARVI": {
        "name": "ARVI",
        "full_name": "Atmospherically Resistant Vegetation Index",
        "category": "vegetation",
        "formula": "(NIR - (2*Red - Blue)) / (NIR + (2*Red - Blue))",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "red": "B4", "blue": "B2"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "red": "SR_B4", "blue": "SR_B2"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "red": "SR_B3", "blue": "SR_B1"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.2, "max": 0.8},
        "default_palette": "RdYlGn",
        "description": "Atmosfera ta'siriga chidamli vegetatsiya indeksi",
        "unit": "",
        "tooltip": "Aerozol ta'sirini kompensatsiya qiladi",
    },

    # ==================== SUV / NAMLIK ====================
    "NDWI": {
        "name": "NDWI",
        "full_name": "Normalized Difference Water Index",
        "category": "water",
        "formula": "(Green - NIR) / (Green + NIR)",
        "satellites": {
            "sentinel2": {"bands": {"green": "B3", "nir": "B8"}, "scale": 10},
            "landsat89": {"bands": {"green": "SR_B3", "nir": "SR_B5"}, "scale": 30},
            "landsat57": {"bands": {"green": "SR_B2", "nir": "SR_B4"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.5, "max": 0.5},
        "default_palette": "Blues",
        "description": "Suv ob'ektlarini aniqlaydi",
        "unit": "",
        "tooltip": "Suv: >0.3. O'simlik: <0. Quruq tuproq: <-0.2",
    },
    "MNDWI": {
        "name": "MNDWI",
        "full_name": "Modified Normalized Difference Water Index",
        "category": "water",
        "formula": "(Green - SWIR) / (Green + SWIR)",
        "satellites": {
            "sentinel2": {"bands": {"green": "B3", "swir": "B11"}, "scale": 20},
            "landsat89": {"bands": {"green": "SR_B3", "swir": "SR_B6"}, "scale": 30},
            "landsat57": {"bands": {"green": "SR_B2", "swir": "SR_B5"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.5, "max": 0.5},
        "default_palette": "Blues",
        "description": "Shaharlardagi suv ob'ektlarini yaxshiroq aniqlaydi",
        "unit": "",
        "tooltip": "NDWI dan yaxshiroq — qurilish hududlaridan suv ajratadi",
    },
    "LSWI": {
        "name": "LSWI",
        "full_name": "Land Surface Water Index",
        "category": "water",
        "formula": "(NIR - SWIR) / (NIR + SWIR)",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "swir": "B11"}, "scale": 20},
            "landsat89": {"bands": {"nir": "SR_B5", "swir": "SR_B6"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "swir": "SR_B5"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.5, "max": 0.5},
        "default_palette": "Blues",
        "description": "Yer yuzasi namligini o'lchaydi",
        "unit": "",
        "tooltip": "O'simlik va tuproq namligini baholaydi",
    },
    "AWEIsh": {
        "name": "AWEIsh",
        "full_name": "Automated Water Extraction Index (shadow)",
        "category": "water",
        "formula": "Blue + 2.5*Green - 1.5*(NIR+SWIR1) - 0.25*SWIR2",
        "satellites": {
            "sentinel2": {"bands": {"blue": "B2", "green": "B3", "nir": "B8", "swir1": "B11", "swir2": "B12"}, "scale": 20},
            "landsat89": {"bands": {"blue": "SR_B2", "green": "SR_B3", "nir": "SR_B5", "swir1": "SR_B6", "swir2": "SR_B7"}, "scale": 30},
        },
        "value_range": {"min": -5, "max": 5},
        "display_range": {"min": -1, "max": 1},
        "default_palette": "Blues",
        "description": "Soya hududlardagi suvni aniqlaydi",
        "unit": "",
        "tooltip": "Tog'li va shaharlardagi soya tushgan suv ob'ektlari uchun",
    },

    # ==================== HARORAT ====================
    "LST": {
        "name": "LST",
        "full_name": "Land Surface Temperature",
        "category": "temperature",
        "formula": "Thermal Band → Brightness Temp → Emissivity Correction",
        "satellites": {
            "landsat89": {"bands": {"thermal": "ST_B10"}, "scale": 100},
            "landsat57": {"bands": {"thermal": "ST_B6"}, "scale": 120},
        },
        "value_range": {"min": -20, "max": 60},
        "display_range": {"min": 10, "max": 50},
        "default_palette": "YlOrRd",
        "description": "Yer yuzasi harorati (°C)",
        "unit": "°C",
        "tooltip": "Landsat termal bandidan hisoblandi. Kelvin -> Celsius",
    },

    # ==================== TUPROQ ====================
    "BSI": {
        "name": "BSI",
        "full_name": "Bare Soil Index",
        "category": "soil",
        "formula": "((SWIR+Red) - (NIR+Blue)) / ((SWIR+Red) + (NIR+Blue))",
        "satellites": {
            "sentinel2": {"bands": {"swir": "B11", "red": "B4", "nir": "B8", "blue": "B2"}, "scale": 20},
            "landsat89": {"bands": {"swir": "SR_B6", "red": "SR_B4", "nir": "SR_B5", "blue": "SR_B2"}, "scale": 30},
            "landsat57": {"bands": {"swir": "SR_B5", "red": "SR_B3", "nir": "SR_B4", "blue": "SR_B1"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.3, "max": 0.5},
        "default_palette": "YlOrRd",
        "description": "Ochiq tuproq hududlarini aniqlaydi",
        "unit": "",
        "tooltip": "Yuqori qiymat = ochiq tuproq. Past qiymat = o'simlik/suv",
    },
    "NDTI": {
        "name": "NDTI",
        "full_name": "Normalized Difference Tillage Index",
        "category": "soil",
        "formula": "(SWIR1 - SWIR2) / (SWIR1 + SWIR2)",
        "satellites": {
            "sentinel2": {"bands": {"swir1": "B11", "swir2": "B12"}, "scale": 20},
            "landsat89": {"bands": {"swir1": "SR_B6", "swir2": "SR_B7"}, "scale": 30},
            "landsat57": {"bands": {"swir1": "SR_B5", "swir2": "SR_B7"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.3, "max": 0.3},
        "default_palette": "YlOrRd",
        "description": "Tuproq ishlov berish (haydash) indeksi",
        "unit": "",
        "tooltip": "Ekin qoldiqlarini va haydalgan tuproqni farqlaydi",
    },

    # ==================== YONG'IN ====================
    "NBR": {
        "name": "NBR",
        "full_name": "Normalized Burn Ratio",
        "category": "fire",
        "formula": "(NIR - SWIR2) / (NIR + SWIR2)",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "swir2": "B12"}, "scale": 20},
            "landsat89": {"bands": {"nir": "SR_B5", "swir2": "SR_B7"}, "scale": 30},
            "landsat57": {"bands": {"nir": "SR_B4", "swir2": "SR_B7"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.5, "max": 0.5},
        "default_palette": "RdYlGn",
        "description": "Yong'in ta'sirlangan hududlarni aniqlaydi",
        "unit": "",
        "tooltip": "Past qiymat = kuchli yongan hudud",
    },
    "dNBR": {
        "name": "dNBR",
        "full_name": "delta Normalized Burn Ratio",
        "category": "fire",
        "formula": "NBR_pre - NBR_post",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "swir2": "B12"}, "scale": 20},
            "landsat89": {"bands": {"nir": "SR_B5", "swir2": "SR_B7"}, "scale": 30},
        },
        "value_range": {"min": -2, "max": 2},
        "display_range": {"min": -0.5, "max": 1.0},
        "default_palette": "RdYlGn",
        "description": "Yong'in og'irligi (pre-fire vs post-fire)",
        "unit": "",
        "tooltip": "Yuqori qiymat = og'ir yong'in zararlanishi",
    },

    # ==================== SHAHAR ====================
    "NDBI": {
        "name": "NDBI",
        "full_name": "Normalized Difference Built-up Index",
        "category": "urban",
        "formula": "(SWIR - NIR) / (SWIR + NIR)",
        "satellites": {
            "sentinel2": {"bands": {"swir": "B11", "nir": "B8"}, "scale": 20},
            "landsat89": {"bands": {"swir": "SR_B6", "nir": "SR_B5"}, "scale": 30},
            "landsat57": {"bands": {"swir": "SR_B5", "nir": "SR_B4"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.3, "max": 0.3},
        "default_palette": "YlOrRd",
        "description": "Qurilish hududlarini aniqlaydi",
        "unit": "",
        "tooltip": "Yuqori qiymat = qurilish va beton hududlar",
    },
    "UI": {
        "name": "UI",
        "full_name": "Urban Index",
        "category": "urban",
        "formula": "(SWIR2 - NIR) / (SWIR2 + NIR)",
        "satellites": {
            "sentinel2": {"bands": {"swir2": "B12", "nir": "B8"}, "scale": 20},
            "landsat89": {"bands": {"swir2": "SR_B7", "nir": "SR_B5"}, "scale": 30},
            "landsat57": {"bands": {"swir2": "SR_B7", "nir": "SR_B4"}, "scale": 30},
        },
        "value_range": {"min": -1, "max": 1},
        "display_range": {"min": -0.3, "max": 0.3},
        "default_palette": "YlOrRd",
        "description": "Urbanizatsiya darajasini o'lchaydi",
        "unit": "",
        "tooltip": "NDBI ga o'xshash, lekin SWIR2 bandini ishlatadi",
    },

    # ==================== IQLIM ====================
    "VCI": {
        "name": "VCI",
        "full_name": "Vegetation Condition Index",
        "category": "climate",
        "formula": "(NDVI - NDVI_min) / (NDVI_max - NDVI_min) * 100",
        "satellites": {
            "sentinel2": {"bands": {"nir": "B8", "red": "B4"}, "scale": 10},
            "landsat89": {"bands": {"nir": "SR_B5", "red": "SR_B4"}, "scale": 30},
        },
        "value_range": {"min": 0, "max": 100},
        "display_range": {"min": 0, "max": 100},
        "default_palette": "RdYlGn",
        "description": "Vegetatsiya holati indeksi (qurg'oqchilik)",
        "unit": "%",
        "tooltip": "<40% = qurg'oqchilik. >60% = yaxshi holat",
    },
    "TCI": {
        "name": "TCI",
        "full_name": "Temperature Condition Index",
        "category": "climate",
        "formula": "(LST_max - LST) / (LST_max - LST_min) * 100",
        "satellites": {
            "landsat89": {"bands": {"thermal": "ST_B10"}, "scale": 100},
            "landsat57": {"bands": {"thermal": "ST_B6"}, "scale": 120},
        },
        "value_range": {"min": 0, "max": 100},
        "display_range": {"min": 0, "max": 100},
        "default_palette": "RdBu",
        "description": "Harorat holati indeksi",
        "unit": "%",
        "tooltip": "<40% = issiq stress. >60% = normal",
    },
}

# Kategoriya nomlari (ko'rsatish uchun)
CATEGORIES = {
    "vegetation": "VEGETATSIYA",
    "water": "SUV / NAMLIK",
    "temperature": "HARORAT",
    "soil": "TUPROQ",
    "fire": "YONG'IN",
    "urban": "SHAHAR",
    "climate": "IQLIM",
}

# Kategoriya tartibi
CATEGORY_ORDER = ["vegetation", "water", "temperature", "soil", "fire", "urban", "climate"]


def get_indices_by_category():
    """
    Indekslarni kategoriya bo'yicha guruhlangan dict qaytaradi.

    Returns:
        dict: {category_name: [index_dict, ...]}
    """
    result = {}
    for cat in CATEGORY_ORDER:
        cat_name = CATEGORIES[cat]
        result[cat_name] = []
        for idx_name, idx_data in INDICES.items():
            if idx_data["category"] == cat:
                result[cat_name].append(idx_data)
    return result


def get_index(name):
    """
    Berilgan nomdagi indeks ma'lumotlarini qaytaradi.

    Args:
        name: str — indeks nomi (NDVI, NDWI va hokazo)

    Returns:
        dict yoki None: indeks ma'lumotlari
    """
    return INDICES.get(name)


def get_available_indices_for_satellite(satellite_id):
    """
    Berilgan satellite uchun mavjud indekslar ro'yxatini qaytaradi.

    Args:
        satellite_id: str — sentinel2, landsat89, va hokazo

    Returns:
        list: mavjud indeks nomlari
    """
    available = []
    for idx_name, idx_data in INDICES.items():
        if satellite_id in idx_data.get("satellites", {}):
            available.append(idx_name)
    return available
