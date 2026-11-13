# Jugada Maestra · fábrica de Shorts

Canal de YouTube "Jugada Maestra": Shorts que explican la jugada genial detrás de una marca, narrados por **Tano, el mapache infiltrado**. **Cada Short sale en dos versiones: español neutro latinoamericano (sin voseo) e inglés** (`producir.py` hace las dos por defecto). Objetivo: canal rentable con producción automatizada (n8n + agentes) y control humano en 3 puntos.

## Antes de cualquier tarea
1. Leer `docs/APRENDIZAJES.md`: **reglas obligatorias** que salen de correcciones del usuario. Ninguna se puede romper.
2. Leer `docs/WORKFLOW_Short.md` (procedimiento) y `docs/ROADMAP_calidad.md` (qué mejorar en el próximo Short).
3. `docs/RESUMEN_canal.md` tiene el contexto completo del canal (nicho, estrategia, personaje, voz, historia); `docs/TEMARIO.md`, los próximos temas.

## División del trabajo
- El **guion** (ideas, datos con fuentes, `guion.json`, `claves.json`) se hace y aprueba en el chat de Claude del proyecto. Si llega un guion sin aprobar, preguntar antes de producir.
- **Acá** se produce: `video.html` → `python pipeline/producir.py shorts/NN_tema` → `NN_tema_ES.mp4` y `NN_tema_EN.mp4`.
- Inglés: `guion.json` lleva `en` y `numeros_en`; cada texto de `video.html` lleva su traducción en `data-en="..."` (la página la usa con `?lang=en`); las palabras ancla van en `en_claves.json`. Voz: Kokoro `am_michael`.

## Estructura
- `pipeline/`: `producir.py` (todo en un comando), `voz_lineas.py`, `armar_voz.py`, `sincronizar.py`, `render.py`, `sonido.py`, `mezclar.py`, `qc.py`, `preview.py`, `config.py` (rutas; se pisan con variables `JM_*`).
- `assets/mundo3d.js` + `assets/vendor/three.min.js`: mundo 3D low-poly desde el Short #4 (Tano 3D, ciudad neón, pedestales, paneles). Ver `docs/REFERENCIA_3D.md`.
- `assets/`: `tano.js` (personaje 2D), `sfx/` (efectos de Mixkit en `sfx/mixkit/` + respaldo CC0; `catalogo.json` por tipo, se regenera con `setup/bajar_sfx_mixkit.py`), `musica/` (Kevin MacLeod, CC BY), `voz/ref_8784.wav`, `CREDITOS.md`.
- `shorts/NN_tema/`: `guion.json`, `claves.json`, `video.html`, MP4 final. Los intermedios están en `.gitignore`.
- `assets/marcas/`: logos reales bajados con `setup/bajar_logo.py` (Wikimedia Commons) + `marcas.json` con fuente y licencia.
- `modelos/chatterbox/` y `modelos/kokoro/`: modelos de voz ES y EN (no versionados; los baja `setup/instalar.py`).
- Intermedios en inglés: mismo nombre con prefijo `en_` (`en_timeline.json`, `en_scene1.mp4`...); `voz_en.wav`.

## Comandos
```
python setup/instalar.py                                   # una vez por máquina
python pipeline/producir.py shorts/02_birkin               # Short completo, ES + EN
python pipeline/producir.py shorts/02_birkin --idioma en   # una sola versión
python pipeline/producir.py shorts/02_birkin --desde render
cd shorts/02_birkin && python ../../pipeline/preview.py video.html 0.5,2,4 prev.jpg [en]   # capturas de prueba
```

## Reglas técnicas que ya costaron errores
- Nunca acelerar/estirar la voz (suena "bajo el agua"); las escenas se adaptan a la voz.
- Animaciones de salida (`hide`) con `forwards`, nunca `both`.
- Todo elemento animado lleva `data-sfx`; los golpes clave van anclados a palabras en `claves.json`.
- Mirar capturas de prueba antes del render completo y la hoja `qc_fotogramas.jpg` después.
- Datos en pantalla = datos verificados de la ficha. No inventar frases de personas reales. **Logos reales sí, solo para identificar a la marca** (desde el Short #4, pedido del usuario): tal cual, sin deformar ni recolorear, nunca protagonista de la miniatura, sin sugerir patrocinio. Productos y diseños protegidos se siguen dibujando genéricos (el bolso sin herrajes de la Birkin).

## Al terminar un Short
Correr `qc.py` en los dos idiomas (lo hace `producir.py`), mirar `qc_fotogramas.jpg` y `en_qc_fotogramas.jpg`, entregar los dos MP4 + 5 títulos y descripción **en cada idioma** con créditos (`assets/CREDITOS.md`), anotar en `docs/APRENDIZAJES.md` cada corrección del usuario y marcar en `docs/ROADMAP_calidad.md` la mejora incorporada.
