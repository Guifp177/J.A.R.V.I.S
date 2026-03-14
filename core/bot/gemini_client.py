from google import genai

from core.config.config_manager import ConfigManager
from core.memory import Memory
from modules.apps import open_app
from modules.web_search import pesquisar_no_chrome


class GeminiClient:
    def __init__(self):
        self.config = ConfigManager()
        self.memory = Memory()
        self.api_key = self.config.get_gemini_key()

        self.system_instructions = """
        Você é o J.A.R.V.I.S., assistente pessoal do MCU.
        Mantenha as respostas claras, inteligentes e concisas.
        Não exiba tags de pensamento <think>.
        Responda sempre em português.
        """

        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.model_id = "gemini-2.5-flash-lite"
            except Exception as e:
                print(f"[ERRO CONFIG GEMINI] {e}")
                self.client = None
        else:
            self.client = None

    def chat(self, user_text: str):

        t = user_text.lower().strip()
        if t.startswith("abrir "):
            app = t.replace("abrir ", "").strip()
            result = open_app(app)
            return (
                f"Abrindo {app}, Senhor." if result["ok"] else f"Falha ao abrir {app}."
            )

        if not self.client:
            return None

        try:
            history = []
            for msg in self.memory.get_context():
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [{"text": msg["content"]}]})

            chat = self.client.chats.create(
                model=self.model_id,
                config={"system_instruction": self.system_instructions},
                history=history,
            )

            response = chat.send_message(user_text)

            raw_text = response.text if response.text else ""
            reply = str(raw_text).strip()

            if not reply:
                return None

            self.memory.add("user", user_text)
            self.memory.add("assistant", reply)
            return reply

        except Exception as e:
            print(f"[ERRO API GEMINI] {e}")
            return None
