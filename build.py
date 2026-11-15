# -*- coding: utf-8 -*-
"""生成「大明国家机器」页面：所有 SVG 坐标在这里计算，输出静态 index.html。

运行：python3 build.py   → 同目录下生成 index.html
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent


def f(v):
    """坐标格式化：整数不带小数点，其余保留一位。"""
    v = round(v, 1)
    return str(int(v)) if v == int(v) else str(v)


# ---------------------------------------------------------------- SVG 基础件

def defs(fig):
    out = ['<defs>']
    for key, cls in (('a', 'mk'), ('z', 'mkz'), ('q', 'mkq')):
        out.append(
            f'<marker id="{fig}-{key}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path class="{cls}" d="M0,0 L10,5 L0,10 z"/></marker>')
    out.append('</defs>')
    return ''.join(out)


def node(x, y, w, h, t, s=None, cls='', nid=None, tag=None, small=False):
    cx, cy = x + w / 2, y + h / 2
    attr = f' data-id="{nid}"' if nid else ''
    out = [f'<g class="n {cls}"{attr}>',
           f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="4"/>']
    tcls = 't sm' if small else 't'
    if s:
        out.append(f'<text class="{tcls}" x="{f(cx)}" y="{f(cy - 3)}">{t}</text>')
        out.append(f'<text class="s" x="{f(cx)}" y="{f(cy + 15)}">{s}</text>')
    else:
        out.append(f'<text class="{tcls}" x="{f(cx)}" y="{f(cy + 5)}">{t}</text>')
    if tag:
        tx, ty = x + w - 16, y - 8
        out.append(f'<g class="tag"><rect x="{f(tx - 10)}" y="{f(ty)}" width="20" height="16" rx="3"/>'
                   f'<text x="{f(tx)}" y="{f(ty + 12)}">{tag}</text></g>')
    out.append('</g>')
    return ''.join(out)


def edge(fig, d, cls='', mk='a', eid=None, label=None, lx=0, ly=0, anchor='middle',
         lcls='', start=False, end=True):
    attr = f' data-e="{eid}"' if eid else ''
    m = f' marker-end="url(#{fig}-{mk})"' if end else ''
    ms = f' marker-start="url(#{fig}-{mk})"' if start else ''
    out = f'<g class="eg"{attr}><path class="e {cls}" d="{d}"{m}{ms}/>'
    if label:
        out += f'<text class="el {lcls}" x="{f(lx)}" y="{f(ly)}" text-anchor="{anchor}">{label}</text>'
    return out + '</g>'


def svg(fig, w, h, aria, body):
    return (f'<svg class="svg" id="{fig}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            + defs(fig) + body + '</svg>')


# ---------------------------------------------------------------- 图 1：四个环节逐朝对比

def fig_eras():
    F = 'f1'
    W, H = 1020, 560
    cols = [130, 360, 590, 820]
    cw = 190
    heads = ['起草 · 拟议', '裁可 · 拍板', '审核 · 驳回', '执行']
    rows = [
        ('唐', '618–907 · 三省制', [
            ('box', 'xiang', '中书省', '起草诏敕', None),
            ('box', 'emp', '皇帝', '画敕裁可', None),
            ('box', 'xiang', '门下省', '审核 · 可封驳', '驳'),
            ('box', 'xiang', '尚书省 → 六部', '执行', None)]),
        ('宋', '960–1279 · 二府三司', [
            ('stack', [('中书门下 · 政务', 'xiang'), ('枢密院 · 军务', 'xiang')]),
            ('box', 'emp', '皇帝', '裁决', None),
            ('box', 'check', '给事中 · 台谏', '封驳 · 言事', '驳'),
            ('box', '', '六部 · 三司', '三司分掌财政', None)]),
        ('元', '1271–1368 · 一省制', [
            ('box', 'xiang', '中书省', '丞相总揽政务', None),
            ('box', 'emp', '皇帝', '裁决', None),
            ('box', 'ghost', '门下省已撤', '无制度性封驳', None),
            ('box', 'xiang', '中书省 → 六部', '六部隶属中书', None)]),
        ('明', '1380 年后 · 罢丞相', [
            ('box', 'weak', '内阁', '大学士正五品 · 票拟', None),
            ('stack', [('皇帝', 'emp'), ('司礼监 · 批红', 'nei')]),
            ('box', 'check', '六科给事中', '正七品 · 封还执奏', '驳'),
            ('box', '', '六部', '尚书正二品 · 直属皇帝', None)]),
        ('清', '1729 年后 · 军机处', [
            ('box', '', '军机处', '承旨 · 拟写谕旨', None),
            ('box', 'emp', '皇帝', '朱批奏折', None),
            ('box', 'ghost', '六科并入都察院', '1723 年后封驳名存实亡', None),
            ('box', '', '督抚 · 六部', '廷寄直达', None)]),
        ('民国', '1912 · 临时约法', [
            ('box', 'xiang', '国务院', '国务总理 · 国务员副署', None),
            ('stack', [('参议院 · 立法', ''), ('临时大总统 · 公布', '')]),
            ('box', 'check', '参议院 · 法院', '弹劾 · 独立审判', '驳'),
            ('box', '', '各部', '依法执行', None)]),
    ]
    b = []
    for i, hd in enumerate(heads):
        b.append(f'<text class="colh" x="{cols[i] + cw / 2}" y="22">{hd}</text>')
    b.append(f'<line class="rule" x1="0" y1="34" x2="{W}" y2="34"/>')
    top, rh = 40, 86
    for r, (era, sub, cells) in enumerate(rows):
        y0 = top + r * rh
        if era == '明':
            b.append(f'<rect class="rowhl" x="0" y="{y0 + 2}" width="{W}" height="{rh - 4}" rx="4"/>')
        if r:
            b.append(f'<line class="rule soft" x1="0" y1="{y0}" x2="{W}" y2="{y0}"/>')
        b.append(f'<text class="lane" x="10" y="{y0 + 40}">{era}</text>')
        b.append(f'<text class="lanes" x="10" y="{y0 + 60}">{sub}</text>')
        cy = y0 + 15 + 28
        for c, cell in enumerate(cells):
            x = cols[c]
            if cell[0] == 'box':
                _, cls, t, s, tag = cell
                b.append(node(x, y0 + 15, cw, 56, t, s, cls, tag=tag))
            else:
                (t1, c1), (t2, c2) = cell[1]
                b.append(node(x, y0 + 15, cw, 26, t1, None, c1, small=True))
                b.append(node(x, y0 + 45, cw, 26, t2, None, c2, small=True))
            if c < 3:
                b.append(edge(F, f'M{x + cw + 4},{cy} L{cols[c + 1] - 4},{cy}'))
    aria = ('六个朝代政令四个环节对比：唐朝三省长官都是宰相；宋朝相权分为政务和军务；元朝中书省一省独大；'
            '明朝废丞相，内阁只拟票、司礼监批红；清朝军机处只承旨，六科并入都察院；民国由国务院、参议院和法院分权。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 2：明代中央结构

def fig_court():
    F = 'f2'
    W, H = 1040, 480
    b = []
    # 厂卫分组框
    b.append('<rect class="grp z" x="130" y="110" width="220" height="70" rx="6"/>')
    b.append('<text class="grpl z" x="112" y="141"><tspan x="112">厂</tspan><tspan x="112" dy="16">卫</tspan></text>')
    # 第一排
    b.append(node(140, 24, 200, 56, '司礼监', '掌印 · 秉笔太监', 'nei', 'sl'))
    b.append(node(440, 24, 160, 56, '皇帝', '最终裁可', 'emp', 'emp'))
    b.append(node(700, 24, 200, 56, '内阁', '大学士 正五品', 'weak', 'ng'))
    # 第二排
    b.append(node(140, 120, 96, 50, '东厂', '太监提督', 'nei', 'dc'))
    b.append(node(244, 120, 96, 50, '锦衣卫', '亲军 · 1382', 'nei', 'jy'))
    b.append(node(440, 120, 160, 50, '中书省 · 丞相', '1380 年撤销', 'ghost', 'ghost'))
    b.append('<line class="strike" x1="470" y1="141" x2="570" y2="141"/>')
    b.append(node(700, 120, 150, 50, '通政司', '正三品 · 收章疏', '', 'tz'))
    b.append(node(870, 120, 160, 50, '翰林院', '阁臣多由此出', '', 'hl'))
    # 第三排
    b.append(node(140, 212, 180, 48, '北镇抚司 · 诏狱', '奉旨拿问 · 不经法司', 'nei', 'zy'))
    b.append(node(330, 212, 440, 48, '六科给事中 · 正七品', '封还执奏 · 抄发章疏 · 稽察六部', 'check', 'lk'))
    # 六部
    bu = [('吏部', 'li'), ('户部', 'hu'), ('礼部', 'lii'), ('兵部', 'bing'), ('刑部', 'xing'), ('工部', 'gong')]
    for i, (name, key) in enumerate(bu):
        b.append(node(330 + i * 74, 300, 66, 48, name, '正二品', '', f'bu bu-{key}'))
    b.append(node(820, 300, 200, 48, '都察院', '都御史正二品 · 御史110人', 'check', 'dcy'))
    b.append(node(60, 300, 200, 48, '五军都督府', '左右都督 正一品', '', 'wf'))
    b.append(node(820, 410, 200, 48, '大理寺', '卿 正三品 · 驳正', '', 'dl'))

    b.append(edge(F, 'M700,52 L604,52', eid='ng-emp', label='票拟 · 墨书小票', lx=652, ly=44))
    b.append(edge(F, 'M440,52 L344,52', 'z', 'z', 'emp-sl', '照阁票批朱', 392, 44, lcls='z'))
    b.append(edge(F, 'M188,80 L188,116', 'z', 'z', 'sl-dc', '提督', 196, 104, 'start', 'z'))
    b.append(edge(F, 'M462,80 L302,117', 'z', 'z', 'emp-jy', '直属', 388, 92, 'start', 'z'))
    b.append(edge(F, 'M720,120 L606,74', eid='tz-emp', label='章疏进呈', lx=606, ly=113, anchor='start'))
    b.append(edge(F, 'M950,120 L892,84', eid='hl-ng', label='入阁', lx=938, ly=100, anchor='start'))
    b.append(edge(F, 'M520,80 L520,208', eid='emp-lk', label='1380 年后直达', lx=528, ly=198, anchor='start'))
    b.append(edge(F, 'M188,170 L188,208', 'z', 'z', 'dc-zy'))
    b.append(edge(F, 'M292,170 L292,208', 'z', 'z', 'jy-zy'))
    six = ''.join(f'<path class="e q" d="M{363 + i * 74},260 L{363 + i * 74},296" marker-end="url(#f2-q)"/>' for i in range(6))
    b.append(f'<g class="eg" data-e="lk-bu">{six}<text class="el q" x="778" y="284" text-anchor="start">一科对一部</text></g>')
    b.append(edge(F, 'M820,324 L770,324', 'q', 'q', 'dcy-bu', '纠劾', 795, 316, lcls='q'))
    b.append(edge(F, 'M585,348 L585,392 L160,392 L160,348', 'd', eid='bing-wf',
                  label='兵部调兵 · 五府统兵', lx=372, ly=386, end=False))
    b.append(edge(F, 'M659,348 L659,434 L816,434', eid='sanfa', label='三法司', lx=738, ly=426, end=False))
    b.append(edge(F, 'M920,348 L920,406', eid='sanfa2', end=False))
    aria = ('明代中央机构图：皇帝两侧是内阁（票拟）和司礼监（批红）；中书省已撤销，皇帝直接管六科和六部；'
            '六科一科对一部稽察；都察院纠劾百官；刑部、都察院、大理寺合称三法司；兵部调兵与五军都督府统兵分离；'
            '东厂、锦衣卫和北镇抚司诏狱直属皇帝。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 3：奏章的旅程

def fig_memorial():
    F = 'f3'
    W, H = 1010, 340
    xs = [20, 186, 352, 518, 684, 850]
    w, y, h = 136, 120, 56
    spec = [('s1', '上疏', '京官 · 督抚 · 题本', ''),
            ('s2', '通政司', '登记 · 封进御前', ''),
            ('s3', '内阁', '票拟 · 墨书小票', 'weak'),
            ('s4', '皇帝 / 司礼监', '朱笔批红', 'emp'),
            ('s5', '六科', '抄发 · 可封驳', 'check'),
            ('s6', '六部 · 各衙门', '照旨执行', '')]
    b = []
    for (nid, t, s, cls), x in zip(spec, xs):
        b.append(node(x, y, w, h, t, s, cls, nid))
    b.append(node(526, 250, 120, 40, '留中', '不批不发 · 搁置', 'ghost', 'lz'))
    for i in range(5):
        b.append(edge(F, f'M{xs[i] + w + 2},{y + 28} L{xs[i + 1] - 4},{y + 28}', eid=f'e{i + 1}{i + 2}'))
    b.append(edge(F, 'M560,120 C560,76 420,76 420,116', 'z d', 'z', 'back34', '不同意 · 发还改票', 490, 70, lcls='z'))
    b.append(edge(F, 'M752,120 C752,76 612,76 612,116', 'q d', 'q', 'back54', '封还执奏', 682, 70, lcls='q'))
    b.append(edge(F, 'M586,176 L586,246', 'z d', 'z', 'e4lz'))
    b.append(edge(F, 'M918,176 L918,214 L770,214 L770,180', 'q dot', 'q', 'k65', '考成法：按月注销', 844, 207, lcls='q'))
    b.append(edge(F, 'M720,176 L720,310 L404,310 L404,180', 'q dot', 'q', 'k53', '六科稽核后报内阁', 562, 328, lcls='q'))
    aria = ('一份奏章的旅程：上疏，经通政司封进，内阁票拟，皇帝或司礼监批红，六科抄发，六部执行。'
            '皇帝可发还改票或留中，六科可封还执奏；考成法增加了六部向六科、六科向内阁的稽核回路。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 4：统兵与调兵

def fig_army():
    F = 'f4'
    W, H = 1000, 320
    b = []
    b.append(node(420, 16, 160, 48, '皇帝', '命将 · 授印', 'emp'))
    b.append(node(40, 110, 220, 56, '五军都督府', '武官 · 管军籍操练 · 正一品'))
    b.append(node(390, 110, 220, 56, '兵部', '文官 · 武选调兵 · 尚书正二品'))
    b.append(node(740, 110, 220, 56, '总兵官', '战时命将 · 无品级无定员', 'temp'))
    b.append(node(40, 250, 160, 56, '都指挥使司', '16 都司 · 5 行都司'))
    b.append(node(230, 250, 160, 56, '卫', '约 5,600 人 · 全国 493'))
    b.append(node(420, 250, 160, 56, '千户所', '约 1,120 人'))
    b.append(node(610, 250, 160, 56, '百户所', '112 人 · 总旗2 小旗10'))
    b.append(edge(F, 'M440,64 L204,108'))
    b.append(edge(F, 'M500,64 L500,106'))
    b.append(edge(F, 'M560,64 L796,107', 'z', 'z', label='命将', lx=690, ly=80, lcls='z'))
    b.append(edge(F, 'M120,166 L120,246', label='日常统辖', lx=128, ly=212, anchor='start'))
    b.append(edge(F, 'M500,166 L500,246', 'd', label='发勘合调兵', lx=508, ly=212, anchor='start'))
    for x in (200, 390, 580):
        b.append(edge(F, f'M{x + 2},278 L{x + 26},278'))
    b.append(edge(F, 'M772,278 L850,278 L850,170', 'z d', 'z', label='出征 · 战毕回卫',
                  lx=858, ly=232, anchor='start', lcls='z', start=True))
    b.append(edge(F, 'M900,110 L900,40 L584,40', 'z d', 'z', label='战毕缴印', lx=742, ly=33, lcls='z'))
    aria = ('明代军权分离：五军都督府日常统辖都司和卫所，兵部发勘合调兵，皇帝临时命将为总兵官，'
            '卫所官军出征归总兵指挥，战毕缴印、官军各回卫所。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 5：地方

def fig_province():
    F = 'f5'
    W, H = 1000, 600
    b = []
    b.append(node(70, 14, 180, 46, '六部', '户部钱粮 · 吏部铨选'))
    b.append(node(340, 14, 180, 46, '刑部 · 都察院', '刑名 · 监察', 'check'))
    b.append(node(610, 14, 180, 46, '五府 · 兵部', '统兵 · 调兵'))
    b.append(node(830, 14, 160, 46, '巡按御史', '都察院差出 · 正七品', 'check'))
    # 督抚框
    b.append('<rect class="grp q" x="30" y="124" width="800" height="160" rx="6"/>')
    b.append('<text class="grpl q big" x="46" y="148">巡抚 · 总督</text>')
    b.append('<text class="grps" x="174" y="148">中央派出 · 挂都御史衔 · 节制三司</text>')
    b.append(node(70, 166, 180, 58, '承宣布政使司', '民政财赋 · 布政使从二品'))
    b.append(node(340, 166, 180, 58, '提刑按察使司', '刑名监察 · 按察使正三品'))
    b.append(node(610, 166, 180, 58, '都指挥使司', '军政 · 都指挥使正二品'))
    b.append('<text class="cap" x="295" y="268">三司互不统属，各自对口中央</text>')
    b.append(edge(F, 'M160,60 L160,162'))
    b.append(edge(F, 'M430,60 L430,162'))
    b.append(edge(F, 'M700,60 L700,162'))
    b.append(edge(F, 'M480,60 L480,120', 'q d', 'q', label='派出', lx=488, ly=96, anchor='start', lcls='q'))
    # 巡按监察线（竖排标签）
    b.append(edge(F, 'M910,60 L910,195 L834,195', 'q d', 'q'))
    vt = ''.join(f'<tspan x="924" dy="{0 if i == 0 else 15}">{ch}</tspan>' for i, ch in enumerate('代天子巡狩'))
    b.append(f'<text class="el q" x="924" y="92">{vt}</text>')
    # 民政线
    b.append(node(70, 316, 180, 46, '府 · 140', '知府 正四品'))
    b.append(node(70, 392, 180, 46, '州 193 · 县 1,138', '知州从五品 · 知县正七品'))
    b.append(node(70, 468, 180, 46, '里 · 69,556', '每里 110 户'))
    b.append(node(70, 544, 180, 46, '甲 · 10 户', '甲首轮役 · 黄册十年一造'))
    b.append(edge(F, 'M160,224 L160,312'))
    for y1, y2 in ((362, 388), (438, 464), (514, 540)):
        b.append(edge(F, f'M160,{y1} L160,{y2}'))
    b.append('<text class="el" x="262" y="496">= 里长 10 户 + 10 甲 × 10 户</text>')
    # 道与直隶
    b.append(node(340, 316, 180, 46, '分守道 · 分巡道', '两司派出 · 督察府州'))
    b.append(edge(F, 'M430,224 L430,312'))
    b.append(edge(F, 'M340,339 L254,339', 'd', label='督察', lx=297, ly=331))
    b.append(node(340, 400, 180, 56, '南、北直隶', '府州直属六部 · 不设布政司', 'ghost'))
    # 军政线
    b.append(node(610, 316, 180, 46, '卫 · 493', '每卫约 5,600 人'))
    b.append(node(610, 392, 180, 46, '所 · 2,593', '另有守御千户所 315'))
    b.append(node(610, 468, 180, 46, '军户 · 世袭', '屯田自养（设计）'))
    b.append(edge(F, 'M700,224 L700,312'))
    for y1, y2 in ((362, 388), (438, 464)):
        b.append(edge(F, f'M700,{y1} L700,{y2}'))
    aria = ('明代地方结构：中央六部、刑部与都察院、五府与兵部分别对口布政使司、按察使司、都指挥使司；'
            '巡抚总督由中央派出节制三司；巡按御史监察全省。民政线为府140、州193、县1138、里69556、甲；'
            '军政线为卫493、所2593、军户。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 6：司法

def fig_justice():
    F = 'f6'
    W, H = 1004, 344
    xs = [10, 154, 298, 442, 586, 730, 874]
    spec = [('里老人', '户婚田土 · 先调处', ''), ('州县', '笞杖 · 自理', ''), ('府', '审转', ''),
            ('按察司', '徒流 · 复审', ''), ('刑部', '死罪 · 审拟', ''), ('大理寺', '驳正 · 复核', ''),
            ('皇帝', '覆奏 · 勾决', 'emp')]
    b = []
    for (t, s, cls), x in zip(spec, xs):
        b.append(node(x, 150, 120, 56, t, s, cls))
    for i in range(6):
        b.append(edge(F, f'M{xs[i] + 122},178 L{xs[i + 1] - 4},178'))
    b.append(node(586, 56, 264, 48, '都察院', '纠察 · 与刑部、大理寺合称三法司', 'check'))
    b.append(edge(F, 'M646,104 L646,146', 'q d', 'q'))
    b.append(edge(F, 'M790,104 L790,146', 'q d', 'q'))
    b.append(node(298, 56, 264, 48, '巡按御史', '出巡录囚 · 审录冤滞', 'check temp'))
    b.append(edge(F, 'M358,104 L358,146', 'q d', 'q'))
    b.append(edge(F, 'M502,104 L502,146', 'q d', 'q'))
    b.append('<text class="el z" x="10" y="250">侧门：洪武二十六年曾诏“内外狱毋得上锦衣卫”，永乐起复用</text>')
    b.append(node(586, 272, 264, 56, '东厂 · 锦衣卫', '缉访 · 奉旨拿人', 'nei'))
    b.append(node(298, 272, 264, 56, '北镇抚司诏狱', '刑讯 · 定案', 'nei'))
    b.append(node(10, 272, 264, 56, '结案 · 廷杖', '不经三法司', 'nei'))
    b.append(edge(F, 'M934,206 L934,300 L854,300', 'z', 'z', label='密旨', lx=942, ly=258, anchor='start', lcls='z'))
    b.append(edge(F, 'M586,300 L566,300', 'z', 'z'))
    b.append(edge(F, 'M298,300 L278,300', 'z', 'z'))
    aria = ('明代司法两条路：正门从里老人调处、州县、府、按察司、刑部、大理寺到皇帝勾决，都察院纠察、巡按录囚；'
            '侧门由皇帝密旨交东厂锦衣卫拿人，入北镇抚司诏狱，不经三法司。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 7：一条鞭法

def fig_tax():
    F = 'f7'
    W, H = 1000, 244
    items = [('田赋 · 夏税秋粮', '按亩交米麦等实物'), ('里甲正役', '按户轮充，十年一轮'),
             ('均徭 · 杂泛差役', '按丁、按户派劳役'), ('上供物料', '按地方摊派实物')]
    b = []
    for i, (t, s) in enumerate(items):
        y = 16 + i * 56
        b.append(node(30, y, 300, 44, t, s))
        b.append(edge(F, f'M332,{y + 22} C430,{y + 22} 430,130 520,130', end=False))
    b.append(edge(F, 'M520,130 L636,130', label='合并折银', lx=578, ly=121))
    b.append('<g class="n silver"><rect x="640" y="72" width="330" height="116" rx="4"/>'
             '<text class="t big" x="805" y="118">一条银</text>'
             '<text class="s" x="805" y="142">按田亩征银 · 官府出钱雇役</text>'
             '<text class="s" x="805" y="162">嘉靖年间各地试行 · 1581 年通行全国</text></g>')
    aria = '一条鞭法：田赋实物、里甲正役、均徭杂役、上供物料四类负担，合并折成白银，按田亩征收，官府出钱雇役。'
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 图 8：时间线

def fig_timeline():
    F = 'f8'
    W, H = 1040, 236
    X = lambda yr: 40 + (yr - 1368) * 960 / 276
    reigns = [('洪武', 1368), ('', 1399), ('永乐', 1403), ('', 1425), ('宣德', 1426), ('正统', 1436),
              ('景泰', 1450), ('', 1457), ('成化', 1465), ('弘治', 1488), ('正德', 1506), ('嘉靖', 1522),
              ('', 1567), ('万历', 1573), ('', 1620), ('崇祯', 1628), (None, 1644)]
    b = []
    band_y, band_h = 112, 24
    for i in range(len(reigns) - 1):
        name, y1 = reigns[i]
        y2 = reigns[i + 1][1]
        x1, x2 = X(y1), X(y2)
        cls = 'band a' if i % 2 == 0 else 'band b'
        b.append(f'<rect class="{cls}" x="{f(x1)}" y="{band_y}" width="{f(x2 - x1)}" height="{band_h}"/>')
        if name:
            b.append(f'<text class="bandl" x="{f((x1 + x2) / 2)}" y="{band_y + 16}">{name}</text>')
    # 上方行（离色带由近到远）与下方行
    up = {1: 92, 2: 70, 3: 48, 4: 26}
    dn = {1: 160, 2: 182}
    ev = [
        (1368, '1368 建国', 'u', 4, []),
        (1376, '1376–82 布政司 · 废相 · 里甲 · 锦衣卫', 'u', 3, [1380, 1381, 1382]),
        (1397, '1397 大明律', 'u', 2, []),
        (1402, '1402 内阁', 'u', 1, []),
        (1420, '1420 东厂', 'd', 2, []),
        (1426, '1426 内书堂', 'd', 1, []),
        (1449, '1449 土木之变', 'u', 1, []),
        (1459, '1459 朝审', 'd', 1, []),
        (1477, '1477 西厂', 'u', 1, []),
        (1500, '1500 问刑条例', 'u', 1, []),
        (1573, '1573 考成法', 'u', 2, []),
        (1581, '1581 一条鞭法', 'd', 1, []),
        (1587, '1587 万历十五年', 'u', 1, []),
        (1644, '1644 明亡', 'u', 1, []),
    ]
    for yr, label, side, row, extra in ev:
        x = X(yr)
        hot = ' z' if yr == 1587 else ''
        t1, t2 = (band_y, band_y + 7) if side == 'u' else (band_y + band_h - 7, band_y + band_h)
        for e in [yr] + extra:
            b.append(f'<line class="tick{hot}" x1="{f(X(e))}" y1="{t1}" x2="{f(X(e))}" y2="{t2}"/>')
        anchor = 'end' if yr == 1644 else 'start'
        tx = x if yr != 1644 else x
        if side == 'u':
            ly = up[row]
            b.append(f'<line class="stem{hot}" x1="{f(x)}" y1="{band_y}" x2="{f(x)}" y2="{ly + 4}"/>')
            b.append(f'<text class="evl{hot}" x="{f(tx + (3 if anchor == "start" else -3))}" y="{ly}" text-anchor="{anchor}">{label}</text>')
        else:
            ly = dn[row]
            b.append(f'<line class="stem{hot}" x1="{f(x)}" y1="{band_y + band_h}" x2="{f(x)}" y2="{ly - 12}"/>')
            b.append(f'<text class="evl{hot}" x="{f(tx + 3)}" y="{ly}" text-anchor="start">{label}</text>')
    for yr in (1400, 1450, 1500, 1550, 1600):
        b.append(f'<text class="axis" x="{f(X(yr))}" y="222">{yr}</text>')
        b.append(f'<line class="axt" x1="{f(X(yr))}" y1="{band_y + band_h}" x2="{f(X(yr))}" y2="{band_y + band_h + 4}"/>')
    aria = ('明代制度时间线 1368–1644：主要制度集中在洪武朝 1376–1397 年设立，此后为内阁 1402、东厂 1420、'
            '内书堂 1426、西厂 1477、问刑条例 1500、考成法 1573、一条鞭法 1581，万历十五年为 1587 年。')
    return svg(F, W, H, aria, ''.join(b))


# ---------------------------------------------------------------- 组装

def main():
    tpl = (HERE / 'template.html').read_text(encoding='utf-8')
    figs = {
        '%%FIG_ERAS%%': fig_eras(),
        '%%FIG_COURT%%': fig_court(),
        '%%FIG_MEMORIAL%%': fig_memorial(),
        '%%FIG_ARMY%%': fig_army(),
        '%%FIG_PROVINCE%%': fig_province(),
        '%%FIG_JUSTICE%%': fig_justice(),
        '%%FIG_TAX%%': fig_tax(),
        '%%FIG_TIMELINE%%': fig_timeline(),
    }
    for k, v in figs.items():
        assert k in tpl, k
        tpl = tpl.replace(k, v)
    (HERE / 'index.html').write_text(tpl, encoding='utf-8')
    print('wrote', HERE / 'index.html', len(tpl), 'bytes')
    publish(tpl)


# ---------------------------------------------------------------- GitHub Pages 公开版

DESC = ('从唐到近代的中国政治制度演变，重点拆解明朝的中枢、奏章流转、军事、地方、司法、赋役六套机制，'
        '可点《万历十五年》人物看他们在体制中的位置。')
BASE_STYLE = ('<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);'
              'padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font-size:14px}'
              'img{max-width:100%}[hidden]{display:none!important}</style>')


def publish(page):
    """Artifact 版没有 doctype/head/body（由宿主补），这里包成完整文档写到 docs/，供 GitHub Pages 发布。"""
    cut = page.index('</style>') + len('</style>')
    head, body = page[:cut], page[cut:]
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    html = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="{DESC}">\n'
            '<meta property="og:title" content="大明国家机器">\n'
            f'<meta property="og:description" content="{DESC}">\n'
            f'{BASE_STYLE}\n{head}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n')
    out = HERE / 'docs'
    out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')
    (out / '.nojekyll').write_text('', encoding='utf-8')
    print('wrote', out / 'index.html')


if __name__ == '__main__':
    main()
