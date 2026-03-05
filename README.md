# CashflowTest

Учебный сервис для учёта доходов и расходов.  
Проект сделан как тренировка backend‑разработки: REST API, работа с базой данных и бизнес‑логикой денежных потоков.

## Стек

- Python 3.10+
- FastAPI 
- SQLite или PostgreSQL 
- SQLAlchemy
- Pydantic
- pytest

## Функциональность

- Хранение финансовых операций:
  - доходы;
  - расходы.
- CRUD‑операции по операциям:
  - добавление;
  - получение списка;
  - просмотр по идентификатору;
  - обновление;
  - удаление.
- (Опционально) Категории операций: например, «зарплата», «еда», «транспорт».
- Расчёт текущего баланса и базовой статистики .
- Валидация входных данных через Pydantic.

## Примеры эндпоинтов

POST /operations/ — создать операцию (доход или расход).

GET /operations/ — получить список операций.

GET /operations/{id} — получить операцию по id.

PUT /operations/{id} — обновить операцию.

DELETE /operations/{id} — удалить операцию.

При наличии отчётов:

GET /report/summary — сводный баланс за период.

Установка и запуск
bash
git clone https://github.com/SaritoHokage/CashflowTest.git
cd CashflowTest

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# При необходимости — инициализация базы данных
  -python init_db.py  # если есть отдельный скрипт
  -uvicorn app.main:app --reload
№После запуска приложение будет доступно по адресу:

http://localhost:8000/docs — Swagger UI.

http://localhost:8000/redoc — документация .

Тесты
```bash
pytest
```
План развития
Добавить авторизацию пользователей и разделение данных по аккаунтам.

Расширить отчёты (статистика по категориям/периодам).

Добавить экспорт/импорт данных (CSV/Excel).

Дописать интеграционные тесты.
