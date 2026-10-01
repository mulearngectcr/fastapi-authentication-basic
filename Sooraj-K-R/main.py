import os
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
SECRET_API_KEY = os.getenv("API_KEY")

app = FastAPI()
todos_db = []
ALLOWED_PRIORITIES = ["low", "medium", "high"]

api_key_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

# 3. Dependency Function to validate the key
def get_api_key(api_key: str = Depends(api_key_header_scheme)):
    if api_key is None:
        raise HTTPException(status_code=403, detail="Forbidden: API key header is missing entirely")
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")
    return api_key


class ToDoItem(BaseModel):
    id: int
    title: str
    checked: bool
    priority: str


class ToDoCreate(BaseModel):
    title: str = Field(..., min_length=3)
    checked: bool = False
    priority: str = "medium"


class ToDoUpdate(BaseModel):
    title: str = Field(..., min_length=3)
    checked: bool = False
    priority: str = "medium"


def validate_priority(priority: str):
    if priority not in ALLOWED_PRIORITIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid priority '{priority}'. Allowed: {ALLOWED_PRIORITIES}",
        )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    messages = []
    for error in exc.errors():
        field = error["loc"][-1]
        messages.append(f"'{field}': {error['msg']}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation failed", "errors": messages},
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API. This endpoint is public!"}


@app.post("/todos", status_code=201)
def insert_item(item: ToDoCreate, api_key: str = Depends(get_api_key)):
    validate_priority(item.priority)
    new_id = len(todos_db) + 1
    new_item = ToDoItem(id=new_id, title=item.title, checked=item.checked, priority=item.priority)
    todos_db.append(new_item)
    return new_item


@app.get("/todos")
def get_all(priority: Optional[str] = None, checked: Optional[bool] = None, api_key: str = Depends(get_api_key)):
    filtered_todos = todos_db

    if priority:
        filtered_todos = [todo for todo in filtered_todos if todo.priority == priority]

    if checked is not None:
        filtered_todos = [todo for todo in filtered_todos if todo.checked == checked]

    return filtered_todos


@app.get("/todos/{id}")
def get_item(id: int, api_key: str = Depends(get_api_key)):
    for i in todos_db:
        if i.id == id:
            return i
    raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")


@app.put("/todos/{id}")
def update_item(id: int, item: ToDoUpdate, api_key: str = Depends(get_api_key)):
    validate_priority(item.priority)
    for index, i in enumerate(todos_db):
        if i.id == id:
            updated = ToDoItem(id=id, title=item.title, checked=item.checked, priority=item.priority)
            todos_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")


@app.delete("/todos/{id}")
def delete_item(id: int, api_key: str = Depends(get_api_key)):
    for i in todos_db:
        if i.id == id:
            todos_db.remove(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")


# Extra endpoint from your original code protected for completeness[cite: 1]
@app.patch("/todos/{id}/complete")
def mark_as_done(id: int, api_key: str = Depends(get_api_key)):
    for i in todos_db:
        if i.id == id:
            i.checked = True
            return i
    raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")