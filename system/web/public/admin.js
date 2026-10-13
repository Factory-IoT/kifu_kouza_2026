const escapeText=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const time=m=>`${String(16+Math.floor(m/60)).padStart(2,'0')}:${String(m%60).padStart(2,'0')}`;
let minute=0;
document.getElementById('pages').innerHTML=slides.map((s,i)=>{const begin=minute;minute+=s.minutes;return `<tr><td>${i+1}</td><td><a href="index.html?preview=1#${i+1}">${escapeText(s.title.replace(/\n/g,' '))}</a></td><td>${escapeText(s.presenter)}</td><td>${time(begin)}–${time(minute)}（${s.minutes}分）</td></tr>`;}).join('');
document.getElementById('total').textContent=`全${slides.length}ページ / ${minute}分の目安 / 16:00〜${time(minute)}`;
document.getElementById('scripts').innerHTML=slides.map((s,i)=>`<details><summary>${i+1}. ${escapeText(s.title.replace(/\n/g,' '))}</summary><pre>${escapeText(s.notes)}</pre></details>`).join('');
