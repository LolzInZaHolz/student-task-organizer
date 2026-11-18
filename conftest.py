import pytest
from fastapi.testclient import TestClient

from main import app
from store import courses_db, tasks_db


@pytest.fixture(autouse=True)
def clean_databases():
    """Give every test an empty database."""
    courses_db.clear()
    tasks_db.clear()
    yield
    courses_db.clear()
    tasks_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def course(client):
    """Create one course and return its JSON representation."""
    response = client.post(
        "/api/courses",
        json={"name": "Software Engineering", "code": "CS301"},
    )
    assert response.status_code == 201
    return response.json()
