"""Metadatos de vista previa de enlaces; disponibles sin ejecutar JavaScript."""
from html import escape
HOME_TITLE='Pelucans · Amor y cuidado para tu perro'
HOME_DESCRIPTION='Peluquería canina en A Laracha. Conoce a Shadia, descubre nuestros cuidados y pide cita: atención individual, sin jaulas y sin prisas.'
IMAGE_ALT='Diseño de Pelucans con un perro de pajarita verde y el lema «Amor y cuidado».'

def social_tags(file,title,description,base):
    base=base.rstrip('/')+'/'
    image=base+'assets/social/pelucans-compartir-v1.jpg'
    share_title=HOME_TITLE if file=='index.html' else title+' | Pelucans'
    share_description=HOME_DESCRIPTION if file=='index.html' else description
    def meta(kind,name,value):return f'<meta {kind}="{name}" content="{escape(str(value),quote=True)}">'
    og={'title':share_title,'description':share_description,'type':'article' if file.startswith('consejo-') else 'website','url':base+file,'site_name':'Pelucans','locale':'es_ES','locale:alternate':'gl_ES','image':image,'image:secure_url':image,'image:type':'image/jpeg','image:width':'1200','image:height':'630','image:alt':IMAGE_ALT}
    twitter={'card':'summary_large_image','title':share_title,'description':share_description,'image':image,'image:alt':IMAGE_ALT}
    return ''.join(meta('property','og:'+key,value) for key,value in og.items())+''.join(meta('name','twitter:'+key,value) for key,value in twitter.items())
