# Task Management API

A FastAPI-based task management system with automatic priority calculation and user authentication.

## Features

- User authentication with JWT tokens
- Task management (CRUD operations)
- Automatic task prioritization based on:
  - Time since creation
  - Task status
  - User-defined priority
- SQLite database with async support
- Comprehensive test coverage
- RESTful API design
- Swagger UI documentation

## Project Structure

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

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory (optional):
```env
SECRET_KEY=your-secret-key
DEBUG=True
```

## Running the Application

To run the development server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Tasks

- `GET /api/v1/tasks/` - Get all tasks (sorted by priority)
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

## Task Priority Algorithm

The task priority is calculated based on:
1. User-defined priority (0.0 to 1.0)
2. Time since creation (urgency increases with time)
3. Task status (different multipliers for different statuses)

The formula is:
```
final_priority = base_priority * (1 + time_factor) * status_factor
```

## Running Tests

To run the test suite:
```bash
pytest
```

## License

MIT