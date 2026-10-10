# Progreso — Reservas de pista

Bitácora del proyecto. Se actualiza al final de cada sesión. El mapa (arquitectura, objetos)
vive en `README.md`; aquí va el "por dónde vamos".

## Estado actual

- **Proyecto:** motor de reservas de pista de pádel. Backend por capas (interfaz / dominio / persistencia).
- **Regla de negocio central:** una franja de una pista no se puede reservar dos veces (no solapar).
- **Fase:** DOMINIO completo (modelos, regla `se_solapa_con` + `choca_con_existentes`, `crear_reserva`) y PERSISTENCIA completa (`guardar` + `cargar` a JSON en `persistencia/repositorio.py`), verificada con round-trip (guardar → cargar → `==` da True). Fase 0 hecha.
- **Última sesión:** 2026-10-04.
- **Repo:** github.com/Miguelhsa/Reserva-de-pistas (rama `main`). `crear_reserva` fusionada por PR.
- **Flujo de trabajo:** en equipo — rama de feature + Pull Request para cada cosa nueva (no picar directo en `main`).
- **Persistencia:** FUSIONADA por PR (guardar + cargar en persistencia/repositorio.py).
- **Atar al flujo: HECHO** — `reservar(nueva, ruta)` en `interfaz/app.py` coordina `cargar` → `crear_reserva` → `guardar`. `crear_reserva` quedó PURA (el dominio no toca archivos). Probado end-to-end (la que cabe se añade; la que choca lanza ValueError y no se guarda). PR de `feature/flujo-reservar` — verificar al retomar si está fusionado.
- **Tests: ESTRENADOS** — pytest configurado (Fase 0 ampliada: `uv add --dev pytest`, carpeta `test/`, `conftest.py` vacío en la raíz para el path) y **3 tests del dominio escritos por él**, pasando (`3 passed`), fusionados a `main` por PR #5. Flujo de equipo pilotado casi en solitario.
- **INTERFAZ web — primer endpoint HECHO y FUSIONADO a `main` (2026-10-04):** `interfaz/app.py` (cableado: `FastAPI()` +
  `include_router`), `interfaz/orquestador.py` (`reservar`), `interfaz/routers/reservas.py` (moldes `UsuarioIn`/`ReservaIn` +
  `POST /reserva` → `solicitar_reserva`). Flujo completo: recibe → traduce a `Reserva` del dominio → `reservar()` → contesta;
  si la franja choca, `except ValueError` → `raise HTTPException(409)`. Probado por `/docs`: 1er envío guarda, 2º idéntico → 409.
  Arranque: `uv run fastapi dev interfaz/app.py`. `__init__.py` añadidos en `interfaz/` y `interfaz/routers/`.
- **Siguiente paso:** (1) actualizar él el README (sección 4 Carpetas y 6 Siguiente paso); (2) **molde de SALIDA** — ahora el
  endpoint devuelve el objeto del dominio tal cual (acoplamiento dominio↔API; en el inmobiliario lo resolvió con `response_model`).
  Después: test del endpoint con pytest, y más capacidades (consultar disponibilidad, cancelar…).

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

### 2026-10-03 — Primeros tests con pytest + 5º Pull Request
- Hecho: puso pytest en el proyecto (`uv add --dev pytest`, carpeta `test/`, y `conftest.py` **vacío en la raíz** para que pytest tenga la raíz en el path). Escribió **3 tests** en `test/test_dominio.py`: (1) dos reservas que se pisan → `se_solapa_con` True; (2) dos pegadas (una acaba a las 21:00, otra empieza a las 21:00) → False (con `assert not`); (3) `crear_reserva` contra una lista con un choque → `with pytest.raises(ValueError)`. `3 passed`. Fusionado a `main` por PR #5.
- Aprendió: para qué sirven los tests; un test necesita cubrir el caso positivo Y el negativo (una función que devolviera siempre True pasaría el primero); el caso límite de franjas pegadas; `assert` / `assert not`; `pytest.raises` para comprobar que algo lanza una excepción; los tests crecen CON el proyecto, no al final.
- Petición registrada en el CLAUDE.md general: incluir SIEMPRE pytest desde el inicio en cada proyecto.
- Atascos: casi ninguno — pilotó el PR (push, abrir PR, merge, sync) casi solo; solo preguntó la sintaxis de `git push -u origin <rama>` y recordar que el `switch main` + `pull` es el ÚLTIMO paso (tras el merge en GitHub), no antes.

### 2026-10-03 (tarde) — Arranca la INTERFAZ web (FastAPI): diseño + molde de entrada
- Hecho: eligió el primer endpoint — POST de reserva que llama a `reservar()` (no a `crear_reserva`, porque esa no guarda).
  Al principio propuso "crear usuario"; se reconsideró porque esa capacidad no tiene dominio ni persistencia aún (la API es
  el camarero: solo lleva pedidos a una cocina que exista). Diseñó el árbol de `interfaz/`: `app.py` (cableado),
  `orquestador.py` (`reservar`, nombrado por su ROL) y `routers/reservas.py`; movió `reservar` él solo. `uv add "fastapi[standard]"`.
  Escribió el molde Pydantic: `UsuarioIn(id, nombre, apellidos, rol)` + `ReservaIn(pista: int, usuarios: list[UsuarioIn],
  fecha_inicio, fecha_fin)`. Vio solo que la lista de usuarios necesita su propio molde. `pista: int` (bien simplificado).
