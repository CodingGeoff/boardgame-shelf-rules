"""Add a detailed-supplement section (components / full example / scoring example / FAQ /
player counts / variants) to every Chinese doc. Idempotent via <!-- detail:start/end --> markers.
English sections are produced by en_section() and appended by build_en.py.
Data: site/meta/d1-d4.py (dict D: id -> tuple or None)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'meta'))
sys.path.insert(0, HERE)

D = {}
for m in ('d1', 'd2', 'd3', 'd4', 'd5'):
    D.update(__import__(m).D)
from dfix import F as _F
for _i, _p in _F.items():
    _t = list(D[_i])
    for _k, _v in _p.items():
        _t[_k] = _v
    D[_i] = tuple(_t)
import adv

S, E = '<!-- detail:start -->', '<!-- detail:end -->'


def components_zh(text):
    """Pull the component list out of the Chinese doc (table row or ## 配件 section)."""
    body = text.split('<!-- deep:start -->')[0]
    out = []
    m = re.search(r'^\|\s*配件[^|]*\|\s*(.+?)\s*\|\s*$', body, re.M)
    if m:
        out.append(m.group(1))
    m = re.search(r'^##+\s*(?:核心)?配件[^\n]*\n(.*?)(?=^##|\Z)', body, re.M | re.S)
    if m:
        for l in m.group(1).strip().splitlines():
            l = l.strip()
            if not l or l.startswith('|---') or l.startswith('>'):
                continue
            if l.startswith('|'):
                cells = [c.strip() for c in l.strip('|').split('|')]
                if cells[0] in ('配件', '项目'):
                    continue
                l = '：'.join(c for c in cells if c)
            out.append(l.lstrip('-* ').strip())
    seen, res = set(), []
    for x in out:
        if x and x not in seen:
            seen.add(x); res.append(x)
    return res[:14]


CHECK_ZH = ['开盒后先按说明书的配件表逐项清点；卡牌按类型分开数，少牌会直接影响平衡。',
            '确认指示物、骰子、计分轨标记齐全；缺失时可以用硬币或其他游戏的通用指示物临时代替。',
            '把参考卡/玩家帮助卡发给每人，第一局能省很多翻规则的时间。']
CHECK_EN = ['Count the components against the rulebook list; sort cards by type — a missing card can break the balance.',
            'Check tokens, dice and score markers; coins or generic tokens can stand in for missing pieces.',
            'Hand out reference cards before the first game to save rulebook time.']


def best(i):
    from common import G
    for g in G:
        if g[0] == i:
            return g[4]
    return ''


def zh_section(i, text):
    d = D.get(i)
    comp = components_zh(text)
    L = [S, '', '## 详细补充：配件清点、示例局、计分、FAQ、人数与变体', '',
         '> 本节是整理者根据上文规则编写的**演示与补充**，用来帮助理解；示例中的数字为演示用。与盒内说明书冲突时，**以说明书为准**。', '',
         '### 配件清点清单', '']
    if comp:
        L += [f'- [ ] {c}' for c in comp]
    else:
        L += ['- [ ] 公开资料没有完整配件表，请以盒内配件表为准。']
    L += ['', '开局前检查：', *[f'- {c}' for c in CHECK_ZH], '']
    if d is None:
        L += ['### 完整示例局', '',
              '公开资料不足，无法给出可靠的示例局。建议第一次玩时：', '',
              '1. 先通读盒内说明书的“回合流程”和“胜利条件”两节；',
              '2. 明牌试玩一轮，边玩边对照说明书；',
              '3. 把本店的约定（家庭规则）记在本页，方便下次直接上手。', '',
              '### 计分示例', '', '见盒内说明书。', '',
              '### 规则 FAQ', '', '- **问：网上能找到规则吗？** 答：本游戏公开资料很少，请以盒内说明书为准；如果知道出版社或英文名，可以补充本文档。', '',
              '### 不同人数', '', '见盒面人数标注。', '',
              '### 变体与扩展', '', '见说明书。', '', *adv.zh(i), E]
        return '\n'.join(L)
    ex_zh, ex_en, sc_zh, sc_en, faq, pl_zh, pl_en, va_zh, va_en = d
    L += ['### 完整示例局（演示）', '', *[f'{k}. {x}' for k, x in enumerate(ex_zh, 1)], '',
          '### 计分示例', '', f'- {sc_zh}', '',
          '### 规则 FAQ / 易混淆点裁定', '']
    if faq:
        L += [f'- **问：{q}**  \n  答：{a}' for q, a, _, _ in faq]
    else:
        L += ['- 常见疑问请参考上文“常见错误与容易混淆的规则”，其余以说明书为准。']
    L += ['', '### 不同人数的差异', '', f'- {pl_zh}', *([f'- 推荐人数：{best(i)} 人。'] if best(i) else []), '',
          '### 官方变体与扩展', '', f'- {va_zh}', '', *adv.zh(i), E]
    return '\n'.join(L)


def en_section(i, zh_text):
    d = D.get(i)
    comp = components_zh(zh_text)
    L = ['## Detailed supplement: components, worked example, scoring, FAQ, player counts, variants', '',
         '> Written by the editor from the rules above as a walkthrough; numbers in the example are illustrative. The rulebook in the box always wins.', '',
         '### Component checklist', '']
    if comp:
        L += ['From the Chinese doc (original wording):', '', *[f'- [ ] {c}' for c in comp]]
    else:
        L += ['- [ ] No complete public component list — use the list in the box.']
    L += ['', 'Before you start:', *[f'- {c}' for c in CHECK_EN], '']
    if d is None:
        L += ['### Worked example', '', 'Public information is too limited for a reliable example. For a first game:', '',
              '1. Read the turn sequence and win conditions in the box rulebook;',
              '2. Play one open-handed practice round;',
              '3. Note any house rules on this page for next time.', '',
              '### Scoring example', '', 'See the rulebook.', '',
              '### Rules FAQ', '', '- **Q: Are the rules online?** A: Very little public info; use the box rulebook.', '',
              '### Player counts', '', 'See the box.', '',
              '### Variants & expansions', '', 'See the rulebook.', '', *adv.en(i)]
        return L
    ex_zh, ex_en, sc_zh, sc_en, faq, pl_zh, pl_en, va_zh, va_en = d
    L += ['### Worked example (illustrative)', '', *[f'{k}. {x}' for k, x in enumerate(ex_en, 1)], '',
          '### Scoring example', '', f'- {sc_en}', '',
          '### Rules FAQ / rulings', '']
    if faq:
        L += [f'- **Q: {q}**  \n  A: {a}' for _, _, q, a in faq]
    else:
        L += ['- See “Common mistakes” above; anything else — check the rulebook.']
    L += ['', '### Player-count differences', '', f'- {pl_en}', *([f'- Best with: {best(i)} players.'] if best(i) else []), '',
          '### Official variants & expansions', '', f'- {va_en}', '', *adv.en(i)]
    return L


def apply_zh():
    from common import G, docfile, BG
    n = 0
    for g in G:
        i = g[0]
        p = f'{BG}/{docfile(i)}'
        s = open(p).read()
        s = re.sub(r'\n?' + re.escape(S) + r'.*?' + re.escape(E) + r'\n?', '\n', s, flags=re.S)
        sec = zh_section(i, s)
        k = s.find('\n## 参考来源')
        if k >= 0:
            s = s[:k].rstrip('\n') + '\n\n' + sec + '\n' + s[k:]
        else:
            s = s.rstrip('\n') + '\n\n' + sec + '\n'
        s = re.sub(r'\n{4,}', '\n\n\n', s)
        open(p, 'w').write(s)
        n += 1
    print('detail zh', n, 'ids with data', sum(1 for v in D.values() if v), 'pending', sorted(k for k, v in D.items() if v is None))


if __name__ == '__main__':
    missing = [i for i in range(1, 167) if i not in D]
    assert not missing, missing
    for i, v in D.items():
        if v is not None:
            assert len(v) == 9, (i, len(v))
            assert all(len(f) == 4 for f in v[4]), i
            assert all(x for x in v[0]) and all(x for x in v[1]), i
    apply_zh()
