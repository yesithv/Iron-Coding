#!/usr/bin/env python3
"""
Andamiaje de la sección de proyectos del sitio de Iron-Coding.

Genera, por cada proyecto, la carpeta web/proyectos/<slug>/ con:

    index.html        ficha del producto
    privacidad.html   política de privacidad de ESA app (la que piden las tiendas)
    terminos.html     términos de uso de ESA app

y además web/proyectos/index.html con el índice.

IMPORTANTE
----------
Esto NO es un paso de compilación: el sitio se sirve tal cual desde el HTML
generado. Este script solo crea el andamiaje la primera vez.

Por defecto **nunca sobrescribe** un archivo que ya exista, de modo que se puede
volver a ejecutar sin miedo para añadir un proyecto nuevo: solo escribe lo que
falta. Una vez generado un archivo, la fuente de verdad es el HTML, no este
script — sobre todo en los textos legales, que se van a corregir a mano tras la
revisión jurídica.

Uso:
    python3 fuentes/herramientas/scaffold_proyectos.py            # crea lo que falte
    python3 fuentes/herramientas/scaffold_proyectos.py --listar   # muestra qué haría
    python3 fuentes/herramientas/scaffold_proyectos.py --forzar   # regenera TODO (pierde ediciones)

Para añadir un proyecto: copia un bloque de PROYECTOS, cambia los datos y
ejecuta el script.
"""

import argparse
import os
import sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'web')
RAIZ = os.path.normpath(RAIZ)

# ===========================================================================
# DATOS DE CADA PROYECTO
# ===========================================================================

