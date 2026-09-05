
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def unique_email():
    return f"test_{uuid4().hex[:8]}@example.com"


def test_server_start():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "FocusFlow API is running"


def test_user_registration():
    email = unique_email()

    response = client.post(
        "/auth/register",
        json={
            "name": "Gayatri",
            "email": email,
            "password": "Test@123"
        }
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["message"] == "Registration successful"
    assert data["user"]["name"] == "Gayatri"
    assert data["user"]["email"] == email
    assert data["user"]["role"] == "user"


def test_valid_login():
    email = unique_email()
    password = "Test@123"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Gayatri Login",
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code in [200, 201]

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["user"]["email"] == email
    assert data["user"]["role"] == "user"


def test_invalid_login():
    email = unique_email()
    password = "Test@123"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Invalid Login User",
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code in [200, 201]

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"

