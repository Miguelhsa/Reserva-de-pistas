# Librería estándar para leer y escribir archivos JSON
import json
# asdict convierte un objeto dataclass (y los objetos que lleva dentro) en un diccionario
from dataclasses import asdict
# Clases del dominio, para reconstruir los objetos al cargar
from dominio.modelos import Pista, Usuario, Reserva
# datetime, para convertir las fechas de texto a fecha al cargar
from datetime import datetime

# FUNCIÓN: guarda la lista de reservas en un archivo JSON (reescribe el archivo entero).
def guardar_reserva(reservas,ruta) -> None:
    # Convierte cada Reserva en diccionario (JSON no entiende objetos)
    datos = [asdict(r) for r in reservas]
    # Abre el archivo para escribir ('w' lo vacía y escribe desde cero); 'with' lo cierra solo al terminar
    with open(ruta,"w") as f:
        # Escribe la lista en el archivo; default=str convierte las fechas a texto (JSON no sabe guardar datetime)
        json.dump(datos,f,default=str)


# FUNCIÓN: lee el archivo JSON y reconstruye los objetos Reserva (el viaje inverso de guardar).
def cargar_reserva(ruta) -> list[Reserva]:
    # Aquí se irán acumulando las reservas ya convertidas en objetos
    lista_reservas = []
    # Abre el archivo para leer
    with open(ruta,"r") as f:
        # json.load devuelve DICCIONARIOS, no objetos
        reservas = json.load(f) #esto entrega una lisa con todas las reservas
        # Recorre cada reserva (cada una es un diccionario)
        for linea_reserva in reservas:
            # Lista para los usuarios de ESTA reserva
            lista_usuarios = []
            # Recorre los usuarios de esta reserva (también son diccionarios)
            for usuario in linea_reserva["usuarios"]:
                #cada usuario hay que convertirlo a un objeto usuario
                objeto_usuario = Usuario(usuario["id"],usuario["nombre"],usuario["apellidos"],usuario["rol"])
                # Añade el usuario ya convertido a la lista de esta reserva
                lista_usuarios.append(objeto_usuario)
            # Reconstruye la Reserva: Pista desde su número, la lista de usuarios y las fechas de texto a datetime
            lista_reservas.append(Reserva(Pista(linea_reserva["pista"]["numero"]),lista_usuarios,datetime.fromisoformat(linea_reserva["fecha_inicio"]),datetime.fromisoformat(linea_reserva["fecha_fin"])))
    # Devuelve la lista de objetos Reserva (fuera de los for: cuando ya están todas)
    return lista_reservas

# Funcion: guardar la lista de pistas
def guardar_pista(pista,ruta: str) -> None:
    #convierte cada pista en un diccionario
    pistas = [asdict(p)for p in pista]
    #Abre el archivo donde guardar ("w lo vacía y escribe desde cero); 'with' lo cierra solo al terminar")
    with open(ruta,"w") as f:
        # Escribe la lista en el archivo
        json.dump(pistas,f)

# FUNCION: carga el listado de pistas, entrega una lista de objetos pista
def cargar_pista(ruta: str) -> list[Pista]:
    #creo una lista vacia para añadir aqui las pistas
    lista_pistas = []
    #abro el archivo donde se guardan las pistas, solo en modo lectura "r"
    with open(ruta,"r") as f:
        #json.load devuelve diccionarios, no objetos
        pistas = json.load(f)#esto entrega una lista con todas las pistas
        #bucle para parar por cada pista que es un diccionario y convertirla en pista
        for p in pistas:
            #reconstruyo la pista desde su numero
            lista_pistas.append(Pista(p["numero"]))
    #Devuelvo el listado de objeto pistas
    return lista_pistas