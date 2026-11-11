# Roadmap de calidad visual

Regla: **cada Short incorpora al menos una mejora de esta lista.** Al terminarla, se marca con el número del Short.

## Referencia
Video de referencia del usuario: "La psicología de las personas flojas pero ambiciosas" (7 min, horizontal, 24 fps).
Lo que hace bien y nosotros no (las técnicas se adoptan; su personaje y su estética exacta NO se copian):
1. **Paleta unificada por video + luz:** todo en una gama de color, brillos suaves (glow/bloom), viñeta, textura sutil.
2. **El personaje actúa:** camina con ciclo de pasos, se sienta, se acuesta, cambia de expresión, globos de pensamiento.
3. **Cámara con profundidad:** desenfoque de fondo cuando algo pasa adelante, zoom, inclinación 3D, transiciones glitch.
4. **Escenarios recurrentes:** living, montaña, parque, habitación con ventana; la historia vuelve a ellos.
5. **Texto chico y dentro de la escena** (rótulos que señalan), no solo subtítulos gigantes.
6. **Metáforas visuales simples:** una pelota que cae por una curva = "seguir es fácil".

## Mejoras, en orden sugerido
| # | Mejora | Esfuerzo | Estado |
|---|---|---|---|
| 1 | **Look cinematográfico:** paleta por Short, glow en elementos clave, viñeta, grano sutil, sombras suaves (CSS filters / capas) | Bajo | pendiente |
| 2 | **Cámara:** zoom lento continuo por escena, paneos, desenfoque de fondo (DOF) al destacar un objeto | Bajo | pendiente |
| 3 | **Transiciones:** glitch/RGB-split, whip-pan con desenfoque de movimiento, match-cut | Bajo | pendiente |
| 4 | **Tano en partes (rig):** cabeza, ojos (parpadeo), cejas, boca (abre/cierra con la voz), brazos, piernas, cola | Alto, una vez | pendiente |
| 5 | **Tano actúa:** poses (señalar, sorpresa, pensar, celebrar), caminar, globos de pensamiento | Medio | pendiente |
| 6 | **Boca sincronizada con la voz** (amplitud del audio → apertura de boca) | Medio | pendiente |
| 7 | **Biblioteca de escenarios** vectoriales reutilizables (tienda, oficina, tribunal, fábrica, calle) | Alto, incremental | pendiente |
| 8 | **Migrar a Remotion** (React): springs con física, motion blur, mejor composición. Evaluar cuando 1–6 estén hechas | Alto | evaluar |
| 9 | **Subtítulos palabra por palabra** con resaltado (marcas de Whisper) | Medio | pendiente |
| 10 | Versión en inglés automática desde el mismo `video.html` (textos en `guion.json`) | Medio | pendiente |