PROYECTOS = [
    {
        'slug': 'health-tracker',
        'nombre': 'Health Tracker',
        'marca_tienda': 'My Vitals',
        'insignia': True,
        'tagline': 'El paciente registra sus indicadores de salud y los ve interpretados '
                   'contra rangos clínicos reales, no contra una tabla genérica.',
        'resumen_corto': 'Seguimiento de indicadores de salud con interpretación clínica, '
                         'historiales con gráficas y exportación a PDF.',
        'estado_chip': 'beta interna',
        'parrafos': [
            'La mayoría de aplicaciones de salud guardan números. Health Tracker los '
            '<strong>interpreta</strong>: cada valor se contrasta con bandas clínicas '
            'administradas en el servidor y resueltas por dispositivo de medición, sexo y '
            'edad, y se presenta con un semáforo de estado. Un perfil lipídico se lee con '
            'los rangos del laboratorio donde se tomó el examen, porque no todos los '
            'laboratorios usan los mismos cortes.',
            'Es local-first de verdad: todo se guarda en SQLite en el dispositivo y la app '
            'es plenamente usable sin red. La sincronización con la API es bidireccional y '
            'solo marca un registro como sincronizado si el servidor confirma, de modo que '
            'un fallo de red nunca pierde datos.',
        ],
        'features': [
            ('Cuatro familias de indicadores', 'signos vitales, antropometría con seis perímetros corporales, perfil lipídico y composición corporal.'),
            ('Semáforo clínico', 'por indicador, con cortes de fábrica como respaldo cuando no hay red.'),
            ('Historiales con gráficas', 'de evolución y bandas de referencia dibujadas sobre la curva.'),
            ('Exportación a PDF y CSV', 'con compartido nativo desde cada pestaña.'),
            ('Cinco idiomas', '(español, inglés, portugués, italiano y alemán) y unidades métricas o imperiales.'),
            ('Dos temas completos', '— Pulso Clínico y Consulta Serena — sobre un vocabulario de tokens semánticos.'),
            ('Copia de seguridad', 'completa en JSON, biometría opcional y recordatorios diarios.'),
        ],
        'ficha': [
            ('Estado', 'Versión 0.1.0 · Fase 0. Funcionalmente completa de punta a punta; quedan por sustituir los andamios de autenticación.'),
            ('Plataformas', 'Android y web ejercitados; iOS, Linux, macOS y Windows compilables.'),
            ('Stack', 'Flutter · Dart · SQLite (sqflite) · provider · go_router · fl_chart'),
            ('Backend', 'HealthTracker-Api, fuente de verdad de los rangos clínicos'),
            ('Calidad', '16 archivos de prueba, incluido un contrato semántico que falla la compilación si un tema baja del contraste AA'),
        ],
        'demo': None,
        'galeria': [
            ('healthtracker-panel.webp', 1543, 'Panel principal con la tendencia de IMC y los signos vitales del día.', 'panel principal'),
            ('healthtracker-lipidos.webp', 1543, 'Gráfica de evolución del perfil lipídico con sus bandas de referencia.', 'perfil lipídico'),
            ('healthtracker-objetivos.webp', 1543, 'Pantalla de metas de salud con el progreso de cada objetivo.', 'metas de salud'),
            ('healthtracker-descubrir.webp', 1543, 'Sección Descubre con artículos y rutinas de salud.', 'descubre'),
        ],
        # ---- Lista de espera: la app todavia no esta publicada ----
        'lista_espera': True,
        'prensa': {
            'categoria': 'Salud y forma física',
            'idiomas': 'Español, inglés, portugués, italiano y alemán',
            'precio': '<span class="pendiente">[POR DEFINIR]</span>',
            'corta': 'Tus indicadores de salud, interpretados contra rangos clínicos reales.',
            'media': 'Health Tracker registra signos vitales, antropometría, perfil lipídico y '
                     'composición corporal, y contrasta cada valor con bandas clínicas resueltas '
                     'por dispositivo de medición, sexo y edad. Funciona sin conexión y exporta a '
                     'PDF y CSV.',
            'larga': 'La mayoría de aplicaciones de salud guardan números; Health Tracker los '
                     'interpreta. Cada medición se contrasta con rangos clínicos administrados en '
                     'servidor —no con una tabla genérica— y se presenta con un semáforo de estado, '
                     'porque un perfil lipídico debe leerse con los cortes del laboratorio donde se '
                     'tomó el examen. Todo se guarda en el dispositivo y la aplicación es plenamente '
                     'usable sin red; la sincronización solo marca un registro como sincronizado si '
                     'el servidor confirma, de modo que un fallo de conexión nunca pierde datos. '
                     'Incluye historiales con gráficas y bandas de referencia, exportación a PDF y '
                     'CSV, copia de seguridad completa, bloqueo biométrico opcional y cinco idiomas.',
        },
        # ---- Soporte: Apple EXIGE una URL de soporte funcional por app ----
        'soporte': {
            'intro': 'Escríbenos y te respondemos en menos de dos días hábiles. '
                     'Si el problema es con un dato concreto, cuéntanos qué indicador es '
                     'y desde qué versión te pasa.',
            'faq': [
                ('¿La aplicación funciona sin conexión?',
                 'Sí. Todos tus registros se guardan en el dispositivo y puedes consultarlos y '
                 'crearlos sin red. Si tienes cuenta, se sincronizan cuando vuelvas a conectarte.'),
                ('¿Cómo exporto mi historial?',
                 'Desde cada pestaña, con el botón de exportar: puedes generar un PDF o un CSV y '
                 'compartirlo con la hoja nativa del sistema.'),
                ('¿Cómo hago una copia de seguridad?',
                 'En Ajustes → Datos puedes crear una copia completa en formato JSON. Guárdala '
                 'fuera del teléfono: si desinstalas la app sin sincronizar, los datos locales se '
                 'borran con ella.'),
                ('¿Por qué un valor mío aparece fuera de rango si mi laboratorio dice que está bien?',
                 'Los rangos se resuelven por dispositivo de medición, sexo y edad, y no todos los '
                 'laboratorios usan los mismos cortes. Revisa que el examen esté registrado con su '
                 'laboratorio correcto. Ante cualquier duda clínica, consulta a tu médico: la app '
                 'no diagnostica.'),
                ('¿Cómo cambio el idioma o las unidades?',
                 'En Ajustes puedes elegir entre cinco idiomas y cambiar entre unidades métricas '
                 'e imperiales. El cambio se aplica de inmediato, sin reiniciar.'),
                ('¿Cómo activo el bloqueo con huella o rostro?',
                 'En Ajustes → Seguridad. La verificación la hace tu sistema operativo; nosotros '
                 'nunca vemos tus datos biométricos.'),
                ('¿Cómo elimino todos mis datos?',
                 'Puedes borrar registros uno a uno desde la app, o eliminar la cuenta completa '
                 'desde Ajustes. Si prefieres que lo hagamos nosotros, escríbenos.'),
            ],
        },
        # ---- Datos para la parte legal de ESTA app ----
        'legal': {
            'trata_datos_personales': True,
            'trata_sensibles': True,
            'tiene_cuenta': True,
            'tiene_compras': False,
            'tiene_publicidad': False,
            'edad_minima': '18',
            'datos': [
                ('Datos de salud', 'Presión arterial, frecuencia cardíaca, peso, talla, perímetros corporales, perfil lipídico y composición corporal.', 'Mostrar tu historial, calcular tendencias e interpretar cada valor contra sus rangos de referencia.', 'Sí, son el objeto de la app'),
                ('Datos de perfil', 'Nombre, correo electrónico, fecha de nacimiento y sexo biológico.', 'Identificar tu cuenta y resolver los rangos clínicos que te corresponden, que dependen de edad y sexo.', 'Sí'),
                ('Metas de salud', 'Objetivos de peso, grasa corporal y masa muscular.', 'Calcular cuánto te falta para tu meta.', 'No'),
                ('Preferencias', 'Idioma, tema, sistema de unidades y hora del recordatorio.', 'Recordar cómo quieres usar la app.', 'No'),
            ],
            'permisos': [
                ('Notificaciones', 'Enviarte el recordatorio diario de registro que tú configuras. Puedes desactivarlo.'),
                ('Biometría (huella o rostro)', 'Bloquear el acceso a la app, si activas esa opción. La verificación la hace el sistema operativo; nosotros nunca vemos tus datos biométricos.'),
                ('Almacenamiento / archivos', 'Guardar los PDF y CSV que exportas y las copias de seguridad que creas.'),
            ],
            'almacenamiento': 'Todos los registros se guardan cifrados en tránsito y en una base de datos '
                              'SQLite dentro de tu dispositivo. Si activas la cuenta, se sincronizan además '
                              'con el servidor de Iron-Coding (HealthTracker-Api).',
            'terceros': [
                ('HealthTracker-Api (Iron-Coding)', 'Sincronizar tus registros entre dispositivos y servir los rangos clínicos.'),
                ('Google Play / App Store', 'Distribuir la aplicación y sus actualizaciones.'),
            ],
            'descargo_titulo': 'Health Tracker no es un dispositivo médico',
            'descargo': 'Health Tracker es una herramienta de <strong>registro y seguimiento personal</strong>. '
                        'Los rangos de referencia que muestra son orientativos y sirven para contextualizar tus '
                        'propias mediciones. <strong>La aplicación no diagnostica, no prescribe tratamientos y '
                        'no sustituye el criterio de un profesional de la salud.</strong> Ninguna decisión '
                        'médica debe tomarse únicamente con base en lo que muestre la aplicación. Ante cualquier '
                        'síntoma o duda, consulta a tu médico. En una urgencia, acude a un servicio de '
                        'emergencias: la aplicación no está diseñada para detectar ni alertar situaciones críticas.',
            'reglas_uso': [
                'Los datos que registras los introduces tú. La aplicación no puede verificar si un valor es correcto, y una interpretación construida sobre un dato mal digitado será igualmente incorrecta.',
                'No uses la aplicación como único registro de información clínica que necesites conservar. Exporta copias de seguridad con regularidad.',
                'No introduzcas datos de salud de otra persona sin su autorización.',
            ],
        },
    },
    {
        'slug': 'run-for-win',
        'nombre': 'Run For Win',
        'marca_tienda': 'Run For Win',
        'insignia': False,
        'tagline': 'Editor de personajes de bloques y endless runner pseudo-3D con jefes de mundo. '
                   'Dos experiencias dentro de la misma app.',
        'resumen_corto': 'Editor de minifiguras y endless runner de tres carriles con jefes, '
                         'economía de monedas y misiones.',
        'estado_chip': 'demo pública',
        'parrafos': [
            'El jugador diseña su minifigura —cara, peinado, torso, piernas, calzado, capa, ocho '
            'ranuras de accesorios y hasta la música de la partida— y luego sale a correr con ella '
            'por mundos temáticos en una vista de tres carriles. Al final de cada mundo espera un '
            'jefe con tres corazones, al que se vence esquivando sus ataques y embistiendo.',
            'Alrededor de esos dos pilares hay una economía completa: monedas, ruleta diaria, cofres '
            'común y VIP, tienda de piezas por rareza, misiones rotativas y ranking local por mundo. '
            'Los personajes, mundos y jefes se dibujan por código, con formas y colores, no con '
            'imágenes: el juego pesa lo que pesa el motor.',
        ],
        'features': [
            ('Editor profundo', '— piel, ojos, boca, cejas, extras faciales, casco, torso, guantes, piernas, calzado, capa y ocho ranuras de accesorios.'),
            ('Personajes precargados', 'agrupados por colección, que sirven de punto de partida y se pueden modificar.'),
            ('Motor Flame', 'con perspectiva pseudo-3D, tres carriles, salto y deslizamiento, y tres zonas de dificultad progresiva.'),
            ('Peleas contra jefes', 'temáticos al cierre de cada mundo.'),
            ('Economía y progresión', '— monedas, ruleta diaria, cofres, desbloqueo de piezas por rareza y misiones rotativas.'),
            ('Ocho mundos', 'con paletas y jefes propios, dos disponibles y el resto bloqueados.'),
            ('Audio completo', '— efectos y música de fondo seleccionable por personaje.'),
        ],
        'ficha': [
            ('Estado', 'Jugable, con demo web pública. Pendiente de publicación en tiendas.'),
            ('Plataformas', 'Android, iOS y web'),
            ('Stack', 'Flutter · Flame · flutter_bloc · Hive · go_router · get_it'),
            ('Arquitectura', 'Clean Architecture por funcionalidad, con las tres capas en cada una'),
        ],
        'demo': ('https://yesithv.github.io/lego-custom-character/', 'jugar_demo()'),
        'galeria': [
            ('runforwin-partida.webp', 1243, 'Partida en curso: el personaje corre por el carril central recogiendo monedas.', 'partida'),
            ('runforwin-editor.webp', 1245, 'Editor de personajes con las pestañas de cabeza, pelo, torso, piernas y accesorios.', 'editor'),
            ('runforwin-mundos.webp', 1251, 'Selector de mundos temáticos del juego.', 'mundos'),
            ('runforwin-ruleta.webp', 1255, 'Ruleta diaria con premios de monedas y piezas por rareza.', 'ruleta diaria'),
        ],
        'lista_espera': True,
        'prensa': {
            'categoria': 'Juegos · Arcade',
            'idiomas': 'Español e inglés',
            'precio': 'Gratuita, sin compras dentro de la aplicación',
            'corta': 'Diseña tu minifigura de bloques y corre con ella esquivando jefes.',
            'media': 'Run For Win combina un editor de personajes de bloques con un endless runner '
                     'pseudo-3D de tres carriles y peleas contra jefes al final de cada mundo. '
                     'Sin anuncios, sin cuentas y sin recoger datos personales.',
            'larga': 'Run For Win son dos juegos en uno. Primero se diseña una minifigura de '
                     'bloques —cara, peinado, torso, piernas, calzado, capa, ocho ranuras de '
                     'accesorios y hasta la música de partida— y después se sale a correr con ella '
                     'por mundos temáticos en una vista pseudo-3D de tres carriles, esquivando '
                     'obstáculos, recogiendo monedas y activando potenciadores. Al cierre de cada '
                     'mundo espera un jefe con tres corazones. Alrededor hay una economía completa: '
                     'ruleta diaria, cofres, tienda de piezas por rareza, misiones rotativas y '
                     'ranking local. Los personajes, mundos y jefes se dibujan por código, no con '
                     'imágenes, así que el juego pesa lo que pesa el motor.',
        },
        'soporte': {
            'intro': 'Escríbenos y te respondemos en menos de dos días hábiles. '
                     'Si el juego se cierra o se queda trabado, dinos en qué mundo estabas y '
                     'qué modelo de dispositivo usas.',
            'faq': [
                ('Perdí mi progreso, ¿se puede recuperar?',
                 'No. El juego guarda todo en el dispositivo y no tiene cuenta ni copia en la '
                 'nube, así que al desinstalarlo el progreso se pierde. Es el precio de no pedirte '
                 'ningún dato personal.'),
                ('¿Las monedas se pueden comprar con dinero real?',
                 'No. Las monedas se ganan jugando, con la ruleta diaria y con los cofres. No hay '
                 'compras dentro del juego y las monedas no tienen valor monetario real.'),
                ('¿Cómo desbloqueo los otros mundos?',
                 'Los mundos se van habilitando con el progreso. Ahora mismo hay dos disponibles y '
                 'el resto llegarán en próximas actualizaciones.'),
                ('No se escucha la música.',
                 'Comprueba que el dispositivo no esté en silencio y que la música del personaje '
                 'esté seleccionada en el editor. Cada personaje puede tener su propia pista.'),
                ('¿El juego tiene publicidad?',
                 'No. No hay anuncios, no hay rastreadores y no se recoge ningún dato personal.'),
                ('¿Puedo jugar sin conexión?',
                 'Sí, el juego funciona completamente sin red.'),
            ],
        },
        'legal': {
            'trata_datos_personales': False,
            'trata_sensibles': False,
            'tiene_cuenta': False,
            'tiene_compras': False,
            'tiene_publicidad': False,
            'edad_minima': None,
            'datos': [
                ('Progreso del juego', 'Personajes creados, monedas, piezas desbloqueadas, misiones y puntuaciones.', 'Guardar tu partida para que la encuentres al volver.', 'No sale del dispositivo'),
                ('Preferencias', 'Volumen, música seleccionada y tema.', 'Recordar cómo configuraste el juego.', 'No sale del dispositivo'),
            ],
            'permisos': [
                ('Ninguno', 'El juego no solicita permisos del sistema. No accede a la cámara, los contactos, la ubicación ni los archivos.'),
            ],
            'almacenamiento': 'Todo el progreso se guarda en una base de datos local (Hive) dentro de tu '
                              'dispositivo. No hay servidor, no hay cuenta y no hay copia en la nube: si '
                              'desinstalas el juego, el progreso se pierde con él.',
            'terceros': [
                ('Google Play / App Store', 'Distribuir la aplicación y sus actualizaciones.'),
            ],
            'descargo_titulo': 'Monedas y objetos del juego',
            'descargo': 'Las monedas, cofres, piezas y cualquier otro objeto del juego son '
                        '<strong>elementos virtuales sin valor monetario real</strong>. No se pueden '
                        'canjear por dinero, no son transferibles fuera del juego y no constituyen '
                        'propiedad ni saldo a favor. Podemos ajustar la economía del juego —precios, '
                        'recompensas y probabilidades— en futuras actualizaciones.',
            'reglas_uso': [
                'No uses trucos, modificaciones del cliente ni herramientas automatizadas para alterar el progreso o el ranking.',
                'El ranking es local a tu dispositivo: no compite contra otras personas ni se envía a ningún servidor.',
            ],
        },
    },
    {
        'slug': 'footcarbonprint',
        'nombre': 'FootCarbonPrint',
        'marca_tienda': 'FootCarbonPrint',
        'insignia': False,
        'tagline': 'Conoce tu huella, cambia tu mundo. Autodiagnóstico de huella de carbono '
                   'en menos de siete minutos.',
        'resumen_corto': 'Test de huella de carbono con equivalencias entendibles y un plan '
                         'de acción ordenado por impacto real.',
        'estado_chip': 'en desarrollo',
        'parrafos': [
            'El problema de las calculadoras de huella de carbono no es medir: es que el resultado '
            'no le dice nada a nadie. FootCarbonPrint traduce las toneladas de CO₂ en imágenes que '
            'sí se entienden —«tu impacto equivale a talar 70 árboles al año»— y entrega un plan de '
            'acción ordenado por impacto real, con el ahorro estimado de cada cambio.',
            'El test se responde deslizando y tocando, nunca escribiendo: seis módulos '
            'independientes, un máximo de 35 preguntas y valores por defecto inteligentes para quien '
            'no conoce sus consumos exactos. Los factores de emisión están calibrados por país, '
            'porque la red eléctrica colombiana (0,175 kgCO₂/kWh, mayoritariamente hidroeléctrica) '
            'no se parece en nada a la alemana.',
        ],
        'features': [
            ('Seis módulos de test', '— transporte, alimentación, hogar y energía, consumo, residuos y agua.'),
            ('Motor de cálculo con fuentes verificables', ': IPCC, EPA, GHG Protocol, DEFRA, ICAO y estudios revisados por pares.'),
            ('Equivalencias visuales', 'que convierten toneladas en árboles, bombillas o cargas de teléfono.'),
            ('Comparativa contextual', 'frente al promedio de Colombia, el mundial y la meta de París 2050.'),
            ('Plan de acción personalizado', 'con las cinco medidas de mayor impacto, su dificultad y su reducción estimada.'),
            ('Gamificación', '— EcoPoints, niveles, medallas y retos semanales.'),
            ('Modo offline', 'básico: los datos son sensibles y el uso sin conexión es una opción de primera clase.'),
        ],
        'ficha': [
            ('Estado', 'Especificación funcional cerrada y desarrollo activo del MVP. Aún no disponible al público.'),
            ('Plataformas previstas', 'Android, iOS y web'),
            ('Stack', 'Flutter · Spring Boot · PostgreSQL · Firebase Auth · ML Kit para OCR de facturas'),
            ('Contexto', 'Factores de emisión calibrados para Colombia, actualizables por región sin redesplegar'),
        ],
        'demo': None,
        'galeria': [
            ('footcarbonprint-huella.webp', 1255, 'Resultado del test: 3,96 toneladas de CO₂ al año con su desglose.', 'tu huella'),
            ('footcarbonprint-plan.webp', 1252, 'Plan de acción con las medidas ordenadas por reducción estimada de CO₂.', 'plan de acción'),
            ('footcarbonprint-retos.webp', 1256, 'Pantalla de logros y reto semanal con su recompensa en puntos.', 'retos y logros'),
        ],
        'lista_espera': True,
        'prensa': {
            'categoria': 'Estilo de vida · Sostenibilidad',
            'idiomas': '<span class="pendiente">[POR CONFIRMAR AL CERRAR EL MVP]</span>',
            'precio': '<span class="pendiente">[POR DEFINIR]</span>',
            'corta': 'Conoce tu huella de carbono en menos de siete minutos y qué hacer con ella.',
            'media': 'FootCarbonPrint calcula la huella de carbono personal con factores de emisión '
                     'del IPCC, la EPA y el GHG Protocol, la traduce en equivalencias entendibles y '
                     'entrega un plan de acción ordenado por impacto real.',
            'larga': 'El problema de las calculadoras de huella de carbono no es medir: es que el '
                     'resultado no le dice nada a nadie. FootCarbonPrint responde con equivalencias '
                     'que sí se entienden —«tu impacto equivale a talar 70 árboles al año»— y con un '
                     'plan de acción ordenado por reducción estimada, indicando la dificultad de cada '
                     'medida. El test se responde deslizando y tocando, nunca escribiendo: seis '
                     'módulos independientes, un máximo de 35 preguntas y valores por defecto '
                     'inteligentes. Los factores están calibrados por país, porque la red eléctrica '
                     'colombiana (0,175 kgCO₂/kWh, mayoritariamente hidroeléctrica) no se parece a la '
                     'alemana. Cada factor del motor de cálculo tiene su referencia documentada.',
        },
        'soporte': {
            'intro': 'Escríbenos y te respondemos en menos de dos días hábiles. '
                     'Si el resultado del test no te cuadra, cuéntanos qué módulo es y qué '
                     'respondiste: casi siempre es un factor de emisión que hay que revisar.',
            'faq': [
                ('¿De dónde salen los números?',
                 'De fuentes públicas y verificables: IPCC, EPA, GHG Protocol, DEFRA, ICAO y '
                 'estudios revisados por pares. Cada factor tiene su referencia documentada. El '
                 'factor de red eléctrica está calibrado por país.'),
                ('¿Puedo repetir el test?',
                 'Sí, y es lo recomendable: mensual, trimestral o anual. La app guarda el '
                 'histórico para que veas tu evolución.'),
                ('¿Por qué mi huella cambió sin que yo cambiara nada?',
                 'Los factores de emisión se actualizan cuando los organismos publican versiones '
                 'nuevas. Si eso pasa, el resultado puede moverse aunque tus respuestas sean las '
                 'mismas.'),
                ('El lector de facturas no reconoce mi recibo.',
                 'Necesita buena luz y que los kWh se vean completos. Si tu comercializadora usa '
                 'un formato poco común, escríbenos con una foto y lo añadimos.'),
                ('¿Sirve para reportar la huella de mi empresa?',
                 'No. Los resultados son estimaciones personales y no constituyen un inventario '
                 'certificado ni valen para reporte regulatorio o corporativo.'),
                ('¿Cómo elimino mi cuenta y mis datos?',
                 'Desde Ajustes → Cuenta, o escribiéndonos a privacidad@iron-coding.art.'),
            ],
        },
        'legal': {
            'trata_datos_personales': True,
            'trata_sensibles': False,
            'tiene_cuenta': True,
            'tiene_compras': True,
            'tiene_publicidad': False,
            'edad_minima': '16',
            'en_desarrollo': True,
            'datos': [
                ('Respuestas del test', 'Medio de transporte, kilómetros, vuelos, tipo de dieta, consumo eléctrico, hábitos de compra y residuos.', 'Calcular tu huella de carbono y construir tu plan de acción.', 'Sí, son el objeto de la app'),
                ('Ubicación aproximada', 'País y ciudad o región, elegidos por ti en una lista.', 'Aplicar los factores de emisión correctos: la red eléctrica varía mucho entre países.', 'Sí'),
                ('Datos de perfil', 'Nombre, correo electrónico y personas que viven en el hogar.', 'Identificar tu cuenta y repartir el consumo del hogar.', 'Sí'),
                ('Progreso y retos', 'EcoPoints, medallas, retos cumplidos e histórico de tests.', 'Mostrar tu evolución en el tiempo.', 'No'),
            ],
            'permisos': [
                ('Cámara', 'Solo si usas el lector de facturas: se fotografía el recibo de luz o gas para extraer los kWh automáticamente. La foto se procesa para ese fin y no se publica.'),
                ('Notificaciones', 'Avisarte de los retos semanales y recordarte repetir el test. Puedes desactivarlo.'),
                ('Ubicación', 'Opcional. Solo si activas el seguimiento automático de transporte. La app funciona completa sin este permiso.'),
            ],
            'almacenamiento': 'Las respuestas y los resultados se guardan en tu dispositivo y, si creas una '
                              'cuenta, también en el servidor de Iron-Coding para que puedas consultarlos '
                              'desde otro dispositivo y comparar tu evolución.',
            'terceros': [
                ('API de FootCarbonPrint (Iron-Coding)', 'Calcular la huella y guardar tu histórico.'),
                ('Firebase Authentication (Google)', 'Permitir el inicio de sesión con correo, Google o Apple.'),
                ('Google ML Kit', 'Leer el texto de la factura que fotografías, para extraer los kWh.'),
                ('Google Play / App Store', 'Distribuir la aplicación y procesar las compras dentro de ella.'),
            ],
            'descargo_titulo': 'Los resultados son estimaciones',
            'descargo': 'Los resultados de huella de carbono son <strong>estimaciones</strong> calculadas a '
                        'partir de factores de emisión publicados por organismos como el IPCC, la EPA y el '
                        'GHG Protocol, aplicados a las respuestas que tú proporcionas. <strong>No '
                        'constituyen una medición certificada</strong> ni sirven como inventario oficial de '
                        'emisiones para efectos regulatorios, de reporte corporativo, de compensación '
                        'obligatoria o de acreditación ante terceros. La precisión del resultado depende '
                        'directamente de la exactitud de lo que respondas.',
            'reglas_uso': [
                'No presentes los resultados de la aplicación como una certificación de huella de carbono ante clientes, autoridades o inversionistas.',
                'Los factores de emisión se actualizan cuando las fuentes publican nuevas versiones: un test repetido puede dar un resultado distinto por ese motivo.',
            ],
        },
    },
    {
        'slug': 'pituapp',
        'nombre': 'PituApp',
        'marca_tienda': 'PituApp — PetBienestar',
        'insignia': False,
        'tagline': 'PetBienestar — el cuidado de tu mascota, siempre al día. Vacunas, '
                   'desparasitaciones, visitas y peso en un solo historial.',
        'resumen_corto': 'Plan de cuidados e historial clínico de mascotas, con recordatorios '
                         'y reporte veterinario en PDF.',
        'estado_chip': 'MVP · demo pública',
        'parrafos': [
            'Quien cuida un animal lleva las fechas en la cabeza o en un cuaderno: la desparasitación '
            'cada cuatro meses, la vacuna anual, el control de peso mensual. PituApp convierte eso en '
            'un plan de cuidados que se recalcula solo cada vez que se marca algo como hecho, y avisa '
            'antes de que venza.',
            'Lo que la separa de una lista de tareas es el historial clínico: visitas médicas, vacunas '
            'con su próxima dosis autosugerida, diagnósticos con estado y registro de peso con aviso '
            'informativo cuando la variación supera el 10 %. Todo eso se exporta a un reporte '
            'veterinario en PDF listo para llevar a la consulta.',
        ],
        'features': [
            ('Varias mascotas', 'con archivado que detiene los recordatorios pero conserva el historial.'),
            ('Catálogo de cuidados por especie', 'precargado, con frecuencias editables y cuidados personalizados.'),
            ('Historial clínico integrado', 'en una línea de tiempo con filtros por tipo y rango de fechas.'),
            ('Documentos adjuntos', 'con galería, filtro por tipo y compresión automática de imágenes.'),
            ('Recordatorios locales', 'del día, vencidos y anticipados, respetando el límite de notificaciones de iOS.'),
            ('Reporte veterinario en PDF', 'con selección de contenido y hoja de compartir nativa.'),
            ('Respaldo y portabilidad', '— exportar e importar en JSON, con opción de reemplazar o combinar.'),
        ],
        'ficha': [
            ('Estado', 'MVP de fase 1 funcionalmente completo, con demo web pública. Pendiente el cifrado en reposo y la publicación en tiendas.'),
            ('Plataformas', 'Android, iOS y web'),
            ('Stack', 'Flutter · Riverpod · Clean Architecture con patrón repositorio'),
            ('Datos', 'Local-first, sin backend. Preparado para sincronizar en la fase 2 sin migraciones destructivas'),
        ],
        'demo': ('https://yesithv.github.io/pitu-app/', 'probar_demo()'),
        'galeria': [
            ('pituapp-mascota.webp', 1247, 'Ficha de una mascota con su línea de tiempo de vacunas, visitas y peso.', 'ficha e historial'),
            ('pituapp-reporte.webp', 1251, 'Reporte veterinario en PDF con condiciones, visitas, vacunas y plan de cuidados.', 'reporte veterinario'),
        ],
        'lista_espera': True,
        'prensa': {
            'categoria': 'Estilo de vida · Mascotas',
            'idiomas': 'Español',
            'precio': 'Gratuita, con versión Pro de pago único',
            'corta': 'El cuidado de tu mascota, siempre al día, sin depender de tu memoria.',
            'media': 'PituApp convierte el cuidado de una mascota en un plan que se recalcula solo: '
                     'vacunas, desparasitaciones, visitas y peso, con recordatorios y un reporte '
                     'veterinario en PDF. Todo se guarda en el dispositivo, sin cuenta ni servidor.',
            'larga': 'Quien cuida un animal lleva las fechas en la cabeza o en un cuaderno: la '
                     'desparasitación cada cuatro meses, la vacuna anual, el control de peso mensual. '
                     'PituApp lo convierte en un plan de cuidados que se recalcula cada vez que se '
                     'marca algo como hecho y avisa antes de que venza. Lo que la separa de una lista '
                     'de tareas es el historial clínico: visitas médicas, vacunas con su próxima '
                     'dosis autosugerida, diagnósticos con estado y registro de peso con aviso '
                     'informativo cuando la variación supera el 10 %. Todo se exporta a un reporte '
                     'veterinario en PDF listo para la consulta. No hay cuenta de usuario ni '
                     'servidor: los datos viven en el teléfono y se llevan con el respaldo en JSON.',
        },
        'soporte': {
            'intro': 'Escríbenos y te respondemos en menos de dos días hábiles. '
                     'Si es un problema con recordatorios, dinos qué sistema operativo y qué '
                     'versión usas: casi siempre es un permiso del sistema.',
            'faq': [
                ('No me llegan los recordatorios.',
                 'Revisa que las notificaciones estén permitidas para PituApp en los ajustes del '
                 'sistema. En Android, además, hay que permitir las alarmas exactas; algunos '
                 'fabricantes las restringen con sus ahorradores de batería.'),
                ('¿Cómo hago una copia de seguridad?',
                 'En Ajustes → Datos → Crear respaldo. Genera un archivo JSON con todo el '
                 'historial y los documentos adjuntos. <strong>Hazlo con regularidad</strong>: '
                 'PituApp no tiene servidor, así que un dispositivo perdido es un historial '
                 'perdido.'),
                ('Cambié de teléfono, ¿cómo paso mis datos?',
                 'Crea un respaldo en el teléfono viejo, pásalo al nuevo y usa Ajustes → Datos → '
                 'Restaurar. Puedes elegir entre reemplazar todo o combinar con lo que ya haya.'),
                ('Compré la versión Pro y no aparece.',
                 'Usa el botón de restaurar compras en Ajustes. Si sigue sin aparecer, escríbenos '
                 'con el correo de la cuenta con la que compraste.'),
                ('¿Cómo genero el reporte para el veterinario?',
                 'Desde la ficha de la mascota, en el menú de opciones: puedes elegir el historial '
                 'completo, solo las vacunas o un rango de fechas.'),
                ('La app me avisó de una variación de peso, ¿debo preocuparme?',
                 'Es un aviso informativo cuando la variación supera el 10 %, no un diagnóstico. '
                 'Coméntalo con tu veterinario.'),
            ],
        },
        'legal': {
            'trata_datos_personales': True,
            'trata_sensibles': False,
            'tiene_cuenta': False,
            'tiene_compras': True,
            'tiene_publicidad': False,
            'edad_minima': None,
            'datos': [
                ('Datos de tus mascotas', 'Nombre, especie, raza, fecha de nacimiento, peso, fotos, vacunas, visitas médicas, diagnósticos y documentos adjuntos.', 'Construir el plan de cuidados, calcular las próximas fechas y generar el reporte veterinario.', 'No sale del dispositivo'),
                ('Nombre del perfil', 'El nombre con el que quieres que te salude la app y que aparece en el reporte.', 'Personalizar la app y encabezar el PDF.', 'No sale del dispositivo'),
                ('Estado de la compra', 'Si has adquirido la versión Pro.', 'Desbloquear las funciones de pago.', 'Lo gestiona la tienda'),
            ],
            'permisos': [
                ('Notificaciones', 'Avisarte de los cuidados del día y de los que ya vencieron. Puedes desactivarlo.'),
                ('Cámara y galería', 'Solo si adjuntas la foto de tu mascota o el documento de una visita. Las imágenes se comprimen y se guardan dentro de la app.'),
                ('Biometría (huella o rostro)', 'Bloquear el acceso a la app, si activas esa opción. La verificación la hace el sistema operativo.'),
                ('Almacenamiento / archivos', 'Guardar los reportes en PDF y las copias de seguridad que exportas.'),
            ],
            'almacenamiento': 'Todo se guarda únicamente en tu dispositivo. <strong>PituApp no tiene '
                              'servidor</strong>: no hay cuenta de usuario, no hay copia en la nube y tus '
                              'datos no viajan a ninguna parte. Si desinstalas la app sin exportar un '
                              'respaldo, la información se pierde con ella.',
            'terceros': [
                ('Google Play / App Store', 'Distribuir la aplicación y procesar la compra de la versión Pro.'),
            ],
            'descargo_titulo': 'PituApp no reemplaza al veterinario',
            'descargo': 'PituApp organiza el plan de cuidados y el historial de tu mascota. Los avisos que '
                        'genera —incluido el de variación de peso superior al 10 %— son '
                        '<strong>informativos y no constituyen un diagnóstico veterinario</strong>. Las '
                        'frecuencias del catálogo de cuidados son orientaciones generales por especie: el '
                        'plan real de vacunación y desparasitación de tu animal lo define su veterinario, '
                        'y puede variar según su edad, su estado de salud y la normativa de tu país.',
            'reglas_uso': [
                'Los recordatorios dependen de que el sistema operativo permita las notificaciones. No los uses como única garantía de que un cuidado se va a cumplir a tiempo.',
                'Exporta un respaldo con regularidad: al no haber servidor, un dispositivo perdido significa un historial perdido.',
            ],
        },
    },
]

