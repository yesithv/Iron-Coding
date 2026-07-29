# Iron-Coding — sitio corporativo

Sitio estático (HTML/CSS/JS puro, sin paso de compilación) de **iron-coding.art**.
Se sirve tal cual desde el hosting compartido cPanel de GoDaddy.

## Estructura

```
web/                      ← esto es el sitio: lo que se sube a public_html
├── index.html            Portada
├── .htaccess             Compresión, caché y MIME para Apache/cPanel
├── .nojekyll             Evita que GitHub Pages procese el sitio con Jekyll
├── favicon.svg
├── css/
│   ├── base.css          Tokens de identidad, reset, nav y pie (todas las páginas)
│   └── home.css          Solo la portada
├── js/
│   └── main.js           Menú móvil y año del pie. Sin dependencias.
├── fonts/                JetBrains Mono y Manrope (variables, subconjunto latino)
├── img/
│   ├── apple-touch-icon.png
│   └── showcase/         Capturas optimizadas a WebP
└── pages/                Resto de páginas del sitio

fuentes/                  ← material de trabajo, NO se publica
├── capturas-originales/  PNG originales de cada app + enlace a su README
└── iteraciones-diseno/   Exploraciones de identidad visual
```

## Identidad visual

| Token | Valor | Uso |
|---|---|---|
| Fondo | `#0A0A0C` | Negro azulado, nunca negro puro |
| Superficie | `#131316` | Tarjetas y bloques |
| Rojo forja | `#C1272D` | **Solo relleno y bordes** (3.4:1 sobre el fondo) |
| Rojo glow | `#FF4D55` | Rojo para texto (6.1:1 sobre el fondo) |
| Violeta IA | `#8B5CF6` | Acentos (4.7:1) |
| Texto | `#F2F0EC` | Blanco cálido (17.4:1) |
| Texto atenuado | `#8A8A93` | Secundario (5.8:1) |
| Líneas | `#2A2A2F` | Bordes y separadores |

Tipografías: **JetBrains Mono** (marca, títulos, código) y **Manrope** (lectura).
Las dos se sirven desde `web/fonts/`, no desde un CDN.

Reglas del lenguaje visual "código": la marca siempre es la etiqueta
`<Iron-Coding/>`; los enlaces del nav van entre corchetes; los CTA son llamadas
a función; los encabezados de sección son comentarios `//`; los proyectos se
indexan como `proyectos[0]`…`proyectos[3]`. La animación de entrada ocurre **una
sola vez, en el hero**, y se desactiva con `prefers-reduced-motion`.

## Publicar en cPanel

1. Comprime **el contenido** de `web/` (no la carpeta `web` en sí).
2. cPanel → *Administrador de archivos* → `public_html` → *Cargar* el ZIP.
3. Extraer ahí mismo. `index.html` tiene que quedar directamente en `public_html`.
4. Comprueba que `.htaccess` se subió (activa "Mostrar archivos ocultos").

Todas las rutas son relativas, así que el sitio funciona igual en la raíz del
dominio, en un subdirectorio o en local.

## Vista previa local

```bash
cd web && python3 -m http.server 8899
# http://127.0.0.1:8899
```

## GitHub Pages

`.github/workflows/deploy-pages.yml` publica `web/` en cada push a `main`.
Sirve como entorno de revisión; el sitio de producción es el de cPanel.

## Preparar nuevas capturas

Los PNG originales viven en `fuentes/capturas-originales/`. Para el sitio se
convierten a WebP de 720 px de ancho (calidad 78), que es lo que reduce el peso
de ~3,4 MB a ~460 KB:

```python
from PIL import Image
im = Image.open('origen.png').convert('RGB')
im = im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS)
im.save('web/img/showcase/destino.webp', 'WEBP', quality=78, method=6)
```
