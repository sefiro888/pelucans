"""Generador de la web de Pelucans.
Ejecutar:  python build.py      (genera los 15 HTML a partir de scripts/content.py y las fotos de assets/img/real)
Las fotos reales se optimizan con:  python scripts/prepare_images.py
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json, sys, re, time
BUILD = str(int(time.time()))

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from content import SERVICES  # noqa: E402
from posts import POSTS  # noqa: E402
import i18n  # noqa: E402
from care_journal import EXTRA_POSTS, TRANSLATIONS, enhance
POSTS.extend(EXTRA_POSTS)
from editorial import panorama
from atelier import decorate, service_icon, write_assets, PAW
write_assets(ROOT)

# --- Ajustes editables -------------------------------------------------
# Instagram en directo: pega aquí la dirección del feed JSON de Behold (https://behold.so) y la
# web cargará las últimas publicaciones sola. Vacío = se muestra la copia fija.
INSTAGRAM_FEED_URL = ''
# Mientras no haya suficientes pares reales en assets/img/antes-despues/, se muestran plantillas
# de ejemplo en el carrusel (ponlo a False para ocultarlas).
SHOW_DEMO_PAIRS = False
MIN_PAIRS = 4
# Dirección pública de la web (con barra final), p. ej. 'https://www.pelucans.es/'. Vacío = no se generan canonical ni sitemap.
SITE_URL = 'https://sefiro888.github.io/pelucans/'
CUR = {'file': 'index.html'}
HEAD_SCRIPT = "<script>(function(){try{var t=localStorage.getItem('pel-theme');if(!t&&matchMedia('(prefers-color-scheme: dark)').matches)t='dark';if(t)document.documentElement.dataset.theme=t;var pl=localStorage.getItem('pel-palette');if(pl==='original')delete document.documentElement.dataset.palette;else if(pl)document.documentElement.dataset.palette=pl;if(document.referrer&&new URL(document.referrer).origin===location.origin&&!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('pt-on')}catch(e){}})()</script>"

IG = 'https://www.instagram.com/pelucans_peluqueriacanina/'
IG_DM = 'https://ig.me/m/pelucans_peluqueriacanina'
FB = 'https://www.facebook.com/Pelucans-peluquería-canina-61591595259987'
GOOGLE = 'https://share.google/wduoSy8D64noUdTHf'
PAXINAS = 'https://www.paxinasgalegas.es/pelucans-733277em.html'
AMARILLAS = 'https://www.paginasamarillas.es/f/a-laracha/pelucans-peluqueria-canina_312229941_000000001.html'
CATALOGO = 'https://wa.me/c/34604207678'
PHONE = '604 207 678'
R = 'assets/img/real/'

def img(name, alt='', cls='', lazy=True, w=None, h=None, pos=None):
    a = f' class="{cls}"' if cls else ''
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    s = f' style="object-position:{pos}"' if pos else ''
    return f'<img src="{R}{name}.webp" alt="{escape(alt, True)}"{a}{l}{s}>'

def icon(n): return f'<i class="bi bi-{n}" aria-hidden="true"></i>'

def wa(msg='Hola Shadia, me gustaría pedir información y cita para mi peludo.'):
    return 'https://wa.me/34604207678?text=' + quote(msg)

def btn(label='Pedir cita por WhatsApp', msg=None, cls='wa', ic='whatsapp'):
    return f'<a class="btn {cls}" href="{wa(msg) if msg else wa()}" target="_blank" rel="noopener">{icon(ic)} {label}</a>'

def heading(kicker, title, text=''):
    return f'<div class="reveal"><span class="eyebrow">{kicker}</span><h2>{title}</h2></div>' + (f'<p class="reveal d1">{text}</p>' if text else '')

def sec_head(kicker, title, text='', extra=''):
    return f'<div class="sec-head"><div class="reveal"><span class="eyebrow">{kicker}</span><h2>{title}</h2></div>' + (f'<p class="reveal d1">{text}</p>' if text else '') + extra + '</div>'

# ----------------------------------------------------------------- datos
CLIENTES = [12,16,19,20,21,26,27,30,31,32,33,35,36,37,38,39,40,41,42,45,46,48,56,75,78,79,80,81,82,83,84,87,88,91,92,93,95,47,99,10,29,28,76,77]
def cl(n): return f'cliente-{n:02d}'

COLORS = ['c-pink', 'c-butter', 'c-sage', 'c-sky', 'c-sand', 'c-pink', 'c-butter', 'c-sage', 'c-sky']
MEDIA = {
 'corte-tijera': dict(hero='story-tijera', hero2='cliente-16', pos='center 28%', sticker='tijera a tijera ✂', strip=['cliente-16','cliente-30','cliente-40','cliente-27'], reel=('DczA2PexJXm','reel-tijera','Shadia, tijera en mano','«Más que un corte es amor y cuidado.»','reel',False)),
 'stripping': dict(hero='cliente-20', hero2='cliente-37', pos='center', sticker='a mano, con calma', strip=['cliente-20','cliente-37','cliente-36','cliente-48'], reel=('DczA2PexJXm','reel-tijera','El trabajo manual en el salón','Un reel de Shadia trabajando a mano, con paciencia: así se ve el oficio.','reel',True)),
 'deslanado': dict(hero='deslanado', hero2='cliente-28', pos='center', sticker='adiós, pelos sueltos', strip=['cliente-28','cliente-29','cliente-76','cliente-12'], reel=('DfmILXjEVbX','deslanado','Deslanado de pelo corto','«¡Aunque tengan el pelo cortito, también necesitan sus buenos deslanados!»','p',False)),
 'ozonoterapia': dict(hero='ozono-secado', hero2='wacho', pos='center 30%', sticker='piel feliz', strip=['ozono-shadia-wacho','piel-detalle','wacho','cliente-05'], reel=('DeKUzOLxCmx','reel-wacho','Wacho, cada 15 días','Su sesión de mantenimiento de ozono','reel',False)),
 'dermocosmetica': dict(hero='psh-ozone', hero2='story-colonias', pos='center', sticker='PSH · Artero', strip=['story-psh','story-artero','cat-colonias','story-colonias'], reel=('DdPLG9LEZw_','ozono-secado','Ozono y cuidado de la piel','Una sesión de cuidado con la línea PSH que usamos en el salón.','p',False)),
 'bano-manto': dict(hero='bruce-bano-1', hero2='bruce-bano-2', pos='center 35%', sticker='¡sin prisas!', strip=['bruce-bano-2','orejeras','cliente-29','cliente-95'], reel=('DfSzBEnvbrk','reel-bruce','Bruce, la sesión completa','Una tarde entera de mimos para un grandullón','reel',False)),
 'corte-unas': dict(hero='cliente-46', hero2='cliente-42', pos='center', sticker='pasitos cómodos', strip=['cliente-42','cliente-46','cliente-45','cliente-39'], reel=('DfX9Q7bxnfN','reel-amor','Paciencia con las patitas','Un vistazo a cómo tratamos a los peludos más sensibles: con calma y mucho cariño.','reel',True)),
 'comida-especializada': dict(hero='story-kong', hero2='cat-arnes', pos='center', sticker='para su cuenco', strip=['cat-colonias','cat-kong','cat-arnes','story-raindrops'], reel=('DfSzBEnvbrk','reel-bruce','Un vistazo al salón','Así es un día en Pelucans: de la bañera a la tienda, con todo el tiempo del mundo.','reel',True)),
 'asesoramiento': dict(hero='shadia-bimba-2', hero2='shadia-bimba-1', pos='center 30%', sticker='te lo explico fácil', strip=['cliente-41','cliente-40','cliente-35','cliente-83'], reel=('DfX9Q7bxnfN','reel-amor','Hay amores que no se explican','Shadia con uno de sus clientes: el trato, antes que la técnica.','reel',True)),
}
REVIEWS = [
 ('Paulina Lichota', 'Muy profesional, amable y cariñosa con los perros.', 'Google'),
 ('María Quintana', 'Trato inmejorable. Tanto con los peludos como con los clientes. Mi perrita ha salido, a parte de preciosa, encantada con los mimos recibidos en Pelucans. Sin duda volveremos.', 'Destacado de Instagram'),
 ('Sara', 'Maravillosa y muy bien de precio, la atención genial y el trato con los peludos exquisito. Lleva atendiendo a mis perros unos años y siempre un 10.', 'Destacado de Instagram'),
 ('Duque Caxias', 'Hoy Jagger, mi pastor alemán, hizo uso de los servicios de Pelucans y salió muy satisfecho, al igual que yo. Bonitas y cuidadas instalaciones, trato exquisito y buenos precios.', 'Páxinas Galegas'),
 ('Nayla Suarez Cousillas', 'Un lugar excelente para dejar a tu mascota en las mejores manos, con mimo y tiempo. Mi peludito salió guapísimo y moviendo la colita de alegría.', 'Destacado de Instagram'),
 ('María Manteiga', 'Hoy Suri tuvo su primera visita con Shadia y solo puedo decir que salimos encantadas.', 'Google'),
 ('Carlos Varela', 'Destaco el buen trato y cariño que le ha dado y lo bonito que salió de allí. El local es muy bonito y está impoluto. Muy buenos productos en general. Volveremos.', 'Destacado de Instagram'),
 ('Laura Esmoris', 'Recomendo este sitio un 20 de 10. Shadia é unha gran profesional e amante dos animales. Notase que non só é traballo para ela, tamén é vocación!', 'Páxinas Galegas'),
]
IG_POSTS = [
 ('deslanado', 'DfmILXjEVbX', 'p', 'Deslanado de pelo corto con cepillo Artero'),
 ('reel-amor', 'DfX9Q7bxnfN', 'reel', 'Reel: hay amores que no se pueden explicar con palabras'),
 ('reel-bruce', 'DfSzBEnvbrk', 'reel', 'Reel: la sesión completa de Bruce'),
 ('bruce-bano-1', 'De1SJW8kVUb', 'p', 'Shadia bañando a Bruce, un San Bernardo'),
 ('reel-wacho', 'DeKUzOLxCmx', 'reel', 'Reel: Wacho y su tratamiento de ozono'),
 ('orejeras', 'Ddj_IxSDaiY', 'p', 'Perrito con orejeras protectoras durante el secado'),
 ('ozono-secado', 'DdPLG9LEZw_', 'p', 'Sesión de ozono y secado'),
 ('reel-tijera', 'DczA2PexJXm', 'reel', 'Reel: corte a tijera en Pelucans'),
 ('shadia-bimba-1', 'DclCM_XjWAj', 'p', 'Shadia Cotelo con su perrita Bimba'),
]
HIGHLIGHTS = [('productos', 'Productos'), ('clientes', 'Clientes'), ('vintedgo', 'Vinted Go'), ('servicios', 'Servicios'), ('horario', 'Horario'), ('resenas', 'Reseñas')]
PRODUCTS = [
 ('cat-colonias', 'Colonias PSH', '13 €', 'Colonias para perro de la línea PSH: Citric Fragrance y Puppy Fragrance. Para ese toque final que se huele a metros.', 'Colonias PSH (13 €)'),
 ('cat-kong', 'Juguetes KONG', '10 €', 'KONG, el juguete resistente que se rellena y entretiene. Hay varios modelos y tamaños: pregunta por lo que tiene tu peludo en mente.', 'Juguetes KONG (10 €)'),
 ('cat-arnes', 'Arnés Pollo & Paco', '25 €', 'Arnés cómodo y ajustable para cualquier paseo. Diseños originales que no pasan desapercibidos.', 'el Arnés Pollo & Paco (25 €)'),
]

# ----------------------------------------------------------------- bloques
TICKER = ['★ 5,0 en Google · 208 opiniones', 'Atención uno a uno · sin jaulas · sin prisas', 'Orejeras protectoras en el secado', 'Desde un maltés hasta un San Bernardo', 'Punto de recogida Vinted Go', f'Pide cita: {PHONE}']
def ticker():
    items = ['<em class="open-pill tk-open" data-open>Horario</em>'] + TICKER
    return '<div class="ticker" aria-label="Información destacada"><div class="ticker-track">' + ''.join(f'<span>{t}</span>' for t in items) + '</div></div>'

def nav(active=''):
    mega = ''.join(f'<a href="servicio-{s["slug"]}.html"><span class="menu-symbol">{service_icon(s["slug"])}</span><span class="menu-care"><b>{s["name"]}</b><small>{s["cat"]}</small></span></a>' for s in SERVICES)
    def cur(k): return ' aria-current="page"' if active == k else ''
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>{ticker()}
<header class="nav"><div class="wrap nav-in"><a class="brand" href="index.html" aria-label="Pelucans, inicio"><img src="{R}perfil.webp" alt="Logotipo de Pelucans" width="52" height="52"><span><b>Pelucans</b><small>PELUQUERÍA CANINA</small></span></a>
<button class="menu-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><i class="bi bi-list"></i></button>
<nav class="nav-links" id="menu" aria-label="Principal"><a href="index.html"{cur('inicio')}>Inicio</a><div class="nav-drop"><a href="servicios.html"{cur('servicios')}>Servicios</a><button aria-label="Mostrar servicios" aria-expanded="false"><i class="bi bi-chevron-down"></i></button><div class="mega"><div class="mega-heading"><span class="eyebrow">La carta de Pelucans</span><strong>Su cuidado empieza aquí.</strong><a href="servicios.html">Explorar los nueve cuidados</a></div><div class="mega-care-grid">{mega}</div></div></div><a href="tienda.html"{cur('tienda')}>Tienda</a><a href="galeria.html"{cur('galeria')}>Galería</a><a href="consejos.html"{cur('consejos')}>Consejos</a><a href="nosotros.html"{cur('nosotros')}>Nosotros</a><a href="contacto.html"{cur('contacto')}>Contacto</a><span class="open-pill" data-open>Horario</span><span class="nav-tools"><span class="pal"><button class="pal-toggle" aria-label="Cambiar paleta de colores" aria-expanded="false" title="Paleta de colores"><i class="bi bi-palette2"></i></button><span class="pal-pop" role="menu" aria-label="Paletas de color"><button role="menuitem" data-pal="original"><i class="sw" style="--a:#ff7ca6;--b:#ffc93c;--c:#cfe6c9"></i><span><b>Original</b><small>Rosa y mantequilla</small></span></button><button role="menuitem" data-pal="logo"><i class="sw" style="--a:#0d0d0d;--b:#bdbdbd;--c:#ffffff"></i><span><b>Logo</b><small>Negro, blanco y grises</small></span></button><button role="menuitem" data-pal="mar"><i class="sw" style="--a:#10253a;--b:#ff7a59;--c:#ffd166"></i><span><b>Mar</b><small>Azul marino y coral</small></span></button><button role="menuitem" data-pal="bosque"><i class="sw" style="--a:#14281d;--b:#e8825a;--c:#c3dcb9"></i><span><b>Bosque</b><small>Verde y terracota</small></span></button><button role="menuitem" data-pal="lila"><i class="sw" style="--a:#251a38;--b:#b58cff;--c:#ffcf8a"></i><span><b>Lila</b><small>Violeta y melocotón</small></span></button></span></span><button class="theme-toggle" aria-label="Cambiar entre modo claro y oscuro" title="Modo claro / oscuro"><i class="bi bi-sun sun"></i><i class="bi bi-moon-stars moon"></i></button><span class="lang-switch" role="group" aria-label="Idioma"><a href="{CUR['file']}" lang="es" aria-current="true">ES</a><a href="gl/{CUR['file']}" lang="gl" hreflang="gl">GL</a></span></span>{btn('Pedir cita')}</nav></div></header>'''

def cta(msg=None, title='Nos encantará conocer a tu <em>peludo.</em>'):
    return f'''<section class="cta"><svg class="paw" viewBox="0 0 120 120" aria-hidden="true"><g fill="#17120f"><ellipse cx="60" cy="78" rx="20" ry="16"/><circle cx="34" cy="52" r="10"/><circle cx="52" cy="36" r="10"/><circle cx="70" cy="36" r="10"/><circle cx="88" cy="52" r="10"/></g></svg><div class="wrap cta-in"><div class="reveal"><span class="eyebrow" style="color:var(--ink)">Tu próximo momento favorito</span><h2>{title}</h2><p>Cuéntanos cómo es, qué le gusta y qué necesita. Del resto nos encargamos nosotros, con calma.</p></div><div class="acts reveal d1">{btn('Hablemos por WhatsApp', msg, 'light')}<a class="btn ghost" href="tel:+34604207678">{icon('telephone')} Llamar al {PHONE}</a><small>Siempre con cita previa · Avda. Doutor López Astray, 40</small></div></div></section>'''

def faces():
    half = len(CLIENTES) // 2
    def row(items, cls=''):
        tiles = ''.join(f'<figure class="face" data-lb="{R}{cl(n)}.webp">{img(cl(n), "Un peludo que ha pasado por Pelucans")}</figure>' for n in items)
        return f'<div class="face-row marquee {cls}" data-lb-group><div class="marquee-track">{tiles}</div></div>'
    return f'''<section class="faces" aria-labelledby="faces-t"><div class="wrap faces-head"><div class="reveal"><span class="eyebrow">El club de los bien cuidados</span><h2 id="faces-t">Caras felices,<br>colas <em>moviéndose.</em></h2></div><p class="reveal d1">Fotos reales de sus historias de Instagram: peludos de todos los tamaños después de su rato en la mesa. Toca una foto para verla grande.</p></div>{row(CLIENTES[:half])}{row(CLIENTES[half:], 'reverse slow')}</section>'''

def band(words, cls=''):
    return f'<div class="band marquee {cls}" aria-hidden="true"><div class="marquee-track">' + ''.join(f'<span>{w}</span>' for w in words) + '</div></div>'

def service_card(s, i, wide=False):
    m = MEDIA[s['slug']]
    return f'''<a class="card {COLORS[i]}{' wide' if wide else ''} reveal" href="servicio-{s['slug']}.html" data-cat="{s['cat']}"><div class="ph">{img(m['hero'], 'Cuidado canino: ' + s['name'].lower(), pos=m['pos'])}<span class="n">{i + 1:02d}</span><span class="go">{icon('arrow-up-right')}</span></div><div class="tx"><small>{s['cat']}</small><h3>{icon(s['icon'])} {s['name']}</h3><p>{s['short']}</p></div></a>'''

WIDE = {0, 1, 5, 6, 7, 8}
def bento(uniform=False):
    return '<div class="bento">' + ''.join(service_card(s, i, (i in WIDE) and not uniform) for i, s in enumerate(SERVICES)) + '</div>'

def stories_block(title='Los destacados de Instagram,<br>aquí <em>dentro.</em>', text='Pulsa un círculo y recorre los destacados reales de Pelucans sin salir de la web: clientes, productos, horario y reseñas.'):
    hl = ''.join(f'<button class="hl-btn" data-hl="{k}"><span class="hl-ring">{img("hl-" + k, "Destacado " + n)}</span>{n}</button>' for k, n in HIGHLIGHTS)
    return f'''<section class="section"><div class="wrap">{sec_head('Directo de su Instagram', title, text)}<div class="hl-row reveal">{hl}</div></div></section>'''

def reels_block(only=None):
    items = [('DczA2PexJXm', 'reel-tijera', 'Corte a tijera', '«Más que un corte es amor y cuidado»'), ('DfSzBEnvbrk', 'reel-bruce', 'Bruce, sesión completa', 'Una tarde de mimos para un San Bernardo'), ('DeKUzOLxCmx', 'reel-wacho', 'Wacho y el ozono', 'Cada 15 días, fiel a su cita'), ('DfX9Q7bxnfN', 'reel-amor', 'Amor perruno', 'Hay amores que no se pueden explicar')]
    return '<div class="reels">' + ''.join(f'<button class="reel reveal d{i % 4}" data-reel="{c}" aria-label="Ver el reel: {t}">{img(im, t)}<span class="play">{icon("play-fill")}</span><span class="cap"><small>Reel · Instagram</small>{t}</span></button>' for i, (c, im, t, d) in enumerate(items)) + '</div>'

def reviews_block():
    cards = ''.join(f'<figure class="rev"><div class="stars" aria-label="5 estrellas">★★★★★</div><blockquote>«{escape(t)}»</blockquote><figcaption><span class="av">{n[0]}</span><span><b>{n}</b></span><span class="src">{src}</span></figcaption></figure>' for n, t, src in REVIEWS)
    return f'''<section class="section pink"><div class="wrap">{sec_head('Lo dicen sus familias', 'El cariño se nota.<br>Y <em>se cuenta.</em>', '', f'<a class="rating-big reveal d1" href="{GOOGLE}" target="_blank" rel="noopener"><b>5,0</b><span><span class="stars">★★★★★</span><small>208 opiniones en Google ↗</small></span></a>')}</div><div class="rev-wrap marquee"><div class="marquee-track">{cards}</div></div><div class="wrap"><p style="margin:1.4rem 0 0;font-size:.9rem;color:var(--ink-2)">Reseñas públicas de clientes reales, recogidas de las historias de Instagram de Pelucans, Google y Páxinas Galegas. <a href="{GOOGLE}" target="_blank" rel="noopener">Léelas todas en Google ↗</a> · <a href="{PAXINAS}" target="_blank" rel="noopener">Páxinas Galegas ↗</a></p></div></section>'''

def ig_block():
    tiles = ''.join(f'<a href="{IG}{t}/{c}/" target="_blank" rel="noopener" aria-label="{escape(a)}">{img(im, a)}{"<span class=tp>" + icon("play-fill") + "</span>" if t == "reel" else ""}</a>' for im, c, t, a in IG_POSTS)
    return f'''<section class="section tint"><div class="wrap ig-split"><div><div class="reveal"><span class="eyebrow">Síguenos</span><h2>Su día a día,<br>sin <em>filtros.</em><span class="live-tag" data-ig-live hidden>En directo</span></h2></div><div class="ig-card reveal d1"><img src="{R}perfil.webp" alt="Perfil de Pelucans en Instagram"><div><b>@pelucans_peluqueriacanina</b><small>Profesional dog groomer · Grooming · Ozono · Dermocosmética</small></div></div><p class="reveal d1">Cada publicación es un peludo de verdad, bañado, cortado y mimado en el salón. Pulsa cualquier foto para ir a la publicación original.</p><div class="socials reveal d2"><a href="{IG}" target="_blank" rel="noopener">{icon('instagram')} Instagram</a><a href="{FB}" target="_blank" rel="noopener">{icon('facebook')} Facebook</a><a href="{GOOGLE}" target="_blank" rel="noopener">{icon('google')} Google</a></div></div><div class="ig-grid reveal d1" data-ig-feed="{INSTAGRAM_FEED_URL}">{tiles}</div></div></section>'''

def visit_block():
    return f'''<section class="section" id="visita"><div class="wrap">{sec_head('Ven a conocernos', 'Te esperamos en<br><em>A Laracha.</em>', 'Avenida Doutor López Astray, 40. Siempre con cita previa y con sitio para aparcar.')}<div class="visit"><div class="hours reveal"><h3>Cuándo venir <span class="open-pill" data-open>Horario</span></h3><div class="hour-row" data-day="1-5"><span>Lunes a viernes</span><strong>9:30–13:30<br>16:00–19:00</strong></div><div class="hour-row" data-day="6"><span>Sábados</span><strong>Con cita previa</strong></div><div class="hour-row" data-day="0"><span>Domingos</span><strong>Cerrado</strong></div><p style="margin:1.2rem 0 0;font-size:.95rem;color:var(--ink-2)">{icon('p-circle')} Parking cerca de la puerta.&nbsp; {icon('box-seam')} Punto Vinted Go.</p><div style="display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.2rem">{btn('Pedir cita')}<a class="btn light" href="tel:+34604207678">{icon('telephone')} {PHONE}</a></div></div><div class="facade reveal d1">{img('fachada', 'Fachada de Pelucans Peluquería Canina en la Avenida Doutor López Astray, A Laracha')}<div class="tagline">{icon('geo-alt-fill')} Avda. Doutor López Astray, 40 bajo · 15145 A Laracha <a class="link-arrow" href="contacto.html#ubicacion">Cómo llegar</a></div></div></div></div></section>'''

def footer():
    return f'''<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="index.html" style="color:#fff"><img src="{R}perfil.webp" alt="" width="52" height="52" style="border-color:#fff"><span><b>Pelucans</b><small style="color:#a89c8e">PELUQUERÍA CANINA</small></span></a><p style="margin-top:1rem">Más que un corte, es amor y cuidado.<br>Peluquería canina en A Laracha.</p><div class="socials"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram de Pelucans">{icon('instagram')}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook de Pelucans">{icon('facebook')}</a><a href="{GOOGLE}" target="_blank" rel="noopener" aria-label="Ficha de Google de Pelucans">{icon('google')}</a><a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{icon('whatsapp')}</a></div></div>
<div><h4>Ven a vernos</h4><p>Avda. Doutor López Astray, 40 bajo<br>15145 A Laracha · A Coruña</p><div class="footer-links"><a href="contacto.html#ubicacion">Cómo llegar ↗</a><a href="tel:+34604207678">{PHONE}</a></div></div>
<div><h4>Horario</h4><p>Lunes a viernes<br>9:30–13:30 · 16:00–19:00<br>Sábados con cita previa<br>Domingos cerrado</p></div>
<div><h4>Explora</h4><div class="footer-links"><a href="servicios.html">Servicios</a><a href="tienda.html">Tienda y Vinted Go</a><a href="galeria.html">Galería</a><a href="consejos.html">Consejos</a><a href="nosotros.html">Shadia y Bimba</a><a href="contacto.html">Pedir cita</a><a href="{CATALOGO}" target="_blank" rel="noopener">Catálogo de WhatsApp ↗</a></div></div></div>
<div class="dirs"><span style="font-size:.85rem;color:#a89c8e;align-self:center">También en:</span><a href="{PAXINAS}" target="_blank" rel="noopener">Páxinas Galegas</a><a href="{AMARILLAS}" target="_blank" rel="noopener">Páginas Amarillas</a><a href="{GOOGLE}" target="_blank" rel="noopener">Google</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{FB}" target="_blank" rel="noopener">Facebook</a></div>
<div class="footer-big" aria-hidden="true">Pelucans</div>
<div class="footer-bottom"><span>© 2026 Pelucans Peluquería Canina · A Laracha</span><span>Hecho con cariño (y algún ladrido).</span><button class="privacy-open">Privacidad</button></div></div></footer>
<a class="fab" href="{wa()}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{icon('whatsapp')}<span>¿Hablamos?</span></a>
<div class="mbar"><a href="tel:+34604207678">{icon('telephone-fill')} Llamar</a><a href="{wa()}" target="_blank" rel="noopener">{icon('whatsapp')} WhatsApp</a></div>
<dialog id="lightbox" aria-label="Foto ampliada"><button class="x" aria-label="Cerrar">×</button><button class="lb-nav prev" aria-label="Anterior">‹</button><img alt=""><button class="lb-nav next" aria-label="Siguiente">›</button></dialog>
<dialog id="reel-dialog" class="reel-dialog" aria-label="Reel de Instagram"><button class="x" aria-label="Cerrar">×</button><iframe title="Reel de Pelucans en Instagram" allow="autoplay; encrypted-media; fullscreen" loading="lazy"></iframe><div style="padding:.7rem;text-align:center;background:var(--paper)"><a class="ext link-arrow" target="_blank" rel="noopener" href="{IG}">Abrir en Instagram ↗</a></div></dialog>
<dialog id="privacy"><button class="x" aria-label="Cerrar">×</button><span class="eyebrow">Tu privacidad</span><h2 style="font-size:2rem">Una consulta directa.</h2><p>El formulario prepara un mensaje en tu dispositivo y abre WhatsApp. Esta web no guarda tus respuestas ni confirma reservas automáticamente: tú decides si envías el mensaje.</p><p>Los reels se cargan desde Instagram y el mapa desde Google Maps solo cuando tú lo pulsas, y cada servicio aplica su propia política de privacidad. No usamos analítica ni publicidad.</p><p>Para consultas sobre los datos que compartas con Pelucans, llama al {PHONE}.</p></dialog>'''

def page(file, title, description, body, active='', og='fachada', home=False, cls='pro', ld=None):
    CUR['file'] = file
    body = panorama(body, file, og, SERVICES, wa)
    body = enhance(body, file)
    body = decorate(body, file, ROOT)
    i18n.GL.update(TRANSLATIONS)
    if SITE_URL:
        canon = f'<link rel="canonical" href="{SITE_URL}{file}">'
        ogurl = f'<meta property="og:url" content="{SITE_URL}{file}">'
        alt = f'<link rel="alternate" hreflang="es" href="{SITE_URL}{file}"><link rel="alternate" hreflang="gl" href="{SITE_URL}gl/{file}"><link rel="alternate" hreflang="x-default" href="{SITE_URL}{file}">'
    else:
        canon = ogurl = ''
        alt = f'<link rel="alternate" hreflang="es" href="{file}"><link rel="alternate" hreflang="gl" href="gl/{file}">'
    ld_scripts = ''
    for item in (ld or []):
        ld_scripts += '<script type="application/ld+json">' + json.dumps(item, ensure_ascii=False) + '</script>'
    if SITE_URL and file != 'index.html':
        trail = [('Inicio', 'index.html')]
        if file.startswith('servicio-'): trail.append(('Servicios', 'servicios.html'))
        if file.startswith('consejo-'): trail.append(('Consejos', 'consejos.html'))
        trail.append((title, file))
        ld_scripts += '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE_URL + f} for i, (n, f) in enumerate(trail)]}, ensure_ascii=False) + '</script>'
    body = body.replace('@@FILE@@', file)
    schema = {'@context': 'https://schema.org', '@type': ['LocalBusiness', 'PetGroomer'] if False else 'LocalBusiness', 'name': 'Pelucans Peluquería Canina', 'description': 'Peluquería canina en A Laracha: corte a tijera, deslanado, stripping, baño de ozono, dermocosmética y asesoramiento.', 'telephone': '+34604207678', 'image': R + 'fachada.webp', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Avda. Doutor López Astray, 40', 'postalCode': '15145', 'addressLocality': 'A Laracha', 'addressRegion': 'A Coruña', 'addressCountry': 'ES'}, 'sameAs': [IG, FB, PAXINAS, AMARILLAS], 'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '5.0', 'reviewCount': '208'}, 'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '09:30', 'closes': '13:30'}, {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '16:00', 'closes': '19:00'}]}
    html = f'''<!doctype html><html lang="es" data-palette="logo"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f7f1e8"><title>{escape(title)} | Pelucans · A Laracha</title><meta name="description" content="{escape(description, True)}"><meta property="og:title" content="{escape(title, True)} | Pelucans"><meta property="og:description" content="{escape(description, True)}"><meta property="og:type" content="website">{ogurl}<meta property="og:image" content="{R}{og}.webp"><link rel="icon" href="{R}perfil.webp"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Figtree:wght@400;500;600;700;800&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;0,9..144,800;1,9..144,500;1,9..144,700&display=swap" rel="stylesheet"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"><link rel="stylesheet" href="assets/css/site.css"><link rel="stylesheet" href="assets/css/extra.css"><link rel="stylesheet" href="assets/css/fx.css"><link rel="stylesheet" href="assets/css/palettes.css"><link rel="stylesheet" href="assets/css/premium.css"><link rel="stylesheet" href="assets/css/premium2.css"><link rel="stylesheet" href="assets/css/palettes-contraste.css"><link rel="stylesheet" href="assets/css/editorial.css"><link rel="stylesheet" href="assets/css/atelier.css">{canon}{alt}<link rel="manifest" href="site.webmanifest"><link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png"><link rel="icon" type="image/png" sizes="32x32" href="assets/icons/favicon-32.png">{HEAD_SCRIPT}<script src="assets/js/site.js" defer></script><script src="assets/js/fx.js" defer></script><script src="assets/js/atelier.js" defer></script><script src="assets/js/instagram-feed.js" defer></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>{ld_scripts}</head><body class="{'home' if home else 'inner'}{(' ' + cls) if cls else ''}"><div class="pt" aria-hidden="true">{PAW}<span>Pelucans</span></div>{nav(active)}<main id="contenido">{body}</main>{footer()}</body></html>'''
    html = re.sub(r'(assets/(?:css|js)/[\w-]+\.(?:css|js))"', r'\1?v=' + BUILD + '"', html)
    (ROOT / file).write_text(html, encoding='utf-8')
    gl_dir = ROOT / 'gl'; gl_dir.mkdir(exist_ok=True)
    (gl_dir / file).write_text(i18n.to_galician(html, file), encoding='utf-8')


# ----------------------------------------------------------------- BLOQUES NUEVOS (v3)
PAW_SVG = '<svg viewBox="0 0 120 120" aria-hidden="true"><g fill="currentColor"><ellipse cx="60" cy="78" rx="20" ry="16"/><circle cx="34" cy="52" r="10"/><circle cx="52" cy="36" r="10"/><circle cx="70" cy="36" r="10"/><circle cx="88" cy="52" r="10"/></g></svg>'

def hero_media():
    video = ROOT / 'assets' / 'video' / 'portada.mp4'
    if video.exists():
        return f'<video autoplay muted loop playsinline poster="{R}shadia-bimba-1.webp" aria-label="Shadia trabajando en Pelucans"><source src="assets/video/portada.mp4" type="video/mp4"></video>'
    return img('shadia-bimba-1', 'Shadia Cotelo con su perrita Bimba en Pelucans', lazy=False, pos='center 30%')

def svc_data():
    data = [dict(slug=x['slug'], name=x['name'], short=x['short'], url=f"servicio-{x['slug']}.html", img=f"{R}{MEDIA[x['slug']]['hero2'] if MEDIA[x['slug']]['hero'].startswith('story') else MEDIA[x['slug']]['hero']}.webp") for x in SERVICES]
    return '<script type="application/json" id="svc-data">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'

def quiz_block():
    return f"""<section class="section sage" id="test"><div class="wrap two-col"><div>{heading('Test rápido', '¿Qué necesita<br>tu <em>peludo?</em>', 'Tres preguntas y te decimos por dónde empezar. Sin registros: el resultado se queda en tu pantalla y, si quieres, se lo mandas a Shadia por WhatsApp.')}</div><div class="quiz reveal d1"><div class="quiz-bar"><i></i></div><div class="quiz-body"><noscript>Activa JavaScript para hacer el test, o <a href="contacto.html">escríbenos</a> y te orientamos.</noscript></div></div></div></section>{svc_data()}"""

def ba_pairs():
    pairs = [dict(a=f'{R}antes.webp', d=f'{R}despues.webp', name='Caniche', service='Su sesión en Pelucans', demo=False)]
    folder = ROOT / 'assets' / 'img' / 'antes-despues'
    names = {x['slug']: x['name'] for x in SERVICES}
    if folder.exists():
        for f in sorted(folder.glob('*_antes.*')):
            stem = f.stem[:-len('_antes')]
            d = next(iter(folder.glob(stem + '_despues.*')), None)
            if not d: continue
            bits = stem.split('_')
            nm = bits[0].replace('-', ' ').title(); breed = bits[1].replace('-', ' ').capitalize() if len(bits) > 1 else ''
            sv = names.get(bits[2], bits[2].replace('-', ' ').capitalize()) if len(bits) > 2 else ''
            pairs.append(dict(a=f'assets/img/antes-despues/{f.name}', d=f'assets/img/antes-despues/{d.name}', name=(f'{nm} · {breed}' if breed else nm), service=sv, demo=False))
    if SHOW_DEMO_PAIRS:
        demos = [('Aquí irá tu peludo', 'Corte a tijera'), ('Un schnauzer, por ejemplo', 'Stripping'), ('Un golden en plena muda', 'Deslanado')]
        for nm, sv in demos:
            if len(pairs) >= MIN_PAIRS: break
            pairs.append(dict(name=nm, service=sv, demo=True))
    return pairs

def _ba_multi():
    sl = ''
    for q in ba_pairs():
        if q['demo']:
            inner = f'<div class="before"><div>{PAW_SVG}<b>Antes</b><span class="demo-note">plantilla de ejemplo</span></div></div><div class="after"><div>{PAW_SVG}<b>Después</b><span class="demo-note">plantilla de ejemplo</span></div></div>'
        else:
            inner = f'<img src="{q["a"]}" alt="{q["name"]} antes de su sesión en Pelucans" loading="lazy"><img class="after" src="{q["d"]}" alt="{q["name"]} después de su sesión en Pelucans" loading="lazy">'
        sl += f'<div class="ba-slide"><div class="compare{" demo" if q["demo"] else ""}" aria-label="Comparador de antes y después: {q["name"]}">{inner}<span class="tag l">Antes</span><span class="tag r">Después</span><div class="handle"></div><input type="range" min="0" max="100" value="50" aria-label="Deslizar para comparar el antes y el después"></div><div class="ba-cap"><b>{q["name"]}</b><span>{q["service"]}</span></div></div>'
    note = '<p style="font-size:.85rem;color:var(--muted);margin:.8rem 0 0">Las tarjetas con huellas son plantillas: cuando Shadia pase más pares de fotos reales, ocuparán su lugar.</p>' if any(q['demo'] for q in ba_pairs()) else ''
    return f'<div class="ba-car"><div class="ba-track" tabindex="0" aria-label="Carrusel de antes y después">{sl}</div><div class="ba-ctrl"><button class="prev" aria-label="Anterior">‹</button><div class="ba-mid"><div class="ba-dots"></div><span class="ba-count" aria-live="polite"></span></div><button class="next" aria-label="Siguiente">›</button></div>{note}</div>'

def ba_carousel():
    qs = ba_pairs()
    if len(qs) == 1:
        q = qs[0]
        return f'<div class="ba-one"><div class="compare" aria-label="Comparador de antes y después: {q["name"]}"><img src="{q["a"]}" alt="{q["name"]} antes de su sesión en Pelucans" loading="lazy"><img class="after" src="{q["d"]}" alt="{q["name"]} después de su sesión en Pelucans" loading="lazy"><span class="tag l">Antes</span><span class="tag r">Después</span><div class="handle"></div><input type="range" min="0" max="100" value="50" aria-label="Deslizar para comparar el antes y el después"></div><div class="ba-cap"><b>{q["name"]}</b><span>{q["service"]}</span></div></div>'
    return _ba_multi()


def showcase():
    pics = ''.join(f'<img src="{R}{MEDIA[x["slug"]]["hero"]}.webp" alt="{x["name"]} en Pelucans" style="object-position:{MEDIA[x["slug"]]["pos"]}"' + (' class="on"' if i == 0 else ' loading="lazy"') + '>' for i, x in enumerate(SERVICES))
    items = ''.join(f'<article class="sc-item" data-tag="{MEDIA[x["slug"]]["sticker"]}"><span class="num">{i + 1:02d}</span><div class="mob-pic">{img(MEDIA[x["slug"]]["hero"], x["name"] + " en Pelucans", pos=MEDIA[x["slug"]]["pos"])}</div><h3>{x["name"]}</h3><p>{x["intro"]}</p><div><a class="btn" href="servicio-{x["slug"]}.html">Ver {x["name"].lower()}</a></div></article>' for i, x in enumerate(SERVICES))
    return f'<section class="section tint"><div class="wrap">{sec_head("Un paseo por los cuidados", "Mientras bajas,<br>ellos <em>cambian.</em>", "La foto se queda y el texto avanza: recorre los nueve cuidados uno a uno.")}<div class="showcase"><div class="sc-pic">{pics}<span class="sc-tag"></span></div><div class="sc-list">{items}</div></div></div></section>'

def shapes_block():
    L = [('bone', 'cliente-40'), ('heart', 'cliente-31'), ('cloud', 'cliente-19'), ('paw', 'cliente-39'), ('arch', 'cliente-26'), ('flower', 'cliente-21'), ('bone', 'cliente-16')]
    t = ''.join(f'<figure class="shape {k} reveal" data-lb="{R}{n}.webp"><div>{img(n, "Un peludo de Pelucans")}</div></figure>' for k, n in L)
    return f'<section class="section"><div class="wrap">{sec_head("Marcos con gracia", "Un hueso, una nube,<br>un <em>corazón.</em>", "Porque no todas las fotos tienen que ser cuadradas.")}<div class="shapes" data-lb-group>{t}</div></div></section>'

def blog_cards(posts=POSTS):
    return '<div class="posts">' + ''.join(f'<a class="post reveal d{i}" href="consejo-{x["slug"]}.html"><div class="ph">{img(x["img"], x["title"], pos=x["pos"])}</div><div class="tx"><span class="meta">{x["tag"]} · {x["mins"]} min</span><h3>{x["title"]}</h3><p>{x["excerpt"]}</p><span class="link-arrow">Leer el consejo ↗</span></div></a>' for i, x in enumerate(posts)) + '</div>'

import areamap


def area_map():
    return areamap.build(icon, heading, PHONE)


def advice_page():
    body = f"""<section class="p-hero"><div class="paw-bg"></div><div class="wrap p-hero-grid"><div><nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Consejos</span></nav><span class="eyebrow">El rincón de Shadia</span><h1>Consejos para<br>su <em class="scribble">día a día.</em></h1><p class="lead">Cepillado, muda, primera visita… Guías cortas y claras para cuidar su manto en casa. Siempre con un recordatorio: ante cualquier duda de salud, su veterinario.</p><div class="hero-cta">{btn('Preguntarle a Shadia')}</div></div><div class="p-photo float">{img('cliente-41', 'Un border collie mirando a cámara en Pelucans', lazy=False)}<span class="sticker">aprende un truco</span></div></div></section>"""
    body += f'<section class="section"><div class="wrap">{sec_head("Del salón a tu casa", "Cinco guías<br>para <em>cuidarlo.</em>")}{blog_cards()}</div></section>'
    body += quiz_block()
    body += cta('Hola Shadia, tengo una duda sobre el cuidado de mi perro.', '¿Tienes una duda <em>concreta?</em>')
    page('consejos.html', 'Consejos de cuidado canino', 'Consejos de Shadia, groomer en A Laracha: cómo cepillar a tu perro, cómo llevar la muda y cómo preparar la primera visita a la peluquería canina.', body, 'consejos', 'cliente-41')

def advice_post_pages():
    for i, x in enumerate(POSTS):
        others = [y for y in POSTS if y['slug'] != x['slug']][:3]
        body = f"""<section class="p-hero"><div class="paw-bg"></div><div class="wrap p-hero-grid"><div><nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <a href="consejos.html">Consejos</a> / <span>{x['tag']}</span></nav><span class="eyebrow">{x['tag']} · {x['mins']} min de lectura</span><h1 style="font-size:clamp(2.2rem,5vw,4.2rem)">{x['title']}</h1><p class="lead">{x['excerpt']}</p></div><div class="p-photo float">{img(x['img'], x['title'], lazy=False, pos=x['pos'])}</div></div></section>
