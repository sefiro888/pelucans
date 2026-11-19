/* Interacciones propias: controles reales, teclado y movimiento reducido. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gl = document.documentElement.lang === 'gl';
  const t = (es, gal) => gl ? gal : es;
  const menuToggle = document.querySelector('.menu-toggle');
  function menuOffset() {
    const nav = document.querySelector('.nav');
    if (nav) document.documentElement.style.setProperty('--mobile-menu-top', Math.max(0,nav.getBoundingClientRect().bottom)+'px');
  }
  menuToggle?.addEventListener('click', menuOffset);
  addEventListener('resize', menuOffset);
  document.querySelectorAll('.phone-film').forEach(figure => {
    const video = figure.querySelector('video'), button = figure.querySelector('.film-play');
    if (!video || !button) return;
    video.controls = false;
    button.addEventListener('click', () => {
      video.controls = true;
      video.play().then(() => { button.hidden = true; }).catch(() => { video.controls = true; button.hidden = true; });
    });
    video.addEventListener('play', () => {
      document.querySelectorAll('video').forEach(other => { if (other !== video) other.pause(); });
      button.hidden = true; figure.classList.add('is-playing');
    });
    video.addEventListener('pause', () => figure.classList.remove('is-playing'));
    video.addEventListener('ended', () => { button.hidden = false; figure.classList.remove('is-playing'); });
    video.addEventListener('error', () => { button.hidden = true; video.controls = true; });
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        if (!entries[0].isIntersecting && !video.paused) video.pause();
      }, {threshold:0.05});
      observer.observe(video);
    }
  });
  const word = document.querySelector('.rotor');
  if (word) {
    const heading = word.closest('h1');
    heading.setAttribute('aria-label', gl ? 'Máis ca un corte, é amor e coidado.' : 'Más que un corte, es amor y cuidado.');
    const line = word.closest('.hand-word');
    const words = gl ? ['amor', 'paciencia', 'mimos'] : word.dataset.words.split('|');
    let current = 0;
    const draw = () => { line.classList.remove('draw'); requestAnimationFrame(() => requestAnimationFrame(() => line.classList.add('draw'))); };
    draw();
    if (!reduced) setInterval(() => {
      if (document.hidden) return;
      word.classList.add('out');
      setTimeout(() => { current = (current + 1) % words.length; word.textContent = words[current]; word.classList.remove('out'); draw(); }, 280);
    }, 4200);
  }
  // Un momento abierto en cada proceso, con controles nativos de teclado.
  document.querySelectorAll('.session-moments').forEach(group => {
    group.querySelectorAll('details').forEach(detail => detail.addEventListener('toggle', () => {
      if (detail.open) group.querySelectorAll('details').forEach(other => { if (other !== detail) other.open = false; });
    }));
  });
  // Cierre del megamenú al salir de él, sin cerrar mientras se navega con teclado.
  document.addEventListener('click',event=>{if(event.target.closest('.nav-drop'))return;document.querySelectorAll('.nav-drop.open').forEach(menu=>{menu.classList.remove('open');menu.querySelector('button')?.setAttribute('aria-expanded','false');});});
})();
