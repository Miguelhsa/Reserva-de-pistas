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
- app : crea la app y enchufa los routers
- orquestador: coordina el flujo de reservar: carga las reservas (persistencia), comprueba y añade la nueva (dominio) y guarda (persistencia).
- router/reservas: el endpoint POST: recibe el pedido, lo traduce a objetos del dominio, llama al orquestador y contesta (409 si choca). Sin lógica de negocio.
- modelos: tenemos como son los objetos que usaremos y los metodos y las funciones para saber si solapan reservas y crearlas
persistencia : guarda las reservas creadas, por ahora en json

## 5. Dominio: los objetos
- Pista: 
Atributos, numero de pista
- Reserva:
Atributos, numero de pista, usuarios, fecha, hora de inicio y fin de reserva
- Usuarios:
Atributos, ID, nombre, apellidos, rol

## 6. Estado y siguiente paso

**Hecho:**
- DOMINIO: modelos (`Pista`, `Usuario`, `Reserva`) + regla de no solapar (`se_solapa_con`, `choca_con_existentes`) + `crear_reserva`.
- PERSISTENCIA: `guardar` + `cargar` a JSON (`reservas.json`), verificada con round-trip. Aislada: el capstone "JSON -> Postgres solo toca persistencia" ya está montado.
- ORQUESTADOR: `reservar()` coordina cargar -> crear_reserva -> guardar.
- TESTS: 3 tests del dominio con pytest.
- INTERFAZ web (FastAPI): `POST /reserva` (`solicitar_reserva`). Recibe `ReservaIn`, lo traduce a `Reserva` del dominio, llama a `reservar()` y contesta. Si la franja choca, devuelve **409**.
  Arranque: `uv run fastapi dev interfaz/app.py` -> `/docs`.

**Siguiente:**
1. **Molde de salida**: decidir qué devuelve el endpoint cuando la reserva sale bien (ahora devuelve el objeto del dominio tal cual -> acoplamiento dominio/API).
2. Test del endpoint con pytest.
3. Más capacidades: consultar disponibilidad, cancelar/modificar, registrar usuario (sustituirá el `id`/`rol` provisionales que hoy manda el cliente).

Flujo: cada cosa nueva va en su rama + Pull Request.
