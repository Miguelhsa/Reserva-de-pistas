# Progreso — Reservas de pista

Bitácora del proyecto. Se actualiza al final de cada sesión. El mapa (arquitectura, objetos)
vive en `README.md`; aquí va el "por dónde vamos".

## Estado actual

- **Proyecto:** motor de reservas de pista de pádel. Backend por capas (interfaz / dominio / persistencia).
- **Regla de negocio central:** una franja de una pista no se puede reservar dos veces (no solapar).
- **Fase:** Fase 0 (higiene) TERMINADA. Diseño (macro + objetos) completo en el README.
- **Última sesión:** 2026-09-18.
- **Repo:** github.com/Miguelhsa/Reserva-de-pistas (rama `main`).
- **Siguiente paso:** entrar al DOMINIO →
  1. crear las carpetas de las capas (`interfaz/`, `dominio/`, `persistencia/`),
  2. retirar el `main.py` de ejemplo de `uv`,
  3. picar las dataclasses `Pista`, `Reserva`, `Usuario` (tipadas de nacimiento),
  4. empezar a dar forma a la regla de no solapar.
- **Pendiente de commit:** cambios sin fotografiar en `README.md` (sección 6) y este `PROGRESO.md`.

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

## Conceptos afianzados (demostrados, no solo leídos)

- [x] Separación en capas y el "qué hace / qué tiene prohibido" de cada una.
- [x] Dirección de dependencias (apunta al dominio) distinta del flujo de datos (va y vuelve).
- [x] Modelado de dominio: la Reserva como franja; no filtrar detalles de persistencia en el dominio.
- [x] Higiene de proyecto: uv/pyproject, entorno aislado, .gitignore (versionar la receta, no el plato),
      git (staging → commit), push a GitHub.

## A vigilar (puntos flacos crónicos)

- Tiende a empezar por los OBJETOS/piezas en vez de por capacidades/capas.
- Tiende a nombrar por la tecnología (frontend, bbdd) en vez de por el rol (interfaz, persistencia).
