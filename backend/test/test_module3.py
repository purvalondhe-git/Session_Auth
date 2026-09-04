import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_sessions_without_login():
    response = client.get("/auth/sessions")

    assert response.status_code == 401


def test_admin_users_without_login():
    response = client.get("/admin/users")

    assert response.status_code == 401