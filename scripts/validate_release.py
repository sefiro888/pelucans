"""Valida recursos de ambas lenguas y que los archivos publicados estén en Git."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import subprocess

ROOT=Path(__file__).resolve().parent.parent
tracked=set(subprocess.check_output(['git','ls-files','--cached'],cwd=ROOT,text=True).splitlines())
issues=[]; pages=list(ROOT.glob('*.html'))+list((ROOT/'gl').glob('*.html'))
for page in pages:
    soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    if len(soup.select('h1'))!=1:issues.append(f'{page.name}: H1 incorrecto')
    if len(soup.select('main>header.page-hero'))!=1:issues.append(f'{page.name}: falta cabecera panorámica')
    if page.parent.name=='gl' and soup.html.get('lang')!='gl':issues.append(f'{page}: idioma incorrecto')
    image=soup.select_one('meta[property="og:image"]')
    if not image or not image.get('content','').startswith('https://'):issues.append(f'{page}: imagen social sin URL HTTPS absoluta')
    else:
        expected='pelucans-compartir-gl-v1.jpg' if page.parent.name=='gl' else 'pelucans-compartir-v1.jpg'
        if not image['content'].endswith('/assets/social/'+expected):issues.append(f'{page}: imagen social del idioma incorrecta')
        target=ROOT/'assets/social'/expected
        if not target.exists() or target.relative_to(ROOT).as_posix() not in tracked:issues.append(f'{page}: tarjeta social no publicada en Git')
    for name in ('og:title','og:description','og:image:alt','og:image:width','og:image:height'):
        meta=soup.select_one(f'meta[property="{name}"]')
        if not meta or not meta.get('content'):issues.append(f'{page}: falta {name}')
    for key,value in [('og:image:width','1200'),('og:image:height','630'),('og:image:type','image/jpeg')]:
        meta=soup.select_one(f'meta[property="{key}"]')
        if not meta or meta.get('content')!=value:issues.append(f'{page}: {key} incorrecto')
    for node in soup.select('[src],[href],[poster],[srcset]'):
        for attr in ('src','href','poster','srcset'):
            value=node.get(attr)
            if not value:continue
            for raw in ([part.strip().split()[0] for part in value.split(',')] if attr=='srcset' else [value]):
                url=urlsplit(raw)
                if url.scheme or url.netloc:continue
                if not url.path:
                    if url.fragment and not soup.find(id=unquote(url.fragment)):issues.append(f'{page.name}: ancla {raw}')
                    continue
                target=(page.parent/unquote(url.path)).resolve()
                if not target.exists():issues.append(f'{page}: recurso ausente {raw}');continue
                rel=target.relative_to(ROOT).as_posix()
                if rel not in tracked:issues.append(f'{page.name}: recurso no incluido en Git {rel}')
    if page.name.startswith('servicio-'):
        chapters=soup.select('.journey-chapter')
        if len(chapters)!=4:issues.append(f'{page.name}: faltan capítulos de cuidado')
        for chapter in chapters:
            if len(chapter.get_text(' ',strip=True).split())<35:issues.append(f'{page.name}: capítulo sin desarrollo suficiente')
        if not soup.select_one('video.native-film source'):issues.append(f'{page.name}: falta MP4')
        if not soup.select_one('#guia'):issues.append(f'{page.name}: falta guía específica')
if issues:
    raise SystemExit('\n'.join(sorted(set(issues))))
print(f'OK: {len(pages)} páginas, cabeceras, idiomas, anclas y recursos incluidos en Git.')
