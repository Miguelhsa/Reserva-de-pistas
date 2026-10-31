#aqui viven las clases Pista, usuario, reserva
# Importa el decorador @dataclass: genera solo el __init__ (para crear objetos) y el == (para compararlos)
from dataclasses import dataclass
# Importa datetime para representar fechas con hora (inicio y fin de cada reserva)
from datetime import datetime

# CLASE Pista: una pista del club. La distingue su número.
@dataclass
class Pista:
    # Número de la pista
    numero: int

# CLASE Usuario: un jugador que participa en una reserva.
@dataclass
class Usuario:
    # Identificador del usuario (provisional: hoy lo manda el cliente)
    id: int
    # Nombre del jugador
    nombre: str
    # Apellidos del jugador
    apellidos: str
    # Rol: socio, admin... (provisional, como el id)
    rol: str 

# CLASE Reserva: una franja de tiempo en una pista, con sus jugadores.
@dataclass
class Reserva:
    # La pista reservada (un objeto Pista, no un número)
    pista: Pista
    # Lista de jugadores (objetos Usuario)
    usuarios: list[Usuario]
    # Cuándo empieza la reserva
    fecha_inicio: datetime
    # Cuándo termina la reserva
    fecha_fin: datetime

    # MÉTODO: ¿esta reserva (self) se pisa con otra? Devuelve True o False.
    def se_solapa_con(self,otra) -> bool:
        #"si una función responde sí/no, devuelve la condición directamente".
        # Se pisan si es la misma pista Y cada una empieza antes de que acabe la otra (hacen falta las dos comparaciones)
        return self.pista == otra.pista and self.fecha_inicio < otra.fecha_fin and otra.fecha_inicio < self.fecha_fin


# FUNCIÓN: ¿la reserva nueva choca con alguna de las existentes? Devuelve True o False.
def choca_con_existentes(nueva,existentes) -> bool:

    # Recorre las reservas que ya existen, una a una
    for existente in existentes:
        # Si la nueva se pisa con esta existente...
        if nueva.se_solapa_con(existente):
            # ...ya hay choque: responde True sin mirar las demás
            return True
    # Solo si ha mirado TODAS sin encontrar choque responde False (por eso va fuera del for)
    return False 

# FUNCIÓN (regla de negocio): crea la reserva si no choca. Recibe la nueva y la lista de las existentes.
def crear_reserva(nueva,existentes):
    # Si choca con alguna existente...
    if choca_con_existentes(nueva,existentes):
        # ...se niega lanzando un error (la interfaz lo convertirá en un 409)
        raise ValueError("reserva solapada")
    # Si no choca:
    else:
        # la añade a la lista (es la MISMA lista que tiene el orquestador, por eso él también la ve)
        existentes.append(nueva)
        # devuelve la reserva creada
        return nueva

# FUNCIÓN (regla de negocio): da de alta una pista si su número no está repetido.
def crear_pista(nueva:Pista, existentes:list[Pista]) -> Pista:
    # Recorre las pistas que ya existen
    for pista_existente in existentes:
        # Si alguna tiene el mismo número que la nueva...
        if nueva.numero == pista_existente.numero:
            # ...se niega lanzando un error
            raise ValueError("pista existente")
    # Solo tras mirarlas TODAS sin repetición añade la nueva (por eso va fuera del for)
    existentes.append(nueva)
    # Devuelve la pista creada (igual que crear_reserva, por coherencia)
    return nueva