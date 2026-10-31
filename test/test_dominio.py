# Clases y funciones del dominio que se van a probar
from dominio.modelos import Pista, Usuario, Reserva, crear_reserva, crear_pista
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
def test_se_solapa_con():
    # assert: si la condición no es verdad, el test falla
    assert reserva_1.se_solapa_con(reserva_2)

# TEST: dos reservas pegadas NO se pisan (caso límite) -> debe dar False
def test_no_se_solapa_con():
    # assert not: comprueba que el resultado es False
    assert not reserva_1.se_solapa_con(reserva_3)

# TEST: crear una reserva que choca debe lanzar ValueError
def test_crear_reserva():

    # Lo de dentro de este bloque TIENE que lanzar ValueError; si no lo lanza, el test falla
    with pytest.raises(ValueError):
        # reserva_3 choca con reserva_2 (de 21:00 a 21:30)
        crear_reserva(reserva_3,[reserva_1,reserva_2])

# TEST: una pista con número nuevo se añade a la lista
def test_crear_pista():
    # Preparar: pistas que ya existen (lista hecha a mano, sin archivos)
    existentes = [Pista(1),Pista(2)]
    # La pista nueva, con un número que no está
    nueva = Pista(3)

    # Ejecutar: la regla de negocio
    crear_pista(nueva, existentes)
    #estoy comprobando que nueva esta en existentes
    assert nueva in existentes

# TEST: una pista con número repetido se rechaza
def test_crear_pista_error():
    # Preparar: pistas que ya existen
    existentes = [Pista(1),Pista(2)]
    # La nueva repite el número 2
    nueva = Pista(2)

    # Tiene que lanzar ValueError
    with pytest.raises(ValueError):
        crear_pista(nueva, existentes)

    # Y no debe haber añadido nada: la lista sigue con 2 pistas
    assert len(existentes) == 2