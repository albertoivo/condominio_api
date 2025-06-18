from fastapi.testclient import TestClient

from app.schemas.user import UserCreate
from app.services.user_service import UserService


def test_login_success(client: TestClient, db_session):
    service = UserService(db_session)
    service.create_user(
        UserCreate(nome="John", email="john@example.com", password="secret")
    )

    response = client.post(
        "/login", json={"email": "john@example.com", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
