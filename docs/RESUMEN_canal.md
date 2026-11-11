# Jugada Maestra: resumen del canal y estado del trabajo

Última actualización: 9 de noviembre de 2026 (noche).

## 1. El canal
- **Nombre:** Jugada Maestra (descartado "Detrás de la Marca" porque ya existe "Detrás de la Etiqueta").
- **Nicho:** "Negocios y marcas explicadas". Shorts que cuentan por qué una empresa hace algo raro o cómo resolvió un problema con una jugada ingeniosa. Más adelante, videos largos de "Historias de productos y empresas" en el mismo canal.
- **Mercado:** dos versiones del mismo contenido.
  - Español neutro latinoamericano, para toda LATAM. **Sin voseo ni argentinismos**: usar "tú/pides", "dinero" (no "plata"), "autos", "me infiltré" (no "me metí"), "te la entregan" (no "te la dan").
  - Inglés.
- **Objetivo:** que el canal sea viral y que gane dinero, con producción automatizada y control de calidad humano.

## 2. Lo que aprendimos investigando
- **Referentes en inglés:** Company Man (el más parecido a nuestra idea), ColdFusion, MagnatesMedia, Modern MBA y Logically Answered.
- **En español** hay demanda y poca competencia seria. Gigantes del Éxito hizo 6,1M de vistas con solo 10 videos y después abandonó.
- **La plata está en los videos largos.** El RPM de Shorts en español ronda US$0,04 por cada mil vistas. Los largos de negocios tienen un CPM de US$10 a 25, y se suman patrocinios.
- **Qué hace viral a un video:** marcas que todos conocen, una sola decisión por video, el final al principio, contraste en el título, tensión (no solo admiración) y números grandes.
- **Riesgo de YouTube:** la política de "contenido no auténtico" desmonetiza el contenido de IA hecho en masa con plantillas.
  - **Cómo evitarlo:** personaje propio, voz con personalidad, títulos y miniaturas variados, y dirección humana.
  - No inventar frases de personas reales ni imitar logos de forma engañosa.

## 3. Estrategia de contenido
- **Ritmo semanal:**
  - 1 video largo (9 a 12 minutos) los lunes.
  - 3 recortes del largo los martes, jueves y sábados, reeditados más rápido y vinculados con la función "video relacionado".
  - Shorts originales el resto de los días, para probar temas. El que mejor funcione se convierte en el próximo video largo.
- **Reglas de cada Short:** tiene que funcionar solo, sin depender del video largo. Gancho en el segundo 1, cambio visual cada 1 o 2 segundos, subtítulos grandes, mucho diseño de sonido y una pregunta al final para generar comentarios.
- **Próximos temas:**
  1. Hermès y la Birkin
  2. El pancho de Costco
  3. El recorrido de IKEA
  4. McDonald's como inmobiliaria
  5. Rolex sin stock
  6. Netflix
  7. Apple y el cargador
  8. Red Bull y los deportes extremos
  9. Mercado Libre contra eBay

  **Verificar los datos antes de guionar cada uno.**

