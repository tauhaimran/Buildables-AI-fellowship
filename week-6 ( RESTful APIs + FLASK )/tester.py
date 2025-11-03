# Tauha Imran| Buildables AI Fellowship – Week 6 Task 1  
# [LinkedIn](https://www.linkedin.com/in/tauha-imran-6185b3280/) 
# [GitHub](https://github.com/tauhaimran)
# [Portfolio](https://tauhaimran.github.io/)  

# *** Task 3 — Rewrite in FastAPI with Type Hints ***
# Importing the necessary libraries and classes
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel

# Create a FastAPI instance
app = FastAPI()

# Define a simple API key for authentication (in real apps, use env vars or a database)
API_KEY = "secret"


# -----------------------------
# Define the data models
# -----------------------------

# Model for a full Todo item (with id and task)
class Todo(BaseModel):
    id: int
    task: str

# Model for creating a new Todo (user only provides the task)
class TodoCreate(BaseModel):
    task: str


# In-memory list of todos (our "fake database")
todos: List[Todo] = [Todo(id=1, task="Buy groceries")]


# -----------------------------
# Helper function to verify API key
# -----------------------------
def verify_api_key(x_api_key: Optional[str]):
    """
    Verifies the 'x-api-key' header from the client.
    Raises an HTTP 401 error if the key is missing or incorrect.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )


# -----------------------------
# API Endpoints
# -----------------------------

# GET /todos — Get all to-do items
@app.get("/todos", response_model=List[Todo])
def get_todos(x_api_key: Optional[str] = Header(None)):
    """
    Returns the list of all to-do items.
    Requires a valid API key in the 'x-api-key' header.
    """
    verify_api_key(x_api_key)
    return todos


# POST /todos — Add a new to-do item
@app.post("/todos", response_model=Todo, status_code=201)
def add_todo(todo: TodoCreate, x_api_key: Optional[str] = Header(None)):
    """
    Adds a new to-do to the list.
    Requires a valid API key in the 'x-api-key' header.
    """
    verify_api_key(x_api_key)
    new_todo = Todo(id=len(todos) + 1, task=todo.task)
    todos.append(new_todo)
    return new_todo


# DELETE /todos/{todo_id} — Delete a to-do by ID
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, x_api_key: Optional[str] = Header(None)):
    """
    Deletes a to-do item by its ID.
    Returns 204 No Content if successful.
    Returns 404 if the ID does not exist.
    Requires a valid API key.
    """
    verify_api_key(x_api_key)
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return
    # If the ID was not found, raise an HTTP 404 error
    raise HTTPException(status_code=404, detail="To-do not found")
