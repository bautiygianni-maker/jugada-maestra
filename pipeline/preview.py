
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import config
import sys, json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
ts=[float(x) for x in sys.argv[2].split(',')]
with sync_playwright() as p:
    b=config.lanzar_chrome(p)
    pg=b.new_page(viewport={"width":1080,"height":1920})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    lang=sys.argv[4] if len(sys.argv)>4 else "es"
    pg.goto(Path(os.getcwd(), sys.argv[1]).as_uri()+f"?lang={lang}"); pg.wait_for_timeout(400)
    ims=[]
    for t in ts:
        pg.evaluate(f"setTime({t})"); pg.screenshot(path="_preview.png")
        ims.append(Image.open("_preview.png").convert("RGB").resize((270,480)))
    print("errores:",errs)
    print(json.dumps(pg.evaluate("cues()")[:5]))
    b.close()
cols=8; rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB",(270*cols,480*rows),"white")
for i,im in enumerate(ims): sheet.paste(im,((i%cols)*270,(i//cols)*480))
sheet.save(sys.argv[3])
