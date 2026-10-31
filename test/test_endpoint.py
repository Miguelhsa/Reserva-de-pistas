# 'Navegador falso' para hacer peticiones a la app sin arrancar el servidor
from fastapi.testclient import TestClient
# La app real, la que se va a probar
from interfaz.app import app
# La 'cafetera' real de la ruta, para poder sustituirla en los tests
from interfaz.routers.reservas import get_ruta
# Para dejar el archivo de prueba vacío ([]) antes de cada test
from persistencia.repositorio import guardar_reserva


# Crea el cliente apuntando a la app
cliente = TestClient(app)

# Datos de una reserva libre, en formato de ENTRADA (con id y rol)
datos_reserva = {
    "pista": 1,
    "usuarios": [
        {"id": 1, "nombre": "Miguel", "apellidos": "Hidalgo", "rol": "socio"},
        {"id": 2, "nombre": "Carlos", "apellidos": "Hidalgo", "rol": "socio"}
    ],
    "fecha_inicio": "2026-10-12T18:00:00",
    "fecha_fin": "2026-10-12T19:30:00",
}

# Lo que debe devolver la API para esa reserva, en formato de SALIDA (sin id ni rol)
respuesta_esperada = {
    "pista": 1,
    "usuarios": [
        {"nombre": "Miguel", "apellidos": "Hidalgo"},
        {"nombre": "Carlos", "apellidos": "Hidalgo"}
    ],
    "fecha_inicio": "2026-10-12T18:00:00",
    "fecha_fin": "2026-10-12T19:30:00",
}

# Reserva pegada a la anterior: empieza a las 19:30, justo cuando acaba la otra
datos_reserva_limite = {
    "pista": 1,
    "usuarios": [
        {"id": 1, "nombre": "Miguel", "apellidos": "Hidalgo", "rol": "socio"},
        {"id": 2, "nombre": "Carlos", "apellidos": "Hidalgo", "rol": "socio"}
    ],
    "fecha_inicio": "2026-10-12T19:30:00",
    "fecha_fin": "2026-10-12T21:30:00",
}

# Reserva que se pisa con la primera (de 18:30 a 21:00)
datos_reserva_solapa = {
    "pista": 1,
    "usuarios": [
        {"id": 1, "nombre": "Miguel", "apellidos": "Hidalgo", "rol": "socio"},
        {"id": 2, "nombre": "Carlos", "apellidos": "Hidalgo", "rol": "socio"}
    ],
    "fecha_inicio": "2026-10-12T18:30:00",
    "fecha_fin": "2026-10-12T21:00:00",
}
# Archivo de prueba: los tests escriben aquí, nunca en reservas.json
RUTA_PRUEBA = "test_reservas.json"
# EN CONSTRUCCIÓN (revisar el nombre de esta constante)
RUTA_RESERVAS = "test_pistas.json"

# 'Cafetera de juguete': devuelve la ruta de prueba en vez de la real
def get_ruta_test() -> str:
    # Devuelve la constante
    return RUTA_PRUEBA

# TEST: una reserva libre se acepta (200) y la respuesta no lleva id ni rol
def test_reserva_libre_se_acepta():
    # Preparar: archivo de prueba vacío
    guardar_reserva([],RUTA_PRUEBA)
    # Preparar: cuando el endpoint pida get_ruta, FastAPI le dará get_ruta_test
    app.dependency_overrides[get_ruta] = get_ruta_test
    # Ejecutar: POST con la reserva (como si fuera un socio desde la web)
    respuesta = cliente.post("/reserva",json = datos_reserva )
    # Comprobar: se aceptó
    assert respuesta.status_code == 200
    # Comprobar: la respuesta tiene la forma de ReservaOut
    assert respuesta.json() == respuesta_esperada
    # Limpiar: quita la sustitución para no afectar a otros tests
    app.dependency_overrides.clear()

# TEST: una reserva pegada a otra (empieza cuando acaba la anterior) se acepta
def test_reserva_limite():
    #creo otra reserva que este al limite de solapar
    # Preparar: archivo de prueba vacío
    guardar_reserva([],RUTA_PRUEBA)
    # Preparar: usar la ruta de prueba
    app.dependency_overrides[get_ruta] = get_ruta_test
    # Preparar: ocupar la franja de 18:00 a 19:30
    respuesta_previa = cliente.post("/reserva", json = datos_reserva)
    # Ejecutar: reserva que empieza a las 19:30
    respuesta = cliente.post("/reserva", json = datos_reserva_limite)
    # Comprobar: la preparación funcionó
    assert respuesta_previa.status_code == 200
    # Comprobar: la pegada se acepta
    assert respuesta.status_code == 200
    # Limpiar
    app.dependency_overrides.clear()

# TEST: una reserva que se pisa con otra se rechaza (409)
def test_reserva_solapa():
    # Preparar: archivo de prueba vacío
    guardar_reserva([],RUTA_PRUEBA)
    # Preparar: usar la ruta de prueba
    app.dependency_overrides[get_ruta] = get_ruta_test
    # Preparar: ocupar la franja de 18:00 a 19:30
    respuesta_previa = cliente.post("/reserva", json = datos_reserva)
    # Ejecutar: reserva de 18:30 a 21:00 (se pisa con la anterior)
    respuesta = cliente.post("/reserva", json = datos_reserva_solapa)
    # Comprobar: la preparación funcionó
    assert respuesta_previa.status_code == 200
    # Comprobar: se rechaza con 409
    assert respuesta.status_code == 409
    # Comprobar: el mensaje de error que devuelve la API
    assert respuesta.json() == {"detail":"Esa franja ya esta reservada"}
    # Limpiar
    app.dependency_overrides.clear()


