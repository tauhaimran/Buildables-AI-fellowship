# Tauha Imran| Buildables AI Fellowship – Week 6 Task 1  
# [LinkedIn](https://www.linkedin.com/in/tauha-imran-6185b3280/) 
# [GitHub](https://github.com/tauhaimran)
# [Portfolio](https://tauhaimran.github.io/)  

# *** Task 2 — Rewrite in FastAPI with Type Hints ***
from typing import List # this is for the type hints
from fastapi import FastAPI # this is for making the FastAPI app
from pydantic import BaseModel # From Pydantic, which is a library FastAPI uses for data validation and serialization

#making the app..
app = FastAPI()


#making the Todo class
class Todo( BaseModel):
    id : int
    task : str

# a class used for creating new todos , client only give the task , id is set by this app
class TodoCreate(BaseModel):
    task: str

#  creating an in-memory list to store todos ( aka a fake database )
todos: List[Todo] = [ Todo( id = 1 , task = "Buy groceries" ) ]

# defining the GET /todos endpoint
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos # the list of todos

# defining the POST /todos endpoint
@app.post("/todos", response_model=Todo ,status_code= 201)  # 201 is the created status code
def add_todo(todo : TodoCreate):
    new_todo = Todo( id = len(todos)+1 , task=todo.task) # create a new todo item
    todos.append(new_todo) # add the new todo to the list
    return new_todo # return the new todo item