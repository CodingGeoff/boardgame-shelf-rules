"""Generate English rules docs boardgames/en/*.md from site/meta/en1-4.py + Chinese metadata."""
import os, re, glob
from urllib.parse import quote
from common import G, docfile, LOC, UNKNOWN_P, BG
from en_common import EN, TAG_EN, codes, inferred, photos_for, crops_for, fit_text_en, WL_EN, enfile, tags_en

OUT = f'{BG}/en'
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(f'{OUT}/*.md'):
    os.remove(f)

REPO = 'https://github.com/CodingGeoff/boardgame-shelf-rules'
PAGES = 'https://codinggeoff.github.io/boardgame-shelf-rules/'


def rng(a, b, unit=''):
    return f'{a}{unit}' if a == b else f'{a}–{b}{unit}'


def loc_lines(i):
    out = []
    c = codes(i)
    inf = inferred(i)
    if c:
        out.append(f'- **Shelf code:** {" / ".join(c)}')
    elif inf:
        out.append(f'- **Shelf code:** none on the photo — inferred area: {inf["en"]} *(inferred)*')
    ph = photos_for(i)
    if ph:
        out.append('- **Photos:** ' + ', '.join(f'[{p}](../../photos/web/IMG20261127{p}.jpg)' for p in ph))
    cr = crops_for(i)
    if cr and not c:
        out.append('- **Close-up crops:** ' + ', '.join(f'[{os.path.basename(x).split("_")[0]}](../../{x})' for x in cr))
    for l in LOC.get(str(i), []):
        out.append(f'- Original note (Chinese): {l["sec"]} → {l["row"]}')
    return out or ['- See the README pending list (位置待确认).']


def doc(g):
    i, name, mn, mx, best, t1, t2, age, w, tags, summ, teach, tips, pits = g
    e = EN[i]
    unk = i in UNKNOWN_P
    good, bad = fit_text_en(g)
    zf = docfile(i)
    L = [f'# {e["n"]}', '',
         f'> Chinese name: **{name}** · Doc #{i} · [中文原文 / Chinese doc](../{quote(zf)}) · [Open in the web app]({PAGES}#doc/{i})', '',
         '## At a glance', '', '| Item | Value |', '|---|---|',
         f'| Players | {"see box" if unk else rng(mn, mx)} (best: {best}) |',
         f'| Play time | {"see box" if unk else rng(t1, t2, " min")} |',
         f'| Age | {"see box" if unk else str(age) + "+"} |',
         f'| Complexity | {"●" * w}{"○" * (5 - w)} {WL_EN[w]} ({w}/5) |',
         f'| Tags | {", ".join(tags_en(tags))} |', '',
         '## Where is it on the shelf?', '', *loc_lines(i), '',
         '## Overview', '', e['s'], '',
         '## Setup', '', *[f'{k}. {x}' for k, x in enumerate(e['su'], 1)], '',
         '## How to play', '', *[f'{k}. {x}' for k, x in enumerate(e['t'], 1)], '',
         '## Game end & scoring', '', *[f'- {x}' for x in e['e']], '',
         *([] if e['e'][0].startswith('See the rulebook') else ['## 5-minute teaching order', '',
         f'1. **Goal first:** {e["e"][0]}',
         f'2. **What you do on a turn:** {e["t"][0]}',
         f'3. **Setup check:** {e["su"][0]}',
         f'4. **The one rule people forget:** {e["pf"][0]}',
         '5. Play one open-handed practice round, then start for real.', '']),
         '## Strategy tips', '', *[f'- {x}' for x in e['tp']], '',
         '## Common mistakes', '', *[f'- {x}' for x in e['pf']], '',
         '## Good for / not for', '', f'- **Good for:** {"; ".join(good)}', f'- **Not ideal for:** {"; ".join(bad)}', '',
         '---', '',
         f'*English summary written from the Chinese doc and public rules. If anything conflicts with the rulebook in the box, the rulebook wins. Sources are listed in the [Chinese doc](../{quote(zf)}).*', '']
    from detail import en_section
    k = L.index('---')
    L[k:k] = en_section(i, open(f'{BG}/{zf}').read())
    if unk or '资料待补' in tags:
        L.insert(4, '> ⚠️ Public rules data for this game is limited; treat this page as a pointer and read the rulebook in the box.\n')
    return '\n'.join(L)


rows = []
bodies = []
for g in G:
    i = g[0]
    f = enfile(i)
    body = doc(g)
    open(f'{OUT}/{f}', 'w').write(body)
    bodies.append((i, body))
    c = codes(i)
    inf = inferred(i)
    where = ' / '.join(c) if c else ('≈ ' + inf['en'].split(' (')[0].lstrip('≈ ') + ' *(inferred)*' if inf else '?')
    unk = i in UNKNOWN_P
    rows.append(f'| {i} | [{EN[i]["n"]}]({quote(f)}) | {g[1]} | {"?" if unk else rng(g[2], g[3])} | {"?" if unk else rng(g[5], g[6])} | {"●" * g[8]} | {where} |')

idx = ['# Board Game Shelf — English Rules Index', '',
       f'{len(G)} English rules summaries, one per Chinese doc. Web app (supports English questions): {PAGES}', '',
       '- Part 1 in one file: [ALL_EN_part1_01-78.md](ALL_EN_part1_01-78.md)',
       '- Part 2 in one file: [ALL_EN_part2_79-166.md](ALL_EN_part2_79-166.md)',
       '- Chinese index: [../README.md](../README.md)', '',
       '“Shelf” shows the code on the shelf label. Games without a visible code show an *inferred* area — use the HD photos and close-up crops linked in each doc.', '',
       '| # | Game | 中文名 | Players | Minutes | Weight | Shelf |', '|---|---|---|---|---|---|---|', *rows, '']
open(f'{OUT}/README.md', 'w').write('\n'.join(idx))


def merged(lo, hi, title):
    part = [b for i, b in bodies if lo <= i <= hi]
    toc = [f'- [{EN[i]["n"]}](#g{i})' for i, _ in bodies if lo <= i <= hi]
    out = [f'# {title}', '', *toc, '']
    for i, b in bodies:
        if lo <= i <= hi:
            b = b.replace('](../', '](../').replace('../../', '../../')
            out += [f'<a id="g{i}"></a>', '', b, '']
    return '\n'.join(out)


open(f'{OUT}/ALL_EN_part1_01-78.md', 'w').write(merged(1, 78, 'All English Rules — Part 1 (01–78)'))
open(f'{OUT}/ALL_EN_part2_79-166.md', 'w').write(merged(79, 166, 'All English Rules — Part 2 (79–166)'))

# add English link line to each Chinese doc (idempotent)
n = 0
for g in G:
    i = g[0]
    p = f'{BG}/{docfile(i)}'
    s = open(p).read()
    s = re.sub(r'\n> 🌐 English version: .*\n', '\n', s)
    line = f'> 🌐 English version: [en/{enfile(i)}](en/{quote(enfile(i))})'
    s = re.sub(r'^(# .+\n)', lambda m: m.group(1) + line + '\n', s, count=1)
    open(p, 'w').write(s)
    n += 1
print('en docs', len(bodies), 'zh links', n)
