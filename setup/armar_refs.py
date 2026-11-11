"""Arma una referencia de ~13 s por hablante y mide tono y expresividad."""
import io, sys
import numpy as np, soundfile as sf, librosa, pyarrow.parquet as pq

t = pq.read_table(sys.argv[1]).to_pandas()
filas = []
for spk, g in t.groupby("speaker_id"):
    if len(g) < 10:
        continue
    partes, dur = [], 0.0
    # clips con más texto primero: suelen tener frases más naturales
    for _, r in g.assign(n=g.text.str.len()).sort_values("n", ascending=False).iterrows():
        y, sr = sf.read(io.BytesIO(r.audio["bytes"]))
        if y.ndim > 1:
            y = y.mean(1)
        y = librosa.resample(y, orig_sr=sr, target_sr=24000)
        y, _ = librosa.effects.trim(y, top_db=35)
        partes += [y, np.zeros(int(0.25 * 24000))]
        dur += len(y) / 24000
        if dur >= 13:
            break
    ref = np.concatenate(partes)
    ref = ref / (np.abs(ref).max() + 1e-9) * 0.9
    f0, _, _ = librosa.pyin(librosa.resample(ref, orig_sr=24000, target_sr=16000), fmin=60, fmax=300, sr=16000)
    f0 = f0[~np.isnan(f0)]
    semis = 12 * np.log2(f0 / np.median(f0))
    sf.write(f"ref_{spk}.wav", ref, 24000)
    filas.append((spk, np.median(f0), semis.std(), len(ref) / 24000))
    print(f"{spk}: F0 {np.median(f0):5.0f} Hz  expresividad {semis.std():4.2f}  {len(ref)/24000:4.1f}s", flush=True)
