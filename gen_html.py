# -*- coding: utf-8 -*-
"""Generate the three self-contained HTML exam pages (9 sections each)."""
import os, html

BASE = os.path.dirname(os.path.abspath(__file__))
EXAM_DIRS = {1: "试卷一测试集", 2: "试卷二测试集", 3: "试卷三测试集"}

GRAD = {1: 1, 2: 1, 3: 1,
        4: 2, 5: 2, 6: 2, 7: 2,
        8: 3, 9: 3}
GRAD_NAME = {1: "基础巩固", 2: "能力提升", 3: "极限挑战"}

# Each problem: (title, body_html, input_desc, output_desc)
EXAMS = {
1: [
 ("括号嵌套的类型推导",
  "给定一个只包含 <code>char</code>、<code>int</code>、<code>float</code>、<code>double</code>、<code>longlong</code> 以及加法 <code>+</code> 运算符的合法表达式，表达式中允许出现括号 <code>()</code>。请判断该表达式最终运算结果的数据类型。<br>规则：括号只改变优先级，不改变类型推导；运算时类型向上转换，结果取两者中“更高”的类型。类型由低到高为：<code>char &lt; int &lt; float &lt; double &lt; longlong</code>。由于只有加法，最终类型就是表达式中出现的最高类型。",
  "一行，一个合法表达式（无空格），长度不超过 1000。",
  "一行，结果类型的字符串。"),
 ("动态步长模拟（生命值）",
  "小P 从坐标 0 出发，每秒向坐标增大的方向前进 1 个单位，必须到达终点 D。他初始血量为 H，最大血量也为 H。<br>游戏中有 N 个泉水，第 i 个泉水位于整数坐标 X<sub>i</sub>（互不相同，均在 1 到 D 之间），回复量为 V<sub>i</sub>。<br>小P 从坐标 0 开始，依次经过坐标 1, 2, …, D：每移动一步（到达下一个坐标）先扣除 1 点血量；若扣除后血量 ≤ 0，则小P 死亡；若到达的坐标恰好有泉水，则立即回复 V<sub>i</sub> 点血量（不超过最大血量 H）。<br>请计算小P 到达终点 D 时的血量；若中途死亡则输出 -1。",
  "第一行三个整数 H, D, N。第二行 N 对整数 X<sub>i</sub> V<sub>i</sub>（保证互不相同）。",
  "一行，到达终点时的血量（整数）；若死亡输出 -1。"),
 ("字符串的 Z 变换（之字形分行）",
  "给定一个字符串 S 和行数 R。请先将 S 的字符按字母表顺序重新排序，然后以“之”字形（Z 字形）填入 R 行的网格中：第一个字符放在第 1 行，之后逐行下移，到达第 R 行后逐行上移，如此往复（行号变化为 1→2→…→R→R-1→…→1→2→…）。<br>最后按行输出：每一行按填入顺序拼接成一个字符串，共 R 行（每行一个字符串，不含多余空格）。",
  "第一行字符串 S（仅小写字母）。第二行整数 R（R ≥ 1）。",
  "R 行，每行一个字符串。"),
 ("区间合并与最大重叠",
  "数轴上有 N 条线段，第 i 条覆盖闭区间 [L<sub>i</sub>, R<sub>i</sub>]。你可以选择任意一个点 P，并将所有包含点 P 的线段合并成一条大线段（这些线段因都含 P，其并集仍是一条连续线段，左端点为其中最小的 L，右端点为其中最大的 R）。<br>求合并后大线段的最大可能长度。等价地，最大化 (max R<sub>i</sub> − min L<sub>i</sub>)，其中 i 取遍所有覆盖某个公共点 P 的线段。",
  "第一行整数 N。接下来 N 行，每行两个整数 L<sub>i</sub> R<sub>i</sub>。",
  "一行，最大长度（整数）。"),
 ("走迷宫的最少步数",
  "给定一个 N×M 的网格，<code>#</code> 表示障碍，<code>.</code> 表示可通行。起点为左上角 (1,1)，终点为右下角 (N,M)，保证这两个格子均可通行。<br>每次操作消耗 1 点，可以是：<br>① 向上下左右移动一步到相邻的可通行格子；<br>② 传送到当前行的两端之一，即 (x,y) → (x,1) 或 (x,y) → (x,M)；<br>③ 传送到当前列的两端之一，即 (x,y) → (1,y) 或 (x,y) → (N,y)。<br>求从起点到终点的最少操作次数；若无法到达输出 -1。",
  "第一行两个整数 N, M。接下来 N 行，每行 M 个字符（<code>#</code> 或 <code>.</code>）。",
  "一行，最少操作次数；无法到达输出 -1。"),
 ("进制转换与小数精度",
  "给定一个十进制数 D（可能含小数部分，以字符串形式给出）和一个目标进制 K（2 ≤ K ≤ 16）。请将 D 转换为 K 进制。<br>整数部分用 K 进制表示（大于 9 的数字用大写字母 A–F）；小数部分采用“乘基取整”法：若能在有限步内除尽，则输出精确的小数部分；若小数部分无限循环，则保留小数点后 8 位（直接截断，不四舍五入）。若 D 没有小数部分，则不输出小数点。",
  "第一行字符串 D。第二行整数 K。",
  "一行，K 进制表示的字符串。"),
 ("贪心排队问题（最小平均等待时间）",
  "有 N 个人排队打水，第 i 个人打水需要 T<sub>i</sub> 分钟。只有 1 个水龙头。你可以把队伍切成若干段，每一段内部可以任意重新排序，规则是每一段内打水时间短的人优先（即每一段都按打水时间升序打水）。<br>求所有人的平均等待时间的最小值（等待时间 = 从开始打水到该人打完水的时间）。输出保留两位小数。",
  "第一行整数 N。第二行 N 个整数 T<sub>i</sub>。",
  "一行，最小平均等待时间（保留两位小数）。"),
 ("矩阵路径最大异或和",
  "给定一个 N×M 的矩阵，每个格子里有一个非负整数（0 ≤ a[i][j] &lt; 2<sup>31</sup>）。从左上角 (1,1) 走到右下角 (N,M)，每次只能向右或向下走一步。路径上所有数字做异或（XOR）运算。<br>求所有可能路径中异或和的最大值。数据范围：1 ≤ N, M ≤ 12。",
  "第一行两个整数 N, M。接下来 N 行，每行 M 个整数。",
  "一行，最大异或和（整数）。"),
 ("模拟大数除法（高精除以低精）",
  "给定一个非负大整数 A（十进制字符串，长度不超过 100）和一个正整数 B（1 ≤ B ≤ 10<sup>18</sup>）以及一个非负整数 K（K ≤ 1000）。计算 A ÷ B 的商，精确到小数点后 K 位（直接截断，不四舍五入）。<br>若 K = 0 则不输出小数部分。",
  "第一行字符串 A。第二行整数 B。第三行整数 K。",
  "一行，商（含小数点后 K 位）。"),
],
2: [
 ("滑动窗口最大值",
  "给定一个长度为 N 的整数数组和一个大小为 K 的滑动窗口。窗口从最左端移动到最右端，每次向右移动一格。对每个窗口位置，输出窗口内元素的最大值。<br>数据范围：1 ≤ N ≤ 10<sup>5</sup>，要求 O(N) 算法（单调队列）。",
  "第一行两个整数 N, K。第二行 N 个整数。",
  "一行，N-K+1 个整数，为每个窗口的最大值（空格分隔）。"),
 ("跳跃游戏（最少跳跃次数）",
  "给定一个非负整数数组，初始位于第 1 个位置。数组中的每个元素代表你在该位置可以跳跃的最大长度。判断能否到达最后一个位置，并输出到达最后一个位置所需的最少跳跃次数；若无法到达输出 -1。<br>数据范围：1 ≤ N ≤ 10<sup>5</sup>。",
  "第一行整数 N。第二行 N 个整数。",
  "一行，最少跳跃次数；无法到达输出 -1。"),
 ("字符串回文分割",
  "给定一个字符串 S，将其分割成若干子串，使得每个子串都是回文串。输出所有可能的分割方案，按字典序排列（每行一个方案，同一方案内的子串用 <code>|</code> 分隔）。<br>数据范围：|S| ≤ 10。",
  "一行，字符串 S（仅小写字母）。",
  "若干行，每行一个分割方案（子串以 <code>|</code> 连接），按字典序升序。"),
 ("区间反转与查询",
  "给定一个 1 到 N 的排列（初始为 1,2,…,N）。进行 M 次操作：<br>操作 1：<code>1 L R</code>，将区间 [L, R] 内的元素反转；<br>操作 2：<code>2 X</code>，查询当前位于位置 X 上的值。<br>每次查询操作输出一行结果。<br>数据范围：1 ≤ N, M ≤ 10<sup>5</sup>，要求使用平衡树（如 Splay / Treap）等 O(log N) 结构。",
  "第一行两个整数 N, M。接下来 M 行，每行一个操作（格式见上）。",
  "若干行，每次查询操作的结果。"),
 ("复杂的 DNA 序列编辑距离",
  "给定两个 DNA 序列 A 和 B（由字符 ACGT 组成）。你可以对 A 进行三种操作：插入一个字符、删除一个字符、替换一个字符，每次操作计 1。求将 A 变为 B 的最少操作次数（编辑距离）。",
  "第一行字符串 A。第二行字符串 B。",
  "一行，最少操作次数（整数）。"),
 ("分数转换（循环小数）",
  "给定两个正整数 A 和 B，输出 A/B 的小数形式。若存在循环节，用括号将其括起来。例如 1/3 = <code>0.(3)</code>，1/6 = <code>0.1(6)</code>，1/2 = <code>0.5</code>，2/1 = <code>2</code>。",
  "一行两个正整数 A, B。",
  "一行，格式化的小数/整数字符串。"),
 ("处理带优先级的运算（表达式求值）",
  "给定一个合法的数学表达式（只含非负整数、<code>+</code>、<code>-</code>、<code>*</code>、<code>/</code>，不含括号）。其中 <code>*</code> 和 <code>/</code> 的优先级高于 <code>+</code> 和 <code>-</code>，同优先级从左到右计算。除法为整数除法（向零截断）。求表达式的结果。",
  "一行，表达式字符串（无空格）。",
  "一行，计算结果（整数）。"),
 ("树的直径",
  "给定一棵包含 N 个节点的树，节点编号 1 到 N，每条边有一个非负权值。求树上距离最远的两个节点之间的距离（树的直径）。<br>数据范围：1 ≤ N ≤ 10<sup>5</sup>，边权 ≤ 10<sup>4</sup>。",
  "第一行整数 N。接下来 N-1 行，每行三个整数 u, v, w，表示一条连接 u 和 v、权值为 w 的边。",
  "一行，最远距离（整数）。"),
 ("最长递增子序列的方案数",
  "给定一个长度为 N 的数组，求最长严格递增子序列（LIS）的长度，以及该长度下不同 LIS 的方案数（两个子序列方案不同当且仅当它们取出的数值序列不同）。方案数对 10<sup>9</sup>+7 取模。<br>数据范围：1 ≤ N ≤ 5000。",
  "第一行整数 N。第二行 N 个整数。",
  "一行两个整数：LIS 长度 和 方案数（模 10<sup>9</sup>+7）。"),
],
3: [
 ("平面上的相交线段",
  "给定二维平面上的两条线段 AB 和 CD（端点坐标为整数）。判断它们是否相交（包含端点相接、共线重叠等情况）。",
  "第一行四个整数 x<sub>A</sub> y<sub>A</sub> x<sub>B</sub> y<sub>B</sub>。<br>第二行四个整数 x<sub>C</sub> y<sub>C</sub> x<sub>D</sub> y<sub>D</sub>。",
  "一行，相交输出 <code>YES</code>，否则输出 <code>NO</code>。"),
 ("寻找缺失的正整数",
  "给定一个包含 n 个整数的数组（元素可能包含负数、0 和重复值）。请找出其中没有出现过的、最小的正整数。<br>要求：时间复杂度 O(n)，额外空间复杂度 O(1)（原地哈希，利用数组下标）。",
  "第一行整数 n。第二行 n 个整数。",
  "一行，缺失的最小正整数。"),
 ("字符串压缩与解压",
  "小P 的压缩规则：遍历字符串，若连续出现 k 个相同的字符 c（k ≥ 2），则压缩为 <code>c</code> 加上数字 k（如 <code>aaa</code> → <code>a3</code>，<code>12</code> 个 a → <code>a12</code>）；若只出现 1 次，则直接保留该字符不加数字。<br>现在给定一个合法的压缩字符串（仅由字母和数字组成，且原始字符串只含字母），请将其解压还原。注意数字可以是多位数。",
  "一行，合法的压缩字符串。",
  "一行，还原后的原始字符串。"),
 ("石头剪刀布的博弈",
  "小P 和小Q 进行 N 局石头剪刀布。小P 每局出的字符已知（字符串 S<sub>p</sub> 由 R/P/S 组成，R=石头，P=布，S=剪刀）。小Q 的出战顺序未知，但已知小Q 一共出了 R 次石头、P 次布、S 次剪刀（R+P+S=N）。<br>请你安排小Q 的出战顺序，使得小Q 获胜的局数最多，输出这个最多获胜局数。",
  "第一行四个整数 N, R, P, S。第二行字符串 S<sub>p</sub>。",
  "一行，小Q 最多能赢的局数。"),
 ("并查集：连通块查询",
  "给定一个 N×M 的网格地图，<code>#</code> 代表陆地，<code>.</code> 代表海洋，上下左右相邻的陆地构成同一个岛屿。初始地图给定后，依次进行 Q 次操作，每次把一个海洋格子变成陆地 <code>#</code>。请在每次操作后，输出当前地图上岛屿的数量。",
  "第一行两个整数 N, M。接下来 N 行，每行 M 个字符。下一行一个整数 Q。接下来 Q 行，每行两个整数 x, y（把该格变为陆地）。",
  "Q 行，每行表示对应操作后的岛屿数量。"),
 ("矩阵旋转与查询",
  "给定一个 N×N 的矩阵。进行 K 次操作，操作分两种：<br><code>1 x y</code>：查询当前矩阵中 (x, y) 位置的值；<br><code>2 r</code>：将整个矩阵顺时针旋转 90 度（旋转累计，r 为旋转次数，等价于 r mod 4 次）。<br>请输出每次查询操作的结果。<br>提示：不要真的旋转矩阵，应推导坐标映射公式。",
  "第一行两个整数 N, K。接下来 N 行，每行 N 个整数。接下来 K 行，每行一个操作。",
  "若干行，每次查询操作的结果。"),
 ("阶乘末尾的零（任意进制）",
  "给定一个正整数 N 和一个进制 B（2 ≤ B ≤ 10）。求 N!（N 的阶乘）在 B 进制表示下末尾连续 0 的个数。<br>提示：对 B 做质因数分解，结合勒让德定理计算每个质因子在 N! 中的幂次，取限制最紧者。",
  "一行两个整数 N, B。",
  "一行，末尾 0 的个数（整数）。"),
 ("位运算的最短路径",
  "给定起始整数 S 和目标整数 T。你可以对当前数进行三种操作：① 乘以 2；② 与 1 做按位异或（XOR 1）；③ 左移 3 位（×8）。求使 S 变成 T 的最少操作次数；若无法达到输出 -1。<br>数据范围：0 ≤ S, T ≤ 10<sup>9</sup>。",
  "一行两个整数 S, T。",
  "一行，最少操作次数；无法达到输出 -1。"),
 ("区间覆盖（选点问题）",
  "给定数轴上的 N 个闭区间 [L<sub>i</sub>, R<sub>i</sub>]。请你选择尽可能少的点，使得每个区间内至少包含一个选中的点。输出所选点的最少数目。<br>提示：经典的区间选点贪心——按右端点升序排序，每次在尚未被覆盖的区间中，选其右端点作为一个点。",
  "第一行整数 N。接下来 N 行，每行两个整数 L<sub>i</sub> R<sub>i</sub>。",
  "一行，所选点的最少数目（整数）。"),
],
}

