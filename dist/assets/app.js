(function(){
'use strict';
const C=window.FELT_CONFIG||{};
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
const LS={
  get(k,d){try{const v=localStorage.getItem(k);return v==null?d:JSON.parse(v)}catch(e){return d}},
  set(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true}catch(e){return false}},
  del(k){try{localStorage.removeItem(k)}catch(e){}}
};

/* ---------- languages ---------- */
const T={
en:{select:'Select and move (V)',hand:'Move around the board (H)',pen:'Marker (P)',eraser:'Eraser (E)',sticky:'Sticky note (N)',text:'Text (T)',shape:'Shape (S)',arrow:'Connecting arrow (L)',
 rect:'Rectangle',ellipse:'Ellipse',tri:'Triangle',diamond:'Diamond',undo:'Undo',redo:'Redo',export:'Export board as PNG',boards:'Your boards',
 dup:'Duplicate',front:'To front',del:'Delete',zoomIn:'Zoom in',zoomOut:'Zoom out',fit:'Fit everything on screen',
 cInk:'Black',cBlue:'Blue',cRed:'Red',cGreen:'Green',cAmber:'Yellow',cViolet:'Purple',thin:'Thin',medium:'Medium',thick:'Thick',
 empty1:'Pick a marker and draw.',empty2:'With the select tool, double-tap for a sticky note.',
 boardsTitle:'Your boards',boardsNote:'Boards are saved in this browser, on this device.',newBoard:'New board',backup:'Back up boards',restore:'Restore',
 rename:'Rename',untitled:'Untitled board',firstBoard:'My first board',confirmDel:'Delete "{name}"? This cannot be undone.',renamePrompt:'Board name',
 limit:'The free plan keeps {n} boards. Go Pro for unlimited boards, or delete one first.',
 goPro:'Go Pro',proOn:'Pro',proTitle:'SiteWhiteboard Pro',pro1:'Unlimited boards',pro2:'No ads anywhere on the site',pro3:'Sharper exports without the SiteWhiteboard mark',pro4:'Back up and restore your boards as a file',
 proActive:'Pro is active in this browser.',buy:'Get Pro',proSoon:'Pro is not on sale yet.',haveKey:'Already bought Pro? Enter your licence key.',activate:'Activate',close:'Close',proOff:'Remove Pro from this browser',
 keyBad:'That key was not accepted. Check it and try again.',keyOk:'Pro activated.',keyErr:'The key could not be checked. Check your connection and try again.',
 nothing:'Nothing to export yet. Draw something first.',exported:'Exported',storageFull:'This browser is out of storage space. Delete a board or export your work.',
 restored:'Boards restored: {n}',restoreBad:'That file is not a SiteWhiteboard backup.',needPro:'Backup and restore come with Pro.',wm:'Made with SiteWhiteboard',
 wTitle:'Welcome to SiteWhiteboard',w1:'Pick a marker from the tray and draw anywhere',w2:'Two fingers, or the hand tool, move and zoom the board',w3:'With the select tool, double-tap for a new note. Delete these when you are ready.',wIdea:'Idea',wPlan:'Plan'},
fr:{select:'Sélectionner et déplacer (V)',hand:'Se déplacer sur le tableau (H)',pen:'Marqueur (P)',eraser:'Gomme (E)',sticky:'Post-it (N)',text:'Texte (T)',shape:'Forme (S)',arrow:'Flèche de liaison (L)',
 rect:'Rectangle',ellipse:'Ellipse',tri:'Triangle',diamond:'Losange',undo:'Annuler',redo:'Rétablir',export:'Exporter le tableau en PNG',boards:'Vos tableaux',
 dup:'Dupliquer',front:'Premier plan',del:'Supprimer',zoomIn:'Zoom avant',zoomOut:'Zoom arrière',fit:'Tout afficher à l’écran',
 cInk:'Noir',cBlue:'Bleu',cRed:'Rouge',cGreen:'Vert',cAmber:'Jaune',cViolet:'Violet',thin:'Fin',medium:'Moyen',thick:'Épais',
 empty1:'Prenez un marqueur et dessinez.',empty2:'Avec l’outil de sélection, touchez deux fois pour un post-it.',
 boardsTitle:'Vos tableaux',boardsNote:'Les tableaux sont enregistrés dans ce navigateur, sur cet appareil.',newBoard:'Nouveau tableau',backup:'Sauvegarder',restore:'Restaurer',
 rename:'Renommer',untitled:'Tableau sans titre',firstBoard:'Mon premier tableau',confirmDel:'Supprimer « {name} » ? Cette action est définitive.',renamePrompt:'Nom du tableau',
 limit:'L’offre gratuite garde {n} tableaux. Passez à Pro pour des tableaux illimités, ou supprimez-en un.',
 goPro:'Passer à Pro',proOn:'Pro',proTitle:'SiteWhiteboard Pro',pro1:'Tableaux illimités',pro2:'Aucune publicité sur le site',pro3:'Exports plus nets, sans la mention SiteWhiteboard',pro4:'Sauvegarde et restauration de vos tableaux dans un fichier',
 proActive:'Pro est actif dans ce navigateur.',buy:'Obtenir Pro',proSoon:'Pro n’est pas encore en vente.',haveKey:'Vous avez déjà acheté Pro ? Saisissez votre clé de licence.',activate:'Activer',close:'Fermer',proOff:'Retirer Pro de ce navigateur',
 keyBad:'Cette clé n’a pas été acceptée. Vérifiez-la et réessayez.',keyOk:'Pro activé.',keyErr:'La clé n’a pas pu être vérifiée. Vérifiez votre connexion et réessayez.',
 nothing:'Rien à exporter pour l’instant. Dessinez d’abord quelque chose.',exported:'Exporté',storageFull:'Ce navigateur n’a plus d’espace de stockage. Supprimez un tableau ou exportez votre travail.',
 restored:'Tableaux restaurés : {n}',restoreBad:'Ce fichier n’est pas une sauvegarde SiteWhiteboard.',needPro:'La sauvegarde et la restauration font partie de Pro.',wm:'Créé avec SiteWhiteboard',
 wTitle:'Bienvenue sur SiteWhiteboard',w1:'Prenez un marqueur dans le plumier et dessinez où vous voulez',w2:'Deux doigts, ou l’outil main, pour déplacer et zoomer',w3:'Avec l’outil de sélection, touchez deux fois pour un post-it. Supprimez ceux-ci quand vous voulez.',wIdea:'Idée',wPlan:'Plan'},
ar:{select:'تحديد وتحريك (V)',hand:'التنقل في اللوحة (H)',pen:'قلم (P)',eraser:'ممحاة (E)',sticky:'ورقة لاصقة (N)',text:'نص (T)',shape:'شكل (S)',arrow:'سهم ربط (L)',
 rect:'مستطيل',ellipse:'شكل بيضاوي',tri:'مثلث',diamond:'معيّن',undo:'تراجع',redo:'إعادة',export:'تصدير اللوحة بصيغة PNG',boards:'لوحاتك',
 dup:'تكرار',front:'إلى الأمام',del:'حذف',zoomIn:'تكبير',zoomOut:'تصغير',fit:'إظهار كل شيء على الشاشة',
 cInk:'أسود',cBlue:'أزرق',cRed:'أحمر',cGreen:'أخضر',cAmber:'أصفر',cViolet:'بنفسجي',thin:'رفيع',medium:'متوسط',thick:'سميك',
 empty1:'اختر قلمًا وابدأ الرسم.',empty2:'بأداة التحديد، انقر مرتين لإضافة ورقة لاصقة.',
 boardsTitle:'لوحاتك',boardsNote:'تُحفظ اللوحات في هذا المتصفح، على هذا الجهاز.',newBoard:'لوحة جديدة',backup:'نسخ احتياطي',restore:'استعادة',
 rename:'إعادة تسمية',untitled:'لوحة بلا عنوان',firstBoard:'لوحتي الأولى',confirmDel:'حذف «{name}»؟ لا يمكن التراجع عن ذلك.',renamePrompt:'اسم اللوحة',
 limit:'الخطة المجانية تحفظ {n} لوحات. اشترك في Pro للحصول على لوحات غير محدودة، أو احذف لوحة أولًا.',
 goPro:'اشترك في Pro',proOn:'Pro',proTitle:'SiteWhiteboard Pro',pro1:'لوحات غير محدودة',pro2:'بدون إعلانات في الموقع',pro3:'تصدير أوضح بدون علامة SiteWhiteboard',pro4:'نسخ احتياطي واستعادة للوحاتك في ملف',
 proActive:'Pro مفعّل في هذا المتصفح.',buy:'احصل على Pro',proSoon:'Pro غير متاح للبيع بعد.',haveKey:'اشتريت Pro من قبل؟ أدخل مفتاح الترخيص.',activate:'تفعيل',close:'إغلاق',proOff:'إزالة Pro من هذا المتصفح',
 keyBad:'لم يُقبل هذا المفتاح. تحقق منه وحاول مرة أخرى.',keyOk:'تم تفعيل Pro.',keyErr:'تعذّر التحقق من المفتاح. تحقق من اتصالك وحاول مرة أخرى.',
 nothing:'لا يوجد ما يُصدَّر بعد. ارسم شيئًا أولًا.',exported:'تم التصدير',storageFull:'لم تعد هناك مساحة تخزين في هذا المتصفح. احذف لوحة أو صدّر عملك.',
 restored:'اللوحات المستعادة: {n}',restoreBad:'هذا الملف ليس نسخة احتياطية من SiteWhiteboard.',needPro:'النسخ الاحتياطي والاستعادة ضمن Pro.',wm:'صُنع بواسطة SiteWhiteboard',
 wTitle:'مرحبًا بك في SiteWhiteboard',w1:'اختر قلمًا من الأسفل وارسم في أي مكان',w2:'بإصبعين، أو بأداة اليد، حرّك اللوحة وكبّرها',w3:'بأداة التحديد، انقر مرتين لورقة جديدة. احذف هذه الأوراق متى شئت.',wIdea:'فكرة',wPlan:'خطة'}
};
const TX={
en:{moreColors:'More colours and thickness',thickness:'Thickness',colors:'Colours',custom:'Custom colour',brand:'SiteWhiteboard',language:'Change language',account:'You',share:'Share board',shareNote:'Boards stay on this device, so there is no live link. Send a picture of the board instead.',shareImg:'Share as image',download:'Download PNG',copied:'Image copied. Paste it where you want.',guest:'Guest',you:'You',role:'Owner · this device',grid:'Show grid',namePrompt:'Your name'},
fr:{moreColors:'Plus de couleurs et épaisseur',thickness:'Épaisseur',colors:'Couleurs',custom:'Couleur personnalisée',brand:'SiteTableauBlanc',language:'Changer de langue',account:'Vous',share:'Partager',shareNote:'Les tableaux restent sur cet appareil : il n’y a pas de lien en direct. Envoyez plutôt une image du tableau.',shareImg:'Partager l’image',download:'Télécharger en PNG',copied:'Image copiée. Collez-la où vous voulez.',guest:'Invité',you:'Vous',role:'Propriétaire · cet appareil',grid:'Afficher la grille',namePrompt:'Votre nom'},
ar:{moreColors:'ألوان أخرى والسماكة',thickness:'السماكة',colors:'الألوان',custom:'لون مخصص',brand:'موقع اللوحة البيضاء',language:'تغيير اللغة',account:'أنت',share:'مشاركة اللوحة',shareNote:'اللوحات تبقى على هذا الجهاز، لذلك لا يوجد رابط مباشر. أرسل صورة للوحة بدلًا من ذلك.',shareImg:'مشاركة كصورة',download:'تنزيل PNG',copied:'تم نسخ الصورة. الصقها حيث تشاء.',guest:'ضيف',you:'أنت',role:'المالك · هذا الجهاز',grid:'إظهار الشبكة',namePrompt:'اسمك'}
};
for(const k in TX)Object.assign(T[k],TX[k]);
const FLAG={en:'<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice"><rect width="60" height="30" fill="#012169"/><path d="M0 0L60 30M60 0L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0L60 30M60 0L0 30" stroke="#C8102E" stroke-width="2"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg>',fr:'<svg viewBox="0 0 3 2" preserveAspectRatio="none"><rect width="1" height="2" fill="#0055A4"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#EF4135"/></svg>',ar:'<svg viewBox="0 0 30 20" preserveAspectRatio="xMidYMid slice"><rect width="30" height="20" fill="#C1272D"/><path d="M15 5L17.94 14.05L10.24 8.45H19.76L12.06 14.05Z" fill="none" stroke="#006233" stroke-width="1.1" stroke-linejoin="round"/></svg>'};
const LANGS=['en','fr','ar'],LNAME={en:'EN',fr:'FR',ar:'ع'};
let me=LS.get('fb:user','');
/* the address decides the language: /board/ = English, /fr/board/, /ar/board/ */
const pathLang=(location.pathname.match(/^\/(fr|ar)\//)||[])[1];
let lang=(pathLang||new URLSearchParams(location.search).get('lang')||(/\/board\//.test(location.pathname)?'en':'')||LS.get('fb:lang','')||(navigator.language||'en').slice(0,2)).toLowerCase();
if(!T[lang])lang='en';
const boardPath=l=>(l==='en'?'':'/'+l)+'/board/';
const tr=(k,v)=>{let s=(T[lang]&&T[lang][k])||T.en[k]||k;if(v)for(const n in v)s=s.replace('{'+n+'}',v[n]);return s};
function applyLang(){
  document.documentElement.lang=lang;document.documentElement.dir=lang==='ar'?'rtl':'ltr';
  $$('[data-t]').forEach(e=>{e.textContent=tr(e.dataset.t)});
  $$('[data-tt]').forEach(e=>{const s=tr(e.dataset.tt);e.title=s;e.setAttribute('aria-label',s)});
  $('#home').setAttribute('aria-label',tr('brand'));$('#home').href=lang==='en'?'/':'/'+lang+'/';$('#langTxt').textContent=LNAME[lang];$('#langFlag').innerHTML=FLAG[lang];$$('#langMenu button').forEach(b=>{if(b.dataset.l===lang)b.setAttribute('aria-current','true');else b.removeAttribute('aria-current')});$('#meTxt').textContent=(me||tr('guest'))+' ('+tr('you')+')';
  proUi();
}

/* ---------- drawing state ---------- */
const cv=$('#cv'),ctx=cv.getContext('2d'),wrap=$('#wrap'),ed=$('#ed');
const mctx=document.createElement('canvas').getContext('2d');
const KEYS=['ink','blue','red','green','amber','violet'];
const PALETTE=['#FFF4A8','#FFD84D','#B5860B','#FFFFFF','#F7D2AE','#FF9E4A','#9C4A0B','#E6E6E6','#FFC3C0','#FF6161',
 '#C2100F','#AAAAAA','#A7EBC6','#2CC45A','#067A30','#555555','#C6DAFF','#629DEF','#2D58AB','#1A1A1A','#DCD6FF','#8F7FEA','#6B2FD6'];
const isHex=c=>/^#[0-9a-f]{6}$/i.test(c||'');
const lum=h=>{const n=parseInt(h.slice(1),16),f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(n>>16)+.7152*f(n>>8&255)+.0722*f(n&255)};
const colOf=c=>isHex(c)?c:(P.m[c]||P.m.ink);            /* line colour */
const paperOf=c=>isHex(c)?c:(P.p[c]||P.p.amber);        /* sticky / shape fill */
const inkOn=c=>isHex(c)?(lum(c)<.32?'#ffffff':'#1b2327'):P.note; /* readable text on a note */
const textPx=s=>clamp(Math.round(11+2.4*s),14,96);      /* thickness 3/6/12 -> 18/26/40 like before */
const TYPES=['pen','rect','ellipse','tri','diamond','line','sticky','text'];
const HAND='"Shantell Sans","Readex Pro","Comic Sans MS","Segoe Print",cursive';
const ICON={
 select:'M5 3l14 7-6 2-2 6z',
 hand:'M8 12V5.5a1.5 1.5 0 013 0V11m0-6.5a1.5 1.5 0 013 0V11m0-5a1.5 1.5 0 013 0V15a6 6 0 01-6 6h-1a6 6 0 01-5-2.7L5 14a1.6 1.6 0 012.6-1.8L8 13',
 pen:'M4 20l1-4L16 5l3 3L8 19zM14 7l3 3',
 eraser:'M8 20h11M5.5 15.5l8-8a2 2 0 012.8 0l2.2 2.2a2 2 0 010 2.8L11 20H8l-2.5-2.5a1.4 1.4 0 010-2zM10 11l5 5',
 sticky:'M5 5h14v9l-5 5H5zM14 19v-5h5',
 text:'M6 6h12M12 6v13M9 19h6',
 rect:'M5 6h14v12H5z',ellipse:'M12 5a8 7 0 100 14 8 7 0 000-14z',tri:'M12 5l8 14H4z',diamond:'M12 4l8 8-8 8-8-8z',
 arrow:'M5 19L19 5M10 5h9v9',
 undo:'M8 6L3 11l5 5M3 11h11a5 5 0 010 10h-3',redo:'M16 6l5 5-5 5M21 11H10a5 5 0 000 10h3',
 export:'M12 4v11M7 10l5 5 5-5M5 20h14',globe:'M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18',share:'M12 15V4M8 8l4-4 4 4M5 13v6h14v-6',
 dup:'M8 8h11v11H8zM5 16V5h11',front:'M12 20V7M6 13l6-6 6 6M5 3h14',trash:'M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13'
};
const svg=n=>'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="'+ICON[n]+'"/></svg>';
$$('[data-i]').forEach(b=>b.insertAdjacentHTML('afterbegin',svg(b.dataset.i)));

const P={m:{},p:{},board:'#ffffff',accent:'#1f5fd1',note:'#1b2327',muted:'#666666',shadow:'rgba(0,0,0,.2)'};
const items=new Map(),sel=new Set(),pointers=new Map();
const view={x:0,y:0,k:1};
let W=1,H=1,sized=false,tool='pen',color=LS.get('fb:color','ink'),size=Math.max(1,Math.min(40,+LS.get('fb:size',6)||6)),shape='rect',g=null,pz=null,editing=null,spaceDown=false;
let undo=[],redo=[],index=[],board='',lastTap=null,raf=0,saveT=0,toastT=0;
let pro=LS.get('fb:pro',null);
const FREE=Math.max(1,+C.freeBoardLimit||3);
const uid=()=>'i'+Date.now().toString(36)+Math.random().toString(36).slice(2,8);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const font=px=>'500 '+px+'px '+HAND;
const isRtl=s=>/[֐-ࣿ]/.test(s||'');

function readTheme(){
  const cs=getComputedStyle(document.documentElement),v=n=>cs.getPropertyValue(n).trim();
  for(const k of KEYS){P.m[k]=v('--m-'+k);P.p[k]=v('--p-'+k)}
  P.board=v('--board');P.accent=v('--accent');P.note=v('--note-fg');P.muted=v('--muted');P.shadow=v('--shadow');
  dirty();
}
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',readTheme)}catch(e){}

/* ---------- text layout ---------- */
const wc=new Map();
function wrapLines(text,f,maxW){
  const key=f+'|'+Math.round(maxW)+'|'+text;let r=wc.get(key);if(r)return r;
  mctx.font=f;const M=s=>mctx.measureText(s).width;r=[];
  for(const para of String(text).split('\n')){
    let line='';
    for(const word of para.split(' ')){
      let t=line?line+' '+word:word;
      if(line&&M(t)>maxW){r.push(line);line='';t=word}
      if(M(t)>maxW){let cur='';for(const ch of t){if(cur&&M(cur+ch)>maxW){r.push(cur);cur=ch}else cur+=ch}line=cur}
      else line=t;
    }
    r.push(line);
  }
  if(wc.size>500)wc.clear();wc.set(key,r);return r;
}
function tl(it){
  const tx=it.tx||'';
  if(it.t==='sticky'){const tw=Math.max(20,it.w-24);let fs=11,lines=[];for(const s of [26,22,18,15,13,11]){fs=s;lines=wrapLines(tx,font(s),tw);if(lines.length*s*1.3<=it.h-20)break}return{fs,lines}}
  if(it.t==='text'){const fs=textPx(it.s||6);return{fs,lines:wrapLines(tx,font(fs),Math.max(20,it.w))}}
  return{fs:18,lines:wrapLines(tx,font(18),Math.max(20,it.w-20))};
}
function textH(it){const L=tl(it);return Math.round(L.lines.length*L.fs*1.3)}

/* ---------- geometry ---------- */
const ctr=it=>({x:it.x+it.w/2,y:it.y+it.h/2});
function clip(box,c,to){const dx=to.x-c.x,dy=to.y-c.y;if(!dx&&!dy)return c;const hw=box.w/2+6,hh=box.h/2+6;
  const t=Math.min(dx?hw/Math.abs(dx):Infinity,dy?hh/Math.abs(dy):Infinity,1);return{x:c.x+dx*t,y:c.y+dy*t}}
function ends(it){
  const A=it.a&&items.get(it.a),B=it.b&&items.get(it.b);
  const okA=A&&A.t!=='line'&&A.t!=='pen',okB=B&&B.t!=='line'&&B.t!=='pen';
  const pa=okA?ctr(A):{x:it.x,y:it.y},pb=okB?ctr(B):{x:it.x2,y:it.y2};
  return{a:okA?clip(A,pa,pb):pa,b:okB?clip(B,pb,pa):pb};
}
function bbox(it){
  if(it.t==='line'){const e=ends(it);const x=Math.min(e.a.x,e.b.x),y=Math.min(e.a.y,e.b.y);return{x,y,w:Math.abs(e.a.x-e.b.x),h:Math.abs(e.a.y-e.b.y)}}
  return{x:it.x,y:it.y,w:it.w||0,h:it.h||0};
}
function dseg(p,a,b){const dx=b.x-a.x,dy=b.y-a.y,l=dx*dx+dy*dy;let t=l?((p.x-a.x)*dx+(p.y-a.y)*dy)/l:0;t=clamp(t,0,1);return Math.hypot(p.x-a.x-t*dx,p.y-a.y-t*dy)}
function sorted(){return[...items.values()].sort((a,b)=>(a.z-b.z)||(a.id<b.id?-1:1))}
function hit(w,opt){
  const tol=10/view.k,L=sorted();
  for(let i=L.length-1;i>=0;i--){
    const it=L[i];
    if(opt&&opt.box&&(it.t==='line'||it.t==='pen'))continue;
    if(it.t==='pen'){
      const r=tol+(it.s||4)/2;
      if(w.x<it.x-r||w.y<it.y-r||w.x>it.x+it.w+r||w.y>it.y+it.h+r)continue;
      const p=it.p;if(p.length<4){if(Math.hypot(w.x-it.x-p[0],w.y-it.y-p[1])<=r)return it;continue}
      for(let j=0;j<p.length-2;j+=2)if(dseg(w,{x:it.x+p[j],y:it.y+p[j+1]},{x:it.x+p[j+2],y:it.y+p[j+3]})<=r)return it;
    }else if(it.t==='line'){const e=ends(it);if(dseg(w,e.a,e.b)<=tol+(it.s||4)/2)return it}
    else if(w.x>=it.x-4&&w.y>=it.y-4&&w.x<=it.x+it.w+4&&w.y<=it.y+it.h+4)return it;
  }
  return null;
}
function handles(){
  if(sel.size!==1)return[];const it=items.get([...sel][0]);if(!it||it.t==='pen')return[];
  if(it.t==='line'){const e=ends(it);return[{n:'p1',x:e.a.x,y:e.a.y},{n:'p2',x:e.b.x,y:e.b.y}]}
  return[{n:'se',x:it.x+it.w,y:it.y+it.h}];
}

/* ---------- drawing ---------- */
function shapePath(c,it){
  const x=it.x,y=it.y,w=it.w,h=it.h;c.beginPath();
  if(it.t==='rect'){if(c.roundRect)c.roundRect(x,y,w,h,6);else c.rect(x,y,w,h)}
  else if(it.t==='ellipse')c.ellipse(x+w/2,y+h/2,Math.abs(w/2),Math.abs(h/2),0,0,Math.PI*2);
  else if(it.t==='tri'){c.moveTo(x+w/2,y);c.lineTo(x+w,y+h);c.lineTo(x,y+h);c.closePath()}
  else{c.moveTo(x+w/2,y);c.lineTo(x+w,y+h/2);c.lineTo(x+w/2,y+h);c.lineTo(x,y+h/2);c.closePath()}
}
function penPath(c,x,y,p){
  c.beginPath();c.moveTo(x+p[0],y+p[1]);
  if(p.length<4){c.lineTo(x+p[0]+.01,y+p[1]);return}
  for(let i=2;i<p.length-2;i+=2)c.quadraticCurveTo(x+p[i],y+p[i+1],x+(p[i]+p[i+2])/2,y+(p[i+1]+p[i+3])/2);
  c.lineTo(x+p[p.length-2],y+p[p.length-1]);
}
function drawText(c,it,col,al){
  const L=tl(it),lh=L.fs*1.3,n=L.lines.length,rtl=isRtl(it.tx);
  c.font=font(L.fs);c.fillStyle=col;c.textBaseline='middle';c.direction=rtl?'rtl':'ltr';
  let x=it.x+it.w/2;c.textAlign='center';
  if(al==='left'){if(rtl){c.textAlign='right';x=it.x+it.w}else{c.textAlign='left';x=it.x}}
  let y=al==='left'?it.y+lh/2:it.y+it.h/2-(n-1)*lh/2;
  for(const s of L.lines){c.fillText(s,x,y);y+=lh}
  c.direction='ltr';
}
function drawItem(c,it,k){
  const col=colOf(it.c),pap=paperOf(it.c),hide=editing&&editing.id===it.id;
  c.lineCap='round';c.lineJoin='round';
  if(it.t==='pen'){c.strokeStyle=col;c.lineWidth=it.s||4;penPath(c,it.x,it.y,it.p);c.stroke();return}
  if(it.t==='line'){
    const e=ends(it);c.strokeStyle=col;c.fillStyle=col;c.lineWidth=it.s||4;
    c.beginPath();c.moveTo(e.a.x,e.a.y);c.lineTo(e.b.x,e.b.y);c.stroke();
    const an=Math.atan2(e.b.y-e.a.y,e.b.x-e.a.x),L=10+(it.s||4)*1.6;
    c.beginPath();c.moveTo(e.b.x,e.b.y);c.lineTo(e.b.x-L*Math.cos(an-.45),e.b.y-L*Math.sin(an-.45));c.lineTo(e.b.x-L*Math.cos(an+.45),e.b.y-L*Math.sin(an+.45));c.closePath();c.fill();c.stroke();return;
  }
  if(it.t==='sticky'){
    c.save();c.shadowColor=P.shadow;c.shadowBlur=12*k;c.shadowOffsetY=4*k;c.fillStyle=pap;c.fillRect(it.x,it.y,it.w,it.h);c.restore();
    if(!hide)drawText(c,it,inkOn(it.c),'center');return;
  }
  if(it.t==='text'){if(!hide)drawText(c,it,col,'left');return}
  shapePath(c,it);c.globalAlpha=.35;c.fillStyle=pap;c.fill();c.globalAlpha=1;c.strokeStyle=col;c.lineWidth=it.s||4;c.stroke();
  if(!hide&&it.tx)drawText(c,it,P.m.ink,'center');
}
function dirty(){if(!raf)raf=requestAnimationFrame(render)}
function render(){
  raf=0;const d=window.devicePixelRatio||1,k=view.k;
  ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,W,H);
  const gs=24*k*(k<.45?4:1);wrap.style.backgroundSize=gs+'px '+gs+'px';wrap.style.backgroundPosition=(view.x-gs/2)+'px '+(view.y-gs/2)+'px';
  ctx.save();ctx.translate(view.x,view.y);ctx.scale(k,k);
  const x0=-view.x/k,y0=-view.y/k,x1=x0+W/k,y1=y0+H/k;
  for(const it of sorted()){const b=bbox(it),m=30;if(b.x>x1+m||b.y>y1+m||b.x+b.w<x0-m||b.y+b.h<y0-m)continue;drawItem(ctx,it,k)}
  if(g&&g.k==='pen'){ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=colOf(color);ctx.lineWidth=size;penPath(ctx,0,0,g.pts);ctx.stroke()}
  if(g&&g.k==='make'&&g.it)drawItem(ctx,g.it,k);
  ctx.strokeStyle=P.accent;ctx.lineWidth=1.5/k;
  if(!editing)for(const id of sel){const it=items.get(id);if(!it)continue;const b=bbox(it),p=6/k;ctx.setLineDash([5/k,4/k]);ctx.strokeRect(b.x-p,b.y-p,b.w+2*p,b.h+2*p)}
  ctx.setLineDash([]);
  if(!editing&&tool==='select')for(const h of handles()){ctx.beginPath();ctx.arc(h.x,h.y,6/k,0,7);ctx.fillStyle=P.board;ctx.fill();ctx.stroke()}
  if(g&&g.k==='marquee'){ctx.globalAlpha=.12;ctx.fillStyle=P.accent;const r=mrect();ctx.fillRect(r.x,r.y,r.w,r.h);ctx.globalAlpha=1;ctx.strokeRect(r.x,r.y,r.w,r.h)}
  ctx.restore();
  if(!items.size&&!g){
    ctx.font=font(20);ctx.fillStyle=P.muted;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(tr('empty1'),W/2,H/2-14);ctx.font=font(15);ctx.fillText(tr('empty2'),W/2,H/2+16);
  }
  $('#zfit').textContent=Math.round(k*100)+'%';
  if(editing)placeEditor();
}
function mrect(){const a=g.start,b=g.cur;return{x:Math.min(a.x,b.x),y:Math.min(a.y,b.y),w:Math.abs(a.x-b.x),h:Math.abs(a.y-b.y)}}

/* ---------- view ---------- */
function resize(){
  const r=wrap.getBoundingClientRect(),d=window.devicePixelRatio||1;
  W=Math.max(1,r.width);H=Math.max(1,r.height);cv.width=Math.round(W*d);cv.height=Math.round(H*d);
  if(!sized){sized=true;fit()}
  proUi();dirty();
}
function zoomAt(px,py,f){const k=clamp(view.k*f,.1,5),wx=(px-view.x)/view.k,wy=(py-view.y)/view.k;view.k=k;view.x=px-wx*k;view.y=py-wy*k;dirty()}
function fit(){
  if(!items.size){view.k=1;view.x=W/2;view.y=H/2;dirty();return}
  let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;
  for(const it of items.values()){const b=bbox(it);x0=Math.min(x0,b.x);y0=Math.min(y0,b.y);x1=Math.max(x1,b.x+b.w);y1=Math.max(y1,b.y+b.h)}
  const k=clamp(Math.min(W/(x1-x0+80),H/(y1-y0+80)),.1,1.25);view.k=k;view.x=W/2-(x0+x1)/2*k;view.y=H/2-(y0+y1)/2*k;dirty();
}
const pos=e=>{const r=cv.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top}};
const toW=p=>({x:(p.x-view.x)/view.k,y:(p.y-view.y)/view.k});

/* ---------- boards and storage ---------- */
function closePops(keep){$$('.pop').forEach(p=>{if(p!==keep)p.hidden=true});const m=document.getElementById('langMenu');if(keep&&m&&!m.hidden){m.hidden=true;$('#lang').setAttribute('aria-expanded','false')}}
function toast(t){const el=$('#toast');el.textContent=t;el.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>{el.hidden=true},3600)}
function clean(d){
  if(!d||typeof d!=='object'||typeof d.id!=='string'||TYPES.indexOf(d.t)<0||!isFinite(d.x)||!isFinite(d.y))return null;
  if(d.t==='pen'&&(!Array.isArray(d.p)||d.p.length<2))return null;
  if(d.t==='line'&&(!isFinite(d.x2)||!isFinite(d.y2)))return null;
  const o=Object.assign({},d,{w:isFinite(d.w)?+d.w:0,h:isFinite(d.h)?+d.h:0,z:isFinite(d.z)?+d.z:0});
  if(o.tx!=null)o.tx=String(o.tx).slice(0,2000);
  if(KEYS.indexOf(o.c)<0&&!isHex(o.c))o.c='ink';
  o.s=clamp(+o.s||4,1,40);
  return o;
}
const meta=()=>index.find(b=>b.id===board);
function saveNow(){
  clearTimeout(saveT);saveT=0;if(!board)return;
  const ok=LS.set('fb:board:'+board,[...items.values()]);
  const m=meta();if(m)m.updated=Date.now();
  if(!ok||!LS.set('fb:boards',index))toast(tr('storageFull'));
}
function save(){clearTimeout(saveT);saveT=setTimeout(saveNow,300)}
function welcome(){
  const z=Date.now();
  return[
   {id:uid(),t:'text',x:-250,y:-236,w:720,h:52,c:'ink',s:12,tx:tr('wTitle'),z:z},
   {id:uid(),t:'pen',x:-250,y:-178,w:300,h:12,c:'red',s:3,p:[0,6,20,1,40,6,60,11,80,6,100,1,120,6,140,11,160,6,180,1,200,6,220,11,240,6,260,1,280,6,300,11],z:z+1},
   {id:uid(),t:'sticky',x:-250,y:-140,w:170,h:170,c:'amber',s:4,tx:tr('w1'),z:z+2},
   {id:uid(),t:'sticky',x:-50,y:-140,w:170,h:170,c:'green',s:4,tx:tr('w2'),z:z+3},
   {id:uid(),t:'sticky',x:150,y:-140,w:170,h:170,c:'violet',s:4,tx:tr('w3'),z:z+4}
  ];
}
function openBoard(id){
  if(saveT)saveNow();closeEditor();
  board=id;items.clear();sel.clear();undo=[];redo=[];g=null;
  for(const d of LS.get('fb:board:'+id,[])){const o=clean(d);if(o)items.set(o.id,o)}
  LS.set('fb:last',id);
  $('#bnameTxt').textContent=(meta()||{}).name||'';
  if(sized)fit();ui();dirty();
}
function newBoard(name,seed){
  const id='b'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
  index.push({id:id,name:name,updated:Date.now()});
  LS.set('fb:board:'+id,seed||[]);LS.set('fb:boards',index);
  return id;
}
function listBoards(){
  const ul=$('#blist');ul.textContent='';
  for(const b of index.slice().sort((a,c)=>c.updated-a.updated)){
    const li=document.createElement('li');if(b.id===board)li.className='cur';
    const o=document.createElement('button');o.className='open';o.textContent=b.name;o.addEventListener('click',()=>{openBoard(b.id);$('#boardsPop').hidden=true});
    const r=document.createElement('button');r.className='ib';r.innerHTML=svg('pen');r.title=tr('rename');r.setAttribute('aria-label',tr('rename'));
    r.addEventListener('click',()=>{const n=prompt(tr('renamePrompt'),b.name);if(n&&n.trim()){b.name=n.trim().slice(0,60);LS.set('fb:boards',index);if(b.id===board)$('#bnameTxt').textContent=b.name;listBoards()}});
    const d=document.createElement('button');d.className='ib';d.innerHTML=svg('trash');d.title=tr('del');d.setAttribute('aria-label',tr('del'));
    d.addEventListener('click',()=>{
      if(!confirm(tr('confirmDel',{name:b.name})))return;
      index=index.filter(x=>x.id!==b.id);LS.del('fb:board:'+b.id);LS.set('fb:boards',index);
      if(b.id===board){clearTimeout(saveT);saveT=0;board='';if(!index.length)newBoard(tr('untitled'));openBoard(index[0].id)}
      listBoards();
    });
    li.append(o,r,d);ul.appendChild(li);
  }
}
function download(blob,name){
  const a=document.createElement('a'),u=URL.createObjectURL(blob);a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),4000);
}
$('#bname').addEventListener('click',()=>{const p=$('#boardsPop');p.hidden=!p.hidden;closePops(p);if(!p.hidden)listBoards()});
$('#bnew').addEventListener('click',()=>{
  if(!pro&&index.length>=FREE){toast(tr('limit',{n:FREE}));openPro();return}
  const id=newBoard(tr('untitled'));openBoard(id);$('#boardsPop').hidden=true;
});
$('#bbackup').addEventListener('click',()=>{
  if(!pro){toast(tr('needPro'));openPro();return}
  if(saveT)saveNow();
  const out={app:'feltboard',v:1,boards:index.map(b=>({id:b.id,name:b.name,updated:b.updated,items:LS.get('fb:board:'+b.id,[])}))};
  download(new Blob([JSON.stringify(out)],{type:'application/json'}),'sitewhiteboard-backup.json');
});
$('#brestore').addEventListener('click',()=>{if(!pro){toast(tr('needPro'));openPro();return}$('#bfile').click()});
$('#bfile').addEventListener('change',async e=>{
  const f=e.target.files[0];e.target.value='';if(!f)return;
  try{
    const j=JSON.parse(await f.text());if(!j||j.app!=='feltboard'||!Array.isArray(j.boards))throw 0;
    let n=0;
    for(const b of j.boards){
      if(!b||!Array.isArray(b.items))continue;
      const its=b.items.map(clean).filter(Boolean);
      newBoard(String(b.name||tr('untitled')).slice(0,60),its);n++;
    }
    listBoards();toast(tr('restored',{n:n}));
  }catch(err){toast(tr('restoreBad'))}
});

