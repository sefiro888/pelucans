/* Pelucans · interacción */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const GL = document.documentElement.lang === 'gl';
  const T = (es, gl) => (GL ? gl : es);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const IMG = (window.PEL_ROOT || '') + 'assets/img/real/';
  const IG = 'https://www.instagram.com/';

  /* ----- barra de progreso + nav ----- */
  const bar = document.createElement('div'); bar.className = 'progress'; document.body.prepend(bar);
  const nav = $('.nav');
  const onScroll = () => {
    const h = document.documentElement; const max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    nav && nav.classList.toggle('scrolled', h.scrollTop > 8);
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ----- menú móvil ----- */
  const toggle = $('.menu-toggle'), links = $('.nav-links');
  toggle && toggle.addEventListener('click', () => {
    const o = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', o); toggle.innerHTML = o ? '<i class="bi bi-x-lg"></i>' : '<i class="bi bi-list"></i>';
    document.body.style.overflow = o ? 'hidden' : '';
  });
  $$('.nav-drop button').forEach(b => b.addEventListener('click', e => {
    e.preventDefault(); const d = b.closest('.nav-drop'); const o = d.classList.toggle('open'); b.setAttribute('aria-expanded', o);
  }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { $$('.nav-drop.open').forEach(d => d.classList.remove('open')); } });

  /* ----- abierto ahora ----- */
  const pills = $$('[data-open]');
  if (pills.length) {
    const fmt = new Intl.DateTimeFormat('es-ES', { timeZone: 'Europe/Madrid', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false });
    const parts = fmt.formatToParts(new Date()); const g = t => parts.find(p => p.type === t).value;
    const wd = g('weekday').toLowerCase().replace('.', ''); const mins = (+g('hour') % 24) * 60 + +g('minute');
    const day = { lun: 1, mar: 2, mié: 3, mie: 3, jue: 4, vie: 5, sáb: 6, sab: 6, dom: 0 }[wd.slice(0, 3)] ?? new Date().getDay();
    const slots = [[570, 810], [960, 1140]]; let state = 'closed', text = 'Cerrado ahora';
    if (day >= 1 && day <= 5) {
      const cur = slots.find(([a, b]) => mins >= a && mins < b);
      if (cur) { state = 'open'; const c = cur[1]; text = T(`Abierto · cierra a las ${Math.floor(c / 60)}:${String(c % 60).padStart(2, '0')}`, `Aberto · pecha ás ${Math.floor(c / 60)}:${String(c % 60).padStart(2, '0')}`); }
      else if (mins < 570) text = T('Cerrado · abre a las 9:30', 'Pechado · abre ás 9:30');
      else if (mins < 960) text = T('Cerrado · abre a las 16:00', 'Pechado · abre ás 16:00');
      else text = day === 5 ? T('Cerrado · abre el lunes 9:30', 'Pechado · abre o luns ás 9:30') : T('Cerrado · abre mañana 9:30', 'Pechado · abre mañá ás 9:30');
    } else if (day === 6) { state = 'cita'; text = T('Sábados · solo con cita previa', 'Sábados · só con cita previa'); }
    else text = T('Domingo · cerrado', 'Domingo · pechado');
    pills.forEach(p => { p.dataset.state = state; p.textContent = text; });
    $$('[data-day]').forEach(r => r.classList.toggle('today', +r.dataset.day === day || (r.dataset.day === '1-5' && day >= 1 && day <= 5)));
  }

  /* ----- reveal + contadores ----- */
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; e.target.classList.add('in'); io.unobserve(e.target);
    if (e.target.dataset.count) count(e.target);
  }), { threshold: .15, rootMargin: '0px 0px -40px' }) : null;
  $$('.reveal,[data-count]').forEach(el => io ? io.observe(el) : el.classList.add('in'));
  function count(el) {
    const end = parseFloat(el.dataset.count), dec = el.dataset.dec ? +el.dataset.dec : 0, suf = el.dataset.suffix || '';
    if (reduce) { el.textContent = end.toLocaleString('es-ES', { minimumFractionDigits: dec }) + suf; return; }
    const t0 = performance.now(), dur = 1600;
    const tick = t => { const p = Math.min(1, (t - t0) / dur), v = end * (1 - Math.pow(1 - p, 3)); el.textContent = v.toLocaleString('es-ES', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf; if (p < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  }

  /* ----- marquees: duplicar contenido para bucle continuo ----- */
  $$('.marquee-track,.ticker-track').forEach(t => { t.innerHTML += t.innerHTML; t.querySelectorAll('img').forEach(i => i.alt = i.alt || ''); });

  /* ----- comparador antes / después ----- */
  $$('.compare').forEach((c, idx) => {
    const after = $('.after', c), handle = $('.handle', c), input = $('input', c);
    const set = v => { after.style.clipPath = `inset(0 0 0 ${v}%)`; handle.style.left = v + '%'; };
    input.addEventListener('input', () => set(input.value)); set(50);
    if (!reduce && io && idx === 0) { let t = 0; const demo = setInterval(() => { t += .06; set(50 + Math.sin(t) * 28); if (t > 6.3) { clearInterval(demo); set(50); input.value = 50; } }, 30); c.addEventListener('pointerdown', () => clearInterval(demo), { once: true }); }
  });

  /* ----- filtros de servicios ----- */
  const fb = $$('.filters button');
  fb.forEach(b => b.addEventListener('click', () => {
    fb.forEach(x => { x.classList.toggle('active', x === b); x.setAttribute('aria-pressed', x === b); });
    $$('.card[data-cat]').forEach(c => c.classList.toggle('hide', b.dataset.f !== 'Todos' && c.dataset.cat !== b.dataset.f));
  }));

  /* ----- lightbox ----- */
  const lb = $('#lightbox');
  if (lb) {
    let list = [], idx = 0; const im = $('img', lb);
    const show = i => { idx = (i + list.length) % list.length; im.src = list[idx].src; im.alt = list[idx].alt; };
    document.addEventListener('click', e => {
      const f = e.target.closest('[data-lb]'); if (!f) return;
      const group = $$('[data-lb]', f.closest('[data-lb-group]') || document);
      list = group.map(g => ({ src: g.dataset.lb || $('img', g).src, alt: $('img', g)?.alt || '' })); show(group.indexOf(f)); lb.showModal();
    });
    $('.next', lb).onclick = () => show(idx + 1); $('.prev', lb).onclick = () => show(idx - 1);
    lb.addEventListener('click', e => { if (e.target === lb || e.target.classList.contains('x')) lb.close(); });
    lb.addEventListener('keydown', e => { if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1); });
  }

  /* ----- reels (reproductor oficial de Instagram, solo al pulsar) ----- */
  const rd = $('#reel-dialog');
  if (rd) {
    document.addEventListener('click', e => {
      const r = e.target.closest('[data-reel]'); if (!r) return;
      const k = r.dataset.kind || 'reel'; $('iframe', rd).src = `${IG}${k}/${r.dataset.reel}/embed/`; $('.ext', rd).href = `${IG}${k}/${r.dataset.reel}/`; rd.showModal();
    });
    rd.addEventListener('close', () => { $('iframe', rd).src = 'about:blank'; });
    rd.addEventListener('click', e => { if (e.target === rd || e.target.classList.contains('x')) rd.close(); });
  }

  /* ----- destacados estilo stories (fotos reales de los destacados) ----- */
  const HL = {
    clientes: { t: 'Clientes', img: 'hl-clientes', url: '18079974470659851', cta: ['Pedir cita', 'wa'], dur: 4200, s: [12, 16, 19, 20, 21, 26, 27, 30, 31, 33, 36, 38, 39, 41, 56, 78, 80, 84, 88, 92].map(n => `cliente-${String(n).padStart(2, '0')}`) },
    productos: { t: T('Productos', 'Produtos'), img: 'hl-productos', url: '18091242935402580', cta: [T('Ver la tienda', 'Ver a tenda'), 'tienda.html'], dur: 5000, s: ['story-percha', 'story-kong', 'story-kong-2', 'story-psh', 'story-arneses', 'story-raindrops', 'story-raindrops-2', 'story-chubasqueros', 'story-colonias', 'story-artero'] },
    vintedgo: { t: 'Punto Vinted Go', img: 'hl-vintedgo', url: '17966233374221728', cta: [T('Cómo llegar', 'Como chegar'), 'contacto.html#ubicacion'], dur: 7000, s: ['story-vinted'] },
    servicios: { t: T('Servicios', 'Servizos'), img: 'hl-servicios', url: '18126462544744497', cta: [T('Ver servicios', 'Ver servizos'), 'servicios.html'], dur: 5500, s: ['story-tijera', 'story-ozono-intro', 'story-ozono', 'story-atopica', 'story-grooming'] },
    horario: { t: 'Horario', img: 'hl-horario', url: '18121812976933255', cta: ['Pedir cita', 'wa'], dur: 7000, s: ['story-horario'] },
    resenas: { t: T('Reseñas', 'Recensións'), img: 'hl-resenas', url: '18183068647423006', cta: [T('Leer más en Google', 'Ler máis en Google'), 'https://share.google/wduoSy8D64noUdTHf'], dur: 7000, s: ['story-resena-1', 'story-resena-2', 'story-resena-3'] },
  };
  const WA = 'https://wa.me/34604207678?text=' + encodeURIComponent(T('Hola Shadia, me gustaría pedir información y cita para mi peludo.', 'Ola Shadia, gustaríame pedir información e cita para o meu peludo.'));
  const box = document.createElement('div'); box.className = 'stories'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Destacados de Pelucans');
  box.innerHTML = '<button class="story-close" aria-label="Cerrar">×</button><div class="story-box"><div class="story-bars"></div><div class="story-head"><img alt=""><div><span></span><br><small>Destacado de Instagram</small></div></div><img class="story-img" alt=""><button class="story-tap l" aria-label="Anterior"></button><button class="story-tap r" aria-label="Siguiente"></button><div class="story-cta"><a class="go" target="_blank" rel="noopener"></a><a class="ig" target="_blank" rel="noopener" style="background:#fff">Ver en Instagram ↗</a></div></div>';
  let keys = [], ki = 0, si = 0, timer = null;
  const bars = () => $('.story-bars', box);
  function openHL(k) { ki = Math.max(0, Object.keys(HL).indexOf(k)); keys = Object.keys(HL); si = 0; document.body.appendChild(box); box.classList.add('on'); document.body.style.overflow = 'hidden'; render(); }
  function render() {
    const h = HL[keys[ki]]; clearTimeout(timer);
    bars().innerHTML = h.s.map((_, i) => `<i class="${i < si ? 'done' : i === si ? 'run' : ''}" style="--dur:${h.dur}ms"><b></b></i>`).join('');
    $('.story-img', box).src = `${IMG}${h.s[si]}.webp`; $('.story-img', box).alt = `${h.t} de Pelucans, imagen ${si + 1} de ${h.s.length}`;
    $('.story-head img', box).src = `${IMG}${h.img}.webp`; $('.story-head span', box).textContent = 'pelucans · ' + h.t;
    const go = $('.go', box); go.textContent = h.cta[0]; go.href = h.cta[1] === 'wa' ? WA : h.cta[1]; go.target = h.cta[1].startsWith('http') || h.cta[1] === 'wa' ? '_blank' : '_self';
    $('.ig', box).href = `${IG}stories/highlights/${h.url}/`;
    timer = setTimeout(next, h.dur);
  }
  function next() { const h = HL[keys[ki]]; if (si < h.s.length - 1) { si++; } else if (ki < keys.length - 1) { ki++; si = 0; } else return closeHL(); render(); }
  function prev() { if (si > 0) si--; else if (ki > 0) { ki--; si = 0; } render(); }
  function closeHL() { clearTimeout(timer); box.classList.remove('on'); document.body.style.overflow = ''; }
  $('.story-close', box).onclick = closeHL; $('.story-tap.r', box).onclick = next; $('.story-tap.l', box).onclick = prev;
  box.addEventListener('click', e => { if (e.target === box) closeHL(); });
  document.addEventListener('keydown', e => { if (!box.classList.contains('on')) return; if (e.key === 'Escape') closeHL(); if (e.key === 'ArrowRight') next(); if (e.key === 'ArrowLeft') prev(); });
  document.addEventListener('click', e => { const b = e.target.closest('[data-hl]'); if (b) openHL(b.dataset.hl); });

  /* ----- formulario → WhatsApp ----- */
  const form = $('#booking-form');
  if (form) {
    const q = new URLSearchParams(location.search).get('servicio'); if (q && form.service) form.service.value = q;
    form.addEventListener('submit', e => {
      e.preventDefault(); const d = Object.fromEntries(new FormData(form));
      const lines = [T('Hola Shadia, me gustaría pedir cita.', 'Ola Shadia, gustaríame pedir cita.'), '', `${T('Mi nombre', 'O meu nome')}: ${d.name}`, `${T('Mi perro', 'O meu can')}: ${d.dog}`];
      if (d.breed) lines.push(`${T('Raza o tamaño', 'Raza ou tamaño')}: ${d.breed}`); if (d.service) lines.push(`${T('Servicio', 'Servizo')}: ${d.service}`);
      if (d.date) lines.push(`${T('Día preferido', 'Día preferido')}: ${d.date}`); if (d.time && d.time !== 'Me adapto' && d.time !== 'Adáptome') lines.push(`${T('Franja', 'Franxa')}: ${d.time}`);
      if (d.notes) lines.push('', `${T('Algo importante', 'Algo importante')}: ${d.notes}`);
      const url = 'https://wa.me/34604207678?text=' + encodeURIComponent(lines.join('\n'));
      $('.form-status', form).textContent = T('Abriendo WhatsApp con tu mensaje preparado… tú decides si lo envías.', 'Abrindo WhatsApp coa túa mensaxe preparada… ti decides se a envías.');
      open(url, '_blank', 'noopener');
    });
  }

  /* ----- mapa bajo demanda ----- */
  const lm = $('#load-map');
  lm && lm.addEventListener('click', () => {
    const p = $('#map-panel'); p.classList.add('loaded');
    p.innerHTML = '<iframe title="Mapa de Pelucans en A Laracha" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Pelucans+Peluquer%C3%ADa+Canina+Avenida+Doutor+L%C3%B3pez+Astray+40+A+Laracha&output=embed"></iframe>';
  });

  /* ----- privacidad ----- */
  const pd = $('#privacy'); $$('.privacy-open').forEach(b => b.addEventListener('click', () => pd.showModal()));
  pd && pd.addEventListener('click', e => { if (e.target === pd || e.target.classList.contains('x')) pd.close(); });
})();