CSS = """
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
       margin: 0; background: #f4f5f7; color: #1f2430; }
header { background: #1f2430; color: #fff; padding: 22px 28px; }
header h1 { margin: 0 0 6px; font-size: 22px; }
header p { margin: 0; opacity: .8; font-size: 13px; }
.wrap { max-width: 980px; margin: 0 auto; padding: 22px; }
.card { background: #fff; border: 1px solid #e3e6ea; border-radius: 10px;
        padding: 20px 24px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,.05); }
.card h2 { margin: 0 0 4px; font-size: 18px; }
.tag { display: inline-block; font-size: 12px; padding: 2px 10px; border-radius: 12px;
       margin-left: 8px; vertical-align: middle; color: #fff; }
.g1 { background: #2e9e5b; } .g2 { background: #d98616; } .g3 { background: #c0392b; }
.sec-label { font-size: 12px; color: #8a93a2; letter-spacing: 1px; text-transform: uppercase; }
.card h3 { font-size: 14px; margin: 16px 0 6px; color: #34405a;
           border-left: 3px solid #4a6cf7; padding-left: 8px; }
.card p, .card li { font-size: 14px; line-height: 1.7; }
code { background: #eef1f6; padding: 1px 5px; border-radius: 4px; font-size: 13px; }
.samples { display: flex; flex-wrap: wrap; gap: 14px; }
.sample { flex: 1 1 300px; border: 1px solid #e3e6ea; border-radius: 8px; overflow: hidden; }
.sample .sh { background: #f0f3f9; padding: 6px 12px; font-size: 12px; font-weight: 600; color: #4a6cf7; }
.sample pre { margin: 0; padding: 10px 12px; font-family: "Cascadia Code", Consolas, monospace;
              font-size: 13px; white-space: pre; overflow-x: auto; background: #fafbfc; }
.sample .lbl { font-size: 11px; color: #8a93a2; padding: 4px 12px 0; }
.note { background: #fff8e6; border: 1px solid #f2e2b0; border-radius: 8px;
        padding: 10px 14px; font-size: 13px; margin: 10px 0; }
"""

