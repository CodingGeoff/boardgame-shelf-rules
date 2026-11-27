from common import *
from detail import en_section
from en_common import EN, TAG_EN, codes, inferred, crops_for, photos_for, fit_text_en, enfile, AREAS
from urllib.parse import quote
import os
ANON=os.environ.get('ANON')=='1'
REPO='' if ANON else 'https://github.com/CodingGeoff/boardgame-shelf-rules'
PH={}
for r,ids in {1:['155036','155038','155042'],2:['155046','155049','155053'],3:['155056','155102','155106'],
              4:['155109','155114','155121'],5:['155125','155128','155142','155145']}.items():
    for p in ids: PH[p]=f'photos/round{r}/IMG20261127{p}.jpg'
games=[];docs={}
for g in G:
    i,name,mn,mx,best,t1,t2,age,w,tags,summ,teach,tips,pits=g
    fn=docfile(i)
    md=open(f'{BG}/{fn}').read()
    det='\n'.join(en_section(i,md))
    md=re.sub(r'<!-- (deep|detail):(start|end) -->\n?','',md)
    docs[fn]=md
    title=re.search(r'^# (.+)$',md,flags=re.M).group(1).strip()
    locs=LOC.get(str(i),[])
    photos=sorted({PH[p] for l in locs for p in re.findall(r'1551\d\d|1550\d\d',l['sec']+l['row']) if p in PH})
    b=[int(x) for x in re.findall(r'\d+',best)]
    e=EN[i]
    games.append(dict(id=i,name=name,title=title,mn=mn,mx=mx,bl=min(b),bh=max(b),t1=t1,t2=t2,age=age,w=w,
        tags=tags.split(),summ=summ,teach=teach,tips=tips,pits=pits,file=fn,loc=locs,photos=photos,
        unk=i in UNKNOWN_P,fit=fit_text(g),fitEn=fit_text_en(g),
        en=dict(n=e['n'],s=e['s'],su=e['su'],t=e['t'],e=e['e'],tp=e['tp'],pf=e['pf'],det=det),enfile=enfile(i),
        codes=codes(i),inf=inferred(i),crops=crops_for(i),ph=[p for p in photos_for(i) if p in PH]))
# photos with captions
allsec=[l['sec']+' '+l['row'] for v in LOC.values() for l in v]
import re as _re
photos=[]
for p in sorted(PH):
    cs=sorted({c for s in allsec if p in s for c in _re.findall(r'(?<![A-Za-z0-9])[A-H][1-9](?![0-9])',s)})
    n=sum(1 for gg in games if p in gg['ph'])
    zh=(f'货架 {"、".join(cs)}' if cs else '无编号区域')+(f' · {n} 款' if n else '')
    en=(f'shelves {", ".join(cs)}' if cs else 'no-code area')+(f' · {n} games' if n else '')
    photos.append(dict(id=p,orig=PH[p],zh=zh,en=en))
crops=json.load(open('/home/user/site/crops.json'))
CAPEN={'c1':'Photo 155049 upper level (HacKClaD, Wanted and Recruit)','c2':'Photo 155049 small-box pile (boxes labelled B2)','c3':'Photo 155046 top card bins',
 'c4':'Photo 155053 big boxes on top','c5':'Photo 155102 big-box stack on top of D/E','c6':'Photo 155114 big-box stack on top','c7':'Photo 155121 big-box stack on top','c8':'Photo 155142 glass bookcase, upper shelf (K\'s Game)'}
for c in crops:
    k=c['file'].split('/')[-1].split('_')[0]
    c['capEn']=CAPEN[k]
    a=[x for x in AREAS if k in x[1]][0]
    c['areaZh']=a[2]; c['areaEn']=a[3]
readme=open(f'{BG}/README.md').read()
docs['README.md']=readme
data=json.dumps(dict(games=games,docs=docs,repo=REPO,photos=photos,crops=crops,tagEn=TAG_EN),ensure_ascii=False).replace('</','<\\/')
tpl=open('/home/user/site/template.html').read()
html=tpl.replace('__DATA__',data)
out=os.environ.get('OUT','/home/user/site/index.html')
open(out,'w').write(html)
print('ok',len(html))
