# CashflowTest

Быстрый старт
Установить зависимости:
"python -m venv venv; venv\Scripts\activate; pip install -r requirements.txt"
Применить миграции и запустить:
"python manage.py migrate; python manage.py runserver"
Полезные ссылки:
UI: / или /entries/
Админка: /admin/
API ping: /api/ping/
OpenAPI schema: /api/schema/
Swagger UI: /api/docs/
Требования
Python 3.12+; SQLite по умолчанию (db.sqlite3 в корне)
Зависимости: Django, DRF, django-filter, drf-spectacular, django-htmx (см. requirements.txt)
Структура
config/ - настройки проекта, корневые urls, wsgi/asgi
ui/ - views/urls/templates для веб-интерфейса
core/ - справочники (статусы, типы, категории)
cashflow/ - операции и логика кассового потока
api/ - serializers/views/urls для REST-API
