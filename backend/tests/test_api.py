from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze():
    response = client.post("/api/analyze", json={
        "language": "python",
        "code": "def hello(): print('world')"
    })
    assert response.status_code == 200
    assert "tokens" in response.json()
    assert response.json()["total_tokens"] > 0

def test_compare():
    response = client.post("/api/compare", json={
        "language": "python",
        "code_a": "def hello(): print('world')",
        "code_b": "def hello_there(): print('world')"
    })
    assert response.status_code == 200
    assert "similarity" in response.json()
    assert response.json()["similarity"] > 0
