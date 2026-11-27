from common import *
from urllib.parse import quote

def build(SUB,TITLE,FN):
    out=[TITLE,'',
    '> 由 `boardgames/` 下 166 篇单篇文档自动合并而成，每篇都包含原规则和“深入玩法”章节。单篇文档仍然保留，修改时请改单篇文档，再重新生成本合集。','',
    '在线选游戏：仓库根目录的 `index.html`（智能匹配 SPA）。','',
    '## 速查总表','',
    '| # | 游戏 | 人数 | 推荐 | 时长 | 复杂度 | 位置 |','|---|---|---|---|---|---|---|']
    for g in SUB:
        i,name,mn,mx,best,t1,t2,age,w,tags=g[:10]
        loc=LOC.get(str(i),[])
        l=(loc[0]['sec'].split('（')[0]+' · '+loc[0]['row']) if loc else '—'
        if len(loc)>1: l+=f' 等 {len(loc)} 处'
        unk=i in UNKNOWN_P
        out.append(f'| {i} | [{name}](#g{i:03d}) | {"?" if unk else f"{mn}–{mx}"} | {"?" if unk else best} | {"?" if unk else f"{t1}–{t2}′"} | {"●"*w} | {l.replace("|","/")} |')
    out+=['','---','']
    for g in SUB:
        i=g[0];fn=docfile(i);t=open(f'{BG}/{fn}').read()
        t=re.sub(r'<!-- deep:(start|end) -->\n?','',t)
        # demote headings
        t=re.sub(r'^(#{1,5}) ',lambda m:'#'+m.group(1)+' ',t,flags=re.M)
        # fix relative links to other docs -> anchors
        def lk(m):
            f=m.group(2); mm=re.match(r'(\d+)_',f)
            return f'[{m.group(1)}](#g{int(mm.group(1)):03d})' if mm else m.group(0)
        t=re.sub(r'\[([^\]]+)\]\(((?:\./)?\d+_[^)]+\.md)\)',lk,t)
        out+=[f'<a id="g{i:03d}"></a>','',t.strip(),'',f'<sub>单篇：[boardgames/{fn}]({quote(fn)}) · [↑ 回到总表](#速查总表)</sub>','','---','']
    
    
    open(f'{BG}/{FN}','w').write('\n'.join(out)); print(FN,os.path.getsize(f'{BG}/{FN}'))

build(G,'# 桌游规则合集（全部 166 篇）','ALL_合集.md')
build([g for g in G if g[0]<=78],'# 桌游规则合集·上册（01–78）','ALL_合集_上册_01-78.md')
build([g for g in G if g[0]>78],'# 桌游规则合集·下册（79–166）','ALL_合集_下册_79-166.md')
