from app.config import app
import sys
import os
from fastapi.testclient import TestClient

# Para cambiar de ruta y poder importar el módulo app.config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)


def test_example1():
    response = client.get("/example/example1")
    assert response.status_code == 200
    assert response.text == '"Example1"'


def test_post_example2():
    data = {
        "email": "test@example.com",
        "pass": "password123",
        "pass_confirm": "password123",
        "name": "John",
        "last_name": "Doe",
        "last_name2": "Smith",
        "run": "123456789",
        "phone": "123456789",
        "phone2": "987654321"
    }

    response = client.post("/example/example2", json=data)
    
    assert response.status_code == 201
    assert response.text



def test_get_example2():
    response = client.get("/example/example2?name=example")
    assert response.status_code == 200
    assert response.json() == {"name": "example", "other_field": "value"}


def test_put_example2():
    data = {"name": "example", "other_field": "updated_value"}
    response = client.put("/example/example2", json=data)
    assert response.status_code == 200
    assert response.text == "Ok"


def test_delete_example2():
    response = client.delete("/example/example2?name=example")
    assert response.status_code == 200
    assert response.json() == {"message": "Data deleted successfully"}
