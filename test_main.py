from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API funcionando"}


def test_somar():
    response = client.get("/somar/5/3")
    assert response.status_code == 200
    assert response.json() == {"resultado": 8}


def test_multiplicar():
    response = client.get("/multiplicar/3/2")
    assert response.status_code == 200
    assert response.json() == {"resultado": 6}
