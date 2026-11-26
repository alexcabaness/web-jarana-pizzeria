# La Jarana te llama · nueva web

Prototipo de la nueva web de la pizzería La Jarana.

- **Hero:** una pizza barbacoa que explota al hacer scroll. Son 145 fotogramas dibujados en un canvas fijo.
  - `h/` es el set HD (812×1116).
  - `f/` es el set ligero, que se usa con ahorro de datos o con 2G/3G.
- **Carta:** pizzas, porciones, entrantes, salsas, bebidas y postres, más el Club Jarana y el botón de pedir. Los datos salen de la carta actual de jaranatellama.es.

## Ver en local

```
python3 -m http.server 8000
```

Después abre http://localhost:8000.

## Estructura

- `index.html`: la página, sin dependencias. El CSS y el JS van dentro.
- `assets/`: tipografía Sardin, logo, fotos y el monigote (llama) en SVG.
- `tools/frames.py` y `tools/frameshd.py`: regeneran los fotogramas a partir del vídeo.
- `tools/carta/`: datos de la carta (`data.py`) y la plantilla con la que se generó la sección.
- `tools/capturas.js`: capturas de prueba en móvil y escritorio con Playwright.

## Pendiente

- Sustituir el vídeo por la versión limpia sin marca de agua.
- Fotos de producto en buena resolución.
