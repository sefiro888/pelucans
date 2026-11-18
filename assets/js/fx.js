/* Pelucans · efectos y funciones extra (v3) */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const GL = root.lang === 'gl';
  const T = (es, gl) => (GL ? gl : es);
  const R = (window.PEL_ROOT || '') + 'assets/img/real/';

  /* ----- 7 · modo oscuro ----- */
  const setTheme = t => { root.dataset.theme = t; try { localStorage.setItem('pel-theme', t); } catch (_) {} const m = $('meta[name=theme-color]'); if (m) m.content = t === 'dark' ? '#1a1512' : '#f7f1e8'; };
  $$('.theme-toggle').forEach(b => b.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark')));

  /* ----- 11 · esqueletos de carga ----- */
  document.addEventListener('load', e => { if (e.target.tagName === 'IMG') e.target.classList.add('ld'); }, true);
  document.addEventListener('error', e => { if (e.target.tagName === 'IMG') e.target.classList.add('ld'); }, true);
  const markLoaded = () => $$('img').forEach(i => { if (i.complete && i.naturalWidth) i.classList.add('ld'); });
  markLoaded(); addEventListener('load', markLoaded);

  /* ----- 6 · transición entre páginas ----- */
  addEventListener('pageshow', () => root.classList.remove('pt-on'));
  requestAnimationFrame(() => setTimeout(() => root.classList.remove('pt-on'), 60));
  if (!reduce) document.addEventListener('click', e => {
    const a = e.target.closest('a[href]'); if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank' || a.hasAttribute('download')) return;
    const u = new URL(a.href, location.href); if (u.origin !== location.origin || !/\.html?$|\/$/.test(u.pathname)) return;
    if (u.pathname === location.pathname && (u.hash || !u.search)) return;
    e.preventDefault(); root.classList.add('pt-on'); setTimeout(() => { location.href = a.href; }, 380);
  });

  /* ----- 3 · servicios con foto fija ----- */
  const items = $$('.sc-item');
  if (items.length && 'IntersectionObserver' in window) {
    const imgs = $$('.sc-pic img'), tag = $('.sc-tag');
    const set = n => { imgs.forEach((im, k) => im.classList.toggle('on', k === n)); items.forEach((it, k) => it.classList.toggle('on', k === n)); if (tag) tag.textContent = items[n].dataset.tag || ''; };
    set(0);
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) set(items.indexOf(e.target)); }), { rootMargin: '-42% 0px -42% 0px' });
    items.forEach(it => io.observe(it));
  }

  /* ----- carrusel antes / después ----- */
  $$('.ba-car').forEach(car => {
    const track = $('.ba-track', car), slides = $$('.ba-slide', car), dots = $('.ba-dots', car), count = $('.ba-count', car);
    dots.innerHTML = slides.map(() => '<i></i>').join('');
    const ds = $$('i', dots);
    const pad = () => parseFloat(getComputedStyle(track).paddingLeft) || 0;
    const cur = () => { const x = track.scrollLeft + pad(); let best = 0, bd = 1e9; slides.forEach((s, i) => { const d = Math.abs(s.offsetLeft - x); if (d < bd) { bd = d; best = i; } }); return best; };
    const upd = () => { const c = cur(); ds.forEach((d, i) => d.classList.toggle('on', i === c)); if (count) count.textContent = (c + 1) + ' / ' + slides.length; };
    const go = i => { const s = slides[(i + slides.length) % slides.length]; track.scrollTo({ left: s.offsetLeft - pad(), behavior: reduce ? 'auto' : 'smooth' }); };
    $('.prev', car).onclick = () => go(cur() - 1); $('.next', car).onclick = () => go(cur() + 1);
    ds.forEach((d, i) => d.addEventListener('click', () => go(i)));
    track.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true });
    track.addEventListener('keydown', e => { if (e.target !== track) return; if (e.key === 'ArrowRight') { e.preventDefault(); go(cur() + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur() - 1); } });
    upd(); addEventListener('resize', upd);
  });

  /* ----- selector de paletas de color ----- */
  const pal = $('.pal');
  if (pal) {
    const tg = $('.pal-toggle', pal), items = $$('[data-pal]', pal);
    const cur = () => root.dataset.palette || 'original';
    const mark = () => items.forEach(b => b.setAttribute('aria-checked', String(b.dataset.pal === cur())));
    const apply = p => { if (p === 'original') delete root.dataset.palette; else root.dataset.palette = p; try { localStorage.setItem('pel-palette', p); } catch (_) {} mark(); };
    mark();
    tg.addEventListener('click', e => { e.stopPropagation(); const o = pal.classList.toggle('open'); tg.setAttribute('aria-expanded', String(o)); });
    items.forEach(b => b.addEventListener('click', () => { apply(b.dataset.pal); pal.classList.remove('open'); tg.setAttribute('aria-expanded', 'false'); }));
    document.addEventListener('click', e => { if (!pal.contains(e.target)) { pal.classList.remove('open'); tg.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') pal.classList.remove('open'); });
  }

  /* ----- test: ¿qué necesita mi perro? ----- */
  const quiz = $('.quiz');
  if (quiz) {
    const data = JSON.parse($('#svc-data').textContent); const by = Object.fromEntries(data.map(s => [s.slug, s]));
    const Q = [
      { k: 'pelo', t: T('¿Cómo es su pelo?', 'Como é o seu pelo?'), o: [
        ['corto', 'bi-wind', T('Corto y liso', 'Curto e liso'), T('Labrador, boxer, pug…', 'Labrador, boxer, pug…')],
        ['largo', 'bi-water', T('Largo y sedoso', 'Longo e sedoso'), T('Yorkshire, shih tzu, cocker…', 'Yorkshire, shih tzu, cocker…')],
        ['rizado', 'bi-bezier2', T('Rizado o lanoso', 'Rizado ou lanoso'), T('Caniche, bichón, maltés…', 'Caniche, bichón, maltés…')],
        ['duro', 'bi-hand-index', T('Duro o áspero', 'Duro ou áspero'), T('Schnauzer, westie, teckel duro…', 'Schnauzer, westie, teckel duro…')],
        ['doble', 'bi-layers', T('Doble capa, mucho subpelo', 'Dobre capa, moito subpelo'), T('Golden, husky, pastor alemán…', 'Golden, husky, pastor alemán…')]] },
      { k: 'piel', t: T('¿Cómo está su piel?', 'Como está a súa pel?'), o: [
        ['bien', 'bi-emoji-smile', T('Bien, sin problemas', 'Ben, sen problemas'), T('Sin picores ni rojeces', 'Sen picores nin avermelladuras')],
        ['sensible', 'bi-droplet-half', T('Sensible o con picor', 'Sensible ou con comezón'), T('Se rasca, se enrojece o huele fuerte', 'Ráscase, avermellase ou cheira forte')],
        ['nose', 'bi-question-circle', T('No lo sé', 'Non o sei'), T('Prefiero que me orientéis', 'Prefiro que me orientedes')]] },
      { k: 'tam', t: T('¿De qué tamaño es?', 'De que tamaño é?'), o: [
        ['mini', 'bi-1-circle', 'Mini', T('Hasta 5 kg', 'Ata 5 kg')], ['med', 'bi-2-circle', T('Mediano', 'Mediano'), '5–20 kg'],
        ['grande', 'bi-3-circle', 'Grande', '20–40 kg'], ['gigante', 'bi-4-circle', T('Gigante', 'Xigante'), T('Más de 40 kg', 'Máis de 40 kg')]] },
    ];
    const ans = {}; let step = 0;
    const bar = $('.quiz-bar i', quiz), body = $('.quiz-body', quiz);
    const render = () => {
      bar.style.width = (step / Q.length * 100) + '%';
      if (step < Q.length) {
        const q = Q[step];
        body.innerHTML = `<h3>${q.t}</h3><div class="quiz-opts">${q.o.map(([v, ic, l, s]) => `<button data-v="${v}"><i class="bi ${ic}"></i><span>${l}<small>${s}</small></span></button>`).join('')}</div>${step ? `<button class="quiz-back">← ${T('Volver', 'Volver')}</button>` : ''}`;
        $$('.quiz-opts button', body).forEach(b => b.onclick = () => { ans[q.k] = b.dataset.v; step++; render(); });
        const bk = $('.quiz-back', body); if (bk) bk.onclick = () => { step--; render(); };
        return;
      }
      const m = { corto: ['deslanado', 'bano-manto'], largo: ['bano-manto', 'corte-tijera'], rizado: ['corte-tijera', 'bano-manto'], duro: ['stripping', 'corte-tijera'], doble: ['deslanado', 'bano-manto'] };
      let rec = [...m[ans.pelo]]; if (ans.piel === 'sensible') rec.splice(1, 0, 'dermocosmetica'); else if (ans.piel === 'nose') rec.push('asesoramiento'); else rec.push('corte-unas');
      rec = [...new Set(rec)].slice(0, 3);
      const note = ans.tam === 'gigante' || ans.tam === 'grande' ? T('Como es grande, reservaremos tiempo de sobra (a veces una tarde entera) y usaremos la bañera adaptada.', 'Como é grande, reservaremos tempo de sobra (ás veces unha tarde enteira) e usaremos a bañeira adaptada.') : ans.tam === 'mini' ? T('Al ser mini, cuidamos mucho la temperatura del secado y los descansos.', 'Ao ser mini, coidamos moito a temperatura do secado e as pausas.') : '';
      const vet = ans.piel === 'sensible' ? `<p class="note"><i class="bi bi-heart-fill"></i><span>${T('Si el picor es persistente o hay heridas, consulta antes con su veterinario: nosotros cuidamos, no diagnosticamos.', 'Se a comezón é persistente ou hai feridas, consulta antes co seu veterinario: nós coidamos, non diagnosticamos.')}</span></p>` : '';
      const names = rec.map(s => by[s].name).join(', ');
      const msg = T(`Hola Shadia, he hecho el test de la web. Mi perro tiene el pelo ${Q[0].o.find(o => o[0] === ans.pelo)[2].toLowerCase()}, piel ${Q[1].o.find(o => o[0] === ans.piel)[2].toLowerCase()} y es ${Q[2].o.find(o => o[0] === ans.tam)[2].toLowerCase()}. Me gustaría información sobre: ${names}.`, `Ola Shadia, fixen o test da web. O meu can ten o pelo ${Q[0].o.find(o => o[0] === ans.pelo)[2].toLowerCase()}, pel ${Q[1].o.find(o => o[0] === ans.piel)[2].toLowerCase()} e é ${Q[2].o.find(o => o[0] === ans.tam)[2].toLowerCase()}. Gustaríame información sobre: ${names}.`);
      body.innerHTML = `<h3>${T('Te recomendamos empezar por…', 'Recomendámosche comezar por…')}</h3><div class="quiz-res">${rec.map(s => `<a class="rec" href="${by[s].url}"><img src="${by[s].img}" alt=""><span><b>${by[s].name}</b><small>${by[s].short}</small></span></a>`).join('')}</div>${vet}${note ? `<p style="margin-top:1rem">${note}</p>` : ''}<div style="display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.2rem;align-items:center"><a class="btn wa" target="_blank" rel="noopener" href="https://wa.me/34604207678?text=${encodeURIComponent(msg)}"><i class="bi bi-whatsapp"></i> ${T('Pedir cita con este resultado', 'Pedir cita con este resultado')}</a><button class="quiz-back" style="margin:0">${T('Repetir el test', 'Repetir o test')}</button></div>`;
      $('.quiz-back', body).onclick = () => { step = 0; render(); };
    };
    render();
  }

  /* ----- índice de servicios: filtros ----- */
  const idx = $('.idx');
  if (idx) {
    const tabs = $$('.s-tabs button');
    tabs.forEach(b => b.addEventListener('click', () => {
      tabs.forEach(x => { x.classList.toggle('active', x === b); x.setAttribute('aria-pressed', String(x === b)); });
      $$('.idx-row', idx).forEach(r => r.classList.toggle('hide', b.dataset.f !== 'Todos' && r.dataset.cat !== b.dataset.f));
    }));
  }

  /* ----- «Ver más» del álbum ----- */
  $$('[data-more]').forEach(b => {
    b.dataset.label = b.textContent;
    b.addEventListener('click', () => {
      const al = $('.album'); const o = al.classList.toggle('open');
      b.setAttribute('aria-expanded', String(o)); b.textContent = o ? T('Ver menos', 'Ver menos') : b.dataset.label;
    });
  });
})();
