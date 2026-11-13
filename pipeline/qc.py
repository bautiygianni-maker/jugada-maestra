"""Control de calidad automático de un Short terminado (etapa 6 del workflow).
Se corre dentro de la carpeta del Short.  Uso: python qc.py VIDEO.mp4
Revisa: duración, volumen, pausas de la voz, transcripción contra el guion y arma una hoja de fotogramas.
Sale con código 1 si algo no pasa."""
import json, re, subprocess, sys, unicodedata
import numpy as np, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
L = config.IDIOMA

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
                 ff(["-i", config.VOZ_PISTA, "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", "-"]), re.S)
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
txt = " ".join(s.text for s in WhisperModel("small", device="cpu", compute_type="int8").transcribe(y, language=L)[0])
num = config.numeros(G)


def norm(t, invertir=False):
    t = config.despronunciar(G, t)
    if invertir:  # el guion tiene números en letras; Whisper los escribe en cifras
        for k, v in sorted(num.items(), key=lambda kv: -len(kv[1])):
            t = t.replace(v, k)
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", t.replace(".", "")).split()


# grafías de Whisper para marcas (ej. "Cosco" por "Costco"); solo si las líneas sueltas ya transcriben bien la marca
alias = G.get("alias_asr" if L == "es" else f"alias_asr_{L}", G.get("alias_asr", {}) if L == "es" else {})
ref, hyp = norm(" ".join(G[L]), True), [alias.get(w, w) for w in norm(txt)]
# Errores por tramos (difflib). Un tramo distinto NO cuenta si es la misma secuencia de letras con otra
# separación de palabras ("ningún apuro" / "ninguna puro", "no saca" / "nos saca"): eso no se oye en la voz.
import difflib, re as _re
def _junta(ws):
    return _re.sub(r"(.)\1+", r"\1", "".join(ws))
errores, juntas = 0, []
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ref, hyp, autojunk=False).get_opcodes():
    if op == "equal":
        continue
    if ref[i1:i2] and hyp[j1:j2] and _junta(ref[i1:i2]) == _junta(hyp[j1:j2]):
        juntas.append(f"{' '.join(ref[i1:i2])} ~ {' '.join(hyp[j1:j2])}")
        continue
    errores += max(i2 - i1, j2 - j1)
if juntas:
    print("separaciones distintas (no cuentan):", "; ".join(juntas))
wer = errores / len(ref)
print(f"error de palabras: {wer:.3f}\ntranscripción: {txt.strip()}")
if wer > 0.05:
    fallas.append(f"error de palabras {wer:.1%} (máx 5%)")

A_QC = config.arch("qc_fotogramas.jpg")
# 5. hoja de 16 fotogramas para revisión visual
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO, "-vf",
                f"fps=16/{dur:.2f},scale=240:-1,tile=8x2", "-frames:v", "1", A_QC], check=True)
print(f"hoja de fotogramas: {A_QC} (revisarla a ojo)")

print("\nRESULTADO:", "OK" if not fallas else "FALLA")
for f in fallas:
    print(" -", f)
sys.exit(1 if fallas else 0)
