# Aprendizajes y reglas vigentes

Se lee antes de cada Short y se actualiza después de cada corrección del usuario.
Formato: regla concreta · por qué · origen.

## Estructura narrativa (obligatoria desde el Short #2)
- **Causalidad de South Park:** cada escena se conecta con la anterior con "pero" o "entonces" (o "por eso"), nunca con "y después". Si dos escenas se unen con "y", una sobra o hay que reescribirla. · Pedido del usuario. · Short #2
- **Arco completo en cada Short:** Hook (0–3 s, la paradoja) → Conflicto (por qué parece absurdo o qué está en juego) → Clímax (la revelación o el número más fuerte) → Payoff (la jugada explicada en una frase memorable) → pregunta final. · Pedido del usuario. · Short #2
- Antes de producir, escribir el guion como cadena de beats "PERO / ENTONCES" y verificar que no haya ningún "y después". · Short #2

## Hook (obligatorio desde el Short #3)
- **El hook abre una brecha de curiosidad:** muestra algo que el espectador cree entender y le agrega una contradicción que no puede resolver solo ("casi no gana nada con esto... y es su mejor arma"). Tiene que dar ganas de saber el porqué, no dar el dato completo. · Pedido del usuario. · Short #3
- **Se entiende en los primeros 3 segundos:** frase de 8 a 12 palabras, sin números largos ni contexto previo, y la imagen dice lo mismo que la voz desde el primer cuadro. Los datos (años, precios) van después, en el conflicto. · Pedido del usuario. · Short #3

## Ritmo visual y sonoro (obligatorio desde el Short #2)
- **Cambio visual cada 1 a 2 segundos** como máximo (entra un elemento, cambia el plano, zoom, corte, número que cambia). Ningún encuadre estático más de 2 s. · Pedido del usuario. · Short #2
- **Un efecto de sonido por cada evento visual** (aparición, golpe de texto, número, corte). Si algo se mueve en pantalla, suena. · Pedido del usuario. · Short #2
- **Música sin copyright, muy baja, por debajo de todo**, generada por código o con licencia libre verificada. · Pedido del usuario. · Short #2
- **Ningún silencio de voz mayor a 1–2 s**, incluido el final. · Pedido del usuario (refuerza Short #1 v1). · Short #2

## Sincronización y sonido (desde el Short #2)
- Cada elemento animado declara su efecto con `data-sfx` (y `data-at` si lo dibuja el código); `render.py` exporta `cues.json` y `sonido.py` arma `sfx.wav`. Así "si algo se mueve, suena" se cumple solo. · Short #2
- Los golpes visuales se anclan a la palabra exacta con `sincronizar.py` + `claves.json` (0,1 s antes de la palabra). Sin anclas, el escalado proporcional dejaba golpes hasta 1,4 s antes. · Short #2
- Efectos: biblioteca CC0 de OpenGameArt (377 sonidos, `sfx_lib`, catálogo por tipo). Golpes graves, whoosh y riser, sintéticos. · Short #2
- Música: Kevin MacLeod (incompetech.com, CC BY 4.0), volumen 0,10 con sidechain suave. **Crédito obligatorio en la descripción.** Temas "virales" de Shorts solo se pueden agregar desde la app de YouTube al subir. · Short #2
- Nombres de marca: Whisper puede oír "el mes" por "Hermès". Si una toma falla solo en la marca, generar 2 semillas más (`voz_lineas.py 2,7 11,23`) antes de aceptarla. · Short #2

## Animación (errores técnicos)
- Una animación de salida (`hide`) debe usar `forwards`, nunca `both`: con `both` el elemento queda visible antes de su entrada. · Encontrado en el Short #2 (también afectaba la plantilla de Ferrari). · Short #2
- Revisar siempre capturas de prueba (`preview.py`) antes del render completo. · Short #2

## Dos idiomas (obligatorio desde el 12/11/2026)
- **Cada Short sale en español neutro Y en inglés.** Mismo `video.html`, mismo ritmo; cambian voz y textos. · Pedido del usuario. · Short #2
- Inglés: voz Kokoro `am_michael` a velocidad 1.1 (aprobada en el Short #1). `python pipeline/producir.py shorts/NN --idioma en`. · Short #2
- Textos de pantalla: diccionario `TR.en` en `video.html` (la clave es el texto en español tal cual). Al renderizar en inglés, `trSinUsar` debe quedar vacío. · Short #2
- Pronunciación de marcas: el guion se escribe bien ("Hermès") y `guion.json -> pronunciacion_en` le da a la voz la versión fonética ("Air-mez"). Kokoro decía "HERMZ". Probar cada marca nueva antes de producir. · Short #2
- `guion.json` lleva `numeros_en` y cada Short lleva `claves_en.json` (palabras en inglés para anclar golpes). Si Whisper escribe distinto un nombre ("Birken"), anclar con un fragmento ("Birk"). · Short #2

## Guion e idioma
- Español neutro: nada de voseo ni argentinismos ("tú pides", "dinero", "me infiltré", "te la entregan"). · El público es toda LATAM. · Short #1
- **Vocabulario neutro, nunca regional:** "perro caliente" (no pancho/jocho/completo), "refresco" (no gaseosa/soda), "autos", "dinero". Ante la duda, la palabra que se entiende en toda Latinoamérica. · Pedido del usuario. · Short #3
- Números de la voz escritos en letras ("dos mil veinticinco"). · Chatterbox los lee mejor. · Short #1
- No inventar frases de personas reales; las "reglas" atribuidas deben estar documentadas. · Política de YouTube y credibilidad. · Short #1

## Voz
- Voz de Tano en español: hablante colombiano 8784 (OpenSLR 72), `exaggeration=0.7`, `cfg_weight=0.4`. · El usuario dijo que "combina con el mapache". · Short #1
- Rechazadas: Kokoro em_alex, Piper (todas), voz de fábrica de Chatterbox ("algo de gringo"), Aldo mexicano ("medio medio"). · No volver a proponerlas. · Short #1
- **Nunca acelerar ni estirar la voz** con time-stretch. · Suena "bajo el agua". · Short #1 v1
- Las escenas se adaptan a la voz, no la voz a las escenas. · Evita silencios largos. · Short #1 v1
- Pausas internas de la voz recortadas a 0,35 s como máximo; cierre de 1,2 s. · "Silencios largos en el medio y al final". · Short #1 v1
- Control con Whisper obligatorio: detectó "February" por "Ferrari" e "infistré". · Short #1

## Mezcla
- Música a 0,28 (no 0,55) y sidechain suave (ratio 3, release 400 ms). · La música tapaba la voz y "bombeaba". · Short #1 v1

## Video
- 30 fps, 1080×1920, crf 18. Inter Black para textos. · Short #1
