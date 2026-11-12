"""Baja la biblioteca de efectos del canal desde Mixkit y arma assets/sfx/catalogo.json.

Licencia: "Mixkit Sound Effects Free License" -> uso comercial (YouTube incluido), sin atribución obligatoria.
Necesita acceso a mixkit.co y assets.mixkit.co.  Uso (desde la raíz):  python setup/bajar_sfx_mixkit.py

La lista está curada a mano (estilo de edición actual de Shorts explicativos: impactos de tráiler,
whooshes rápidos, risers, scratch de vinilo, ding de acierto, buzzer de concurso, monedas, boing...).
Para sumar efectos: buscar en https://mixkit.co/free-sound-effects/<categoria>/, agregar (id, "título")
al tipo que corresponda y volver a correr. Los tipos sin efectos de Mixkit usan los viejos de OpenGameArt."""
import json, subprocess, time, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SFX = RAIZ / "assets" / "sfx"
UA = {"User-Agent": "Mozilla/5.0"}
MAX_SEG = 6.0  # se recorta lo que dure más (colas largas no sirven en un Short)

CURADOS = {
    # transiciones y movimiento
    "whoosh":  [(1492, "Cinematic whoosh fast transition"), (1490, "Fast whoosh transition"), (1489, "Air woosh"),
                (3115, "Fast transitions swoosh"), (1464, "Quick swoosh accent"), (166, "Fast small sweep transition"),
                (174, "Fast sweep transition"), (168, "Fast air sweep transition"), (175, "Short transition sweep"),
                (1461, "Short wind swoosh"), (3161, "Transition flying swoosh"), (2637, "Fast air transition sweep")],
    "riser":   [(790, "Cinematic trailer riser"), (645, "Cinematic synth riser"), (632, "Cinematic drama riser"),
                (786, "Cinematic suspense swell"), (678, "Trailer cinematic suspense swell"), (2283, "Cinematic mysterious riser brass")],
    # golpes
    "slam":    [(772, "Quick zoom impact"), (2902, "Movie impact intro presentation"), (2180, "Exciting fast hit"),
                (2655, "Fast impact blow"), (2909, "Cool impact movie trailer"), (2919, "Movie trailer whoosh hit"),
                (2903, "Movie whoosh impact presentation"), (2150, "Impact of a blow")],
    "hit":     [(2299, "Short bass hit"), (2151, "Soft quick punch"), (2167, "Short slap or clap"),
                (2161, "Air in a hit"), (2149, "Cartoon punch"), (2072, "Small hit in a game")],
    "boom":    [(1143, "Cinematic whoosh deep impact"), (2901, "Epic movie impact"), (563, "Drum deep impact"),
                (553, "Blockbuster trailer bass drum"), (2294, "Drum bass hit"), (2303, "Futuristic bass hit"),
                (1286, "Cinematic impact thunder"), (2916, "Movie impact transition"), (549, "Deep cinematic subtle drum impact")],
    "gong":    [(2918, "Epic movie trailer whoosh impact"), (2900, "Movie logo intro impact"), (2907, "Epic blockbuster movie transition"),
                (2908, "Movie trailer epic impact")],
    # interfaz y texto
    "pop":     [(2358, "Long pop"), (2364, "Hard pop click"), (2357, "Bubble pop up alert notification"),
                (2356, "Dry pop up notification alert"), (2359, "Silly pop cluster"), (3005, "Explainer video pops whoosh light pop"),
                (2887, "Arcade video game pop"), (3069, "Game balloon or bubble pop")],
    "click":   [(1109, "Select click"), (2568, "Cool interface click tone"), (1117, "Classic click"),
                (1120, "Modern click box check"), (2577, "Interface device click"), (2997, "Clear mouse clicks")],
    "tick":    [(1061, "Clock ticker single"), (1053, "Ticking counter"), (1054, "Electric ticking counter"), (1063, "Fast wall clock ticking")],
    "typing":  [(1397, "Electronic typing"), (1396, "Soft typing on a digital keyboard"), (1386, "Keyboard typing")],
    "camera":  [(1430, "Camera shutter hard click"), (1432, "Camera digital shutter"), (1440, "Classic camera click"), (1438, "Vintage camera shutter")],
    "glitch":  [(2950, "Intro text glitch"), (2951, "Digital glitch break"), (2946, "Virtual quick glitch"),
                (1031, "Glitch short"), (1457, "Glitch static"), (2595, "Small electric glitch"), (1021, "Cinematic glitch trailer")],
    # reacciones
    "ding":    [(2870, "Correct answer tone"), (952, "Correct answer reward"), (933, "Bell notification"), (937, "Happy bells notification"),
                (600, "Achievement bell"), (601, "Happy bell alert"), (586, "Attention bell ding"), (2867, "Confirmation tone")],
    "reveal":  [(961, "Musical reveal"), (235, "Explainer video game reveal"), (960, "Tile game reveal")],
    "fanfare": [(2068, "Achievement completed"), (2059, "Game level completed"), (555, "Achievement win drums"), (2067, "Casino bling achievement")],
    "error":   [(950, "Game show wrong answer buzz"), (954, "Wrong long buzzer"), (3219, "Wrong answer game show"),
                (946, "Wrong answer fail notification"), (2876, "Funny fail low tone"), (2964, "System beep buzzer fail")],
    "fail":    [(472, "Slow sad trombone fail"), (744, "Trombone disappoint"), (471, "Sad game over trombone")],
    "scratch": [(702, "Record player vinyl scratch"), (704, "Vinyl stop fast scratch"), (703, "Vinyl forward and back fast scratch"),
                (708, "DJ record swipe"), (710, "Vinyl record small scratch"), (707, "Vinyl record swipe")],
    "boing":   [(2894, "Boing hit sound"), (2895, "Metallic boing hit")],
    "drumroll": [(566, "Drum Roll"), (577, "Tension and suspense drum roll")],
    "badum":   [(579, "Drum joke accent"), (578, "Joke drums")],
    "heartbeat": [(498, "Deep heartbeat impact"), (490, "Human single heart beat")],
    "laugh":   [(424, "Crowd laugh"), (422, "Small crowd laugh and applause")],
    # objetos
    "coin":    [(1993, "Clinking coins"), (1999, "Gold coin prize"), (1939, "Coins handling"), (2003, "Coins sound"),
                (1936, "Magical coin win"), (1992, "Coin win notification"), (2069, "Winning a coin, video game"), (3187, "Bag of coins touch")],
    "cash":    [(1989, "Money bag drop"), (2067, "Casino bling achievement"), (2841, "Atm cash machine key press")],
    "paper":   [(1530, "Paper slide"), (2380, "Paper quick movement"), (1104, "Page turn single"), (2384, "Paper quick slice")],
    "wood":    [(2182, "Wood hard hit"), (3141, "Small wood plank pile drop"), (562, "Hand tribal drum")],
    "glass":   [(2936, "Wine glass clink"), (2836, "Glasses clinking"), (3083, "Magic sparkle touch"), (3062, "Magic wand sparkle"), (871, "Fairy magic sparkle")],
    "sparkle": [(3083, "Magic sparkle touch"), (3062, "Magic wand sparkle"), (871, "Fairy magic sparkle"), (3060, "Sparkle hybrid transition")],
}


