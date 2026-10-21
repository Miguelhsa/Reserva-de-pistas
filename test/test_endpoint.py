from fastapi.testclient import TestClient
from interfaz.app import app
from interfaz.routers.reservas import get_ruta
from persistencia.repositorio import guardar

cliente = TestClient(app)

datos_reserva = {
    "pista": 1,
    "usuarios": [
        {"id": 1, "nombre": "Miguel", "apellidos": "Hidalgo", "rol": "socio"},
        {"id": 2, "nombre": "Carlos", "apellidos": "Hidalgo", "rol": "socio"}
    ],
    "fecha_inicio": "2026-10-12T18:00:00",
    "fecha_fin": "2026-10-12T19:30:00",
}

respuesta_esperada = {
    "pista": 1,
    "usuarios": [
        {"nombre": "Miguel", "apellidos": "Hidalgo"},
        {"nombre": "Carlos", "apellidos": "Hidalgo"}
    ],
    "fecha_inicio": "2026-10-12T18:00:00",
    "fecha_fin": "2026-10-12T19:30:00",
}

datos_reserva_limite = {
    "pista": 1,
    "usuarios": [
        {"id": 1, "nombre": "Miguel", "apellidos": "Hidalgo", "rol": "socio"},
        {"id": 2, "nombre": "Carlos", "apellidos": "Hidalgo", "rol": "socio"}
    ],
    "fecha_inicio": "2026-10-12T19:30:00",
    "fecha_fin": "2026-10-12T21:30:00",
}

datos_reserva_solapa = {
    "pista": 1,
    "usuarios": [
        {"id": 1, "nombre": "Miguel", "apellidos": "Hidalgo", "rol": "socio"},
        {"id": 2, "nombre": "Carlos", "apellidos": "Hidalgo", "rol": "socio"}
    ],
    "fecha_inicio": "2026-10-12T18:30:00",
    "fecha_fin": "2026-10-12T21:00:00",
}
RUTA_PRUEBA = "test_reservas.json"

def get_ruta_test() -> str:
    return RUTA_PRUEBA

def test_guardar_reservas():
    guardar([],RUTA_PRUEBA)
    app.dependency_overrides[get_ruta] = get_ruta_test
    escribir = cliente.post("/reserva",json = datos_reserva )
    assert escribir.status_code == 200
    assert escribir.json() == respuesta_esperada
    app.dependency_overrides.clear()

def test_reserva_limite():
    #creo otra reserva que este al limite de solapar
    guardar([],RUTA_PRUEBA)
    app.dependency_overrides[get_ruta] = get_ruta_test
    reserva = cliente.post("/reserva", json = datos_reserva)
    escribir = cliente.post("/reserva", json = datos_reserva_limite)
    assert reserva.status_code == 200
    assert escribir.status_code == 200
    #assert escribir.json() == respuesta_esperada
    app.dependency_overrides.clear()

def test_reserva_solapa():
    guardar([],RUTA_PRUEBA)
    app.dependency_overrides[get_ruta] = get_ruta_test
    reserva = cliente.post("/reserva", json = datos_reserva)
    escribir = cliente.post("/reserva", json = datos_reserva_solapa)
    assert reserva.status_code == 200
    assert escribir.status_code == 409
    assert escribir.json() == {"detail":"Esa franja ya esta reservada"}
    app.dependency_overrides.clear()