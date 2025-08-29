import pytest

# --------- AUTH ---------
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# def test_create_user(client):
#     response = client.post("/api/v1/user/", json={
#                                             "email": "test@example.com",
#                                             "role": "admin",
#                                             "first_name": "string",
#                                             "last_name": "string",
#                                             "department_id": "string",
#                                             "DOB": "2025-08-29",
#                                             "password": "string",
#                                             "student_id": "string",
#                                             "teacher_id": "string",
#                                             "school_year": "string"})
#     assert response.status_code == 201
#     assert response.json()["email"] == "test@example.com"

def test_get_user(client):
    response = client.get("/api/v1/user/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_login_success(client):
#     response = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "string"})
#     assert response.status_code == 200
#     assert "access_token" in response.json()

