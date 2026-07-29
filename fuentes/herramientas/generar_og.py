#!/usr/bin/env python3
"""
Genera las imágenes de previsualización para redes sociales (og:image).

Produce web/img/og/*.png a 1200x630, que es lo que esperan WhatsApp, LinkedIn,
X, Slack y Facebook cuando alguien comparte un enlace del sitio.

Usa las mismas tipografías que el sitio. Como se sirven en woff2 y Pillow
necesita TTF, se convierten al vuelo con fontTools (solo en memoria del script;
el sitio sigue sirviendo los woff2).

    pip install Pillow fonttools brotli
    python3 fuentes/herramientas/generar_og.py

No es un paso de compilación: los PNG resultantes se versionan y se sirven tal
cual. Solo hay que reejecutarlo si cambian los textos o se añade un proyecto.
"""

import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'web'))
SALIDA = os.path.join(RAIZ, 'img', 'og')

W, H = 1200, 630
BG = (0x0a, 0x0a, 0x0c)
SUP = (0x13, 0x13, 0x16)
TEXTO = (0xf2, 0xf0, 0xec)
MUTED = (0x8a, 0x8a, 0x93)
LINEA = (0x2a, 0x2a, 0x2f)
ROJO = (0xff, 0x4d, 0x55)
ROJO2 = (0xc1, 0x27, 0x2d)
VIOLETA = (0x8b, 0x5c, 0xf6)


def cargar(woff2, peso):
    """woff2 -> TTF en memoria, fijando el peso del eje variable."""
    f = TTFont(os.path.join(RAIZ, 'fonts', woff2))
    f.flavor = None
    buf = io.BytesIO()
    f.save(buf)
    buf.seek(0)
    return buf.read(), peso


def fuente(datos_peso, tam):
    datos, peso = datos_peso
    fnt = ImageFont.truetype(io.BytesIO(datos), tam)
    try:
        fnt.set_variation_by_axes([peso])
    except Exception:
        pass  # si FreeType no trae soporte de variables, queda el peso base
    return fnt


def rejilla(img):
    """La misma textura de forja del sitio, al 2 %."""
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(242, 240, 236, 8))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(242, 240, 236, 8))
    return Image.alpha_composite(img.convert('RGBA'), capa).convert('RGB')


def degradado(ancho, alto):
    g = Image.new('RGB', (ancho, alto))
    p = g.load()
    for y in range(alto):
        for x in range(ancho):
            t = (x / max(ancho - 1, 1)) * 0.75 + (y / max(alto - 1, 1)) * 0.25
            if t < 0.4:
                k, a, b = t / 0.4, ROJO, ROJO2
            else:
                k, a, b = (t - 0.4) / 0.6, ROJO2, VIOLETA
            p[x, y] = tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))
    return g


def texto_degradado(img, xy, txt, fnt):
    """Dibuja texto relleno con el degradado de marca."""
    d = ImageDraw.Draw(img)
    caja = d.textbbox(xy, txt, font=fnt)
    ancho = max(caja[2] - caja[0], 1)
    alto = max(caja[3] - caja[1], 1)
    mascara = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mascara).text(xy, txt, font=fnt, fill=255)
    grad = Image.new('RGB', (W, H), ROJO2)
    grad.paste(degradado(ancho, alto).resize((W, H)), (0, 0))
    img.paste(grad, (0, 0), mascara)
    return caja


def base():
    return rejilla(Image.new('RGB', (W, H), BG))


def envolver(d, txt, fnt, ancho_max):
    """Parte el texto en líneas que quepan en ancho_max."""
    palabras, lineas, actual = txt.split(), [], ''
    for p in palabras:
        prueba = (actual + ' ' + p).strip()
        if d.textlength(prueba, font=fnt) <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def portada(mono, sans):
    img = base()
    d = ImageDraw.Draw(img)

    f_firma = fuente(mono, 82)
    texto_degradado(img, (80, 190), '<Iron-Coding/>', f_firma)

    f_tit = fuente(sans, 40)
    d.text((80, 310), 'Forjamos software que', font=f_tit, fill=TEXTO)
    d.text((80, 362), 'resuelve problemas reales.', font=f_tit, fill=TEXTO)

    f_sub = fuente(sans, 24)
    d.text((80, 438), 'Aplicaciones móviles multiplataforma · salud, sostenibilidad,',
           font=f_sub, fill=MUTED)
    d.text((80, 472), 'cuidado animal y juego', font=f_sub, fill=MUTED)

    f_pie = fuente(mono, 22)
    d.text((80, 545), 'iron-coding.art', font=f_pie, fill=MUTED)
    d.line([(80, 520), (1120, 520)], fill=LINEA, width=1)
    return img


