#aqui viven las clases Pista, usuario, reserva
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Pista:
    numero: int

@dataclass
class Usuario:
    id: int
    nombre: str
    apellidos: str
    rol: str 

@dataclass
class Reserva:
    pista: Pista
    usuarios: list[Usuario]
    fecha_inicio: datetime
    fecha_fin: datetime

    def se_solapa_con(self,otra) -> bool:
        #"si una función responde sí/no, devuelve la condición directamente".
        return self.pista == otra.pista and self.fecha_inicio < otra.fecha_fin and otra.fecha_inicio < self.fecha_fin

