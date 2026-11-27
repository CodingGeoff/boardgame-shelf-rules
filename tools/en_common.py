import sys,re
sys.path.insert(0,'/home/user/site/meta')
import en1,en2,en3,en4,en5
EN={**en1.E,**en2.E,**en3.E,**en4.E,**en5.E}
TAG_EN=dict(x.split(':',1) for x in re.split(r'\s+(?=\S+:)','''家庭:family 卡牌:cards 派对:party 推理:deduction 经典:classic 策略:strategy 骰子:dice 隐藏身份:hidden role 资料待补:data incomplete 阵营:teams 双人:2-player 引擎:engine 推运:push-your-luck 合作:co-op 轻策:light strategy 嘴炮:talky 谈判:negotiation 动漫:anime 儿童:kids 空间:spatial 战斗:combat 轮抽:drafting 收集:set collection 经济:economic 语言:word 拍卖:auction 区域控制:area control 重策:heavy 竞速:race 反应:reaction 吹牛:bluffing 实时:real-time 数字:numbers 构筑:deck-building 交易:trading 团队:team 投票:voting 押注:betting 拼图:puzzle 黑色幽默:dark humour 生存:survival 移动:movement 淘汰:elimination 手牌管理:hand management 剧情:story 联想:association 身份推理:social deduction 解谜:puzzle-solving App:app 文明:civilization 地城:dungeon 连锁:combo 抽象:abstract 聊天:conversation 同时行动:simultaneous 爬梯:ladder-climbing 虚张声势:bluff 记忆:memory 扑克:poker IP:licensed IP 隐藏移动:hidden movement 拼块:polyomino 战役:campaign 卡牌驱动:card-driven 探索:exploration 背叛:traitor 掷骰:dice rolling 原创:Chinese original 吃墩:trick-taking 区域多数:majority 隐藏阵营:hidden teams 汉字:Chinese characters 亲子:parent-child 敏捷:dexterity 平衡:balance 科幻:sci-fi 不淘汰:no elimination 角色扮演:role-play 国风:Chinese style 分赃:loot split 密室:escape room 搞笑:funny 沉默:silent 读人:read people 投机:speculation RPG:RPG 角色:characters 美术:art 计分:scoring Boss:boss 材料转化:conversion 偷取:stealing 问答:Q&A 互动:interaction 作弊:cheating 铺路:path building 外交:diplomacy 风险:risk 海龟汤:lateral thinking 一对多:one-vs-many 编程:programming 同时计划:simultaneous planning 动作:action 轮选:card selection MOBA:MOBA 无骰子:no dice 工人放置:worker placement 探险:adventure 传承:legacy 二战:WWII 网络:network 拼放:pattern building 资源:resources 艺术:art 市场操纵:market manipulation 恐怖:horror 半合作:semi-co-op 印第安扑克:Indian poker 真伪:authenticity 身份:identity 古风:ancient China 中式恐怖:Chinese horror 民俗:folklore 猜词:word guessing 陷害:take-that 板块拼放:tile placement 贿赂:bribery 互殴:brawl 路网:route building 灵巧:flicking 算术:arithmetic 破冰:icebreaker 拉锯:tug-of-war 猫:cats 经营:management 字谜:riddles 成语:idioms 资源转换:resource conversion 堆叠:stacking 资源管理:resource management 克苏鲁:Cthulhu 有限沟通:limited communication 隐藏信息:hidden information 饮酒:drinking 竞争:competitive 三方:three factions 冲突:conflict 野心:ambition 牌组构筑:deck construction 锦标赛:tournament 自走棋:auto-battler 抽袋:bag-building 默契:mind-meld 写答案:writing 指控:accusation 枪战:shootout 股票:stocks 线索:clues 猜谜:riddle 现实:realistic 体验:experience 比划:charades 传话:telephone 阻挠:blocking 对战:versus 舰娘:warship girls 编队:fleet building 春节:Spring Festival 谍战:espionage 同时选择:simultaneous choice 剧本杀:murder mystery 一次性:one-time 快速:quick'''))
LOC_EN=[('用户补充','Added by the owner'),('不在照片中','not in the photos'),('位置待确认','location to be confirmed'),('请在店内询问','ask the staff'),('第六轮','Round 6'),('铁网后货架','shelf behind the wire grid'),('最上面','very top'),('最下面','bottom'),('第三轮照片','Round-3 photo '),('第四轮','Round 4 '),('第五轮','Round 5 '),('照片','Photo '),('货架','shelf'),('免费借玩','free-to-borrow'),('顶部大盒堆','big-box stack on top'),('大盒堆','big-box stack'),('小盒堆','small-box pile'),('收纳盒','storage bins'),('卡牌收纳盒','card storage bins'),('透明收纳箱','clear storage box'),('玻璃书柜','glass bookcase'),('盒装剧本杀','boxed murder mysteries'),('上层','upper level'),('下层','lower level'),('中层','middle level'),('顶层','top level'),('底层','bottom level'),('右列','right column'),('左侧',' left side '),('右侧',' right side '),('左边缘','left edge'),('中部',' middle '),('中间那摞','middle stack'),('左侧整摞','left stack'),('右上','top right'),('左上','top left'),('那摞','stack'),('一摞','stack'),('层','level '),('行','row '),('白色大标签','white labels'),('蓝色编号标签','blue number labels'),('白标','white label'),('蓝标','blue label'),('蓝框编号标签','blue-framed number labels'),('标签','label'),('贴','with'),('另一组货架','another shelf group'),('一带','area'),('与',' and '),('和',' and '),('及',' and '),('（',' ('),('）',')'),('：',': '),('，',', '),('、',', '),('不重复计数','not double-counted'),('拍到的是同一堆','shows the same pile'),('确认是','confirmed'),('疑似','possibly'),('等','etc.'),('处','places')]
def loc_en(s):
    for a,b in LOC_EN: s=s.replace(a,b)
    return re.sub(r'\s+',' ',s).strip()