- Decisión: `id` y `rol` los manda el cliente de forma PROVISIONAL (opción A, la más barata de tirar); en el diseño final
  saldrán de la BBDD de usuarios cuando exista "registrar usuario" (riesgo anotado: cliente mandando `"rol": "admin"`).
- Atascos: la explicación con tabla no le llegó (funcionó la analogía camarero/cocina); en el árbol se le cayó dos veces el
  orquestador; nombres del molde no casaban con el dominio (`apellido`, `fecha_final`) + falta de `:` en la clase. Al llegar a
  "pasos del endpoint" se bloqueó y cortó la sesión: "no me estoy enterando de nada". Sesión larga de pasos pequeños
  encadenados → se saturó.
- Nota: VS Code muestra "No module named pip" en el venv de uv — ruido inofensivo de la extensión de Python.
- Dudas para la próxima: retomar con el MAPA del endpoint (camarero: recibe `ReservaIn` → traduce a `Reserva` del dominio →
  `reservar()` → responde / error si choca), en corto y con analogía. Luego que escriba los pasos 1-3 (traducción).

### 2026-10-04 — Endpoint POST de reserva COMPLETO (los 4 pasos del "camarero") + PR fusionado
- Hecho: esqueleto del router (`APIRouter(prefix="/reserva", tags=[...])`, `@router.post`), cableado en `app.py`, y el cuerpo de
  `solicitar_reserva`: construye `Pista`, lista de `Usuario` (bucle, mismo patrón que `cargar()` con `.atributo`) y la `Reserva`;
  llama a `reservar(reserva, RUTA_RESERVAS)` (constante arriba del archivo); `try/except ValueError` → `raise HTTPException(409)`.
  Probado de punta a punta por `/docs`. Rama → PR → merge a `main` pilotado por él.
- Aprendió: `fastapi dev` necesita `__init__.py` para encontrar la raíz (a Python no le hacen falta; a la herramienta sí) —
  eligió ponerlos; leer un traceback buscando SUS archivos e ignorando `.venv`; un archivo JSON vacío no es una lista vacía
  (`[]`), y `guardar` escribe una lista de dicts; Pydantic ya convierte a `datetime` (no re-envolver con `datetime(...)`);
  fechas con `Z` (con zona) no se pueden comparar con las sin zona; 409 Conflict; el borde traduce el error de negocio a HTTP
  (el dominio no sabe de códigos); `raise` vs crear la excepción sin lanzarla; `except` con tipo concreto como filtro.
- Atascos: no recordaba montar router ni import (se resolvió enseñándole SU código de control-gastos); `prefix` sin `/` y
  `.Post` en mayúscula; nombres (`registrar` copiado, errata `rentrada_reserva`) → acabó en `solicitar_reserva`; la HTTPException
  sin `raise` y `except:` a secas — se atascó y hubo que subir a pseudocódigo con huecos.
- Funcionó: arrancar con el mapa de 4 pasos (camarero) y volver a él tras cada paso; usar su propio código antiguo como chuleta.
- Dudas para la próxima: ninguna abierta. Empezar por el molde de salida (qué devuelve cuando sale bien).

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

- [x] Molde de entrada Pydantic con modelo anidado (`list[UsuarioIn]`) en el borde, separado del dominio (dataclass).
- [x] Endpoint FastAPI completo: router + cableado, traducir entrada Pydantic → objeto de dominio, llamar al orquestador, y traducir el error de dominio a HTTP (`try/except ValueError` + `raise HTTPException(409)`).
- [x] Testing con pytest: archivos `test_*.py` y funciones `def test_*()` (sin parámetros, o pytest los toma por fixtures); `assert` / `assert not`; `pytest.raises` para afirmar que se lanza una excepción; `conftest.py` vacío en la raíz resuelve el `ModuleNotFoundError` (pone la raíz en el path); cubrir caso positivo Y negativo (+ límite).

## A vigilar (puntos flacos crónicos)

- Tiende a empezar por los OBJETOS/piezas en vez de por capacidades/capas.
- Tiende a nombrar por la tecnología (frontend, bbdd) en vez de por el rol (interfaz, persistencia).
- Sesiones largas de pasos pequeños encadenados le saturan (2026-10-03 tarde): cortar antes, recolocar el mapa más a menudo, y preferir analogías a tablas.
- Con temas NUEVOS o desconocidos (p.ej. git), ir aún más despacio y UNA sola cosa a la vez: se abruma si se le juntan varios pasos o jerga nueva (pasó al arrancar el 2026-09-23).
