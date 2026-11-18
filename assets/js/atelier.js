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
  // Las tarjetas originales siguen siendo legibles cuando no hay JavaScript.
  document.querySelectorAll('.steps, .s-steps').forEach((group, groupIndex) => {
    const children = [...group.children];
    const data = children.map(el => ({title:el.querySelector('h3')?.textContent,text:el.querySelector('p')?.textContent})).filter(x => x.title && x.text);
    if (data.length < 2) return;
    group.className = 'session-experience';
    group.replaceChildren();
    const tabs = document.createElement('div'); tabs.className = 'session-tabs'; tabs.setAttribute('role','tablist'); tabs.setAttribute('aria-label',t('Pasos de la sesión','Pasos da sesión'));
    const panel = document.createElement('div'); panel.className='session-panel'; panel.setAttribute('role','tabpanel'); panel.id='session-panel-'+groupIndex;
    const visual=document.createElement('div');visual.className='session-visual';visual.setAttribute('aria-hidden','true');
    const mark=document.querySelector('.brand-divider svg, .pt svg'); if(mark) visual.append(mark.cloneNode(true));
    const orbit=document.createElement('span');orbit.className='step-orbit';visual.append(orbit);
    const copy=document.createElement('div');copy.className='session-copy';
    const kicker=document.createElement('span');kicker.className='eyebrow';kicker.textContent=t('Su momento, paso a paso','O seu momento, paso a paso');
    const title=document.createElement('h3'),text=document.createElement('p'),controls=document.createElement('div');controls.className='session-controls';
    const prev=document.createElement('button'),next=document.createElement('button'),count=document.createElement('span');prev.type=next.type='button';prev.textContent=t('Anterior','Anterior');next.textContent=t('Siguiente','Seguinte');
    controls.append(prev,count,next);copy.append(kicker,title,text,controls);panel.append(visual,copy);
    const progress=document.createElement('div');progress.className='session-progress';progress.setAttribute('aria-hidden','true');const fill=document.createElement('i');progress.append(fill);
    let active=0;
    const buttons=data.map((item,index)=>{
      const button=document.createElement('button');button.type='button';button.setAttribute('role','tab');button.id=`session-tab-${groupIndex}-${index}`;button.setAttribute('aria-controls',panel.id);
      const num=document.createElement('span');num.textContent=String(index+1).padStart(2,'0');const heading=document.createElement('strong');heading.textContent=item.title;button.append(num,heading);
      button.addEventListener('click',()=>select(index));
      button.addEventListener('keydown',event=>{let target=index;if(event.key==='ArrowRight')target=(index+1)%data.length;else if(event.key==='ArrowLeft')target=(index-1+data.length)%data.length;else if(event.key==='Home')target=0;else if(event.key==='End')target=data.length-1;else return;event.preventDefault();select(target);buttons[target].focus();});tabs.append(button);return button;
    });
    function select(index){active=(index+data.length)%data.length;buttons.forEach((button,i)=>{button.setAttribute('aria-selected',String(i===active));button.tabIndex=i===active?0:-1;});title.textContent=data[active].title;text.textContent=data[active].text;count.textContent=`${active+1} / ${data.length}`;panel.setAttribute('aria-labelledby',buttons[active].id);fill.style.width=`${(active+1)/data.length*100}%`;copy.classList.remove('refresh');if(!reduced)requestAnimationFrame(()=>copy.classList.add('refresh'));orbit.style.transform=`rotate(${active*90}deg)`;}
    prev.addEventListener('click',()=>select(active-1));next.addEventListener('click',()=>select(active+1));group.append(tabs,panel,progress);select(0);
  });
  // Cierre del megamenú al salir de él, sin cerrar mientras se navega con teclado.
  document.addEventListener('click',event=>{if(event.target.closest('.nav-drop'))return;document.querySelectorAll('.nav-drop.open').forEach(menu=>{menu.classList.remove('open');menu.querySelector('button')?.setAttribute('aria-expanded','false');});});
})();