# ===========================================================================
# PLANTILLAS
# ===========================================================================

def esc(t):
    return t

def cabecera(prof, titulo, descripcion, canonical, nav_actual, noindex=False,
             og='iron-coding'):
    """prof = profundidad respecto de web/ (1 = proyectos/, 2 = proyectos/slug/).

    og = nombre del PNG en img/og/ que se muestra al compartir el enlace.
    Tiene que ser absoluto: los rastreadores de redes no resuelven rutas
    relativas.
    """
    r = '../' * prof
    proy_href = 'index.html' if prof == 1 else '../index.html'
    act = lambda k: ' aria-current="page"' if nav_actual == k else ''
    meta_noindex = '\n<meta name="robots" content="noindex, nofollow">' if noindex else ''
    og_url = f'https://iron-coding.art/img/og/{og}.png'
    return f'''<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<meta name="theme-color" content="#0a0a0c">{meta_noindex}
<link rel="canonical" href="https://iron-coding.art/{canonical}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Iron-Coding">
<meta property="og:locale" content="es_ES">
<meta property="og:url" content="https://iron-coding.art/{canonical}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_url}">

<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}img/apple-touch-icon.png">

<link rel="preload" href="{r}fonts/jetbrains-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}css/base.css">
<link rel="stylesheet" href="{r}css/pages.css">

<script>document.documentElement.className='js';setTimeout(function(){{document.documentElement.classList.add('sin-revelado')}},3000);</script>
</head>
<body>

<a class="skip-link" href="#contenido">saltar_al_contenido()</a>

<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="{r}index.html" aria-label="Iron-Coding, inicio">&lt;Iron<span class="tag">-Coding</span>/&gt;</a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu">
      <span class="nav-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
      <span class="nav-toggle__label">menu()</span>
    </button>

    <nav aria-label="Principal">
      <ul class="navlinks" id="nav-menu">
        <li><a href="{proy_href}"{act('proyectos')}>Proyectos</a></li>
        <li><a href="{r}pages/blog.html"{act('blog')}>Blog</a></li>
        <li><a href="{r}pages/nosotros.html"{act('nosotros')}>Nosotros</a></li>
        <li><a href="{r}pages/contacto.html"{act('contacto')}>Contacto</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="contenido">
'''


