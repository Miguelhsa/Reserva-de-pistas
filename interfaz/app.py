from persistencia.repositorio import cargar, guardar
from dominio.modelos import crear_reserva

def reservar(nueva,ruta):
#cargar la lista del archivo (guárdala en una variable),
#crear_reserva pasándole esa lista (decide: añade o lanza error),
#guardar esa lista ya actualizada
    #cargo todas las reservas y la guardo en una variable
    lista_reservas = cargar(ruta)
    #con esa lista compruebo que no coincide con ninguna ya creada 
    #solo compruebo, si se solapa da error, sino añade la reserva a la lista que esta en memoria
    crear_reserva(nueva,lista_reservas)
    #Si la ha guardado, la lista ahora tiene añadida esa nueva reserva
    guardar(lista_reservas,ruta)