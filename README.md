# TeamFinder — Вариант 2 (Навыки пользователей)

Платформа для поиска единомышленников на pet-проекты.

## Быстрый запуск (SQLite, без Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data       # создаёт тестовые данные
python manage.py runserver
```

Откройте http://127.0.0.1:8000

## Тестовые аккаунты

| Роль | Email | Пароль |
|------|-------|--------|
| Администратор | admin@example.com | admin123 |
| Пользователь | maria@yandex.ru | password |
| Пользователь | ivan@example.com | password123 |
| Пользователь | anna@example.com | password123 |

## Запуск с PostgreSQL

1. Скопируйте `.env.example` → `.env`
2. Заполните `DATABASE_URL=postgresql://user:pass@host:5432/dbname`
3. Запустите миграции и сид-команду

## Реализованный вариант

**Вариант 2** — Навыки пользователей + фильтрация участников по навыкам:
- На странице пользователя блок «Навыки» с управлением (добавление с автодополнением, удаление)
- На странице участников фильтр по навыкам (`/users/list/?skill=Python`)
- API: `GET /users/skills/?q=`, `POST /users/<id>/skills/add`, `POST /users/<id>/skills/<id>/remove/`
