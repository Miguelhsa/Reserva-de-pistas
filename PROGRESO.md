# Progreso — Reservas de pista

Bitácora del proyecto. Se actualiza al final de cada sesión. El mapa (arquitectura, objetos)
vive en `README.md`; aquí va el "por dónde vamos".

## Estado actual

- **Proyecto:** motor de reservas de pista de pádel. Backend por capas (interfaz / dominio / persistencia).
- **Regla de negocio central:** una franja de una pista no se puede reservar dos veces (no solapar).
- **Fase:** DOMINIO completo (modelos, regla `se_solapa_con` + `choca_con_existentes`, `crear_reserva`) y PERSISTENCIA completa (`guardar` + `cargar` a JSON en `persistencia/repositorio.py`), verificada con round-trip (guardar → cargar → `==` da True). Fase 0 hecha.
- **Última sesión:** 2026-09-30.
- **Repo:** github.com/Miguelhsa/Reserva-de-pistas (rama `main`). `crear_reserva` fusionada por PR.
- **Flujo de trabajo:** en equipo — rama de feature + Pull Request para cada cosa nueva (no picar directo en `main`).
- **Persistencia:** FUSIONADA por PR (guardar + cargar en persistencia/repositorio.py).
- **Atar al flujo: HECHO** — `reservar(nueva, ruta)` en `interfaz/app.py` coordina `cargar` → `crear_reserva` → `guardar`. `crear_reserva` quedó PURA (el dominio no toca archivos). Probado end-to-end (la que cabe se añade; la que choca lanza ValueError y no se guarda). PR de `feature/flujo-reservar` — verificar al retomar si está fusionado.
- **Siguiente paso:** elegir entre (1) primeros **tests con pytest**, o (2) empezar la **INTERFAZ web con FastAPI**. (Dominio + persistencia + flujo ya están.) Nota: la persistencia aislada deja montado el capstone "JSON→Postgres solo toca persistencia".

## Bitácora

### 2026-09-13 — Elección de proyecto y arquitectura macro
- Hecho: elegido el proyecto (pista deportiva, la opción más limpia para aprender). Razonó él la
  arquitectura macro: 7 capacidades, 3 capas con su hace/prohibido, y la dirección de dependencias
  (interfaz → dominio ← persistencia).
- Atascos: confundir capacidades con objetos; flujo de datos con dirección de dependencias.

### 2026-09-16 / 17 — README como mapa vivo (secciones 1-5)
- Hecho: rellenó el README entero — qué es (+para quién), capacidades, capas (hace/prohibido),
  flechas, carpetas (una por capa, nombradas por rol) y objetos (Pista, Reserva como franja
  fecha+inicio+fin, Usuario con rol y sin filtrar la BBDD).
- Atascos: reincidió en mezclar "qué hace" con "con qué está hecho"; se re-explicó el flujo vs
  dependencia con el ejemplo del viaje de una reserva → lo entendió.

### 2026-09-18 — Fase 0: higiene de proyecto
- Hecho: `uv init` (pyproject, .python-version), `.gitignore` (ignora .venv, cachés, .env, .DS_Store),
  `git init`, config de identidad de git, primer commit (`b6568ea`) y push a GitHub.
- Atascos: licencia de Xcode sin aceptar (git no arrancaba); identidad de git sin configurar (falló el
  primer commit); `index.lock` suelto; rama `master` vs `main` al hacer push. Todo resuelto.

### 2026-09-20 — Dominio: modelos y la regla de solapamiento
- Hecho (modelos): `dominio/modelos.py` con las 3 dataclasses tipadas. Reserva compone `Pista` + `list[Usuario]` y la franja con dos `datetime`. Probado en REPL (composición navegable). `.venv` creado con `uv run`.
- Hecho (regla): método `Reserva.se_solapa_con(otra)` en una línea — `return misma_pista and inicio_self < fin_otra and inicio_otra < fin_self`. Probado: True cuando chocan, False cuando no.
- Atascos: el solapamiento costó (creía que bastaba una comparación; hacían falta las DOS con `and`); se lió con ifs/return antes de ver que se devuelve la condición directa. Resuelto.

### 2026-09-23 — Pieza 2 de la regla + primer Pull Request
- Hecho: función `choca_con_existentes(nueva, existentes)` en `dominio/modelos.py` — bucle `for` sobre la lista, `if nueva.se_solapa_con(existente): return True`, y `return False` al final. Probada en REPL.
- Flujo de equipo estrenado y completado: rama `feature/...` -> commit -> push -> Pull Request -> review (Files changed) -> merge -> borrar rama -> sync local (`switch main`, `pull`, `branch -d`).
- Atascos: arranque de sesión abrumado (se le juntaron git + diseño a la vez); bug de sangría (el `return False` dentro del `for` en vez de fuera) — lo cazó él solo.

