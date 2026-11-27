from common import *
S='<!-- deep:start -->';E='<!-- deep:end -->'
for g in G:
    i,name,mn,mx,best,t1,t2,age,w,tags,summ,teach,tips,pits=g
    fn=docfile(i);p=f'{BG}/{fn}';t=open(p).read()
    t=re.sub(re.escape(S)+r'.*?'+re.escape(E)+r'\n*','',t,flags=re.S)
    good,bad=fit_text(g)
    steps=[s.strip(' 。') for s in re.split(r'[；;]',teach) if s.strip(' 。')]
    pl='见盒面' if i in UNKNOWN_P else (f'{mn} 人' if mn==mx else f'{mn}–{mx} 人')
    tm='见盒面' if i in UNKNOWN_P else (f'{t1} 分钟' if t1==t2 else f'{t1}–{t2} 分钟')
    sec=[S,'## 深入玩法：教学、策略与易错点','',
    '> 本节是整理者根据上文规则和公开资料做的归纳，方便快速上手。与盒内说明书冲突时，以说明书为准。','',
    f'**一句话介绍**：{summ}','',
    '| 维度 | 参考 |','|---|---|',
    f'| 支持人数 | {pl} |',
    f'| 推荐人数 | {"见盒面" if i in UNKNOWN_P else best+" 人"} |',
    f'| 单局时长 | {tm} |',
    f'| 建议年龄 | {"见盒面" if i in UNKNOWN_P else str(age)+"+"} |',
    f'| 复杂度 | {"●"*w}{"○"*(5-w)} {WL[w]} |',
    f'| 标签 | {" · ".join(tags.split())} |','',
    '### 5 分钟教学顺序','']
    sec+= [f'{k}. {s}' for k,s in enumerate(steps,1)]
    sec+=['','### 进阶策略','']+[f'- {x}' for x in tips]
    sec+=['','### 常见错误与容易混淆的规则','']+[f'- {x}' for x in pits]
    sec+=['','### 适合 / 不适合','',f'- 👍 **适合**：{"；".join(good)}',f'- 👎 **不太适合**：{"；".join(bad)}','',E,'']
    block='\n'.join(sec)
    m=re.search(r'^## 参考来源',t,flags=re.M)
    if m: t=t[:m.start()]+block+'\n'+t[m.start():]
    else: t=t.rstrip()+'\n\n'+block
    open(p,'w').write(t)
print('deepened',len(G))
