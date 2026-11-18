"""Página de servicios · dirección premium y editorial.
Se construye con los ayudantes de build.py (se pasan en `g`, que es globals())."""


def build(g):
    img, icon, btn, heading, sec_head = g['img'], g['icon'], g['btn'], g['heading'], g['sec_head']
    SERVICES, MEDIA, R, PHONE, GOOGLE = g['SERVICES'], g['MEDIA'], g['R'], g['PHONE'], g['GOOGLE']
    faq, cta, quiz_block, showcase, page, REVIEWS = g['faq'], g['cta'], g['quiz_block'], g['showcase'], g['page'], g['REVIEWS']

    # ------------------------------------------------------------ HERO
    badge = '<svg class="s-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="ring" d="M100,100 m-80,0 a80,80 0 1,1 160,0 a80,80 0 1,1 -160,0"/></defs><text><textPath href="#ring" textLength="498" lengthAdjust="spacing">PELUCANS · PELUQUERÍA CANINA · A LARACHA · </textPath></text></svg>'
    hero = f'''<section class="s-hero"><div class="wrap s-hero-grid"><div class="s-hero-copy">
<nav class="crumbs" aria-label="Migas"><a href="index.html">Inicio</a> / <span>Servicios</span></nav>
<span class="eyebrow">Carta de cuidados</span>
<h1>Nueve cuidados.<br><em>Un mismo cariño.</em></h1>
<p class="lead">Del corte a tijera al baño de ozono: cada servicio se hace uno a uno, sin jaulas y con todo el tiempo que tu perro necesita. Elige el suyo o cuéntanos y lo decidimos juntos.</p>
<div class="s-cta">{btn('Pedir cita por WhatsApp')}<a class="s-link" href="#indice">Ver el índice {icon('arrow-down')}</a></div>
<dl class="s-facts"><div><dt>9</dt><dd>cuidados<br>a su medida</dd></div><div><dt>1:1</dt><dd>atención<br>individual</dd></div><div><dt>5,0</dt><dd>en Google<br>· 208 opiniones</dd></div></dl>
</div><div class="s-hero-art">
<figure class="s-main">{img('ozono-shadia-wacho', 'Shadia secando a Wacho en la bañera de Pelucans', lazy=False, pos='center 35%')}</figure>
<figure class="s-small">{img('cliente-26', 'Un goldendoodle recién arreglado en Pelucans', lazy=False)}</figure>
{badge}
<span class="s-note">Shadia · Pelucans</span>
</div></div></section>'''

    # ------------------------------------------------------------ CINTA FINA
    words = ['Corte a tijera', 'Deslanado', 'Stripping', 'Baño de ozono', 'Dermocosmética', 'Corte de uñas', 'Asesoramiento', 'Tienda']
    ribbon = '<div class="s-ribbon marquee" aria-hidden="true"><div class="marquee-track">' + ''.join(f'<span>{w}</span>' for w in words) + '</div></div>'

    # ------------------------------------------------------------ ÍNDICE
    cats = ['Todos', 'Estilismo', 'Manto e higiene', 'Piel y bienestar', 'En casa']
    tabs = ''.join(f'<button data-f="{c}" aria-pressed="{str(i == 0).lower()}" class="{"active" if i == 0 else ""}">{c}</button>' for i, c in enumerate(cats))
    rows = ''
    for i, x in enumerate(SERVICES):
        m = MEDIA[x['slug']]
        thumb = f'{R}{m["hero2"] if m["hero"].startswith("story") else m["hero"]}.webp'
        rows += f'''<li class="idx-row" data-cat="{x['cat']}"><a href="servicio-{x['slug']}.html"><span class="n">{i + 1:02d}</span><span class="th"><img src="{thumb}" alt="" loading="lazy"></span><span class="t">{x['name']}</span><span class="d">{x['short']}</span><span class="c">{x['cat']}</span><span class="go" aria-hidden="true">{icon('arrow-up-right')}</span></a></li>'''
    index = f'''<section class="s-index" id="indice"><div class="wrap">
<header class="s-head"><div class="reveal"><span class="eyebrow">Índice</span><h2>Encuentra<br>su <em>cuidado.</em></h2></div><div class="reveal d1"><p>Filtra por tipo de cuidado o entra en cualquiera para ver cómo lo hacemos, qué incluye y a qué perros va dirigido.</p><div class="s-tabs" role="group" aria-label="Filtrar servicios">{tabs}</div></div></header>
<ol class="idx reveal">{rows}</ol></div></section>'''

    # ------------------------------------------------------------ CÓMO ES UNA CITA
    steps = [('Escríbenos', 'Por WhatsApp o por teléfono. Cuéntanos cómo es tu perro, qué necesita y si tiene alguna sensibilidad.'),
             ('Reservamos su hueco', 'Cita previa y tiempo solo para él. Si es grande o tiene mucho pelo, reservamos de más.'),
             ('Una sesión sin prisas', 'Uno a uno, sin jaulas, con pausas y orejeras protectoras en el secado si las necesita.'),
             ('A casa, feliz', 'Te explicamos cómo mantener el resultado y cada cuánto conviene volver.')]
    st = ''.join(f'<li class="reveal d{i}"><span class="n">{i + 1:02d}</span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps))
    process = f'''<section class="s-process"><div class="wrap">{sec_head('Cómo es una cita', 'Tranquila de<br>principio a <em>fin.</em>')}<ol class="s-steps">{st}</ol></div></section>'''

    # ------------------------------------------------------------ CITA DE SHADIA + RESEÑAS
    pick = [r for r in REVIEWS if r[0] in ('Sara', 'María Quintana', 'Duque Caxias')]
    rv = ''.join(f'<figure class="rv reveal d{i}"><div class="stars" aria-label="5 estrellas">★★★★★</div><blockquote>«{t}»</blockquote><figcaption><b>{n}</b><span>{src}</span></figcaption></figure>' for i, (n, t, src) in enumerate(pick))
    voices = f'''<section class="s-voices"><div class="wrap"><div class="s-quote reveal"><figure class="portrait">{img('shadia-bimba-2', 'Shadia Cotelo con su perrita Bimba', pos='center 25%')}</figure><blockquote><p>«Porque una buena peluquería canina no es solo que salgan guapos… también es cuidar de su bienestar durante todo el proceso.»</p><cite>— Shadia Cotelo</cite></blockquote></div>
<div class="s-rv-head reveal"><span class="eyebrow">Lo que dicen sus familias</span><a class="s-rating" href="{GOOGLE}" target="_blank" rel="noopener"><b>5,0</b><span class="stars">★★★★★</span><small>208 opiniones en Google ↗</small></a></div><div class="rvs">{rv}</div></div></section>'''

    # ------------------------------------------------------------ MARCAS
    brands = '<section class="s-brands"><div class="wrap"><span>Trabajamos con</span><b>PSH Pro Health</b><b>Artero</b><b>KONG</b><b>Vinted Go</b></div></section>'

    # ------------------------------------------------------------ PREGUNTAS
    questions = faq([('¿Cuánto cuesta cada servicio?', 'El presupuesto depende del tamaño, el estado del manto y el trabajo necesario. Escríbenos por WhatsApp con una foto reciente de tu perro y el servicio que buscas, y te orientamos.'), ('¿Necesito cita previa?', f'Sí, siempre. Reservamos un hueco solo para tu perro y el tiempo que necesite. Lunes a viernes de 9:30 a 13:30 y de 16:00 a 19:00; los sábados, con cita previa. Pide la tuya en el {PHONE}.'), ('¿Y si no sé qué servicio elegir?', 'No pasa nada. Cuéntanos cómo es su pelo y qué quieres mejorar; revisamos contigo las opciones antes de reservar.'), ('¿Atendéis perros grandes?', 'Sí, y nos encantan. Tenemos una bañera de acero inoxidable adaptada para razas gigantes y reservamos tiempo de sobra: Bruce, nuestro San Bernardo, se lleva una tarde entera de mimos.'), ('¿Qué pasa si le asusta el secador?', 'Usamos orejeras protectoras para amortiguar el ruido y hacemos pausas. Avísanos al reservar y adaptamos el ritmo.')])
    faqs = f'''<section class="s-faq"><div class="wrap two-col"><div>{heading('Antes de reservar', 'Sin dudas.<br>Sin <em>sorpresas.</em>', 'Cada perro necesita un tiempo y un cuidado distintos, por eso hablamos antes de empezar.')}</div><div class="reveal">{questions}</div></div></section>'''

    body = hero + ribbon + index + showcase() + process + quiz_block() + voices + brands + faqs + cta()
    page('servicios.html', 'Servicios de peluquería canina', 'Nueve cuidados para tu perro en A Laracha: corte a tijera, stripping, deslanado, baño de ozono, dermocosmética, baño, uñas, alimentación y asesoramiento.', body, 'servicios', 'ozono-shadia-wacho', cls='pro')
