from fastapi.testclient import TestClient
from main import app, courses_db

client = TestClient(app)


def setup_function():
    # Clear the in-memory database before each test
    courses_db.clear()


def test_add_course():
    response = client.post(
        "/api/courses",
        json={"name": "Software Engineering", "code": "CS301"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Software Engineering"
    assert data["code"] == "CS301"
    assert data["id"] == 1


def test_add_course_empty_name():
    response = client.post(
        "/api/courses",
        json={"name": "   ", "code": "CS301"}
    )
    assert response.status_code == 400


def test_get_courses():
    client.post("/api/courses", json={"name": "Databases", "code": "CS202"})
    response = client.get("/api/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Databases"
    