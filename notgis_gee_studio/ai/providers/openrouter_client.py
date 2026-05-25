"""OpenRouter AI client."""
from utils.log_manager import add_log


class OpenRouterClient:
    """OpenRouter API bilan ishlash (OpenAI-compatible)."""

    def __init__(self, api_key, model="meta-llama/llama-3.3-70b-instruct"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _init_client(self):
        """Clientni boshlaydi."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1",
                )
            except Exception as e:
                add_log(f"OpenRouter client xatosi: {str(e)}", "error")

    def chat(self, messages, system_prompt=None):
        """
        OpenRouter ga so'rov yuboradi.

        Args:
            messages: list — xabarlar ro'yxati
            system_prompt: str yoki None

        Returns:
            str: javob matni
        """
        self._init_client()
        if self._client is None:
            return "OpenRouter client ishlamadi"

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
            add_log(f"OpenRouter javob xatosi: {str(e)}", "error")
            return f"Xato: {str(e)}"

    def test(self):
        """Ulanishni tekshiradi."""
        try:
            result = self.chat([{"role": "user", "content": "Say OK"}])
            return len(result) > 0
        except Exception:
            return False
