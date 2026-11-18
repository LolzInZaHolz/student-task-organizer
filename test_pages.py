import pytest


@pytest.mark.parametrize("path", ["/", "/tasks", "/week", "/warnings"])
def test_pages_load(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert "Student Task Organizer" in response.text
