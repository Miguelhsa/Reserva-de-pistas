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
    def se_solapa_con(self, otra: Reserva) -> bool:
        #"si una función responde sí/no, devuelve la condición directamente".
        # Se pisan si es la misma pista Y cada una empieza antes de que acabe la otra (hacen falta las dos comparaciones)
        return self.pista == otra.pista and self.fecha_inicio < otra.fecha_fin and otra.fecha_inicio < self.fecha_fin


# FUNCIÓN: ¿la reserva nueva choca con alguna de las existentes? Devuelve True o False.
def choca_con_existentes(nueva: Reserva, existentes: list[Reserva]) -> bool:

    # Recorre las reservas que ya existen, una a una
    for existente in existentes:
        # Si la nueva se pisa con esta existente...
        if nueva.se_solapa_con(existente):
            # ...ya hay choque: responde True sin mirar las demás
            return True
    # Solo si ha mirado TODAS sin encontrar choque responde False (por eso va fuera del for)
    return False 

# FUNCIÓN (regla de negocio): crea la reserva si no choca. Recibe la nueva y la lista de las existentes.
def crear_reserva(nueva: Reserva, existentes: list[Reserva]) -> Reserva:
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
def crear_pista(nueva: Pista, existentes: list[Pista]) -> Pista:
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

# FUNCIÓN (regla de negocio): ¿qué pistas del club están libres en la franja que pide el socio?
# RECIBE los datos ya cargados (las pistas del club y las reservas existentes): el dominio NO va a buscarlos al disco,
# se los da el orquestador. Para cada pista pregunta "si alguien la reservara en esta franja, ¿chocaría?" reutilizando
# choca_con_existentes (la misma regla de solapamiento que usan las reservas). Devuelve solo las que NO chocan.
def consulta_pistas_libres(pistas_club: list[Pista],fecha_inicio:datetime,fecha_fin:datetime, reservas_existentes:list[Reserva]) -> list[Pista]:
    #Pasos:
    #1 Preparo una lista vacía donde iré apuntando las pistas libres
    pistas_libres = []
    #2 Recorro las pistas del club (pistas_club), una a una
    for pista in pistas_club:
        #2.1 Monto una reserva HIPOTÉTICA con esa pista, sin jugadores (lista vacía) y la franja del socio (fecha_inicio, fecha_fin)
        reserva_hipotetica = Reserva(
            pista,
            [],
            fecha_inicio,
            fecha_fin
        )
        #2.2 Pregunto a choca_con_existentes si esa reserva hipotética choca con las reservas_existentes
        if not choca_con_existentes(reserva_hipotetica,reservas_existentes):
        #2.3 Si NO choca, la pista está libre: la añado a la lista de libres
            pistas_libres.append(pista)
    #3 Después de mirarlas TODAS (fuera del for), devuelvo la lista de pistas libres
    return pistas_libres