const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
const html=require('fs').readFileSync(process.argv[2],'utf8');
await p.setContent('<!doctype html><meta charset=utf-8>'+html);
const out=await p.evaluate(()=>{const r={yue:[],cmn:[]};for(const l of ['yue','cmn']){const s=new Set(window.__SAYS.map(f=>norm(f(l))));r[l]=[...s];}return r;});
require('fs').writeFileSync('texts.json',JSON.stringify(out,null,1));console.log(out.yue.length,out.cmn.length,errs);await b.close();})();
