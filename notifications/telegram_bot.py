import os
from telegram import Bot
import asyncio

class TelegramNotifier:
    def __init__(self, token: str = None, chat_id: str = None):
        """
        Initialise le bot Telegram.
        Si token ou chat_id ne sont pas fournis, on essaie de les lire depuis config.json
        puis depuis les variables d'environnement.
        """
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from backend.config_manager import config_manager

        cfg = config_manager.get_telegram_config()
        self.token = token or cfg.get("token") or os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or cfg.get("chat_id") or os.environ.get("TELEGRAM_CHAT_ID")

        if self.token:
            self.bot = Bot(token=self.token)
        else:
            self.bot = None
            print("Avertissement: TELEGRAM_BOT_TOKEN non configuré. Les notifications seront affichées dans la console.")

    async def _send_message_async(self, message: str):
        if self.bot and self.chat_id:
            try:
                await self.bot.send_message(chat_id=self.chat_id, text=message)
                print(f"Notification envoyée à Telegram: {message}")
            except Exception as e:
                print(f"Erreur lors de l'envoi du message Telegram: {e}")
        else:
            print(f"[FALLBACK NOTIFICATION] => {message}")

    def send_alert(self, message: str):
        """
        Envoie l'alerte. Gère la boucle d'événements asyncio.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Si nous sommes déjà dans une boucle (par ex. Streamlit), on crée une task
            loop.create_task(self._send_message_async(message))
        else:
            asyncio.run(self._send_message_async(message))

if __name__ == "__main__":
    notifier = TelegramNotifier()
    notifier.send_alert("Ceci est un test de notification de l'Agent de Trading.")
