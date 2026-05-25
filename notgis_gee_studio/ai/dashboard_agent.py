"""
Auto-config agent + chat agent.

Tabiiy tildagi so'rovni konfiguratsiyaga aylantiradi.
GEE haqidagi savollarga javob beradi.
"""
import json
from utils.log_manager import add_log
from core.indices import INDICES
from config.settings import Settings


SYSTEM_PROMPT = """Sen notGIS GEE Studio platformasi uchun GIS va masofadan zondlash bo'yicha mutaxassis yordamchisan.

Mavjud satellitlar: {satellites}
Mavjud indekslar: {indices}
O'zbekiston viloyatlari: {regions}

Foydalanuvchi so'rovini tahlil qilib, JSON formatida konfiguratsiya qaytaring.
Agar foydalanuvchi oddiy savol bersa — GIS, masofadan zondlash, GEE haqida tushunarli javob bering.

Konfiguratsiya formati:
{{
  "action": "configure",
  "satellite": "...",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "selected_indices": ["NDVI", ...],
  "aoi_name": "...",
  "cloud_pct": 20,
  "time_unit": "Yillik",
  "explanation": "Qisqa tushuntirish"
}}

Yoki oddiy javob:
{{
  "action": "answer",
  "answer": "Javob matni"
}}
"""


class DashboardAgent:
    """Dashboard auto-config va chat agenti."""

    @staticmethod
    def analyze_and_configure(prompt, router, provider, current_config=None):
        """
        Foydalanuvchi so'rovini tahlil qilib konfiguratsiya yaratadi.

        Args:
            prompt: str — foydalanuvchi so'rovi
            router: AIRouter — AI router
            provider: str — provider nomi
            current_config: dict yoki None — joriy konfiguratsiya

        Returns:
            dict: yangi konfiguratsiya yoki javob
        """
        from config.aoi_registry import AOIRegistry

        system = SYSTEM_PROMPT.format(
            satellites=", ".join(Settings.SATELLITES.keys()),
            indices=", ".join(INDICES.keys()),
            regions=", ".join(AOIRegistry.get_region_names()),
        )

        messages = [{"role": "user", "content": prompt}]
        response = router.chat(provider, messages, system_prompt=system)

        config = DashboardAgent._parse_ai_response(response)
        if config:
            validated = DashboardAgent._validate_config(config)
            if validated:
                return validated
            else:
                add_log("AI javobidagi konfiguratsiya noto'g'ri", "warning")
                return {"action": "answer", "answer": response}

        return {"action": "answer", "answer": response}

    @staticmethod
    def ask_gee_question(question, router, provider, context=None):
        """
        GEE haqidagi erkin savolga javob beradi.

        Args:
            question: str — savol
            router: AIRouter
            provider: str — provider nomi
            context: dict yoki None — kontekst

        Returns:
            str: javob matni
        """
        system = """Sen GIS, masofadan zondlash va Google Earth Engine bo'yicha mutaxassisan.
Savolga aniq, qisqa va tushunarli javob ber. Misollar bilan tushuntir.
Javobni o'zbek yoki rus tilida ber (foydalanuvchi qaysi tilda so'rasa)."""

        messages = [{"role": "user", "content": question}]
        return router.chat(provider, messages, system_prompt=system)

    @staticmethod
    def _parse_ai_response(response):
        """
        AI javobidan JSON ajratib oladi.

        Args:
            response: str — AI javob matni

        Returns:
            dict yoki None
        """
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        return None

    @staticmethod
    def _validate_config(config):
        """
        AI javobidagi konfiguratsiyani tekshiradi.

        Args:
            config: dict — AI javobidan ajratilgan config

        Returns:
            dict yoki None: validatsiya qilingan config
        """
        if config.get("action") == "answer":
            return config

        if config.get("action") != "configure":
            return None

        valid_indices = set(INDICES.keys())
        selected = config.get("selected_indices", [])
        validated_indices = [idx for idx in selected if idx in valid_indices]

        if not validated_indices:
            add_log("AI noto'g'ri indeks nomlari qaytardi", "warning")
            return None

        config["selected_indices"] = validated_indices

        valid_sats = set(Settings.SATELLITES.keys())
        if config.get("satellite") and config["satellite"] not in valid_sats:
            add_log(f"AI noto'g'ri satellite qaytardi: {config['satellite']}", "warning")
            config["satellite"] = "Sentinel-2 SR Harmonized"

        return config
