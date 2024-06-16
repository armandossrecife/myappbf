from fastapi.testclient import TestClient
from app.entidades import UserLogin
from main import app_media

cliente = TestClient(app_media)

def test_login_usuario():
    # Create a valid user for testing
    test_user = UserLogin(username="armando", password="armando")

    # Send a POST request with valid credentials
    response = cliente.post("/login", json=test_user.model_dump())
    
    # Assert successful response with status code and access token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    # Send a POST request with invalid username
    invalid_username = UserLogin(username="invalid_user", password="armando")
    response = cliente.post("/login", json=invalid_username.model_dump())

    # Assert bad request with error message
    assert response.status_code == 400
    assert "Incorrect username or password" in response.text