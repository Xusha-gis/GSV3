"""Groq AI client."""
from utils.log_manager import add_log


class GroqClient:
    """Groq API bilan ishlash."""

    def __init__(self, api_key, model="llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _init_client(self):
        """Clientni boshlaydi."""
        if self._client is None:
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
            except Exception as e:
                add_log(f"Groq client xatosi: {str(e)}", "error")

    def chat(self, messages, system_prompt=None):
        """
        Groq ga so'rov yuboradi.

        Args:
            messages: list — xabarlar ro'yxati
            system_prompt: str yoki None — tizim prompti

        Returns:
            str: javob matni
        """
        self._init_client()
        if self._client is None:
            return "Groq client ishlamadi"

        try:
            formatted = []
            if system_prompt:
                formatted.append({"role": "system", "content": system_prompt})
            formatted.extend(messages)

            response = self._client.chat.completions.create(
                model=self.model,
                messages=formatted,
                temperature=0.3,
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except Exception as e:
            add_log(f"Groq javob xatosi: {str(e)}", "error")
            return f"Xato: {str(e)}"

    def test(self):
        """Ulanishni tekshiradi."""
        try:
            result = self.chat([{"role": "user", "content": "Say OK"}])
            return len(result) > 0
        except Exception:
            return False
