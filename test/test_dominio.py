from dominio.modelos import Pista, Usuario, Reserva
from datetime import datetime
import pytest
from dominio.modelos import crear_reserva

#cree dos reservas de la misma pista que se pisan (como las que montabas en el REPL),
#llame a a.se_solapa_con(b),
#compruebe con assert que el resultado es True.

pista_1 = Pista(1)
usuario_1 = Usuario(1,"Miguel","Hidalgo","usuario")
usuario_2 = Usuario(2,"Carlos","Hidalgo","usuario")

reserva_1 = Reserva(pista_1,[usuario_1],datetime(2026,10,3,20,0),datetime(2026,10,3,21,0))
reserva_2 = Reserva(pista_1,[usuario_2],datetime(2026,10,3,20,30),datetime(2026,10,3,21,30))
reserva_3 = Reserva(pista_1,[usuario_2],datetime(2026,10,3,21,00),datetime(2026,10,3,22,00))

def test_se_solapa_con():
    assert reserva_1.se_solapa_con(reserva_2)

def test_no_se_solapa_con():
    assert not reserva_1.se_solapa_con(reserva_3)

def test_crear_reserva():

    with pytest.raises(ValueError):
        crear_reserva(reserva_3,[reserva_1,reserva_2])