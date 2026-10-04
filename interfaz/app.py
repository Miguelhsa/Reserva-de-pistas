from fastapi import FastAPI
from interfaz.routers.reservas import router as reserva

app = FastAPI()
app.include_router(reserva)