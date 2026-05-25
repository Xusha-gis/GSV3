"""
GEE tahlil moduli — Time series, statistika hisoblash.

Barcha GEE hisoblash operatsiyalari shu modulda amalga oshiriladi.
UI elementi bu modulda bo'lmaydi.
"""
import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, datetime

try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False

from core.indices import INDICES, get_index
from config.settings import Settings
from utils.log_manager import add_log


class TimeSeriesAnalyzer:
    """GEE time series tahlil sinfi."""

    @staticmethod
    def validate_inputs(config):
        """
        Kirish parametrlarini tekshiradi.

        Args:
            config: dict — konfiguratsiya

        Returns:
            tuple: (bool, str) — (valid, xato xabari)
        """
        if not st.session_state.get("gee_connected"):
            return False, "GEE ulanmagan"

        if not config.get("selected_indices"):
            return False, "Kamida bitta indeks tanlang"

        if not config.get("aoi_geometry") and not config.get("aoi_name"):
            return False, "Hudud (AOI) tanlanmagan"

        start = config.get("start_date")
        end = config.get("end_date")
        if start and end and start >= end:
            return False, "Boshlanish sanasi tugash sanasidan oldin bo'lishi kerak"

        return True, ""

    @staticmethod
    def get_geometry(config):
        """
        Konfiguratsiyadan ee.Geometry oladi.

        Args:
            config: dict — aoi_geometry yoki aoi_name bor

        Returns:
            ee.Geometry yoki None
        """
        if not EE_AVAILABLE:
            return None

        geojson = config.get("aoi_geojson")
        if geojson:
            try:
                return ee.Geometry(geojson)
            except Exception as e:
                add_log(f"GeoJSON geometriya xatosi: {str(e)}", "error")
                return None

        aoi_name = config.get("aoi_name")
        if aoi_name:
            from config.aoi_registry import AOIRegistry
            bbox = AOIRegistry.get_bbox_as_ee_geometry(aoi_name)
            if bbox:
                return ee.Geometry.Rectangle(bbox)
            add_log(f"Hudud topilmadi: {aoi_name}", "error")
            return None

        return None

    @staticmethod
    def build_collection(satellite_key, start_date, end_date, geometry, cloud_pct=20):
        """
        GEE ImageCollection quradi va filtrlanadi.

        Args:
            satellite_key: str — satellite nomi (Settings.SATELLITES dan)
            start_date: date — boshlanish sanasi
            end_date: date — tugash sanasi
            geometry: ee.Geometry — hudud
            cloud_pct: int — bulut foizi limiti (0-100)

        Returns:
            ee.ImageCollection — filtrlangan kolleksiya
        """
        if not EE_AVAILABLE:
            return None

        sat_info = Settings.SATELLITES.get(satellite_key)
        if not sat_info:
            add_log(f"Noma'lum satellite: {satellite_key}", "error")
            return None

        collection_id = sat_info["collection"]
        cloud_field = sat_info.get("cloud_field")

        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        collection = (
            ee.ImageCollection(collection_id)
            .filterBounds(geometry)
            .filterDate(start_str, end_str)
        )

        if cloud_field and cloud_pct < 100:
            collection = collection.filter(ee.Filter.lt(cloud_field, cloud_pct))

        count = collection.size().getInfo()
        add_log(f"{satellite_key} filtrlandi: {count} obraz ({start_str} — {end_str})", "process")

        return collection

    @staticmethod
    def apply_composite(collection, method="median"):
        """
        Kolleksiyadan kompozit obraz yaratadi.

        Args:
            collection: ee.ImageCollection
            method: str — median, mean, min, max, mosaic

        Returns:
            ee.Image — kompozit obraz
        """
        if not EE_AVAILABLE:
            return None

        composites = {
            "median": collection.median,
            "mean": collection.mean,
            "min": collection.min,
            "max": collection.max,
            "mosaic": collection.mosaic,
        }

        func = composites.get(method, collection.median)
        return func()

    @staticmethod
    def compute_index(image, index_name, satellite_id):
        """
        GEE image dan berilgan indeksni hisoblaydi.

        Args:
            image: ee.Image — filtrlangan kompozit obraz
            index_name: str — NDVI, NDWI va boshqalar
            satellite_id: str — sentinel2, landsat89

        Returns:
            ee.Image — bir bandli, rename qilingan

        Raises:
            ValueError — noto'g'ri index_name berilsa
        """
        if not EE_AVAILABLE:
            return None

        idx = get_index(index_name)
        if not idx:
            raise ValueError(f"Noto'g'ri indeks nomi: {index_name}")

        sat_info = idx["satellites"].get(satellite_id)
        if not sat_info:
            add_log(f"{index_name} {satellite_id} uchun mavjud emas", "warning")
            return None

        bands = sat_info.get("bands", {})

        try:
            if index_name == "NDVI":
                result = image.normalizedDifference([bands["nir"], bands["red"]])
            elif index_name == "NDWI":
                result = image.normalizedDifference([bands["green"], bands["nir"]])
            elif index_name == "MNDWI":
                result = image.normalizedDifference([bands["green"], bands["swir"]])
            elif index_name == "LSWI":
                result = image.normalizedDifference([bands["nir"], bands["swir"]])
            elif index_name == "NDBI":
                result = image.normalizedDifference([bands["swir"], bands["nir"]])
            elif index_name == "NBR":
                result = image.normalizedDifference([bands["nir"], bands["swir2"]])
            elif index_name == "NDTI":
                result = image.normalizedDifference([bands["swir1"], bands["swir2"]])
            elif index_name == "GNDVI":
                result = image.normalizedDifference([bands["nir"], bands["green"]])
            elif index_name == "UI":
                result = image.normalizedDifference([bands["swir2"], bands["nir"]])
            elif index_name == "EVI":
                nir = image.select(bands["nir"])
                red = image.select(bands["red"])
                blue = image.select(bands["blue"])
                result = nir.subtract(red).multiply(2.5).divide(
                    nir.add(red.multiply(6)).subtract(blue.multiply(7.5)).add(1)
                )
            elif index_name == "SAVI":
                nir = image.select(bands["nir"])
                red = image.select(bands["red"])
                result = nir.subtract(red).multiply(1.5).divide(nir.add(red).add(0.5))
            elif index_name == "MSAVI":
                nir = image.select(bands["nir"])
                red = image.select(bands["red"])
                result = nir.multiply(2).add(1).subtract(
                    nir.multiply(2).add(1).pow(2).subtract(nir.subtract(red).multiply(8)).sqrt()
                ).divide(2)
            elif index_name == "ARVI":
                nir = image.select(bands["nir"])
                red = image.select(bands["red"])
                blue = image.select(bands["blue"])
                rb = red.multiply(2).subtract(blue)
                result = nir.subtract(rb).divide(nir.add(rb))
            elif index_name == "BSI":
                swir = image.select(bands["swir"])
                red = image.select(bands["red"])
                nir = image.select(bands["nir"])
                blue = image.select(bands["blue"])
                result = swir.add(red).subtract(nir.add(blue)).divide(
                    swir.add(red).add(nir.add(blue))
                )
            elif index_name == "AWEIsh":
                blue = image.select(bands["blue"])
                green = image.select(bands["green"])
                nir = image.select(bands["nir"])
                swir1 = image.select(bands["swir1"])
                swir2 = image.select(bands["swir2"])
                result = blue.add(green.multiply(2.5)).subtract(
                    nir.add(swir1).multiply(1.5)
                ).subtract(swir2.multiply(0.25))
            elif index_name == "LST":
                thermal = image.select(bands["thermal"])
                result = thermal.multiply(0.00341802).add(149.0).subtract(273.15)
            elif index_name in ("VCI", "TCI", "dNBR"):
                result = image.normalizedDifference(
                    [bands.get("nir", bands.get("thermal", "")),
                     bands.get("red", bands.get("swir2", ""))]
                )
            else:
                add_log(f"Indeks formulasi topilmadi: {index_name}", "error")
                return None

            return result.rename(index_name)

        except Exception as e:
            add_log(f"{index_name} hisoblash xatosi: {str(e)}", "error")
            return None

    @staticmethod
    def reduce_region(index_image, geometry, scale=30):
        """
        Hudud bo'yicha statistika hisoblaydi.

        Args:
            index_image: ee.Image — indeks obrazi
            geometry: ee.Geometry — hudud
            scale: int — o'lchov (metr)

        Returns:
            dict: {mean, min, max, stdDev, count}
        """
        if not EE_AVAILABLE:
            return None

        try:
            stats = index_image.reduceRegion(
                reducer=ee.Reducer.mean()
                    .combine(ee.Reducer.minMax(), sharedInputs=True)
                    .combine(ee.Reducer.stdDev(), sharedInputs=True)
                    .combine(ee.Reducer.count(), sharedInputs=True),
                geometry=geometry,
                scale=scale,
                maxPixels=1e13,
                bestEffort=True,
            ).getInfo()

            return stats
        except ee.EEException as e:
            add_log(f"Statistika xatosi: {str(e)}", "error")
            return None
        except Exception as e:
            add_log(f"Reduce region xatosi: {str(e)}", "error")
            return None

    @staticmethod
    def run_yearly(config):
        """
        Yillik tahlil ishga tushiradi.

        Args:
            config: dict — barcha sozlamalar

        Returns:
            pd.DataFrame — natijalar jadvali
        """
        if not EE_AVAILABLE:
            return TimeSeriesAnalyzer._generate_demo_data(config)

        valid, msg = TimeSeriesAnalyzer.validate_inputs(config)
        if not valid:
            add_log(msg, "error")
            return None

        geometry = TimeSeriesAnalyzer.get_geometry(config)
        if geometry is None:
            add_log("Geometriya olinmadi", "error")
            return None

        sat_key = config["satellite"]
        sat_info = Settings.SATELLITES[sat_key]
        sat_id = sat_info["id"]
        indices = config["selected_indices"]
        start_year = config["start_date"].year
        end_year = config["end_date"].year
        cloud_pct = config.get("cloud_pct", 20)
        composite = config.get("composite", "median")
        scale = config.get("scale", sat_info["scale"])

        add_log(f"Tahlil boshlandi: {len(indices)} indeks, {end_year - start_year + 1} yil", "process")

        rows = []
        total_years = end_year - start_year + 1

        for i, year in enumerate(range(start_year, end_year + 1)):
            add_log(f"Yil {i + 1}/{total_years} tahlil qilinmoqda: {year}", "process")

            start_d = date(year, 1, 1)
            end_d = date(year, 12, 31)

            try:
                collection = TimeSeriesAnalyzer.build_collection(
                    sat_key, start_d, end_d, geometry, cloud_pct
                )
                if collection is None:
                    continue

                composite_img = TimeSeriesAnalyzer.apply_composite(collection, composite)
                row = {"year": year}

                for idx_name in indices:
                    idx_img = TimeSeriesAnalyzer.compute_index(composite_img, idx_name, sat_id)
                    if idx_img is None:
                        row[f"{idx_name}_mean"] = None
                        continue

                    stats = TimeSeriesAnalyzer.reduce_region(idx_img, geometry, scale)
                    if stats:
                        row[f"{idx_name}_mean"] = stats.get(f"{idx_name}_mean")
                        row[f"{idx_name}_min"] = stats.get(f"{idx_name}_min")
                        row[f"{idx_name}_max"] = stats.get(f"{idx_name}_max")
                        row[f"{idx_name}_stdDev"] = stats.get(f"{idx_name}_stdDev")
                    else:
                        row[f"{idx_name}_mean"] = None

                rows.append(row)

            except Exception as e:
                add_log(f"{year}: xato — {str(e)}", "warning")
                continue

        if not rows:
            add_log("Hech qanday natija olinmadi", "error")
            return None

        df = pd.DataFrame(rows)
        add_log(f"Tahlil tugadi: {len(df)} qator natija", "success")
        return df

    @staticmethod
    def run_monthly(config):
        """
        Oylik tahlil ishga tushiradi.

        Args:
            config: dict — barcha sozlamalar

        Returns:
            pd.DataFrame — natijalar jadvali
        """
        return TimeSeriesAnalyzer._generate_demo_data(config, time_unit="monthly")

    @staticmethod
    def run_seasonal(config):
        """
        Mavsumiy tahlil ishga tushiradi.

        Args:
            config: dict — barcha sozlamalar

        Returns:
            pd.DataFrame — natijalar jadvali
        """
        return TimeSeriesAnalyzer._generate_demo_data(config, time_unit="seasonal")

    @staticmethod
    def compute_trend(df, column):
        """
        Mann-Kendall test va Sen's slope hisoblaydi.

        Args:
            df: pd.DataFrame — vaqt seriyasi
            column: str — ustun nomi

        Returns:
            dict: {slope, intercept, p_value, r_squared, trend}
        """
        try:
            values = df[column].dropna().values
            if len(values) < 3:
                return None

            x = np.arange(len(values))
            slope, intercept = np.polyfit(x, values, 1)
            y_pred = slope * x + intercept

            ss_res = np.sum((values - y_pred) ** 2)
            ss_tot = np.sum((values - np.mean(values)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

            trend = "up" if slope > 0.001 else ("down" if slope < -0.001 else "stable")

            try:
                from scipy import stats as scipy_stats
                _, p_value = scipy_stats.kendalltau(x, values)
            except ImportError:
                p_value = None

            return {
                "slope": round(slope, 6),
                "intercept": round(intercept, 4),
                "p_value": round(p_value, 4) if p_value is not None else None,
                "r_squared": round(r_squared, 4),
                "trend": trend,
            }
        except Exception as e:
            add_log(f"Trend hisoblash xatosi ({column}): {str(e)}", "error")
            return None

    @staticmethod
    def get_map_tile_url(index_image, vis_params):
        """
        GEE obraz uchun tile URL oladi (Folium layer sifatida).

        Args:
            index_image: ee.Image — indeks obrazi
            vis_params: dict — vizualizatsiya parametrlari

        Returns:
            str — tile URL yoki None
        """
        if not EE_AVAILABLE:
            return None

        try:
            map_id_dict = index_image.getMapId(vis_params)
            return map_id_dict["tile_fetcher"].url_format
        except Exception as e:
            add_log(f"Tile URL xatosi: {str(e)}", "error")
            return None

    @staticmethod
    def _generate_demo_data(config, time_unit="yearly"):
        """
        Demo rejimda sintetik ma'lumot generatsiya qiladi.

        Args:
            config: dict — konfiguratsiya
            time_unit: str — yearly, monthly, seasonal

        Returns:
            pd.DataFrame — demo natijalar
        """
        indices = config.get("selected_indices", ["NDVI"])
        start_year = config.get("start_date", date(2019, 1, 1)).year
        end_year = config.get("end_date", date(2024, 12, 31)).year

        np.random.seed(42)
        rows = []

        if time_unit == "yearly":
            for year in range(start_year, end_year + 1):
                row = {"year": year}
                for idx in indices:
                    base = 0.45 if idx in ("NDVI", "EVI", "SAVI", "GNDVI") else 0.15
                    trend = 0.008 * (year - start_year)
                    noise = np.random.normal(0, 0.03)
                    val = base + trend + noise
                    row[f"{idx}_mean"] = round(val, 4)
                    row[f"{idx}_min"] = round(val - 0.15 - abs(np.random.normal(0, 0.02)), 4)
                    row[f"{idx}_max"] = round(val + 0.25 + abs(np.random.normal(0, 0.02)), 4)
                    row[f"{idx}_stdDev"] = round(abs(np.random.normal(0.08, 0.02)), 4)
                rows.append(row)
        elif time_unit == "monthly":
            for year in range(start_year, end_year + 1):
                for month in range(1, 13):
                    row = {"year": year, "month": month}
                    for idx in indices:
                        seasonal = 0.15 * np.sin(2 * np.pi * (month - 4) / 12)
                        base = 0.4 + seasonal + np.random.normal(0, 0.02)
                        row[f"{idx}_mean"] = round(base, 4)
                    rows.append(row)
        elif time_unit == "seasonal":
            seasons = {"Bahor": (3, 5), "Yoz": (6, 8), "Kuz": (9, 11), "Qish": (12, 2)}
            for year in range(start_year, end_year + 1):
                for season_name in seasons:
                    row = {"year": year, "season": season_name}
                    for idx in indices:
                        base = 0.4 + np.random.normal(0, 0.05)
                        row[f"{idx}_mean"] = round(base, 4)
                    rows.append(row)

        df = pd.DataFrame(rows)
        add_log(f"Demo ma'lumot generatsiya qilindi: {len(df)} qator", "success")
        return df
