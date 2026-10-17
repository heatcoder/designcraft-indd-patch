#!/usr/bin/env python3
"""Exercise extracted CLI: real INDD fixture import and Malayalam commands."""
from pathlib import Path
import argparse,json,subprocess,urllib.request,hashlib
p=argparse.ArgumentParser();p.add_argument('--cli',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
u='https://raw.githubusercontent.com/openpreserve/format-corpus/0bd37b0d10f397e0c2a7785befa2253f912b77fc/desktop-publishing/InDesign/Neddy_Flyer_HeatherRyan.indd';fixture=a.work/'CC0-Neddy-Flyer.indd';data=urllib.request.urlopen(u,timeout=60).read();assert hashlib.sha256(data).hexdigest()=='8f206d618c0161cfddf4c18aa3932ed99d9e500bf1260c2551e316b12a4e3ed2';fixture.write_bytes(data)
output=a.work/'imported.idml';subprocess.run([str(a.cli),'run','--in',str(fixture),'--export',str(output)],check=True);assert output.stat().st_size>100
steps=[{'command':'frame.create','params':{'rect':[40,40,400,200],'content':'text','text':'OLD'}},{'command':'text.select','params':{'story':'$0.story','anchor':0,'focus':3}},{'command':'malayalam.insert','params':{'text':'namaskaaram','mode':'manglish'}},{'command':'story.get','params':{'story':'$0.story'}},{'command':'edit.undo'},{'command':'story.get','params':{'story':'$0.story'}},{'command':'edit.redo'},{'command':'story.get','params':{'story':'$0.story'}},{'command':'malayalam.convert','params':{'text':"Cd'",'mode':'inscript'}}]
r=subprocess.run([str(a.cli),'script','-'],input=json.dumps(steps),text=True,encoding="utf-8",capture_output=True,check=True);(a.work/'typing-results.json').write_text(r.stdout, encoding='utf-8');result=json.loads(r.stdout);assert result['completed']==len(steps),result
r=result['results'];assert r[3]['text']=='നമസ്കാരം' and r[5]['text']=='OLD' and r[7]['text']=='നമസ്കാരം' and r[8]['text']=='ണ്ട',result
print('PASS extracted CLI real INDD import, Malayalam insertion/replacement, undo/redo, InScript conversion. UI event tests run separately.')
