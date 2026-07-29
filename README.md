# Iron-Coding — sitio corporativo

Sitio estático (HTML/CSS/JS puro, sin paso de compilación) de **iron-coding.art**.
Se sirve tal cual desde el hosting compartido cPanel de GoDaddy.

## Estructura

```
web/                      ← esto es el sitio: lo que se sube a public_html
├── index.html            Portada
├── enviar.php            Manejador del formulario de contacto (solo cPanel)
├── .htaccess             Compresión, caché y MIME para Apache/cPanel
├── .nojekyll             Evita que GitHub Pages procese el sitio con Jekyll
├── robots.txt
├── sitemap.xml
├── favicon.svg
├── css/
│   ├── base.css          Tokens de identidad, reset, nav y pie (todas las páginas)
│   ├── home.css          Solo la portada
│   └── pages.css         Páginas interiores
├── js/
│   ├── main.js           Menú móvil y año del pie. Sin dependencias.
│   └── contacto.js       Validación del formulario y mensaje de resultado
├── fonts/                JetBrains Mono y Manrope (variables, subconjunto latino)
├── img/
│   ├── apple-touch-icon.png
│   ├── og/               Imágenes de previsualización para redes (1200x630)
│   └── showcase/         Capturas optimizadas a WebP
├── pages/                Páginas transversales del sitio
│   ├── blog.html         Índice del blog
│   ├── blog-plantilla.html   Plantilla para escribir un artículo
│   ├── nosotros.html
│   ├── contacto.html
│   ├── privacidad.html   Política GENERAL del sitio · BORRADOR, requiere revisión legal
│   └── terminos.html     Términos GENERALES del sitio · BORRADOR, requiere revisión legal
└── proyectos/            Un directorio por producto
    ├── index.html        Índice del portafolio
    ├── health-tracker/
    │   ├── index.html        Ficha del producto + lista de espera
    │   ├── privacidad.html   Política de ESTA app (la URL que pide la tienda)
    │   ├── terminos.html     Términos de ESTA app
    │   ├── soporte.html      Soporte y FAQ (OBLIGATORIA en App Store)
    │   └── prensa.html       Press kit: descripciones, ficha y capturas
    ├── run-for-win/      (misma estructura)
    ├── footcarbonprint/  (misma estructura)
    └── pituapp/          (misma estructura)

fuentes/                  ← material de trabajo, NO se publica
├── capturas-originales/  PNG originales de cada app + enlace a su README
├── iteraciones-diseno/   Exploraciones de identidad visual
└── herramientas/
    ├── scaffold_proyectos.py   Andamiaje de la sección de proyectos
    └── generar_og.py           Imágenes og:image para compartir en redes
```

> El encabezado y el pie están duplicados en cada archivo HTML, porque el sitio
> no tiene paso de compilación y por tanto no hay "includes". Si cambias un
> enlace del menú o del pie, hay que cambiarlo en **todas** las páginas.

## Dos niveles de documentos legales

Esta separación es deliberada y responde a lo que exigen las tiendas:

| Nivel | Dónde | Qué cubre |
|---|---|---|
| **General** | `pages/privacidad.html`<br>`pages/terminos.html` | El sitio web, el formulario de contacto y los principios comunes de la compañía. Aplica de forma supletoria a todo. |
| **Por aplicación** | `proyectos/<slug>/privacidad.html`<br>`proyectos/<slug>/terminos.html`<br>`proyectos/<slug>/soporte.html` | Los datos, permisos, terceros y descargos concretos de **esa** app, más su página de soporte. **Son las URL que se pegan en Google Play Console y App Store Connect.** Prevalece sobre la general para esa app. |

Google Play y la App Store exigen una política de privacidad **por ficha de
aplicación**, que describa exactamente lo que esa app recoge. Una política
genérica de empresa es motivo frecuente de rechazo en revisión.

Las URL que se registran en cada tienda quedan así:

```
https://iron-coding.art/proyectos/<slug>/privacidad.html    Play + App Store
https://iron-coding.art/proyectos/<slug>/terminos.html      opcional (EULA)
https://iron-coding.art/proyectos/<slug>/soporte.html       OBLIGATORIA en App Store
https://iron-coding.art/proyectos/<slug>/prensa.html        press kit
```

con `<slug>` = `health-tracker`, `run-for-win`, `footcarbonprint` o `pituapp`.

## Cómo agregar un proyecto

1. Abre `fuentes/herramientas/scaffold_proyectos.py`, copia un bloque de la
   lista `PROYECTOS` y cambia los datos: `slug`, nombre, textos, capturas y la
   sección `legal` (datos que trata, permisos, terceros y su descargo propio).
