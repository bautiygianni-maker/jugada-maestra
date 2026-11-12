"""Instalación en una máquina nueva (Windows, Mac o Linux). Correr desde la raíz del repo:
    python setup/instalar.py
Hace: (1) torch con CUDA si hay NVIDIA, (2) dependencias, (3) Chromium de Playwright,
(4) baja el modelo Chatterbox (~3 GB) a modelos/chatterbox, (5) verifica ffmpeg."""
import shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PY = sys.executable
ARCHIVOS = ["t3_mtl23ls_v2.safetensors", "s3gen.pt", "ve.pt", "conds.pt",
            "grapheme_mtl_merged_expanded_v1.json", "Cangjie5_TC.json"]


def pip(*args):
    subprocess.run([PY, "-m", "pip", "install", *args], check=True)


print("1/5 PyTorch")
tiene_nvidia = shutil.which("nvidia-smi") is not None
if tiene_nvidia:
    print("   placa NVIDIA detectada: instalo torch con CUDA")
    pip("torch==2.6.0", "torchaudio==2.6.0", "--index-url", "https://download.pytorch.org/whl/cu124")
else:
    print("   sin NVIDIA: torch normal (en Mac con chip Apple usa la GPU igual)")

print("2/5 Dependencias")
pip("-r", str(RAIZ / "requirements.txt"))

print("3/5 Chromium para capturar la animación")
subprocess.run([PY, "-m", "playwright", "install", "chromium"], check=True)

print("4/5 Modelo de voz Chatterbox")
from huggingface_hub import hf_hub_download
destino = RAIZ / "modelos" / "chatterbox"
destino.mkdir(parents=True, exist_ok=True)
for f in ARCHIVOS:
    if (destino / f).exists():
        print(f"   {f}: ya está")
        continue
    print(f"   bajando {f} ...")
    hf_hub_download("ResembleAI/chatterbox", f, local_dir=str(destino))

print("   modelo Kokoro (voz en inglés)")
import urllib.request
kdir = RAIZ / "modelos" / "kokoro"; kdir.mkdir(parents=True, exist_ok=True)
for f in ["kokoro-v1.0.onnx", "voices-v1.0.bin"]:
    if not (kdir / f).exists():
        print(f"   bajando {f} ...")
        urllib.request.urlretrieve(f"https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{f}", kdir / f)

print("5/5 ffmpeg")
if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    print("   ffmpeg OK")
else:
    print("   FALTA ffmpeg. Windows: `winget install Gyan.FFmpeg` · Mac: `brew install ffmpeg` · Linux: `apt install ffmpeg`")
    sys.exit(1)

import torch
dev = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"\nListo. La voz va a correr en: {dev}")
