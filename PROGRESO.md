# Progreso — Reservas de pista

Bitácora del proyecto. Se actualiza al final de cada sesión. El mapa (arquitectura, objetos)
vive en `README.md`; aquí va el "por dónde vamos".

## Estado actual

- **Proyecto:** motor de reservas de pista de pádel. Backend por capas (interfaz / dominio / persistencia).
- **Regla de negocio central:** una franja de una pista no se puede reservar dos veces (no solapar).
- **Fase:** DOMINIO completo (modelos, regla `se_solapa_con` + `choca_con_existentes`, `crear_reserva`) y PERSISTENCIA completa (`guardar` + `cargar` a JSON en `persistencia/repositorio.py`), verificada con round-trip (guardar → cargar → `==` da True). Fase 0 hecha.
- **Última sesión:** 2026-10-24.
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
- **MOLDE DE SALIDA — HECHO y FUSIONADO a `main` (2026-10-10, rama `feature/molde-salida`):** `UsuarioOut(nombre, apellidos)` +
  `ReservaOut(pista: int, usuarios: list[UsuarioOut], fecha_inicio, fecha_fin)`; el router traduce dominio → `ReservaOut` al
  salir (simétrico a la entrada) y el decorador lleva `response_model=ReservaOut`. La respuesta ya NO expone `id` ni `rol`.
  Probado con un set de 8 casos manuales en `/docs` (200 libre, 409 idéntica/parcial/contenida, 200 pegada, 200 otra pista,
  422 tipo incorrecto, 422 campo que falta) — todos correctos.
- **README al día** (secciones 4 Carpetas y 6 Estado/siguiente paso).
- **TESTS DEL ENDPOINT — HECHOS Y FUSIONADOS (2026-10-21, rama `feature/test-endpoint` → PR → merge):**
  - El endpoint pide la ruta con `ruta: str = Depends(get_ruta)` (`get_ruta()` en `routers/reservas.py`).
  - `test/test_endpoint.py`: `RUTA_PRUEBA = "test_reservas.json"`, `get_ruta_test()`, `cliente = TestClient(app)`, y 3 tests
    INDEPENDIENTES (cada uno: `guardar([], RUTA_PRUEBA)` → `dependency_overrides[get_ruta] = get_ruta_test` → POSTs →
    asserts → `.clear()`): reserva libre → 200 + `respuesta_esperada` (sin id/rol); reserva pegada (19:30) → 200;
    reserva que solapa → 409 + `{"detail": "Esa franja ya esta reservada"}`. `reservas.json` real verificado intacto.
  - `.gitignore`: `practicas/` y `test_reservas.json`. Ejercicio aparte de Depends en `practicas/` (local, no versionado).
- **Pendientes pequeños de tests: HECHOS** (rama `feature/limpieza-tests`, mergeada): `respuesta`, `respuesta_previa`,
  `respuesta_esperada`, `test_reserva_libre_se_acepta`; 200 del POST de preparación comprobado; basura de pista 0 borrada.
- **NUEVA CAPACIDAD EN CURSO: "dar de alta una pista"** (rama `feature/alta-pista`, sin commitear). Decidido por él:
  primero alta de pista (para practicar el ciclo completo) y DESPUÉS "consultar disponibilidad" (que necesita la lista de
  pistas del club). Cancelar queda para más tarde (requiere decidir cómo identificar una reserva: pista+inicio o un `id`).
  - Regla de negocio: no se puede dar de alta una pista con un número que ya existe → `ValueError` → (409 en la API).
  - Dominio HECHO: `crear_pista(nueva: Pista, existentes: list[Pista]) -> Pista` (bucle comparando `.numero`, `append` FUERA
    del bucle, devuelve la nueva). Tests en `test_dominio.py`: número nuevo (`assert nueva in existentes`) y repetido
    (`pytest.raises`). 8 passed.
  - SIGUIENTE: persistencia de pistas. Pregunta abierta: ¿mismo `repositorio.py` o archivo nuevo?, ¿cómo nombrar las
    funciones si ya existen `guardar`/`cargar`? Luego orquestador → router `/pista` (+moldes, include_router) → tests endpoint.

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