def pie(prof):
    r = '../' * prof
    proy_href = 'index.html' if prof == 1 else '../index.html'
    return f'''
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__top">
      <a class="brand" href="{r}index.html">&lt;Iron<span class="tag">-Coding</span>/&gt;</a>
      <nav class="site-footer__links" aria-label="Pie de página">
        <a href="{proy_href}">Proyectos</a>
        <a href="{r}pages/blog.html">Blog</a>
        <a href="{r}pages/nosotros.html">Nosotros</a>
        <a href="{r}pages/contacto.html">Contacto</a>
        <a href="{r}pages/privacidad.html">Privacidad</a>
        <a href="{r}pages/terminos.html">Términos</a>
      </nav>
      <!-- PENDIENTE: reemplazar por los perfiles reales de Iron-Coding -->
      <div class="site-footer__social">
        <a href="https://www.linkedin.com/company/iron-coding" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
        <a href="https://github.com/iron-coding" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
        <a href="https://www.instagram.com/ironcoding" target="_blank" rel="noopener noreferrer">Instagram ↗</a>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>© <span data-year>2026</span> Iron-Coding</span>
      <span class="site-footer__loop">for (año = 2026; activo; año++)</span>
      <span>iron-coding.art</span>
    </div>
  </div>
</footer>

<script src="{r}js/main.js" defer></script>

</body>
</html>
'''


