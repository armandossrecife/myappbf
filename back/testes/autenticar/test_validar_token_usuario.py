from fastapi.testclient import TestClient
from app.entidades import UserLogin
from main import app_media

cliente = TestClient(app_media)

def test_valid_token():
    # Loga com um usuario valido
    test_user = UserLogin(username="armando", password="armando")
    response = cliente.post("/login", json=test_user.model_dump())
    
    # Assert successful response with status code and access token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

    # Captura as informacoes do token de acesso
    acess_token = data["access_token"]
    header = {"Authorization": f"Bearer {acess_token}"}

    # Faz uma nova requisicao com um token valido
    new_response = cliente.get("/users/armando", headers=header)
    assert new_response.status_code == 200
        
def test_invalid_token():
    # Loga com um usuario valido
    test_user = UserLogin(username="armando", password="armando")
    response = cliente.post("/login", json=test_user.model_dump())
    
    # Assert successful response with status code and access token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

    # Gera um token invalido
    header = {"Authorization": f"Bearer ???"}
    # Faz a requisicao com um token invalido
    new_response = cliente.get("/users/armando", headers=header)
    assert new_response.status_code == 401