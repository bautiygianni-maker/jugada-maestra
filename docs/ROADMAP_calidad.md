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

## Meta: animación cinematográfica adictiva
El usuario quiere que cada Short sea mejor que el anterior hasta llegar a una animación cinematográfica que enganche.
"Cinematográfica" = personaje vivo + cámara + luz + transiciones + diseño de sonido.
"Adictiva" = retención: algo nuevo cada 1–2 s, preguntas abiertas que se cierran tarde, final que conecta con el inicio.

### Plan Short por Short (una o dos mejoras grandes por video)
| Short | Mejoras | Estado |
|---|---|---|
| #3 Costco | Look (1) + zoom de cámara (2, parcial) + **biblioteca de sonidos Mixkit** | hecho |
| #4 | **Tano en partes (4) + parpadeo + boca con la voz (6)**: el salto más grande, el personaje deja de ser una figura fija | próximo |
| #5 | **Transiciones (3)** + cámara completa (2): paneo, desenfoque de fondo, whip-pan con whoosh | |
| #6 | **Tano actúa (5)**: poses, caminar, reacciones; primer **escenario** reutilizable (7) | |
| #7 | **Subtítulos palabra por palabra (9)** + retención (R1–R4) | |
| #8 | Evaluar **Remotion (8)** con todo lo anterior | |

### Retención (se suma en cualquier Short)
| # | Técnica | Estado |
|---|---|---|
| R1 | **Loop:** la última frase empalma con la primera, así el Short se vuelve a ver | pendiente |
| R2 | **Pregunta abierta temprana** ("y lo más raro viene al final") que se cierra en el clímax | pendiente |
| R3 | **Interrupción de patrón** cada 3–5 s: cambio de fondo, zoom brusco, scratch, freeze-frame | pendiente |
| R4 | Miniatura y primer cuadro iguales (la imagen del hook es la portada) | pendiente |
| R5 | **Logo real de la marca** en el hook o en "me infiltré en…" (reconocimiento instantáneo) | desde #4 |

## Mejoras, en orden sugerido
| # | Mejora | Esfuerzo | Estado |
|---|---|---|---|
| 1 | **Look cinematográfico:** paleta por Short, glow en elementos clave, viñeta, grano sutil, sombras suaves (CSS filters / capas) | Bajo | **hecho · Short #3** (paleta ketchup/mostaza, `.glow`, `#vig`, `#grain`, `.soft`) |
| 2 | **Cámara:** zoom lento continuo por escena, paneos, desenfoque de fondo (DOF) al destacar un objeto | Bajo | parcial · Short #3 (zoom lento `.cam` por escena; falta paneo y DOF) |
| 3 | **Transiciones:** glitch/RGB-split, whip-pan con desenfoque de movimiento, match-cut | Bajo | pendiente |
| 4 | **Tano en partes (rig):** cabeza, ojos (parpadeo), cejas, boca (abre/cierra con la voz), brazos, piernas, cola | Alto, una vez | pendiente |
| 5 | **Tano actúa:** poses (señalar, sorpresa, pensar, celebrar), caminar, globos de pensamiento | Medio | pendiente |
| 6 | **Boca sincronizada con la voz** (amplitud del audio → apertura de boca) | Medio | pendiente |
| 7 | **Biblioteca de escenarios** vectoriales reutilizables (tienda, oficina, tribunal, fábrica, calle) | Alto, incremental | pendiente |
| 8 | **Migrar a Remotion** (React): springs con física, motion blur, mejor composición. Evaluar cuando 1–6 estén hechas | Alto | evaluar |
| 9 | **Subtítulos palabra por palabra** con resaltado (marcas de Whisper) | Medio | pendiente |
| 10 | Versión en inglés automática desde el mismo `video.html` (textos en `data-en`, voz Kokoro) | Medio | **hecho · Short #3** |
