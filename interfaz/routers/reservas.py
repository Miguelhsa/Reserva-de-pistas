from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException
from dominio.modelos import Pista, Usuario, Reserva
from interfaz.orquestador import reservar

RUTA_RESERVAS = "reservas.json"

router = APIRouter(prefix="/reserva",tags=["Reservas"])
#En UsuarioIn id y rol son provisionales
class UsuarioIn(BaseModel):
    id: int
    nombre: str
    apellidos: str
    rol: str

class ReservaIn(BaseModel):
    pista: int
    usuarios: list[UsuarioIn]
    fecha_inicio: datetime
    fecha_fin: datetime

@router.post("")
def solicitar_reserva(nueva_reserva: ReservaIn):
    #pasos:
    #Construir una pista
    #Construir una lista con los usuarios
    #Montar la reserva con la funcion reserva
    pista_reserva = Pista(nueva_reserva.pista)
    usuarios_reserva = []
    for usuario in nueva_reserva.usuarios:
        usuarios_reserva.append(Usuario(usuario.id, usuario.nombre, usuario.apellidos, usuario.rol))

    reserva_nueva_guardar = Reserva(
        pista_reserva,
        usuarios_reserva,
        nueva_reserva.fecha_inicio,
        nueva_reserva.fecha_fin
        )

    try:
        reservar(reserva_nueva_guardar,RUTA_RESERVAS)

    except ValueError:
        raise HTTPException(status_code=409, detail="Esa franja ya esta reservada")
    
    return reserva_nueva_guardar