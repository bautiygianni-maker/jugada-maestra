# Workflow de producción: un Short de Jugada Maestra

Procedimiento fijo. Se sigue en orden, siempre. Antes de empezar se lee `docs/APRENDIZAJES.md`
y al terminar se actualiza con lo que el usuario corrigió.

## Quién hace qué
| Parte | Dónde | Entrega |
|---|---|---|
| Idea, investigación, guion, títulos, descripción | **Claude (chat) en el proyecto "Workflow Canales automatizados"** | `guion.json` + `claves.json` aprobados por el usuario |
| Animación, voz, sonido, mezcla, control de calidad | **Claude Code en este repositorio** | `NN_tema_ES.mp4` y `NN_tema_EN.mp4` que pasan `qc.py` |

## Etapa 1: Investigación y datos (chat · punto de control humano)
1. Buscar el tema en la web. **Cada dato con su fuente**, preferir fuentes primarias. Verificar que los datos "de hoy" sigan siendo ciertos (ej.: Hermès vs. LVMH ya no era cierto en 2026).
2. Ficha: la jugada en una frase, 3 a 5 datos verificados con fuente, la tensión ("parece absurdo porque…").
3. **El usuario aprueba la ficha.**

## Etapa 2: Guion (chat · punto de control humano)
1. 7 beats, 30 a 45 s: Hook → (entonces) Tano se infiltra → (pero) conflicto → (por eso) escalada → (porque) razón → (entonces) clímax → (por eso) payoff. Ningún "y después" entre escenas (causalidad de South Park).
2. Español neutro (sin voseo) e inglés. Números de la voz en letras. "..." para pausas dramáticas.
3. Payoff simple y memorable; el cierre puede ser una frase fuerte y la pregunta va solo en pantalla.
4. **El usuario aprueba el guion.**
5. Se arma `guion.json` (`es`, `en`, `numeros`, `numeros_en`), `claves.json` y `en_claves.json` (palabras donde caen los golpes visuales en cada idioma).

## Etapa 3: Producción (Claude Code)
1. `mkdir shorts/NN_tema` con `guion.json` y `claves.json`.
2. Escribir `video.html` partiendo del último Short (hoy `shorts/03_costco/video.html`, que ya trae viñeta, grano, glow y cámara): 7 `<section class="scene" data-start data-end>`, cada elemento animado con `data-sfx`, Tano desde `assets/tano.js`.
3. **Capturas de prueba antes del render:** `python ../../pipeline/preview.py video.html 0.5,1.5,... prev.jpg` y mirarlas.
4. Traducir cada texto de pantalla en `data-en` y mirar capturas en inglés (`preview.py video.html 0.5,... prev.jpg en`).
5. `python pipeline/producir.py shorts/NN_tema` (voz → armado → sincronía → render → sonido → mezcla → qc, en ES y en EN).
6. Si alguna línea tiene error de voz en todas las tomas: `python ../../pipeline/voz_lineas.py N 11,23` y repetir desde `armar_voz`.

## Etapa 4: Control de calidad (automático, antes de mostrar nada)
`qc.py` exige: duración 25–60 s · −14 ± 1 LUFS · ninguna pausa de voz > 0,8 s (final ≤ 1,5 s) · error de palabras ≤ 5 % en el video final · y deja `qc_fotogramas.jpg` para revisar a ojo (texto legible, nada cortado ni encimado, datos en pantalla = datos de la ficha).

## Etapa 5: Entrega y feedback (punto de control humano)
1. Mandar el MP4 + 5 títulos + descripción con fuentes y créditos (`assets/CREDITOS.md`).
2. Cada corrección del usuario se anota en `docs/APRENDIZAJES.md` (regla · por qué · Short de origen).
3. Si la corrección vale para todos los Shorts, se cambia el código o la plantilla, no solo el video.
4. Elegir **una mejora de `docs/ROADMAP_calidad.md`** para el próximo Short: cada video tiene que verse mejor que el anterior.

## Regla de oro
Un error que el usuario ya marcó una vez no puede volver a aparecer. Si aparece, se corrige el workflow.
