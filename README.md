# Reservas de pista — mapa vivo del proyecto

> Este README es el MAPA del proyecto. Se escribe lo primero y se va alimentando sesión a sesión.
> Rellena tú cada sección con tus palabras. Regla: macro primero, micro después.

## 1. Qué es
Sistema para gestionar reservas de pistas de Padel, usado por socios (que reservan) y admnistradores (que gestionan las pistas)

## 2. Qué sabe hacer (capacidades)
El sistema tiene varias responsabilidades: 
- Registrar un usuario
- Dar de alta una pista
- Autenticar usuario y comprobar su rol
- Consultar disponibilidad de pista
- Reservar pista (apuntando que jugadores juegan)
- Cancelar o modificar una reserva
- Avisar al jugador 24h antes de su reserva

## 3. Capas y dirección de dependencias

### Interfaz
- Hace: muestra y recibe datos
- Prohibido: realizar calculos ni validaciones

### Dominio
- Hace: crear usuario, pista. cuando alguien quiere reservar una franja, mira si esa franja ya está ocupada; si lo está, NO deja reservar.
- Prohibido: comunicar con la bbdd, mostrar datos a usuario

### Persistencia (repositorio)
- Hace: comunicar con la bbdd
- Prohibido: hacer calculos, validaciones ni autenticaciones

### Flechas (dirección de dependencias)
- interfaz -> Dominio <- persistencia

## 4. Carpetas
reserva-pistas/
interfaz
dominio
persistencia

## 5. Dominio: los objetos
- Pista: 
Atributos, numero de pista
- Reserva:
Atributos, numero de pista, usuarios, fecha, hora de inicio y fin de reserva
- Usuarios:
Atributos, ID, nombre, apellidos, rol

## 6. Siguiente paso
Fase 0 HECHA: proyecto con `uv` (pyproject, .python-version), `.gitignore`, repo git con primer commit, y subido a GitHub (github.com/Miguelhsa/Reserva-de-pistas, rama `main`).

Siguiente: empezar a picar el **dominio** — las dataclasses `Pista`, `Reserva`, `Usuario` (tipadas de nacimiento) y la regla de no solapar franjas. Antes: retirar el `main.py` de ejemplo y crear las carpetas de las capas (interfaz/dominio/persistencia).

Pendiente menor: añadir en la sección 3 la frase-prueba "cambiar de JSON a Postgres solo toca la persistencia".
