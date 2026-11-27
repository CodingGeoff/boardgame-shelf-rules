import sys,glob,os,json,re
sys.path.insert(0,'/home/user/site/meta')
import m1,m2,m3,m4,m5,m6
G=m1.G+m2.G+m3.G+m4.G+m5.G+m6.G
G.sort(key=lambda g:g[0])
BG='/home/user/boardgames'
def docfile(i):
    f=glob.glob(f'{BG}/{i:02d}_*.md')
    return os.path.basename(f[0])
LOC=json.load(open('/home/user/site/loc.json'))
WL={1:'入门',2:'轻度',3:'中度',4:'中重度',5:'重度'}
UNKNOWN_P={29,89,93,94,113,114,115,141,142,143,144,145,152,158,162,163,165}
def fit_text(g):
    i,name,mn,mx,best,t1,t2,age,w,tags,*_=g
    tg=set(tags.split())
    good=[];bad=[]
    if '双人' in tg or mx==2: good.append('情侣 / 两人对战')
    if mx>=8: good.append('人多的聚会')
    if '合作' in tg: good.append('喜欢合作、不想互相伤害的朋友')
    if tg&{'吹牛','嘴炮','谈判'}: good.append('爱聊天、爱演戏的朋友')
    if tg&{'推理','隐藏身份','阵营'}: good.append('喜欢推理、互相猜身份的朋友')
    if tg&{'儿童','亲子'} or (age<=6): good.append('带小朋友的家庭')
    if w>=4: good.append('想深度烧脑的老玩家')
    if w<=1 and '儿童' not in tg: good.append('新手破冰、长辈也能马上上手')
    if t2<=20: good.append('等人、饭前饭后的短时间')
    if tg&{'反应','敏捷','实时'}: good.append('喜欢手速和刺激的人')
    if w>=4: bad.append('只想轻松聊天的场合')
    if tg&{'吹牛','嘴炮','谈判','背叛','陷害'}: bad.append('不喜欢冲突或“坑人”的玩家')
    if tg&{'反应','敏捷','实时'}: bad.append('想安静慢慢思考的人')
    if t1>=90: bad.append('时间紧张的时候')
    if '饮酒' in tg or age>=18: bad.append('未成年人')
    if '一次性' in tg or '剧本杀' in tg: bad.append('已经玩过同一本的人')
    if '资料待补' in tg: bad.append('（规则资料不足，需要先读说明书）')
    return good or ['大多数桌游爱好者'], bad or ['暂无明显的不适合场景']
