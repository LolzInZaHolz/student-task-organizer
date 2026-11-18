from fastapi.testclient import TestClient

from main import app, courses_db

client = TestClient(app)


def setup_function():
    # Clear the in-memory database before each test
    courses_db.clear()


def add_course(**overrides):
    payload = {"name": "Software Engineering", "code": "CS301"}
    payload.update(overrides)
    return client.post("/api/courses", json=payload)


def test_add_course():
    response = add_course(color="#2563EB")
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Software Engineering",
        "code": "CS301",
        "color": "#2563EB",
    }


def test_add_course_trims_whitespace():
    response = add_course(name="  Databases  ", code="  CS202  ")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Databases"
    assert data["code"] == "CS202"


def test_blank_code_becomes_null():
    response = add_course(code="   ")
    assert response.status_code == 201
    assert response.json()["code"] is None


def test_add_course_empty_name():
    for name in ("", "   "):
        response = add_course(name=name)
        assert response.status_code == 400


def test_add_course_rejects_duplicate_name():
    assert add_course(name="Math").status_code == 201

    response = add_course(name="  math  ")
    assert response.status_code == 409


def test_add_course_rejects_invalid_color():
    response = add_course(color="blue")
    assert response.status_code == 422


def test_get_courses_is_empty_at_start():
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_courses():
    add_course(name="Databases", code="CS202")

    response = client.get("/api/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Databases"


def test_get_course_by_id():
    created = add_course().json()

    response = client.get(f"/api/courses/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_course_not_found():
    response = client.get("/api/courses/999")
    assert response.status_code == 404


def test_ids_are_not_reused_after_a_middle_course_is_removed():
    add_course(name="Algebra")
    middle = add_course(name="Biology").json()
    last = add_course(name="Chemistry").json()

    # Simulates a future delete endpoint removing a course from the middle.
    courses_db.remove(next(course for course in courses_db if course.id == middle["id"]))

    new_course = add_course(name="Databases").json()
    assert new_course["id"] == last["id"] + 1
    assert len({course.id for course in courses_db}) == 3


def test_index_serves_the_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "Student Task Organizer" in response.text
