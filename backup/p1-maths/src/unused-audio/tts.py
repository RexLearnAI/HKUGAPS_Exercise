import sherpa_onnx, sys, wave, numpy as np
def wav(p,samples,sr):
    w=wave.open(p,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(np.array(samples),-1,1)*32767).astype('<i2').tobytes());w.close()
M='/tmp/claude-0/models/'
def mk(lang):
    if lang=='yue':
        d=M+'vits-cantonese-hf-xiaomaiiwn/'
        v=sherpa_onnx.OfflineTtsVitsModelConfig(model=d+'vits-cantonese-hf-xiaomaiiwn.onnx',lexicon=d+'lexicon.txt',tokens=d+'tokens.txt')
        fst=d+'rule.fst'
    else:
        d=M+'vits-melo-tts-zh_en/'
        v=sherpa_onnx.OfflineTtsVitsModelConfig(model=d+'model.onnx',lexicon=d+'lexicon.txt',tokens=d+'tokens.txt',dict_dir=d+'dict')
        fst=','.join(d+x for x in ['date.fst','phone.fst','number.fst','new_heteronym.fst'])
    cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=v,num_threads=4),rule_fsts=fst,max_num_sentences=2)
    return sherpa_onnx.OfflineTts(cfg)
if __name__=='__main__':
    for lang in ['yue','cmn']:
        t=mk(lang); a=t.generate("每 2 個一數。2，4，6，空格。我的彈珠比 20 粒多，比 30 粒少。",sid=0,speed=1.0)
        wav(f'test_{lang}.wav',a.samples,a.sample_rate); print(lang,a.sample_rate,len(a.samples)/a.sample_rate)
