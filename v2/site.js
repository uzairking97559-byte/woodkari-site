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
    var t=d.getElementById('shop-t'),va=d.getElementById('viewall');if(t)t.textContent=names[k];if(va)va.hidden=(k==='all');}
  if(shop){
    $$('.tabs a[data-cat], #viewall, .drawer a[data-cat]').forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();filter(a.dataset.cat||'all');
      shop.scrollIntoView({behavior:rm?'auto':'smooth',block:'start'})})});
    var f=new URLSearchParams(location.search).get('f');if(f)filter(f);
  }

  /* reveal on scroll */
  var rv=$$('.rv,.wipe');
  if(rm||!('IntersectionObserver' in window)){rv.forEach(function(x){x.classList.add('in')})}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;var t=en.target,w=0;
      if(t.classList.contains('p')||t.classList.contains('tile')||t.parentNode.classList.contains('dz')){w=(Array.prototype.indexOf.call(t.parentNode.children,t)%3)*110}
      setTimeout(function(){t.classList.add('in')},w);io.unobserve(t)})},{rootMargin:'0px 0px -7% 0px'});
    rv.forEach(function(x){io.observe(x)});}

  /* hero pictures */
  var sl=$$('.slide'),dt=$$('.dot'),hero=$('.hero');
  if(sl.length&&hero){var cur=0,tm=null;
    function go(n){sl[cur].classList.remove('on');dt[cur].removeAttribute('aria-current');cur=(n+sl.length)%sl.length;
      sl[cur].classList.add('on');dt[cur].setAttribute('aria-current','true');}
    function play(){if(rm)return;clearInterval(tm);tm=setInterval(function(){go(cur+1)},5500);hero.classList.remove('paused')}
    function stop(){clearInterval(tm);hero.classList.add('paused')}
    dt.forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.i);play()})});
    var show=$('.show');show.addEventListener('mouseenter',stop);show.addEventListener('mouseleave',play);
    d.addEventListener('visibilitychange',function(){d.hidden?stop():play()});
    if(rm)hero.classList.add('paused');play();}
})();
