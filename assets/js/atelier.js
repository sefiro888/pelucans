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
  const menu=document.querySelector('#menu');
  const mobile=matchMedia('(max-width:1100px)');
  const outside=[...document.querySelectorAll('main,footer,.mbar,.fab')];
  function synchronizeMenu(){
    if(!menu||!menuToggle)return;
    const opened=mobile.matches&&menu.classList.contains('open');
    menuToggle.setAttribute('aria-expanded',String(opened));
    menuToggle.setAttribute('aria-label',opened?t('Cerrar menú','Pechar menú'):t('Abrir menú','Abrir menú'));
    outside.forEach(el=>{el.inert=opened;});
    document.body.style.overflow=opened?'hidden':'';
    menuOffset();
  }
  function closeMenu(focus=false){
    menu?.classList.remove('open');
    if(menuToggle)menuToggle.innerHTML='<i class="bi bi-list" aria-hidden="true"></i>';
    synchronizeMenu();
    if(focus)menuToggle?.focus();
  }
  menuToggle?.addEventListener('click',synchronizeMenu);
  menu?.addEventListener('click',event=>{if(mobile.matches&&event.target.closest('a[href]'))closeMenu();});
  mobile.addEventListener('change',()=>{if(!mobile.matches)closeMenu();});
  document.addEventListener('keydown',event=>{
    if(!mobile.matches||!menu?.classList.contains('open'))return;
    if(event.key==='Escape'){event.preventDefault();closeMenu(true);return;}
    if(event.key!=='Tab')return;
    const focusable=[menuToggle,...menu.querySelectorAll('a[href],button')].filter(el=>el.getClientRects().length&&!el.disabled&&getComputedStyle(el).visibility!=='hidden');
    const first=focusable[0],last=focusable.at(-1);
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
  });
  const booking=document.querySelector('#booking-form');
  booking?.querySelectorAll('input[required]').forEach(input=>{
    input.addEventListener('input',()=>input.setCustomValidity(input.value&&!input.value.trim()?t('Escribe un nombre válido.','Escribe un nome válido.') : ''));
  });
  document.querySelectorAll('.phone-film video').forEach(video => {
    video.controls = true;
    video.addEventListener('play', () => {
      document.querySelectorAll('video').forEach(other => { if(other!==video)other.pause(); });
      video.closest('.phone-film').classList.add('is-playing');
    });
    const stop=()=>video.closest('.phone-film').classList.remove('is-playing');
    video.addEventListener('pause',stop);
    video.addEventListener('ended',stop);
    if('IntersectionObserver' in window){
      const observer=new IntersectionObserver(entries=>{
        if(!entries[0].isIntersecting&&!video.paused)video.pause();
      },{threshold:.05});
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
/* Calendario accesible: todo el contenido sigue disponible sin JavaScript. */
(() => {
  document.querySelectorAll('.season-journal').forEach(section=>{
    const tabs=[...section.querySelectorAll('[role=tab]')];
    const panels=[...section.querySelectorAll('.season-panel')];
    const list=section.querySelector('[role=tablist]');
    if(!list||tabs.length!==panels.length)return;
    function activate(index,focus=false){
      tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;panels[i].hidden=i!==index;});
      if(focus)tabs[index].focus();
    }
    tabs.forEach((tab,i)=>{
      panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',tab.id);panels[i].tabIndex=0;
      tab.addEventListener('click',()=>activate(i));
      tab.addEventListener('keydown',event=>{
        let next=i;
        if(event.key==='ArrowRight')next=(i+1)%tabs.length;
        else if(event.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;
        else if(event.key==='Home')next=0;
        else if(event.key==='End')next=tabs.length-1;
        else return;
        event.preventDefault();activate(next,true);
      });
    });
    const month=Number(new Intl.DateTimeFormat('en',{month:'numeric',timeZone:'Europe/Madrid'}).format(new Date()));
    activate(month>=3&&month<=5?0:month>=6&&month<=8?1:month>=9&&month<=11?2:3);
    list.hidden=false;
  });
})();
