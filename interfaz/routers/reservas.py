from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException
from dominio.modelos import Pista, Usuario, Reserva
from interfaz.orquestador import reservar

RUTA_RESERVAS = "reservas.json"

router = APIRouter(prefix="/reserva",tags=["Reservas"])
#En UsuarioIn id y rol son provisionales
#Molde de entrada por el endpoint para el usuario
class UsuarioIn(BaseModel):
    id: int
    nombre: str
    apellidos: str
    rol: str
#Molde de entrada por el endpoint para la peticion de reserva
class ReservaIn(BaseModel):
    pista: int
    usuarios: list[UsuarioIn]
    fecha_inicio: datetime
    fecha_fin: datetime

#Si se ha hecho la reserva el Usuario que entregaremos no tendrá id ni rol
class UsuarioOut(BaseModel):
    nombre:str
    apellidos: str
#Si se ha reservado, molde de salida 
class ReservaOut(BaseModel):
    pista: Pista
    usuarios: list[UsuarioOut]
    fecha_inicio: datetime
    fecha_fin: datetime

@router.post("",response_model=ReservaOut)
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

    #Construyo las datos de salida con UsuarioOut y ReservOut

    usuarios_reserva_out = []
    for usuario_reserva in reserva_nueva_guardar.usuarios:
        usuarios_reserva_out.append(UsuarioOut(nombre= usuario_reserva.nombre,apellidos= usuario_reserva.apellidos))

    reserva_nueva_out = ReservaOut(
        pista = pista_reserva.numero,
        usuarios= usuarios_reserva_out,
        fecha_inicio = reserva_nueva_guardar.fecha_inicio,
        fecha_fin= reserva_nueva_guardar.fecha_fin
    )
    return reserva_nueva_out