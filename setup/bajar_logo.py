"""Baja el logo de una marca desde Wikimedia Commons a assets/marcas/<marca>.svg (o .png) y anota su
licencia en assets/marcas/marcas.json.  Necesita acceso a commons.wikimedia.org y upload.wikimedia.org.

Uso (desde la raíz):
  python setup/bajar_logo.py costco                         # busca "costco logo" y muestra opciones
  python setup/bajar_logo.py costco "File:Costco Wholesale logo 2010-10-26.svg"   # baja ese archivo

Regla del canal (docs/APRENDIZAJES.md): el logo real solo identifica a la marca de la que hablamos.
Se usa tal cual (sin deformarlo, recolorearlo ni animar sus partes), nunca como protagonista de la
miniatura y sin sugerir que la marca patrocina el video."""
import hashlib, json, re, sys, urllib.parse, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "assets" / "marcas"
UA = {"User-Agent": "JugadaMaestraBot/1.0 (produccion de video; uso editorial)"}
API = "https://commons.wikimedia.org/w/api.php?"


def api(**p):
    p.setdefault("format", "json")
    return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(p), headers=UA), timeout=60))


marca = sys.argv[1].lower()
if len(sys.argv) < 3:
    r = api(action="query", list="search", srsearch=f"{marca} logo filetype:drawing", srnamespace=6, srlimit=15)
    print("Opciones (elegir una y volver a correr con el nombre entre comillas):")
    for x in r["query"]["search"]:
        print("  ", x["title"])
    sys.exit(0)

archivo = sys.argv[2]
nombre = archivo.split(":", 1)[-1].replace(" ", "_")
pagina = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(nombre)
try:
    r = api(action="query", titles=archivo, prop="imageinfo", iiprop="url|extmetadata|mime")
    info = next(iter(r["query"]["pages"].values()))["imageinfo"][0]
    md = info["extmetadata"]
    url = info["url"]
    lic = re.sub("<[^>]+>", "", md.get("LicenseShortName", {}).get("value", "?"))
    autor = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "?")).strip()
except Exception as e:
    # la API suele limitar pedidos anónimos (429); el archivo se puede bajar igual por su ruta md5
    print(f"API de Commons no disponible ({e}); bajo el archivo directo. Revisar la licencia en {pagina}")
    h = hashlib.md5(nombre.encode()).hexdigest()
    url = f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{urllib.parse.quote(nombre)}"
    lic, autor = "verificar en la página de Commons", "?"
ext = ".svg" if nombre.lower().endswith(".svg") else ".png"
DEST.mkdir(parents=True, exist_ok=True)
datos = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
(DEST / f"{marca}{ext}").write_bytes(datos)

idx_f = DEST / "marcas.json"
idx = json.load(open(idx_f, encoding="utf-8")) if idx_f.exists() else {}
idx[marca] = {"archivo": f"{marca}{ext}", "fuente": pagina, "licencia": lic, "autor": autor,
              "nota": "Marca registrada de su dueño. Uso editorial para identificar a la empresa; sin modificarla."}
json.dump(idx, open(idx_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{DEST / (marca + ext)}  ({len(datos)//1024} KB) · licencia: {lic}")
