# Reescalado de los fotogramas (Real-ESRGAN)

Los fotogramas de `x/`, `h/` y `f/` salen del vídeo de Kling (812×1116). Antes de reducirlos a cada tamaño, se reescalan ×4 con **Real-ESRGAN** (`realesr-general-x4v3`). Así salen más nítidos y con menos artefactos de compresión.

El modelo se ejecuta con onnxruntime en CPU, sin PyTorch, y tarda unos 14 s por fotograma con 4 núcleos.

1. Descarga `realesr-general-x4v3.pth` de las *releases* de Real-ESRGAN.
2. Convierte el modelo: `python3 onnx_desde_pth.py` (genera `sr.onnx`).
3. Extrae los fotogramas del vídeo en `raw/`: `ffmpeg -i video.mp4 raw/f_%03d.png`.
4. Genera los tres sets: `python3 fotogramas.py`.

| Set | Tamaño | Cuándo se usa |
|---|---|---|
| `x/` | 1218×1674 | Pantallas grandes o retina |
| `h/` | 812×1116 | Por defecto |
| `f/` | 720×990 | Con ahorro de datos o en 2G/3G |
