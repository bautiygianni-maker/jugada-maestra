
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import config
import subprocess, os, json
from pathlib import Path
from playwright.sync_api import sync_playwright

FPS = 30
import sys
HERE = os.getcwd()  # se corre dentro de la carpeta del Short
PAGINA = sys.argv[1] if len(sys.argv) > 1 else "video.html"
A = config.arch
TL = json.load(open(f"{HERE}/{A('timeline.json')}"))
SCENES = [(a, b) for a, b, _ in TL["escenas"]]

with sync_playwright() as p:
    b = config.lanzar_chrome(p)
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(Path(HERE, PAGINA).as_uri() + f"?lang={config.IDIOMA}")
    pg.wait_for_timeout(500)
    pg.evaluate(f"setTimeline({json.dumps(TL)})")
    if pg.evaluate("typeof cues") == "function":
        json.dump(pg.evaluate("cues()"), open(f"{HERE}/{A('cues.json')}", "w"), indent=0)
        print(A("cues.json"), "exportado", flush=True)
    names = []
    for idx, (s, e) in enumerate(SCENES, 1):
        tmp = f"{HERE}/{A(f'scene{idx}.tmp.mp4')}"
        final = f"{HERE}/{A(f'scene{idx}.mp4')}"
        names.append(final)
        if os.path.exists(final):
            print("escena", idx, "ya estaba", flush=True)
            continue
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
             "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
            stdin=subprocess.PIPE)
        for f in range(round(s * FPS), round(e * FPS)):
            pg.evaluate(f"setTime({f / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close()
        if ff.wait() == 0:
            os.replace(tmp, final)
            print("escena", idx, "lista", flush=True)
        else:
            raise SystemExit(f"falló la escena {idx}")
    b.close()

with open(f"{HERE}/{A('list.txt')}", "w") as f:
    for nm in names:
        f.write(f"file '{nm}'\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{HERE}/{A('list.txt')}",
                "-c", "copy", f"{HERE}/{A('video_mudo.mp4')}"], check=True)
print(A("video_mudo.mp4"), "listo", flush=True)