### 2026-10-07 / 10 — README al día + MOLDE DE SALIDA (dominio y API desacoplados por los dos lados) + PR fusionado
- Hecho: actualizó el README (sección 4: rol de `app`, `orquestador`, `router`, `modelos`, `persistencia`; la 6 la reescribió el
  mentor a petición suya). Decidió qué ve el socio en la confirmación (pista, quién juega, cuándo) y qué NO (id, rol). Escribió
  `UsuarioOut`/`ReservaOut`, la traducción dominio → salida con bucle, y `response_model`. Rama `feature/molde-salida` → PR → merge.
- Aprendió: traducir al entrar Y al salir (el borde aísla el dominio en ambos sentidos); `response_model` = contrato de salida
  (documenta en `/docs` y filtra lo que sale); **Pydantic solo acepta argumentos con nombre** (`campo=valor`), las dataclass
  también por posición — dos moldes, ambos crean objetos, reglas distintas para rellenarlos; sacar un `int` de dentro de un
  objeto (`.pista.numero`); `fastapi dev` recarga solo al guardar (solo hay que refrescar `/docs`).
- Atascos: en el README describió el router como "endpoints y su lógica" (contradice su regla de interfaz sin lógica) y el
  orquestador como si guardara él; empezó a trabajar en `main` sin rama (avisado → creó la rama sin perder cambios); construyó
  los `Out` por posición y metió el objeto `Pista` donde iba un `int` — no lo había probado antes de enseñarlo.
- Funcionó: apoyarse en SU código (`HTTPException(status_code=..., detail=...)`, `response_model` del inmobiliario) como pista;
  un set de pruebas con resultado esperado para que prediga antes de ejecutar.
- Dudas para la próxima: ninguna abierta. Empezar por el test del endpoint (pytest + cliente de pruebas de FastAPI).

### 2026-10-12 / 13 — Test del endpoint: refactor a `Depends(get_ruta)` + ejercicio aparte de `Depends`
- Hecho: razonó por qué un test no puede usar el `reservas.json` real (2ª ejecución → 409; ensucia datos; un test debe dar
  siempre el mismo resultado). Recordó `Depends` del inmobiliario. Escribió `get_ruta` y la inyectó como parámetro del
  endpoint. Pidió un ejercicio aparte para entenderlo: hizo la mini-app (`/saludo` con Depends como parámetro, `/secreto`
  con `dependencies=[...]` en el decorador) y su primer test de endpoint con `TestClient` (`1 passed`).
- Aprendió: `Depends` = FastAPI llama a la función ANTES del endpoint (no tú); en el decorador → control de paso, el valor
  se tira; como parámetro → te entrega el valor. Por eso se puede sustituir desde fuera en un test. `print` va a la terminal
  (cocina), `return` al cliente. `pytest -v` (nombre de cada test) y `-s` (deja ver los print). Un test necesita
  `def test_...()` sin parámetros, guardar la respuesta y `assert` sobre `.status_code` y `.json()`.
- Atascos: muchos. `return "RUTA_RESERVAS"` con comillas (texto literal en vez de la variable); función nombrada
  `get_repositorio` (copiada); definida DEBAJO del endpoint; volvió a poner `pista: Pista` en `ReservaOut`; puso
  `Depends(get_ruta)` en el decorador y luego `dependencies=[...]` como parámetro de función (confunde los dos sitios);
  propuso un `if` test/real dentro de `get_` (se explicó que el código de producción no debe saber de tests). El test 1 se
  le dio hecho (último peldaño) y se explicó línea a línea con su porqué.
- Dudas para la próxima: **repasar `Depends` y decorador vs. parámetro** (lo pidió explícitamente). Después test 2 del
  ejercicio (él solo) y el test real del endpoint de reservas.

### 2026-10-17 / 21 — Repaso de Depends + tests del endpoint (3, independientes) + PR fusionado
- Hecho: repasó `Depends` (decorador = control de paso, el valor se tira; parámetro = te entrega el valor); se corrigió que
  el valor va DE la función AL parámetro, no al revés. Cerró la práctica (`dependency_overrides` + `.clear()`; `TestClient`
  sí prueba el endpoint, no solo funciones). Escribió `test/test_endpoint.py` con 3 tests y los separó en independientes.
  Rama → PR → merge.
- Aprendió: lo que manda el cliente es entrada (molde); lo que pone el servidor es `Depends`. Tres formatos de una reserva
  (entrada API / salida API / archivo JSON) — no mezclarlos. Reset con `guardar([], RUTA)` reutilizando su persistencia.
  Un test = una cosa; cada test monta su propio escenario (ejecutable solo y en cualquier orden). `.clear()` a mitad de test
  = el siguiente POST va a los datos REALES. FastAPI responde un `HTTPException` como `{"detail": "..."}`. `-v` / `-s`.
  Infografía del recorrido de pytest en `practicas/recorrido_pytest.html`.