def marco_captura(ruta, alto_objetivo):
    """Recorta la captura y le pone esquinas redondeadas y borde."""
    im = Image.open(ruta).convert('RGB')
    escala = alto_objetivo / im.height
    ancho = round(im.width * escala)
    im = im.resize((ancho, alto_objetivo), Image.LANCZOS)

    radio = 26
    mascara = Image.new('L', im.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                              radius=radio, fill=255)
    marco = Image.new('RGB', im.size, SUP)
    marco.paste(im, (0, 0), mascara)

    borde = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(borde).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                            radius=radio, outline=LINEA + (255,), width=2)
    marco = Image.alpha_composite(marco.convert('RGBA'), borde).convert('RGB')
    return marco, mascara


def producto(p, mono, sans):
    img = base()
    d = ImageDraw.Draw(img)

    # Captura a la derecha, recortada por la parte de abajo
    captura = os.path.join(RAIZ, 'img', 'showcase', p['img'])
    if os.path.exists(captura):
        marco, mascara = marco_captura(captura, 470)
        img.paste(marco, (860, 80), mascara)

    f_marca = fuente(mono, 26)
    texto_degradado(img, (80, 78), '<Iron-Coding/>', f_marca)

    f_nom = fuente(mono, 58)
    d.text((80, 210), p['nombre'], font=f_nom, fill=TEXTO)

    f_desc = fuente(sans, 26)
    for i, linea in enumerate(envolver(d, p['desc'], f_desc, 700)[:3]):
        d.text((80, 300 + i * 40), linea, font=f_desc, fill=MUTED)

    f_pie = fuente(mono, 21)
    d.line([(80, 520), (800, 520)], fill=LINEA, width=1)
    d.text((80, 545), 'iron-coding.art', font=f_pie, fill=MUTED)
    return img


PRODUCTOS = [
    {'slug': 'health-tracker', 'nombre': 'Health Tracker', 'img': 'healthtracker-panel.webp',
     'desc': 'Tus indicadores de salud interpretados contra rangos clínicos reales, '
             'no contra una tabla genérica.'},
    {'slug': 'run-for-win', 'nombre': 'Run For Win', 'img': 'runforwin-partida.webp',
     'desc': 'Editor de personajes de bloques y endless runner con jefes de mundo. '
             'Dos experiencias en una app.'},
    {'slug': 'footcarbonprint', 'nombre': 'FootCarbonPrint', 'img': 'footcarbonprint-huella.webp',
     'desc': 'Conoce tu huella de carbono en menos de siete minutos y qué hacer '
             'para bajarla, ordenado por impacto.'},
    {'slug': 'pituapp', 'nombre': 'PituApp', 'img': 'pituapp-mascota.webp',
     'desc': 'El cuidado de tu mascota siempre al día: vacunas, visitas y peso, '
             'con reporte veterinario en PDF.'},
]


def main():
    os.makedirs(SALIDA, exist_ok=True)
    mono = cargar('jetbrains-mono-latin.woff2', 800)
    sans = cargar('manrope-latin.woff2', 600)

    hechos = []

    ruta = os.path.join(SALIDA, 'iron-coding.png')
    portada(mono, sans).save(ruta, optimize=True)
    hechos.append(ruta)

    for p in PRODUCTOS:
        ruta = os.path.join(SALIDA, p['slug'] + '.png')
        producto(p, mono, sans).save(ruta, optimize=True)
        hechos.append(ruta)

    for r in hechos:
        print(f'  {os.path.getsize(r) // 1024:>4} KB  {os.path.relpath(r, os.path.dirname(RAIZ))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
