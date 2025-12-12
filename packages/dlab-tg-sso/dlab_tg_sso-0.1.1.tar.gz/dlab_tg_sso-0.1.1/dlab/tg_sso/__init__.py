import os
from collections.abc import Sequence
from dotenv import load_dotenv
import requests as req


class _UsersView(Sequence):
    def __init__(self, owner: "TgUserList"):
        self._owner = owner

    def _data(self):
        # Каждый доступ обновляет данные
        return self._owner.get_users()

    def __iter__(self):
        return iter(self._data())

    def __len__(self):
        return len(self._data())

    def __getitem__(self, index):
        return self._data()[index]

    def __repr__(self):
        return repr(self._data())

    def __str__(self):
        return str(self._data())

    def __contains__(self, item):
        return item in self._data()

    def to_list(self):
        return list(self._data())


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
        self._users = []
        self._users_view = _UsersView(self)

    def get_users(self, chat_id: str | None = None):
        response = self.session.get(self.url)
        data = response.json()
        users = data.get("users", [])
        self._users = users
        return self._users

    @property
    def users(self):
        return self._users_view


__all__ = ["TgUserList"]


