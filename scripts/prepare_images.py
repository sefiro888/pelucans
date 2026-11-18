"""Optimiza las fotos reales (Instagram, destacados, catálogo de WhatsApp y Google) a WebP para la web."""
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'raw_ig'
POSTS = ROOT / 'img' / 'instagram'
OUT = ROOT / 'assets' / 'img' / 'real'
OUT.mkdir(parents=True, exist_ok=True)

def save(src, name, long_side, q=80, crop=None):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    im.thumbnail((long_side, long_side), Image.LANCZOS)
    im.save(OUT / f'{name}.webp', 'WEBP', quality=q, method=6)

# Publicaciones del feed (alta resolución)
for src, name, ls in [
    ('post-9-shadia-cotelo-bimba-1.jpg', 'shadia-bimba-1', 1600),
    ('post-9-shadia-cotelo-bimba-2.jpg', 'shadia-bimba-2', 1600),
    ('post-4-bruce-bano-1.jpg', 'bruce-bano-1', 1500),
    ('post-4-bruce-bano-2.jpg', 'bruce-bano-2', 1500),
    ('post-1-deslanado-pelo-corto.jpg', 'deslanado', 1500),
    ('post-6-orejeras-protectoras-secado.jpg', 'orejeras', 1200),
    ('post-7-ozono-dermocosmetica-2.jpg', 'ozono-secado', 1500),
    ('post-7-ozono-dermocosmetica-3.jpg', 'ozono-shadia-wacho', 1500),
    ('post-7-ozono-dermocosmetica-5.jpg', 'wacho', 1500),
    ('post-7-ozono-dermocosmetica-1.jpg', 'piel-detalle', 1200),
    ('post-7-productos-psh-ozono-4.jpg', 'psh-ozone', 1500),
    ('post-2-mastin-amor-perruno.jpg', 'reel-amor', 640),
    ('post-3-bruce-san-bernardo-sesion.jpg', 'reel-bruce', 640),
    ('post-5-wacho-ozonoterapia.jpg', 'reel-wacho', 640),
    ('post-8-corte-tijera-maltes.jpg', 'reel-tijera', 640),
]:
    save(POSTS / src, name, ls)
save(POSTS / 'logo-pelucans.jpg', 'perfil', 400)
for i, n in enumerate(['productos', 'clientes', 'vintedgo', 'servicios', 'horario', 'resenas'], 1):
    save(POSTS / f'highlight-{i}-{n}.jpg', f'hl-{n}', 300)

# Fachada (ficha de Google)
save(RAW / 'google-fachada.jpg', 'fachada', 1290, 82)

# Clientes: muro de caras felices (destacado «Clientes»)
clientes = [5,12,16,19,20,21,26,27,30,31,32,33,35,36,37,38,39,40,41,42,45,46,48,56,75,78,79,80,81,82,83,84,87,88,91,92,93,95,47,99,10,29,28,76,77]
for n in clientes:
    f = RAW / f'hl-clientes-{n:02d}.jpg'
    if f.exists(): save(f, f'cliente-{n:02d}', 720, 78)

# Antes / Después (destacado Clientes, nº 17: foto apilada) -> dos mitades
im = Image.open(RAW / 'hl-clientes-17.jpg').convert('RGB'); w, h = im.size
save(RAW / 'hl-clientes-17.jpg', 'antes', 720, 82, crop=(0, 0, w, int(h * 0.5 * 0.86)))
save(RAW / 'hl-clientes-17.jpg', 'despues', 720, 82, crop=(0, h // 2, w, h // 2 + int(h * 0.5 * 0.86)))

# Gráficos de los destacados (productos, horario, reseñas, Vinted Go, servicios)
def first(patterns):
    for p in patterns:
        f = RAW / p
        if f.exists(): return f
for name, pats in {
    'story-horario': ['hl-serv-04.jpg'],
    'story-resena-1': ['hl-serv-05.jpg'],
    'story-resena-2': ['hl-serv-06.jpg'],
    'story-resena-3': ['hl-serv-07.jpg'],
    'story-vinted': ['hl-productos-12.jpg'],
    'story-lluvia': ['hl-productos-11.jpg'],
    'story-ozono': ['hl-productos-15.jpg'],
    'story-ozono-intro': ['hl-productos-14.jpg'],
    'story-atopica': ['hl-productos-16.jpg'],
    'story-kong': ['hl-productos-02.jpg'],
    'story-kong-2': ['hl-productos-03.jpg'],
    'story-psh': ['hl-productos-04.jpg'],
    'story-arneses': ['hl-productos-05.jpg'],
    'story-raindrops': ['hl-productos-06.jpg'],
    'story-raindrops-2': ['hl-productos-07.jpg'],
    'story-chubasqueros': ['hl-productos-08.jpg'],
    'story-colonias': ['hl-productos-09.jpg'],
    'story-artero': ['hl-productos-10.jpg'],
    'story-percha': ['hl-productos-01.jpg'],
    'story-tijera': ['hl-productos-13.jpg'],
    'story-antes-despues': ['hl-clientes-17.jpg'],
    'story-grooming': ['hl-clientes-44.jpg'],
}.items():
    f = first(pats)
    if f: save(f, name, 1080, 80)
# Catálogo de WhatsApp
for src, name in [('wa-cat-colonias-psh','cat-colonias'),('wa-cat-juguetes-kong','cat-kong'),('wa-cat-arnes-pollo-paco','cat-arnes'),('wa-cat-servicio-suri','cat-suri'),('wa-cat-servicio-thor-lacky','cat-thor'),('wa-cat-servicio-blue','cat-blue')]:
    save(RAW / f'{src}.jpg', name, 900, 80)
print(len(list(OUT.glob('*.webp'))), 'imágenes en', OUT)
