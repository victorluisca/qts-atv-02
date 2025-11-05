# type: ignore
from unittest.mock import Mock, patch

import pytest
import requests
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_todo():
    """Fixture that returns a sample todo dict"""
    return {"userId": 1, "id": 1, "title": "Test Todo", "completed": False}


@pytest.fixture
def mock_todos_list(mock_todo):
    """Fixture that returns a list of todos"""
    return [
        mock_todo,
        {"userId": 1, "id": 2, "title": "Another Todo", "completed": True},
    ]


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@patch("app.main.requests.get")
def test_list_todos_success(mock_get, mock_todos_list):
    """Test successful retrieval of todos list"""
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = mock_todos_list
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Execute
    response = client.get("/todos")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Test Todo"
    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/todos")


@patch("app.main.requests.get")
def test_list_todos_failure(mock_get):
    """Test failure when retrieving todos list"""
    # Setup mock to raise RequestException
    mock_get.side_effect = requests.RequestException("Connection error")

    # Execute
    response = client.get("/todos")

    # Assert
    assert response.status_code == 500
    assert "Connection error" in response.json()["detail"]


@patch("app.main.requests.get")
def test_get_todo_by_id_success(mock_get, mock_todo):
    """Test successful retrieval of a single todo"""
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = mock_todo
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Execute
    response = client.get("/todos/1")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test Todo"
    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/todos/1")


@patch("app.main.requests.get")
def test_get_todo_by_id_failure(mock_get):
    """Test failure when retrieving a single todo"""
    # Setup mock to raise RequestException
    mock_get.side_effect = requests.RequestException("Todo not found")

    # Execute
    response = client.get("/todos/999")

    # Assert
    assert response.status_code == 500
    assert "Todo not found" in response.json()["detail"]


@patch("app.main.requests.post")
def test_create_todo_success(mock_post):
    """Test successful creation of a todo"""
    # Setup mock
    new_todo = {"userId": 1, "title": "New Todo", "completed": False}
    created_todo = {**new_todo, "id": 201}

    mock_response = Mock()
    mock_response.json.return_value = created_todo
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    # Execute
    response = client.post("/todos/", json=new_todo)

    # Assert
    assert response.status_code == 201
    assert response.json()["id"] == 201
    assert response.json()["title"] == "New Todo"
    mock_post.assert_called_once()


@patch("app.main.requests.post")
def test_create_todo_failure(mock_post):
    """Test failure when creating a todo"""
    # Setup mock to raise RequestException
    mock_post.side_effect = requests.RequestException("Failed to create todo")

    # Execute
    new_todo = {"userId": 1, "title": "New Todo", "completed": False}
    response = client.post("/todos/", json=new_todo)

    # Assert
    assert response.status_code == 500
    assert "Failed to create todo" in response.json()["detail"]
