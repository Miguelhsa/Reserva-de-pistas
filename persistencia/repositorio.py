import json
from dataclasses import asdict
from dominio.modelos import Pista, Usuario, Reserva
from datetime import datetime

def guardar(reservas,ruta):
    datos = [asdict(r) for r in reservas]
    with open(ruta,"w") as f:
        json.dump(datos,f,default=str)


def cargar(ruta) -> list[Reserva]:
    lista_reservas = []
    with open(ruta,"r") as f:
        reservas = json.load(f) #esto entrega una lisa con todas las reservas
        for linea_reserva in reservas:
            lista_usuarios = []
            for usuario in linea_reserva["usuarios"]:
                #cada usuario hay que convertirlo a un objeto usuario
                objeto_usuario = Usuario(usuario["id"],usuario["nombre"],usuario["apellidos"],usuario["rol"])
                lista_usuarios.append(objeto_usuario)
            lista_reservas.append(Reserva(Pista(linea_reserva["pista"]["numero"]),lista_usuarios,datetime.fromisoformat(linea_reserva["fecha_inicio"]),datetime.fromisoformat(linea_reserva["fecha_fin"])))
    return lista_reservas