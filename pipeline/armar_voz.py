"""Elige la mejor toma de cada línea con Whisper, acorta pausas internas largas
y arma la pista de voz. Las escenas se adaptan a la voz (no al revés): sin aceleración.
Escribe voz_<idioma>.wav y timeline.json (en inglés: en_timeline.json) (inicio y fin nuevos de cada escena)."""
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import config

import json, re, unicodedata
import numpy as np, soundfile as sf, librosa
from faster_whisper import WhisperModel

SR = 24000
import re as _re
# escenas nominales: se leen de video.html (data-start / data-end de cada <section class="scene">)
ORIG = [(float(a), float(b)) for a, b in _re.findall(r'class="scene"[^>]*data-start="([\d.]+)" data-end="([\d.]+)"', open("video.html", encoding="utf-8").read())]
assert ORIG, "no encontré escenas en video.html"
G = json.load(open("guion.json", encoding="utf-8"))
LINEAS = G[config.IDIOMA]
SEMILLAS = [42, 7]
INICIO = 0.08        # la voz entra 0,08 s después del corte
COLA = 0.35          # aire después de la frase antes del próximo corte
COLA_FINAL = 1.2     # deja leer la pregunta final
PAUSA_MAX = 0.35     # pausas internas más largas se recortan a esto
MIN_ESCENA = 3.0
NUM = config.numeros(G)


def norm(t):
    for k, v in sorted(NUM.items(), key=lambda kv: -len(kv[0])):
        t = re.sub(rf"\b{k}\b", v, t)
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zñ ]", " ", t).split()


def wer(ref, hyp):
    d = np.arange(len(hyp) + 1)
    for i, r in enumerate(ref, 1):
        prev, d[0] = d.copy(), i
        for j, h in enumerate(hyp, 1):
            d[j] = min(prev[j] + 1, d[j - 1] + 1, prev[j - 1] + (r != h))
    return d[-1] / len(ref)


def acortar_pausas(y):
    """Recorta silencios internos a PAUSA_MAX con fundido corto para no generar clics."""
    tramos = librosa.effects.split(y, top_db=38, frame_length=1024, hop_length=256)
    fade = int(0.01 * SR)
    partes = []
    for k, (a, b) in enumerate(tramos):
        seg = y[a:b].copy()
        seg[:fade] *= np.linspace(0, 1, min(fade, len(seg)))
        seg[-fade:] *= np.linspace(1, 0, min(fade, len(seg)))
        partes.append(seg)
        if k < len(tramos) - 1:
            hueco = (tramos[k + 1][0] - b) / SR
            partes.append(np.zeros(int(min(hueco, PAUSA_MAX) * SR), dtype=y.dtype))
    return np.concatenate(partes)


asr = WhisperModel("small", device="cpu", compute_type="int8")
elegidas = []
for n, linea in enumerate(LINEAS, 1):
    cands = []
    import glob
    for f in sorted(glob.glob(config.arch(f"linea{n}_s*.wav"))):
        sem = int(f.split("_s")[1][:-4])
        y, _ = librosa.load(f, sr=SR)
        y = acortar_pausas(y)
        segs, _ = asr.transcribe(librosa.resample(y, orig_sr=SR, target_sr=16000), language=config.IDIOMA, beam_size=5)
        txt = " ".join(sg.text for sg in segs).strip()
        err = wer(norm(linea), norm(txt))
        cands.append((err, len(y) / SR, sem, y, txt))
        print(f"línea {n} s{sem}: error {err:.2f}  {len(y)/SR:.2f}s  «{txt}»", flush=True)
    err, dur, sem, y, txt = min(cands, key=lambda c: (round(c[0], 2), c[1]))
    elegidas.append(y / (np.abs(y).max() + 1e-9) * 0.9)
    print(f"  -> elegida s{sem} ({dur:.2f}s)", flush=True)

timeline, t = [], 0.0
for n, y in enumerate(elegidas):
    cola = COLA_FINAL if n == len(elegidas) - 1 else COLA
    dur = max(MIN_ESCENA, round(INICIO + len(y) / SR + cola, 2))
    timeline.append([round(t, 2), round(t + dur, 2), ORIG[n][1] - ORIG[n][0]])
    t += dur
total = round(t, 2)

pista = np.zeros(int((total + 0.5) * SR), dtype=np.float32)
for (s, e, _), y in zip(timeline, elegidas):
    i = int((s + INICIO) * SR)
    pista[i:i + len(y)] += y
sf.write(config.VOZ_PISTA, pista[: int(total * SR)], SR)
json.dump({"total": total, "escenas": timeline, "orig": ORIG}, open(config.arch("timeline.json"), "w"), indent=1)
for k, (s, e, od) in enumerate(timeline, 1):
    print(f"escena {k}: {s:5.2f}–{e:5.2f}  ({e-s:.2f}s, antes {od:.2f}s)")
print("total", total)
