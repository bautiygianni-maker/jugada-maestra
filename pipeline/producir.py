"""Produce un Short completo con un solo comando (pensado también para n8n).

Uso:
  python pipeline/producir.py shorts/02_birkin                 # todo
  python pipeline/producir.py shorts/02_birkin --desde render  # retoma desde un paso
  python pipeline/producir.py shorts/02_birkin --solo qc

La carpeta del Short necesita: guion.json, video.html y (opcional) claves.json.
Pasos: voz -> armar_voz -> sincronizar -> render -> sonido -> mezclar -> qc
El paso "voz" se saltea si ya existen todas las tomas (linea*_s*.wav).
"""
import argparse, glob, json, os, subprocess, sys, time
from pathlib import Path

PIPE = Path(__file__).resolve().parent
PASOS = ["voz", "armar_voz", "sincronizar", "render", "sonido", "mezclar", "qc"]

ap = argparse.ArgumentParser()
ap.add_argument("carpeta")
ap.add_argument("--desde", choices=PASOS)
ap.add_argument("--solo", choices=PASOS)
ap.add_argument("--musica", help="ruta a un .mp3 (por defecto, el de config.py)")
ap.add_argument("--salida", help="nombre del MP4 final (por defecto <carpeta>_ES.mp4 / _EN.mp4)")
ap.add_argument("--idioma", default="es", choices=["es", "en"], help="es (Chatterbox) o en (Kokoro)")
a = ap.parse_args()

os.environ["JM_IDIOMA"] = a.idioma
sys.path.insert(0, str(PIPE))
import config  # noqa: E402  (lee JM_IDIOMA)
os.chdir(a.carpeta)
nombre = a.salida or f"{Path(a.carpeta).name}_{a.idioma.upper()}.mp4"
G = json.load(open("guion.json", encoding="utf-8"))
py = sys.executable


def correr(*args):
    print(f"\n=== {' '.join(str(x) for x in args)}", flush=True)
    subprocess.run([py, *map(str, args)], check=True)


def paso(n):
    if n == "voz":
        faltan = [i for i in range(1, len(G[a.idioma]) + 1) if not glob.glob(f"{config.PRE}linea{i}_s*.wav")]
        if faltan:
            correr(PIPE / "voz_lineas.py", ",".join(map(str, faltan)))
        else:
            print("\n=== voz: ya están todas las tomas")
    elif n == "armar_voz":
        correr(PIPE / "armar_voz.py")
    elif n == "sincronizar":
        if Path(config.arch("claves.json")).exists():
            correr(PIPE / "sincronizar.py")
        else:
            print(f"\n=== sincronizar: no hay {config.arch('claves.json')}, queda proporcional")
    elif n == "render":
        for f in glob.glob(f"{config.PRE}scene*.mp4"):
            os.remove(f)
        correr(PIPE / "render.py", "video.html")
    elif n == "sonido":
        correr(PIPE / "sonido.py", *( [a.musica] if a.musica else []))
    elif n == "mezclar":
        correr(PIPE / "mezclar.py", nombre)
    elif n == "qc":
        correr(PIPE / "qc.py", nombre)


lista = [a.solo] if a.solo else PASOS[PASOS.index(a.desde):] if a.desde else PASOS
t0 = time.time()
for n in lista:
    paso(n)
print(f"\nListo en {(time.time()-t0)/60:.1f} min -> {Path(a.carpeta, nombre)}")
