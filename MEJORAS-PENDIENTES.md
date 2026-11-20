# Revisión y mejoras de Pelucans

## Fase anterior: cabeceras y contenido
- [x] Cabeceras a todo el ancho en los 20 HTML actuales y sus versiones GL.
- [x] Introducción legible y contenido específico ampliado en los nueve servicios.
- [x] Revisar anclas, recursos y adaptación a ordenador y móvil.

## Nueva lista solicitada (capturas incluidas)
- [x] Corregir encuadres de cabeceras para no cortar cabezas: fotografía completa en una composición panorámica.
- [x] Menú de servicios más atractivo, con iconos propios coherentes con el logo.
- [x] Pasos de la sesión interactivos y con una presentación más cuidada.
- [x] Reels dentro de todos los servicios, con reproducción directa en un marco de móvil, sin interfaz de Instagram cuando haya MP4.
- [x] Descargar los cuatro reels públicos si están disponibles.
- [x] Fundido entre páginas con la huella de Pelucans.
- [x] Titular con rotación amor / paciencia / mimos y subrayado que se dibuja.
- [x] Servicios con fotografía sticky y contenido que cambia al avanzar.
- [x] Marcas de agua propias y discretas, sin tapar fotos ni texto.
- [x] Muro de Instagram preparado para Behold, con reserva local y actualización automática.
- [x] Probar interacciones y revisar cabeceras en ordenador y móvil.
- [x] Documentar configuración, recursos y limitaciones.

## Dependencia externa confirmada por el usuario
El usuario todavía no tiene feed de Behold. La sincronización real queda pendiente de conectar su cuenta y facilitar la URL pública. No se presenta el contenido fijo como un feed en directo.

Los vídeos de clientes son escenas del salón. Los mismos cuatro reels pueden reutilizarse en varias fichas; no se presentarán como demostraciones de una técnica que el vídeo no muestra.

## Publicación
- [x] Publicar la versión completa en el repositorio público sefiro888/pelucans.
- [x] Comprobar GitHub Pages, imágenes y MP4 en el enlace público.

La parte de implementación del muro está terminada; su activación real depende de la URL de Behold que el usuario aún no tiene.

## Resultado comprobado en público
- Repositorio público: https://github.com/sefiro888/pelucans
- Web: https://sefiro888.github.io/pelucans/
- 38 páginas públicas ES/GL actualizadas (más 404 en cada idioma).
- 103 recursos públicos con respuesta HTTP 200.
- Foto principal cargada y vídeo MP4 reproducido hasta sus 27 segundos desde GitHub Pages.
- La sincronización de Behold es la única activación externa pendiente; el usuario aún no tiene feed.

## Corrección posterior de dirección visual
- [x] Cabeceras fotográficas de borde a borde con texto superpuesto, sin foto lateral.
- [x] Usar exclusivamente fotos reales de Pelucans en las cabeceras.
- [x] Retirar el panel de pestañas y la huella de los pasos; sustituirlo por fotografía real y momentos desplegables.
- [x] Verificar las 20 páginas en ordenador y móvil.

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

## Selección 21, 15, 6, 24, 1 · 19/11/2026
- [x] 21: calendario estacional interactivo en Consejos y acceso desde Inicio.
- [x] 15: guía de sensibilidad al secador, enlazada desde el baño.
- [x] 6: sección editorial de fotografías reales de manos y herramientas en Inicio y Servicios.
- [x] 24: artículo con seis mitos desplegables y fuentes para ampliar.
- [x] Contenidos ES/GL y revisión de 60 combinaciones de las seis páginas nuevas o ampliadas, en 320/390/768/1100/1440 px. Sin desbordamientos ni solapamientos de cabecera. Calendario probado en las cuatro estaciones, flechas, Home y End; mitos abiertos en móvil.
- [x] 1, preparación: soporte de fotos de cabecera específicas para ordenador y móvil. Sin modificar las fotos reales mediante IA.
- [ ] 1, fotografía nueva: pendiente una sesión real de tomas horizontales hechas expresamente. Pautas de encuadre y nombres de archivo en README.md. No se afirma que se hayan tomado fotos nuevas.

## Restauración de fotos de perros · 20/11/2026
- [x] Retocar exclusivamente cinco fotos de perros solos, con siete restauraciones (cinco panorámicas y dos verticales).
- [x] Mantener intactas todas las fotos con personas y las fotos originales de resultados.
- [x] Exportaciones WebP hasta 3840 × 2160 px, identificadas como reescaladas, no 4K nativo.
- [x] Selección automática por pantalla y rutas ES/GL de los srcset.
- [x] Ajustar las variantes móviles para evitar recortar las orejas.
- [x] Comprobadas 96 vistas con anchura efectiva verificada: 320/390/800/801/1440/3840 px en ES/GL. Todas las vistas 4K seleccionan la variante de 3840 px y las móviles, la vertical.

## Rediseño pedido en las capturas · 20/11/2026
- [x] Reemplazar los pasos de una línea por 36 capítulos específicos y detallados, en los nueve servicios ES/GL.
- [x] Presentación propia con contraste negro/blanco, fotografías y navegación entre momentos.
- [x] Foto y contador que siguen la lectura en ordenador; foto en cada capítulo en móvil.
- [x] Renovar menú de ordenador, desplegable de servicios y menú móvil.
- [x] Sustituir la huella de transición por el logo real con anillos y apertura de telón.
- [x] Verificar 148 vistas y controles; mantener las fotos con personas sin retocar.

## Miniatura y descripción al compartir · 20/11/2026
- [x] Tarjeta de marca 1200 × 630 px con logo, perro y lema, en español y gallego.
- [x] Título y descripción específicos para compartir la portada.
- [x] Metadatos sociales completos en las 44 páginas, con URLs públicas absolutas.
- [x] Formato JPEG ligero y dimensiones declaradas; validación de recursos incluidos en Git.

## Recuperar selector de colores · 20/11/2026
- [x] Botón Colores integrado en el nuevo menú de las 44 páginas ES/GL.
- [x] Cinco paletas y compatibilidad con modo claro/oscuro.
- [x] Selección recordada entre páginas en el mismo navegador.
- [x] Selección móvil con vista directa del resultado y controles de teclado.
- [x] Pruebas de diez combinaciones de paleta/modo y ocho anchos, sin desbordamiento.
