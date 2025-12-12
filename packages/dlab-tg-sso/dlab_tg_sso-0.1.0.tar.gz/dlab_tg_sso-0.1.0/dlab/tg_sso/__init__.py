import os
from dotenv import load_dotenv
import requests as req


class TgUserList:
    def __init__(self, url: str | None = None, login: str | None = None, password: str | None = None):
        if login is None or password is None:
            load_dotenv()
            login = os.getenv("LOGIN")
            password = os.getenv("PASSWORD")
            if login is None or password is None:
                raise ValueError("Login and password are not set")
        if url is None:
            url = os.getenv("URL")
            if url is None:
                raise ValueError("URL is not set")

        self.url = url
        self.session = req.Session()
        self.session.auth = (login, password)

    def get_users(self, chat_id: str | None = None):
        response = self.session.get(self.url)
        data = response.json()
        users = data.get("users", [])
        return users


__all__ = ["TgUserList"]


