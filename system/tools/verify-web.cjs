const { chromium } = require('C:/Users/yamashita_y00031/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const os = require('os');
const slides = vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../web/public/slides.js'),'utf8')+';slides');
const base=process.env.LECTURE_URL||'http://127.0.0.1:8310';
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1600,height:1000}});
 const page=await context.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/?session=qa');
 const captures=path.join(os.tmpdir(),'kifu-lecture-qa');fs.mkdirSync(captures,{recursive:true});
 for(let i=0;i<slides.length;i++){
  await page.evaluate(i=>show(i),i);
  await page.locator('#slide img').evaluateAll(imgs=>Promise.all(imgs.map(img=>img.decode())));
  const bad=await page.evaluate(()=>{
   const slide=document.querySelector('#slide'),footer=slide.querySelector('.footer').getBoundingClientRect();
   return [...slide.querySelectorAll('h1,h2,.lead,li,.caption,.statement,.visual img,table')].map(el=>({text:el.textContent.slice(0,55)||el.alt,r:el.getBoundingClientRect()})).filter(x=>x.r.bottom>footer.top-4||x.r.right>slide.getBoundingClientRect().right-20).map(x=>x.text);
  });
  if(bad.length)errors.push(`Slide ${i+1} overflow: ${bad.join('; ')}`);
  if((await page.locator('#slide').innerText()).includes('<strong>'))errors.push(`Slide ${i+1} literal markup`);
  await page.screenshot({path:path.join(captures,`slide-${String(i+1).padStart(2,'0')}.png`)});
 }
 await page.evaluate(()=>show(0));
 const popupPromise=page.waitForEvent('popup');await page.locator('#presenter').click();const speaker=await popupPromise;await speaker.waitForLoadState();
 speaker.on('pageerror',e=>errors.push(e.message));
 await speaker.locator('#next').click();await page.waitForFunction(()=>current===1);
 await speaker.keyboard.press('ArrowRight');await page.waitForFunction(()=>current===2);
 await speaker.mouse.move(350,300);await speaker.mouse.wheel(0,180);await speaker.waitForTimeout(900);if(await speaker.evaluate(()=>current)!==2)throw new Error('Presenter wheel must not change pages');
 await speaker.mouse.wheel(0,-180);await speaker.waitForTimeout(900);if(await speaker.evaluate(()=>current)!==2)throw new Error('Presenter wheel must not change pages');
 await page.keyboard.press('ArrowRight');await speaker.waitForFunction(()=>current===3);
 await speaker.locator('#timer').click();await page.waitForFunction(()=>running);await speaker.waitForTimeout(1100);await speaker.locator('#timer').click();await page.waitForFunction(()=>!running);
 const e=await page.evaluate(()=>elapsed);if(e<1000)errors.push('Presenter timer toggle failed');
 await speaker.locator('#reset').click();await page.waitForFunction(()=>elapsed===0);
 await speaker.locator('#jump').selectOption('24');await page.waitForFunction(()=>current===24);await speaker.waitForTimeout(100);
 await speaker.screenshot({path:path.join(captures,'presenter.png')});
 await speaker.locator('#jump').selectOption('0');await speaker.locator('#prev').isDisabled().then(v=>{if(!v)errors.push('First page previous enabled');});
 await speaker.locator('#jump').selectOption(String(slides.length-1));await speaker.locator('#next').isDisabled().then(v=>{if(!v)errors.push('Last page next enabled');});
 await page.keyboard.press('Escape');await page.locator('#overview').click();await page.locator('[data-slide="5"]').click();await speaker.waitForFunction(()=>current===5);
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(captures,'mobile.png')});
 await browser.close();
 console.log(JSON.stringify({pages:slides.length,totalMinutes:slides.reduce((n,s)=>n+s.minutes,0),captures,errors},null,2));
 if(errors.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1);});