2. Convierte sus capturas a WebP en `web/img/showcase/` (ver más abajo).
3. Ejecuta el script:

   ```bash
   python3 fuentes/herramientas/scaffold_proyectos.py --listar   # ver qué haría
   python3 fuentes/herramientas/scaffold_proyectos.py            # crear
   ```

4. Añade sus URL a `web/sitemap.xml` y, si quieres que salga en la portada,
   una tarjeta en `web/index.html`.

**El script nunca sobrescribe un archivo que ya existe**, así que se puede
volver a ejecutar sin miedo: solo crea lo que falta. No es un paso de
compilación — una vez generado el HTML, la fuente de verdad es el HTML, sobre
todo en los textos legales, que se van a corregir a mano tras la revisión
jurídica. `--forzar` regenera todo y descarta esas correcciones.

## Lista de espera

Ninguna app está publicada todavía, así que cada ficha de producto lleva un
formulario para avisar del lanzamiento. Es la conversión principal del sitio.

`proyectos/<slug>/index.html` envía por POST a `suscribir.php`, que valida,
descarta el spam con un campo trampa y guarda la fila en un CSV. La URL de
retorno **se deriva del slug en el servidor**, nunca del formulario, para que
esto no se pueda usar como redirector abierto.

Dónde queda el CSV, en orden de preferencia:

1. `/home/<usuario>/iron-coding-datos/lista-espera.csv` — **por encima** de la
   raíz web. Es lo normal y lo deseable: son datos personales y ahí no hay forma
   de servirlos por HTTP.
2. `public_html/datos/lista-espera.csv` — solo si el hosting no deja escribir
   arriba. Va protegido con `.htaccess`, pero eso depende de que ese archivo
   oculto se haya subido.

Cuando la lista crezca, conviene pasar a un servicio de correo de verdad
(Buttondown, MailerLite y similares): un CSV no gestiona bajas ni rebotes.

Al publicar una app hay que quitar su formulario: pon `'lista_espera': False`
en `scaffold_proyectos.py` y regenera esa ficha.

## Soporte por aplicación

`proyectos/<slug>/soporte.html`. **La App Store exige una URL de soporte
funcional por cada app y sin ella no se puede ni enviar a revisión.** Tiene que
ofrecer un método de contacto real: una FAQ sola, un placeholder o un
«próximamente» son motivo de rechazo. Google Play exige correo de soporte.

## Formulario de contacto

`pages/contacto.html` envía por POST a `enviar.php`, que valida en el servidor,
descarta el spam con un campo trampa y manda el mensaje con `mail()`. Tras
enviar redirige a `pages/contacto.html?estado=ok` o `?estado=error`, y
`js/contacto.js` muestra el aviso correspondiente.

**El formulario solo funciona en cPanel**, que tiene PHP. En GitHub Pages, que
sirve archivos estáticos, el envío devuelve 404.

Antes de publicar hay que crear los buzones en cPanel → *Cuentas de correo* y
ajustar `DESTINO` y `REMITENTE` al principio de `enviar.php`. `REMITENTE` tiene
que ser una dirección del propio dominio: si se pone ahí el correo de quien
escribe, los servidores lo tratan como suplantación y el mensaje acaba en spam.

## Cómo agregar un artículo al blog

1. Copia `pages/blog-plantilla.html` como `pages/blog-mi-articulo.html`.
2. Borra la línea `<meta name="robots" content="noindex, nofollow">`.
3. Rellena título, fecha, tiempo de lectura y cuerpo.
4. En `pages/blog.html`, descomenta el bloque `<article class="post-card">`,
   duplícalo para tu artículo y borra el bloque `blog-vacio`.
5. Añade la URL nueva a `sitemap.xml`.

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

## Movimiento

Dos únicos mecanismos, ambos en CSS:

1. **Entrada del hero** — una sola vez, escalonada, solo en la portada.
2. **Revelado al hacer scroll** — `[data-revelar]`, una vez por elemento, con
   `IntersectionObserver` (~1 KB en `main.js`). Nada se repite en bucle.

Los dos respetan `prefers-reduced-motion`. Y el estado oculto solo se aplica con
`html.js`, más una salvaguarda de 3 s en el script del `<head>`: si `main.js` no
llega a ejecutarse, el contenido aparece igual en lugar de quedarse invisible.

Se descartó a propósito el fondo animado tipo «red neuronal»: los héroes WebGL
degradan el LCP, y con este sitio en hosting compartido eso costaría más de lo
que aporta.

## Imágenes para redes

`python3 fuentes/herramientas/generar_og.py` regenera `web/img/og/*.png`
(1200 × 630) con las tipografías del propio sitio. Hay una genérica y una por
producto, con su captura. Se versionan y se sirven tal cual; solo hay que
reejecutar el script si cambian los textos o se añade un proyecto.
