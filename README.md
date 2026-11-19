# Pelucans · web pública

Sitio estático de 20 páginas en español y 20 en gallego, incluida la página 404. Se publica desde `main` en GitHub Pages: https://sefiro888.github.io/pelucans/.

## Trabajo local

Para ver la web: `python -m http.server 8774 --bind 127.0.0.1`.
Para regenerar: instalar `requirements.txt`, ejecutar `python build.py` y `python check_site.py`.

`build.py` compone los HTML. Los módulos de `scripts/` guardan contenido, traducciones y secciones. Las imágenes optimizadas utilizadas por la web están en `assets/img/real/`; deben estar incluidas en Git. La regla `/img/` de `.gitignore` excluye solo los originales de trabajo en la raíz, no `assets/img/`. Este era el motivo de que las fotos no aparecieran en la publicación anterior. `.nojekyll` indica que la salida es estática.

## Cabeceras y contenido

Todas las páginas tienen una cabecera a todo el ancho con introducción y contraste para el texto. Las cabeceras usan fotografías reales como fondo de borde a borde con `object-fit: cover`, puntos focales por página y texto superpuesto sobre un degradado. Se ha eliminado la composición de fotografía lateral. Las nueve fichas incluyen explicación, beneficios, destinatarios, proceso, guía antes/durante/después, recomendaciones para reservar, preguntas y cuidados relacionados.

## Interacciones nuevas

- Menú de servicios con nueve iconos SVG propios y categorías.
- Proceso con una fotografía real y cuatro momentos desplegables, accesibles con teclado. Se ha retirado el panel de pestañas y la ilustración vacía de la huella.
- Cuatro reels públicos descargados y reproducidos como MP4 propios, sin interfaz de Instagram, en un marco de móvil. Hay un reproductor en cada ficha. Solo reproduce uno a la vez y se pausa al salir de pantalla. Las escenas generales no se describen como vídeos de una técnica específica.
- Titular con amor / paciencia / mimos y subrayado vectorial dibujado. Respeta movimiento reducido y mantiene una lectura accesible estable.
- Fundido entre páginas con una huella propia inspirada en el logo.
- Recorrido de servicios con foto sticky, cambios de imagen y texto; en móvil se presenta en vertical sin fijar la fotografía.
- Marcas de identidad en separadores propios, sin superponerse a textos ni fotos. SVG reutilizables en `assets/brand/`.
- Blanco, negro y grises del logo por defecto; se conserva el selector de paletas y el modo oscuro.

## Vídeos locales

Fuentes públicas descargadas durante esta revisión:

- https://www.instagram.com/reel/DczA2PexJXm/ — corte a tijera.
- https://www.instagram.com/reel/DfSzBEnvbrk/ — sesión de Bruce.
- https://www.instagram.com/reel/DeKUzOLxCmx/ — Wacho y el ozono.
- https://www.instagram.com/reel/DfX9Q7bxnfN/ — trato con los perros.

Archivos en `assets/video/`, aproximadamente 18 MB en total. Las fotos y vídeos conservan el contenido original. No se han inventado vídeos de consejos ni testimonios.

## Muro automático de Instagram

El usuario ha confirmado que todavía no dispone de una URL de Behold. El muro muestra las publicaciones seleccionadas del salón y no se presenta como sincronización en directo.

Para activarlo:

1. Conectar la cuenta de Instagram en Behold y crear un feed JSON.
2. Copiar la URL pública `https://feeds.behold.so/...` en `instagramFeedUrl` de `assets/config/social.json`.
3. Publicar ese archivo. No hace falta cambiar el diseño ni incluir claves privadas.

El código consulta el feed al abrir la página, cada 10 minutos mientras la pestaña está visible y al volver a ella. Si falla la conexión, conserva las publicaciones disponibles y una copia local reciente. La actualización de Instagram depende de los intervalos y del plan de Behold. Documentación: https://behold.so/docs/json-feeds/.

## Fuentes y confirmaciones

Datos aportados en `info-negocio-pelucans.md`, guía de imágenes, Instagram, Google, Páxinas Galegas y Páginas Amarillas. Valoración 5,0/208: instantánea consultada el 18/11/2026, no sincronización automática. Precios de catálogo: confirmar stock y precio al consultar. Horario de sábado: cita previa según el destacado aportado.

Se mantiene una redacción prudente para piel y ozono: el cuidado cosmético no sustituye la valoración ni las pautas veterinarias. Datos legales completos del titular, precios y permisos de imágenes deben mantenerse actualizados por el negocio.

## Validación de esta revisión

