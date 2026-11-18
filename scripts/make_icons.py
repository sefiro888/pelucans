"""Genera los iconos de la web y el manifest (PWA) a partir del logo circular."""
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent.parent
src = Image.open(root / 'assets' / 'img' / 'real' / 'perfil.webp').convert('RGBA')
out = root / 'assets' / 'icons'
out.mkdir(parents=True, exist_ok=True)

def square(size, pad=0.0, bg=(247, 241, 232, 255)):
    canvas = Image.new('RGBA', (size, size), bg)
    inner = int(size * (1 - pad * 2))
    im = src.resize((inner, inner), Image.LANCZOS)
    canvas.paste(im, ((size - inner) // 2, (size - inner) // 2), im)
    return canvas

square(32).save(out / 'favicon-32.png')
square(180, 0.06).save(out / 'apple-touch-icon.png')
square(192, 0.04).save(out / 'icon-192.png')
square(512, 0.04).save(out / 'icon-512.png')
square(512, 0.16).save(out / 'icon-512-maskable.png')

manifest = {
    'name': 'Pelucans · Peluquería Canina',
    'short_name': 'Pelucans',
    'description': 'Peluquería canina en A Laracha. Pide cita por WhatsApp.',
    'lang': 'es',
    'start_url': 'index.html',
    'scope': './',
    'display': 'standalone',
    'background_color': '#f7f1e8',
    'theme_color': '#f7f1e8',
    'icons': [
        {'src': 'assets/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'assets/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'assets/icons/icon-512-maskable.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}
(root / 'site.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('iconos y manifest generados')
