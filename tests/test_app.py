from fastapi.testclient import TestClient
import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

print("Test script completed successfully, no errors.")
