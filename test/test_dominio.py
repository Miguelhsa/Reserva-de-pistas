# Clases y funciones del dominio que se van a probar
from dominio.modelos import Pista, Usuario, Reserva, crear_reserva, crear_pista, consulta_pistas_libres
# Para crear las fechas de las reservas de prueba
from datetime import datetime
# pytest: para pytest.raises (comprobar que algo lanza un error)
import pytest

#cree dos reservas de la misma pista que se pisan (como las que montabas en el REPL),
#llame a a.se_solapa_con(b),
#compruebe con assert que el resultado es True.

# Datos de prueba: una pista y dos usuarios
pista_1 = Pista(1)
usuario_1 = Usuario(1,"Miguel","Hidalgo","usuario")
usuario_2 = Usuario(2,"Carlos","Hidalgo","usuario")

# Reserva de 20:00 a 21:00
reserva_1 = Reserva(pista_1,[usuario_1],datetime(2026,10,3,20,0),datetime(2026,10,3,21,0))
# Reserva de 20:30 a 21:30: se pisa con la 1
reserva_2 = Reserva(pista_1,[usuario_2],datetime(2026,10,3,20,30),datetime(2026,10,3,21,30))
# Reserva de 21:00 a 22:00: pegada a la 1 (empieza justo cuando acaba)
reserva_3 = Reserva(pista_1,[usuario_2],datetime(2026,10,3,21,00),datetime(2026,10,3,22,00))

# TEST: dos reservas que se pisan -> se_solapa_con debe dar True
def test_se_solapa_con() -> None:
    # assert: si la condición no es verdad, el test falla
    assert reserva_1.se_solapa_con(reserva_2)

# TEST: dos reservas pegadas NO se pisan (caso límite) -> debe dar False
def test_no_se_solapa_con() -> None:
    # assert not: comprueba que el resultado es False
    assert not reserva_1.se_solapa_con(reserva_3)

# TEST: crear una reserva que choca debe lanzar ValueError
def test_crear_reserva() -> None:

    # Lo de dentro de este bloque TIENE que lanzar ValueError; si no lo lanza, el test falla
    with pytest.raises(ValueError):
        # reserva_3 choca con reserva_2 (de 21:00 a 21:30)
        crear_reserva(reserva_3,[reserva_1,reserva_2])

# TEST: una pista con número nuevo se añade a la lista
def test_crear_pista() -> None:
    # Preparar: pistas que ya existen (lista hecha a mano, sin archivos)
    existentes = [Pista(1),Pista(2)]
    # La pista nueva, con un número que no está
    nueva = Pista(3)

    # Ejecutar: la regla de negocio
    crear_pista(nueva, existentes)
    #estoy comprobando que nueva esta en existentes
    assert nueva in existentes

# TEST: una pista con número repetido se rechaza
def test_crear_pista_error() -> None:
    # Preparar: pistas que ya existen
    existentes = [Pista(1),Pista(2)]
    # La nueva repite el número 2
    nueva = Pista(2)

    # Tiene que lanzar ValueError
    with pytest.raises(ValueError):
        crear_pista(nueva, existentes)

    # Y no debe haber añadido nada: la lista sigue con 2 pistas
    assert len(existentes) == 2

#Datos COMPARTIDOS para los tests de consulta_pistas_libres (en MAYÚSCULAS: constantes que nadie modifica;
#la función solo las lee). Cada test consulta una FRANJA distinta sobre el mismo club y las mismas reservas.
#Pistas del club
PISTAS_CLUB = [
    Pista(1),
    Pista(2)
]
#Reservas existentes
# Pista 1 de 20:00 a 21:00
RESERVAS_EXISTENTES = [
    Reserva(Pista(1),[usuario_1],datetime(2026,10,3,20,0),datetime(2026,10,3,21,0)),
# Reserva de la pista 2 de 19:00 a 20:00 (termina justo cuando empieza la franja del primer test)
    Reserva(Pista(2),[usuario_2],datetime(2026,10,3,19,00),datetime(2026,10,3,20,00)),
# Pista 1 de 21:00 a 22:00 (pegada a su reserva de 20:00-21:00)
    Reserva(Pista(1),[usuario_2],datetime(2026,10,3,21,00),datetime(2026,10,3,22,00))
]

#Franja 20:00-21:00: la pista 1 está ocupada; la pista 2 está libre (su reserva acaba justo a las 20:00)
INICIO_FRANJA_PISTA_1_OCUPADA = datetime(2026,10,3,20,0)
FIN_FRANJA_PISTA_1_OCUPADA = datetime(2026,10,3,21,0)
#Franja 01:00-23:00: pisa reservas de todas las pistas
INICIO_FRANJA_TODO_OCUPADO = datetime(2026,10,3,1,0)
FIN_FRANJA_TODO_OCUPADO = datetime(2026,10,3,23,0)
#Franja 08:00-09:00: no hay ninguna reserva, todas las pistas libres
INICIO_FRANJA_LIBRE = datetime(2026,10,3,8,0)
FIN_FRANJA_LIBRE = datetime(2026,10,3,9,0) 

#Tests de consulta_pistas_libres: uno por caso, para que el nombre del que falle diga qué se ha roto
#TEST: la pista 1 tiene reserva en la franja -> no sale; la pista 2 (reserva pegada, no choca) -> sí sale
def test_pista_reservada_no_aparece_libre() -> None:
    #Solo debe devolver la pista 2
    assert consulta_pistas_libres(
        PISTAS_CLUB,
        INICIO_FRANJA_PISTA_1_OCUPADA,
        FIN_FRANJA_PISTA_1_OCUPADA,
        RESERVAS_EXISTENTES
        ) == [Pista(2)]

#TEST: la franja choca con reservas de todas las pistas -> lista vacía
def test_franja_ocupada_en_todas_no_devuelve_ninguna() -> None:
    #No debe devolver ninguna pista    
    assert consulta_pistas_libres(
        PISTAS_CLUB,
        INICIO_FRANJA_TODO_OCUPADO,
        FIN_FRANJA_TODO_OCUPADO,
        RESERVAS_EXISTENTES
        ) == []    

#TEST: franja sin ninguna reserva -> devuelve todas las pistas del club
def test_franja_sin_reservas_devuelve_todas() -> None:
    #Debe devolver las dos pistas
    assert consulta_pistas_libres(
        PISTAS_CLUB,
        INICIO_FRANJA_LIBRE,
        FIN_FRANJA_LIBRE,
        RESERVAS_EXISTENTES
        ) == [Pista(1),Pista(2)]  