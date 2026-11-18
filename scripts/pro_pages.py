"""Portada y galería · dirección premium, ordenada y explicada.
Reutiliza los ayudantes de build.py (se pasan en `g`, que es globals())."""

RING = '<svg class="s-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="ring" d="M100,100 m-80,0 a80,80 0 1,1 160,0 a80,80 0 1,1 -160,0"/></defs><text><textPath href="#ring" textLength="498" lengthAdjust="spacing">PELUCANS · PELUQUERÍA CANINA · A LARACHA · </textPath></text></svg>'


def hero(g, kicker, h1, lead, ctas, facts, main, small, note, crumb=None):
    img = g['img']
    cr = f'<nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <span>{crumb}</span></nav>' if crumb else ''
    fx = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in facts)
    return f'''<section class="s-hero"><div class="wrap s-hero-grid"><div class="s-hero-copy">{cr}<span class="eyebrow">{kicker}</span><h1>{h1}</h1><p class="lead">{lead}</p><div class="s-cta">{ctas}</div><dl class="s-facts">{fx}</dl></div><div class="s-hero-art"><figure class="s-main">{img(main[0], main[1], lazy=False, pos=main[2])}</figure><figure class="s-small">{img(small[0], small[1], lazy=False)}</figure>{RING}<span class="s-note">{note}</span></div></div></section>'''


def ribbon(words):
    return '<div class="s-ribbon marquee" aria-hidden="true"><div class="marquee-track">' + ''.join(f'<span>{w}</span>' for w in words) + '</div></div>'


def index_rows(g, cats=True):
    SERVICES, MEDIA, R, icon = g['SERVICES'], g['MEDIA'], g['R'], g['icon']
    rows = ''
    for i, x in enumerate(SERVICES):
        m = MEDIA[x['slug']]
        thumb = f'{R}{m["hero2"] if m["hero"].startswith("story") else m["hero"]}.webp'
        rows += f'''<li class="idx-row" data-cat="{x['cat']}"><a href="servicio-{x['slug']}.html"><span class="n">{i + 1:02d}</span><span class="th"><img src="{thumb}" alt="" loading="lazy"></span><span class="t">{x['name']}</span><span class="d">{x['short']}</span><span class="c">{x['cat']}</span><span class="go" aria-hidden="true">{icon('arrow-up-right')}</span></a></li>'''
    return f'<ol class="idx reveal">{rows}</ol>'


def reviews3(g, kicker='Lo que dicen sus familias'):
    REVIEWS, GOOGLE = g['REVIEWS'], g['GOOGLE']
    pick = [r for r in REVIEWS if r[0] in ('Sara', 'María Quintana', 'Duque Caxias')]
    rv = ''.join(f'<figure class="rv reveal d{i}"><div class="stars" aria-label="5 estrellas">★★★★★</div><blockquote>«{t}»</blockquote><figcaption><b>{n}</b><span>{src}</span></figcaption></figure>' for i, (n, t, src) in enumerate(pick))
    return f'''<div class="s-rv-head reveal"><span class="eyebrow">{kicker}</span><a class="s-rating" href="{GOOGLE}" target="_blank" rel="noopener"><b>5,0</b><span class="stars">★★★★★</span><small>208 opiniones en Google ↗</small></a></div><div class="rvs">{rv}</div>'''


