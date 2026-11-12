"""Genera las líneas del guion con la voz de Tano. Se corre dentro de la carpeta del Short.
Español (JM_IDIOMA=es): Chatterbox Multilingual -> linea{N}_s{SEMILLA}.wav
Inglés (JM_IDIOMA=en): Kokoro am_michael -> en_linea{N}_s0.wav (Kokoro es determinista: una toma por línea)

Uso:
  python voz_lineas.py                 # todas las líneas, semillas 42 y 7
  python voz_lineas.py 2,7 11,23       # solo líneas 2 y 7, con semillas 11 y 23
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
LINEAS = json.load(open("guion.json", encoding="utf-8"))[config.IDIOMA]
SOLO = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else None
SEMILLAS = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [42, 7]
EXAGERACION, CFG = 0.7, 0.4  # valores aprobados para Tano (ver docs/APRENDIZAJES.md)

if config.IDIOMA == "en":
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(str(config.KOKORO_DIR / "onnx" / "model.onnx"), str(config.KOKORO_DIR / "voices.npz"))
    for i, txt in enumerate(LINEAS, 1):
        if SOLO and i not in SOLO:
            continue
        t0 = time.time()
        y, sr = k.create(txt, voice=config.KOKORO_VOZ, speed=1.0, lang="en-us")
        sf.write(config.arch(f"linea{i}_s0.wav"), y, sr)
        print(f"en linea {i}: {len(y)/sr:.2f}s ({time.time()-t0:.0f}s)", flush=True)
    sys.exit(0)

import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

dev = config.dispositivo()
if dev == "cpu":
    torch.set_num_threads(max(1, (os.cpu_count() or 2)))
m = ChatterboxMultilingualTTS.from_local(str(config.MODELO_DIR), device=dev)
m.prepare_conditionals(str(config.REF_VOZ), exaggeration=EXAGERACION)
print(f"modelo cargado en {dev}", flush=True)

for i, txt in enumerate(LINEAS, 1):
    if SOLO and i not in SOLO:
        continue
    for s in SEMILLAS:
        t0 = time.time()
        torch.manual_seed(s)
        wav = m.generate(txt, language_id="es", exaggeration=EXAGERACION, cfg_weight=CFG)
        torchaudio.save(f"linea{i}_s{s}.wav", wav.cpu(), m.sr)
        print(f"linea {i} semilla {s}: {wav.shape[-1]/m.sr:.2f}s ({time.time()-t0:.0f}s)", flush=True)