### 2026-09-24 — crear_reserva + 2º Pull Request (casi solo)
- Hecho: `crear_reserva(nueva, existentes)` — `raise ValueError` si choca, si no `append` + `return nueva`. Pulida (sin `is True`) y probada. Fusionada por PR pilotado casi en solitario.

### 2026-09-26 — Persistencia: guardar (serializar a JSON)
- Hecho: capa `persistencia/repositorio.py`. `guardar(reservas, ruta)`: `asdict` a cada reserva -> `json.dump` al archivo con `default=str` (truco para los datetime). Crea `reservas.json` (al `.gitignore`: dato, no código).
- Aprendió: serializar; `asdict`; `datetime` no es JSON-serializable; `dump` (archivo) vs `dumps` (texto); list comprehension.

### 2026-09-30 — Persistencia: cargar (deserializar) — lo más difícil
- Hecho: `cargar(ruta)`: `json.load` (lista de dicts) -> bucle -> reconstruir a mano cada objeto (`Pista` desde el dict, `Usuario`s en bucle, fechas con `datetime.fromisoformat`). Verificado con round-trip (`==` da True).
- Costó (varias vueltas): json devuelve DICTS, no objetos (acceso `["clave"]`, no `.atributo`); reconstruir lo anidado; la pista es un dict único (no lista), los usuarios sí lista; la sangría del `return`. Perseveró y lo sacó.

### 2026-10-01 — Atar la persistencia al flujo
- Hecho: `interfaz/app.py` con `reservar(nueva, ruta)`: coordina `cargar` → `crear_reserva` → `guardar`. Probado end-to-end (la que cabe se añade; la que choca lanza ValueError y no se guarda).
- Diseño: entendió que el front y el coordinador son papeles distintos del "borde"; `reservar` se quedó en interfaz por YAGNI (sin capa `aplicacion` aparte). Tendía a guardar solo la reserva nueva en vez de la lista completa; corregido.

## Conceptos afianzados (demostrados, no solo leídos)

- [x] Separación en capas y el "qué hace / qué tiene prohibido" de cada una.
- [x] Dirección de dependencias (apunta al dominio) distinta del flujo de datos (va y vuelve).
- [x] Modelado de dominio: la Reserva como franja; no filtrar detalles de persistencia en el dominio.
- [x] Higiene de proyecto: uv/pyproject, entorno aislado, .gitignore (versionar la receta, no el plato),
      git (staging → commit), push a GitHub.
- [x] Dataclass tipada (`:` anota, no `=` asigna); molde (clase) vs objeto (instancia); guardar objetos en variables.
- [x] Composición con objetos reales; `datetime` como clase que se instancia; argumentos por posición vs con nombre.
- [x] Lógica de solapamiento de franjas (dos comparaciones con `and`); una función sí/no devuelve la condición directamente.
- [x] Recargar el REPL para ver cambios del archivo; predecir-y-comprobar al testear.
- [x] Recorrer una lista con `for` + decidir con `if`/`se_solapa_con`; patrón "return True a la primera, return False al final".
- [x] La sangría en Python define qué va dentro/fuera de un bucle (bug del `return` dentro vs. fuera del `for`).
- [x] Flujo de trabajo en equipo con git: rama de feature, commit, push, Pull Request, review, merge, sync y borrado de rama.

- [x] Serialización/deserialización: objeto <-> texto JSON. `asdict`; `json.dump`/`dumps` y `load`/`loads` (la `s` = string/texto); `datetime` con `.isoformat()` y `datetime.fromisoformat()`.
- [x] Reconstruir objetos anidados desde dicts: json devuelve dicts (acceso `["clave"]`, no `.atributo`); acceso encadenado; construir cada objeto desde sus campos.
- [x] List comprehension; una carpeta es paquete importable sin `__init__.py` (namespace package).

## A vigilar (puntos flacos crónicos)

- Tiende a empezar por los OBJETOS/piezas en vez de por capacidades/capas.
- Tiende a nombrar por la tecnología (frontend, bbdd) en vez de por el rol (interfaz, persistencia).
- Con temas NUEVOS o desconocidos (p.ej. git), ir aún más despacio y UNA sola cosa a la vez: se abruma si se le juntan varios pasos o jerga nueva (pasó al arrancar el 2026-09-23).
