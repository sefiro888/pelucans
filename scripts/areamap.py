"""Mapa ilustrado (esquema orientativo) de la zona de Pelucans."""

def build(icon, heading, PHONE):
    svg = """<svg class="amap" viewBox="0 0 900 520" role="img" aria-labelledby="amap-t amap-d"><title id="amap-t">Esquema de la zona de Pelucans</title><desc id="amap-d">Esquema ilustrado, no a escala: la avenida Doutor López Astray con la tienda Pelucans, su puerta, el aparcamiento junto a la acera y un árbol a la izquierda.</desc>
<rect class="m-bg" width="900" height="520" rx="34"/>
<g class="m-blocks"><rect x="40" y="70" width="190" height="190" rx="14"/><rect x="250" y="70" width="90" height="190" rx="14"/><rect class="m-shop" x="360" y="50" width="200" height="210" rx="16"/><rect x="580" y="70" width="120" height="190" rx="14"/><rect x="720" y="70" width="140" height="190" rx="14"/></g>
<g class="m-win"><rect x="378" y="90" width="52" height="54" rx="6"/><rect x="490" y="90" width="52" height="54" rx="6"/><rect x="378" y="160" width="164" height="60" rx="6"/></g>
<rect class="m-sign" x="392" y="62" width="136" height="22" rx="11"/><text class="m-t m-sign-t" x="460" y="78" text-anchor="middle">PELUCANS</text>
<rect class="m-door" x="445" y="214" width="30" height="46" rx="4"/>
<g class="m-tree"><circle cx="318" cy="238" r="26"/><rect x="314" y="250" width="8" height="26"/></g>
<rect class="m-walk" x="0" y="268" width="900" height="34"/>
<rect class="m-road" x="0" y="302" width="900" height="118"/><path class="m-dash" d="M0 361H900"/>
<text class="m-t m-road-t" x="450" y="338" text-anchor="middle">Avda. Doutor López Astray</text>
<g class="m-park"><path d="M90 400H330M100 400V420M180 400V420M260 400V420M330 400V420"/><path d="M590 400H810M600 400V420M680 400V420M760 400V420M810 400V420"/></g>
<g class="m-pk"><rect x="118" y="392" width="40" height="22" rx="11"/><text class="m-t" x="138" y="408" text-anchor="middle">P</text><rect x="618" y="392" width="40" height="22" rx="11"/><text class="m-t" x="638" y="408" text-anchor="middle">P</text></g>
<g class="m-car"><rect x="0" y="318" width="64" height="24" rx="10"/><rect x="14" y="310" width="34" height="14" rx="6"/><circle cx="14" cy="344" r="6"/><circle cx="50" cy="344" r="6"/></g>
<path class="m-route" d="M138 392 C138 330 300 300 460 262"/>
<g class="m-pin"><path d="M460 50L444 26A19 19 0 1 1 476 26Z"/><circle cx="460" cy="21" r="7" class="m-pin-dot"/></g>
<g class="m-label"><rect x="560" y="440" width="300" height="52" rx="14"/><text class="m-t m-small" x="710" y="462" text-anchor="middle">Esquema orientativo,</text><text class="m-t m-small" x="710" y="480" text-anchor="middle">no a escala</text></g>
<g class="m-label"><rect x="40" y="440" width="230" height="52" rx="14"/><text class="m-t m-small" x="155" y="462" text-anchor="middle">Aparcamiento</text><text class="m-t m-small" x="155" y="480" text-anchor="middle">cerca de la puerta</text></g>
<g class="m-door-l"><text class="m-t m-small" x="460" y="296" text-anchor="middle">TU PUERTA</text></g>
</svg>"""
    tips = f"""<ul class="ticks reveal d2"><li>{icon('geo-alt')}<span><b>Busca el cristal con la huella</b> y el cartel «Pelucans», en la avenida Doutor López Astray, 40 bajo.</span></li><li>{icon('p-circle')}<span><b>Aparca cerca de la puerta.</b> Hay sitio junto a la acera.</span></li><li>{icon('telephone')}<span><b>¿No nos encuentras?</b> Llámanos al {PHONE} y te guiamos.</span></li></ul>"""
    return f'''<section class="section tint" id="como-llegar"><div class="wrap two-col"><div>{heading('Cómo llegar', 'Sin perderte.<br>Sin <em>vueltas.</em>', 'Un esquema sencillo de la zona para que sepas dónde buscar antes de salir de casa.')}{tips}<div class="reveal d3" style="display:flex;flex-wrap:wrap;gap:.8rem"><a class="btn" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=Pelucans+Peluquer%C3%ADa+Canina+Avenida+Doutor+L%C3%B3pez+Astray+40+A+Laracha">{icon('signpost-2')} Abrir ruta en Google Maps</a><a class="btn light" href="tel:+34604207678">{icon('telephone')} {PHONE}</a></div></div><div class="amap-wrap reveal d1">{svg}</div></div></section>'''
