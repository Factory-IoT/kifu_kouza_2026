// Export from the same source as the presenter window; no duplicated script text.
const fs=require('fs');const path=require('path');const vm=require('vm');
const publicDir=path.join(__dirname,'../web/public');
const slides=vm.runInNewContext(fs.readFileSync(path.join(publicDir,'slides.js'),'utf8')+';slides');
const time=m=>`${String(16+Math.floor(m/60)).padStart(2,'0')}:${String(m%60).padStart(2,'0')}`;
const dir=path.join(publicDir,'downloads');fs.mkdirSync(dir,{recursive:true});
for(const withNotes of [false,true]){
 let minute=0;
 const sections=slides.map((s,i)=>{const begin=minute;minute+=s.minutes;const notes=withNotes?s.notes:s.notes.split(/\n(?=【)/)[0];return [`【${i+1}/${slides.length}】${s.title.replace(/\n/g,' ')}`,`パート：${s.section}`,`担当：${s.presenter}`,`目安：${time(begin)}〜${time(minute)}（${s.minutes}分）`,'',notes].join('\n');});
 const header=`技術者と社会 — プラスチックが支える持続可能な技術\n岡山県立大学 寄付講座 第10回 / 2026年11月16日\nみのる化成株式会社 / 坪井 裕之・山下 泰弘\n全${slides.length}ページ / ${minute}分の目安\n${withNotes?'セリフ・進行メモ付き':'セリフのみ（進行メモを除く）'}\n時間配分には、写真の説明・問いかけ・質疑を含みます。\n\n`;
 const name=withNotes?'lecture-script-with-notes.txt':'lecture-script.txt';
 fs.writeFileSync(path.join(dir,name),'\ufeff'+(header+sections.join('\n\n'+'─'.repeat(48)+'\n\n')+'\n').replace(/\n/g,'\r\n'),'utf8');
 console.log(`Exported ${name}: ${slides.length} pages, ${minute} minutes`);
}
