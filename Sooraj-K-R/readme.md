# FastAPI Todo API with API Key Authentication

A FastAPI-based Todo CRUD application secured with API Key authentication using the `X-API-Key` header. Built with Pydantic validation and query-based filtering.

## Features

- **API Key Authentication** — All endpoints (except `/`) are protected via the `X-API-Key` header
- **Full CRUD Operations** — Create, Read, Update, and Delete todos
- **Mark as Complete** — Dedicated `PATCH` endpoint to mark a todo as done
- **Priority Filtering** — Filter todos by priority (`low`, `medium`, `high`)
- **Status Filtering** — Filter todos by checked/unchecked status
- **Pydantic Validation** — Input validation with custom error responses

## Tech Stack

- **FastAPI** — Web framework
- **Pydantic** — Data validation
- **python-dotenv** — Environment variable management

## Setup

1. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn python-dotenv
   ```

2. **Create a `.env` file** with your API key:

   ```
   API_KEY="your-secret-key"
   ```

3. **Run the server:**

   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

| Method   | Endpoint               | Description              | Auth Required |
| -------- | ---------------------- | ------------------------ | ------------- |
| `GET`    | `/`                    | Welcome message          | No            |
| `POST`   | `/todos`               | Create a new todo        | Yes           |
| `GET`    | `/todos`               | List all todos           | Yes           |
| `GET`    | `/todos/{id}`          | Get a specific todo      | Yes           |
| `PUT`    | `/todos/{id}`          | Update a todo            | Yes           |
| `DELETE` | `/todos/{id}`          | Delete a todo            | Yes           |
| `PATCH`  | `/todos/{id}/complete` | Mark a todo as completed | Yes           |

### Query Parameters (GET /todos)

- `priority` — Filter by priority: `low`, `medium`, or `high`
- `checked` — Filter by status: `true` or `false`

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high"}'
```

## Author

**Sooraj K R**
