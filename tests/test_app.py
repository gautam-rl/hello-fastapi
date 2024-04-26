from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

print("Test script completed successfully, no errors.")
