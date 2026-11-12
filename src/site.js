(function(){
'use strict';
var C=window.FELT_CONFIG||{},pro=null;
try{pro=JSON.parse(localStorage.getItem('fb:pro')||'null')}catch(e){}

/* ads: loaded only when an AdSense client id is configured and Pro is not active */
if(C.adsenseClient&&!pro){
  var s=document.createElement('script');s.async=true;s.crossOrigin='anonymous';
  s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+encodeURIComponent(C.adsenseClient);
  document.head.appendChild(s);
  document.querySelectorAll('.ad').forEach(function(el){
    var id=(C.adSlots||{})[el.getAttribute('data-ad')];if(!id)return;
    var l=document.createElement('span');l.className='ad-l';l.textContent=el.getAttribute('data-label')||'Advertisement';
    var ins=document.createElement('ins');ins.className='adsbygoogle';ins.style.display='block';
    ins.setAttribute('data-ad-client',C.adsenseClient);ins.setAttribute('data-ad-slot',id);
    ins.setAttribute('data-ad-format','auto');ins.setAttribute('data-full-width-responsive','true');
    el.appendChild(l);el.appendChild(ins);(window.adsbygoogle=window.adsbygoogle||[]).push({});
  });
}

/* pricing buttons */
var buy=document.getElementById('buy'),soon=document.getElementById('soon'),act=document.getElementById('proActive'),price=document.getElementById('price');
if(buy){
  if(price&&C.proPrice)price.textContent=C.proPrice;
  if(pro){act.hidden=false}
  else if(C.proCheckoutUrl){buy.href=C.proCheckoutUrl;buy.hidden=false}
  else soon.hidden=false;
}
var em=document.querySelectorAll('[data-email]');
em.forEach(function(e){if(C.contactEmail)e.textContent=C.contactEmail});

/* language menu: close when clicking elsewhere or pressing Escape */
var dd=document.querySelector('.langdd');
if(dd){
  document.addEventListener('click',function(ev){if(dd.open&&!dd.contains(ev.target))dd.open=false});
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&dd.open){dd.open=false;dd.querySelector('summary').focus()}});
}
document.querySelectorAll('[data-mailto]').forEach(function(a){if(C.contactEmail)a.href='mailto:'+C.contactEmail});

/* back to top: shown after scrolling down one screen */
var tt=document.getElementById('totop');
if(tt){
  var onScroll=function(){tt.classList.toggle('show',window.scrollY>window.innerHeight*.6)};
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  tt.addEventListener('click',function(ev){ev.preventDefault();var r=matchMedia('(prefers-reduced-motion: reduce)').matches;window.scrollTo({top:0,behavior:r?'auto':'smooth'})});
}

/* hero demo: a small pad you can draw on */
var cv=document.getElementById('demo');if(!cv)return;
var ctx=cv.getContext('2d'),strokes=[],cur=null,color='blue',W=1,H=1;
function col(n){return getComputedStyle(document.documentElement).getPropertyValue('--m-'+n).trim()}
function path(p){
  ctx.beginPath();ctx.moveTo(p[0]*W,p[1]*H);
  if(p.length<4){ctx.lineTo(p[0]*W+.01,p[1]*H);return}
  for(var i=2;i<p.length-2;i+=2)ctx.quadraticCurveTo(p[i]*W,p[i+1]*H,(p[i]+p[i+2])/2*W,(p[i+1]+p[i+3])/2*H);
  ctx.lineTo(p[p.length-2]*W,p[p.length-1]*H);
}
function draw(){
  var d=window.devicePixelRatio||1;ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,W,H);ctx.lineCap='round';ctx.lineJoin='round';
  strokes.concat(cur?[cur]:[]).forEach(function(s){ctx.strokeStyle=col(s.c);ctx.lineWidth=Math.max(3,Math.min(6,W/120));path(s.p);ctx.stroke()});
}
function size(){var r=cv.getBoundingClientRect(),d=window.devicePixelRatio||1;W=Math.max(1,r.width);H=Math.max(1,r.height);cv.width=Math.round(W*d);cv.height=Math.round(H*d);draw()}
function seed(){
  var a=[],b=[],c=[],i;
  for(i=0;i<=40;i++){var t=i/40*Math.PI*2;a.push(.3+.1*Math.cos(t),.52+.17*Math.sin(t))}
  for(i=0;i<=24;i++){b.push(.44+i/24*.25,.52+.012*Math.sin(i/24*Math.PI*3))}
  c=[.65,.45,.7,.52,.65,.6];
  var e=[];for(i=0;i<=40;i++){var u=i/40*Math.PI*2;e.push(.81+.08*Math.cos(u),.52+.14*Math.sin(u))}
  strokes=[{c:'blue',p:a},{c:'ink',p:b},{c:'ink',p:c},{c:'red',p:e}];
}
function pt(e){var r=cv.getBoundingClientRect();return[(e.clientX-r.left)/W,(e.clientY-r.top)/H]}
cv.addEventListener('pointerdown',function(e){try{cv.setPointerCapture(e.pointerId)}catch(_){}cur={c:color,p:pt(e)};var h=document.getElementById('hint');if(h)h.hidden=true;draw()});
cv.addEventListener('pointermove',function(e){if(!cur)return;var p=pt(e);cur.p.push(p[0],p[1]);draw()});
function up(){if(cur){strokes.push(cur);cur=null;draw()}}
cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
document.querySelectorAll('.demo .cap').forEach(function(b){b.addEventListener('click',function(){color=b.getAttribute('data-c');document.querySelectorAll('.demo .cap').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))})})});
var clr=document.getElementById('demoClear');if(clr)clr.addEventListener('click',function(){strokes=[];draw()});
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',draw)}catch(e){}
seed();new ResizeObserver(size).observe(cv);size();
})();