def migas(prof, *tramos):
    """tramos = (texto, href|None)"""
    r = '../' * prof
    partes = [f'<a href="{r}index.html">inicio</a>']
    for texto, href in tramos:
        partes.append(f'<a href="{href}">{texto}</a>' if href else texto)
    return '  <div class="wrap">\n    <p class="crumbs">' + '<span>/</span>'.join(partes) + '</p>\n  </div>\n'


# --------------------------------------------------------------------------
# Ficha del producto
# --------------------------------------------------------------------------

def pagina_producto(p, i):
    slug = p['slug']
    prof = 2
    insignia = '\n      <p class="proyecto__flag">producto insignia</p>' if p['insignia'] else ''

    parrafos = '\n'.join(f'        <p>{t}</p>' for t in p['parrafos'])
    features = '\n'.join(
        f'          <li><strong>{a}</strong> {b}</li>' for a, b in p['features'])
    ficha = '\n'.join(
        f'            <dt>{k}</dt>\n            <dd>{v}</dd>' for k, v in p['ficha'])

    acciones = []
    if p['demo']:
        url, etiqueta = p['demo']
        acciones.append(f'<a class="cta cta--primary" href="{url}" target="_blank" rel="noopener noreferrer">{etiqueta}</a>')
    if p.get('lista_espera'):
        acciones.append('<a class="cta" href="#lista-espera">avisarme()</a>')
    acciones.append('<a class="cta" href="soporte.html">soporte()</a>')
    acciones.append('<a class="cta" href="prensa.html">prensa()</a>')
    bloque_acciones = '\n          '.join(acciones)

    # Bloque de lista de espera: solo mientras la app no este publicada.
    # Es la conversion principal de una ficha de producto sin lanzar.
    lista = ''
    if p.get('lista_espera'):
        lista = f'''
  <section class="section wrap" id="lista-espera" aria-labelledby="titulo-lista-{slug}">
    <p class="eyebrow">// todavía no está publicada</p>
    <h2 class="section__title" id="titulo-lista-{slug}">Te avisamos el día que salga.</h2>

    <div class="lista-espera">
      <div class="resultado resultado--ok" id="resultado-ok" hidden role="status">
        <strong>listo()</strong>
        <p>Te escribiremos a ese correo cuando {p['nombre']} esté disponible. Nada más.</p>
      </div>
      <div class="resultado resultado--error" id="resultado-error" hidden role="alert">
        <strong>error()</strong>
        <p>No pudimos registrar tu correo. Inténtalo de nuevo o escríbenos a
           <a href="mailto:contacto@iron-coding.art">contacto@iron-coding.art</a>.</p>
      </div>

      <form class="form form--lista" action="../../suscribir.php" method="post" novalidate>
        <input type="hidden" name="app" value="{slug}">

        <div class="campo" id="campo-correo">
          <label for="correo">tu correo</label>
          <input type="email" id="correo" name="correo" required maxlength="180"
                 autocomplete="email" placeholder="donde te avisamos"
                 aria-describedby="error-correo">
          <p class="campo__error" id="error-correo"></p>
        </div>

        <div class="campo" id="campo-acepto">
          <div class="consentimiento">
            <input type="checkbox" id="acepto" name="acepto" value="si" required
                   aria-describedby="error-acepto">
            <label for="acepto">
              Autorizo a Iron-Coding a guardar mi correo con el único fin de avisarme del
              lanzamiento de esta aplicación, conforme a la
              <a href="../../pages/privacidad.html">política de privacidad</a>.
            </label>
          </div>
          <p class="campo__error" id="error-acepto"></p>
        </div>

        <div class="trampa" aria-hidden="true">
          <label for="pagina-web">No rellenar este campo</label>
          <input type="text" id="pagina-web" name="pagina_web" tabindex="-1" autocomplete="off">
        </div>

        <div>
          <button type="submit" class="cta cta--primary">avisarme()</button>
        </div>
      </form>

      <p class="lista-espera__nota">
        Un solo correo, el del lanzamiento. Ni boletines ni reenvíos a terceros: puedes pedir
        que te borremos cuando quieras escribiendo a
        <a href="mailto:privacidad@iron-coding.art">privacidad@iron-coding.art</a>.
      </p>
    </div>
  </section>
'''

    galeria = '\n'.join(f'''        <figure data-revelar>
          <img src="../../img/showcase/{img}" alt="{alt}" width="720" height="{h}" loading="lazy" decoding="async">
          <figcaption>{cap}</figcaption>
        </figure>''' for img, h, alt, cap in p['galeria'])

    cuerpo = f'''
{migas(prof, ('proyectos', '../index.html'), (p['nombre'], None))}
  <article class="proyecto wrap" style="border-top:0">
    <div class="proyecto__head">
      <p class="proyecto__index">proyectos[{i}]</p>{insignia}
    </div>
    <h1 class="proyecto__titulo">{p['nombre']}</h1>
    <p class="proyecto__tagline">{p['tagline']}</p>

    <div class="proyecto__grid">
      <div class="proyecto__texto">
{parrafos}

        <ul class="proyecto__features">
{features}
        </ul>

        <div class="ficha">
          <dl>
{ficha}
          </dl>
        </div>

        <div class="proyecto__acciones">
          {bloque_acciones}
        </div>
      </div>

      <div class="galeria">
{galeria}
      </div>
    </div>
  </article>
{lista}
  <section class="section wrap" aria-labelledby="otros-{slug}">
    <p class="eyebrow">// seguir mirando</p>
    <h2 class="section__title" id="otros-{slug}">El resto del portafolio.</h2>
    <a class="cta cta--primary" href="../index.html">ver_proyectos()</a>
  </section>
'''
    return (cabecera(prof, f"{p['nombre']} — Iron-Coding", p['resumen_corto'],
                     f'proyectos/{slug}/', 'proyectos', og=slug)
            + cuerpo + pie(prof)).replace(
        '<script src="../../js/main.js" defer></script>',
        '<script src="../../js/main.js" defer></script>\n<script src="../../js/formularios.js" defer></script>'
        if p.get('lista_espera') else '<script src="../../js/main.js" defer></script>')


# --------------------------------------------------------------------------
# Press kit de la app
# --------------------------------------------------------------------------

