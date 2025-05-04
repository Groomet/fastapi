# Task Management API

Система управления задачами на FastAPI с автоматическим расчетом приоритета и аутентификацией пользователей.

## Возможности

- Аутентификация пользователей с помощью JWT токенов
- Управление задачами (CRUD-операции)
- Автоматический расчет приоритета задачи на основе:
  - Времени с момента создания
  - Статуса задачи
  - Приоритета, заданного пользователем
- База данных SQLite с поддержкой асинхронности
- Покрытие тестами
- RESTful API
- Документация Swagger UI

## Структура проекта

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   └── tasks.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── priority.py
│   │   └── security.py
│   ├── crud/
│   │   ├── task.py
│   │   └── user.py
│   ├── models/
│   │   ├── task.py
│   │   └── user.py
│   └── schemas/
│       ├── task.py
│       └── user.py
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
├── requirements.txt
├── main.py
└── README.md
```

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
```

2. Активируйте виртуальное окружение:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта (опционально):
```env
SECRET_KEY=your-secret-key
DEBUG=True
```

## Запуск приложения

Для запуска сервера в режиме разработки:
```bash
python main.py
```

API будет доступен по адресу `http://localhost:8000`

## Документация API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Эндпоинты API

### Аутентификация

- `POST /api/v1/auth/register` - Регистрация нового пользователя
- `POST /api/v1/auth/login` - Вход и получение токена

### Задачи

- `GET /api/v1/tasks/` - Получить все задачи (отсортированы по приоритету)
- `POST /api/v1/tasks/` - Создать новую задачу
- `GET /api/v1/tasks/{task_id}` - Получить конкретную задачу
- `PUT /api/v1/tasks/{task_id}` - Обновить задачу
- `DELETE /api/v1/tasks/{task_id}` - Удалить задачу

## Алгоритм приоритета задачи

Приоритет задачи рассчитывается на основе:
1. Приоритета, заданного пользователем (от 0.0 до 1.0)
2. Времени с момента создания (срочность увеличивается со временем)
3. Статуса задачи (разные множители для разных статусов)

Формула:
```
final_priority = base_priority * (1 + time_factor) * status_factor
```

## Запуск тестов

Для запуска тестов:
```bash
pytest
```

## Лицензия

MIT