def tags_en(tags): return [TAG_EN.get(t,t) for t in tags.split()]

# ---------- shelf codes / inferred areas ----------
import json as _j
_LOC=_j.load(open('/home/user/site/loc.json'))
CODE_RE=re.compile(r'(?<![A-Za-z0-9])[A-H][1-9](?![0-9])')
def codes(i):
    return sorted({c for l in _LOC.get(str(i),[]) for c in CODE_RE.findall(l['sec']+' '+l['row'])})
AREAS=[ # (sec prefix, crop ids, zh, en)
 ('照片 155049 上层',['c1'],'≈ B 区上层（同一层旁边有 B4 箱子）','≈ upper level of the B section (a B4 box sits beside it)'),
 ('照片 155049 小盒堆',['c2'],'≈ B2（这堆小盒大多贴 B2 标签，右侧个别是 C3/B3）','≈ B2 (most boxes in this small pile carry B2 labels; a few on the right show C3/B3)'),
 ('照片 155046 顶层',['c3'],'≈ B4 货架上方的顶层卡牌收纳盒（按蓝色编号标签找）','≈ card bins on top, above shelf B4 (look for the blue number label)'),
 ('照片 155053：顶层',['c4'],'≈ D/E 柜顶（在 D1/D2、E1/E2 标牌上方）','≈ top of the D/E cabinet (above the D1/D2 and E1/E2 signs)'),
 ('第三轮照片 155102：D/E',['c5'],'≈ D/E 柜顶（“免费借玩”货架顶部）','≈ top of the D/E "free to borrow" cabinet'),
 ('照片 155114 / 155121：顶部',['c6','c7'],'≈ E–G 柜顶（在 E1/E2、F1/F2、G1/G2 标牌上方）','≈ top of the E–G cabinets (above the E1/E2, F1/F2, G1/G2 signs)'),
 ('照片 155142',['c8'],'玻璃书柜上层（没有编号）','glass bookcase, upper shelf (no code)'),
 ('照片 204000：上层左侧',['c9'],'铁网后货架·上层左侧那摞（没有编号）','shelf behind the wire grid, upper level, left stack (no code)'),
 ('照片 204000：上层中部',['c10'],'铁网后货架·上层中部（没有编号）','shelf behind the wire grid, upper level, middle (no code)'),
 ('照片 204000：上层右侧',['c11'],'铁网后货架·上层右侧顶部（没有编号）','shelf behind the wire grid, upper level, top right (no code)'),
]
_CROPS={c['file'].split('/')[-1].split('_')[0]:c for c in _j.load(open('/home/user/site/crops.json'))}
def area_of(sec):
    for p,cr,zh,en in AREAS:
        if sec.startswith(p): return cr,zh,en
    return [],'',''
def crops_for(i):
    out=[]
    for l in _LOC.get(str(i),[]):
        cr,_,_=area_of(l['sec'])
        for c in cr:
            f=_CROPS[c]['file']
            if f not in out: out.append(f)
    return out
def inferred(i):
    if codes(i): return None
    zh=[];en=[]
    for l in _LOC.get(str(i),[]):
        _,z,e=area_of(l['sec'])
        if z and z not in zh: zh.append(z); en.append(e)
    return dict(zh='；'.join(zh),en='; '.join(en))
PHOTO_RE=re.compile(r'1550\d\d|1551\d\d|204000')
def photos_for(i):
    return sorted({p for l in _LOC.get(str(i),[]) for p in PHOTO_RE.findall(l['sec']+l['row'])})

WL_EN={1:'Very light',2:'Light',3:'Medium',4:'Medium-heavy',5:'Heavy'}
def fit_text_en(g):
    i,name,mn,mx,best,t1,t2,age,w,tags,*_=g
    tg=set(tags.split()); good=[];bad=[]
    if '双人' in tg or mx==2: good.append('couples / head-to-head duels')
    if mx>=8: good.append('big parties')
    if '合作' in tg: good.append('friends who prefer working together')
    if tg&{'吹牛','嘴炮','谈判'}: good.append('talkative groups who enjoy acting and bluffing')
    if tg&{'推理','隐藏身份','阵营'}: good.append('people who love deduction and guessing identities')
    if tg&{'儿童','亲子'} or age<=6: good.append('families with young children')
    if w>=4: good.append('experienced gamers who want a deep think')
    if w<=1 and '儿童' not in tg: good.append('icebreakers; newcomers and grandparents can learn it instantly')
    if t2<=20: good.append('short gaps — waiting for friends, before or after dinner')
    if tg&{'反应','敏捷','实时'}: good.append('fans of speed and excitement')
    if w>=4: bad.append('relaxed chatting sessions')
    if tg&{'吹牛','嘴炮','谈判','背叛','陷害'}: bad.append('players who dislike conflict or backstabbing')
    if tg&{'反应','敏捷','实时'}: bad.append('people who want to think slowly and quietly')
    if t1>=90: bad.append('when time is short')
    if '饮酒' in tg or age>=18: bad.append('minors')
    if '一次性' in tg or '剧本杀' in tg: bad.append('anyone who has already played the same script')
    if '资料待补' in tg: bad.append('(rules data incomplete — read the rulebook first)')
    return good or ['most board gamers'], bad or ['no obvious bad fit']
def slug(s):
    s=re.sub(r'[^A-Za-z0-9]+','_',s.split('(')[0]).strip('_')
    return s[:40] or 'game'
def enfile(i): return f'{i:02d}_{slug(EN[i]["n"])}.md'