def pagina_prensa(p):
    slug, nombre, R = p['slug'], p['nombre'], p['prensa']
    prof = 2

    capturas = '\n'.join(f'''        <figure data-revelar>
          <img src="../../img/showcase/{img}" alt="{alt}" width="720" height="{h}" loading="lazy" decoding="async">
          <figcaption><a href="../../img/showcase/{img}" download>{cap} ↓</a></figcaption>
        </figure>''' for img, h, alt, cap in p['galeria'])

    demo = ''
    if p['demo']:
        url, _ = p['demo']
        demo = f'''
            <dt>Demo jugable</dt>
            <dd><a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a></dd>'''

    cuerpo = f'''
{migas(prof, ('proyectos', '../index.html'), (nombre, 'index.html'), ('prensa', None))}
  <section class="page-hero wrap">
    <p class="eyebrow">// press kit · {slug}</p>
    <h1>Prensa — {nombre}</h1>
    <p class="page-hero__lead">
      Todo lo que necesitas para escribir sobre {nombre}: descripciones listas para copiar,
      ficha técnica, capturas en alta y contacto directo. Puedes usar este material
      libremente en artículos, reseñas y publicaciones sobre la aplicación.
    </p>
  </section>

  <section class="section wrap">
    <div class="prose">

      <h2 id="descripciones">Descripciones</h2>
      <p>Tres versiones, según el espacio del que dispongas. Se pueden usar tal cual.</p>

      <h3>Una línea</h3>
      <div class="cita-copiable"><p>{R['corta']}</p></div>

      <h3>Párrafo corto</h3>
      <div class="cita-copiable"><p>{R['media']}</p></div>

      <h3>Descripción completa</h3>
      <div class="cita-copiable"><p>{R['larga']}</p></div>

      <h2 id="ficha">Ficha técnica</h2>
      <div class="tabla-wrap">
        <table>
          <caption class="sr-only">Ficha técnica de {nombre}</caption>
          <tbody>
            <tr><th scope="row">Nombre</th><td>{p['marca_tienda']}</td></tr>
            <tr><th scope="row">Desarrollador</th><td>Iron-Coding — <span class="pendiente">[RAZÓN SOCIAL]</span></td></tr>
            <tr><th scope="row">Categoría</th><td>{R['categoria']}</td></tr>
            <tr><th scope="row">Plataformas</th><td>{p['ficha'][1][1]}</td></tr>
            <tr><th scope="row">Idiomas</th><td>{R['idiomas']}</td></tr>
            <tr><th scope="row">Precio</th><td>{R['precio']}</td></tr>
            <tr><th scope="row">Estado</th><td>{p['ficha'][0][1]}</td></tr>
            <tr><th scope="row">Fecha de lanzamiento</th><td><span class="pendiente">[POR DEFINIR]</span></td></tr>
            <tr><th scope="row">Sitio</th><td><a href="index.html">iron-coding.art/proyectos/{slug}/</a></td></tr>
          </tbody>
        </table>
      </div>

      <h2 id="capturas">Capturas</h2>
      <p>
        En formato WebP, 720 px de ancho. Si necesitas otra resolución u otro formato,
        pídenoslas y te las mandamos.
      </p>
    </div>

    <div class="galeria galeria--prensa">
{capturas}
    </div>

    <div class="prose" style="margin-top:56px">
      <h2 id="marca">Marca</h2>
      <p>
        El logotipo es la etiqueta autocontenida <code>&lt;Iron-Coding/&gt;</code> y debe usarse
        siempre completa, sin recortar los signos ni alterar sus colores.
      </p>
      <ul>
        <li><a href="../../favicon.svg" download>Isotipo en SVG</a> — vectorial, escala sin perder calidad.</li>
        <li><a href="../../img/apple-touch-icon.png" download>Icono en PNG</a> — 180 × 180 px.</li>
        <li><a href="../../img/og/{slug}.png" download>Imagen de portada</a> — 1200 × 630 px.</li>
      </ul>
      <p>
        Colores de marca: negro de forja <code>#0A0A0C</code>, rojo <code>#C1272D</code>,
        violeta <code>#8B5CF6</code> y blanco cálido <code>#F2F0EC</code>.
      </p>

      <h2 id="contacto-prensa">Contacto de prensa</h2>
      <dl class="datos-prensa">
        <dt>Correo</dt>
        <dd><a href="mailto:prensa@iron-coding.art">prensa@iron-coding.art</a></dd>
        <dt>Tiempo de respuesta</dt>
        <dd>Menos de dos días hábiles</dd>
        <dt>Idiomas</dt>
        <dd>Español e inglés</dd>{demo}
      </dl>
      <p>
        ¿Necesitas una entrevista, una versión de prueba anticipada o material que no esté
        aquí? Escríbenos y lo preparamos.
      </p>
    </div>
  </section>
'''
    return (cabecera(prof, f'Prensa — {nombre} — Iron-Coding',
                     f'Press kit de {nombre}: descripciones, ficha técnica, capturas y contacto de prensa.',
                     f'proyectos/{slug}/prensa.html', 'proyectos', og=slug)
            + cuerpo + pie(prof))


# --------------------------------------------------------------------------
# Soporte de la app — Apple lo exige para poder publicar
# --------------------------------------------------------------------------

def pagina_soporte(p):
    slug, nombre, S = p['slug'], p['nombre'], p['soporte']
    prof = 2

    faq = '\n'.join(f'''      <h2 id="p{i}">{q}</h2>
      <p>{a}</p>''' for i, (q, a) in enumerate(S['faq'], 1))

    indice = '\n'.join(f'          <li><a href="#p{i}">{q}</a></li>'
                       for i, (q, _) in enumerate(S['faq'], 1))

    cuerpo = f'''
{migas(prof, ('proyectos', '../index.html'), (nombre, 'index.html'), ('soporte', None))}
  <section class="page-hero wrap">
    <p class="eyebrow">// soporte · {slug}</p>
    <h1>Soporte de {nombre}</h1>
    <p class="page-hero__lead">{S['intro']}</p>
  </section>

  <section class="section wrap">
    <div class="contacto-grid">
      <div class="prose">
        <div class="toc">
          <p>// preguntas frecuentes</p>
          <ol>
{indice}
          </ol>
        </div>

{faq}

        <h2 id="mas">¿No está tu pregunta aquí?</h2>
        <p>
          Escríbenos a <a href="mailto:soporte@iron-coding.art">soporte@iron-coding.art</a> o
          usa el <a href="../../pages/contacto.html">formulario de contacto</a>. Respondemos en
          menos de dos días hábiles, en español o en inglés.
        </p>
      </div>

      <aside class="contacto-info">
        <h2>contacto_directo()</h2>
        <dl>
          <div>
            <dt>Soporte de {nombre}</dt>
            <dd><a href="mailto:soporte@iron-coding.art">soporte@iron-coding.art</a></dd>
          </div>
          <div>
            <dt>Tiempo de respuesta</dt>
            <dd>Menos de dos días hábiles</dd>
          </div>
          <div>
            <dt>Idiomas</dt>
            <dd>Español e inglés</dd>
          </div>
          <div>
            <dt>Privacidad y datos</dt>
            <dd><a href="mailto:privacidad@iron-coding.art">privacidad@iron-coding.art</a></dd>
          </div>
          <div>
            <dt>Documentos</dt>
            <dd>
              <a href="privacidad.html">Privacidad</a> ·
              <a href="terminos.html">Términos</a>
            </dd>
          </div>
        </dl>
      </aside>
    </div>
  </section>
'''
    return (cabecera(prof, f'Soporte de {nombre} — Iron-Coding',
                     f'Ayuda, preguntas frecuentes y contacto de soporte de la aplicación {nombre}.',
                     f'proyectos/{slug}/soporte.html', 'proyectos', og=slug)
            + cuerpo + pie(prof))


# --------------------------------------------------------------------------
# Privacidad de la app
# --------------------------------------------------------------------------