# =================================================================== PORTADA
def home(g):
    img, icon, btn, heading, sec_head = g['img'], g['icon'], g['btn'], g['heading'], g['sec_head']
    R, GOOGLE, IG, FB, page = g['R'], g['GOOGLE'], g['IG'], g['FB'], g['page']
    ba_carousel, reels_block, visit_block, cta, HIGHLIGHTS, PRODUCTS = g['ba_carousel'], g['reels_block'], g['visit_block'], g['cta'], g['HIGHLIGHTS'], g['PRODUCTS']

    h = hero(g, 'Peluquería canina · A Laracha', 'Más que un corte,<br><em>es amor y cuidado.</em>',
             'Peluquería canina con Shadia: corte a tijera, deslanado, stripping y baño de ozono. Atendemos uno a uno, sin jaulas y sin prisas, con todo el tiempo que tu perro necesita.',
             btn('Pedir cita por WhatsApp') + '<a class="s-link" href="#cuidados">Ver los cuidados ' + icon('arrow-down') + '</a>',
             [('9', 'cuidados<br>a su medida'), ('1:1', 'atención<br>individual'), ('5,0', 'en Google<br>· 208 opiniones')],
             ('shadia-bimba-1', 'Shadia Cotelo con su perrita Bimba en Pelucans', 'center 30%'), ('bruce-bano-1', 'Bruce, un San Bernardo, durante su baño'), 'Shadia + Bimba')
    h = h.replace('<figure class="s-small">' + img('bruce-bano-1', 'Bruce, un San Bernardo, durante su baño', lazy=False) + '</figure>', '<figure class="s-small">' + img('bruce-bano-1', 'Bruce, un San Bernardo, durante su baño', lazy=False, pos='center 40%') + '</figure>')

    cuidados = f'''<section class="s-index" id="cuidados"><div class="wrap"><header class="s-head"><div class="reveal"><span class="eyebrow">Nuestros cuidados</span><h2>Nueve cuidados,<br>un mismo <em>cariño.</em></h2></div><div class="reveal d1"><p>Todos se hacen con cita previa y a su ritmo. Entra en cada uno para ver cómo lo hacemos, qué incluye y a qué perros va dirigido.</p><a class="btn" href="servicios.html">Ver todos los servicios {icon('arrow-right')}</a></div></header>{index_rows(g)}</div></section>'''

    puntos = [('Atención uno a uno', 'Trabajamos con un solo perro cada vez para dedicarle toda la atención.'),
              ('Sin jaulas, sin prisas', 'No hay jaulas de espera y reservamos el tiempo que cada manto necesita.'),
              ('Orejeras en el secado', 'Protegemos sus oídos del ruido del secador cuando lo necesitan.'),
              ('Para todos los tamaños', 'Bañera de acero inoxidable adaptada a razas gigantes: desde un maltés hasta un San Bernardo.')]
    lst = ''.join(f'<li class="reveal d{i}"><span class="n">{i + 1:02d}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(puntos))
    como = f'''<section class="s-how"><div class="wrap s-how-grid"><div class="s-how-art reveal"><figure class="a">{img('bruce-bano-2', 'Shadia secando a Bruce en la bañera profesional de acero inoxidable', pos='center 30%')}</figure><figure class="b">{img('orejeras', 'Perrito con orejeras protectoras rosas durante el secado')}</figure></div><div>{heading('Cómo cuidamos', 'Aquí se viene<br>a estar <em>a gusto.</em>', 'Una buena peluquería canina no es solo que salgan guapos… también es cuidar de su bienestar durante todo el proceso.')}<ol class="s-points">{lst}</ol><div class="reveal d3" style="margin-top:2rem"><a class="s-link" href="nosotros.html">Conoce a Shadia y a Bimba {icon('arrow-up-right')}</a></div></div></div></section>'''

    antes = f'''<section class="section tint s-ba"><div class="wrap">{sec_head('Antes y después', 'El cambio<br>se <em>nota.</em>', 'Desliza cada foto para comparar. Son sesiones reales en el salón: sin filtros y sin retoques.')}</div><div class="reveal">{ba_carousel()}</div></section>'''

    opiniones = f'<section class="s-voices"><div class="wrap">{sec_head("Opiniones", "El cariño se nota.<br>Y <em>se cuenta.</em>", "Reseñas de familias que repiten: unas de Google, otras de las historias de Instagram y de Páxinas Galegas.")}{reviews3(g, "Lo que dicen")}</div></section>'

    hl = ''.join(f'<button class="hl-btn" data-hl="{k}"><span class="hl-ring">{img("hl-" + k, "Destacado " + n)}</span>{n}</button>' for k, n in HIGHLIGHTS)
    dia = f'''<section class="section"><div class="wrap">{sec_head('Su día a día', 'Un día en <em>Pelucans.</em>', 'Los destacados y reels de su Instagram, sin salir de la web. Pulsa un círculo para recorrerlo o un reel para verlo con sonido.', f'<a class="btn light reveal d2" href="{IG}" target="_blank" rel="noopener">{icon("instagram")} Seguir en Instagram</a>')}<div class="hl-row reveal">{hl}</div>{reels_block()}</div></section>'''

    thumbs = ''.join(f'<span>{img(im, n)}</span>' for im, n, _, _, _ in PRODUCTS)
    tienda = f'''<section class="s-shop"><div class="wrap s-shop-in"><div class="reveal"><span class="eyebrow">Tienda en el salón</span><h2>Para casa, para el paseo,<br>para <em>la lluvia.</em></h2><p>Cosmética PSH y Artero, juguetes KONG, arneses con diseño y chubasqueros reversibles. Consulta stock y precios en su catálogo de WhatsApp. También somos punto de recogida Vinted Go.</p><div style="display:flex;flex-wrap:wrap;gap:.8rem"><a class="btn" href="tienda.html">Ver la tienda</a><a class="btn light" href="https://wa.me/c/34604207678" target="_blank" rel="noopener">{icon("whatsapp")} Catálogo en WhatsApp</a></div></div><div class="s-shop-thumbs reveal d1">{thumbs}</div></div></section>'''

    body = h + ribbon(['Corte a tijera', 'Deslanado', 'Stripping', 'Baño de ozono', 'Dermocosmética', 'Corte de uñas', 'Asesoramiento', 'Tienda']) + cuidados + como + antes + opiniones + dia + tienda + visit_block() + cta()
    page('index.html', 'Peluquería canina en A Laracha', 'Peluquería canina en A Laracha con Shadia: corte a tijera, deslanado, stripping, baño de ozono y dermocosmética. Atención uno a uno, sin jaulas. Pide cita: 604 207 678.', body, 'inicio', 'shadia-bimba-1', True)


# =================================================================== GALERÍA
def gallery(g):
    img, icon, btn, heading, sec_head = g['img'], g['icon'], g['btn'], g['heading'], g['sec_head']
    R, IG, page, CLIENTES, cl = g['R'], g['IG'], g['page'], g['CLIENTES'], g['cl']
    ba_carousel, reels_block, ig_block, cta, HIGHLIGHTS = g['ba_carousel'], g['reels_block'], g['ig_block'], g['cta'], g['HIGHLIGHTS']
    n = len(CLIENTES)
    h = hero(g, 'Galería', 'Fotos reales,<br><em>peludos de verdad.</em>',
             'Todo lo que ves aquí sale del Instagram de Pelucans: sus publicaciones, destacados y reels. Sin fotos de archivo.',
             f'<a class="btn" href="{IG}" target="_blank" rel="noopener">{icon("instagram")} Seguir en Instagram</a><a class="s-link" href="#album">Ver el álbum {icon("arrow-down")}</a>',
             [(f'+{n}', 'fotos de<br>clientes'), ('6', 'destacados<br>de Instagram'), ('4', 'reels<br>del salón')],
             ('cliente-80', 'Un perro posando frente al cristal de Pelucans', 'center 25%'), ('cliente-26', 'Un goldendoodle recién arreglado en Pelucans'), 'Del Instagram de Pelucans', crumb='Galería')
    hl = ''.join(f'<button class="hl-btn" data-hl="{k}"><span class="hl-ring">{img("hl-" + k, "Destacado " + n_)}</span>{n_}</button>' for k, n_ in HIGHLIGHTS)
    dest = f'<section class="section"><div class="wrap">{sec_head("Destacados", "Los seis <em>destacados.</em>", "Los mismos de su perfil: clientes, productos, Vinted Go, servicios, horario y reseñas. Pulsa un círculo para recorrerlo a pantalla completa.")}<div class="hl-row reveal">{hl}</div></div></section>'
    reels = f'<section class="section tint"><div class="wrap">{sec_head("Reels", "Con <em>movimiento.</em>", "Cuatro vídeos del salón. Se abren con el reproductor oficial de Instagram solo cuando los pulsas.")}{reels_block()}</div></section>'
    antes = f'<section class="section s-ba"><div class="wrap">{sec_head("Antes y después", "El cambio<br>se <em>nota.</em>", "Desliza cada foto para comparar.")}</div><div class="reveal">{ba_carousel()}</div></section>'
    figs = ''.join(f'<figure class="reveal{" extra" if i >= 12 else ""}" data-lb="{R}{cl(k)}.webp">{img(cl(k), "Un cliente de Pelucans")}</figure>' for i, k in enumerate(CLIENTES))
    album = f'''<section class="section tint" id="album"><div class="wrap">{sec_head('Álbum', 'Caras felices,<br>colas <em>moviéndose.</em>', f'Fotos de clientes tomadas de los destacados de Instagram. Pulsa una foto para verla grande y usa las flechas para recorrerlas.')}<div class="album" data-lb-group>{figs}</div><div class="album-more"><button class="btn light" data-more aria-expanded="false">Ver las {n} fotos</button></div></div></section>'''
    body = h + dest + reels + antes + album + ig_block() + cta()
    page('galeria.html', 'Galería de peludos', 'Galería real de Pelucans: fotos y reels de perros de todos los tamaños en la peluquería canina de A Laracha. Destacados de Instagram y antes y después.', body, 'galeria', 'cliente-80')
