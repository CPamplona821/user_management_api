import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "role": "user"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user():
    response = client.post("/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_current_user():
    login_response = client.post("/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    access_token = login_response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_password_reset_request():
    response = client.post("/password-reset/request", json={"email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json()["detail"] == "Password reset link sent to your email."

def test_password_reset_confirm():
    response = client.post("/password-reset/confirm/some-token", json={"new_password": "newpassword"})
    assert response.status_code == 200
    assert response.json()["detail"] == "Password updated successfully."