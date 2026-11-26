const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const root=process.argv[2];const out=process.argv[3]||'.';
const wrap=b=>`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>${b}</body></html>`;
const ct={'.webp':'image/webp','.png':'image/png','.ttf':'font/ttf','.html':'text/html'};
const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u=='/')u='/index.html';const f=path.join(root,u);if(!fs.existsSync(f)){r.writeHead(404);return r.end();}
 let d=fs.readFileSync(f);if(u=='/index.html')d=wrap(d.toString());r.writeHead(200,{'content-type':ct[path.extname(u)]||'application/octet-stream'});r.end(d);}).listen(8766);
(async()=>{const b=await chromium.launch();
for(const [name,vp] of [['m',{width:390,height:844}],['d',{width:1440,height:900}]]){
 const p=await b.newPage({viewport:vp});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()=='error')errs.push(m.text())});
 p.on('requestfailed',r=>errs.push('fail '+r.url()));p.on('response',r=>{if(r.status()>=400)errs.push(r.status()+' '+r.url())});
 await p.goto('http://localhost:8766/');await p.waitForTimeout(3000);
 await p.screenshot({path:`${out}/${name}_hero.png`});
 const H=await p.evaluate(()=>document.body.scrollHeight);
 for(let y=0;y<H;y+=300){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(40);}
 for(const sel of ['#carta','.feat','#pizzas','#porciones','#salsas','#postres','#club','.rewards','#pedir']){
   await p.evaluate(s=>{const el=document.querySelector(s);scrollTo(0,el.getBoundingClientRect().top+scrollY-(s.startsWith('#p')&&s!='#pedir'||s=='#salsas'||s=='#postres'?120:0))},sel);await p.waitForTimeout(900);
   await p.screenshot({path:`${out}/${name}_${sel.replace(/[#.]/g,'')}.png`});}
 console.log(name,H,errs);}
await b.close();srv.close();})();
