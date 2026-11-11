import numpy as np, wave, json

SR = 44100
ORIG = [(0, 3.5), (3.5, 9), (9, 16), (16, 22), (22, 28.5), (28.5, 35), (35, 41.5)]
TL = json.load(open("timeline.json"))
NEW = [(a, b) for a, b, _ in TL["escenas"]]
DUR = TL["total"]

def remap(t):
    """Lleva un instante de la línea de tiempo original a la nueva, escena por escena."""
    for (os_, oe), (ns, ne) in zip(ORIG, NEW):
        if t < oe:
            return ns + (t - os_) * (ne - ns) / (oe - os_)
    return NEW[-1][1]
N = int(SR * DUR)
out = np.zeros(N)
rng = np.random.default_rng(7)

def add_raw(sig, t, gain=1.0):
    i = int(t * SR)
    j = min(N, i + len(sig))
    if i < N:
        out[i:j] += sig[: j - i] * gain

def add(sig, t, gain=1.0):
    add_raw(sig, remap(t), gain)

def env(n, attack=0.005, decay=0.2):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)

def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.12)

def hat():
    n = int(0.05 * SR); x = rng.standard_normal(n)
    x = x - lowpass(x, 6)
    return x * env(n, 0.001, 0.015)

def clap():
    n = int(0.18 * SR); x = rng.standard_normal(n)
    x = lowpass(x, 3) - lowpass(x, 40)
    return x * env(n, 0.002, 0.05)

def whoosh(length=0.45):
    n = int(length * SR); x = rng.standard_normal(n)
    t = np.arange(n) / n
    y = np.zeros(n); seg = 2048
    for s in range(0, n, seg):
        k = int(60 - 54 * t[s])  # se abre el filtro: sube el brillo
        y[s:s + seg] = lowpass(x[s:s + seg + 200], max(k, 2))[: len(y[s:s + seg])]
    return y * np.sin(np.pi * t) ** 2 * 1.6

def boom(big=1.0):
    n = int(1.2 * SR); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t * 9)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45)
    c = rng.standard_normal(n) * np.exp(-t / 0.02) * 0.6
    return (s + lowpass(c, 4)) * big

def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2200 * t) * np.exp(-t / 0.006)

def ding(f0=1320):
    n = int(0.9 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 2.01 * t)) * np.exp(-t / 0.25) * 0.5

def pop():
    n = int(0.08 * SR); t = np.arange(n) / SR
    f = 300 + 900 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03)

def rev():
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = 55 + 160 * (t / 0.7) ** 0.8
    ph = np.cumsum(f) / SR
    saw = 2 * (ph % 1) - 1
    return lowpass(saw, 8) * np.clip(t / 0.05, 0, 1) * np.exp(-np.clip(t - 0.6, 0, None) / 0.1) * 0.7

def screech():
    n = int(0.4 * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); x = x - lowpass(x, 3)
    return (x * 0.3 + np.sin(2 * np.pi * 3100 * t) * 0.2) * np.sin(np.pi * t / t[-1])

def riser(length):
    n = int(length * SR); t = np.arange(n) / SR
    f = 300 + 900 * (t / length) ** 2
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / length) * 0.25

# Ritmo de fondo: 120 bpm, más bajo en la escena sepia
beat = 0.5
t = 0.0
k = 0
while t < DUR - 0.4:
    g = 0.35 if NEW[4][0] <= t < NEW[4][1] else 1.0
    add_raw(kick(), t, 0.55 * g)
    if k % 2 == 1:
        add_raw(clap(), t, 0.35 * g)
    add_raw(hat(), t + beat / 2, 0.25 * g)
    add_raw(hat(), t, 0.12 * g)
    t += beat; k += 1

# Efectos
add(rev(), 0.0, 0.9)
add(screech(), 0.45, 0.5)
add(boom(0.9), 0.72)
add(boom(1.1), 1.85)
for ns, _ in NEW[1:]:
    add_raw(whoosh(), ns - 0.32, 0.8)
add(pop(), 3.55, 0.9)
add(boom(0.6), 3.62)
for i in range(30):
    add(tick(), 9.8 + i * 0.06, 0.35)
add(boom(0.9), 11.85)
add(riser(1.4), 12.6)
add(ding(1568), 14.05)
for i in range(14):
    p = i / 13
    add(tick(), 16.5 + 2.6 * (p ** 0.7), 0.4)
add(boom(1.1), 19.47)
add(boom(1.3), 23.37)
for i in range(12):
    add(pop(), 28.58 + i * 0.07, 0.5)
add(boom(0.6), 29.75)
add(whoosh(0.6), 30.6, 0.6)
add(ding(1046), 31.1)
add(boom(0.7), 31.85)
add(boom(1.3), 36.75)
add(pop(), 35.4, 0.8)
add(ding(1318), 38.45)

# Mezcla final
out = np.tanh(out * 1.1) * 0.85
fade = int(0.05 * SR)
out[-fade:] *= np.linspace(1, 0, fade)
pcm = (np.stack([out, out], axis=1) * 32767).astype(np.int16)
with wave.open("audio.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", out.max())
