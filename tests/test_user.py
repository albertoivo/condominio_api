from fastapi.testclient import TestClient

from app.schemas.user import UserCreate
from app.services.user_service import UserService


def test_create_user(client: TestClient, db_session):
    service = UserService(db_session)
    data = service.create_user(
        UserCreate(nome="Jane", email="jane@example.com", password="secret")
    )

    assert data.nome == "Jane"
    assert data.email == "jane@example.com"


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


def test_login_failure(client: TestClient):
    response = client.post(
        "/login", json={"email": "ivo@nao-existe.com", "password": "123456"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenciais inválidas"


def test_create_user_duplicate_email(client: TestClient, db_session):
    # Primeiro, cria um usuário com sucesso
    user_data = {
        "nome": "Duplicate",
        "email": "duplicate@example.com",
        "password": "secret",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    # Agora, tenta criar o mesmo usuário novamente
    response = client.post("/users", json=user_data)

    # Verifica se a API retorna o erro esperado (400 Bad Request)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email já está em uso"


def test_get_users_successful(client: TestClient, db_session):
    # Cria alguns usuários para testar a listagem
    user_data1 = {
        "nome": "Ivo",
        "email": "ivo@example.com",
        "password": "abc123",
        "role": "admin",
    }
    user_data2 = {
        "nome": "Mari",
        "email": "mari@example.com",
        "password": "abc123",
        "role": "user",
    }
    user_data3 = {"nome": "Cat", "email": "cat@example.com", "password": "abc123"}

    response = client.post("/users", json=user_data1)
    assert response.status_code == 201

    response = client.post("/users", json=user_data2)
    assert response.status_code == 201

    response = client.post("/users", json=user_data3)
    assert response.status_code == 201

    response = client.post(
        "/login", json={"email": "ivo@example.com", "password": "abc123"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # Verifica se retornou pelo menos 3 usuários


def test_get_users_fail(client: TestClient, db_session):
    # Cria alguns usuários para testar a listagem
    user_data1 = {
        "nome": "Ivo",
        "email": "ivo@example.com",
        "password": "abc123",
        "role": "admin",
    }
    user_data2 = {
        "nome": "Mari",
        "email": "mari@example.com",
        "password": "abc123",
        "role": "user",
    }
    user_data3 = {"nome": "Cat", "email": "cat@example.com", "password": "abc123"}

    response = client.post("/users", json=user_data1)
    assert response.status_code == 201

    response = client.post("/users", json=user_data2)
    assert response.status_code == 201

    response = client.post("/users", json=user_data3)
    assert response.status_code == 201

    response = client.post(
        "/login", json={"email": "mari@example.com", "password": "abc123"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    assert response.status_code == 403


def test_delete_users(client: TestClient, db_session):
    # Cria alguns usuários para testar a listagem
    user_data1 = {
        "nome": "Ivo",
        "email": "ivo@example.com",
        "password": "abc123",
        "role": "admin",
    }
    user_data2 = {
        "nome": "Mari",
        "email": "mari@example.com",
        "password": "abc123",
        "role": "user",
    }
    user_data3 = {"nome": "Cat", "email": "cat@example.com", "password": "abc123"}

    response = client.post("/users", json=user_data1)
    assert response.status_code == 201

    response = client.post("/users", json=user_data2)
    assert response.status_code == 201

    response = client.post("/users", json=user_data3)
    assert response.status_code == 201

    response = client.post(
        "/login", json={"email": "ivo@example.com", "password": "abc123"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data

    response = client.get(
        "/users", headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # Verifica se retornou pelo menos 3 usuários

    # Remove o usuário criado
    user_id = data[0]["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Usuário removido com sucesso"


def test_get_user_by_id(client: TestClient, db_session):
    # Cria alguns usuários para testar a listagem
    user_data1 = {
        "nome": "Ivo",
        "email": "ivo@example.com",
        "password": "abc123",
        "role": "admin",
    }
    user_data2 = {
        "nome": "Mari",
        "email": "mari@example.com",
        "password": "abc123",
        "role": "user",
    }
    user_data3 = {"nome": "Cat", "email": "cat@example.com", "password": "abc123"}

    response = client.post("/users", json=user_data1)
    assert response.status_code == 201

    response = client.post("/users", json=user_data2)
    assert response.status_code == 201

    response = client.post("/users", json=user_data3)
    assert response.status_code == 201

    response = client.get("/users/1")
    data = response.json()
    assert data["nome"] == "Ivo"
    assert data["email"] == "ivo@example.com"
    assert data["id"] == 1
    assert data["role"] == "admin"


def test_get_users_me(client: TestClient, db_session):
    user_data1 = {"nome": "Cat", "email": "cat@example.com", "password": "abc123"}

    response = client.post("/users", json=user_data1)
    assert response.status_code == 201

    response = client.post(
        "/login", json={"email": "cat@example.com", "password": "abc123"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    data = response.json()
    assert data["nome"] == "Cat"
