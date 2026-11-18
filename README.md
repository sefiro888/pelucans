# Pelucans · web v2 (rediseño completo)

Web estática de 15 páginas, sin dependencias. Abre `index.html` o sirve la carpeta:

```powershell
python -m http.server 8768 --bind 127.0.0.1
```

## Estructura

- `index`, `servicios`, 9 × `servicio-*.html`, `tienda`, `galeria`, `nosotros`, `contacto`.
- `build.py` genera los 15 HTML. Texto de servicios en `scripts/content.py`.
- `scripts/prepare_images.py` convierte las fotos reales de `raw_ig/` e `img/instagram/` a WebP en `assets/img/real/`.
- `assets/css/site.css` (+ `extra.css`), `assets/js/site.js`.
- `_backup_v1/`: la versión anterior completa, por si hay que consultar algo.
- `check_site.py`: comprueba enlaces, H1 y alt.

Flujo de trabajo: editar `build.py` o `scripts/content.py` → `python build.py` → `python check_site.py`.

## Qué incluye

- Cinta superior y bandas en movimiento (marquee), carriles de fotos de clientes, contadores animados, huellas que siguen al ratón, parallax en la portada, tarjetas con inclinación, botón de WhatsApp flotante y barra fija en móvil.
- **Destacados de Instagram dentro de la web** (visor tipo stories con las imágenes reales de Clientes, Productos, Vinted Go, Servicios, Horario y Reseñas).
- **Reels** con el reproductor oficial de Instagram (solo se cargan al pulsar).
- Comparador **antes / después**, muro de fotos con lightbox, reseñas reales en movimiento.
- Indicador **«Abierto ahora»** calculado con la hora de Madrid.
- Formulario que prepara un mensaje de WhatsApp (no envía nada ni guarda datos). Mapa de Google solo al pulsar.
- Tienda con el catálogo de WhatsApp Business y sección Vinted Go.

## De dónde sale cada cosa (consultado el 18/11/2026)

- **Instagram** `@pelucans_peluqueriacanina` (sesión del usuario): 9 publicaciones, 4 reels (códigos DfX9Q7bxnfN, DfSzBEnvbrk, DeKUzOLxCmx, DczA2PexJXm) y los 6 destacados recorridos historia a historia. «Clientes» tiene más de 100 historias; se usan ~45 fotogramas limpios.
- **WhatsApp Business** (catálogo `wa.me/c/34604207678`): Colonias PSH 13 €, Juguetes KONG 10 €, Arnés Pollo & Paco 25 € y las fotos de los servicios.
- **Google** (ficha): 5,0 · 208 opiniones; foto de la fachada.
- **Páxinas Galegas / Páginas Amarillas**: horario (L–V 9:30–13:30 y 16:00–19:00, **sábado con cita previa**), servicios, reseñas de Duque Caxias y Laura Esmoris.

## Pendiente / a confirmar con Shadia

- Autorización para usar las fotos de clientes y la foto de fachada de Google (publicadas por terceros).
- Precios y stock actuales de la tienda; se muestran solo los del catálogo.
- Confirmar el horario del sábado («con cita previa», según su destacado de Horario y Páxinas Galegas).
- Datos legales (titular, NIF) para el aviso legal antes de publicar. No se han inventado.
- Los vídeos en bruto de los reels no se pueden descargar desde Instagram; si Shadia los pasa en `.mp4` se pueden reproducir en bucle dentro de la web.

## v3 · novedades (18/11/2026)

- **19 páginas en castellano + 19 en gallego** (`gl/`). El gallego se genera traduciendo el HTML con `scripts/gl.py` (diccionario alineado con `scripts/gl/*.txt`). Si cambias un texto en castellano, aparecerá en `scripts/gl_pendientes.txt` tras `python build.py`; añade su traducción en `EXTRA` dentro de `scripts/gl.py`. Conviene que alguien de la zona revise el gallego.
- **Mini blog** `consejos.html` + 3 artículos (`scripts/posts.py`).
- **Test «¿qué necesita mi perro?»** en portada, servicios y consejos.
- **Reels/publicaciones de Instagram en cada servicio** (`MEDIA` en `build.py`; los marcados como «Un vistazo al salón» son genéricos porque no hay un reel específico).
- **Carrusel antes/después**: pares reales en `assets/img/antes-despues/` (ver `LEEME.txt`). Mientras haya menos de 4, salen plantillas; `SHOW_DEMO_PAIRS = False` las oculta.
- **Vídeo en la portada**: si existe `assets/video/portada.mp4`, sustituye a la foto del arco.
- **Instagram en directo**: pon la dirección del feed JSON de Behold en `INSTAGRAM_FEED_URL` (`build.py`). Probado con un feed simulado (`scripts/ejemplo-feed.json`); falta crear la cuenta de Behold con el Instagram de Shadia (debe ser cuenta profesional).
- Efectos: titular que rota, servicios con foto fija, huellas que caminan hasta el botón de cita (≥1100 px), cursor con huella, transición entre páginas, modo oscuro, formas en la galería, texturas, esqueletos de carga y cola de perrito en los botones.

## v4 · carrusel, paletas y mapa

- **Antes/después** ahora ocupa todo el ancho, con contador, puntos clicables, teclado y plantillas más claras.
- **Paletas de color** (botón de paleta en la barra, se recuerda la elección): Original, **Logo** (solo negro, blanco y grises), Mar, Bosque y Lila. Todas funcionan también en modo oscuro. Se definen en `assets/css/palettes.css`; para cambiar la paleta por defecto, añade `data-palette="logo"` a la etiqueta `<html>` en `build.py`.
- **Mapa ilustrado de la zona** en `contacto.html#como-llegar` (`scripts/areamap.py`): esquema orientativo, no a escala, con la avenida, la puerta, el aparcamiento y el árbol de la fachada. No se han inventado calles ni comercios cercanos.

## v5 · servicios premium

- `servicios.html` rehecha con dirección editorial (`scripts/servicios_pro.py` + `assets/css/premium.css`): hero con foto y datos, cinta fina, **índice tipográfico con vista previa de foto al pasar el ratón** y filtros, recorrido con foto fija, cita paso a paso, cita de Shadia con reseñas, marcas, preguntas y cierre oscuro.
- Las 9 fichas `servicio-*.html` usan la misma dirección (clase `pro` en `<body>`): líneas finas, serif grande, beneficios y pasos en columnas sin cajas, tarjetas suaves.
- Funciona con las 5 paletas, modo oscuro, móvil y gallego.

## v6 · web más ordenada y sin efectos de ratón

- Todas las páginas siguen la dirección premium (clase `pro`): líneas finas, serif grande, poco color y secciones con una introducción que explica qué vas a ver.
- **Se quitó todo lo que seguía al ratón**: cursor con huella, huellas que caminan, parallax, inclinación de tarjetas, botones magnéticos y vista previa flotante del índice.
- Portada reducida a lo esencial; galería reorganizada (destacados, reels, antes y después, álbum con «Ver más» e Instagram).

## Repositorio

Este repositorio no incluye los materiales de trabajo (`raw_ig/`, `img/`, `_backup_v1/`, `preview/`, `referencias/`). Las fotos ya optimizadas están en `assets/img/real/`. Para regenerar el HTML basta con `python build.py`; `scripts/prepare_images.py` solo es necesario si se vuelven a descargar las fotos originales.