/* ---------- Pro ---------- */
function proUi(){
  $('#pro').textContent=pro||innerWidth<560?tr('proOn'):tr('goPro');
  $('#proActive').hidden=!pro;$('#proOff').hidden=!pro;$('#keyBox').hidden=!!pro;
  const buy=$('#buy');buy.hidden=!!pro||!C.proCheckoutUrl;
  if(C.proCheckoutUrl){buy.href=C.proCheckoutUrl;buy.textContent=tr('buy')+(C.proPrice?' · '+C.proPrice:'')}
  $('#soon').hidden=!!pro||!!C.proCheckoutUrl;
}
function openPro(){$('#proPop').hidden=false;$('#keymsg').textContent='';proUi()}
async function checkKey(key){
  const r=await fetch(C.licenseValidateUrl,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/x-www-form-urlencoded'},body:'license_key='+encodeURIComponent(key)});
  const j=await r.json();return !!(j&&j.valid===true);
}
$('#pro').addEventListener('click',()=>{const p=$('#proPop');if(p.hidden){closePops();openPro()}else p.hidden=true});
$('#proClose').addEventListener('click',()=>{$('#proPop').hidden=true});
$('#proOff').addEventListener('click',()=>{pro=null;LS.del('fb:pro');proUi()});
$('#act').addEventListener('click',async()=>{
  const key=$('#key').value.trim(),msg=$('#keymsg');if(!key)return;
  if(!C.licenseValidateUrl){msg.textContent=tr('proSoon');return}
  $('#act').disabled=true;
  try{if(await checkKey(key)){pro={key:key,at:Date.now()};LS.set('fb:pro',pro);msg.textContent=tr('keyOk');proUi()}else msg.textContent=tr('keyBad')}
  catch(e){msg.textContent=tr('keyErr')}
  $('#act').disabled=false;
});
/* re-check a stored key once a week; drop it only when the provider says it is no longer valid */
if(pro&&pro.key&&C.licenseValidateUrl&&Date.now()-(pro.at||0)>6048e5){
  checkKey(pro.key).then(ok=>{if(ok){pro.at=Date.now();LS.set('fb:pro',pro)}else{pro=null;LS.del('fb:pro');proUi()}}).catch(()=>{});
}

/* ---------- edits and undo ---------- */
function applyMap(m){
  for(const id in m){const v=m[id];if(v)items.set(id,v);else{items.delete(id);sel.delete(id)}}
  save();ui();dirty();
}
function commit(before,after){undo.push({before,after});if(undo.length>200)undo.shift();redo=[];applyMap(after)}
function doUndo(){const op=undo.pop();if(!op)return;closeEditor();redo.push(op);applyMap(op.before)}
function doRedo(){const op=redo.pop();if(!op)return;closeEditor();undo.push(op);applyMap(op.after)}
function restyle(patch){
  const b={},a={};let n=0;
  for(const id of sel){const it=items.get(id);if(!it)continue;const o=Object.assign({},it,patch);if(o.t==='text')o.h=textH(o);b[id]=it;a[id]=o;n++}
  if(n)commit(b,a);
}
function delSel(){if(!sel.size)return;const b={},a={};for(const id of sel){const it=items.get(id);if(it){b[id]=it;a[id]=null}}commit(b,a)}
function dupSel(){
  if(!sel.size)return;const b={},a={},ids=[];let i=0;
  for(const id of [...sel]){const it=items.get(id);if(!it)continue;const o=Object.assign({},it,{id:uid(),x:it.x+24,y:it.y+24,z:Date.now()+(i++)});
    if(o.t==='line'){const e=ends(it);o.x=e.a.x+24;o.y=e.a.y+24;o.x2=e.b.x+24;o.y2=e.b.y+24;o.a='';o.b=''}
    b[o.id]=null;a[o.id]=o;ids.push(o.id)}
  commit(b,a);sel.clear();ids.forEach(x=>sel.add(x));ui();dirty();
}
function frontSel(){if(!sel.size)return;const b={},a={};let i=0;for(const it of sorted()){if(sel.has(it.id)){b[it.id]=it;a[it.id]=Object.assign({},it,{z:Date.now()+(i++)})}}commit(b,a)}

/* ---------- text editor ---------- */
function openEditor(it,isNew){editing={id:it.id,isNew:isNew};ed.value=it.tx||'';ed.hidden=false;placeEditor();ed.focus();try{ed.setSelectionRange(ed.value.length,ed.value.length)}catch(e){}ui();dirty()}
function placeEditor(){
  const it=items.get(editing.id);if(!it)return;const k=view.k,L=tl(Object.assign({},it,{tx:ed.value})),pad=it.t==='text'?0:it.t==='sticky'?12:10;
  const h=Math.max(it.h,L.lines.length*L.fs*1.3+pad*2);
  ed.style.left=(it.x*k+view.x)+'px';ed.style.top=(it.y*k+view.y)+'px';ed.style.width=Math.max(40,it.w*k)+'px';ed.style.height=Math.max(24,h*k)+'px';
  ed.style.fontSize=(L.fs*k)+'px';ed.style.padding=(pad*k)+'px';ed.style.textAlign=it.t==='text'?'start':'center';
  ed.style.color=it.t==='sticky'?inkOn(it.c):it.t==='text'?colOf(it.c):P.m.ink;
}
function closeEditor(){
  if(!editing)return;const e=editing;editing=null;ed.hidden=true;
  const it=items.get(e.id);if(!it){ui();dirty();return}
  const tx=ed.value.replace(/\s+$/,'').slice(0,2000),id=it.id;
  if(e.isNew){
    items.delete(id);
    if(it.t==='text'&&!tx){sel.delete(id)}
    else{const n=Object.assign({},it,{tx:tx});if(n.t==='text')n.h=textH(n);commit({[id]:null},{[id]:n})}
  }else if(tx!==(it.tx||'')){
    const n=Object.assign({},it,{tx:tx});if(n.t==='text')n.h=Math.max(10,textH(n));
    if(n.t==='text'&&!tx)commit({[id]:it},{[id]:null});else commit({[id]:it},{[id]:n});
  }
  ui();dirty();
}
ed.addEventListener('input',()=>{if(editing)placeEditor()});
ed.addEventListener('blur',()=>setTimeout(closeEditor,0));
ed.addEventListener('keydown',e=>{if(e.key==='Escape'||(e.key==='Enter'&&(e.ctrlKey||e.metaKey))){e.preventDefault();closeEditor()}e.stopPropagation()});

/* ---------- pointer gestures ---------- */
function cancelGesture(){
  if(!g)return;
  if(g.orig)for(const [id,it] of g.orig)items.set(id,it);
  if(g.del)for(const [id,it] of g.del)items.set(id,it);
  g=null;dirty();
}
function pinchStart(){const a=[...pointers.values()];pz={d:Math.max(10,Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y)),cx:(a[0].x+a[1].x)/2,cy:(a[0].y+a[1].y)/2,k:view.k,x:view.x,y:view.y}}
function pinchMove(){
  const a=[...pointers.values()];if(a.length<2||!pz)return;
  const d=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),cx=(a[0].x+a[1].x)/2,cy=(a[0].y+a[1].y)/2;
  const k=clamp(pz.k*d/pz.d,.1,5),wx=(pz.cx-pz.x)/pz.k,wy=(pz.cy-pz.y)/pz.k;view.k=k;view.x=cx-wx*k;view.y=cy-wy*k;dirty();
}
function eraseAt(w){const it=hit(w);if(it){g.del.set(it.id,it);items.delete(it.id);sel.delete(it.id);dirty()}}

