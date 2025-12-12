# tg-member-list-sdk

SDK для получения списка участников Telegram-чата через простой HTTP-эндпоинт с базовой авторизацией.

## Установка

```bash
python3 -m pip install .
```

## Использование

```python
from dlab.tg_sso import TgUserList

client = TgUserList()  # Читает URL, LOGIN, PASSWORD из .env или переменных окружения
users = client.get_users()
print(users)
```

Переменные окружения:
- `URL` — адрес HTTP-эндпоинта, который возвращает JSON вида `{"users": [...]}`.
- `LOGIN` — логин для базовой авторизации.
- `PASSWORD` — пароль для базовой авторизации.


