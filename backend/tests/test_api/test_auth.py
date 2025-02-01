from fastapi.testclient import TestClient
import pytest
from app.core.security import create_access_token

def test_login(client: TestClient, db):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json() 