- 40 comprobaciones de diseño en navegador: 20 páginas a 1440 px y a 390 px, sin desbordamientos y con cabeceras a todo el ancho.
- Nueve fichas con reproductor propio y cuatro pasos interactivos cada una.
- Reproducción MP4 comprobada con duración y avance real; menú con nueve SVG y encaje dentro de pantalla; proceso probado con ratón y teclado.
- Foto de servicios comprobada con posición sticky y cambio a Deslanado al desplazarse.
- Recursos y anclas verificados en ES y GL. Traducciones nuevas sin textos pendientes.

El detalle de la solicitud y su estado se conserva en `MEJORAS-PENDIENTES.md`.

## Publicación verificada

Repositorio público: https://github.com/sefiro888/pelucans. GitHub Pages sirve desde `main`, raíz `/`. Se han comprobado 38 páginas públicas actualizadas y 103 recursos (imágenes, vídeos, CSS y JavaScript) con respuesta HTTP 200. El vídeo de corte a tijera se ha reproducido completo desde el enlace público.

## Corrección solicitada tras la revisión visual

Se sustituyó el panel de pasos por una composición editorial con fotos reales. Las 40 páginas ES/GL usan ahora imágenes de fondo a todo el ancho y texto encima. No se añadieron imágenes de IA: las cabeceras emplean exclusivamente fotos del salón y sus clientes, con puntos focales por página. Las imágenes generadas de la carpeta original `img/` no forman parte de esta publicación. Comprobadas 40 combinaciones de página y tamaño (1440/390 px) sin desbordamiento ni solapamientos del contenido de cabecera.

## Revisión móvil del 19/11/2026
- Corregido el desbordamiento del nombre de Instagram a 320 px y el menú de tablet a 1024 px; navegación compacta hasta 1100 px.
- Reels con desplazamiento horizontal y ajuste por tarjeta en móvil; controles nativos accesibles incluso sin JavaScript, sin interfaz de Instagram.
- Campos de 16 px, botones táctiles amplios, margen para la barra fija y zonas seguras del dispositivo.
- Menú con cierre mediante Escape, foco contenido y fondo inactivo mientras está abierto.
- Consulta de WhatsApp con enlace alternativo y validación de nombres vacíos; preparación probada sin enviar mensajes.
- Dimensiones reales en las imágenes para reducir saltos de contenido durante la carga.
- Revisión en navegador: 40 páginas ES/GL a 320 px, más portada, contacto, servicios y galería a 390/768/1024/1440 px. Detectados y corregidos los dos desbordamientos indicados.
- La prueba es de navegador con tamaños de pantalla; no equivale a una prueba física en iPhone y Android.

### Cierre de publicación
La versión publicada se comprobó con 72 combinaciones de página y ancho (320, 360, 390, 430, 768, 1024, 1100, 1280 y 1440 px), sin desbordamientos, imágenes rotas cargadas ni solapamientos de la introducción con el pie de cabecera. Las 40 páginas se recorrieron a 320 px; en los demás anchos se probaron portada, contacto, servicios y galería.
Comprobación pública: 40 páginas y 101 recursos devuelven HTTP 200. MP4 público de corte a tijera cargado (27,118 s), listo y avanzando hasta 7,7 s en la comprobación móvil. Capturas de la revisión en la carpeta local `preview/` (ignorada por Git).

## Selección de mejoras 21, 15, 6, 24 y 1
- Calendario de cuatro estaciones en Consejos: selección de estación según el mes en Madrid, navegación con flechas/Home/End y contenido accesible sin JavaScript. Orientación, no una pauta de citas ni una fecha universal de muda.
- Guía propia para sensibilidad al secador y enlace desde Baño y cuidado del manto.
- Seis mitos desplegables con enlaces a fuentes de bienestar animal.
- Tres fotografías reales de manos, herramienta de cepillado y preparación del secado, en Inicio y Servicios. No se han generado fotografías con IA.
- Nuevos contenidos ES/GL; dos artículos nuevos por idioma.

### Fotografías de cabecera: preparación y toma pendiente
Las fotografías hechas expresamente requieren una nueva sesión real en el salón. La integración de variantes ya está preparada: colocar archivos WebP en `assets/img/headers/`, con el nombre de la página sin `.html` seguido de `-desktop.webp` o `-mobile.webp`, y ejecutar `python build.py`. Ejemplo: `nosotros-desktop.webp` y `nosotros-mobile.webp`. Si no existen, se conserva la foto real actual. El navegador elige la variante adecuada y mantiene la cabecera a todo el ancho.

Para la sesión: tomas horizontales de al menos 2400 × 1400 px, espacio tranquilo a la izquierda para el texto y personas/perros a la derecha, con margen sobre la cabeza. Fotografiar también una variante vertical para móvil y dejar aire alrededor del sujeto. Priorizar Shadia y Bimba, baño con Bruce, corte con manos y tijeras visibles, cepillado, bienvenida y fachada. No se propone sustituir esas tomas por imágenes generadas. Las fotografías actuales proceden del material ya aportado.
