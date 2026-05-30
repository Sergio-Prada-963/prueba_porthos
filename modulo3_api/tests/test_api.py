from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def token_valido() -> str:
    respuesta = client.post("/auth/login", json={"usuario": "admin", "contrasena": "admin123"})
    return respuesta.json()["access_token"]


def test_login_exitoso():
    respuesta = client.post("/auth/login", json={"usuario": "admin", "contrasena": "admin123"})
    assert respuesta.status_code == 200
    assert respuesta.json()["token_type"] == "bearer"
    assert respuesta.json()["access_token"]


def test_crear_tarea_con_token():
    cabeceras = {"Authorization": f"Bearer {token_valido()}"}
    respuesta = client.post(
        "/tasks",
        headers=cabeceras,
        json={"titulo": "Preparar entrega", "descripcion": "Revisar checklist", "estado": "pendiente"},
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["titulo"] == "Preparar entrega"
    assert cuerpo["estado"] == "pendiente"
    assert "id" in cuerpo


def test_rechazo_sin_token():
    respuesta = client.get("/tasks")
    assert respuesta.status_code == 401
