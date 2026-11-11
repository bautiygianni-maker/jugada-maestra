"""Genera las líneas del guion (guion.json, clave "es") con la voz de Tano (Chatterbox Multilingual).
Se corre dentro de la carpeta del Short. Escribe linea{N}_s{SEMILLA}.wav.

Uso:
  python voz_lineas.py                 # todas las líneas, semillas 42 y 7
  python voz_lineas.py 2,7 11,23       # solo líneas 2 y 7, con semillas 11 y 23
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

LINEAS = json.load(open("guion.json", encoding="utf-8"))["es"]
SOLO = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else None
SEMILLAS = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [42, 7]
EXAGERACION, CFG = 0.7, 0.4  # valores aprobados para Tano (ver docs/APRENDIZAJES.md)

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