def get(url):
    for k in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(5 * (k + 1))
    raise RuntimeError("demasiados pedidos (429)")


def duracion(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    return float(r.stdout or 0)


indice, nuevo = {}, {}
for tipo, lista in CURADOS.items():
    nuevo[tipo] = []
    for i, titulo in lista:
        rel = f"mixkit/{i}.ogg"
        dest = SFX / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                wav = get(f"https://assets.mixkit.co/active_storage/sfx/{i}/{i}.wav")
            except Exception as e:
                print(f"  {i} {titulo}: no se pudo bajar ({e})")
                continue
            tmp = dest.with_suffix(".wav")
            tmp.write_bytes(wav)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-t", str(MAX_SEG),
                            "-af", f"afade=t=out:st={MAX_SEG-0.4}:d=0.4", "-c:a", "libvorbis", "-q:a", "6", str(dest)], check=True)
            tmp.unlink()
            time.sleep(0.5)
        d = round(duracion(dest), 2)
        nuevo[tipo].append([rel, d, i])
        indice[str(i)] = {"titulo": titulo, "tipo": tipo, "dur": d, "url": f"https://mixkit.co/free-sound-effects/?q={i}"}
    print(f"{tipo}: {len(nuevo[tipo])}")

# catálogo: Mixkit primero; los tipos que Mixkit no cubre siguen con OpenGameArt
viejo_f = SFX / "catalogo_opengameart.json"
if not viejo_f.exists():
    viejo_f.write_text((SFX / "catalogo.json").read_text(encoding="utf-8"), encoding="utf-8")
viejo = json.load(open(viejo_f, encoding="utf-8"))
final = {t: v for t, v in nuevo.items() if v}
for t, v in viejo.items():
    final.setdefault(t, v)
json.dump(final, open(SFX / "catalogo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(indice, open(SFX / "mixkit" / "indice.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("catalogo.json:", {k: len(v) for k, v in final.items()})
