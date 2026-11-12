"""Arma efectos y música a partir de cues.json (exportado por la animación).
Salida: sfx.wav (efectos) y musica.wav (música recortada con fundidos), 44,1 kHz estéreo.
Efectos: biblioteca de Mixkit (setup/bajar_sfx_mixkit.py) con respaldo CC0 de OpenGameArt y sintéticos.
Música: Kevin MacLeod (incompetech.com), CC BY 4.0 -> requiere crédito en la descripción."""
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import config

import json, sys, itertools
import numpy as np, librosa, soundfile as sf

SR = 44100
LIB = str(config.SFX_LIB)
MUSICA = sys.argv[1] if len(sys.argv) > 1 else str(config.MUSICA_DEFECTO)
MUSICA_DESDE = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

cues = json.load(open("cues.json"))
TOTAL = json.load(open("timeline.json"))["total"]
N = int(TOTAL * SR)
out = np.zeros(N)
rng = np.random.default_rng(3)
cat = {k: [f for f, d, c in v] for k, v in json.load(open(f"{LIB}/catalogo.json", encoding="utf-8")).items()}
rot = {k: itertools.cycle(v) for k, v in cat.items()}
cache = {}


def cargar(f):
    if f not in cache:
        y, _ = librosa.load(f"{LIB}/{f}", sr=SR, mono=True)
        y, _ = librosa.effects.trim(y, top_db=45)
        cache[f] = y / (np.abs(y).max() + 1e-9)
    return cache[f]


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def boom(big=1.0):
    n = int(1.0 * SR); t = np.arange(n) / SR
    f = 40 + 70 * np.exp(-t * 9)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35) * big


def whoosh(length=0.4):
    n = int(length * SR); x = rng.standard_normal(n); t = np.arange(n) / n
    y = np.zeros(n); seg = 2048
    for s in range(0, n, seg):
        k = max(int(50 - 44 * t[s]), 2)
        y[s:s + seg] = lowpass(x[s:s + seg + 200], k)[: len(y[s:s + seg])]
    return y * np.sin(np.pi * t) ** 2 * 1.4


def riser(length=1.2):
    n = int(length * SR); t = np.arange(n) / SR
    f = 250 + 900 * (t / length) ** 2
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / length) * 0.5


SINTETICOS = {"boom": boom, "whoosh": whoosh, "riser": riser}
GANANCIA = {"boom": 0.9, "whoosh": 0.7, "riser": 0.5, "pop": 0.6, "click": 0.5, "tick": 0.45,
            "slam": 0.8, "hit": 0.7, "ding": 0.55, "error": 0.6, "glitch": 0.5, "gong": 0.6,
            "paper": 0.6, "wood": 0.8, "glass": 0.5, "scratch": 0.5, "door": 0.6, "coin": 0.5,
            "reveal": 0.55, "fanfare": 0.55, "fail": 0.6, "boing": 0.6, "drumroll": 0.5, "badum": 0.6,
            "heartbeat": 0.7, "laugh": 0.5, "cash": 0.6, "sparkle": 0.45, "typing": 0.45, "camera": 0.6}


def add(sig, t, g):
    i = int(t * SR)
    if i >= N or i < -len(sig):
        return
    a, b = max(i, 0), min(N, i + len(sig))
    out[a:b] += sig[a - i:b - i] * g


def pico(y):
    """posición (en muestras) del pico de energía: ahí tiene que caer el corte o el golpe"""
    env = np.convolve(np.abs(y), np.ones(1024) / 1024, mode="same")
    return int(np.argmax(env))


LARGO_MAX = {"riser": 2.2, "whoosh": 1.2, "drumroll": 2.5}  # segundos antes del pico / largo total


for c in cues:
    tipo, t, g = c["sfx"], c["t"], c.get("gain", 1.0)
    for tp in tipo.split("+"):  # permite capas: "slam+boom"
        if tp in cat:  # biblioteca (Mixkit primero; ver setup/bajar_sfx_mixkit.py)
            y = cargar(next(rot[tp]))
            if tp in ("whoosh", "riser"):
                # el pico del whoosh/riser cae justo en el corte o en el golpe
                k = pico(y)
                ini = max(0, k - int(LARGO_MAX[tp] * SR))
                y = y[ini:k + int(0.25 * SR)].copy()
                n = min(len(y), int(0.15 * SR))
                y[:n] *= np.linspace(0, 1, n)
                add(y, t - (k - ini) / SR, GANANCIA.get(tp, 0.6) * g)
            else:
                lim = int(LARGO_MAX.get(tp, 2.5) * SR)
                if len(y) > lim:
                    y = y[:lim].copy()
                    y[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))
                add(y, t, GANANCIA.get(tp, 0.6) * g)
        elif tp in SINTETICOS:
            sig = SINTETICOS[tp]()
            # el whoosh tiene que terminar en el corte, no empezar
            if tp == "whoosh":
                t2 = t - len(sig) / SR * 0.8
            elif tp == "riser":
                t2 = t - len(sig) / SR
            else:
                t2 = t
            add(sig, t2, GANANCIA[tp] * g)
        else:
            print(f"aviso: no hay efectos de tipo «{tp}»")

out = np.tanh(out * 1.0) * 0.9
sf.write("sfx.wav", np.stack([out, out], 1), SR)

# Música: tramo desde MUSICA_DESDE, del largo del video, con fundidos
m, _ = librosa.load(MUSICA, sr=SR, mono=False, offset=MUSICA_DESDE, duration=TOTAL + 0.5)
if m.ndim == 1:
    m = np.stack([m, m])
m = m[:, :N]
if m.shape[1] < N:
    m = np.pad(m, ((0, 0), (0, N - m.shape[1])))
fi, fo = int(0.3 * SR), int(1.5 * SR)
m[:, :fi] *= np.linspace(0, 1, fi)
m[:, -fo:] *= np.linspace(1, 0, fo)
sf.write("musica.wav", m.T, SR)
print(f"sfx.wav ({len(cues)} efectos) y musica.wav listos, {TOTAL}s")
