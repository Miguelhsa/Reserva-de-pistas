# BaseModel: la base de los moldes Pydantic (validan lo que entra y lo que sale por la web)
from pydantic import BaseModel
# APIRouter (agrupa endpoints), HTTPException (responder con un código de error), Depends (pedirle algo a FastAPI)
from fastapi import APIRouter, HTTPException, Depends
# Clases del dominio, para traducir lo que entra a objetos de la cocina
from dominio.modelos import Pista
# El orquestador, al que el endpoint le pasa la pista
from interfaz.orquestador import dar_de_alta_pista

#Archivo donde se van a guardar las pistas
RUTA_PISTAS = "pistas.json"

#Funcion que entrega la ruta del archivo. El endpoint la pide con Depends;
#En los test la sustituimos por otra para cambiar el archivo donde escribimos test o produccion
def get_ruta_pistas() -> str:
    #devuelve la ruta del archivo de pistas de producción
    return RUTA_PISTAS

#creamos el router: sus rutas empiezan por /pista y salen agrupadas como 'Pistas' en docs
router = APIRouter(prefix="/pista",tags=["Pistas"])

#Molde de entrada por el endpoint
class PistaIn(BaseModel):
    #numero de pista que llega
    numero:int

#Molde de salida en el endpoint: lo que se deja ver al cliente cuando el alta sale bien
class PistaOut(BaseModel):
    #numero de la pista dada de alta
    numero: int

#Endpoint POST /pista; response_fija el contrato de salida 
@router.post("",response_model=PistaOut)
#funcion del endpoint: recibe la pista (validada por PistaIn) y pide la ruta del archivo con Depends
def solicitar_crear_pista(nueva_pista: PistaIn, ruta:str = Depends(get_ruta_pistas)) -> PistaOut:
    #pasos:
    #El endpoint recibe un json {numero: int}. Para acceder a este int 
    #hay que convertirlo a objeto Pista --> llama a objeto Pista
    pista_a_crear = Pista(nueva_pista.numero)
    #Llama a funcion del orquestador dar_de_alta_pista que se encarga de:
    #cargar el listado de pistas, crea la pista y guarda.
    try:
        #como argumento pasamos ruta
        #que la usará FASTAPI según el Depends de la funcion que entrega a la variable ruta
        #para sustituir por test o prod
        dar_de_alta_pista(pista_a_crear,ruta)
    #si la pista existe lanza un error ValueError que hay mostrar cuando se hace la llamada
    except ValueError:
        raise HTTPException(status_code=409, detail= "La pista ya existe")
    #Si la pista no existe hay que traducirla a PistaOut
    pista_creada = PistaOut(
        numero = pista_a_crear.numero
    )
    
    return pista_creada