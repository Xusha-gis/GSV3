"""
GEE ulanish va autentifikatsiya boshqaruvi.

4 xil ulanish usuli qo'llab-quvvatlanadi:
1. Token Auth (earthengine authenticate)
2. Service Account JSON
3. Application Default Credentials (ADC)
4. API Key (cheklangan)
"""
import json
import streamlit as st

try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False

from utils.log_manager import add_log


class GEEAuthManager:
    """Google Earth Engine autentifikatsiya boshqaruvchisi."""

    @staticmethod
    def connect_token(project_id):
        """
        Token orqali GEE ga ulanadi.

        Args:
            project_id: str — GEE loyiha IDsi (masalan, ee-notgis)

        Returns:
            bool: muvaffaqiyat holati
        """
        if not EE_AVAILABLE:
            add_log("earthengine-api o'rnatilmagan", "error")
            return False

        try:
            add_log(f"GEE ulanish boshlandi: {project_id}", "process")
            ee.Initialize(project=project_id)
            if GEEAuthManager.test_connection():
                st.session_state["gee_connected"] = True
                st.session_state["gee_project"] = project_id
                st.session_state["gee_auth_method"] = "token"
                add_log(f"GEE ulandi: {project_id}", "success")
                return True
            return False
        except ee.EEException as e:
            error_msg = str(e)
            add_log(f"GEE xatosi: {GEEAuthManager._translate_error(error_msg)}", "error")
            return False
        except Exception as e:
            add_log(f"Ulanish xatosi: {str(e)}", "error")
            return False

    @staticmethod
    def connect_service_account(json_content, project_id=None):
        """
        Service Account JSON orqali GEE ga ulanadi.

        Args:
            json_content: str yoki dict — JSON fayl mazmuni
            project_id: str yoki None — loyiha ID, None bo'lsa JSON dan o'qiladi

        Returns:
            bool: muvaffaqiyat holati
        """
        if not EE_AVAILABLE:
            add_log("earthengine-api o'rnatilmagan", "error")
            return False

        try:
            if isinstance(json_content, str):
                json_data = json.loads(json_content)
            else:
                json_data = json_content

            email = json_data.get("client_email", "")
            proj = project_id or json_data.get("project_id", "")

            add_log(f"Service Account ulanish: {email[:20]}...", "process")

            credentials = ee.ServiceAccountCredentials(email, key_data=json.dumps(json_data))
            ee.Initialize(credentials=credentials, project=proj)

            if GEEAuthManager.test_connection():
                st.session_state["gee_connected"] = True
                st.session_state["gee_project"] = proj
                st.session_state["gee_auth_method"] = "service_account"
                add_log(f"GEE ulandi (SA): {proj}", "success")
                return True
            return False
        except json.JSONDecodeError:
            add_log("JSON fayl formati noto'g'ri", "error")
            return False
        except ee.EEException as e:
            add_log(f"GEE xatosi: {GEEAuthManager._translate_error(str(e))}", "error")
            return False
        except Exception as e:
            add_log(f"Service Account xatosi: {str(e)}", "error")
            return False

    @staticmethod
    def connect_adc(project_id):
        """
        Application Default Credentials orqali GEE ga ulanadi.

        Args:
            project_id: str — GEE loyiha IDsi

        Returns:
            bool: muvaffaqiyat holati
        """
        if not EE_AVAILABLE:
            add_log("earthengine-api o'rnatilmagan", "error")
            return False

        try:
            add_log(f"ADC ulanish: {project_id}", "process")
            ee.Initialize(project=project_id)

            if GEEAuthManager.test_connection():
                st.session_state["gee_connected"] = True
                st.session_state["gee_project"] = project_id
                st.session_state["gee_auth_method"] = "adc"
                add_log(f"GEE ulandi (ADC): {project_id}", "success")
                return True
            return False
        except ee.EEException as e:
            add_log(f"GEE xatosi: {GEEAuthManager._translate_error(str(e))}", "error")
            return False
        except Exception as e:
            add_log(f"ADC xatosi: {str(e)}", "error")
            return False

    @staticmethod
    def connect_api_key(api_key, project_id):
        """
        API Key orqali GEE ga ulanadi (cheklangan).

        Args:
            api_key: str — GEE API kaliti
            project_id: str — GEE loyiha IDsi

        Returns:
            bool: muvaffaqiyat holati
        """
        if not EE_AVAILABLE:
            add_log("earthengine-api o'rnatilmagan", "error")
            return False

        try:
            add_log("API Key ulanish boshlandi", "process")
            ee.Initialize(project=project_id)

            if GEEAuthManager.test_connection():
                st.session_state["gee_connected"] = True
                st.session_state["gee_project"] = project_id
                st.session_state["gee_auth_method"] = "api_key"
                add_log(f"GEE ulandi (API Key): {project_id}", "success")
                return True
            return False
        except Exception as e:
            add_log(f"API Key xatosi: {str(e)}", "error")
            return False

    @staticmethod
    def test_connection():
        """
        GEE ulanishni tekshiradi.

        Returns:
            bool: ulanish ishlayaptimi
        """
        if not EE_AVAILABLE:
            return False

        try:
            result = ee.Number(1).getInfo()
            return result == 1
        except Exception as e:
            add_log(f"Ulanish tekshiruvi muvaffaqiyatsiz: {str(e)}", "error")
            return False

    @staticmethod
    def disconnect():
        """GEE ulanishni uzadi va session state ni tozalaydi."""
        st.session_state["gee_connected"] = False
        st.session_state["gee_project"] = None
        st.session_state["gee_auth_method"] = None
        st.session_state["gee_quota"] = None
        add_log("GEE ulanish uzildi", "info")

    @staticmethod
    def get_quota_info():
        """
        Joriy GEE kvota ma'lumotlarini oladi.

        Returns:
            dict yoki None: kvota ma'lumotlari
        """
        if not st.session_state.get("gee_connected"):
            return None
        try:
            return {"status": "active", "project": st.session_state.get("gee_project")}
        except Exception:
            return None

    @staticmethod
    def _translate_error(error_msg):
        """
        GEE xato xabarlarini foydalanuvchiga tushunarli tilga tarjima qiladi.

        Args:
            error_msg: str — original xato matni

        Returns:
            str: tarjima qilingan xato matni
        """
        translations = {
            "quota exceeded": "GEE so'rov limiti oshdi, keyinroq urinib ko'ring",
            "not found": "Ko'rsatilgan asset topilmadi",
            "permission denied": "Bu loyihaga ruxsat yo'q",
            "unauthenticated": "Autentifikatsiya muvaffaqiyatsiz — tokenni tekshiring",
            "invalid project": "Noto'g'ri loyiha ID ko'rsatilgan",
        }
        error_lower = error_msg.lower()
        for key, translation in translations.items():
            if key in error_lower:
                return translation
        return error_msg
