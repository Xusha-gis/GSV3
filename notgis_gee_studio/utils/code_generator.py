"""
GEE JavaScript va Python kod generatsiya.

Foydalanuvchi sozlamalari asosida tayyor GEE kod yaratadi.
"""
from config.settings import Settings
from core.indices import get_index


def generate_js_code(config):
    """
    GEE Code Editor uchun JavaScript kodi generatsiya qiladi.

    Args:
        config: dict — barcha sozlamalar

    Returns:
        str: JavaScript kod matni
    """
    sat_key = config.get("satellite", "Sentinel-2 SR Harmonized")
    sat_info = Settings.SATELLITES.get(sat_key, {})
    collection_id = sat_info.get("collection", "COPERNICUS/S2_SR_HARMONIZED")
    cloud_field = sat_info.get("cloud_field", "CLOUDY_PIXEL_PERCENTAGE")
    indices = config.get("selected_indices", ["NDVI"])
    start = config.get("start_date")
    end = config.get("end_date")
    cloud_pct = config.get("cloud_pct", 20)
    aoi_name = config.get("aoi_name", "O'zbekiston")

    start_str = start.strftime("%Y-%m-%d") if start else "2020-01-01"
    end_str = end.strftime("%Y-%m-%d") if end else "2024-12-31"

    code = f"""// ==========================================
// notGIS GEE Studio — Auto-Generated Code
// ==========================================
// Satellite: {sat_key}
// Indices: {', '.join(indices)}
// Period: {start_str} to {end_str}
// Region: {aoi_name}

// 1. Hudud belgilash
var aoi = ee.Geometry.Rectangle([/* koordinatlar */]);
Map.centerObject(aoi, 9);

// 2. Kolleksiya filtrlash
var collection = ee.ImageCollection('{collection_id}')
  .filterBounds(aoi)
  .filterDate('{start_str}', '{end_str}')"""

    if cloud_field:
        code += f"""
  .filter(ee.Filter.lt('{cloud_field}', {cloud_pct}))"""

    code += """;

print('Obraz soni:', collection.size());

// 3. Kompozit yaratish
var composite = collection.median();
"""

    for idx_name in indices:
        idx = get_index(idx_name)
        if not idx:
            continue
        sat_id = sat_info.get("id", "sentinel2")
        bands = idx.get("satellites", {}).get(sat_id, {}).get("bands", {})

        if idx_name == "NDVI" and "nir" in bands and "red" in bands:
            code += f"""
// {idx_name} — {idx['full_name']}
var {idx_name.lower()} = composite.normalizedDifference(['{bands["nir"]}', '{bands["red"]}'])
  .rename('{idx_name}');
"""
        elif idx_name == "NDWI" and "green" in bands and "nir" in bands:
            code += f"""
// {idx_name} — {idx['full_name']}
var {idx_name.lower()} = composite.normalizedDifference(['{bands["green"]}', '{bands["nir"]}'])
  .rename('{idx_name}');
"""

    palette_name = config.get("palette", "RdYlGn")
    palette = Settings.PALETTES.get(palette_name, Settings.PALETTES["RdYlGn"])
    palette_str = ", ".join([f"'{c}'" for c in palette])

    code += f"""
// 4. Vizualizatsiya
var visParams = {{
  min: {config.get('value_min', -0.2)},
  max: {config.get('value_max', 0.8)},
  palette: [{palette_str}]
}};

Map.addLayer({indices[0].lower()}, visParams, '{indices[0]}');
Map.addLayer(aoi, {{color: 'yellow'}}, 'AOI', true, 0.5);

// 5. Statistika
var stats = {indices[0].lower()}.reduceRegion({{
  reducer: ee.Reducer.mean().combine(ee.Reducer.minMax(), null, true),
  geometry: aoi,
  scale: {config.get('scale', 30)},
  maxPixels: 1e13
}});
print('{indices[0]} statistikasi:', stats);
"""
    return code


def generate_python_code(config):
    """
    geemap bilan Python kodi generatsiya qiladi.

    Args:
        config: dict — barcha sozlamalar

    Returns:
        str: Python kod matni
    """
    sat_key = config.get("satellite", "Sentinel-2 SR Harmonized")
    sat_info = Settings.SATELLITES.get(sat_key, {})
    collection_id = sat_info.get("collection", "COPERNICUS/S2_SR_HARMONIZED")
    indices = config.get("selected_indices", ["NDVI"])
    start = config.get("start_date")
    end = config.get("end_date")
    cloud_pct = config.get("cloud_pct", 20)

    start_str = start.strftime("%Y-%m-%d") if start else "2020-01-01"
    end_str = end.strftime("%Y-%m-%d") if end else "2024-12-31"

    code = f'''# ==========================================
# notGIS GEE Studio — Auto-Generated Python Code
# ==========================================
import ee
import geemap

# 1. GEE ulanish
ee.Authenticate()
ee.Initialize(project='{config.get("gee_project", "ee-your-project")}')

# 2. Hudud
aoi = ee.Geometry.Rectangle([/* koordinatlar */])

# 3. Kolleksiya
collection = (
    ee.ImageCollection('{collection_id}')
    .filterBounds(aoi)
    .filterDate('{start_str}', '{end_str}')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', {cloud_pct}))
)

print(f'Obraz soni: {{collection.size().getInfo()}}')

# 4. Kompozit
composite = collection.median()

# 5. Indekslar
'''

    for idx_name in indices:
        idx = get_index(idx_name)
        if not idx:
            continue
        sat_id = sat_info.get("id", "sentinel2")
        bands = idx.get("satellites", {}).get(sat_id, {}).get("bands", {})

        if "nir" in bands and "red" in bands:
            code += f"{idx_name.lower()} = composite.normalizedDifference(['{bands.get('nir', 'B8')}', '{bands.get('red', 'B4')}'])\n"

    code += f'''
# 6. Vizualizatsiya
Map = geemap.Map()
Map.centerObject(aoi, 9)
Map.addLayer({indices[0].lower()}, {{
    'min': {config.get('value_min', -0.2)},
    'max': {config.get('value_max', 0.8)},
    'palette': ['red', 'yellow', 'green']
}}, '{indices[0]}')
Map
'''
    return code