<section class="section tint"><div class="wrap"><article class="article">{x['body']}<figure>{img(x['img2'], 'Imagen del salón de Pelucans', pos='center 30%')}<figcaption>Del día a día en Pelucans.</figcaption></figure><div class="note">{icon('heart-fill')}<span>Estos consejos son orientativos. Cada perro es distinto: si tienes dudas, escríbenos y lo vemos con su manto delante.</span></div><div style="margin-top:1.6rem">{btn('Consultar a Shadia', 'Hola Shadia, he leído el consejo «' + x['title'] + '» y tengo una pregunta.')}</div></article></div></section>
<section class="section"><div class="wrap">{sec_head('Sigue leyendo', 'Más <em>consejos.</em>')}{blog_cards(others)}</div></section>""" + cta()
        page(f'consejo-{x["slug"]}.html', x['title'], x['excerpt'], body, 'consejos', x['img'], ld=[{'@context': 'https://schema.org', '@type': 'Article', 'headline': x['title'], 'description': x['excerpt'], 'image': R + x['img'] + '.webp', 'author': {'@type': 'Person', 'name': 'Shadia Cotelo'}, 'publisher': {'@type': 'Organization', 'name': 'Pelucans Peluquería Canina'}}])

# ----------------------------------------------------------------- INICIO
def home_page():
    import pro_pages
    pro_pages.home(globals())


def prod_card(p):
    im, name, price, text, msg = p
    return f'''<article class="prod reveal"><div class="ph">{img(im, name)}<span class="price">{price}</span></div><div class="tx"><h3>{name}</h3><p>{text}</p>{btn('Preguntar por WhatsApp', f'Hola Shadia, me interesa {msg}. ¿Lo tenéis disponible?', 'light')}</div></article>'''

# ----------------------------------------------------------------- SERVICIOS
def services_page():
    import servicios_pro
    servicios_pro.build(globals())

def faq(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}<i class="bi bi-plus-lg"></i></summary><p>{a}</p></details>' for q, a in items) + '</div>'

# ----------------------------------------------------------------- SERVICIO
def service_page(s, i):
    m = MEDIA[s['slug']]
    t = s['title'].replace('\n', '<br>')
    body = f'''<section class="p-hero"><div class="paw-bg"></div><div class="wrap p-hero-grid"><div><nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <a href="servicios.html">Servicios</a> / <span>{s['name']}</span></nav><span class="eyebrow">{s['cat']}</span><h1>{t}</h1><p class="lead">{s['intro']}</p><div class="hero-cta">{btn('Pedir cita para ' + s['name'].lower(), f"Hola Shadia, me gustaría pedir información y cita para {s['name']}.")}<a class="btn ghost" href="#detalle">Cómo lo hacemos {icon('arrow-down')}</a></div></div><div class="p-photo {'tall' if m['hero'].startswith('story') else ''} float">{img(m['hero'], s['name'] + ' en Pelucans', lazy=False, pos=m['pos'])}<span class="sticker">{m['sticker']}</span></div></div></section>'''
    body += f'''<section class="section tint" id="detalle"><div class="wrap two-col"><div>{heading('En qué consiste', 'El cuidado está<br>en los <em>detalles.</em>')}<div class="note reveal d2">{icon('heart-fill')}<span>Uno a uno, sin jaulas y respetando sus tiempos.</span></div></div><div class="prose reveal"><p class="lead">{s['detail']}</p><p>{s['extra']}</p></div></div></section>'''
    body += f'''<section class="section"><div class="wrap benefits">''' + ''.join(f'<article class="benefit reveal d{k}">{icon([s["icon"], "heart-fill", "check2-circle"][k])}<h3>{a}</h3><p>{b}</p></article>' for k, (a, b) in enumerate(s['benefits'])) + '</div></section>'
    body += f'''<section class="section sage"><div class="wrap split"><div class="p-photo reveal" style="rotate:-1.5deg">{img(m['hero2'], s['name'] + ': otro momento en Pelucans', pos='center 30%')}</div><div>{heading('Pensado para él', '¿Es lo que<br>necesita <em>tu perro?</em>', s['recommended'])}<div style="margin-top:1.4rem" class="reveal d2">{btn('Cuéntanos su caso', f"Hola Shadia, quería consultarte sobre {s['name']} para mi perro.")}</div></div></div></section>'''
    body += f'''<section class="section"><div class="wrap">{sec_head('Así lo cuidamos', 'Su sesión,<br>paso a <em>paso.</em>')}<div class="steps">''' + ''.join(f'<article class="step reveal d{k % 4}"><h3>{a}</h3><p>{b}</p></article>' for k, (a, b) in enumerate(s['steps'])) + '</div></div></section>'
    # extras específicos
    extra = ''
    if s['slug'] == 'ozonoterapia':
        extra += f'''<section class="section pink"><div class="wrap split"><div>{heading('Con las palabras de Shadia', '«Por suerte, el tratamiento<br>de ozono <em>me ayuda.</em>»', 'Así lo cuenta Pelucans en sus historias: una guía visual para entender cómo se vive la piel atópica y qué papel puede tener el ozono en el cuidado. Recuerda: ante picor persistente o heridas, primero consulta con tu veterinario.')}<div class="reveal d2" style="margin-top:1.4rem">{btn('Preguntar por el ozono', 'Hola Shadia, quería información sobre el baño de ozono.')}</div></div><div style="display:flex;gap:1rem;justify-content:center" data-lb-group>{''.join(f'<figure class="p-photo tall" data-lb="{R}{n}.webp" style="margin:0;width:46%;cursor:zoom-in;rotate:{r}deg">{img(n, a)}</figure>' for n, a, r in [('story-atopica', 'Historia de Pelucans: la piel atópica es un rollo', -3), ('story-ozono', 'Historia de Pelucans: tratamiento de ozono', 3)])}</div></div></section>'''
    if s['slug'] == 'dermocosmetica':
        extra += f'''<section class="section pink"><div class="wrap"><div class="sec-head"><div class="reveal"><span class="eyebrow">Marcas que usamos</span><h2>Profesionales,<br>para <em>casa también.</em></h2></div><p class="reveal d1">Trabajamos con PSH Pro Health y Artero. Si quieres llevarte algo para casa, mira nuestra tienda.</p></div><div class="brands reveal"><span>PSH Pro Health</span><span>Ozone Hard Shampoo</span><span>Ozone Sweet Conditioner</span><span>Artero</span><a class="btn" href="tienda.html">Ver la tienda</a></div></div></section>'''
    if m['reel']:
        c, im, tt, dd, kind, gen = m['reel']
        lab = 'Publicación · Instagram' if kind == 'p' else 'Reel · Instagram'
        extra += f'''<section class="section"><div class="wrap split"><button class="reel reveal" data-reel="{c}" data-kind="{kind}" style="max-width:340px;margin-inline:auto;width:100%" aria-label="Ver en Instagram: {tt}">{img(im, tt)}<span class="play">{icon("play-fill")}</span><span class="cap"><small>{lab}</small>{tt}</span></button><div>{heading('Un vistazo al salón' if gen else 'Míralo en acción', tt + '.', dd)}<p class="reveal d2">Pulsa para verlo con el reproductor de Instagram. No cargamos nada de Instagram hasta que tú lo decides.</p></div></div></section>'''
    body += extra
    body += f'''<section class="section"><div class="wrap">{sec_head('Del salón', 'Resultados <em>reales.</em>', 'Fotos de clientes de Pelucans. Pulsa para ampliar.')}<div class="strip" data-lb-group>''' + ''.join(f'<figure data-lb="{R}{n}.webp" class="reveal d{k}">{img(n, "Resultado en Pelucans: " + s["name"].lower())}</figure>' for k, n in enumerate(m['strip'])) + '</div></div></section>'
    body += f'''<section class="section tint"><div class="wrap two-col"><div>{heading('Te lo contamos con calma', 'Todo lo que<br>quieres <em>saber.</em>')}</div><div class="reveal">{faq(s['faq'])}</div></div></section>'''
    others = [(k, o) for k, o in enumerate(SERVICES) if o['slug'] != s['slug']]
    nxt = [others[(i + j) % len(others)] for j in range(3)]
    body += f'''<section class="section"><div class="wrap">{sec_head('Más cuidados', 'Quizá también<br>le <em>apetezca…</em>')}<div class="bento">''' + ''.join(service_card(o, k, False) for k, o in nxt) + '</div></div></section>'
    body += cta(f"Hola Shadia, me gustaría pedir información y cita para {s['name']}.", f'Reserva {s["name"].lower()} <em>sin prisas.</em>')
    page(f'servicio-{s["slug"]}.html', s['name'], s['short'] + ' En Pelucans, A Laracha. Atención individual con Shadia y cita por WhatsApp.', body, 'servicios', m['hero'] if not m['hero'].startswith('story') else m['hero2'], cls='pro', ld=[{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faq']]}, {'@context': 'https://schema.org', '@type': 'Service', 'name': s['name'], 'description': s['short'], 'areaServed': 'A Laracha, A Coruña', 'provider': {'@type': 'LocalBusiness', 'name': 'Pelucans Peluquería Canina', 'telephone': '+34604207678'}}])

# ----------------------------------------------------------------- TIENDA
def shop_page():
    body = f'''<section class="p-hero"><div class="paw-bg"></div><div class="wrap p-hero-grid"><div><nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Tienda</span></nav><span class="eyebrow">Tienda en el salón</span><h1>Todo para<br>su <em class="scribble">día a día.</em></h1><p class="lead">Cosmética profesional, juguetes KONG, arneses con diseño, chubasqueros y alimentación especializada. Y además, somos punto Vinted Go.</p><div class="hero-cta"><a class="btn wa" href="{CATALOGO}" target="_blank" rel="noopener">{icon('whatsapp')} Ver el catálogo en WhatsApp</a><a class="btn ghost" href="#vinted">Punto Vinted Go {icon('arrow-down')}</a></div></div><div class="p-photo float">{img('story-kong', 'Juguetes KONG y accesorios en la tienda de Pelucans', lazy=False)}<span class="sticker">recién llegado</span></div></div></section>'''
    body += f'''<section class="section"><div class="wrap">{sec_head('Catálogo de WhatsApp', 'Lo que hay<br>en las <em>estanterías.</em>', 'Estos son los artículos de su catálogo de WhatsApp Business. Consulta stock y formatos escribiendo a Shadia.')}<div class="shop-grid">{''.join(prod_card(p) for p in PRODUCTS)}</div><p style="margin-top:1.4rem;font-size:.9rem;color:var(--ink-2)">Precios del catálogo de WhatsApp consultados el 18 de noviembre de 2026; confirma precio y disponibilidad al pedir.</p></div></section>'''
    more = [('story-chubasqueros', 'Chubasqueros reversibles', 'Para la lluvia, abrigos y chubasqueros que protegen y calientan. ¡Mira los reversibles!', 'los chubasqueros reversibles'), ('story-raindrops', 'Raindrops', 'Impermeable, con cierre de velcro cómodo y apertura para la correa. Para paseos sin complicaciones.', 'el chubasquero Raindrops'), ('story-arneses', 'Arneses Body', 'Los arneses Body más molones ya están aquí. Para que tu peludo pasee con estilo.', 'los arneses Body'), ('story-artero', 'Cosmética Artero', 'Impact, Tierra, Fresh y Violet: la línea profesional que usamos en el baño, también para casa.', 'la cosmética Artero'), ('story-psh', 'PSH Ozone', 'Ozone Hard Shampoo y Ozone Sweet Conditioner, formulados para el cuidado de la piel.', 'PSH Ozone'), ('story-colonias', 'Colonias y perfumes', 'Citric y Puppy Fragrance para un acabado que huele a recién bañado.', 'las colonias PSH')]
    body += f'''<section class="section sage"><div class="wrap">{sec_head('Más en tienda', 'Novedades de<br>sus <em>historias.</em>', 'Pregunta precio y stock de lo que ves en sus destacados de Instagram.', f'<button class="btn light reveal d2" data-hl="productos">{icon("play-circle")} Ver destacado de Productos</button>')}<div class="shop-grid">''' + ''.join(f'<article class="prod reveal"><div class="ph" data-lb="{R}{im}.webp" style="cursor:zoom-in">{img(im, n)}</div><div class="tx"><h3>{n}</h3><p>{tx}</p>{btn("Pedir información", f"Hola Shadia, me gustaría información (precio y stock) sobre {msg}.", "light")}</div></article>' for im, n, tx, msg in more) + '</div></div></section>'
    body += f'''<section class="section" id="vinted"><div class="wrap"><div class="vinted"><div class="reveal" data-lb="{R}story-vinted.webp" style="cursor:zoom-in">{img('story-vinted', 'Pelucans es punto de recogida Vinted Go')}</div><div>{heading('También en Pelucans', 'Tu punto<br><em>Vinted Go.</em>', 'Recoge tus compras de Vinted en nuestro local y también puedes devolver tus envíos. Un servicio cómodo, rápido y seguro mientras tu peludo se pone guapo.')}<ul class="ticks reveal d2"><li>{icon('box-seam')}<span>Recogida de paquetes de Vinted en el salón.</span></li><li>{icon('arrow-repeat')}<span>Devoluciones y envíos.</span></li><li>{icon('geo-alt')}<span>Avda. Doutor López Astray, 40 bajo, A Laracha.</span></li></ul><p class="reveal d3" style="font-size:.92rem;color:var(--ink-2)">Consulta las instrucciones y la disponibilidad en la aplicación de Vinted antes de acercarte.</p><div class="reveal d3"><a class="btn" href="contacto.html#ubicacion">Cómo llegar</a></div></div></div></div></section>'''
    body += f'''<section class="section tint"><div class="wrap two-col"><div>{heading('Alimentación especializada', 'Su cuenco<br>también <em>importa.</em>', 'Pregúntanos por las opciones de alimentación disponibles. Si necesita una dieta clínica, sigue siempre la pauta de su veterinario.')}<div class="reveal d2" style="margin-top:1.4rem"><a class="btn" href="servicio-comida-especializada.html">Más información</a></div></div><div class="faq reveal">{faq([('¿Cómo hago un pedido?', 'Escribe por WhatsApp con el producto, formato y cantidad. Te confirmamos disponibilidad y cuándo puedes pasar a recogerlo.'), ('¿Puedo comprar sin reservar peluquería?', 'Sí. Escríbenos y quedamos para que pases a recogerlo cuando te venga bien.'), ('¿Hacéis envíos?', 'Por ahora los productos se recogen en el salón. Pregunta a Shadia si necesitas otra opción.')])}</div></div></section>''' + cta('Hola Shadia, me gustaría consultar productos de la tienda.', '¿Buscas algo <em>en concreto?</em>')
    page('tienda.html', 'Tienda y punto Vinted Go', 'Tienda de Pelucans en A Laracha: colonias PSH, juguetes KONG, arneses, chubasqueros, cosmética Artero y punto de recogida Vinted Go. Catálogo en WhatsApp.', body, 'tienda', 'story-kong')

# ----------------------------------------------------------------- GALERÍA
def gallery_page():
    import pro_pages
    pro_pages.gallery(globals())


# ----------------------------------------------------------------- NOSOTROS
def about_page():
    body = f'''<section class="p-hero"><div class="paw-bg"></div><div class="wrap p-hero-grid"><div><nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Nosotros</span></nav><span class="eyebrow">Quién hay detrás</span><h1>Hola, soy Shadia.<br>Y ella es <em class="scribble">Bimba.</em></h1><p class="lead">Después de muchos años trabajando en el sector, decidí montar mi propio negocio. Bimba, mi bulldog francés, es la razón de todo esto.</p><div class="hero-cta">{btn('Hablemos')}</div></div><div class="p-photo float">{img('shadia-bimba-2', 'Shadia Cotelo con su bulldog francés Bimba', lazy=False, pos='center 28%')}<span class="sticker">Shadia + Bimba ♡</span></div></div></section>'''
    body += f'''<section class="section tint"><div class="wrap two-col"><div>{heading('Mi historia', 'Una vocación<br>que viene de <em>lejos.</em>')}</div><div class="timeline reveal"><div class="tl"><b>2014 · El comienzo</b>Empiezo mi camino con los animales, formándome como auxiliar veterinaria y peluquera canina profesional.</div><div class="tl"><b>Años de oficio</b>Trabajo en Ponteceso, Pazos y A Coruña. Aprendo que cada perro pide un ritmo distinto.</div><div class="tl"><b>Nace Pelucans</b>Abro mi propio salón en la Avda. Doutor López Astray, 40, en A Laracha, con Bimba como inspiración.</div><div class="tl"><b>Hoy</b>5,0 en Google con 208 opiniones, clientes que repiten cada 15 días y un punto Vinted Go en la puerta.</div></div></div></section>'''
    body += f'''<section class="section"><div class="wrap split"><div class="photo-stack reveal"><figure class="p1">{img('shadia-bimba-1', 'Shadia y Bimba en la peluquería', pos='center 25%')}</figure><figure class="p2">{img('wacho', 'Wacho, mastín, en su sesión de mantenimiento')}</figure><span class="stick">con mucho<br>cariño</span></div><div><div class="quote reveal">«Porque una buena peluquería canina no es solo que salgan guapos… también es cuidar de su bienestar durante todo el proceso.»<cite>— Shadia Cotelo</cite></div><p class="reveal d1" style="margin-top:1.4rem">En Pelucans cada detalle está hecho con paciencia, dedicación y mucho cariño. Por eso trabajamos uno a uno, sin jaulas, con orejeras protectoras en el secado y con tiempo de sobra para los grandullones.</p></div></div></section>'''
    body += f'''<section class="section sage"><div class="wrap">{sec_head('Nuestra forma de hacer las cosas', 'El tiempo también<br>es un <em>cuidado.</em>')}<div class="values"><article class="value reveal"><span>01 · tranquilidad</span><h3>Uno a uno.<br>De verdad.</h3><p>Atención individual y sin jaulas. Organizamos las citas para dedicarle el espacio y la atención que necesita.</p></article><article class="value reveal d1"><span>02 · paciencia</span><h3>Sin mirar<br>el reloj.</h3><p>Si un perro grande necesita una tarde entera, reservamos ese tiempo para cuidarlo con calma, como a Bruce.</p></article><article class="value reveal d2"><span>03 · cercanía</span><h3>Nos cuentas.<br>Te escuchamos.</h3><p>Su carácter y vuestra rutina importan tanto como el acabado. Hablamos contigo antes de empezar.</p></article></div></div></section>'''
    body += f'''<section class="section"><div class="wrap">{sec_head('Los protagonistas', 'Clientes que son<br><em>de la casa.</em>')}<div class="shop-grid">''' + ''.join(f'<article class="prod reveal d{k}"><div class="ph">{img(im, n, pos="center 30%")}</div><div class="tx"><h3>{n}</h3><p>{tx}</p></div></article>' for k, (im, n, tx) in enumerate([('shadia-bimba-2', 'Bimba', 'Bulldog francés y fundadora honoraria. «La razón de todo esto.»'), ('bruce-bano-1', 'Bruce', 'San Bernardo. Todo lo que tiene de grande lo tiene de amoroso. Se lleva una tarde entera de mimos.'), ('wacho', 'Wacho', 'Mastín y cliente fiel: viene cada 15 días a su sesión de mantenimiento de ozono.')])) + '</div></div></section>'
    body += f'''<section class="section tint"><div class="wrap two-col"><div>{heading('Lo que usamos', 'Equipo y cosmética<br><em>profesional.</em>')}</div><div class="reveal"><p class="lead">Bañera de acero inoxidable para todos los tamaños, orejeras protectoras en el secado y cosmética formulada para perros.</p><div class="brands"><span>PSH Pro Health</span><span>Artero</span><span>Orejeras anti-ruido</span><span>Bañera profesional</span></div></div></div></section>''' + cta()
    page('nosotros.html', 'Shadia, Bimba y nuestra forma de cuidar', 'Conoce a Shadia Cotelo, groomer en A Laracha desde 2014, y a Bimba, su bulldog francés. Atención uno a uno, sin jaulas, con orejeras en el secado.', body, 'nosotros', 'shadia-bimba-2')

# ----------------------------------------------------------------- CONTACTO
def contact_page():
    opts = '<option value="">Ayúdame a elegir</option>' + ''.join(f'<option>{s["name"]}</option>' for s in SERVICES) + '<option>Tienda / productos</option>'
    body = f'''<section class="p-hero"><div class="paw-bg"></div><div class="wrap p-hero-grid"><div><nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Contacto</span></nav><span class="eyebrow">Pide tu cita</span><h1>Su próximo cuidado<br>empieza con un <em class="scribble">hola.</em></h1><p class="lead">Cuéntanos cómo es tu perro y qué necesita. Te responderemos para acordar el servicio, el presupuesto y su cita.</p><a class="big-phone" href="tel:+34604207678">{icon('telephone-fill')} {PHONE}</a><div class="hero-cta" style="margin-top:0">{btn()}<a class="btn light" href="{IG_DM}" target="_blank" rel="noopener">{icon('instagram')} Escribir por Instagram</a></div></div><div class="p-photo float">{img('fachada', 'Fachada de Pelucans en la Avenida Doutor López Astray', lazy=False)}<span class="sticker">¡aquí estamos!</span></div></div></section>'''
    body += f'''<section class="section tint"><div class="wrap contact-grid"><div>{heading('Hablemos de tu peludo', '¿Le guardamos<br>un <em>momento?</em>', 'Rellena lo que quieras contarnos. Prepararemos el mensaje para que lo revises y lo envíes por WhatsApp.')}<div class="hours reveal d1" style="margin-top:1.6rem"><h3>Cuándo venir <span class="open-pill" data-open>Horario</span></h3><div class="hour-row" data-day="1-5"><span>Lunes a viernes</span><strong>9:30–13:30<br>16:00–19:00</strong></div><div class="hour-row" data-day="6"><span>Sábados</span><strong>Con cita previa</strong></div><div class="hour-row" data-day="0"><span>Domingos</span><strong>Cerrado</strong></div></div></div>
<form class="form reveal d1" id="booking-form"><span class="eyebrow">Su primer hola</span><h2 style="font-size:2.2rem">Cuéntanos un poquito.</h2><div class="form-grid"><label>Tu nombre *<input name="name" autocomplete="given-name" required maxlength="80" placeholder="¿Cómo te llamas?"></label><label>Nombre de tu perro *<input name="dog" required maxlength="80" placeholder="El protagonista"></label><label>Raza o tamaño<input name="breed" maxlength="100" placeholder="Mestizo, 12 kg…"></label><label>¿Qué necesita?<select name="service">{opts}</select></label><label>Día preferido<input type="date" name="date" data-date><small class="hint" data-date-hint>Lunes a viernes, y sábados con cita previa.</small></label><fieldset class="chips"><legend>Franja</legend><label><input type="radio" name="time" value="Me adapto" checked><span>Me adapto</span></label><label><input type="radio" name="time" value="Por la mañana"><span>Por la mañana · 9:30–13:30</span></label><label><input type="radio" name="time" value="Por la tarde"><span>Por la tarde · 16:00–19:00</span></label></fieldset><label class="full">Algo que debamos saber<textarea name="notes" rows="3" maxlength="800" placeholder="Es su primera visita, se asusta con el secador…"></textarea></label></div><p class="form-note">No guardamos este formulario. Al continuar se abre WhatsApp; el mensaje solo se envía cuando tú lo confirmas allí.</p><div class="preview"><span class="eyebrow">Así quedará tu mensaje</span><pre data-preview aria-live="polite"></pre></div><div class="form-actions"><button class="btn wa" type="submit">{icon('whatsapp')} Preparar mi consulta</button><button class="btn light" type="button" data-copy>{icon('clipboard')} Copiar mensaje</button></div><p class="form-status" aria-live="polite"></p></form></div></section>'''
    body += area_map()
    body += f'''<section class="section" id="ubicacion"><div class="wrap">{sec_head('Nos vemos en A Laracha', 'Muy cerca.<br>Muy fácil <em>llegar.</em>', 'Avda. Doutor López Astray, 40 bajo · 15145 A Laracha, A Coruña. Con sitio para aparcar.')}<div class="visit"><div class="facade reveal">{img('fachada', 'Fachada de Pelucans')}<div class="tagline">Busca el cristal con la huella y el cartel «Pelucans».</div></div><div class="map-panel reveal d1" id="map-panel"><div><h3>Tu próxima parada: Pelucans</h3><p>Carga el mapa de Google para ver la ubicación. Al hacerlo, conectarás con Google Maps.</p><button class="btn" id="load-map">{icon('geo-alt-fill')} Ver mapa interactivo</button><p style="margin-top:1rem"><a class="link-arrow" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=Pelucans+Peluquer%C3%ADa+Canina+Avenida+Doutor+L%C3%B3pez+Astray+40+A+Laracha">Abrir ruta en Google Maps ↗</a></p></div></div></div></div></section>'''
    body += f'''<section class="section sage"><div class="wrap split"><div>{heading('También en Pelucans', 'Punto <em>Vinted Go.</em>', 'Recoge y devuelve tus paquetes de Vinted en el salón.')}<div class="reveal d2" style="margin-top:1.2rem"><a class="btn" href="tienda.html#vinted">Más información</a></div></div><div class="socials reveal d1" style="justify-content:flex-start"><a href="{IG}" target="_blank" rel="noopener">{icon('instagram')} Instagram</a><a href="{FB}" target="_blank" rel="noopener">{icon('facebook')} Facebook</a><a href="{GOOGLE}" target="_blank" rel="noopener">{icon('google')} Reseñas en Google</a><a href="{CATALOGO}" target="_blank" rel="noopener">{icon('whatsapp')} Catálogo WhatsApp</a><a href="{PAXINAS}" target="_blank" rel="noopener">{icon('journal-text')} Páxinas Galegas</a><a href="{AMARILLAS}" target="_blank" rel="noopener">{icon('journal-bookmark')} Páginas Amarillas</a></div></div></section>'''
    page('contacto.html', 'Contacto y cita por WhatsApp', 'Pide cita en Pelucans, peluquería canina en A Laracha. Teléfono y WhatsApp 604 207 678. Avda. Doutor López Astray, 40. Horario, mapa y parking.', body, 'contacto', 'fachada')

def not_found():
    body = f'''<section class="s-hero"><div class="wrap" style="max-width:760px;text-align:center;padding-block:clamp(3rem,8vw,6rem)"><span class="eyebrow" style="justify-content:center">Error 404</span><h1>Esta página<br><em>no existe.</em></h1><p class="lead" style="margin-inline:auto">Puede que el enlace esté roto o que la página haya cambiado de sitio. Te llevamos de vuelta a lo importante.</p><div class="s-cta" style="justify-content:center"><a class="btn" href="index.html">Volver al inicio</a><a class="s-link" href="servicios.html">Ver los servicios {icon('arrow-up-right')}</a></div></div></section>'''
    page('404.html', 'Página no encontrada', 'La página que buscas no existe. Vuelve al inicio de Pelucans, peluquería canina en A Laracha.', body, '', 'fachada')


def seo_files():
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n' + (f'Sitemap: {SITE_URL}sitemap.xml\n' if SITE_URL else ''), encoding='utf-8')
    if not SITE_URL:
        return
    pages = sorted(f.name for f in ROOT.glob('*.html') if f.name != '404.html')
    urls = ''.join(f'<url><loc>{SITE_URL}{n}</loc><xhtml:link rel="alternate" hreflang="es" href="{SITE_URL}{n}"/><xhtml:link rel="alternate" hreflang="gl" href="{SITE_URL}gl/{n}"/></url><url><loc>{SITE_URL}gl/{n}</loc><xhtml:link rel="alternate" hreflang="es" href="{SITE_URL}{n}"/><xhtml:link rel="alternate" hreflang="gl" href="{SITE_URL}gl/{n}"/></url>' for n in pages)
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + '</urlset>', encoding='utf-8')


home_page(); services_page(); shop_page(); gallery_page(); about_page(); contact_page(); advice_page(); advice_post_pages(); not_found(); seo_files()
for i, s in enumerate(SERVICES): service_page(s, i)
n = i18n.report()
print('Generadas', len(list(ROOT.glob('*.html'))), 'páginas por idioma. Textos pendientes de traducir:', n)