cv.addEventListener('pointerdown',e=>{
  if(e.button===2)return;
  /* a tap that closes an open menu only closes it: it does not also draw */
  const menuOpen=[...$$('.pop'),$('#palPop'),$('#langMenu')].some(m=>m&&!m.hidden);
  if(menuOpen&&!editing){closePops();showPal(false);showLangMenu(false);return}
  const p=pos(e);pointers.set(e.pointerId,p);try{cv.setPointerCapture(e.pointerId)}catch(_){}
  if(pointers.size===2){cancelGesture();pinchStart();return}
  if(pointers.size>2)return;
  if(editing){closeEditor();return}
  const w=toW(p),tl_=(spaceDown||e.button===1)?'hand':tool;
  if(tl_==='hand'){g={k:'pan',sx:p.x,sy:p.y,ox:view.x,oy:view.y};return}
  if(tl_==='select'){
    const hr=(e.pointerType==='touch'?18:10)/view.k;
    const hd=handles().find(h=>Math.hypot(h.x-w.x,h.y-w.y)<=hr);
    if(hd){const it=items.get([...sel][0]);g={k:'handle',n:hd.n,start:w,orig:new Map([[it.id,it]]),moved:false};return}
    const it=hit(w);
    if(it){
      if(!sel.has(it.id)){if(!e.shiftKey)sel.clear();sel.add(it.id)}else if(e.shiftKey)sel.delete(it.id);
      const orig=new Map();for(const id of sel){const o=items.get(id);if(o)orig.set(id,o)}
      g={k:'move',start:w,sp:p,orig:orig,moved:false,hitId:it.id};
    }else{if(!e.shiftKey)sel.clear();g={k:'marquee',start:w,cur:w,sp:p}}
    ui();dirty();return;
  }
  if(tl_==='pen'){g={k:'pen',pts:[w.x,w.y]};dirty();return}
  if(tl_==='eraser'){g={k:'erase',del:new Map()};eraseAt(w);return}
  if(tl_==='shape'){g={k:'make',start:w,it:null,kind:shape};return}
  if(tl_==='arrow'){const a=hit(w,{box:true});g={k:'make',start:w,kind:'line',it:null,a:a?a.id:''};return}
  if(tl_==='sticky'||tl_==='text'){g={k:'place',kind:tl_,start:w};return}
});
cv.addEventListener('pointermove',e=>{
  const p=pos(e);if(pointers.has(e.pointerId))pointers.set(e.pointerId,p);
  if(pointers.size>=2){pinchMove();return}
  if(!g)return;
  const w=toW(p);
  if(g.k==='pan'){view.x=g.ox+p.x-g.sx;view.y=g.oy+p.y-g.sy;dirty();return}
  if(g.k==='pen'){const n=g.pts.length;if(Math.hypot(w.x-g.pts[n-2],w.y-g.pts[n-1])>=1.5/view.k){g.pts.push(w.x,w.y);dirty()}return}
  if(g.k==='erase'){eraseAt(w);return}
  if(g.k==='marquee'){g.cur=w;dirty();return}
  const dx=w.x-g.start.x,dy=w.y-g.start.y;
  if(g.k==='move'){
    if(!g.moved){if(Math.hypot(p.x-g.sp.x,p.y-g.sp.y)<5)return;g.moved=true}
    for(const [id,o] of g.orig){
      if(o.t!=='line'){items.set(id,Object.assign({},o,{x:o.x+dx,y:o.y+dy}));continue}
      const both=(o.a||o.b)&&(!o.a||g.orig.has(o.a))&&(!o.b||g.orig.has(o.b))&&g.orig.size>1;
      if(both)items.set(id,Object.assign({},o,{x:o.x+dx,y:o.y+dy,x2:o.x2+dx,y2:o.y2+dy}));
      else{const en=ends(o);items.set(id,Object.assign({},o,{x:en.a.x+dx,y:en.a.y+dy,x2:en.b.x+dx,y2:en.b.y+dy,a:'',b:''}))}
    }
    dirty();return;
  }
  if(g.k==='handle'){
    g.moved=true;const o=[...g.orig.values()][0];let n;
    if(g.n==='se'){const min=o.t==='sticky'?80:24;n=Object.assign({},o,{w:Math.max(min,o.w+dx),h:Math.max(min,o.h+dy)});if(o.t==='text'){n.w=Math.max(60,o.w+dx);n.h=textH(n)}}
    else{const en=ends(o),t=hit(w,{box:true});n=Object.assign({},o,{x:en.a.x,y:en.a.y,x2:en.b.x,y2:en.b.y});
      if(g.n==='p1'){n.x=w.x;n.y=w.y;n.a=t&&t.id!==o.b?t.id:''}else{n.x2=w.x;n.y2=w.y;n.b=t&&t.id!==o.a?t.id:''}}
    items.set(o.id,n);dirty();return;
  }
  if(g.k==='make'){
    if(g.kind==='line')g.it={id:'tmp',t:'line',x:g.start.x,y:g.start.y,x2:w.x,y2:w.y,a:g.a,b:'',c:color,s:size,z:Date.now()};
    else g.it={id:'tmp',t:g.kind,x:Math.min(g.start.x,w.x),y:Math.min(g.start.y,w.y),w:Math.abs(dx),h:Math.abs(dy),c:color,s:size,z:Date.now()};
    dirty();
  }
});
function isDouble(p){const n=Date.now(),d=lastTap&&n-lastTap.t<380&&Math.hypot(p.x-lastTap.x,p.y-lastTap.y)<28;lastTap=d?null:{t:n,x:p.x,y:p.y};return d}
/* dark or white picks make poor notes: fall back to yellow */
function noteColor(){const c=colOf(color);return isHex(color)&&lum(c)>.08&&lum(c)<.97?color:color!=='ink'&&!isHex(color)?color:'#FFF4A8'}
function newNote(w){return{id:uid(),t:'sticky',x:Math.round(w.x-85),y:Math.round(w.y-85),w:170,h:170,c:noteColor(),s:4,tx:'',z:Date.now()}}
function endPointer(e,cancelled){
  const had=pointers.has(e.pointerId);pointers.delete(e.pointerId);
  if(pz){if(pointers.size<2)pz=null;if(pointers.size===0)g=null;return}
  if(!had||!g)return;
  if(cancelled){cancelGesture();return}
  const p=pos(e),w=toW(p),gg=g;g=null;
  if(gg.k==='pen'){
    const pts=gg.pts;let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;
    for(let i=0;i<pts.length;i+=2){x0=Math.min(x0,pts[i]);y0=Math.min(y0,pts[i+1]);x1=Math.max(x1,pts[i]);y1=Math.max(y1,pts[i+1])}
    x0=Math.floor(x0);y0=Math.floor(y0);const rel=[];for(let i=0;i<pts.length;i+=2)rel.push(Math.round((pts[i]-x0)*10)/10,Math.round((pts[i+1]-y0)*10)/10);
    const it={id:uid(),t:'pen',x:x0,y:y0,w:Math.ceil(x1-x0),h:Math.ceil(y1-y0),p:rel,c:color,s:size,z:Date.now()};
    commit({[it.id]:null},{[it.id]:it});return;
  }
  if(gg.k==='erase'){if(gg.del.size){const b={},a={};for(const [id,it] of gg.del){b[id]=it;a[id]=null}commit(b,a)}return}
  if(gg.k==='move'){
    if(gg.moved){const b={},a={};for(const [id,o] of gg.orig){b[id]=o;a[id]=items.get(id)}commit(b,a)}
    else if(isDouble(p)){const it=items.get(gg.hitId);if(it&&it.t!=='pen'&&it.t!=='line'){sel.clear();sel.add(it.id);openEditor(it,false)}}
    return;
  }
  if(gg.k==='handle'){if(gg.moved){const o=[...gg.orig.values()][0];commit({[o.id]:o},{[o.id]:items.get(o.id)})}return}
  if(gg.k==='marquee'){
    const r={x:Math.min(gg.start.x,w.x),y:Math.min(gg.start.y,w.y),w:Math.abs(gg.start.x-w.x),h:Math.abs(gg.start.y-w.y)};
    if(Math.hypot(p.x-gg.sp.x,p.y-gg.sp.y)<6){
      if(isDouble(p)){const it=newNote(w);items.set(it.id,it);sel.clear();sel.add(it.id);openEditor(it,true)}
    }else for(const it of items.values()){const b=bbox(it);if(b.x<r.x+r.w&&b.x+b.w>r.x&&b.y<r.y+r.h&&b.y+b.h>r.y)sel.add(it.id)}
    ui();dirty();return;
  }
  if(gg.k==='make'){
    let it=gg.it;
    if(gg.kind==='line'){
      if(!it||Math.hypot(it.x2-it.x,it.y2-it.y)<8/view.k){dirty();return}
      const t=hit(w,{box:true});it=Object.assign({},it,{id:uid(),x:Math.round(it.x),y:Math.round(it.y),x2:Math.round(it.x2),y2:Math.round(it.y2),b:t&&t.id!==it.a?t.id:''});
    }else{
      if(!it||it.w<8||it.h<8)it={t:gg.kind,x:gg.start.x-70,y:gg.start.y-50,w:140,h:100,c:color,s:size,z:Date.now()};
      it=Object.assign({},it,{id:uid(),x:Math.round(it.x),y:Math.round(it.y),w:Math.round(it.w),h:Math.round(it.h)});
    }
    commit({[it.id]:null},{[it.id]:it});sel.clear();sel.add(it.id);setTool('select');return;
  }
  if(gg.k==='place'){
    const it=gg.kind==='sticky'?newNote(w)
      :{id:uid(),t:'text',x:Math.round(w.x),y:Math.round(w.y-textPx(size)*.65),w:260,h:Math.round(textPx(size)*1.3),c:color,s:size,tx:'',z:Date.now()};
    items.set(it.id,it);sel.clear();sel.add(it.id);setTool('select');openEditor(it,true);
  }
}
cv.addEventListener('pointerup',e=>endPointer(e,false));
cv.addEventListener('pointercancel',e=>endPointer(e,true));
cv.addEventListener('contextmenu',e=>e.preventDefault());
cv.addEventListener('wheel',e=>{
  e.preventDefault();const p=pos(e);
  if(e.ctrlKey||e.metaKey)zoomAt(p.x,p.y,Math.exp(-e.deltaY*.01));
  else if(e.deltaMode===1)zoomAt(p.x,p.y,Math.exp(-e.deltaY*.05));
  else if(!e.deltaX&&Math.abs(e.deltaY)>=100&&(Math.abs(e.deltaY)%100===0||Math.abs(e.deltaY)%120===0))zoomAt(p.x,p.y,Math.exp(-e.deltaY*.0015));
  else{view.x-=e.deltaX;view.y-=e.deltaY;dirty()}
},{passive:false});

