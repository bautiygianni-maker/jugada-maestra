"""Control de calidad automático de un Short terminado (etapa 6 del workflow).
Se corre dentro de la carpeta del Short.  Uso: python qc.py VIDEO.mp4
Revisa: duración, volumen, pausas de la voz, transcripción contra el guion y arma una hoja de fotogramas.
Sale con código 1 si algo no pasa."""
import json, re, subprocess, sys, unicodedata
import numpy as np

VIDEO = sys.argv[1]
G = json.load(open("guion.json", encoding="utf-8"))
fallas = []


def ff(args):
    return subprocess.run(["ffmpeg", "-hide_banner", *args], capture_output=True, text=True).stderr


# 1. duración
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VIDEO],
                           capture_output=True, text=True).stdout)
print(f"duración: {dur:.1f} s")
if not 25 <= dur <= 60:
    fallas.append(f"duración {dur:.1f}s fuera de 25-60 s")

# 2. volumen integrado
m = re.search(r"I:\s+(-?[\d.]+) LUFS", ff(["-i", VIDEO, "-af", "ebur128", "-f", "null", "-"]).split("Summary")[-1])
lufs = float(m.group(1))
print(f"volumen: {lufs} LUFS")
if abs(lufs + 14) > 1:
    fallas.append(f"volumen {lufs} LUFS (objetivo -14 ± 1)")

# 3. pausas de la voz (la del final puede ser más larga)
sil = re.findall(r"silence_start: ([\d.]+).*?silence_duration: ([\d.]+)",
                 ff(["-i", "voz_es.wav", "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", "-"]), re.S)
for ini, d in sil:
    ini, d = float(ini), float(d)
    final = ini + d >= dur - 0.2
    if (final and d > 1.5) or (not final and d > 0.8):
        fallas.append(f"pausa de voz de {d:.2f}s en {ini:.1f}s")
print(f"pausas de voz > 0,6 s: {[(round(float(a),1), round(float(b),2)) for a, b in sil]}")

# 4. transcripción del video final contra el guion
from faster_whisper import WhisperModel
import soundfile as sf
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO, "-ac", "1", "-ar", "16000", "_qc16k.wav"], check=True)
y, _ = sf.read("_qc16k.wav", dtype="float32")
txt = " ".join(s.text for s in WhisperModel("small", device="cpu", compute_type="int8").transcribe(y, language="es")[0])
num = G.get("numeros", {})


def norm(t, invertir=False):
    if invertir:  # el guion tiene números en letras; Whisper los escribe en cifras
        for k, v in sorted(num.items(), key=lambda kv: -len(kv[1])):
            t = t.replace(v, k)
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", t.replace(".", "")).split()


# grafías de Whisper para marcas (ej. "Cosco" por "Costco"); solo si las líneas sueltas ya transcriben bien la marca
alias = G.get("alias_asr", {})
ref, hyp = norm(" ".join(G["es"]), True), [alias.get(w, w) for w in norm(txt)]
d = np.arange(len(hyp) + 1)
for i, r in enumerate(ref, 1):
    p, d[0] = d.copy(), i
    for j, h in enumerate(hyp, 1):
        d[j] = min(p[j] + 1, d[j - 1] + 1, p[j - 1] + (r != h))
wer = d[-1] / len(ref)
print(f"error de palabras: {wer:.3f}\ntranscripción: {txt.strip()}")
if wer > 0.05:
    fallas.append(f"error de palabras {wer:.1%} (máx 5%)")

# 5. hoja de 16 fotogramas para revisión visual
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO, "-vf",
                f"fps=16/{dur:.2f},scale=240:-1,tile=8x2", "-frames:v", "1", "qc_fotogramas.jpg"], check=True)
print("hoja de fotogramas: qc_fotogramas.jpg (revisarla a ojo)")

print("\nRESULTADO:", "OK" if not fallas else "FALLA")
for f in fallas:
    print(" -", f)
sys.exit(1 if fallas else 0)