def pagina_privacidad(p):
    slug, nombre, L = p['slug'], p['nombre'], p['legal']
    prof = 2

    filas_datos = '\n'.join(f'''            <tr>
              <th scope="row">{cat}</th>
              <td>{ej}</td>
              <td>{fin}</td>
              <td>{obl}</td>
            </tr>''' for cat, ej, fin, obl in L['datos'])

    permisos = '\n'.join(
        f'        <li><strong>{k}</strong> — {v}</li>' for k, v in L['permisos'])

    terceros = '\n'.join(f'''            <tr>
              <th scope="row">{k}</th>
              <td>{v}</td>
            </tr>''' for k, v in L['terceros'])

    sensibles = ''
    if L['trata_sensibles']:
        sensibles = f'''
      <h2 id="sensibles">5. Datos sensibles</h2>
      <p>
        {nombre} trata <strong>datos relacionados con la salud</strong>, que la legislación
        colombiana clasifica como datos sensibles y que en el RGPD son categorías especiales.
        Por eso:
      </p>
      <ul>
        <li>Su registro es siempre voluntario: la app te pide autorización expresa y separada antes del primer registro.</li>
        <li>Se usan exclusivamente para mostrarte tu propia información y su evolución.</li>
        <li><strong>No se comparten con aseguradoras, empleadores, anunciantes ni intermediarios de datos.</strong></li>
        <li>Puedes eliminarlos desde la propia aplicación en cualquier momento.</li>
        <li>No estás obligado a autorizar su tratamiento; si no lo haces, la app no puede prestar su función principal.</li>
      </ul>
'''

    compras = ''
    if L['tiene_compras']:
        compras = '''
      <h3>Compras dentro de la aplicación</h3>
      <p>
        Las compras las procesan Google Play y la App Store. <strong>Iron-Coding no recibe ni
        almacena los datos de tu tarjeta.</strong> Solo recibimos de la tienda la confirmación
        de que la compra existe, para desbloquear las funciones correspondientes.
      </p>
'''

    en_desarrollo = ''
    if L.get('en_desarrollo'):
        en_desarrollo = '''
      <div class="aviso">
        <p>
          <strong>Esta aplicación está en desarrollo.</strong> El detalle de los datos tratados
          corresponde al diseño funcional aprobado y debe confirmarse contra la implementación
          final antes de declararlo en la ficha de la tienda.
        </p>
      </div>
'''

    edad = L['edad_minima'] or '<span class="pendiente">[EDAD]</span>'

    n = 5 if not L['trata_sensibles'] else 6  # numeración a partir de sensibles

    cuerpo = f'''
{migas(prof, ('proyectos', '../index.html'), (nombre, 'index.html'), ('privacidad', None))}
  <section class="page-hero wrap">
    <p class="eyebrow">// legal · {slug}</p>
    <h1>Privacidad de {nombre}</h1>
    <p class="page-hero__lead">
      Cómo trata los datos personales la aplicación <strong>{p['marca_tienda']}</strong>.
      Este documento se refiere <strong>solo a esta aplicación</strong>; el sitio web y la
      empresa se rigen por la <a href="../../pages/privacidad.html">política general de Iron-Coding</a>.
    </p>
  </section>

  <section class="section wrap">
    <div class="prose">

      <p class="prose__updated">Última actualización: <span class="pendiente">[FECHA DE PUBLICACIÓN]</span></p>

      <div class="aviso">
        <p>
          <strong>Borrador de trabajo.</strong> Antes de declarar esta URL como política de
          privacidad en Google Play Console o App Store Connect, tiene que revisarla un
          profesional en protección de datos y hay que reemplazar los campos marcados en amarillo.
        </p>
        <p>
          Lo declarado aquí debe coincidir exactamente con la sección <em>Seguridad de los datos</em>
          de la ficha de Google Play y con las <em>App Privacy Details</em> de App Store Connect.
        </p>
      </div>
{en_desarrollo}
      <h2 id="responsable">1. Quién responde por tus datos</h2>
      <p>
        El responsable del tratamiento es <span class="pendiente">[RAZÓN SOCIAL COMPLETA]</span>,
        NIT <span class="pendiente">[NIT]</span>, con domicilio en
        <span class="pendiente">[DIRECCIÓN, CIUDAD, PAÍS]</span>, que opera bajo la marca
        <strong>Iron-Coding</strong>.
      </p>
      <p>
        Para cualquier asunto sobre tus datos en esta aplicación escribe a
        <a href="mailto:privacidad@iron-coding.art">privacidad@iron-coding.art</a> indicando
        que se trata de <strong>{nombre}</strong>.
      </p>

      <h2 id="datos">2. Qué datos trata la aplicación</h2>
      <div class="tabla-wrap">
        <table>
          <caption class="sr-only">Datos que trata {nombre}</caption>
          <thead>
            <tr>
              <th scope="col">Categoría</th>
              <th scope="col">Qué incluye</th>
              <th scope="col">Para qué</th>
              <th scope="col">¿Obligatorio?</th>
            </tr>
          </thead>
          <tbody>
{filas_datos}
          </tbody>
        </table>
      </div>
      <p>
        <strong>No vendemos datos personales</strong>, no los usamos para publicidad y no
        construimos perfiles comerciales con ellos.
      </p>

      <h2 id="permisos">3. Permisos del dispositivo</h2>
      <p>Cada permiso se pide en el momento en que activas la función que lo necesita, y puedes revocarlo desde los ajustes del sistema:</p>
      <ul>
{permisos}
      </ul>

      <h2 id="almacenamiento">4. Dónde se guardan</h2>
      <p>{L['almacenamiento']}</p>
{sensibles}
      <h2 id="terceros">{n}. Con quién se comparten</h2>
      <div class="tabla-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Proveedor</th>
              <th scope="col">Para qué</th>
            </tr>
          </thead>
          <tbody>
{terceros}
          </tbody>
        </table>
      </div>
      <p>
        También podemos entregar información cuando una autoridad competente lo exija por ley.
        Algunos proveedores están fuera de Colombia; al aceptar esta política autorizas esa
        transferencia internacional.
      </p>
{compras}
      <h2 id="conservacion">{n + 1}. Cuánto tiempo se guardan</h2>
      <p>
        Los datos que viven en tu dispositivo permanecen mientras tengas la aplicación instalada;
        al desinstalarla se eliminan con ella. Los datos sincronizados en nuestros servidores, si
        los hay, se conservan mientras la cuenta esté activa y hasta
        <span class="pendiente">[X DÍAS]</span> después de que pidas eliminarla.
      </p>

      <h2 id="derechos">{n + 2}. Tus derechos</h2>
      <p>
        Puedes conocer, actualizar, rectificar y suprimir tus datos, revocar la autorización,
        solicitar prueba de ella y obtener una copia en formato legible por máquina, conforme a la
        <strong>Ley 1581 de 2012</strong> de Colombia y, si resides en el EEE o el Reino Unido, al RGPD.
      </p>
      <p>
        La forma más rápida de ejercerlos es desde la propia aplicación: borrar un registro o
        desinstalarla elimina los datos locales. Para los demás casos escribe a
        <a href="mailto:privacidad@iron-coding.art">privacidad@iron-coding.art</a>. Respondemos las
        consultas en un máximo de diez días hábiles y los reclamos en quince.
      </p>
      <p>
        Si consideras que incumplimos la ley, puedes presentar una queja ante la Superintendencia
        de Industria y Comercio de Colombia.
      </p>

      <h2 id="menores">{n + 3}. Menores de edad</h2>
      <p>
        Esta aplicación no está dirigida a menores de {edad} años y no recogemos deliberadamente
        sus datos. Si eres madre, padre o tutor y crees que un menor a tu cargo nos ha facilitado
        información, escríbenos y la eliminaremos.
      </p>

      <h2 id="seguridad">{n + 4}. Seguridad</h2>
      <p>
        Aplicamos cifrado en tránsito, acceso restringido a la información y el principio de
        minimización: no pedimos datos que no necesitemos para prestar la función. Ningún sistema
        es infalible; si ocurriera un incidente que afecte tus datos, te lo comunicaremos y lo
        reportaremos a la autoridad competente en los plazos que exige la ley.
      </p>

      <h2 id="cambios">{n + 5}. Cambios</h2>
      <p>
        Si cambiamos lo que la aplicación recoge, actualizaremos este documento y la ficha de la
        tienda antes de publicar la versión correspondiente. La fecha de la última actualización
        aparece al principio.
      </p>

      <h2 id="contacto">{n + 6}. Contacto</h2>
      <ul>
        <li><strong>Privacidad:</strong> <a href="mailto:privacidad@iron-coding.art">privacidad@iron-coding.art</a></li>
        <li><strong>Soporte de la aplicación:</strong> <a href="mailto:contacto@iron-coding.art">contacto@iron-coding.art</a></li>
        <li><strong>Términos de {nombre}:</strong> <a href="terminos.html">ver términos de uso</a></li>
        <li><strong>Política general del sitio:</strong> <a href="../../pages/privacidad.html">iron-coding.art/pages/privacidad.html</a></li>
      </ul>

    </div>
  </section>
'''
    return (cabecera(prof, f'Privacidad de {nombre} — Iron-Coding',
                     f'Política de privacidad de la aplicación {nombre} de Iron-Coding.',
                     f'proyectos/{slug}/privacidad.html', 'proyectos', og=slug)
            + cuerpo + pie(prof))


# --------------------------------------------------------------------------
# Términos de la app
# --------------------------------------------------------------------------

def pagina_terminos(p):
    slug, nombre, L = p['slug'], p['nombre'], p['legal']
    prof = 2

    reglas = '\n'.join(f'        <li>{t}</li>' for t in L['reglas_uso'])

    cuenta = ''
    if L['tiene_cuenta']:
        cuenta = '''
      <h2 id="cuenta">4. Tu cuenta</h2>
      <p>
        Para sincronizar tu información necesitas una cuenta. Eres responsable de la veracidad de
        los datos que registres y de mantener tus credenciales en secreto. Avísanos de inmediato
        si detectas un uso no autorizado. Puedes cerrar la cuenta desde la propia aplicación o
        escribiéndonos.
      </p>
'''
    else:
        cuenta = '''
      <h2 id="cuenta">4. Sin cuenta de usuario</h2>
      <p>
        Esta aplicación no requiere registro. Todo funciona en tu dispositivo, lo que también
        significa que <strong>no podemos recuperar tu información si pierdes el dispositivo</strong>
        o desinstalas la aplicación sin exportar un respaldo.
      </p>
'''

    compras = ''
    if L['tiene_compras']:
        compras = '''
      <h2 id="compras">7. Compras dentro de la aplicación</h2>
      <p>
        Algunas funciones son de pago. Las transacciones las procesan <strong>Google Play</strong>
        y la <strong>App Store</strong>, no nosotros: nunca recibimos ni almacenamos los datos de
        tu medio de pago.
      </p>
      <p>
        Las devoluciones se rigen por la política de la tienda donde compraste. Si una compra no se
        refleja en la aplicación, usa la opción de restaurar compras o escríbenos. Los precios
        pueden cambiar, pero un cambio de precio nunca afecta a una compra ya realizada.
      </p>
'''

    cuerpo = f'''
{migas(prof, ('proyectos', '../index.html'), (nombre, 'index.html'), ('términos', None))}
  <section class="page-hero wrap">
    <p class="eyebrow">// legal · {slug}</p>
    <h1>Términos de {nombre}</h1>
    <p class="page-hero__lead">
      Condiciones de uso de la aplicación <strong>{p['marca_tienda']}</strong>.
      Este documento se refiere <strong>solo a esta aplicación</strong>; el sitio web y la empresa
      se rigen por los <a href="../../pages/terminos.html">términos generales de Iron-Coding</a>.
    </p>
  </section>

  <section class="section wrap">
    <div class="prose">

      <p class="prose__updated">Última actualización: <span class="pendiente">[FECHA DE PUBLICACIÓN]</span></p>

      <div class="aviso">
        <p>
          <strong>Borrador de trabajo.</strong> Debe revisarlo un abogado y hay que reemplazar los
          campos marcados en amarillo antes de publicarlo. Las cláusulas de limitación de
          responsabilidad y de jurisdicción tienen efectos legales reales.
        </p>
      </div>

      <h2 id="aceptacion">1. Aceptación</h2>
      <p>
        Al instalar o usar {nombre} aceptas estos términos. Si no estás de acuerdo con alguno, no
        uses la aplicación.
      </p>

      <h2 id="quienes">2. Quién presta el servicio</h2>
      <p>
        {nombre} es una aplicación de <span class="pendiente">[RAZÓN SOCIAL COMPLETA]</span>,
        NIT <span class="pendiente">[NIT]</span>, con domicilio en
        <span class="pendiente">[DIRECCIÓN, CIUDAD, PAÍS]</span>, que opera bajo la marca
        <strong>Iron-Coding</strong>.
      </p>

      <h2 id="licencia">3. Licencia de uso</h2>
      <p>
        Te concedemos una licencia personal, limitada, revocable y no transferible para usar la
        aplicación con fines lícitos. No puedes copiarla, modificarla, descompilarla, aplicarle
        ingeniería inversa —salvo en la medida en que la ley lo permita expresamente—, revenderla,
        sublicenciarla ni suprimir sus avisos de propiedad intelectual.
      </p>
{cuenta}
      <h2 id="contenido">5. Tu contenido</h2>
      <p>
        <strong>Lo que registras en la aplicación es tuyo.</strong> No reclamamos propiedad sobre
        ello. Nos concedes únicamente la licencia técnica mínima necesaria para almacenarlo,
        procesarlo y mostrártelo, y para sincronizarlo entre tus dispositivos si activas esa
        función. Esa licencia termina cuando eliminas el contenido o dejas de usar la aplicación.
      </p>
      <p>
        La aplicación incluye funciones de exportación para que puedas llevarte tu información
        cuando quieras.
      </p>

      <h2 id="naturaleza">6. {L['descargo_titulo']}</h2>
      <div class="aviso">
        <p>{L['descargo']}</p>
      </div>
      <p>Además, al usar la aplicación aceptas que:</p>
      <ul>
{reglas}
      </ul>
{compras}
      <h2 id="disponibilidad">8. Disponibilidad y cambios</h2>
      <p>
        Hacemos lo razonable por mantener la aplicación funcionando, pero no garantizamos
        funcionamiento ininterrumpido ni libre de errores. Podemos modificar, suspender o
        descontinuar funciones; si retiramos una función importante o la aplicación completa,
        avisaremos con antelación razonable y, cuando aplique, ofreceremos una forma de exportar tu
        información.
      </p>
      <p>
        Las versiones identificadas como <em>beta</em>, <em>demo</em> o <em>en desarrollo</em> se
        ofrecen para evaluación: pueden contener errores, cambiar sin previo aviso y perder datos.
      </p>

      <h2 id="garantias">9. Ausencia de garantías</h2>
      <p>
        La aplicación se ofrece <strong>«tal cual» y «según disponibilidad»</strong>. En la medida
        en que la ley lo permita, no otorgamos garantías de comerciabilidad, idoneidad para un fin
        determinado, exactitud de los resultados o ausencia de errores. Esto no limita los derechos
        que la legislación de protección al consumidor te reconozca de forma imperativa en tu país
        de residencia.
      </p>

      <h2 id="responsabilidad">10. Limitación de responsabilidad</h2>
      <p>
        En la medida máxima permitida por la ley, Iron-Coding no responderá por daños indirectos,
        incidentales o consecuenciales, ni por lucro cesante o pérdida de datos derivados del uso o
        la imposibilidad de uso de la aplicación.
      </p>
      <p>
        Nuestra responsabilidad total acumulada se limita al mayor de estos dos valores: el importe
        que hayas pagado por la aplicación en los doce meses anteriores al hecho, o
        <span class="pendiente">[IMPORTE MÍNIMO Y MONEDA]</span>.
      </p>
      <p>
        Nada en estos términos excluye la responsabilidad por dolo, culpa grave o daños a la vida y
        la integridad de las personas.
      </p>

      <h2 id="terminacion">11. Terminación</h2>
      <p>
        Puedes dejar de usar la aplicación cuando quieras desinstalándola. Podemos suspender el
        acceso si incumples estos términos de forma grave o reiterada, o si la ley nos obliga. Al
        terminar siguen vigentes las secciones de propiedad intelectual, ausencia de garantías,
        limitación de responsabilidad y ley aplicable.
      </p>

      <h2 id="ley">12. Ley aplicable</h2>
      <p>
        Estos términos se rigen por las leyes de <span class="pendiente">[PAÍS]</span>. Cualquier
        controversia se someterá a los jueces de <span class="pendiente">[CIUDAD, PAÍS]</span>, sin
        perjuicio del fuero que corresponda de forma imperativa a las personas consumidoras en su
        lugar de residencia. Si una cláusula resultara inválida, las demás seguirán vigentes.
      </p>

      <h2 id="contacto">13. Contacto</h2>
      <ul>
        <li><strong>Soporte:</strong> <a href="mailto:contacto@iron-coding.art">contacto@iron-coding.art</a></li>
        <li><strong>Asuntos legales:</strong> <a href="mailto:legal@iron-coding.art">legal@iron-coding.art</a></li>
        <li><strong>Privacidad de {nombre}:</strong> <a href="privacidad.html">ver política de privacidad</a></li>
        <li><strong>Términos generales del sitio:</strong> <a href="../../pages/terminos.html">iron-coding.art/pages/terminos.html</a></li>
      </ul>

    </div>
  </section>
'''
    return (cabecera(prof, f'Términos de {nombre} — Iron-Coding',
                     f'Términos de uso de la aplicación {nombre} de Iron-Coding.',
                     f'proyectos/{slug}/terminos.html', 'proyectos', og=slug)
            + cuerpo + pie(prof))