/* ---------- chrome ---------- */
function setTool(t){if(editing)closeEditor();tool=t;if(t!=='select')sel.clear();ui();dirty()}
function ui(){
  $$('[data-tool]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tool===tool)));
  paletteUi();
  $$('[data-kind]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind===shape)));
  $('#kinds').hidden=tool!=='shape';
  $('#undo').disabled=!undo.length;$('#redo').disabled=!redo.length;
  $('#selbar').hidden=!sel.size||!!editing||tool!=='select';
  cv.style.cursor=cursorFor(tool);
}
/* each tool has its own pointer: a pencil in the current colour, an eraser ring, a note, a hand */
function cursorFor(t){
  const u=(s,x,y,fb)=>'url("data:image/svg+xml,'+encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24'>"+s+'</svg>')+'") '+x+' '+y+', '+fb;
  const c=colOf(color);
  if(t==='pen')return u("<path d='M3 21l1.2-4.6L16.5 4.1a1.5 1.5 0 012.1 0l1.3 1.3a1.5 1.5 0 010 2.1L7.6 19.8z' fill='"+c+"' stroke='#fff' stroke-width='1.4' stroke-linejoin='round'/><path d='M3 21l1.2-4.6 3.4 3.4z' fill='#1b2327' stroke='#fff' stroke-width='.6' stroke-linejoin='round'/>",4,24,'crosshair');
  if(t==='eraser')return u("<circle cx='12' cy='12' r='8.5' fill='rgba(255,255,255,.7)' stroke='#1b2327' stroke-width='1.4'/>",14,14,'cell');
  if(t==='sticky')return u("<path d='M8 8h13v9l-4 4H8z' fill='"+paperOf(noteColor())+"' stroke='#1b2327' stroke-width='1.2' stroke-linejoin='round'/><path d='M1 4h6M4 1v6' stroke='#1b2327' stroke-width='1.4'/>",5,5,'copy');
  return t==='hand'?(g&&g.k==='pan'?'grabbing':'grab'):t==='select'?'default':t==='text'?'text':'crosshair';
}
$$('[data-tool]').forEach(b=>b.addEventListener('click',()=>setTool(b.dataset.tool)));
$$('[data-kind]').forEach(b=>b.addEventListener('click',()=>{shape=b.dataset.kind;$('#shapeBtn').innerHTML=svg(shape);ui()}));
/* ---------- colour and thickness palette ---------- */
let recent=LS.get('fb:recent',[]),custom=LS.get('fb:custom',[]);
if(!Array.isArray(recent))recent=[];if(!Array.isArray(custom))custom=[];
recent=recent.filter(isHex).slice(0,3);custom=custom.filter(isHex).slice(0,10);
const palPop=$('#palPop'),sizeIn=$('#sizeIn');
function pickColor(c){
  color=c;LS.set('fb:color',c);
  if(isHex(c)){recent=[c].concat(recent.filter(x=>x.toLowerCase()!==c.toLowerCase())).slice(0,3);LS.set('fb:recent',recent)}
  if(sel.size)restyle({c:color});
  if(tool==='eraser'||tool==='hand'||tool==='select')setTool(sel.size?'select':'pen');
  ui();
}
function swatch(c,extra){
  const b=document.createElement('button');b.style.background=c;b.title=c;b.setAttribute('aria-label',c);b.setAttribute('role','option');
  b.style.setProperty('--chk',lum(c)>.6?'#1b2327':'#ffffff');if(extra)b.className=extra;
  b.addEventListener('click',()=>pickColor(c));return b;
}
function paletteUi(){
  const c=colOf(color),cur=(isHex(color)?color:'').toLowerCase();
  sizeIn.value=size;$('#sizeOut').textContent=size;
  /* the marker caps: the 6 classic colours + the last colours picked from the palette */
  const caps=$('#caps');caps.textContent='';
  const extra=recent.filter(x=>isHex(x)).slice(0,3);
  for(const k of KEYS.concat(extra)){
    const b=document.createElement('button');b.className='cap';b.style.background=colOf(k);
    const name=isHex(k)?k:tr('c'+{ink:'Ink',blue:'Blue',red:'Red',green:'Green',amber:'Amber',violet:'Violet'}[k]);
    b.title=name;b.setAttribute('aria-label',name);
    b.setAttribute('aria-pressed',String((isHex(k)?k.toLowerCase():k)===(isHex(color)?color.toLowerCase():color)));
    b.addEventListener('click',()=>pickColor(k));caps.appendChild(b);
  }
  const s=$('#swatches');s.textContent='';
  const all=PALETTE.concat(custom.filter(x=>PALETTE.indexOf(x.toUpperCase())<0));
  for(const x of all){const b=swatch(x);b.setAttribute('aria-selected',String(x.toLowerCase()===cur));s.appendChild(b)}
  const add=document.createElement('button');add.className='add';add.textContent='+';add.title=tr('custom');add.setAttribute('aria-label',tr('custom'));
  add.addEventListener('click',()=>{const p=$('#pickIn');p.value=isHex(color)?color:'#1a1a1a';p.click()});s.appendChild(add);
}
$('#pickIn').addEventListener('change',e=>{const c=e.target.value.toUpperCase();if(!isHex(c))return;if(PALETTE.indexOf(c)<0){custom=[c].concat(custom.filter(x=>x!==c)).slice(0,10);LS.set('fb:custom',custom)}pickColor(c)});
function showPal(open){palPop.hidden=!open;$('#qsColor').setAttribute('aria-expanded',String(open));if(open){paletteUi()}}
$('#qsColor').addEventListener('click',e=>{e.stopPropagation();showPal(palPop.hidden)});
palPop.addEventListener('click',e=>e.stopPropagation());
sizeIn.addEventListener('input',()=>{size=+sizeIn.value;LS.set('fb:size',size);paletteUi()});
sizeIn.addEventListener('change',()=>{if(sel.size)restyle({s:size})});
document.addEventListener('click',()=>{if(!palPop.hidden)showPal(false)});

$('#undo').addEventListener('click',doUndo);$('#redo').addEventListener('click',doRedo);
$('#dup').addEventListener('click',dupSel);$('#front').addEventListener('click',frontSel);$('#del').addEventListener('click',delSel);
$('#zin').addEventListener('click',()=>zoomAt(W/2,H/2,1.25));$('#zout').addEventListener('click',()=>zoomAt(W/2,H/2,.8));$('#zfit').addEventListener('click',fit);
const langMenu=$('#langMenu');
$$('#langMenu button').forEach(b=>b.insertAdjacentHTML('afterbegin','<i class="flag" aria-hidden="true">'+FLAG[b.dataset.l]+'</i>'));
function showLangMenu(open){langMenu.hidden=!open;$('#lang').setAttribute('aria-expanded',String(open));if(open)closePops()}
$('#lang').addEventListener('click',e=>{e.stopPropagation();showLangMenu(langMenu.hidden)});
$$('#langMenu button').forEach(b=>b.addEventListener('click',()=>{
  showLangMenu(false);if(b.dataset.l===lang)return;
  lang=b.dataset.l;LS.set('fb:lang',lang);try{history.replaceState(null,'',boardPath(lang))}catch(e){}applyLang();dirty();
}));
document.addEventListener('click',e=>{if(!langMenu.hidden&&!e.target.closest('.langdd'))showLangMenu(false)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!langMenu.hidden){showLangMenu(false);$('#lang').focus()}});
window.addEventListener('pagehide',()=>{if(saveT)saveNow()});
window.addEventListener('keydown',e=>{
  if(editing||/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName))return;
  if(e.code==='Space'){spaceDown=true;e.preventDefault();return}
  const mod=e.ctrlKey||e.metaKey,k=e.key.toLowerCase();
  if(mod&&k==='z'){e.preventDefault();if(e.shiftKey)doRedo();else doUndo();return}
  if(mod&&k==='y'){e.preventDefault();doRedo();return}
  if(mod&&k==='d'){e.preventDefault();dupSel();return}
  if(mod&&k==='a'){e.preventDefault();setTool('select');for(const id of items.keys())sel.add(id);ui();dirty();return}
  if(mod)return;
  if(k==='delete'||k==='backspace'){e.preventDefault();delSel();return}
  if(k==='escape'){sel.clear();closePops();ui();dirty();return}
  const map={v:'select',h:'hand',p:'pen',e:'eraser',n:'sticky',t:'text',s:'shape',l:'arrow'};
  if(map[k])setTool(map[k]);
});
window.addEventListener('keyup',e=>{if(e.code==='Space')spaceDown=false});

