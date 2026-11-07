# 'Navegador falso' para hacer peticiones a la app sin arrancar el servidor
from fastapi.testclient import TestClient
# La app real, la que se va a probar
from interfaz.app import app
#Funcion que nos entrega la ruta, en este caso prod, pero haremos el cambio entre prod
#y test con get_ruta_pistas_test
from interfaz.routers.pistas import get_ruta_pistas
#funcion que guarda las pistas, pero le pasaremos lista vacia para resetear 
from persistencia.repositorio import guardar_pista

# Crea el "navegador falso": un cliente que hace peticiones HTTP (POST, GET...) a nuestra app
# directamente en memoria, sin arrancar el servidor con fastapi dev. Así los tests pueden
# llamar a /pista como lo haría un usuario desde /docs, pero de forma automática y repetible.
cliente = TestClient(app)

#Ejemplo para pista 
pista_test = {
    "numero": 1
}
#ruta para las pistas de prueba 
RUTA_TEST_PISTAS = "test_pistas.json"

#funcion que entrega la ruta de test, para los tests sustituiremos get_ruta_pistas por 
#esta funcion con -> app.dependency_overrides[get_ruta_pistas] = get_ruta_pistas_test
def get_ruta_pistas_test() -> str:
    #Devuelve la ruta de Test de pistas
    return RUTA_TEST_PISTAS

#Test: vamos a ver varios casos.
#1. Creacion de pista. Devuelve 200 y devuelve la pista
def test_creacion_pista() -> None:
    #llamamos a guarda_pista con la lista vacia, si no existe crea el archivo vacio
    guardar_pista([],RUTA_TEST_PISTAS)
    #con overrides cambiamos una funcion por otra para llamar a la funcion que entrega la ruta test
    app.dependency_overrides[get_ruta_pistas] = get_ruta_pistas_test
    #llamamos al endpoint post crear pista y el resultado que nos arroja es HTTP 200 y la pista
    respuesta = cliente.post("/pista", json= pista_test)
    #la respuesta del post tiene que se código HTTP200
    assert respuesta.status_code == 200
    #La respuesta en json tiene que ser la pista 
    assert respuesta.json() == pista_test
    #hay que resetear el overrides ya que si no se queda en memoria
    app.dependency_overrides.clear()
    
#2. Intento de creacion de pista pero esta pista ya existe
def test_error_pista_repetida() -> None:
    #llamamos a guarda_pista con la lista vacia, si no existe crea el archivo vacio
    #La volvemos a ejecutar por si necesitamos ejecutar unicamente este test y no tener ningun error.
    guardar_pista([],RUTA_TEST_PISTAS)
    #con overrides cambiamos una funcion por otra para llamar a la funcion que entrega la ruta test
    app.dependency_overrides[get_ruta_pistas] = get_ruta_pistas_test
    #Creamos una pista con la pista test
    cliente.post("/pista", json= pista_test)
    #llamamos al endpoint post crear pista y el resultado que nos arroja es HTTP 409 y el json "la pista ya existe"
    respuesta = cliente.post("/pista", json= pista_test)
    #Tendremos un error por ValueError ya que la pista existe
    assert respuesta.status_code == 409
    #El texto que nos arroja es el de detail = "La pista ya existe"
    assert respuesta.json() == {"detail": "La pista ya existe"}
    #hay que resetear el overrides ya que si no se queda en memoria
    app.dependency_overrides.clear()

#3. Intento de creacion pero en el body se manda texto
def test_error_valor_str() -> None:
    #con overrides cambiamos una funcion por otra para llamar a la funcion que entrega la ruta test
    app.dependency_overrides[get_ruta_pistas] = get_ruta_pistas_test
    #llamamos al endpoint post crear pista y le pasamos una pista en formato string que tiene que arrojar error 422
    respuesta = cliente.post("/pista", json= {"numero":"a"})
    #En este caso no tenemos montado el error en ninguna funcion, se comprueba cuando 
    #se manda la info en el cuerpo al endpoint y este la valida con PistaIn
    assert respuesta.status_code == 422
    #hay que resetear el overrides ya que si no se queda en memoria
    app.dependency_overrides.clear()