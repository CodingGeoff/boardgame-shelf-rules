from common import *
from urllib.parse import quote
REPO='https://github.com/CodingGeoff/boardgame-shelf-rules'
PH={}
for r,ids in {1:['155036','155038','155042'],2:['155046','155049','155053'],3:['155056','155102','155106'],
              4:['155109','155114','155121'],5:['155125','155128','155142','155145']}.items():
    for p in ids: PH[p]=f'photos/round{r}/IMG20261127{p}.jpg'
games=[];docs={}
for g in G:
    i,name,mn,mx,best,t1,t2,age,w,tags,summ,teach,tips,pits=g
    fn=docfile(i)
    md=open(f'{BG}/{fn}').read()
    md=re.sub(r'<!-- deep:(start|end) -->\n?','',md)
    docs[fn]=md
    title=re.search(r'^# (.+)$',md,flags=re.M).group(1).strip()
    locs=LOC.get(str(i),[])
    photos=sorted({PH[p] for l in locs for p in re.findall(r'1551\d\d|1550\d\d',l['sec']+l['row']) if p in PH})
    b=[int(x) for x in re.findall(r'\d+',best)]
    games.append(dict(id=i,name=name,title=title,mn=mn,mx=mx,bl=min(b),bh=max(b),t1=t1,t2=t2,age=age,w=w,
        tags=tags.split(),summ=summ,teach=teach,tips=tips,pits=pits,file=fn,loc=locs,photos=photos,
        unk=i in UNKNOWN_P,fit=fit_text(g)))
readme=open(f'{BG}/README.md').read()
docs['README.md']=readme
data=json.dumps(dict(games=games,docs=docs,repo=REPO),ensure_ascii=False).replace('</','<\\/')
tpl=open('/home/user/site/template.html').read()
html=tpl.replace('__DATA__',data)
open('/home/user/site/index.html','w').write(html)
print('ok',len(html))
