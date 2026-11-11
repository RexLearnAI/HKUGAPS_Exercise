import sys,json,base64,subprocess,os,hashlib
sys.path.insert(0,'/tmp/claude-0'); import tts, opencc
cc=opencc.OpenCC('t2s')
texts=json.load(open('texts.json')); out={}
os.makedirs('clips',exist_ok=True)
for lang in ['yue','cmn']:
    t=tts.mk(lang); out[lang]={}
    for txt in texts[lang]:
        h=hashlib.md5((lang+txt).encode()).hexdigest()[:10]; mp3=f'clips/{lang}-{h}.mp3'
        if not os.path.exists(mp3):
            a=t.generate(cc.convert(txt),sid=0,speed=0.85)
            tts.wav('tmp.wav',a.samples,a.sample_rate)
            subprocess.run(['ffmpeg','-y','-loglevel','error','-i','tmp.wav','-af','apad=pad_dur=0.2','-ac','1','-ar','22050','-b:a','40k',mp3],check=True)
        out[lang][txt]=base64.b64encode(open(mp3,'rb').read()).decode()
json.dump(out,open('audio.json','w'),ensure_ascii=False,separators=(',',':'))
print('done',sum(len(v) for v in out.values()),os.path.getsize('audio.json'))
