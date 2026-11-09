# Persistencia: cargar y guardar las reservas y las pistas en su archivo
from persistencia.repositorio import cargar_reserva, guardar_reserva, cargar_pista, guardar_pista
#Dominio importo lo necesario para realizar la orquestacion
from dominio.modelos import crear_reserva, Reserva, Pista, crear_pista, consulta_pistas_libres
# Importa datetime para representar fechas con hora (inicio y fin de cada reserva)
from datetime import datetime


# FUNCIÓN (orquestador): coordina el flujo de reservar: cargar -> decidir -> guardar. Ella no decide ni guarda nada.
def reservar(nueva: Reserva, ruta: str) -> None:
#cargar la lista del archivo (guárdala en una variable),
#crear_reserva pasándole esa lista (decide: añade o lanza error),
#guardar esa lista ya actualizada
    #cargo todas las reservas y la guardo en una variable
    lista_reservas = cargar_reserva(ruta)
    #con esa lista compruebo que no coincide con ninguna ya creada 
    #solo compruebo, si se solapa da error, sino añade la reserva a la lista que esta en memoria
    crear_reserva(nueva,lista_reservas)
    #Si la ha guardado, la lista ahora tiene añadida esa nueva reserva
    guardar_reserva(lista_reservas,ruta)

#Funcion (orquestador): coordina la creacion de una pista
def dar_de_alta_pista(nueva: Pista,ruta:str) -> Pista:
    #cargar las pistas existentes y guardarlas en una variable
    pistas_existentes = cargar_pista(ruta)
    #lanzar crear pista que pasa por el listado de pistas existentes
    #si la pista existe --> error, si no existe, la crea y la guarda en la lista
    crear_pista(nueva,pistas_existentes) #retorna la pista creada
    #guardar: paso la lista de pistas ya actualizada a guardar_pista, para que quede escrita en el archivo
    guardar_pista(pistas_existentes,ruta)
    #return: devuelvo la pista nueva a quien me llamó (el router)
    return nueva

#Funcion (orquestador): coordina la consulta de las pistas libres que hay según la fecha inicio y fin de 
#una solicitud. Entregará una lista de pistas libres
#Pasos: cargar las pistas, cargar las reservas, llamar a consulta_pistas_libres
def consulta_disponibilidad(fecha_inicio: datetime, fecha_fin: datetime, ruta_reservas: str, ruta_pistas:str) -> list[Pista]: 
    #Paso 1: cargar las pistas y guardarlas en una variable. Para ello llamamos a cargar_pista
    lista_pistas = cargar_pista(ruta_pistas)
    #Paso 2: Cargar las reservas
    lista_reservas = cargar_reserva(ruta_reservas)
    #Llamamos a consultar_pistas_libres y le pasamos los parámetros necesarios
    return consulta_pistas_libres(lista_pistas,fecha_inicio,fecha_fin,lista_reservas)