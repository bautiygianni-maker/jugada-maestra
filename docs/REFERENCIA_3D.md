# Referencia de estilo 3D (desde el Short #4)

Canal de referencia del usuario: TikTok @emptymind63. Video analizado: "Elon Musk va perdiendo la carrera de la IA,
pero su plan es otro" (302 s, vertical, ~938 mil vistas, ~93 mil me gusta, 13/11/2026).
**Se adoptan técnicas, no su estética exacta ni sus personajes.** Nuestra identidad: Tano en 3D y la paleta del canal.

## Qué hace (y por qué engancha)
| Técnica | Cómo lo hace | Lo adoptamos así |
|---|---|---|
| Mundo 3D low-poly | Autopista y ciudad neón de noche, oficina, tribunal, fábrica, la Tierra, la Luna | `assets/mundo3d.js`: `grilla`, `autopista`, `ciudad`, `tienda`; se suman escenarios Short a Short |
| Personaje sobre pedestal | Persona de bloques sobre un disco con anillo de luz | `M3D.pedestal()` + `M3D.tano()` (Tano low-poly con antifaz, cola con anillos y credencial) |
| Paneles holográficos | "PLAN MAESTRO", contador dorado "$1.000.000.000.000", tabla de posiciones, flotando en 3D | `M3D.panel({dibujar})`: canvas que se redibuja por cuadro (contadores) |
| Cámara siempre en movimiento | Vuelos sobre la autopista, órbitas, grúas; un corte cada ~5 s (59 cortes en 302 s) | `M3D.camara([[t,pos,mira,fov],...])` con suavizado; un plano por escena |
| Subtítulos palabra por palabra | Arriba, blancos, la palabra clave con recuadro de color | `.sub` con `data-sub="t:palabra|t:*clave"` (roadmap #9) |
| Rótulo chico abajo | Píldora oscura con dato o fecha ("OpenAI, 2015", "vas perdiendo") | `.pill` |
| Gente que llena la escena | Multitudes de bloques caminando, entrando a edificios | `M3D.persona()` con `.caminar(t)` |
| Narración en segunda persona | "Imagina que eres Elon Musk…" | Propuesta para el guion: "Imagina que eres el dueño de…" (decide el chat del guion) |
| Glow sin postproceso | Neón saturado, halos | Sin tone mapping (si no, el neón se lava a blanco) + `M3D.halo()` aditivo |

## Técnica
- Three.js r158 (`assets/vendor/three.min.js`, MIT; la última versión con build UMD, que funciona con `file://`).
- WebGL por software (SwiftShader) en Chromium headless: `config.lanzar_chrome` ya pasa las banderas.
- Velocidad medida: ~0,85 s por cuadro con sombras y niebla → un Short de 45 s tarda ~19 min por idioma.
  Mejora pendiente: renderizar la capa 3D una sola vez y solo las capas de texto por idioma.
- Determinista: todo depende de `setTime(t)`; `M3D.render(escena, tiempoLocal)`; semilla fija para ciudad y gente.
- Prueba: `shorts/_prueba3d/video.html` (3 planos, 9,5 s).

## Errores ya encontrados
- Con `ACESFilmicToneMapping` el amarillo neón sale crema/blanco: usar `NoToneMapping` y emisivos ≤ 1.
- El panel holográfico no puede quedar en la franja de subtítulos (y 250–450): bajarlo o apuntar la cámara más alto.
- Arriba va un degradé oscuro (`.topfade`) para que los subtítulos se lean sobre cualquier fondo.
