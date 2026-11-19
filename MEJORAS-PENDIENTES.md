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
