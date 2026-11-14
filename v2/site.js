(function(){
  var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s,r){return (r||d).querySelector(s)}
  function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))}

  /* header: shadow + tabs tuck away on the way down */
  var hd=$('.hd'),ly=0;
  if(hd)addEventListener('scroll',function(){var y=scrollY;
    if(y>ly+6&&y>220)hd.classList.add('min');else if(y<ly-6||y<=220)hd.classList.remove('min');
    hd.classList.toggle('sc',y>8);ly=y},{passive:true});

  /* menu and search */
  function dlg(btn,id,onopen){var b=$(btn),g=d.getElementById(id);if(!b||!g||!g.showModal)return;
    b.addEventListener('click',function(){g.showModal();b.setAttribute('aria-expanded','true');if(onopen)onopen(g)});
    g.addEventListener('close',function(){b.setAttribute('aria-expanded','false')});
    g.addEventListener('click',function(ev){if(ev.target===g||ev.target.closest('[data-close]')||ev.target.closest('a'))g.close()});}
  dlg('.menu','drawer');
  var sx=d.getElementById('sx'),items=sx?JSON.parse(sx.textContent):[],list=$('.sr-list'),inp=$('.sr-bar input'),none=$('.sr-none');
  function render(q){if(!list)return;q=(q||'').trim().toLowerCase();list.textContent='';var n=0;
    items.forEach(function(it){if(q&&(it.n+' '+it.s).toLowerCase().indexOf(q)<0)return;n++;
      var li=d.createElement('li'),a=d.createElement('a'),im=d.createElement('img'),sp=d.createElement('span'),b=d.createElement('b'),sm=d.createElement('small');
      a.href=it.u;im.src=it.i;im.alt='';im.width=56;im.height=56;im.loading='lazy';b.textContent=it.n;sm.textContent=it.s;
      sp.appendChild(b);sp.appendChild(sm);a.appendChild(im);a.appendChild(sp);li.appendChild(a);list.appendChild(li)});
    if(none)none.hidden=n>0;}
  dlg('.search','srch',function(){render('');if(inp){inp.value='';inp.focus()}});
  if(inp){inp.addEventListener('input',function(){render(inp.value)});inp.addEventListener('keydown',function(ev){if(ev.key==='Escape'){ev.preventDefault();d.getElementById('srch').close()}})}

  /* shop filter from the category tabs */
  var cards=$$('.p[data-cat]'),shop=d.getElementById('shop'),names={all:'Trays & boxes',wood:'Acacia wood',resin:'Resin trays'};
  function filter(k){if(!names[k])k='all';
    $$('.tabs a[data-cat]').forEach(function(a){if(a.dataset.cat===k)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
    cards.forEach(function(p){p.hidden=!(k==='all'||p.dataset.cat===k)});
    var t=d.getElementById('shop-t'),va=d.getElementById('viewall');if(t)(t.firstElementChild||t).textContent=names[k];if(va)va.hidden=(k==='all');}
  if(shop){
    $$('.tabs a[data-cat], #viewall, .drawer a[data-cat]').forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();filter(a.dataset.cat||'all');
      shop.scrollIntoView({behavior:rm?'auto':'smooth',block:'start'})})});
    var f=new URLSearchParams(location.search).get('f');if(f)filter(f);
  }

  /* reveal on scroll: headings rise out of a slot, cards stagger by the real number of columns */
  $$('main h2').forEach(function(h){if(!h.closest('.rv'))return;var s=d.createElement('span');while(h.firstChild)s.appendChild(h.firstChild);h.appendChild(s);h.classList.add('mk')});
  var rv=$$('.rv,.wipe,.mega');
  if(rm||!('IntersectionObserver' in window)){rv.forEach(function(x){x.classList.add('in')})}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;var t=en.target,w=0,pa=t.parentNode;
      if(t.classList.contains('p')||t.classList.contains('tile')||pa.classList.contains('dz')||pa.classList.contains('real')){
        w=(Array.prototype.indexOf.call(pa.children,t)%Math.max(1,Math.round(pa.clientWidth/(t.offsetWidth||1))))*90}
      setTimeout(function(){t.classList.add('in')},w);io.unobserve(t)})},{rootMargin:'0px 0px -7% 0px'});
    rv.forEach(function(x){io.observe(x)});}

  /* the workshop paragraph lights up word by word as it is scrolled into the reading zone */
  var wl=$('#workshop .lead');
  if(wl&&!rm){var ws=wl.textContent.trim().split(/\s+/),offs=[],tk=false;wl.textContent='';
    ws.forEach(function(w,i){var s=d.createElement('span');s.textContent=w;wl.appendChild(s);if(i<ws.length-1)wl.appendChild(d.createTextNode(' '))});
    var sp=$$('span',wl);
    function measure(){var w=wl.offsetWidth||1;offs=sp.map(function(s){return s.offsetTop+s.offsetLeft/w*s.offsetHeight})}
    function lit(){tk=false;var r=wl.getBoundingClientRect(),vh=innerHeight;if(r.top>vh||r.bottom<0)return;
      var a=vh*.92,b=vh*.62;sp.forEach(function(s,i){var t=(a-(r.top+offs[i]))/(a-b);s.style.opacity=(.22+.78*(t<0?0:t>1?1:t)).toFixed(2)})}
    measure();lit();
    addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(lit)}},{passive:true});
    addEventListener('resize',function(){measure();lit()});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(function(){measure();lit()});}

  /* the floating WhatsApp button steps aside where a WhatsApp button is already on screen */
  var fab=$('.fab');
  if(fab&&'IntersectionObserver' in window){var near=[],fo=new IntersectionObserver(function(es){es.forEach(function(en){var i=near.indexOf(en.target);
      if(en.isIntersecting&&i<0)near.push(en.target);else if(!en.isIntersecting&&i>=0)near.splice(i,1)});fab.classList.toggle('off',near.length>0)});
    $$('.end,.ft').forEach(function(x){fo.observe(x)});}

  /* hero pictures */
  var sl=$$('.slide'),dt=$$('.dot'),hero=$('.hero');
  if(sl.length&&hero){var cur=0,show=$('.show'),pb=$('.pp'),st={user:false,hov:false,foc:false,out:false},x0=null,y0=0,sw=false;
    /* later pictures are fetched one ahead, not all at first paint */
    function load(i){var im=$('img',sl[(i+sl.length)%sl.length]);if(im&&im.dataset.src){im.src=im.dataset.src;im.removeAttribute('data-src')}}
    function go(n){sl[cur].classList.remove('on');dt[cur].removeAttribute('aria-current');cur=(n+sl.length)%sl.length;load(cur);
      sl[cur].classList.add('on');dt[cur].setAttribute('aria-current','true');setTimeout(function(){load(cur+1)},2500)}
    function sync(){hero.classList.toggle('paused',st.user||st.hov||st.foc||st.out||d.hidden);
      if(pb){pb.setAttribute('aria-pressed',String(st.user));pb.setAttribute('aria-label',st.user?'Play pictures':'Pause pictures')}}
    /* the dot's fill animation is the only clock: when it ends, the next picture comes. Pausing the animation pauses everything */
    hero.addEventListener('animationend',function(ev){if(ev.animationName==='fill')go(cur+1)});
    dt.forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.i)})});
    if(pb)pb.addEventListener('click',function(){st.user=!st.user;sync()});
    if(matchMedia('(hover:hover)').matches){show.addEventListener('mouseenter',function(){st.hov=true;sync()});show.addEventListener('mouseleave',function(){st.hov=false;sync()})}
    hero.addEventListener('focusin',function(ev){st.foc=ev.target!==pb&&ev.target.matches(':focus-visible');sync()});
    hero.addEventListener('focusout',function(){st.foc=false;sync()});
    d.addEventListener('visibilitychange',sync);
    if('IntersectionObserver' in window)new IntersectionObserver(function(es){st.out=!es[0].isIntersecting;sync()}).observe(hero);
    /* swipe on phones */
    show.addEventListener('touchstart',function(ev){x0=ev.touches[0].clientX;y0=ev.touches[0].clientY},{passive:true});
    show.addEventListener('touchend',function(ev){if(x0===null)return;var t=ev.changedTouches[0],dx=t.clientX-x0,dy=t.clientY-y0;x0=null;
      if(Math.abs(dx)>44&&Math.abs(dx)>Math.abs(dy)*1.5){sw=true;go(cur+(dx<0?1:-1));setTimeout(function(){sw=false},400)}},{passive:true});
    show.addEventListener('click',function(ev){if(sw){ev.preventDefault();sw=false}},true);
    addEventListener('load',function(){setTimeout(function(){load(1)},1200)});
    sync();}
})();
