# La clase que crea la aplicación web
from fastapi import FastAPI
# El router de reservas (con su endpoint POST /reserva), importado con el apodo 'reserva'
from interfaz.routers.reservas import router as reserva
#El router de reservas (con su endpoint POST /pista), importado con el apodo "pistas"
from interfaz.routers.pistas import router as pistas

# Crea la app: el 'restaurante' donde trabajan los routers
app = FastAPI()
# Enchufa el router de reservas: desde aquí sus rutas existen en la app
app.include_router(reserva)
#Enchufa el router de psitas
app.include_router(pistas)