# Jugada Maestra · fábrica de Shorts

Canal de YouTube "Jugada Maestra": Shorts que explican la jugada genial detrás de una marca, narrados por **Tano, el mapache infiltrado**. Dos versiones: español neutro latinoamericano (sin voseo) e inglés. Objetivo: canal rentable con producción automatizada (n8n + agentes) y control humano en 3 puntos.

## Antes de cualquier tarea
1. Leer `docs/APRENDIZAJES.md`: **reglas obligatorias** que salen de correcciones del usuario. Ninguna se puede romper.
2. Leer `docs/WORKFLOW_Short.md` (procedimiento) y `docs/ROADMAP_calidad.md` (qué mejorar en el próximo Short).
3. `docs/RESUMEN_canal.md` tiene el contexto completo del canal (nicho, estrategia, personaje, voz, historia).

## División del trabajo
- El **guion** (ideas, datos con fuentes, `guion.json`, `claves.json`) se hace y aprueba en el chat de Claude del proyecto. Si llega un guion sin aprobar, preguntar antes de producir.
- **Acá** se produce: `video.html` → `python pipeline/producir.py shorts/NN_tema`.

## Estructura
- `pipeline/`: `producir.py` (todo en un comando), `voz_lineas.py`, `armar_voz.py`, `sincronizar.py`, `render.py`, `sonido.py`, `mezclar.py`, `qc.py`, `preview.py`, `config.py` (rutas; se pisan con variables `JM_*`).
- `assets/`: `tano.js` (personaje), `sfx/` (377 efectos CC0 + `catalogo.json`), `musica/` (Kevin MacLeod, CC BY), `voz/ref_8784.wav`, `CREDITOS.md`.
- `shorts/NN_tema/`: `guion.json`, `claves.json`, `video.html`, MP4 final. Los intermedios están en `.gitignore`.
- `modelos/chatterbox/`: modelo de voz (no versionado; lo baja `setup/instalar.py`).

## Comandos
```
python setup/instalar.py                                   # una vez por máquina
python pipeline/producir.py shorts/02_birkin               # Short completo
python pipeline/producir.py shorts/02_birkin --desde render
cd shorts/02_birkin && python ../../pipeline/preview.py video.html 0.5,2,4 prev.jpg   # capturas de prueba
```

## Reglas técnicas que ya costaron errores
- Nunca acelerar/estirar la voz (suena "bajo el agua"); las escenas se adaptan a la voz.
- Animaciones de salida (`hide`) con `forwards`, nunca `both`.
- Todo elemento animado lleva `data-sfx`; los golpes clave van anclados a palabras en `claves.json`.
- Mirar capturas de prueba antes del render completo y la hoja `qc_fotogramas.jpg` después.
- Datos en pantalla = datos verificados de la ficha. No inventar frases de personas reales. No reproducir logos ni diseños protegidos (el bolso es genérico, sin herrajes de la Birkin).

## Al terminar un Short
Correr `qc.py` (lo hace `producir.py`), entregar MP4 + 5 títulos + descripción con créditos (`assets/CREDITOS.md`), anotar en `docs/APRENDIZAJES.md` cada corrección del usuario y marcar en `docs/ROADMAP_calidad.md` la mejora incorporada.
