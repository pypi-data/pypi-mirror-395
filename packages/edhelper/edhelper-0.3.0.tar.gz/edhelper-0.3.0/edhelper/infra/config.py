from dotenv import load_dotenv
import os
import keyring
from pathlib import Path

load_dotenv()

SERVICE_NAME = "edhelper"


class Settings:
    BASE_PATH = Path(__file__).resolve().parents[1]

    NAME = "mtg-deck"
    VERSION = "0.3.0"
    DATABASE_URL = str(BASE_PATH / "db.sqlite3")
    API_URL = "https://mtg-api-production.up.railway.app"

    @property
    def API_KEY(self) -> str:
        keyring_key = keyring.get_password(SERVICE_NAME, "api_key")
        return keyring_key or os.getenv("API_KEY", "")

    @property
    def CLIENT_ID(self) -> str:
        keyring_id = keyring.get_password(SERVICE_NAME, "client_id")
        return keyring_id or os.getenv("CLIENT_ID", "")

    def set_credentials(self, api_key: str, client_id: str):
        keyring.set_password(SERVICE_NAME, "api_key", api_key)
        keyring.set_password(SERVICE_NAME, "client_id", client_id)

    def clear_credentials(self):
        try:
            keyring.delete_password(SERVICE_NAME, "api_key")
        except Exception:
            pass
        try:
            keyring.delete_password(SERVICE_NAME, "client_id")
        except Exception:
            pass

    def user_is_authenticated(self):
        return self.API_KEY != "" and self.CLIENT_ID != ""


settings = Settings()
