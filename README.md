# La Jarana te llama · nueva web

**Web publicada:** https://alexcabaness.github.io/web-jarana-pizzeria/

Nueva web de la pizzería La Jarana te llama ([jaranatellama.es](https://jaranatellama.es), [@la_jarana_te_llama](https://www.instagram.com/la_jarana_te_llama/)). Se abre con una animación a pantalla completa: al hacer scroll, una pizza barbacoa explota. Debajo está la carta completa. Está pensada primero para móvil, pero también funciona bien en escritorio. Usa los colores de la marca (marrón oscuro, verde lima y blanco), la tipografía Sardin y el monigote de la llama.

## Qué incluye

- **Hero:** el monigote de la llama comiéndose una porción (grande a la izquierda en escritorio, pequeño en móvil). La explosión se hace con 145 fotogramas que se dibujan en un canvas fijo mientras haces scroll.
  - `h/` es el set HD (812×1116).
  - `f/` es el set ligero, que se usa con ahorro de datos o con 2G/3G.
- **Carta:**
  - pizzas, porciones, entrantes, salsas, bebidas y postres, con precios y alérgenos;
  - el botón de pedir.

  Los datos salen de la carta actual de jaranatellama.es.

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
