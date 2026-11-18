(function(){
  var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s,r){return (r||d).querySelector(s)}
  function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))}

  /* header: shadow + tabs tuck away on the way down */
  var hd=$('.hd'),ly=scrollY,run=0;
  if(hd)addEventListener('scroll',function(){var y=scrollY,dy=y-ly;ly=y;
    run=(dy>0)===(run>0)?run+dy:dy; /* distance covered in the current direction */
    if(y<=220||run<-24)hd.classList.remove('min');else if(run>48)hd.classList.add('min');
    hd.classList.toggle('sc',y>8)},{passive:true});

  d.addEventListener('touchstart',function(){},{passive:true}); /* lets :active work on iOS */

  /* menu and search */
  function dlg(btn,id,onopen){var bs=$$(btn),g=d.getElementById(id);if(!bs.length||!g||!g.showModal)return;
    bs.forEach(function(b){b.addEventListener('click',function(){g.showModal();bs.forEach(function(x){x.setAttribute('aria-expanded','true')});if(onopen)onopen(g)})});
    g.addEventListener('close',function(){bs.forEach(function(x){x.setAttribute('aria-expanded','false')})});
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

  /* page transition: only the tapped card's picture travels to the product page (and back) */
  $$('.p').forEach(function(a){a.addEventListener('click',function(){
    $$('[style*="view-transition-name"]').forEach(function(x){x.style.viewTransitionName=''});
    var im=$('.ph img',a);if(im)im.style.viewTransitionName='pic'})});

  /* category menu: one shared dropdown panel under the tab row (tap to open on phones, hover or click on desktop) */
  var tn=$('.tn'),sub=tn&&$('.sub',tn),gs=tn?$$('a.g',tn):[],openG=null,hov=matchMedia('(hover:hover) and (pointer:fine)');
  function closeSub(){if(!sub)return;sub.hidden=true;gs.forEach(function(a){a.setAttribute('aria-expanded','false')});openG=null}
  function openSub(a){if(!sub)return;$$('.sub-set',sub).forEach(function(x){x.hidden=x.dataset.for!==a.dataset.g});
    gs.forEach(function(x){x.setAttribute('aria-expanded',String(x===a))});sub.hidden=false;openG=a;
    var nr=$('nav',tn),l=a.getBoundingClientRect().left-tn.getBoundingClientRect().left,w=sub.offsetWidth,max=tn.clientWidth-w-8;
    if(innerWidth>=900)sub.style.left=Math.max(8,Math.min(l,max))+'px';else sub.style.left='0'}
  gs.forEach(function(a){
    a.addEventListener('click',function(ev){ev.preventDefault();if(openG===a)closeSub();else openSub(a)});
    a.addEventListener('mouseenter',function(){if(hov.matches&&innerWidth>=900)openSub(a)})});
  if(tn){tn.addEventListener('mouseleave',function(){if(hov.matches&&innerWidth>=900)closeSub()});
    d.addEventListener('click',function(ev){if(openG&&!ev.target.closest('.tn'))closeSub()});
    d.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&openG){var g=openG;closeSub();g.focus()}});
    addEventListener('scroll',function(){if(openG&&!hov.matches)closeSub()},{passive:true});}

  /* old links (index.html?f=wood) go to the new All pieces page */
  var old=new URLSearchParams(location.search).get('f');
  if(old&&d.getElementById('newarr'))location.replace('shop.html'+(old==='wood'?'?c=acacia':old==='resin'?'?c=resin-trays':''));

  /* All pieces: filter by kind with the chips (every card has data-cats) */
  var grid=d.getElementById('all-grid');
  if(grid){var pc=$$('.p',grid),chips=$$('#shop-chips a'),hh=d.getElementById('shop-h'),cn=d.getElementById('shop-n'),none=d.getElementById('shop-none'),
      nm={all:'All pieces'};chips.forEach(function(a){nm[a.dataset.c]=a.firstChild.textContent});
    $$('.tn a.g').forEach(function(a){nm[a.dataset.g]=a.textContent});
    function apply(k,push){if(!nm[k])k='all';var n=0;
      pc.forEach(function(p){var on=k==='all'||(' '+p.dataset.cats+' ').indexOf(' '+k+' ')>=0;p.hidden=!on;if(on)n++});
      chips.forEach(function(a){if(a.dataset.c===k||a.dataset.p===k)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
      $$('.tn nav a[data-has],.tn nav a[data-c]').forEach(function(a){var h=(a.dataset.has||a.dataset.c||'').split(' ');if(k!=='all'&&h.indexOf(k)>=0)a.setAttribute('aria-current','true');else if(a.dataset.c==='all'&&k==='all')a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
      if(hh)hh.textContent=nm[k];if(cn)cn.textContent=n;if(none)none.hidden=n>0;
      if(push){try{history.replaceState(null,'',location.pathname+(k==='all'?'':'?c='+k))}catch(_){}}}
    chips.forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();apply(a.dataset.c,true);closeSub()})});
    apply(new URLSearchParams(location.search).get('c')||'all',false);}

  /* reveal on scroll: headings rise out of a slot, cards stagger by the real number of columns */
  $$('main h2').forEach(function(h){if(!h.closest('.rv'))return;var s=d.createElement('span');while(h.firstChild)s.appendChild(h.firstChild);h.appendChild(s);h.classList.add('mk')});
  var rv=$$('.rv,.wipe,.mega');
  if(rm||!('IntersectionObserver' in window)){rv.forEach(function(x){x.classList.add('in')})}
  else{var gap=[0,70,120,150],io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;var t=en.target,row=[t],pa=t.parentNode;
      /* cards on one visual row, and a whole side-scrolling strip, come in together, left to right; nothing is still hidden when it is swiped into view */
      if(pa.matches('.grid,.tiles,.dz,.real')){var top=t.offsetTop;row=$$('.rv',pa).filter(function(x){return !x.dataset.rv&&x.offsetTop===top})}
      row.forEach(function(x,i){x.dataset.rv=1;io.unobserve(x);setTimeout(function(){x.classList.add('in')},gap[Math.min(i,3)])})})},{rootMargin:'0px 0px -7% 0px'});
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
  if(sl.length&&hero){var cur=0,z=1,show=$('.show'),pb=$('.pp'),st={user:false,hov:false,foc:false,out:false},x0=null,y0=0,sw=false;
    /* later pictures are fetched one ahead, not all at first paint */
    function load(i){var im=$('img',sl[(i+sl.length)%sl.length]);if(im&&im.dataset.src){im.src=im.dataset.src;im.removeAttribute('data-src')}}
    /* the new picture fades in ON TOP; the old one stays solid underneath until it is covered (no dip to the dark ground) */
    function tidy(){sl.forEach(function(s,i){if(i!==cur)s.classList.remove('on')})}
    function go(n){n=(n+sl.length)%sl.length;if(n===cur)return;dt[cur].removeAttribute('aria-current');cur=n;load(n);
      var s=sl[n],was=s.classList.contains('on');s.style.zIndex=++z;s.classList.add('on');dt[n].setAttribute('aria-current','true');
      if(rm||(was&&getComputedStyle(s).opacity==='1'))tidy();setTimeout(function(){load(cur+1)},2500)}
    sl.forEach(function(s){s.addEventListener('transitionend',function(ev){if(ev.target===s&&s===sl[cur])tidy()})});
    function sync(){hero.classList.toggle('paused',st.user||st.hov||st.foc||st.out||d.hidden);
      if(pb){pb.setAttribute('aria-pressed',String(st.user));pb.setAttribute('aria-label',st.user?'Play pictures':'Pause pictures')}}
    /* the dot's fill animation is the only clock: when it ends, the next picture comes. Pausing the animation pauses everything */
    hero.addEventListener('animationend',function(ev){if(ev.animationName!=='fill')return;var c=cur,im=$('img',sl[(c+1)%sl.length]);load(c+1);
      function nx(){if(cur===c)go(c+1)} /* on a slow connection, wait for the next picture instead of fading to an empty frame */
      if(im&&im.decode)im.decode().then(nx,nx);else nx()});
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

  /* product gallery: arrows + small pictures (owner 16 Nov) */
  $$('.galw.has-th').forEach(function(w){var g=$('.gal',w),th=$$('.th',w),pv=$('.gprev',w),nx=$('.gnext',w),n=th.length,cur=0,lock=0;
    function show(i,smooth){i=Math.max(0,Math.min(n-1,i));lock=Date.now()+700;mark(i);g.scrollTo({left:i*g.clientWidth,behavior:(smooth&&!rm)?'smooth':'auto'})}
    function mark(i){if(i===cur)return;cur=i;th.forEach(function(t,j){t.classList.toggle('on',j===i);if(j===i)t.setAttribute('aria-current','true');else t.removeAttribute('aria-current')});
      pv.disabled=i===0;nx.disabled=i===n-1;var t=th[i];if(t&&t.scrollIntoView)t.scrollIntoView({block:'nearest',inline:'nearest'})}
    th.forEach(function(t,j){t.addEventListener('click',function(){show(j,true)})});
    pv.addEventListener('click',function(){show(cur-1,true)});nx.addEventListener('click',function(){show(cur+1,true)});
    var tk;g.addEventListener('scroll',function(){clearTimeout(tk);tk=setTimeout(function(){if(Date.now()<lock)return;mark(Math.round(g.scrollLeft/Math.max(1,g.clientWidth)))},80)},{passive:true});
    w.addEventListener('keydown',function(ev){if(ev.key==='ArrowRight'){show(cur+1,true)}else if(ev.key==='ArrowLeft'){show(cur-1,true)}});
  });
})();
