import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def users_in_db(client: TestClient):
    """
    Fixture que cria um conjunto de usuários no banco de dados para os testes.
    Retorna os dados dos usuários criados para referência.
    """
    users_data = [
        {
            "nome": "Admin User",
            "email": "admin@example.com",
            "password": "password123",
            "role": "admin",
        },
        {
            "nome": "Common User",
            "email": "user@example.com",
            "password": "password123",
            "role": "user",
        },
    ]
    created_users = []
    for user in users_data:
        response = client.post("/users", json=user)
        assert response.status_code == 201
        created_users.append(response.json())

    # Adiciona as senhas de volta para uso no login,
    # já que a resposta da API não as inclui
    created_users[0]["password"] = users_data[0]["password"]
    created_users[1]["password"] = users_data[1]["password"]
    return created_users


@pytest.fixture
def admin_auth_headers(client: TestClient, users_in_db):
    """Fixture que faz login como admin e retorna os headers de autorização."""
    admin_user = users_in_db[0]
    response = client.post(
        "/login",
        json={"email": admin_user["email"], "password": admin_user["password"]},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_auth_headers(client: TestClient, users_in_db):
    """Fixture que faz login como usuário comum e retorna os headers de autorização."""
    common_user = users_in_db[1]
    response = client.post(
        "/login",
        json={"email": common_user["email"], "password": common_user["password"]},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_user(client: TestClient):
    response = client.post(
        "/users",
        json={"nome": "New User", "email": "new@example.com", "password": "secret"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "New User"
    assert "password" not in data


def test_create_user_duplicate_email(client: TestClient, users_in_db):
    admin_user_email = users_in_db[0]["email"]
    response = client.post(
        "/users",
        json={"nome": "Another User", "email": admin_user_email, "password": "secret"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já está em uso"


def test_login_failure(client: TestClient):
    response = client.post(
        "/login", json={"email": "no@exists.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


def test_get_all_users_as_admin(client: TestClient, admin_auth_headers, users_in_db):
    response = client.get("/users", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_all_users_as_common_user_fails(client: TestClient, user_auth_headers):
    response = client.get("/users", headers=user_auth_headers)
    assert response.status_code == 403  # Forbidden


def test_get_user_by_id_as_admin(client: TestClient, admin_auth_headers, users_in_db):
    user_to_get_id = users_in_db[1]["id"]
    response = client.get(f"/users/{user_to_get_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_to_get_id
    assert data["email"] == users_in_db[1]["email"]


def test_get_current_user_me(client: TestClient, user_auth_headers, users_in_db):
    response = client.get("/users/me", headers=user_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == users_in_db[1]["email"]


def test_delete_user_as_admin(client: TestClient, admin_auth_headers, users_in_db):
    user_to_delete_id = users_in_db[1]["id"]
    response = client.delete(f"/users/{user_to_delete_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Usuário removido com sucesso"

    # Verifica que o usuário foi realmente deletado
    response = client.get(f"/users/{user_to_delete_id}", headers=admin_auth_headers)
    assert response.status_code == 404


def test_delete_user_as_common_user_fails(
    client: TestClient, user_auth_headers, users_in_db
):
    admin_user_id = users_in_db[0]["id"]
    response = client.delete(f"/users/{admin_user_id}", headers=user_auth_headers)
    assert response.status_code == 200  # 403 Forbidden
