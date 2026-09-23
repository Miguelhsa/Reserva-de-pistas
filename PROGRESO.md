# Progreso — Reservas de pista

Bitácora del proyecto. Se actualiza al final de cada sesión. El mapa (arquitectura, objetos)
vive en `README.md`; aquí va el "por dónde vamos".

## Estado actual

- **Proyecto:** motor de reservas de pista de pádel. Backend por capas (interfaz / dominio / persistencia).
- **Regla de negocio central:** una franja de una pista no se puede reservar dos veces (no solapar).
- **Fase:** Dominio. Regla COMPLETA: método atómico `Reserva.se_solapa_con(otra)` + función `choca_con_existentes(nueva, existentes)` que la comprueba contra la lista. Todo probado en REPL. Fase 0 hecha.
- **Última sesión:** 2026-09-23.
- **Repo:** github.com/Miguelhsa/Reserva-de-pistas (rama `main`).
- **Flujo de trabajo:** en equipo — rama de feature + Pull Request para cada cosa nueva (no picar directo en `main`). Primer ciclo de PR completado el 2026-09-23.
- **Siguiente paso:** atar la regla a un flujo de "crear reserva" (que use `choca_con_existentes` antes de aceptar) y empezar a asomarse a la PERSISTENCIA (¿dónde viven las reservas existentes?). Pendiente también: primeros tests con pytest.

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

## A vigilar (puntos flacos crónicos)

- Tiende a empezar por los OBJETOS/piezas en vez de por capacidades/capas.
- Tiende a nombrar por la tecnología (frontend, bbdd) en vez de por el rol (interfaz, persistencia).
- Con temas NUEVOS o desconocidos (p.ej. git), ir aún más despacio y UNA sola cosa a la vez: se abruma si se le juntan varios pasos o jerga nueva (pasó al arrancar el 2026-09-23).
