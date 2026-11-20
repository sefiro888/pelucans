/* Los capítulos se pueden leer sin JavaScript; el desplazamiento solo cambia la escena. */
(() => {
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.care-journey').forEach(journey=>{
    const chapters=[...journey.querySelectorAll('[data-chapter]')];
    const frames=[...journey.querySelectorAll('[data-frame]')];
    const links=[...journey.querySelectorAll('[data-journey-link]')];
    const count=journey.querySelector('[data-journey-count]');
    const activate=n=>{
      chapters.forEach((c,i)=>c.classList.toggle('on',i===n));
      frames.forEach((f,i)=>{f.classList.toggle('on',i===n);f.setAttribute('aria-hidden',String(i!==n));});
      links.forEach((l,i)=>{if(i===n)l.setAttribute('aria-current','step');else l.removeAttribute('aria-current');});
      if(count)count.textContent=String(n+1).padStart(2,'0');
    };
    links.forEach((link,i)=>link.addEventListener('click',()=>activate(i)));
    let pending=false;
    function update(){
      const area=journey.getBoundingClientRect();
      if(area.bottom<0||area.top>innerHeight)return;
      const pivot=innerHeight*.43;
      let chosen=0,distance=Infinity;
      chapters.forEach((chapter,i)=>{
        const rect=chapter.getBoundingClientRect();
        const gap=rect.top<=pivot&&rect.bottom>=pivot?0:Math.min(Math.abs(rect.top-pivot),Math.abs(rect.bottom-pivot));
        if(gap<distance){distance=gap;chosen=i;}
      });
      activate(chosen);
    }
    addEventListener('scroll',()=>{
      if(pending)return;pending=true;
      requestAnimationFrame(()=>{pending=false;update();});
    },{passive:true});
    addEventListener('resize',update);
    update();
  });
  // El contenido sigue visible con movimiento reducido.
  if(reduced)document.querySelectorAll('.journey-image').forEach(img=>img.style.transition='none');
})();
