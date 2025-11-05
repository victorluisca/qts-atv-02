from typing import List

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool


class CreateTodo(BaseModel):
    userId: int
    title: str
    completed: bool


API_URL = "https://jsonplaceholder.typicode.com/todos"


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/todos", response_model=List[Todo])
def list_todos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    try:
        response = requests.get(f"{API_URL}/{todo_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/todos/", status_code=201, response_model=Todo)
def create_todo(todo: CreateTodo):
    try:
        response = requests.post(API_URL, json=todo.model_dump())
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
