"""Tarjeta de enlace: composición vectorial con el logo y una imagen existente de la web."""
from pathlib import Path
import base64
import io
from PIL import Image
import cairosvg
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/social';OUT.mkdir(parents=True,exist_ok=True)
def embedded(path,mime):return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()
photo=embedded(ROOT/'assets/img/headers/cliente-80-restored-1920.webp','image/webp')
logo=embedded(ROOT/'assets/img/real/perfil.webp','image/webp')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="630" viewBox="0 0 1200 630">
<defs><linearGradient id="shade"><stop stop-color="#101010" stop-opacity=".97"/><stop offset=".45" stop-color="#101010" stop-opacity=".83"/><stop offset=".70" stop-color="#101010" stop-opacity=".12"/><stop offset="1" stop-color="#101010" stop-opacity="0"/></linearGradient><clipPath id="logo"><circle cx="91" cy="87" r="35"/></clipPath></defs>
<rect width="1200" height="630" fill="#111"/>
<image x="0" y="-22" width="1200" height="675" xlink:href="{photo}"/>
<rect width="1200" height="630" fill="url(#shade)"/>
<image x="56" y="52" width="70" height="70" xlink:href="{logo}" clip-path="url(#logo)"/>
<g fill="#fff"><text x="143" y="94" font-family="Georgia,serif" font-size="49" letter-spacing="-2">Pelucans</text>
<text x="145" y="119" font-family="Arial,sans-serif" font-size="12" letter-spacing="2">PELUQUERÍA CANINA · A LARACHA</text>
<path d="M58 206h42" stroke="#fff" stroke-opacity=".7"/>
<text x="58" y="268" font-family="Georgia,serif" font-size="48" letter-spacing="-1.5">Más que un corte.</text>
<text x="58" y="331" font-family="Georgia,serif" font-style="italic" font-size="49" letter-spacing="-1.3">Amor y cuidado.</text>
<text x="60" y="390" font-family="Arial,sans-serif" font-size="20" fill="#e8e8e8">Uno a uno. Sin jaulas. Sin prisas.</text>
<path d="M58 526h1084" stroke="#fff" stroke-opacity=".27"/>
<text x="60" y="570" font-family="Arial,sans-serif" font-size="12" letter-spacing="2.5">DESCUBRE PELUCANS</text>
<text x="60" y="598" font-family="Arial,sans-serif" font-size="15" fill="#ddd">Tu peluquería canina en A Laracha</text>
<rect x="972" y="550" width="170" height="44" rx="22" fill="#111"/>
<text x="1057" y="578" font-family="Arial,sans-serif" font-size="12" text-anchor="middle" letter-spacing="1.4">PIDE TU CITA</text></g></svg>'''
(OUT/'pelucans-compartir-v1.svg').write_text(svg,encoding='utf-8')
rendered=cairosvg.svg2png(bytestring=svg.encode('utf-8'),output_width=1200,output_height=630)
with Image.open(io.BytesIO(rendered)) as im:im.convert('RGB').save(OUT/'pelucans-compartir-v1.jpg',quality=92,optimize=True,progressive=False)
print('Tarjeta 1200x630:',(OUT/'pelucans-compartir-v1.jpg').stat().st_size,'bytes')
# La misma composición, con copy en gallego para enlaces /gl/.
svg_gl=svg
for es,gl in {'PELUQUERÍA CANINA · A LARACHA':'PEITEADO CANINO · A LARACHA','Más que un corte.':'Máis que un corte.','Amor y cuidado.':'Amor e coidado.','Uno a uno. Sin jaulas. Sin prisas.':'Un a un. Sen gaiolas. Sen présas.','Tu peluquería canina en A Laracha':'O teu salón de peiteado canino na Laracha','PIDE TU CITA':'PIDE A TÚA CITA'}.items():svg_gl=svg_gl.replace(es,gl)
(OUT/'pelucans-compartir-gl-v1.svg').write_text(svg_gl,encoding='utf-8')
rendered_gl=cairosvg.svg2png(bytestring=svg_gl.encode('utf-8'),output_width=1200,output_height=630)
with Image.open(io.BytesIO(rendered_gl)) as im:im.convert('RGB').save(OUT/'pelucans-compartir-gl-v1.jpg',quality=92,optimize=True,progressive=False)
