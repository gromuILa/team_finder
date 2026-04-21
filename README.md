# TeamFinder — Вариант 2 (Навыки пользователей)

Платформа для поиска единомышленников на pet-проекты.

## Запуск через Docker (рекомендуется)

```bash
# 1. Скопируйте файл с переменными окружения
cp .env.example .env

# 2. Запустите контейнеры
docker compose up --build

# 3. Откройте в браузере
# http://localhost:8000
```

Миграции, сбор статики и тестовые данные применяются автоматически при первом запуске.

## Запуск без Docker (SQLite)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Тестовые аккаунты

| Роль | Email | Пароль |
|------|-------|--------|
| Администратор | admin@example.com | admin123 |
| Пользователь | maria@yandex.ru | password |
| Пользователь | ivan@example.com | password123 |
| Пользователь | anna@example.com | password123 |

## Реализованный вариант

**Вариант 2** — Навыки пользователей + фильтрация участников по навыкам:
- На странице пользователя блок «Навыки» с управлением (добавление с автодополнением, удаление без перезагрузки)
- На странице участников фильтр по навыкам (`/users/list/?skill=Python`)
- API: `GET /users/skills/?q=`, `POST /users/<id>/skills/add`, `POST /users/<id>/skills/<id>/remove/`

## Переменные окружения (`.env`)

| Переменная | Описание |
|------------|----------|
| `SECRET_KEY` | Django секретный ключ |
| `DEBUG` | Режим отладки (`True`/`False`) |
| `POSTGRES_DB` | Имя базы данных |
| `POSTGRES_USER` | Пользователь БД |
| `POSTGRES_PASSWORD` | Пароль БД |
| `POSTGRES_HOST` | Хост БД (`db` внутри Docker) |
| `POSTGRES_PORT` | Порт БД (по умолчанию `5432`) |