- Atascos: muchos de comprensión (dirección del Depends, para qué el `.clear()`, qué hace cada línea del test); renombró las
  funciones de la app con `test_` (confunde el prefijo); intentó encadenar tests que dependían del anterior; copió el formato
  del archivo JSON como si fuera el de la API; `.clear()` en mitad del test. Pidió varias veces el código hecho (se le dio el
  diccionario del caso 1 y el assert de la respuesta esperada).
- Fortalezas: explicó con sus palabras lo que hace cada línea; razonó la limpieza del archivo; propuso él el test del caso
  límite (pegada).
- Dudas para la próxima: ninguna abierta. Arrancar con los pendientes pequeños y elegir la siguiente capacidad.

### 2026-10-23 / 24 — Limpieza de tests + elección de capacidad + dominio de "alta de pista"
- Hecho: pendientes de tests cerrados y mergeados. Razonó la siguiente capacidad (consultar/cancelar reutilizan lo hecho;
  cancelar exige identificar una reserva → consultar primero; consultar necesita la lista de pistas → alta de pista primero,
  "para practicar"). Diseñó por capas, encontró la regla (número repetido) y escribió `crear_pista` + 2 tests.
- Aprendió: el dominio RECIBE los datos, no los muestra ni los pide (su README lo prohíbe); un parámetro es un "apodo" de lo
  que pasa quien llama (y por eso el `append` modifica la lista del orquestador); el `else` dentro del bucle (misma trampa
  que en `choca_con_existentes`); `in` + igualdad de dataclass vs comparar `.numero` explícito; `assert` (condición verdadera)
  vs `pytest.raises` (se espera el error); los tests del dominio van en `test_dominio.py`, los de la puerta en `test_endpoint.py`;
  renombrar con F2 en VS Code (Cmd+Shift+L partió `respuesta_esperada`).
- Atascos: renombró la cosa equivocada (la cafetera como `respuesta`); propuso una función de dominio que mostraba y pedía datos;
  metió los tests de pista en `test_endpoint.py`; pidió el código hecho varias veces (se le dio el test 1 de pista).
- **Petición nueva (en CLAUDE.md):** explicar SIEMPRE el porqué de cada cosa.

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
- [x] Molde de salida (`...Out` + `response_model`): traducir dominio → salida en el borde; no exponer datos internos (id, rol).
- [x] Pydantic se construye solo con argumentos con nombre (`campo=valor`); dataclass admite también posición.
- [x] Tests de endpoint con `TestClient` + `dependency_overrides`: inyectar una ruta de prueba, resetear el archivo, tests independientes.
- [x] Testing con pytest: archivos `test_*.py` y funciones `def test_*()` (sin parámetros, o pytest los toma por fixtures); `assert` / `assert not`; `pytest.raises` para afirmar que se lanza una excepción; `conftest.py` vacío en la raíz resuelve el `ModuleNotFoundError` (pone la raíz en el path); cubrir caso positivo Y negativo (+ límite).

## A vigilar (puntos flacos crónicos)

- Tiende a empezar por los OBJETOS/piezas en vez de por capacidades/capas.
- Tiende a nombrar por la tecnología (frontend, bbdd) en vez de por el rol (interfaz, persistencia).
- Prefijo `test_` solo para funciones que SON tests (no para las piezas que usan, ni para la app).
- Tests que dependen del anterior: cada test monta su escenario.
- Confunde los dos sitios de `Depends` (decorador vs. parámetro) — repasar hasta que salga solo.
- Comillas vs. variable: `"RUTA"` (texto) vs `RUTA` (valor).
- Enseña código sin probarlo antes: pedirle que lo ejecute/pruebe él antes de pasarlo a revisión.
- Olvida crear la rama antes de empezar (empezó en `main` el 2026-10-10).
- Sesiones largas de pasos pequeños encadenados le saturan (2026-10-03 tarde): cortar antes, recolocar el mapa más a menudo, y preferir analogías a tablas.
- Con temas NUEVOS o desconocidos (p.ej. git), ir aún más despacio y UNA sola cosa a la vez: se abruma si se le juntan varios pasos o jerga nueva (pasó al arrancar el 2026-09-23).
