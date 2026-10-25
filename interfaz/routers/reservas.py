# BaseModel: la base de los moldes Pydantic (validan lo que entra y lo que sale por la web)
from pydantic import BaseModel
# datetime: tipo de las fechas en los moldes
from datetime import datetime
# APIRouter (agrupa endpoints), HTTPException (responder con un código de error), Depends (pedirle algo a FastAPI)
from fastapi import APIRouter, HTTPException, Depends
# Clases del dominio, para traducir lo que entra a objetos de la cocina
from dominio.modelos import Pista, Usuario, Reserva
# El orquestador, al que el endpoint le pasa la reserva
from interfaz.orquestador import reservar

# Archivo donde se guardan las reservas reales
RUTA_RESERVAS = "reservas.json"

# FUNCIÓN 'cafetera': entrega la ruta del archivo. El endpoint la pide con Depends; en los tests se sustituye por otra.
def get_ruta() -> str:
    # Devuelve el valor de la constante (sin comillas = la variable, no el texto)
    return RUTA_RESERVAS

# Crea el router: sus rutas empiezan por /reserva y salen agrupadas como 'Reservas' en /docs
router = APIRouter(prefix="/reserva",tags=["Reservas"])
#En UsuarioIn id y rol son provisionales
#Molde de entrada por el endpoint para el usuario
class UsuarioIn(BaseModel):
    # Campos que debe traer cada usuario en el JSON de entrada (si falta alguno o el tipo no cuadra -> 422)
    id: int
    nombre: str
    apellidos: str
    rol: str
#Molde de entrada por el endpoint para la peticion de reserva
class ReservaIn(BaseModel):
    # Número de pista (llega un número; luego se convierte en objeto Pista)
    pista: int
    # Lista de usuarios, cada uno con la forma de UsuarioIn
    usuarios: list[UsuarioIn]
    # Fechas: Pydantic convierte el texto del JSON a datetime
    fecha_inicio: datetime
    fecha_fin: datetime

#Si se ha hecho la reserva el Usuario que entregaremos no tendrá id ni rol
class UsuarioOut(BaseModel):
    # Solo los datos que se enseñan al socio (sin id ni rol)
    nombre:str
    apellidos: str
#Si se ha reservado, molde de salida 
class ReservaOut(BaseModel):
    # En la salida la pista vuelve a ser un número
    pista: int
    # Usuarios con la forma de UsuarioOut
    usuarios: list[UsuarioOut]
    # Fechas de la reserva confirmada
    fecha_inicio: datetime
    fecha_fin: datetime

# ENDPOINT POST /reserva; response_model fija el contrato de salida (lo que se ve en /docs y lo que se deja salir)
@router.post("",response_model=ReservaOut)
# FUNCIÓN del endpoint: recibe la reserva (ya validada por ReservaIn) y PIDE la ruta del archivo con Depends
def solicitar_reserva(nueva_reserva: ReservaIn, ruta : str = Depends(get_ruta)):
    #pasos:
    #Construir una pista
    #Construir una lista con los usuarios
    #Montar la reserva con la funcion reserva
    # 1. Traduce: construye la Pista del dominio a partir del número
    pista_reserva = Pista(nueva_reserva.pista)
    # 2. Traduce los usuarios: lista vacía para ir llenándola
    usuarios_reserva = []
    # Recorre cada usuario que llegó por la web
    for usuario in nueva_reserva.usuarios:
        # Construye un Usuario del dominio con sus datos y lo añade
        usuarios_reserva.append(Usuario(usuario.id, usuario.nombre, usuario.apellidos, usuario.rol))

    # 3. Monta la Reserva del dominio con la pista, los usuarios y las fechas
    reserva_nueva_guardar = Reserva(
        pista_reserva,
        usuarios_reserva,
        nueva_reserva.fecha_inicio,
        nueva_reserva.fecha_fin
        )

    # 4. Intenta reservar: el orquestador carga, el dominio decide y se guarda
    try:
        reservar(reserva_nueva_guardar,ruta)

    # Si el dominio dice que choca (ValueError)...
    except ValueError:
        # ...lo traduce al idioma web: un 409 con un mensaje para el cliente
        raise HTTPException(status_code=409, detail="Esa franja ya esta reservada")

    #Construyo las datos de salida con UsuarioOut y ReservOut

    # 5. Traduce la salida: lista para los usuarios sin id ni rol
    usuarios_reserva_out = []
    # Recorre los usuarios de la reserva creada
    for usuario_reserva in reserva_nueva_guardar.usuarios:
        # Crea cada UsuarioOut (Pydantic exige argumentos con nombre)
        usuarios_reserva_out.append(UsuarioOut(nombre= usuario_reserva.nombre,apellidos= usuario_reserva.apellidos))

    # Monta la respuesta con la forma de ReservaOut (la pista como número)
    reserva_nueva_out = ReservaOut(
        pista = pista_reserva.numero,
        usuarios= usuarios_reserva_out,
        fecha_inicio = reserva_nueva_guardar.fecha_inicio,
        fecha_fin= reserva_nueva_guardar.fecha_fin
    )
    # Devuelve la respuesta: FastAPI la convierte en JSON
    return reserva_nueva_out


