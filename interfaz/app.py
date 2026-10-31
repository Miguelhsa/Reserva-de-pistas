# La clase que crea la aplicación web
from fastapi import FastAPI
# El router de reservas (con su endpoint POST /reserva), importado con el apodo 'reserva'
from interfaz.routers.reservas import router as reserva

# Crea la app: el 'restaurante' donde trabajan los routers
app = FastAPI()
# Enchufa el router de reservas: desde aquí sus rutas existen en la app
app.include_router(reserva)