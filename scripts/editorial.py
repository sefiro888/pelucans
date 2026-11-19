"""Cabeceras panorámicas y guías de mantenimiento específicas por servicio."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json

GUIDES = {
 'corte-tijera': ('Un acabado bonito que puedas mantener',
  'Trae una foto del estilo que te gusta y cuéntanos cuánto tiempo puedes dedicar al cepillado. La referencia sirve para conversar: la textura, el volumen y el estado del pelo determinan el acabado posible.',
  'Revisamos especialmente axilas, ingles, detrás de las orejas y zonas de roce del arnés. Si hay nudos adheridos a la piel, te explicamos las opciones antes de elegir una longitud. El objetivo es que el arreglo resulte cómodo también después de salir del salón.',
  'Entre citas, comprueba el manto con un peine adecuado, por zonas y sin tirar. Mantén una rutina que llegue a las capas interiores; un acabado largo necesita más mantenimiento que uno práctico.',
  ['Una foto reciente del cuerpo y otra del rostro.', 'El largo que te gustaría conservar y cómo lo cepillas.', 'Su experiencia con el secador y con la manipulación de las patas.'],
  'El corte se elige juntos: estilo, comodidad y mantenimiento tienen que encajar.'),
 'stripping': ('La textura decide la técnica',
  'Dinos si el manto se ha trabajado antes con stripping, tijera o máquina. Esa historia ayuda a valorar la textura actual y a plantear un mantenimiento realista.',
  'Se comprueba si el pelo está maduro y puede retirarse de forma selectiva. Un manto no preparado, una piel sensible o un perro incómodo pueden hacer necesario adaptar o aplazar el trabajo. La técnica se decide tras la valoración.',
  'Pregunta qué herramienta utilizar entre sesiones y evita improvisar una retirada de pelo en casa. El calendario depende del crecimiento y del objetivo del arreglo, por lo que no todas las visitas serán iguales.',
  ['Raza o cruce y una foto del pelo a la luz natural.', 'Qué técnicas se han usado en sus últimas sesiones.', 'Si has observado irritación o sensibilidad al tocar el manto.'],
  'No es un corte estándar: requiere revisar textura, ciclo del pelo y tolerancia.'),
 'deslanado': ('Entender la muda, sin pelearse con ella',
  'Cuéntanos cuándo ha empezado a soltar más pelo y qué herramientas utilizas. Los perros de pelo corto también mudan: la cantidad de pelo visible no es la única señal de que necesitan mantenimiento.',
  'Trabajamos el pelo desprendido por zonas y revisamos cómo responde la piel. El baño, el secado y el cepillado se adaptan a cada capa. En perros con mucho subpelo, la sesión puede necesitar pausas y más tiempo.',
  'Continúa con un cepillado suave y regular, utilizando la herramienta acordada. No hace falta insistir hasta que deje de salir pelo: la muda continúa su ciclo natural. Si aparece una caída irregular o zonas sin pelo, consulta con su veterinario.',
  ['Tamaño, tipo de pelo y una foto reciente.', 'Si está en plena muda o presenta zonas apelmazadas.', 'Cómo tolera el cepillado y el ruido del secado.'],
  'Retiramos pelo suelto; la muda no desaparece ni se resuelve rapando todos los mantos.'),
 'ozonoterapia': ('Primero su piel. Después, el baño',
  'Antes de reservar, informa de los productos que utiliza, de cualquier reacción previa y de las pautas de su veterinario. Si hay lesiones, picor persistente o un tratamiento en curso, necesitamos conocerlo para valorar la cita.',
  'El lavado de ozono se plantea como cuidado complementario. Se revisa si la sesión es adecuada y se adapta el manejo al perro. Las necesidades de una piel sensible no se resuelven con una misma rutina para todos.',
  'Sigue las indicaciones de cuidado que hayas acordado con su veterinario. Si observas un cambio en la piel, no añadas productos nuevos por tu cuenta: consulta antes de repetir o modificar la rutina.',
  ['Motivo de la consulta y estado actual de la piel.', 'Productos, tratamientos e indicaciones veterinarias.', 'Cómo ha tolerado los baños anteriores.'],
  'El baño no sustituye un diagnóstico ni permite prometer la curación de alergias o dermatitis.'),
 'dermocosmetica': ('Elegir mejor, aplicar con cuidado',
  'Trae el nombre del champú que usas y cuéntanos qué resultado buscas: facilitar el peinado, mejorar la manejabilidad del manto o revisar una rutina que no termina de encajar.',
  'Elegimos el cuidado según el pelo y la información que nos facilitas. La aplicación, el aclarado y el secado importan tanto como la selección de un champú, mascarilla o acondicionador.',
  'Utiliza productos formulados para perros y respeta sus instrucciones. Si te llevas cosmética para casa, pregunta cómo aplicarla y cómo combinarla con el cepillado. Más productos no significan un mejor resultado.',
  ['Nombre o foto de los productos que ya utilizas.', 'Reacciones anteriores o sensibilidades conocidas.', 'Las pautas veterinarias si utiliza un champú específico.'],
  'La cosmética acompaña al cuidado del manto; una alteración de la piel requiere valoración veterinaria.'),
 'bano-manto': ('Un baño completo empieza escuchándolo',
  'Avísanos si es su primera visita, si le cuesta entrar en la bañera o si el secador le da miedo. También nos ayuda conocer su movilidad y cualquier zona que prefiera que toquemos con especial cuidado.',
  'Revisamos el pelo antes de mojarlo, seleccionamos el cuidado y organizamos el secado. Las pausas y la protección para amortiguar el ruido se valoran según el perro. Con los grandullones reservamos el tiempo necesario.',
  'Antes de marcharos, pregunta qué zonas conviene cepillar y con qué frecuencia revisar el manto. Si se moja durante los paseos, presta atención al secado y a las zonas donde el pelo tiende a enredarse.',
  ['Nombre, tamaño y tipo de pelo.', 'Nudos, sensibilidades o dificultades de movilidad.', 'Su relación con el agua, el cepillo y el secador.'],
  'La higiene se adapta al perro: el tiempo de secado cambia mucho entre mantos.'),
 'corte-unas': ('Un cuidado pequeño que pide precisión',
  'Coméntanos si alguna vez ha tenido una mala experiencia con las uñas o si evita que le toquen las patas. Saberlo permite preparar un manejo más gradual.',
  'La longitud que puede recortarse depende de cada uña y de su parte sensible. En las uñas oscuras avanzamos con especial prudencia. Unas uñas muy largas pueden requerir varias revisiones, en lugar de un único corte grande.',
  'Observa el crecimiento y acuerda cuándo volver a revisarlas. No olvides los espolones. Si hay dolor, sangrado, rotura o inflamación, la revisión debe hacerla su veterinario.',
  ['Si viene solo para uñas o junto con otro cuidado.', 'Cómo tolera que le toquen las patas.', 'Si alguna uña está dañada o le molesta al apoyar.'],
  'Cortar más no siempre es mejor: respetamos el límite de cada uña.'),
 'comida-especializada': ('Una compra informada para su cuenco',
  'Al consultar, indica el producto que buscas, el formato y la cantidad. Si quieres conocer otras opciones, cuéntanos qué come actualmente y qué necesitas encontrar.',
  'Te explicamos las características de la selección disponible y confirmamos precio y stock antes de la recogida. Las necesidades clínicas, las intolerancias diagnosticadas y los cambios de dieta deben seguir la pauta veterinaria.',
  'Conserva el alimento siguiendo las instrucciones del fabricante y revisa las recomendaciones de ración. Ante dudas sobre peso, digestión o una dieta prescrita, consulta con un profesional veterinario.',
  ['Marca, variedad y formato si buscas algo concreto.', 'Cantidad y fecha aproximada de recogida.', 'La recomendación veterinaria si necesita una dieta clínica.'],
  'Disponibilidad y opciones se confirman por WhatsApp; cada consulta se responde de forma individual.'),
 'asesoramiento': ('Una rutina que encaje en vuestra vida',
  'Piensa qué parte del cuidado os cuesta más: los nudos, las patas, elegir cepillo o encontrar tiempo. Puedes traer tus herramientas para revisar cuáles son útiles para su pelo.',
  'Observamos el manto y hablamos de vuestra rutina. Explicamos qué zonas requieren atención y cómo reconocer que un cuidado está resultando incómodo. Buscamos hábitos sencillos que puedas repetir con calma.',
  'Empieza con sesiones breves y agradables, sin esperar a que el manto esté muy enredado. Si una herramienta no funciona o aparecen dudas, coméntalo en la siguiente visita para ajustar la rutina.',
  ['Las herramientas y productos que tienes en casa.', 'Cuánto tiempo dedicas al cepillado.', 'Qué cuidados tolera bien y cuáles le cuestan.'],
  'El mejor mantenimiento es el que puedes hacer de forma constante y sin molestias.'),
}

def service_depth(s):
    title, before, during, after, checklist, note = GUIDES[s['slug']]
    cards = ''.join(f'<article><span class="eyebrow">{label}</span><h3>{heading}</h3><p>{text}</p></article>' for label, heading, text in [
        ('Antes de venir', 'Preparamos su visita', before),
        ('En el salón', 'Decidimos con criterio', during),
        ('De vuelta a casa', 'Mantenemos el cuidado', after)])
    checks = ''.join(f'<li>{escape(x)}</li>' for x in checklist)
    return f'''<section class="section editorial-depth" id="guia"><div class="wrap"><div class="depth-heading reveal"><span class="eyebrow">Su cuidado, bien explicado</span><h2>{title}</h2><p>La sesión empieza antes de entrar en el salón y continúa con los cuidados de casa.</p></div><div class="depth-cards">{cards}</div><div class="depth-notes"><div><h3>Qué contarnos al reservar</h3><ul>{checks}</ul></div><aside><span class="eyebrow">El criterio de Pelucans</span><p>{note}</p></aside></div></div></section>'''

def panorama(body, file, photo, services, wa):
    """Sustituye únicamente la primera cabecera; conserva el resto y sus controles."""
    end = body.find('</section>')
    if end == -1: return body
    soup = BeautifulSoup(body[:end + 10], 'html.parser')
    old = soup.find('section')
    h1 = old.find('h1')
    if not h1: return body
    title = h1.decode_contents()
    lead = old.select_one('.lead')
    eyebrow = old.select_one('.eyebrow')
    crumbs = old.select_one('.crumbs')
    if crumbs is None and file != 'index.html':
        crumbs = f'<nav class="crumbs" aria-label="Migas de pan"><a href="index.html">Inicio</a><span>/</span><span>{escape(h1.get_text(" ",strip=True))}</span></nav>'
    controls = old.select_one('.hero-cta, .s-cta')
    actions = str(controls) if controls else f'<div class="hero-cta"><a class="btn wa" href="{wa()}">Consultar por WhatsApp</a></div>'
    # Una introducción breve deja respirar a la fotografía.
    summary = lead.decode_contents() if lead else 'Conoce Pelucans: cuidados a medida, atención individual y tiempo para tu peludo.'
    if file == 'index.html': summary = 'Con Shadia, cada perro tiene su momento. Peluquería canina en A Laracha: uno a uno, sin jaulas y con todo el tiempo que necesita.'
    specific = next((s for s in services if file == 'servicio-'+s['slug']+'.html'), None)
    # Solo fotografías reales. El punto focal se elige según las cabezas de cada toma.
    photo_map = {
        'index.html':('cliente-80','center 50%'),
        'nosotros.html':('shadia-bimba-1','center top'),
        'servicios.html':('bruce-bano-2','center 35%'),
        'contacto.html':('fachada','center 40%'),
        'galeria.html':('cliente-80','center 42%'),
        'tienda.html':('story-colonias','center 15%'),
        'servicio-corte-tijera.html':('cliente-16','center 42%'),
        'servicio-stripping.html':('cliente-20','center 20%'),
        'servicio-deslanado.html':('cliente-41','center 35%'),
        'servicio-ozonoterapia.html':('ozono-shadia-wacho','center 40%'),
        'servicio-dermocosmetica.html':('psh-ozone','center top'),
        'servicio-bano-manto.html':('bruce-bano-2','center 35%'),
        'servicio-corte-unas.html':('cliente-46','center 22%'),
        'servicio-comida-especializada.html':('fachada','center 40%'),
        'servicio-asesoramiento.html':('ozono-shadia-wacho','center 40%'),
        'consejos.html':('orejeras','center 35%'),
        'consejo-cepillado.html':('cliente-41','center 35%'),
        'consejo-muda.html':('cliente-20','center 20%'),
        'consejo-primera-visita.html':('bruce-bano-2','center 35%'),
        'consejo-secador-sin-miedo.html':('orejeras','center 30%'),
        'consejo-mitos-del-manto.html':('deslanado','center 42%'),
        '404.html':('fachada','center 40%'),
    }
    source, pos = photo_map.get(file,(photo,'center 35%'))
    image_src = f'assets/img/real/{source}.webp'
    # Variantes reales específicas: se activan al añadir la sesión fotográfica.
    asset_root=Path(__file__).resolve().parent.parent
    desktop=f'assets/img/headers/{file.removesuffix(".html")}-desktop.webp'
    mobile=f'assets/img/headers/{file.removesuffix(".html")}-mobile.webp'
    sources=''
    if (asset_root/desktop).is_file(): sources+=f'<source media="(min-width: 801px)" srcset="{desktop}">'
    if (asset_root/mobile).is_file(): sources+=f'<source media="(max-width: 800px)" srcset="{mobile}">'
    photo_markup=f'<picture>{sources}<img class="panorama-image" src="{image_src}" alt="" fetchpriority="high" decoding="async"></picture>'
    restored_class=''
    mobile_pos=pos
    manifest_path=asset_root/'assets/img/headers/manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    if source in manifest:
        entry=manifest[source]
        candidates=', '.join(f"{item['src']} {item['width']}w" for item in entry['variants'])
        mobile_image=entry['mobile']
        fallback=entry['variants'][1]['src']
        photo_markup=f'<picture><source media="(max-width: 800px)" srcset="{mobile_image["src"]} {mobile_image["width"]}w" sizes="100vw" width="{mobile_image["width"]}" height="{mobile_image["height"]}"><img class="panorama-image" src="{fallback}" srcset="{candidates}" sizes="100vw" alt="" fetchpriority="high" decoding="async"></picture>'
        pos='center top'
        restored_class='restored-dog-hero'
    header = f'''<header class="page-hero cinematic-hero {restored_class} {'cinematic-home' if file=='index.html' else ''}" style="--hero-pos:{pos};--hero-pos-mobile:{mobile_pos}">{photo_markup}<div class="panorama-shade"></div><div class="wrap panorama-content">{str(crumbs) if crumbs else ''}<div class="panorama-copy"><span class="eyebrow">{eyebrow.decode_contents() if eyebrow else 'Pelucans · A Laracha'}</span><h1>{title}</h1><p class="lead">{summary}</p>{actions}</div><div class="panorama-foot"><span>PELUCANS · A LARACHA</span><span>Atención individual · Cita previa</span></div></div></header>'''
    rest = body[end + 10:]
    if specific:
        # La guía se sitúa antes de las preguntas, sin duplicar la explicación inicial.
        marker = '<section class="section tint"><div class="wrap two-col"><div>'
        point = rest.find(marker)
        if point >= 0: rest = rest[:point] + service_depth(specific) + rest[point:]
        else: rest += service_depth(specific)
    if specific:
        rest = rest.replace('class="faq reveal"', 'class="faq reveal" id="preguntas"', 1)
        # El acordeón puede llevar otra variante de clase.
        if 'id="preguntas"' not in rest:
            rest = rest.replace('<div class="faq', '<div id="preguntas" class="faq', 1)
        subnav = '<nav class="service-chapters" aria-label="En esta página"><div class="wrap"><span>Explora este cuidado</span><a href="#detalle">En qué consiste</a><a href="#guia">Guía de cuidados</a><a href="#preguntas">Preguntas frecuentes</a></div></nav>'
    else: subnav = ''
    return header + subnav + rest
