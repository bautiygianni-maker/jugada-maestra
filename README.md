# Jugada Maestra

Fábrica de Shorts del canal **Jugada Maestra**: las jugadas geniales detrás de las marcas, contadas por Tano, el mapache infiltrado.

Un guion aprobado (`guion.json`) + una animación (`video.html`) → un comando → MP4 vertical 1080×1920 con voz, efectos, música y control de calidad.

## Instalación (una vez por computadora)
1. Instalar **Python 3.12** (python.org; en Windows marcar "Add Python to PATH").
2. Instalar **ffmpeg**: Windows `winget install Gyan.FFmpeg` · Mac `brew install ffmpeg`.
3. En la carpeta del repo:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows   (Mac/Linux: source .venv/bin/activate)
   python setup/instalar.py      # dependencias + modelo de voz (~3 GB)
   ```

## Producir un Short
```
python pipeline/producir.py shorts/02_birkin
```
Resultado: `shorts/02_birkin/02_birkin_ES.mp4` y `qc_fotogramas.jpg`.

## Documentación
- `CLAUDE.md`: instrucciones para Claude Code.
- `docs/WORKFLOW_Short.md`: el procedimiento completo.
- `docs/APRENDIZAJES.md`: reglas que salen de cada corrección.
- `docs/ROADMAP_calidad.md`: mejoras visuales, una por Short.
- `assets/CREDITOS.md`: licencias y créditos obligatorios en la descripción.