/* ---------- export ---------- */
function exportBlob(cb){
  closeEditor();
  if(!items.size){toast(tr('nothing'));return}
  let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;
  for(const it of items.values()){const b=bbox(it),m=(it.s||0)+4;x0=Math.min(x0,b.x-m);y0=Math.min(y0,b.y-m);x1=Math.max(x1,b.x+b.w+m);y1=Math.max(y1,b.y+b.h+m)}
  x0-=40;y0-=40;x1+=40;y1+=40;
  const sc=Math.min(pro?2:1,4096/Math.max(x1-x0,y1-y0)),c=document.createElement('canvas');
  c.width=Math.max(1,Math.round((x1-x0)*sc));c.height=Math.max(1,Math.round((y1-y0)*sc));
  const x=c.getContext('2d');x.fillStyle=P.board;x.fillRect(0,0,c.width,c.height);x.scale(sc,sc);x.translate(-x0,-y0);
  for(const it of sorted())drawItem(x,it,sc);
  if(!pro){x.font=font(13);x.fillStyle=P.muted;x.textAlign='right';x.textBaseline='alphabetic';x.fillText(tr('wm'),x1-12,y1-12)}
  c.toBlob(blob=>{if(blob)cb(blob)},'image/png');
}
const savePng=()=>exportBlob(b=>{download(b,'sitewhiteboard.png');toast(tr('exported'))});
$('#export').addEventListener('click',savePng);

