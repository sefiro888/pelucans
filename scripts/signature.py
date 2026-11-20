"""Navegación y sello de transición a partir del logotipo real, sin redibujar su identidad."""
from bs4 import BeautifulSoup
from pathlib import Path
import base64

def write_seal(root):
    data=base64.b64encode((root/'assets/img/real/perfil.webp').read_bytes()).decode()
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 240 240"><defs><clipPath id="logo-circle"><circle cx="120" cy="120" r="88"/></clipPath></defs><circle cx="120" cy="120" r="118" fill="#101010"/><circle cx="120" cy="120" r="111" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width=".7"/><circle cx="120" cy="120" r="103" fill="none" stroke="#ffffff" stroke-opacity=".55" stroke-width=".7"/><image clip-path="url(#logo-circle)" x="32" y="32" width="176" height="176" xlink:href="data:image/webp;base64,{data}"/></svg>'''
    (root/'assets/brand/sello-pelucans.svg').write_text(svg,encoding='utf-8')

SUN='<svg class="sun" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4.2 4.2l2.1 2.1m11.4 11.4 2.1 2.1M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>'
MOON='<svg class="moon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M20 14.5A9 9 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"/></svg>'
MENU='<span>Menú</span><svg viewBox="0 0 28 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M1 5h26M8 15h19"/></svg>'

def signature_nav(markup):
    soup=BeautifulSoup(markup,'html.parser')
    nav=soup.select_one('header.nav')
    if not nav:return markup
    nav['class']=nav.get('class',[])+['signature-nav']
    for node in nav.select('.open-pill'):node.decompose()
    for node in nav.select('.nav-links>a:not(.btn),.nav-drop>a'):node['class']=node.get('class',[])+['nav-link']
    pal=nav.select_one('.pal')
    if pal:
        control=pal.select_one('.pal-toggle');popup=pal.select_one('.pal-pop')
        control['aria-label']='Cambiar colores de la web';control['title']='Probar colores';control['aria-controls']='palette-menu';control['aria-haspopup']='menu'
        control.clear();control.append(BeautifulSoup('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.35"><path d="M12 3a9 9 0 1 0 0 18h1c2 0 3-2 2-3-1-2 0-3 2-3h1a4 4 0 0 0 4-4c0-5-5-8-10-8Z"/><circle cx="7" cy="11" r="1" fill="currentColor"/><circle cx="10" cy="7" r="1" fill="currentColor"/><circle cx="15" cy="7" r="1" fill="currentColor"/></svg><span>Colores</span>','html.parser'))
        popup['id']='palette-menu'
        title=BeautifulSoup('<span class="pal-heading" role="presentation">Colores para tu web<small>Prueba, compara y elige.</small></span>','html.parser')
        popup.insert(0,title)
        options=list(popup.select('[data-pal]'))
        for option in options:option['role']='menuitemradio';option['aria-checked']='false'
        logo=popup.select_one('[data-pal="logo"]')
        if logo:logo.extract();popup.insert(1,logo)
    theme=nav.select_one('.theme-toggle')
    if theme:theme.clear();theme.append(BeautifulSoup(SUN+MOON,'html.parser'))
    toggle=nav.select_one('.menu-toggle')
    if toggle:toggle.clear();toggle.append(BeautifulSoup(MENU,'html.parser'))
    mega=nav.select_one('.mega')
    if mega:
        feature=BeautifulSoup('<a class="mega-story" href="nosotros.html"><img src="assets/img/real/cliente-80.webp" alt="" width="405" height="720" loading="lazy"><span><small>La forma Pelucans</small><strong>Cada manto.<br>Su propio cuidado.</strong><b>Conoce el salón ↗</b></span></a>','html.parser')
        mega.append(feature)
    return str(soup)

TRANSITION='''<div class="pt" aria-hidden="true"><div class="pt-curtain pt-left"></div><div class="pt-curtain pt-right"></div><div class="pt-center"><div class="pt-seal"><svg viewBox="0 0 240 240" aria-hidden="true"><circle cx="120" cy="120" r="116"/></svg><img src="assets/brand/sello-pelucans.svg" alt="" width="240" height="240"></div><span class="pt-wordmark">Pelucans</span><span class="pt-line"></span><span class="pt-destination">Un momento para cuidarlo</span></div></div>'''
