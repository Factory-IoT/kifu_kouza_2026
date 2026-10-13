/* No external resources: lecture images, script and styles work offline. */
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rich=s=>esc(s).replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>');
let current=0,elapsed=0,start=0,running=false;
const query=new URLSearchParams(location.search);
const session=query.get('session')||'lecture';
const isPreview=query.get('preview')==='1';
const channel=isPreview?{postMessage(){}}:new BroadcastChannel('kifu-kouza-'+session);
let receiving=false;
function publish(){if(!receiving)channel.postMessage({type:'state',current,elapsed,start,running});}
channel.onmessage=e=>{const m=e.data;if(m.type==='request')publish();if(m.type==='navigate')show(m.current);if(m.type==='timer')$(m.action==='reset'?'reset':'timer').click();if(m.type==='state'){receiving=true;elapsed=m.elapsed;start=m.start;running=m.running;show(m.current);updateTimer();receiving=false;}};
if(query.get('audience')==='1')document.body.classList.add('presenting');
window.addEventListener('message',e=>{if(isPreview&&e.origin===location.origin&&e.data?.type==='preview')show(e.data.current);});
let cumulative=0; slides.forEach(s=>{s.start=cumulative;cumulative+=s.minutes;s.end=cumulative;});
const clock=m=>`${String(16+Math.floor(m/60)).padStart(2,'0')}:${String(m%60).padStart(2,'0')}`;
function markup(s,i){
 const figure=s.image?`<figure class="visual"><img src="assets/${esc(s.image)}" alt="${esc(s.alt||s.title)}"><figcaption>${esc(s.credit||'')}</figcaption></figure>`:'';
 const table=s.rows?`<table class="timeline"><thead><tr><th>時間</th><th>内容</th><th>担当</th></tr></thead><tbody>${s.rows.map(r=>`<tr>${r.map(c=>`<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>`:'';
 const body=s.statement?`<div class="statement">${rich(s.statement)}</div>`:`<div class="content"><div class="copy">${s.lead?`<p class="lead">${rich(s.lead)}</p>`:''}${s.points?`<ul class="body">${s.points.map((p,k)=>`<li${s.focus==null?'':k===s.focus?' class="focus"':' class="dim"'}>${rich(p)}</li>`).join('')}</ul>`:''}${table}${s.caption?`<p class="caption">${rich(s.caption)}</p>`:''}</div>${figure}</div>`;
 return `<p class="eyebrow">${esc(s.section)} · ${esc(s.presenter)}</p><${s.cover?'h1':'h2'}>${rich(s.title)}</${s.cover?'h1':'h2'}>${body}<footer class="footer"><span>技術者と社会 / みのる化成 / 2026.11.16</span><span>${clock(s.start)}–${clock(s.end)} · ${s.minutes}分</span><span class="page">${String(i+1).padStart(2,'0')} / ${slides.length}</span></footer>`;
}
function resize(){const r=$('stage').getBoundingClientRect();$('slide').style.transform=`scale(${Math.min(r.width/1600,r.height/900)})`;}
function show(i){current=Math.max(0,Math.min(slides.length-1,i));const s=slides[current];$('slide').className=`slide ${s.theme||''} ${s.image?(s.wide?'wide':'photo'):''}`;$('slide').innerHTML=markup(s,current);$('counter').textContent=`${current+1} / ${slides.length}`;$('prev').disabled=current===0;$('next').disabled=current===slides.length-1;history.replaceState(null,'',`#${current+1}`);document.title=`${current+1}. ${s.title.replace(/\n/g,' ')}｜技術者と社会`;$('note-body').innerHTML=`<p class="schedule">${esc(s.presenter)} / ${clock(s.start)}〜${clock(s.end)}（目安${s.minutes}分）</p><h3>${esc(s.title)}</h3><p>${rich(s.notes)}</p><h3>出典・画像</h3><ul>${(s.sources||['講義レジュメ（2026年度・案）']).map(x=>`<li>${x.startsWith('https://')?`<a href="${esc(x)}" target="_blank" rel="noopener">${esc(x)}</a>`:esc(x)}</li>`).join('')}${s.image?`<li>${esc(s.credit)}<br>画像の詳細は <a href="assets-manifest.json" target="_blank">素材一覧</a> に記録。</li>`:''}</ul>`;resize();}
const localShow=show;show=function(i){localShow(i);publish();};
$('prev').onclick=()=>show(current-1);$('next').onclick=()=>show(current+1);
$('presenter').onclick=()=>{const w=window.open(`presenter.html?session=${encodeURIComponent(session)}#${current+1}`,'kifu-presenter','popup,width=1250,height=900');if(w){document.body.classList.add('presenting');resize();setTimeout(publish,500);}else{$('presenter').textContent='ポップアップを許可してください';}};
window.addEventListener('keydown',e=>{if(e.key==='Escape'){document.body.classList.remove('presenting');resize();}});
let wheelAt=0;window.addEventListener('wheel',e=>{if(document.querySelector('dialog[open]')||e.ctrlKey||Math.abs(e.deltaY)<20)return;e.preventDefault();if(Date.now()-wheelAt<650)return;wheelAt=Date.now();show(current+(e.deltaY>0?1:-1));},{passive:false});
$('overview').onclick=()=>{$('slide-list').innerHTML=slides.map((s,i)=>`<button data-slide="${i}" class="${i===current?'current':''}">${String(i+1).padStart(2,'0')} ${esc(s.title.replace(/\n/g,' '))}<span>${esc(s.section)} · ${clock(s.start)}–${clock(s.end)}</span></button>`).join('');$('menu').showModal();};
$('slide-list').onclick=e=>{const b=e.target.closest('[data-slide]');if(b){show(Number(b.dataset.slide));$('menu').close();}};
$('notes').onclick=()=>$('note-panel').showModal();document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>b.closest('dialog').close());
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{$('fullscreen').textContent='ブラウザのF11で全画面';}};
function updateTimer(){const t=Math.floor((elapsed+(running?Date.now()-start:0))/1000);$('timer').textContent=`${running?'経過':t?'再開':'開始'} ${String(Math.floor(t/60)).padStart(2,'0')}:${String(t%60).padStart(2,'0')}`;$('timer').classList.toggle('running',running);}
$('timer').onclick=()=>{if(running)elapsed+=Date.now()-start;else start=Date.now();running=!running;updateTimer();publish();};$('reset').onclick=()=>{elapsed=0;running=false;updateTimer();publish();};setInterval(updateTimer,1000);
window.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]'))return;if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1);}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1);}if(e.key==='Home'){e.preventDefault();show(0);}if(e.key==='End'){e.preventDefault();show(slides.length-1);}if(e.key.toLowerCase()==='n')$('notes').click();if(e.key.toLowerCase()==='o')$('overview').click();if(e.key.toLowerCase()==='f')$('fullscreen').click();});
window.addEventListener('resize',resize);window.addEventListener('hashchange',()=>show((Number(location.hash.slice(1))||1)-1));
window.addEventListener('beforeprint',()=>{window.printBackup=$('stage').innerHTML;$('stage').innerHTML=slides.map((s,i)=>`<article class="slide ${s.theme||''} ${s.image?(s.wide?'wide':'photo'):''}">${markup(s,i)}</article>`).join('');});window.addEventListener('afterprint',()=>{$('stage').innerHTML=window.printBackup;show(current);});
show((Number(location.hash.slice(1))||1)-1);
channel.postMessage({type:'request'});
