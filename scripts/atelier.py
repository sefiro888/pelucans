"""Identidad vectorial, navegación y reproductores propios de Pelucans."""
from pathlib import Path
from bs4 import BeautifulSoup

PATHS = {
 'corte-tijera':'<circle cx="8" cy="23" r="4"/><circle cx="23" cy="23" r="4"/><path d="m11 20 15-16M20 20 6 4M16 14l3 3"/>',
 'stripping':'<path d="M10 26c-5-4-6-8-3-9l4 3V8c0-3 4-3 4 0v8-11c0-3 4-3 4 0v11-8c0-3 4-3 4 0v10-5c0-3 4-3 4 0v9c0 4-3 6-6 6H12"/>',
 'deslanado':'<path d="M4 10h15c7 0 7-7 2-7-3 0-3 3-3 3M4 16h23M4 22h15c7 0 7 7 2 7-3 0-3-3-3-3"/>',
 'ozonoterapia':'<path d="M2 12c4-5 6 5 10 0s6 5 10 0 5 0 8 0M2 19c4-5 6 5 10 0s6 5 10 0 5 0 8 0M2 26c4-5 6 5 10 0s6 5 10 0 5 0 8 0"/><circle cx="8" cy="5" r="2"/><circle cx="22" cy="4" r="2"/>',
 'dermocosmetica':'<path d="M17 2c-2 7-10 12-10 19a10 10 0 0 0 20 0c0-7-8-12-10-19Z"/><path d="M12 21c0 4 2 5 5 5M4 4v6M1 7h6"/>',
 'bano-manto':'<path d="M3 15h28l-3 11H6L3 15Zm3 11-2 4m22-4 2 4M5 15V6c0-6 10-6 10 0v2M12 8h6"/><circle cx="22" cy="10" r="2"/><circle cx="28" cy="5" r="3"/>',
 'corte-unas':'<path d="M8 26 5 14c-1-5 5-6 6-2l2 8V7c0-4 6-4 6 0v11l3-7c2-4 7-1 5 3l-4 12c-2 5-13 5-15 0Z"/><path d="m6 7 2 1m16-4-2 2M15 2V0"/>',
 'comida-especializada':'<path d="M3 18h28l-4 11H7L3 18Z"/><path d="M8 13c-3-3 1-7 4-4l2 2 5-5c3-3 7 1 4 4l-7 7"/><path d="M8 22h16"/>',
 'asesoramiento':'<path d="M27 20c7-12-14-21-22-10-5 7 1 14 8 14l-4 6 10-7"/><path d="M13 11c-4-5-9 2 3 8 12-6 7-13 3-8l-3 3-3-3Z"/>',
}
PAW='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="3"><ellipse cx="32" cy="42" rx="10" ry="15" transform="rotate(-25 32 42)"/><ellipse cx="51" cy="26" rx="10" ry="16"/><ellipse cx="73" cy="26" rx="10" ry="16"/><ellipse cx="93" cy="43" rx="10" ry="15" transform="rotate(25 93 43)"/><path d="M33 74c0-14 17-25 29-25s29 12 29 25c0 27-22 13-29 13S33 101 33 74Z"/><path d="m48 59 26 26m0-26L48 85"/><circle cx="45" cy="88" r="5"/><circle cx="78" cy="88" r="5"/></svg>'
def service_icon(slug):
    return '<svg viewBox="0 0 34 34" class="care-icon" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round">'+PATHS[slug]+'</svg>'

def write_assets(root):
    target=root/'assets/brand';target.mkdir(exist_ok=True)
    (target/'huella-pelucans.svg').write_text(PAW.replace('currentColor','#111111'),encoding='utf-8')
    (target/'huella-blanca.svg').write_text(PAW.replace('currentColor','#ffffff'),encoding='utf-8')
    for slug in PATHS:
        (target/(slug+'.svg')).write_text(service_icon(slug).replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ',1),encoding='utf-8')

def decorate(body,file,root):
    soup=BeautifulSoup(body,'html.parser')
    # El titular conserva su lectura accesible mientras rota la palabra visual.
    if file=='index.html':
        title=soup.select_one('.panorama-copy h1')
        if title:
            title.clear()
            title.append(BeautifulSoup('Más que un corte,<br/><em>es <span class="hand-word"><span class="rotor" data-words="amor|paciencia|mimos">amor</span><svg viewBox="0 0 300 25" preserveAspectRatio="none" aria-hidden="true"><path d="M4 17C70 2 220 3 295 10M24 23C130 10 205 12 271 17"/></svg></span> y cuidado.</em>','html.parser'))
    # Cada vídeo se carga desde los MP4 locales: ningún iframe de terceros.
    fallbacks={'DfmILXjEVbX':'DfSzBEnvbrk','DdPLG9LEZw_':'DeKUzOLxCmx'}
    for button in list(soup.select('[data-reel]')):
        code=fallbacks.get(button['data-reel'],button['data-reel'])
        path=root/'assets/video'/f'{code}.mp4'
        if not path.exists(): continue
        poster=button.find('img')
        caption=button.select_one('.cap')
        label=caption.get_text(' ',strip=True) if caption else 'Un momento en Pelucans'
        label=label.replace('Reel · Instagram','').replace('Publicación · Instagram','').strip()
        if code=='DfX9Q7bxnfN': label='El trato de Shadia'
        if button['data-reel'] in fallbacks: label='Un momento de cuidado en el salón'
        figure=soup.new_tag('figure',attrs={'class':'phone-film'})
        shell=soup.new_tag('div',attrs={'class':'phone-shell'})
        video=soup.new_tag('video',attrs={'class':'native-film','playsinline':'','preload':'none','controls':'','poster':poster['src'] if poster else '', 'aria-label':label})
        source=soup.new_tag('source',attrs={'src':f'assets/video/{code}.mp4','type':'video/mp4'})
        video.append(source)
        play=soup.new_tag('button',attrs={'class':'film-play','type':'button','aria-label':'Reproducir: '+label})
        play.append(BeautifulSoup('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 4 13 8L8 20Z" fill="currentColor"/></svg>','html.parser'))
        shell.append(video);shell.append(play);figure.append(shell)
        cap=soup.new_tag('figcaption');cap.string=label;figure.append(cap)
        button.replace_with(figure)
    # Texto coherente con el reproductor nuevo.
    for p in soup.find_all('p'):
        if 'Pulsa para verlo con el reproductor de Instagram.' in p.get_text():
            p.string='Pulsa para reproducir la escena completa aquí mismo, con sonido y controles. Puedes pausar, avanzar o verla a pantalla completa.'
    # Marcas de identidad en su propio espacio, nunca encima del contenido.
    for index,section in enumerate(list(soup.find_all('section',recursive=False))):
        if index not in (2,6): continue
        divider=soup.new_tag('div',attrs={'class':'brand-divider','aria-hidden':'true'})
        divider.append(BeautifulSoup(PAW,'html.parser'))
        section.insert_before(divider)
    return str(soup)
