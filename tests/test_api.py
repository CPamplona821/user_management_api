import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "test_user", "email": "test@example.com", "password": "test_password", "role": "user"})
    assert response.status_code == 200

def test_login_user():
    response = client.post("/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

def test_read_users_me():
    response = client.get("/users/me", headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200

def test_read_users():
    response = client.get("/users/", headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200

def test_read_user():
    response = client.get("/users/USER_ID", headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200

def test_update_user():
    response = client.put("/users/USER_ID", json={"username": "updated_username", "email": "updated_email@example.com", "password": "updated_password", "role": "user"}, headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200

def test_delete_user():
    response = client.delete("/users/USER_ID", headers={"Authorization": "Bearer YOUR_ACCESS_TOKEN"})
    assert response.status_code == 200