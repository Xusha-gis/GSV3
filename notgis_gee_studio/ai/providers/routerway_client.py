"""RouterWay AI client."""
import requests
from utils.log_manager import add_log


class RouterWayClient:
    """RouterWay API bilan ishlash."""

    BASE_URL = "https://api.routerway.com/v1"

    def __init__(self, api_key, model="gpt-4o"):
        self.api_key = api_key
        self.model = model

    def chat(self, messages, system_prompt=None):
        """
        RouterWay ga so'rov yuboradi.

        Args:
            messages: list — xabarlar ro'yxati
            system_prompt: str yoki None

        Returns:
            str: javob matni
        """
        try:
            formatted = []
            if system_prompt:
                formatted.append({"role": "system", "content": system_prompt})
            formatted.extend(messages)

            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": formatted,
                    "temperature": 0.3,
                    "max_tokens": 2048,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                add_log(f"RouterWay xatosi: {response.status_code}", "error")
                return f"Xato: HTTP {response.status_code}"

        except requests.Timeout:
            add_log("RouterWay: timeout", "error")
            return "Xato: so'rov vaqti oshdi"
        except Exception as e:
            add_log(f"RouterWay javob xatosi: {str(e)}", "error")
            return f"Xato: {str(e)}"

    def test(self):
        """Ulanishni tekshiradi."""
        try:
            result = self.chat([{"role": "user", "content": "Say OK"}])
            return "xato" not in result.lower()
        except Exception:
            return False
