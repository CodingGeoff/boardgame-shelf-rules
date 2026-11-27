"""Advanced guide (进阶详解) appended inside the detail block: teaching script, first-game time budget,
phase strategy, extra FAQ. Data: meta/a1-a6.py (A: id -> tuple or None). Also dfix.py patches detail tuples."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'meta'))
A = {}
for m in ('a1', 'a2', 'a3', 'a4', 'a5', 'a6'):
    A.update(__import__(m).A)
TEACH_MIN = {1: 5, 2: 10, 3: 15, 4: 25, 5: 40}


def _g(i):
    from common import G
    return next(g for g in G if g[0] == i)


def _s(s):
    return re.sub(r'^(开局|前期|中期|后期|终局)(?!条件|前)[，,]?', '', s)


def budget(i):
    g = _g(i)
    t1, t2, w = g[5], g[6], g[8]
    tm = TEACH_MIN.get(w, 10)
    first = round(t2 * 1.2 / 5) * 5 or t2
    return tm, t1, t2, first


def zh(i):
    d = A.get(i)
    tm, t1, t2, first = budget(i)
    unk = '资料待补' in _g(i)[9]
    L = ['', '## 进阶详解：讲解稿、时间预算、分阶段策略与补充 FAQ', '',
         '> 本节由整理者根据上文规则归纳，用于带新手和提高水平；与说明书冲突时以说明书为准。', '',
         '### 首局时间预算', '']
    if unk:
        L += ['- 公开资料不足，时长以盒面为准；第一次玩建议多留 15–20 分钟读说明书。', '']
    else:
        L += [f'- 讲规则：约 {tm} 分钟（复杂度 {"●" * _g(i)[8]}）。',
              f'- 正式游戏：{t1}–{t2} 分钟；新手第一局按约 {first} 分钟预留。',
              f'- 合计建议预留：约 {tm + first} 分钟。', '']
    if d is None:
        L += ['### 如何快速读懂说明书', '',
              '1. 先找“游戏目标 / 胜利条件”，用一句话说给大家听。',
              '2. 再找“回合流程”，把一个回合拆成 3–5 步写在纸上。',
              '3. 清点配件，对照说明书图示摆好开局。',
              '4. 明牌试玩一轮，遇到疑问先按最直观的理解玩，记下来赛后再查。',
              '5. 把本店的约定写回本文档，方便下次直接上手。', '']
        return L
    tz, te, sz, se, fq = d
    L += ['### 讲解稿（可以直接念给新手听）', '', f'> {tz}', '',
          '### 分阶段策略', '', f'- **开局**：{_s(sz[0])}', f'- **中盘**：{_s(sz[1])}', f'- **收尾**：{_s(sz[2])}', '',
          '### 补充 FAQ', '', *[f'- **问：{q}**  \n  答：{a}' for q, a, _, _ in fq], '']
    return L


def en(i):
    d = A.get(i)
    tm, t1, t2, first = budget(i)
    unk = '资料待补' in _g(i)[9]
    L = ['## Advanced guide: teaching script, time budget, phase strategy, extra FAQ', '',
         '> Summarised by the editor from the rules above for teaching and improving; the rulebook wins on conflicts.', '',
         '### First-game time budget', '']
    if unk:
        L += ['- Public data is limited — see the box for play time; allow an extra 15–20 minutes to read the rules.', '']
    else:
        L += [f'- Teaching: about {tm} min (weight {"●" * _g(i)[8]}).',
              f'- Play: {t1}–{t2} min; budget about {first} min for a first game.',
              f'- Total: about {tm + first} min.', '']
    if d is None:
        L += ['### How to learn it fast from the rulebook', '',
              '1. Find the goal / win condition and say it in one sentence.',
              '2. Break one turn into 3–5 steps on paper.',
              '3. Count components and set up following the rulebook pictures.',
              '4. Play one open-handed practice round; note doubts and check them afterwards.',
              '5. Write your house rules into this doc for next time.', '']
        return L
    tz, te, sz, se, fq = d
    L += ['### Teaching script (read it aloud)', '', f'> {te}', '',
          '### Strategy by phase', '', f'- **Early:** {se[0]}', f'- **Mid:** {se[1]}', f'- **Late:** {se[2]}', '',
          '### Extra FAQ', '', *[f'- **Q: {q}**  \n  A: {a}' for _, _, q, a in fq], '']
    return L


if __name__ == '__main__':
    miss = [i for i in range(1, 167) if i not in A]
    print('missing', miss, 'none', sorted(k for k, v in A.items() if v is None))
