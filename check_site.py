"""Comprobación rápida: enlaces/recursos locales, un H1 por página, alt en imágenes."""
import re, glob, os
bad = 0
for f in sorted(glob.glob('*.html')):
    t = open(f, encoding='utf-8').read()
    if len(re.findall(r'<h1[ >]', t)) != 1: print(f, 'H1 != 1'); bad += 1
    for m in re.finditer(r'(?:src|href)="([^"#?:]+?)(?:#[^"]*)?"', t):
        u = m.group(1)
        if u.startswith(('http', 'mailto', 'tel')): continue
        if not os.path.exists(u): print(f, 'FALTA', u); bad += 1
    for m in re.finditer(r'<img (?![^>]*alt=)', t): print(f, 'img sin alt'); bad += 1
    for m in re.finditer(r'#([a-z-]+)"', t):
        pass
print('páginas:', len(glob.glob('*.html')), '· problemas:', bad)
