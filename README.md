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