def sample_block(prob_dir, idx):
    ip = os.path.join(prob_dir, f"{idx:02d}.in")
    op = os.path.join(prob_dir, f"{idx:02d}.out")
    if not (os.path.exists(ip) and os.path.exists(op)):
        return ""
    with open(ip, "r", encoding="utf-8") as f: i = f.read()
    with open(op, "r", encoding="utf-8") as f: o = f.read()
    return f"""<div class="sample">
  <div class="sh">样例 {idx}</div>
  <div class="lbl">输入</div><pre>{html.escape(i)}</pre>
  <div class="lbl">输出</div><pre>{html.escape(o)}</pre>
</div>"""

def build(exam):
    title = ["", "模拟试卷（一）· 偏向算法综合与模拟实现",
             "模拟试卷（二）· 偏向动态规划与复杂结构",
             "模拟试卷（三）· 偏向数学逻辑与数据结构应用"][exam]
    subtitle = ["", "基础巩固 / 能力提升 / 极限挑战", "基础巩固 / 能力提升 / 极限挑战",
                "基础巩固 / 能力提升 / 极限挑战"][exam]
    parts = []
    parts.append(f"<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>")
    parts.append(f"<meta name='viewport' content='width=device-width, initial-scale=1'>")
    parts.append(f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>")
    parts.append(f"<header><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)} · 共 9 题 · 点击各题查看样例</p></header>")
    parts.append("<div class='wrap'>")
    for i, (t, body, ind, outd) in enumerate(EXAMS[exam], start=1):
        g = GRAD[i]
        gname = GRAD_NAME[g]
        prob_dir = os.path.join(BASE, EXAM_DIRS[exam], str(i))
        samples = sample_block(prob_dir, 1) + sample_block(prob_dir, 2)
        parts.append(f"""<div class='card'>
  <div class='sec-label'>第 {i} 题 / 共 9 题</div>
  <h2>{html.escape(t)}<span class='tag g{g}'>{gname}</span></h2>
  <h3>题目描述</h3><p>{body}</p>
  <h3>输入格式</h3><p>{ind}</p>
  <h3>输出格式</h3><p>{outd}</p>
  <h3>样例</h3><div class='samples'>{samples}</div>
</div>""")
    parts.append("</div></body></html>")
    return "\n".join(parts)

def main():
    for exam in (1, 2, 3):
        fn = os.path.join(BASE, f"试卷{'一二三'[exam-1]}.html")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(build(exam))
        print("wrote", fn)

if __name__ == "__main__":
    main()
