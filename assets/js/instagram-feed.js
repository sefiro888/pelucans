/* Feed Behold v2: nunca sustituye la reserva local si la respuesta no es válida. */
(() => {
  'use strict';
  const grids=[...document.querySelectorAll('[data-ig-feed]')];
  if(!grids.length)return;
  const base=window.PEL_ROOT||'';
  const cacheKey='pelucans-instagram-feed-v2';
  const safe=value=>{try{const url=new URL(value);return url.protocol==='https:'?url.href:'';}catch{return '';}};
  function render(posts,live){
    const valid=posts.slice(0,9).map(post=>{
      const image=safe(post.sizes?.medium?.mediaUrl||post.sizes?.small?.mediaUrl||post.thumbnailUrl||post.mediaUrl);
      const link=safe(post.permalink);
      if(!image||!link)return null;
      const card=document.createElement('a');card.href=link;card.target='_blank';card.rel='noopener';
      const caption=String(post.prunedCaption||post.caption||'Pelucans').split('\n')[0].slice(0,110);
      card.setAttribute('aria-label',caption);
      const img=document.createElement('img');img.src=image;img.alt=caption;img.loading='lazy';card.append(img);
      const label=document.createElement('span');label.className='cap';label.textContent=caption;card.append(label);
      if(post.mediaType==='VIDEO'){const play=document.createElement('span');play.className='tp';play.textContent='▶';play.setAttribute('aria-hidden','true');card.append(play);}
      return card;
    }).filter(Boolean);
    if(!valid.length)return false;
    grids.forEach(grid=>grid.replaceChildren(...valid.map(card=>card.cloneNode(true))));
    document.querySelectorAll('[data-ig-live]').forEach(tag=>{tag.hidden=!live;});
    return true;
  }
  async function start(){
    let settings={};
    try{const res=await fetch(base+'assets/config/social.json',{cache:'no-store'});if(res.ok)settings=await res.json();}catch{}
    const url=safe(settings.instagramFeedUrl||grids[0].dataset.igFeed);
    if(!url)return; // Sin conectar, se mantiene el muro de publicaciones seleccionadas.
    try{const cached=JSON.parse(localStorage.getItem(cacheKey)||'null');if(cached?.url===url&&Date.now()-cached.at<86400000)render(cached.posts,false);}catch{}
    let running=false;
    async function refresh(){
      if(running||document.hidden)return;
      running=true;
      try{
        const response=await fetch(url,{cache:'no-store',signal:AbortSignal.timeout(12000)});
        if(!response.ok)return;
        const json=await response.json();const posts=Array.isArray(json)?json:json.posts;
        if(!Array.isArray(posts)||!posts.length)return;
        if(render(posts,true)){try{localStorage.setItem(cacheKey,JSON.stringify({url,at:Date.now(),posts:posts.slice(0,9)}));}catch{}}
      }catch{}finally{running=false;}
    }
    await refresh();
    setInterval(refresh,Math.max(5,Number(settings.refreshMinutes)||10)*60000);
    document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
  }
  start();
})();
