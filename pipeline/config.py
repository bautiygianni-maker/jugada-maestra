"""Rutas y ajustes compartidos. Todo es relativo a la raíz del repositorio,
y cualquier ruta se puede pisar con una variable de entorno (útil en otra máquina o en n8n)."""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Modelo Chatterbox Multilingual (6 archivos, ~3 GB). Lo baja setup/instalar.py.
MODELO_DIR = Path(os.environ.get("JM_MODELO", RAIZ / "modelos" / "chatterbox"))
# Referencia de la voz de Tano en español (hablante 8784, OpenSLR 72, CC BY-SA 4.0)
REF_VOZ = Path(os.environ.get("JM_REF_VOZ", RAIZ / "assets" / "voz" / "ref_8784.wav"))
# Biblioteca de efectos CC0 (OpenGameArt) con catalogo.json
SFX_LIB = Path(os.environ.get("JM_SFX", RAIZ / "assets" / "sfx"))
# Música (Kevin MacLeod, CC BY 4.0: requiere crédito en la descripción)
MUSICA_DIR = Path(os.environ.get("JM_MUSICA", RAIZ / "assets" / "musica"))
MUSICA_DEFECTO = MUSICA_DIR / "Sneaky_Snitch.mp3"

# Chrome/Chromium para capturar la animación. Vacío = el Chromium de Playwright.
CHROME = os.environ.get("JM_CHROME") or None

# Dispositivo para la voz: "cuda" si hay placa NVIDIA, "mps" en Mac con chip Apple, si no "cpu".
def dispositivo():
    if os.environ.get("JM_DEVICE"):
        return os.environ["JM_DEVICE"]
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


def lanzar_chrome(playwright):
    args = {"args": ["--no-sandbox"]}
    if CHROME:
        args["executable_path"] = CHROME
    return playwright.chromium.launch(**args)


# ---------- idioma ----------
# producir.py pone JM_IDIOMA=es o en para cada versión. Los archivos intermedios en inglés llevan prefijo "en_"
# (en_linea1_s0.wav, en_timeline.json, en_claves.json...); los del español quedan con el nombre de siempre.
IDIOMA = os.environ.get("JM_IDIOMA", "es")
IDIOMAS = ("es", "en")


def arch(nombre):
    return nombre if IDIOMA == "es" else f"{IDIOMA}_{nombre}"


VOZ_PISTA = f"voz_{IDIOMA}.wav"


def numeros(G):
    """mapa cifra -> palabras del guion para el idioma actual (clave "numeros" o "numeros_en")"""
    return G.get("numeros" if IDIOMA == "es" else f"numeros_{IDIOMA}", {})


# Voz en inglés: Kokoro v1.0 (ONNX, Apache 2.0), voz am_michael (aprobada en el Short #1). La baja setup/instalar.py.
KOKORO_DIR = Path(os.environ.get("JM_KOKORO", RAIZ / "modelos" / "kokoro"))
KOKORO_VOZ = os.environ.get("JM_KOKORO_VOZ", "am_michael")
