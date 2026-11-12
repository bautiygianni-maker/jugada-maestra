"""Ancla los momentos clave de la animación a las palabras de la voz.
Lee claves.json: [[escena (1..7), tiempo local nominal, palabra], ...]
Busca cada palabra con Whisper (marcas por palabra) dentro de su escena y guarda en timeline.json,
para cada escena, una lista de anclas [tiempo nominal, tiempo real] (locales). La animación
interpola entre anclas, así cada golpe visual cae ADELANTO segundos antes de su palabra."""
import json, os, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import librosa
from faster_whisper import WhisperModel

ADELANTO = 0.10
TL = json.load(open(config.arch("timeline.json")))
CLAVES = json.load(open(config.arch("claves.json"), encoding="utf-8"))
ORIG = TL["orig"]


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if unicodedata.category(c) != "Mn" and (c.isalnum()))


y, _ = librosa.load(config.VOZ_PISTA, sr=16000)
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(y, language=config.IDIOMA, word_timestamps=True)
words = [(norm(w.word), w.start) for s in segs for w in s.words]

anclas = []
for i, ((os_, oe), (ns, ne, _)) in enumerate(zip(ORIG, TL["escenas"])):
    dn, da = oe - os_, ne - ns
    pts = [(0.0, 0.0)]
    usadas = set()
    for esc, lt, palabra in sorted((c for c in CLAVES if c[0] == i + 1), key=lambda c: c[1]):
        p = norm(palabra)
        cand = [(t, k) for k, (w, t) in enumerate(words) if p and p in w and ns - 0.1 <= t <= ne and k not in usadas]
        if not cand:
            print(f"  escena {esc}: no encontré «{palabra}», queda proporcional")
            continue
        t, k = cand[0]
        usadas.add(k)
        a = max(0.0, t - ns - ADELANTO)
        # solo anclas que avanzan en los dos ejes y dejan margen al final
        if lt > pts[-1][0] + 0.05 and a > pts[-1][1] + 0.05 and lt < dn - 0.1 and a < da - 0.1:
            pts.append((round(lt, 3), round(a, 3)))
            print(f"  escena {esc}: «{palabra}» nominal {lt:.2f}s -> real {a:.2f}s")
    pts.append((dn, da))
    anclas.append(pts)

TL["anclas"] = anclas
json.dump(TL, open(config.arch("timeline.json"), "w"), indent=1)
print("timeline.json con anclas")
