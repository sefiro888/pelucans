"""Exporta las restauraciones de perros a WebP; jamás modifica fotos con personas.
Los PNG restaurados se conservan localmente en raw_ig/header-restorations/.
La exportación 3840 es reescalada: el restaurador entrega 1672 px de ancho.
"""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parent.parent
LOCAL=ROOT/'raw_ig/header-restorations'
OUT=ROOT/'assets/img/headers'
OUT.mkdir(parents=True,exist_ok=True)
manifest={}
for code in ['80','16','20','41','46']:
    master=LOCAL/f'cliente-{code}.png'
    if not master.exists():raise SystemExit(f'Falta restauración local: {master}')
    with Image.open(master) as im:
        im=im.convert('RGB');native=im.size;variants=[]
        for width in [1280,1920,2560,3840]:
            height=width*9//16
            target=OUT/f'cliente-{code}-restored-{width}.webp'
            im.resize((width,height),Image.Resampling.LANCZOS).save(target,'WEBP',quality=88,method=6)
            variants.append({'src':target.relative_to(ROOT).as_posix(),'width':width,'height':height})
    mobile_master=LOCAL/f'cliente-{code}-mobile.png'
    restored_mobile=mobile_master.exists()
    with Image.open(mobile_master if restored_mobile else ROOT/f'raw_ig/hl-clientes-{code}.jpg') as original:
        target=OUT/f'cliente-{code}-mobile-{"restored" if restored_mobile else "original"}.webp'
        original.convert('RGB').save(target,'WEBP',quality=94,method=6)
        mobile={'src':target.relative_to(ROOT).as_posix(),'width':original.width,'height':original.height,'restored':restored_mobile}
    manifest[f'cliente-{code}']={'restoration':'AI restoration and extended background, dogs only','nativeRestorationSize':native,'originalSource':f'raw_ig/hl-clientes-{code}.jpg','variants':variants,'mobile':mobile,'uhdExport':'resampled, not native 4K'}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Exportadas cinco restauraciones, cuatro tamaños por perro y variantes móviles.')