# --------------------------------------------------------------------------
# Índice de proyectos
# --------------------------------------------------------------------------

def pagina_indice(proyectos):
    prof = 1
    tarjetas = []
    for i, p in enumerate(proyectos):
        img, h, alt, _ = p['galeria'][0]
        insignia = '<span class="chip chip--state">producto insignia</span>\n            ' if p['insignia'] else ''
        tarjetas.append(f'''      <article class="project" data-revelar>
        <div class="project__shot">
          <img src="../img/showcase/{img}" alt="{alt}" width="720" height="{h}" loading="lazy" decoding="async">
        </div>
        <div class="project__body">
          <p class="project__index">proyectos[{i}]</p>
          <h2 class="project__name"><a href="{p['slug']}/index.html">{p['nombre']}</a></h2>
          <p class="project__desc">{p['resumen_corto']}</p>
          <div class="project__meta">
            {insignia}<span class="chip">estado: {p['estado_chip']}</span>
          </div>
          <p class="project__more">ver_detalle() →</p>
        </div>
      </article>''')

    filas_legales = '\n'.join(f'''            <tr>
              <th scope="row"><a href="{p['slug']}/index.html">{p['nombre']}</a></th>
              <td><a href="{p['slug']}/privacidad.html">privacidad.html</a></td>
              <td><a href="{p['slug']}/terminos.html">terminos.html</a></td>
              <td><a href="{p['slug']}/soporte.html">soporte.html</a></td>
              <td><a href="{p['slug']}/prensa.html">prensa.html</a></td>
            </tr>''' for p in proyectos)

    cuerpo = f'''
{migas(prof, ('proyectos', None))}
  <section class="page-hero wrap">
    <p class="eyebrow">// showcase</p>
    <h1>proyectos[]</h1>
    <p class="page-hero__lead">
      Cada producto tiene su propia ficha y sus propios documentos legales, porque eso es lo
      que exigen Google Play y la App Store: una política de privacidad por aplicación, no una
      genérica de la empresa.
    </p>
  </section>

  <section class="section wrap" aria-labelledby="lista-proyectos">
    <h2 class="sr-only" id="lista-proyectos">Listado de proyectos</h2>
    <div class="projects projects--indice">
{chr(10).join(tarjetas)}
    </div>
  </section>

  <section class="section wrap" aria-labelledby="legal-proyectos">
    <p class="eyebrow">// legal por aplicación</p>
    <h2 class="section__title" id="legal-proyectos">Documentos que pide cada tienda.</h2>
    <p style="color:var(--muted); max-width:62ch; margin-bottom:28px;">
      Estas son las URL que se pegan en Google Play Console y App Store Connect. La de soporte
      es obligatoria en la App Store y tiene que ser una página real con un método de contacto:
      un placeholder es motivo de rechazo. Los documentos que cubren el sitio web y la empresa
      son otros: la
      <a href="../pages/privacidad.html" style="color:var(--red-glow)">política general</a> y los
      <a href="../pages/terminos.html" style="color:var(--red-glow)">términos generales</a>.
    </p>
    <div class="tabla-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Aplicación</th>
            <th scope="col">Privacidad</th>
            <th scope="col">Términos</th>
            <th scope="col">Soporte</th>
            <th scope="col">Prensa</th>
          </tr>
        </thead>
        <tbody>
{filas_legales}
        </tbody>
      </table>
    </div>
  </section>

  <section class="section wrap" aria-labelledby="cierre-indice">
    <p class="eyebrow">// siguiente</p>
    <h2 class="section__title" id="cierre-indice">¿Tu producto podría estar en esta lista?</h2>
    <a class="cta cta--primary" href="../pages/contacto.html">contactar()</a>
  </section>
'''
    return (cabecera(prof, 'Proyectos — Iron-Coding',
                     'Los productos de Iron-Coding, cada uno con su ficha y sus documentos legales.',
                     'proyectos/', 'proyectos')
            + cuerpo + pie(prof))


# ===========================================================================
# EJECUCIÓN
# ===========================================================================

def escribir(ruta, contenido, forzar, listar, creados, saltados):
    existe = os.path.exists(ruta)
    rel = os.path.relpath(ruta, os.path.dirname(RAIZ))
    if existe and not forzar:
        saltados.append(rel)
        return
    if listar:
        creados.append(rel + (' (SOBRESCRIBE)' if existe else ''))
        return
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    creados.append(rel + (' (sobrescrito)' if existe else ''))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--forzar', action='store_true',
                    help='regenera archivos existentes (PIERDE ediciones manuales)')
    ap.add_argument('--listar', action='store_true',
                    help='muestra qué haría, sin escribir nada')
    args = ap.parse_args()

    creados, saltados = [], []

    escribir(os.path.join(RAIZ, 'proyectos', 'index.html'),
             pagina_indice(PROYECTOS), args.forzar, args.listar, creados, saltados)

    for i, p in enumerate(PROYECTOS):
        base = os.path.join(RAIZ, 'proyectos', p['slug'])
        escribir(os.path.join(base, 'index.html'), pagina_producto(p, i),
                 args.forzar, args.listar, creados, saltados)
        escribir(os.path.join(base, 'privacidad.html'), pagina_privacidad(p),
                 args.forzar, args.listar, creados, saltados)
        escribir(os.path.join(base, 'terminos.html'), pagina_terminos(p),
                 args.forzar, args.listar, creados, saltados)
        escribir(os.path.join(base, 'soporte.html'), pagina_soporte(p),
                 args.forzar, args.listar, creados, saltados)
        escribir(os.path.join(base, 'prensa.html'), pagina_prensa(p),
                 args.forzar, args.listar, creados, saltados)

    verbo = 'Se crearían' if args.listar else 'Creados'
    print(f'{verbo} {len(creados)} archivo(s):')
    for c in creados:
        print('  +', c)
    if saltados:
        print(f'\nSin tocar {len(saltados)} archivo(s) que ya existen '
              f'(usa --forzar para regenerarlos):')
        for s in saltados:
            print('  =', s)
    return 0


if __name__ == '__main__':
    sys.exit(main())
