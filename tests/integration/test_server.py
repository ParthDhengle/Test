from fastapi.testclient import TestClient
from main2 import app

client=TestClient(app)

def test_home():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()=={"status":"this is home!! welcome"}
