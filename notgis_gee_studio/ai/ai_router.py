"""
4 ta AI provider routeri.

Provider tanlash, so'rov yuborish va ulanishni tekshirish.
"""
import time
from utils.log_manager import add_log


class AIRouter:
    """AI providerlar routeri."""

    def __init__(self):
        self._clients = {}

    def configure(self, provider, api_key, model=None):
        """
        AI providerni sozlaydi.

        Args:
            provider: str — Gemini, Groq, OpenRouter, RouterWay
            api_key: str — API kaliti
            model: str yoki None — model nomi
        """
        try:
            if provider == "Gemini":
                from ai.providers.gemini_client import GeminiClient
                self._clients[provider] = GeminiClient(api_key, model or "gemini-2.0-flash")
            elif provider == "Groq":
                from ai.providers.groq_client import GroqClient
                self._clients[provider] = GroqClient(api_key, model or "llama-3.3-70b-versatile")
            elif provider == "OpenRouter":
                from ai.providers.openrouter_client import OpenRouterClient
                self._clients[provider] = OpenRouterClient(api_key, model or "meta-llama/llama-3.3-70b-instruct")
            elif provider == "RouterWay":
                from ai.providers.routerway_client import RouterWayClient
                self._clients[provider] = RouterWayClient(api_key, model or "gpt-4o")
            else:
                add_log(f"Noma'lum provider: {provider}", "error")
                return

            add_log(f"AI sozlandi: {provider} ({model})", "info")
        except Exception as e:
            add_log(f"AI sozlash xatosi: {str(e)}", "error")

    def chat(self, provider, messages, system_prompt=None):
        """
        Berilgan providerga so'rov yuboradi.

        Args:
            provider: str — provider nomi
            messages: list — xabarlar
            system_prompt: str yoki None

        Returns:
            str: javob matni
        """
        client = self._clients.get(provider)
        if not client:
            return f"{provider} sozlanmagan. Avval API kalitini kiriting."

        add_log(f"AI so'rov: {provider}", "process")
        start = time.time()

        result = client.chat(messages, system_prompt)

        elapsed = time.time() - start
        add_log(f"AI javob olindi ({elapsed:.1f}s)", "success")

        return result

    def test_connection(self, provider):
        """
        Provider ulanishni tekshiradi.

        Args:
            provider: str — provider nomi

        Returns:
            bool
        """
        client = self._clients.get(provider)
        if not client:
            return False
        return client.test()

    def is_configured(self, provider):
        """Provider sozlanganmi."""
        return provider in self._clients