## 4. Personaje: Tano, el mapache infiltrado
- **Diseño:** mapache gris (#8E949C) con antifaz oscuro (#2B2E33), cara clara (#E9E6DF), contorno negro grueso (#14161A), ceja derecha levantada, credencial blanca colgando de un cordón rojo (#E8483B) que dice "VISITA" o "VISITOR", y cola con anillos. Señala hacia arriba.
- **Personalidad:** pícaro, curioso y siempre sabe algo. "Se mete adentro de las empresas" y cada Short es una misión ("Misión #001 · Ferrari").
- **Voz en español:** ver sección 7 (voz colombiana 8784, más aguda y enérgica; "combina con el mapache").
- **Paleta del canal:** amarillo #F5B82E, negro #14161A, rojo #E8483B, verde #3DDC84 y crema #F4F1EA. Tipografía: Inter, en peso Black o Extrabold.
- El SVG de Tano está dentro de `claude/plantilla_short_es.html`.

## 5. Lo que ya está hecho
- **Logo** de 800×800 (la cara de Tano sobre amarillo con rayos) y **banner** de 2560×1440 ("JUGADA MAESTRA" + Tano + "Las jugadas geniales detrás de las marcas que usás"). Fuente: `claude/branding.html`.
- **Short #1: Ferrari** (41,5 segundos, vertical 1080×1920, 30 fps), en 7 escenas:

  | Escena | Tiempo | Contenido |
  |---|---|---|
  | 1 | 0–3,5 s | Gancho |
  | 2 | 3,5–9 s | Tano entra |
  | 3 | 9–16 s | Contador de 13.752 a 13.640 y ganancias que suben |
  | 4 | 16–22 s | Calendario y "AGOTADO HASTA 2027" |
  | 5 | 22–28,5 s | La regla de Enzo: "−1" |
  | 6 | 28,5–35 s | Si sobran / si faltan |
  | 7 | 35–41,5 s | "VENDE ESPERA" y pregunta final |

  - **Datos verificados:** Ferrari entregó 13.640 autos en 2025, 112 menos que en 2024, y ganó más. Tiene pedidos hasta fines de 2027. La regla de Enzo es "vender siempre un auto menos de lo que pide el mercado".
  - **Versión en inglés:** terminada y aprobada. Voz Kokoro `am_michael`.
  - **Versión en español neutro: TERMINADA** (9/11/2026). Archivo `Ferrari_ES_neutro.mp4`, −14,6 LUFS. Pendiente que el usuario la apruebe.
  - **Crédito obligatorio en la descripción del video en español:** "Voz basada en el corpus de español colombiano de Google (OpenSLR 72, CC BY-SA 4.0)".

## 6. Guion de voz en español neutro (aprobado)
1. ¡Ferrari podría vender el doble de autos... y no quiere!
2. Así que me infiltré en Ferrari, para descubrir por qué.
3. En dos mil veinticinco vendió ciento doce autos menos... y aun así, ganó más dinero.
4. Si hoy pides una Ferrari... está agotada hasta dos mil veintisiete. Te llega en dos mil veintiocho.
5. ¿Por qué? Por una regla de Enzo Ferrari: vender siempre un auto menos de lo que pide el mercado.
6. Si sobran Ferraris, valen menos. Si faltan... la gente espera años, y paga lo que sea.
7. Ferrari no vende autos. Vende espera. ¿Tú esperarías dos años?

Cada línea empieza en el inicio de su escena, 0,08 segundos después del corte.

## 7. Voz en español: RESUELTA
- **Motor:** Chatterbox Multilingual de Resemble AI (licencia MIT), `ChatterboxMultilingualTTS.from_local(carpeta, device="cpu")`, `language_id="es"`, `exaggeration=0.7`, `cfg_weight=0.4`. Tarda unos 40 s por frase en CPU de 2 núcleos.
- **Archivos del modelo** (de `ResembleAI/chatterbox` en Hugging Face): `t3_mtl23ls_v2.safetensors`, `s3gen.pt`, `ve.pt`, `conds.pt`, `grapheme_mtl_merged_expanded_v1.json`, `Cangjie5_TC.json`.
- **Red:** la sesión necesita permitidos `huggingface.co` y `*.hf.co` (los archivos grandes bajan de `us.aws.cdn.hf.co`).
- **Voz elegida:** hablante masculino **8784** del corpus de español colombiano de Google (OpenSLR 72, dataset HF `ylacombe/google-colombian-spanish`, carpeta `male/`, primer parquet). Licencia CC BY-SA 4.0: uso comercial permitido con atribución. Referencia de ~15 s armada con `claude/armar_refs.py` (concatena los clips más largos del hablante).
- **Lo que se probó y fue rechazado:**
  - Kokoro `em_alex`, mezcla Kokoro + `am_michael`, Piper `es_MX-claude-high` (femenina), Piper `es_MX-ald-medium` bajada 3 semitonos.
  - Voz de fábrica de Chatterbox (`conds.pt`): masculina pero "con algo de gringo".
  - Referencias de Aldo (dataset `rmcpantoja/Ald_Mexican_Spanish_speech_dataset`, Unlicense): "medio medio".
  - Otras voces colombianas probadas: 8421, 3349, 2484 (medias), 7049, 3034 (graves).
- **Control de calidad automático:** `claude/armar_voz.py` genera 2 tomas por línea, las transcribe con faster-whisper `small`, mide el error contra el guion, elige la mejor, la acelera con time-stretch si no entra en su escena y arma `voz_es.wav`. Detecta errores reales (p. ej. "February" en vez de "Ferrari", "infistré").

## 8. Cómo se produce el video (técnico)
- **Animación:** una página HTML de 1080×1920 con escenas en CSS y una función `setTime(t)` que congela las animaciones en el instante t.
- **Captura:** Playwright y Chrome (`/usr/bin/google-chrome`) sacan capturas JPEG con calidad 92, que pasan a ffmpeg con libx264, crf 18, preset veryfast y yuv420p. Un archivo por escena, unidos con concat y `-c copy` en `video_mudo.mp4`. Script: `claude/render.py`.
- **Música y efectos:** generados por código con numpy (`claude/audio.py`), sin derechos de terceros. 120 bpm, whooshes en cada corte, golpes, ticks y dings sincronizados con la imagen.
- **Voz en español:** `claude/voz_lineas.py` (genera las tomas) + `claude/armar_voz.py` (elige y arma la pista).
- **Voz en inglés:** Kokoro v1.0 en ONNX (`claude/tts.py` y `claude/build_voice.py`).
- **Mezcla final con ffmpeg:**
  - Voz: highpass 90 Hz, ecualización +3 dB en 3 kHz, compresor (−18 dB, 3:1), volumen 1,6.
  - Música: volumen 0,55 y sidechaincompress con la voz.
  - Final: amix sin normalizar + loudnorm I=−14, TP=−1,5. AAC 192k, `-movflags +faststart`.
- **Dependencias:** `pip install chatterbox-tts faster-whisper pyarrow pandas playwright` (torch sale de PyPI; download.pytorch.org está bloqueado).
- Al leer los scripts, hay que actualizar las rutas de carpetas.

## 9. Próximos pasos
1. Que el usuario apruebe `Ferrari_ES_neutro.mp4`.
2. Convertir la plantilla en un sistema reutilizable para los temas de la sección 3 (guion + escenas en datos, un solo comando para ES y EN).
3. Guionar y producir los Shorts 2 a 10, en español y en inglés.
4. Después, automatizar el proceso con n8n y agentes, manteniendo el control de calidad humano.
