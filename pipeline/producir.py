"""Produce un Short completo con un solo comando (pensado también para n8n).

Uso:
  python pipeline/producir.py shorts/02_birkin                 # todo, en español y en inglés
  python pipeline/producir.py shorts/02_birkin --idioma en     # solo una versión
  python pipeline/producir.py shorts/02_birkin --desde render  # retoma desde un paso
  python pipeline/producir.py shorts/02_birkin --solo qc

La carpeta del Short necesita: guion.json (claves "es" y "en"), video.html (textos en inglés en data-en)
y (opcional) claves.json / en_claves.json. Salida: <carpeta>_ES.mp4 y <carpeta>_EN.mp4.
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
ap.add_argument("--idioma", choices=["es", "en", "todos"], default="todos")
ap.add_argument("--salida", help="nombre del MP4 final (solo con un idioma; por defecto <carpeta>_ES.mp4)")
a = ap.parse_args()

base = Path(a.carpeta).resolve().name
os.chdir(a.carpeta)
G = json.load(open("guion.json", encoding="utf-8"))
py = sys.executable
idiomas = ["es", "en"] if a.idioma == "todos" else [a.idioma]
IDIOMA = "es"


def arch(n):
    return n if IDIOMA == "es" else f"{IDIOMA}_{n}"


def correr(*args):
    print(f"\n=== [{IDIOMA}] {' '.join(str(x) for x in args)}", flush=True)
    subprocess.run([py, *map(str, args)], check=True, env={**os.environ, "JM_IDIOMA": IDIOMA})


def paso(n, nombre):
    if n == "voz":
        faltan = [i for i in range(1, len(G[IDIOMA]) + 1) if not glob.glob(arch(f"linea{i}_s*.wav"))]
        if faltan:
            correr(PIPE / "voz_lineas.py", ",".join(map(str, faltan)))
        else:
            print(f"\n=== [{IDIOMA}] voz: ya están todas las tomas")
    elif n == "armar_voz":
        correr(PIPE / "armar_voz.py")
    elif n == "sincronizar":
        if Path(arch("claves.json")).exists():
            correr(PIPE / "sincronizar.py")
        else:
            print(f"\n=== [{IDIOMA}] sincronizar: no hay {arch('claves.json')}, queda proporcional")
    elif n == "render":
        for f in glob.glob(arch("scene*.mp4")):  # "scene*" no incluye los "en_scene*"
            os.remove(f)
        correr(PIPE / "render.py", "video.html")
    elif n == "sonido":
        correr(PIPE / "sonido.py", *([a.musica] if a.musica else []))
    elif n == "mezclar":
        correr(PIPE / "mezclar.py", nombre)
    elif n == "qc":
        correr(PIPE / "qc.py", nombre)


lista = [a.solo] if a.solo else PASOS[PASOS.index(a.desde):] if a.desde else PASOS
t0 = time.time()
salidas = []
for IDIOMA in idiomas:
    if IDIOMA not in G:
        sys.exit(f"guion.json no tiene la clave \"{IDIOMA}\"")
    nombre = (a.salida if a.salida and len(idiomas) == 1 else f"{base}_{IDIOMA.upper()}.mp4")
    for n in lista:
        paso(n, nombre)
    salidas.append(nombre)
print(f"\nListo en {(time.time()-t0)/60:.1f} min -> {', '.join(str(Path(a.carpeta, s)) for s in salidas)}")
