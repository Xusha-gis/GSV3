"""Google Gemini AI client."""
from utils.log_manager import add_log


class GeminiClient:
    """Google Gemini API bilan ishlash."""

    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _init_client(self):
        """Clientni boshlaydi."""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model)
            except Exception as e:
                add_log(f"Gemini client xatosi: {str(e)}", "error")

    def chat(self, messages, system_prompt=None):
        """
        Gemini ga so'rov yuboradi.

        Args:
            messages: list — xabarlar ro'yxati
            system_prompt: str yoki None — tizim prompti

        Returns:
            str: javob matni
        """
        self._init_client()
        if self._client is None:
            return "Gemini client ishlamadi"

        try:
            prompt_parts = []
            if system_prompt:
                prompt_parts.append(system_prompt)
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role}: {content}")

            response = self._client.generate_content("\n".join(prompt_parts))
            return response.text
        except Exception as e:
            add_log(f"Gemini javob xatosi: {str(e)}", "error")
            return f"Xato: {str(e)}"

    def test(self):
        """Ulanishni tekshiradi."""
        try:
            result = self.chat([{"role": "user", "content": "Say OK"}])
            return "ok" in result.lower() or len(result) > 0
        except Exception:
            return False
