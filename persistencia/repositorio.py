import json
from dataclasses import asdict

def guardar(reservas,ruta):
    datos = [asdict(r) for r in reservas]
    with open(ruta,"w") as f:
        json.dump(datos,f,default=str)