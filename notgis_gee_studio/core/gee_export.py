"""
GEE eksport moduli — Drive, Asset, GeoTIFF eksport.

Eksport vazifalari GEE serverda asinxron ishlaydi.
"""
import streamlit as st
import json

try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False

from utils.log_manager import add_log


class GEEExporter:
    """GEE eksport operatsiyalari."""

    @staticmethod
    def export_to_drive(image, description, folder, region, scale=30, crs="EPSG:4326", max_pixels=1e13):
        """
        GEE obrazini Google Drive ga eksport qiladi.

        Args:
            image: ee.Image — eksport qilinadigan obraz
            description: str — fayl nomi
            folder: str — Drive papka nomi
            region: ee.Geometry — hudud
            scale: int — o'lchov (metr)
            crs: str — koordinat tizimi
            max_pixels: float — maksimal piksellar soni

        Returns:
            ee.batch.Task yoki None
        """
        if not EE_AVAILABLE or not st.session_state.get("gee_connected"):
            add_log("GEE ulanmagan, eksport mumkin emas", "error")
            return None

        try:
            task = ee.batch.Export.image.toDrive(
                image=image,
                description=description,
                folder=folder,
                region=region,
                scale=scale,
                crs=crs,
                maxPixels=max_pixels,
                fileFormat="GeoTIFF",
            )
            task.start()
            add_log(f"Drive eksport boshlandi: {description} → {folder}/", "success")
            return task
        except Exception as e:
            add_log(f"Drive eksport xatosi: {str(e)}", "error")
            return None

    @staticmethod
    def export_to_asset(image, asset_id, region, scale=30, crs="EPSG:4326", max_pixels=1e13):
        """
        GEE obrazini Asset sifatida saqlaydi.

        Args:
            image: ee.Image — eksport qilinadigan obraz
            asset_id: str — asset yo'li
            region: ee.Geometry — hudud
            scale: int — o'lchov
            crs: str — koordinat tizimi
            max_pixels: float — maksimal piksellar

        Returns:
            ee.batch.Task yoki None
        """
        if not EE_AVAILABLE or not st.session_state.get("gee_connected"):
            add_log("GEE ulanmagan, eksport mumkin emas", "error")
            return None

        try:
            task = ee.batch.Export.image.toAsset(
                image=image,
                description=asset_id.split("/")[-1],
                assetId=asset_id,
                region=region,
                scale=scale,
                crs=crs,
                maxPixels=max_pixels,
            )
            task.start()
            add_log(f"Asset eksport boshlandi: {asset_id}", "success")
            return task
        except Exception as e:
            add_log(f"Asset eksport xatosi: {str(e)}", "error")
            return None

    @staticmethod
    def check_task_status(task):
        """
        Eksport vazifasi holatini tekshiradi.

        Args:
            task: ee.batch.Task

        Returns:
            dict: {state, description, progress}
        """
        if task is None:
            return {"state": "UNKNOWN"}

        try:
            status = task.status()
            return {
                "state": status.get("state", "UNKNOWN"),
                "description": status.get("description", ""),
            }
        except Exception:
            return {"state": "ERROR"}

    @staticmethod
    def list_running_tasks():
        """
        Joriy ishlayotgan GEE vazifalarini ko'rsatadi.

        Returns:
            list: vazifalar ro'yxati
        """
        if not EE_AVAILABLE or not st.session_state.get("gee_connected"):
            return []

        try:
            tasks = ee.batch.Task.list()
            return [
                {
                    "id": t.id,
                    "state": t.state,
                    "description": t.config.get("description", ""),
                }
                for t in tasks[:10]
            ]
        except Exception:
            return []