/* ---------- share and user menu ---------- */
function togglePop(id){const p=$(id);p.hidden=!p.hidden;closePops(p)}
$('#share').addEventListener('click',()=>togglePop('#sharePop'));
$('#user').addEventListener('click',()=>togglePop('#userPop'));
$('#shDl').addEventListener('click',()=>{savePng();closePops()});
$('#shImg').addEventListener('click',()=>exportBlob(async b=>{
  closePops();
  const f=new File([b],'sitewhiteboard.png',{type:'image/png'});
  try{if(navigator.canShare&&navigator.canShare({files:[f]})){await navigator.share({files:[f],title:(meta()||{}).name||'SiteWhiteboard'});return}}
  catch(e){if(e&&e.name==='AbortError')return}
  try{await navigator.clipboard.write([new ClipboardItem({'image/png':b})]);toast(tr('copied'))}
  catch(e){download(b,'sitewhiteboard.png');toast(tr('exported'))}
}));
$('#meName').addEventListener('click',()=>{const n=prompt(tr('namePrompt'),me);if(n==null)return;me=n.trim().slice(0,40);LS.set('fb:user',me);applyLang()});
const gridT=$('#gridT');gridT.checked=LS.get('fb:grid',true)!==false;
const applyGrid=()=>wrap.classList.toggle('nogrid',!gridT.checked);
gridT.addEventListener('change',()=>{LS.set('fb:grid',gridT.checked);applyGrid()});applyGrid();

/* ---------- start ---------- */
applyLang();readTheme();
index=LS.get('fb:boards',[]);if(!Array.isArray(index))index=[];
index=index.filter(b=>b&&typeof b.id==='string');
if(!index.length)newBoard(tr('firstBoard'),welcome());
const want=location.hash.slice(1)||LS.get('fb:last','');
try{if(location.search||location.hash||location.pathname!==boardPath(lang))history.replaceState(null,'',boardPath(lang))}catch(e){}
openBoard(index.some(b=>b.id===want)?want:index[0].id);
new ResizeObserver(resize).observe(wrap);resize();
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>{wc.clear();dirty()});
})();
