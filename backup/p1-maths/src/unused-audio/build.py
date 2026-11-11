import sys
t=open(sys.argv[1],encoding='utf8').read(); a=open('audio.json',encoding='utf8').read()
assert '</' not in a
open(sys.argv[2],'w',encoding='utf8').write(t.rstrip()+'\n<script id="audio-data" type="application/json">'+a+'</script>\n')
