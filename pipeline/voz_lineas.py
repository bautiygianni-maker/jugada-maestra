"""Genera las líneas del guion con la voz de Tano.
  Español (JM_IDIOMA=es, por defecto): Chatterbox Multilingual + referencia 8784. Varias tomas (semillas).
  Inglés  (JM_IDIOMA=en): Kokoro v1.0, voz am_michael (aprobada en el Short #1). Una toma (es determinista).
Se corre dentro de la carpeta del Short. Escribe {PRE}linea{N}_s{SEMILLA}.wav.

Uso:
  python voz_lineas.py                 # todas las líneas
  python voz_lineas.py 2,7 11,23       # solo líneas 2 y 7, con semillas 11 y 23 (solo español)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

G = json.load(open("guion.json", encoding="utf-8"))
LINEAS = G[config.IDIOMA]
# Pronunciación: el texto del guion queda como se escribe ("Hermès") y la voz recibe la versión fonética
# ("Air-mez"). Se define por idioma en guion.json -> "pronunciacion_en": {"Hermès": "Air-mez"}
PRON = G.get(f"pronunciacion_{config.IDIOMA}", {})


def para_voz(t):
    for k, v in PRON.items():
        t = t.replace(k, v)
    return t
SOLO = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else None
SEMILLAS = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [42, 7]
EXAGERACION, CFG = 0.7, 0.4  # valores aprobados para Tano en español (ver docs/APRENDIZAJES.md)


def elegidas():
    return [(i, t) for i, t in enumerate(LINEAS, 1) if not SOLO or i in SOLO]


if config.IDIOMA == "en":
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(str(config.KOKORO_DIR / "kokoro-v1.0.onnx"), str(config.KOKORO_DIR / "voices-v1.0.bin"))
    for i, txt in elegidas():
        t0 = time.time()
        wav, sr = k.create(para_voz(txt), voice=config.KOKORO_VOZ, speed=config.KOKORO_VEL, lang="en-us")
        sf.write(f"{config.PRE}linea{i}_s0.wav", wav, sr)
        print(f"linea {i}: {len(wav)/sr:.2f}s ({time.time()-t0:.0f}s)", flush=True)
    sys.exit(0)

import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

dev = config.dispositivo()
if dev == "cpu":
    torch.set_num_threads(max(1, (os.cpu_count() or 2)))
m = ChatterboxMultilingualTTS.from_local(str(config.MODELO_DIR), device=dev)
m.prepare_conditionals(str(config.REF_VOZ), exaggeration=EXAGERACION)
print(f"modelo cargado en {dev}", flush=True)
for i, txt in elegidas():
    for s in SEMILLAS:
        t0 = time.time()
        torch.manual_seed(s)
        wav = m.generate(para_voz(txt), language_id=config.IDIOMA, exaggeration=EXAGERACION, cfg_weight=CFG)
        torchaudio.save(f"{config.PRE}linea{i}_s{s}.wav", wav.cpu(), m.sr)
        print(f"linea {i} semilla {s}: {wav.shape[-1]/m.sr:.2f}s ({time.time()-t0:.0f}s)", flush=True)
