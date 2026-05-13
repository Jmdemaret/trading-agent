import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "telegram": {
        "token": "",
        "chat_id": ""
    },
    "portfolio": [
        {"ticker": "AAPL", "quantity": 50, "buyPrice": 150.0},
        {"ticker": "MSFT", "quantity": 30, "buyPrice": 300.0}
    ]
}

class ConfigManager:
    def __init__(self):
        self._load()

    def _load(self):
        if not os.path.exists(CONFIG_FILE):
            self.config = DEFAULT_CONFIG.copy()
            self.save()
        else:
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)

        # Assurer que les clés existent
        if "telegram" not in self.config:
            self.config["telegram"] = {"token": "", "chat_id": ""}
        if "portfolio" not in self.config:
            self.config["portfolio"] = []

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_portfolio(self):
        return self.config.get("portfolio", [])

    def add_to_portfolio(self, item):
        self.config["portfolio"].append(item)
        self.save()

    def remove_from_portfolio(self, ticker):
        self.config["portfolio"] = [i for i in self.config["portfolio"] if i["ticker"] != ticker]
        self.save()

    def get_telegram_config(self):
        return self.config.get("telegram", {})

    def set_telegram_config(self, token, chat_id):
        self.config["telegram"]["token"] = token
        self.config["telegram"]["chat_id"] = chat_id
        self.save()

config_manager = ConfigManager()
