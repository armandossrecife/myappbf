from fastapi.testclient import TestClient
from entidades import UserLogin
from main import app  # Replace with your app import path

def test_login_successful():
  with TestClient(app) as client:
    # Create a valid user for testing
    test_user = UserLogin(username="armando", password="armando")

    # Send a POST request with valid credentials
    response = client.post("/login", json=test_user.model_dump())

    # Assert successful response with status code and access token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
  with TestClient(app) as client:
    # Send a POST request with invalid username
    invalid_username = UserLogin(username="invalid_user", password="armando")
    response = client.post("/login", json=invalid_username.model_dump())

    # Assert bad request with error message
    assert response.status_code == 400
    assert "Incorrect username or password" in response.text