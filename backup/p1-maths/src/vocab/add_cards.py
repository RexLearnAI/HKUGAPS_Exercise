import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vocab import VOCAB
tpl, key = sys.argv[1], sys.argv[2]
s = open(tpl, encoding='utf8').read()
if 'id="tab-cards"' in s:
    print('already has cards'); sys.exit(0)
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep('data-show="test">模擬測驗</button>', 'data-show="test">模擬測驗</button>\n      <button role="tab" id="tab-cards" aria-selected="false" data-show="cards">生字卡</button>')
rep('  <div id="parent" class="sheet" hidden>', '''  <div id="cards" class="sheet" hidden>
    <div class="sheet-head"><h2>生字卡</h2><span class="meta">練習卷和模擬測驗裏的字詞</span></div>
    <p class="instr">先看字，想想怎樣讀，再按一下卡片翻轉，就會聽到讀音。上面可以選廣東話或普通話。</p>
    <div class="cardgrid" id="cardgrid"></div>
  </div>
  <div id="parent" class="sheet" hidden>''')
rep('@media (max-width:480px){', '''.cardgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}
.fc{perspective:700px;height:150px;border:0;background:none;padding:0;cursor:pointer;font:inherit;color:inherit}
.fc:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:12px}
.fc-in{position:relative;width:100%;height:100%;transition:transform .45s;transform-style:preserve-3d}
.fc.flip .fc-in{transform:rotateY(180deg)}
.fc-f,.fc-b{position:absolute;inset:0;border-radius:12px;border:1.5px solid var(--line);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:8px;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.fc-f{background:var(--paper)}
.fc-f .w{font-family:var(--f-display);font-size:2.2rem;line-height:1.2;text-align:center}
.fc-f .hint{font-size:12px;color:var(--muted)}
.fc-b{background:var(--accent-soft);transform:rotateY(180deg)}
.fc-b .e{font-size:2.2rem;line-height:1.1}
.fc-b .w2{font-family:var(--f-display);font-size:1.3rem}
.fc-b .en{font-size:14px;color:var(--muted);text-align:center;line-height:1.3}
.fc.on .fc-b{box-shadow:0 0 0 3px var(--accent) inset}
@media (prefers-reduced-motion:reduce){.fc-in{transition:none}}
@media (max-width:480px){''')
rep('["practice","test","parent"].forEach(id=>', '["practice","test","cards","parent"].forEach(id=>')
js = 'const VOCAB=' + json.dumps([{'w': w, 'e': e, 'en': en} for w, e, en in VOCAB[key]], ensure_ascii=False) + ''';
(function(){
  const g=document.getElementById("cardgrid"); if(!g) return;
  VOCAB.forEach((v,i)=>{
    const c=el("button","fc"); c.type="button"; c.id="fc-"+i; c.setAttribute("aria-label",v.w+"，按一下翻卡並讀出");
    c.innerHTML=`<div class="fc-in"><div class="fc-f"><span class="w">${v.w}</span><span class="hint">按一下翻轉</span></div><div class="fc-b"><span class="e">${v.e}</span><span class="w2">${v.w}</span><span class="en">${v.en}</span></div></div>`;
    c.onclick=()=>{ const back=!c.classList.contains("flip"); c.classList.toggle("flip",back);
      if(back){ if(TTS.cur&&TTS.cur.btn===c) stopSpeak(); speak(v.w,c,null); } else if(TTS.cur&&TTS.cur.btn===c) stopSpeak(); };
    g.append(c);
  });
})();
'''
idx = s.rindex('</script>')
s = s[:idx] + js + s[idx:]
open(tpl, 'w', encoding='utf8').write(s)
print('ok', key, len(VOCAB[key]))
