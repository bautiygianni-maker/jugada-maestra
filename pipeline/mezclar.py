"""Mezcla final: video_mudo.mp4 + voz_es.wav + sfx.wav + musica.wav -> MP4 listo para subir.
Se corre dentro de la carpeta del Short.  Uso: python mezclar.py SALIDA.mp4
Valores aprobados (ver docs/APRENDIZAJES.md): voz al frente, efectos 0.45, música 0.10 con sidechain suave,
volumen final -14 LUFS."""
import json, os, subprocess, sys

SALIDA = sys.argv[1] if len(sys.argv) > 1 else "final.mp4"
VOZ = os.environ.get("VOZ", "voz_es.wav")
MUSICA_VOL = os.environ.get("MUSICA_VOL", "0.10")
SFX_VOL = os.environ.get("SFX_VOL", "0.45")
T = json.load(open("timeline.json"))["total"]

VOZF = ("aresample=44100,aformat=channel_layouts=stereo,highpass=f=80,"
        "equalizer=f=3000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120,volume=1.8")
filtro = (
    f"[1:a]{VOZF},asplit=2[voz][sc];"
    f"[3:a]volume={MUSICA_VOL}[m0];[m0][sc]sidechaincompress=threshold=0.08:ratio=3:attack=20:release=400[mus];"
    f"[2:a]volume={SFX_VOL}[sfx];"
    "[voz][sfx][mus]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "video_mudo.mp4", "-i", VOZ, "-i", "sfx.wav",
                "-i", "musica.wav", "-filter_complex", filtro, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", str(T), "-movflags", "+faststart", SALIDA],
               check=True)
print(f"{SALIDA} listo ({T} s)")
