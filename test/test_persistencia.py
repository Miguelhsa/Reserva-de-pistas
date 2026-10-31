#importo de persistencia las funciones de guardar y cargar
from persistencia.repositorio import guardar_pista, cargar_pista
#importo el modelo de clase Pista
from dominio.modelos import Pista

#creo la constante que es la ruta donde ser guardarán y cargaran las pistas de test
RUTA_PRUEBA = "test_persistencia.json"



# test: las pistas que se guardan en disco vuelven iguales al cargarlas
def test_pistas_guardadas_se_cargan_iguales() -> None:
    # preparo las pistas originales que voy a guardar
    pistas_originales = [
        Pista(1),
        Pista(2)
    ]
    #llamo a la funcion guardar_pista y le paso los datos nuevos
    guardar_pista(pistas_originales,RUTA_PRUEBA)
    #compruebo que lo que ha guardado es igual a lo que le he pasado en el anterior paso
    #assert, si no se cumple error
    assert pistas_originales == cargar_pista(RUTA_PRUEBA)
    #limpio los datos 
    guardar_pista([],RUTA_PRUEBA)