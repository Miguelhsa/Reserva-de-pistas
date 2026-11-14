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
```
reservas-pistas/
├── dominio/
│   └── modelos.py        # Pista, Usuario, Reserva + reglas: se_solapa_con, choca_con_existentes,
│                         #   crear_reserva, crear_pista, consulta_pistas_libres
├── persistencia/
│   └── repositorio.py    # guardar/cargar reservas y pistas en JSON (si el archivo no existe → lista vacía)
├── interfaz/
│   ├── app.py            # crea la app y enchufa los routers (cuadro de enchufes)
│   ├── orquestador.py    # coordina cada flujo (no decide ni toca archivos): reservar, dar_de_alta_pista,
│   │                     #   consulta_disponibilidad
│   └── routers/
│       ├── reservas.py   # POST /reserva, GET /reserva/disponibilidad (moldes In/Out, 409, Depends de rutas)
│       └── pistas.py     # POST /pista (PistaIn/PistaOut, 409)
├── test/                 # un archivo por capa/puerta: test_dominio, test_persistencia,
│                         #   test_endpoint_reservas, test_endpoint_pistas
├── conftest.py           # vacío: pone la raíz en el path para pytest
├── MAPA.html             # mapa visual interactivo (flujos, dependencias, tests)
└── README.md             # este mapa
```

## 5. Dominio: los objetos
- Pista: 
Atributos, numero de pista
- Reserva:
Atributos, numero de pista, usuarios, fecha, hora de inicio y fin de reserva
- Usuarios:
Atributos, ID, nombre, apellidos, rol

## 6. Estado y siguiente paso

**Hecho (3 capacidades completas, cada una con todas sus capas y tests — 16 en verde):**
- **Reservar una franja** — `POST /reserva` → `reservar()` → `crear_reserva` (no solapar → 409). Salida `ReservaOut` (sin id ni rol del usuario).
- **Dar de alta una pista** — `POST /pista` → `dar_de_alta_pista()` → `crear_pista` (número repetido → 409).
- **Consultar disponibilidad** — `GET /reserva/disponibilidad?fecha_inicio=&fecha_fin=` → `consulta_disponibilidad()` →
  `consulta_pistas_libres` (por cada pista, una reserva hipotética: si no choca, está libre) → `list[PistaOut]`.
- Rutas de los archivos inyectadas con `Depends` → los tests usan archivos de prueba con `dependency_overrides`.
- Arranque: `uv run fastapi dev interfaz/app.py` → `/docs`. Tests: `uv run pytest`.

**En curso: CANCELAR UNA RESERVA** (rama `feature/cancelar-reserva`). Modificar, más adelante (≈ cancelar + crear).

Decisiones de diseño:
- **Identificador:** cada reserva tiene un `id` propio, **UUID**, que genera el **DOMINIO** al crear la reserva
  (nunca viene de fuera: no se puede falsificar ni adivinar; no depende de la base de datos). Se cancela por `id`.
  *Por qué no pista+inicio:* al modificar una reserva cambiarían; el `id` se mantiene.
- **Puerta:** `DELETE /reserva/{id}` — el `id` va en el **path** (es la dirección de UNA reserva concreta).
  Si no existe → **404**.
- **Por capas:**
  - *Dominio:* `Reserva` gana el campo `id` (UUID). Nueva regla `cancelar_reserva(id, existentes)`: la quita de la lista
    o lanza error si no existe.
  - *Persistencia:* guardar y cargar el `id`. Las reservas antiguas de `reservas.json` (sin `id`) se borran: son de prueba.
  - *Orquestador:* nuevo flujo `cancelar`: cargar → `cancelar_reserva` → guardar (mismo patrón que `reservar`).
  - *Interfaz:* `ReservaOut` devuelve el `id` (si no, el socio no sabría qué cancelar) + endpoint `DELETE`
    (error del dominio → 404).

**Ideas para después:**
- «Mis reservas»: el socio, identificado, ve su listado (pista + fecha/hora) y elige cuál cancelar → depende de
  **registrar usuarios**.
- Con base de datos real: cargar solo las reservas de la franja consultada (filtro en persistencia).
- Avisar 24 h antes (tarea programada).

Flujo: cada pieza nueva va en su rama + Pull Request, con sus tests.
