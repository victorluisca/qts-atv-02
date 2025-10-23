import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool


API_URL = "https://jsonplaceholder.typicode.com/todos"


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/todos", response_model=List[Todo])
async def list_todos():
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        return response.json()


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo_by_id(todo_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/{todo_id}")
        response.raise_for_status()
        return response.json()
