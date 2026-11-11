from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "alive"}

def test_create_order_success():
    res = client.post("/orders", json={"item_id": "sku-123", "quantity": 2})
    assert res.status_code == 201
    assert res.json()["status"] == "created"

def test_create_order_invalid_quantity():
    res = client.post("/orders", json={"item_id": "sku-123", "quantity": 0})
    assert res.status_code == 400