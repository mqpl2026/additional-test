# -*- coding: utf-8 -*-
"""Exam 2 test-data generator with verified reference solutions."""
import os, random
from collections import deque

BASE = os.path.dirname(os.path.abspath(__file__))
EXAM = os.path.join(BASE, "试卷二测试集")

def w(prob, idx, inp, out):
    d = os.path.join(EXAM, str(prob))
    with open(os.path.join(d, f"{idx:02d}.in"), "w", encoding="utf-8") as f:
        f.write(inp)
    with open(os.path.join(d, f"{idx:02d}.out"), "w", encoding="utf-8") as f:
        f.write(out)

# ================= P1: sliding window max =================
def p1_ref(a, k):
    from collections import deque
    dq = deque()
    res = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return res
def p1_gen():
    tests = []
    tests.append(([1,3,-1,-3,5,3,6,7], 3))
    tests.append(([9,8,7,6], 2))
    random.seed(1001)
    # ramp up sizes; the largest tests punish O(N*K)/O(N^2) brute force
    sizes = [5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 200000]
    for n in sizes:
        if n <= 100:
            k = random.randint(1, n)
        else:
            # k near n/2 maximizes the O(n*k) window-scan brute force -> TLE
            k = max(1, n // 2 + random.randint(-n // 20, n // 20))
        a = [random.randint(-50, 50) for _ in range(n)]
        tests.append((a, k))
    return tests

# ================= P2: jump game min jumps =================
def p2_ref(a):
    n = len(a)
    if n <= 1:
        return 0
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + a[i])
        if i == cur_end:
            if farthest <= i:
                return -1
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break
    return jumps if cur_end >= n - 1 else -1
def p2_gen():
    tests = []
    tests.append([2,3,1,1,4])
    tests.append([3,2,1,0,4])
    tests.append([0])
    tests.append([1,1,1,1])
    random.seed(1002)
    # ramp up sizes; large tests use reachable arrays so the answer is meaningful
    sizes = [5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 200000]
    for n in sizes:
        lo, hi = (1, 6) if n >= 1000 else (0, 6)
        a = [random.randint(lo, hi) for _ in range(n)]
        tests.append(a)
    return tests

# ================= P3: palindrome partitioning (all, lex) =================
def is_pal(s, i, j):
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1; j -= 1
    return True
def p3_ref(s):
    res = []
    n = len(s)
    part = []
    def dfs(start):
        if start == n:
            res.append("|".join(part))
            return
        for end in range(start, n):
            if is_pal(s, start, end):
                part.append(s[start:end+1])
                dfs(end+1)
                part.pop()
    dfs(0)
    return res
def p3_gen():
    tests = []
    tests.append(("aab", 0))
    tests.append(("abc", 0))
    tests.append(("aaa", 0))
    random.seed(1003)
    for _ in range(10):
        L = random.randint(1, 8)
        s = "".join(random.choice("aabbc") for _ in range(L))
        tests.append((s, 0))
    return tests

# ================= P4: interval reverse + point query (implicit treap) =================
class TreapNode:
    __slots__ = ("val","pri","size","left","right","rev")
    def __init__(self, val):
        self.val = val
        self.pri = random.random()
        self.size = 1
        self.left = None
        self.right = None
        self.rev = False
def sz(t): return t.size if t else 0
def upd(t):
    if t: t.size = 1 + sz(t.left) + sz(t.right)
def push(t):
    if t and t.rev:
        t.rev = False
        t.left, t.right = t.right, t.left
        if t.left: t.left.rev = not t.left.rev
        if t.right: t.right.rev = not t.right.rev
def split(t, k):
    # first k nodes -> a, rest -> b
    if not t: return (None, None)
    push(t)
    if sz(t.left) >= k:
        a, b = split(t.left, k)
        t.left = b
        upd(t)
        return (a, t)
    else:
        a, b = split(t.right, k - sz(t.left) - 1)
        t.right = a
        upd(t)
        return (t, b)
def merge(a, b):
    if not a: return b
    if not b: return a
    if a.pri > b.pri:
        push(a)
        a.right = merge(a.right, b)
        upd(a)
        return a
    else:
        push(b)
        b.left = merge(a, b.left)
        upd(b)
        return b
def build_treap(arr):
    root = None
    for v in arr:
        root = merge(root, TreapNode(v))
    return root
def build_treap_fast(arr):
    # O(N) Cartesian-tree build by priority (max-heap); in-order = arr.
    nodes = [TreapNode(v) for v in arr]
    stack = []
    for node in nodes:
        last = None
        while stack and stack[-1].pri < node.pri:
            last = stack.pop()
        node.left = last
        if stack:
            stack[-1].right = node
        stack.append(node)
    root = stack[0]
    # iterative post-order to recompute subtree sizes
    order = []
    st = [(root, False)]
    while st:
        node, visited = st.pop()
        if node is None:
            continue
        if visited:
            order.append(node)
        else:
            st.append((node, True))
            st.append((node.right, False))
            st.append((node.left, False))
    for node in order:
        node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)
    return root
def tval(t, idx):
    # 0-based index
    push(t)
    l = sz(t.left)
    if idx < l:
        return tval(t.left, idx)
    elif idx == l:
        return t.val
    else:
        return tval(t.right, idx - l - 1)
def p4_ref(n, ops):
    root = build_treap(list(range(1, n+1)))
    out = []
    for op in ops:
        if op[0] == 1:
            _, L, R = op
            a, bc = split(root, L-1)
            b, c = split(bc, R-L+1)
            if b: b.rev = not b.rev
            root = merge(a, merge(b, c))
        else:
            _, X = op
            out.append(tval(root, X-1))
    return out
def p4_ref_fast(n, ops):
    root = build_treap_fast(list(range(1, n+1)))
    out = []
    for op in ops:
        if op[0] == 1:
            _, L, R = op
            a, bc = split(root, L-1)
            b, c = split(bc, R-L+1)
            if b: b.rev = not b.rev
            root = merge(a, merge(b, c))
        else:
            _, X = op
            out.append(tval(root, X-1))
    return out
def p4_gen():
    tests = []
    tests.append((5, [(2,3),(1,1,5),(2,3),(1,2,4),(2,2)]))
    tests.append((3, [(1,1,3),(2,1),(2,2),(2,3)]))
    random.seed(1004)
    # ramp up sizes; ops scale with n so O(N) per reversal brute force TLEs
    sizes = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000, 200000]
    for n in sizes:
        m = max(1, int(n * 0.5))
        ops = []
        for _ in range(m):
            if random.random() < 0.5:
                L = random.randint(1, n); R = random.randint(L, n)
                ops.append((1, L, R))
            else:
                ops.append((2, random.randint(1, n)))
        tests.append((n, ops))
    return tests

# ================= P5: edit distance =================
def p5_ref(a, b):
    n, m = len(a), len(b)
    prev = list(range(m+1))
    for i in range(1, n+1):
        cur = [i] + [0]*m
        ai = a[i-1]
        for j in range(1, m+1):
            if ai == b[j-1]:
                cur[j] = prev[j-1]
            else:
                cur[j] = 1 + min(prev[j], cur[j-1], prev[j-1])
        prev = cur
    return prev[m]
def p5_gen():
    tests = []
    tests.append(("horse","ros"))
    tests.append(("intention","execution"))
    tests.append(("A","TTT"))
    tests.append(("TTT","A"))
    random.seed(1005)
    # large tests punish O(3^(a+b)) recursive brute force; DP handles them easily
    tests.append(("A"*2000, "T"*2000))
    tests.append(("G"*1500 + "ACGT"*100, "C"*2000))
    for _ in range(9):
        la = random.randint(1, 500)
        lb = random.randint(1, la)
        a = "".join(random.choice("ACGT") for _ in range(la))
        b = "".join(random.choice("ACGT") for _ in range(lb))
        tests.append((a, b))
    return tests

# ================= P6: fraction to decimal with repeating =================
def p6_ref(A, B):
    intpart = A // B
    rem = A % B
    if rem == 0:
        return str(intpart)
    digits = []
    pos = {}  # remainder -> index
    while rem != 0 and rem not in pos:
        pos[rem] = len(digits)
        rem *= 10
        digits.append(str(rem // B))
        rem = rem % B
    if rem == 0:
        return f"{intpart}." + "".join(digits)
    else:
        p = pos[rem]
        return f"{intpart}." + "".join(digits[:p]) + "(" + "".join(digits[p:]) + ")"
def p6_gen():
    tests = []
    tests.append((1,3))
    tests.append((1,6))
    tests.append((1,2))
    tests.append((2,1))
    tests.append((1,7))
    tests.append((22,7))
    random.seed(1006)
    for _ in range(11):
        A = random.randint(1, 1000)
        B = random.randint(2, 100)
        tests.append((A,B))
    return tests

# ================= P7: infix eval (no parens), + - * / =================
def cdiv(a, b):
    # C++ truncation toward zero
    q = abs(a) // abs(b)
    return -q if (a < 0) ^ (b < 0) else q
def p7_ref(expr):
    # tokens: numbers and operators
    vals = []
    ops = []
    i = 0
    n = len(expr)
    def apply():
        b = vals.pop(); a = vals.pop(); op = ops.pop()
        if op == '+': vals.append(a+b)
        elif op == '-': vals.append(a-b)
        elif op == '*': vals.append(a*b)
        else: vals.append(cdiv(a,b))
    prec = {'+':1,'-':1,'*':2,'/':2}
    while i < n:
        if expr[i].isdigit():
            j = i
            while j < n and expr[j].isdigit():
                j += 1
            vals.append(int(expr[i:j]))
            i = j
        elif expr[i] in prec:
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[expr[i]]:
                apply()
            ops.append(expr[i])
            i += 1
        else:
            i += 1
    while ops:
        apply()
    return vals[0]
def p7_gen():
    tests = []
    tests.append(("2+3*4", 0))
    tests.append(("10-2-3", 0))
    tests.append(("2*3+4*5", 0))
    tests.append(("100/5/2", 0))
    tests.append(("7+8*2-4/2", 0))
    random.seed(1007)
    for _ in range(11):
        parts = []
        cnt = random.randint(2, 6)
        for k in range(cnt):
            parts.append(str(random.randint(1, 20)))
            if k < cnt-1:
                parts.append(random.choice("+-*/"))
        tests.append(("".join(parts), 0))
    return tests

# ================= P8: tree diameter =================
def p8_ref(n, edges):
    if n == 1:
        return 0
    g = [[] for _ in range(n)]
    for u,v,ww in edges:
        g[u-1].append((v-1, ww))
        g[v-1].append((u-1, ww))
    def bfs(src):
        dist = [-1]*n
        dist[src] = 0
        q = deque([src])
        far = src
        while q:
            x = q.popleft()
            for y, ww in g[x]:
                if dist[y] < 0:
                    dist[y] = dist[x] + ww
                    q.append(y)
                    if dist[y] > dist[far]:
                        far = y
        return far, dist
    a, _ = bfs(0)
    b, dist = bfs(a)
    return dist[b]
def p8_gen():
    tests = []
    tests.append((2, [(1,2,5)]))
    tests.append((3, [(1,2,1),(2,3,2)]))
    random.seed(1008)
    # ramp up sizes; the largest tests punish O(N^2) all-pairs BFS
    sizes = [5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 200000]
    for n in sizes:
        edges = []
        for i in range(2, n+1):
            p = random.randint(1, i-1)
            edges.append((p, i, random.randint(1, 100)))
        tests.append((n, edges))
    return tests

# ================= P9: LIS length + count (value-distinct) =================
def p9_ref(a):
    n = len(a)
    dp = [1]*n
    ways = [1]*n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                if dp[j]+1 > dp[i]:
                    dp[i] = dp[j]+1
                    ways[i] = ways[j]
                elif dp[j]+1 == dp[i]:
                    ways[i] += ways[j]
            elif a[j] == a[i] and dp[j] == dp[i]:
                ways[j] = 0
    if n == 0:
        return (0, 0)
    mx = max(dp)
    total = sum(ways[i] for i in range(n) if dp[i] == mx)
    return (mx, total)
def p9_brute(a):
    # enumerate distinct value-sequences that are strictly increasing, of max length
    n = len(a)
    from itertools import combinations
    best = 0
    seqs = set()
    for r in range(1, n+1):
        for idx in combinations(range(n), r):
            vals = [a[i] for i in idx]
            if all(vals[k] < vals[k+1] for k in range(len(vals)-1)):
                if r > best:
                    best = r
                    seqs = {tuple(vals)}
                elif r == best:
                    seqs.add(tuple(vals))
    return (best, len(seqs))
def p9_gen():
    tests = []
    tests.append([1,3,5,4,7])
    tests.append([5,4,3,2,1])
    tests.append([1,3,2,4])
    random.seed(1009)
    # small tests verified against brute-force enumeration
    for _ in range(6):
        n = random.randint(1, 12)
        a = random.sample(range(1, 100), n)   # DISTINCT values -> count convention unambiguous
        assert p9_ref(a) == p9_brute(a), f"P9 mismatch {a}: {p9_ref(a)} vs {p9_brute(a)}"
        tests.append(a)
    # large tests: O(n^2) DP only (O(2^n) enumeration is infeasible)
    for n in [50, 100, 200, 500, 1000, 2000]:
        a = random.sample(range(-10**9, 10**9), n)   # DISTINCT values
        tests.append(a)
    return tests

# ================= run =================
def main():
    for idx,(a,k) in enumerate(p1_gen(), start=1):
        inp = f"{len(a)} {k}\n" + " ".join(map(str,a)) + "\n"
        w(1, idx, inp, " ".join(map(str,p1_ref(a,k))) + "\n")
    for idx,a in enumerate(p2_gen(), start=1):
        inp = f"{len(a)}\n" + " ".join(map(str,a)) + "\n"
        w(2, idx, inp, str(p2_ref(a)) + "\n")
    for idx,(s,_) in enumerate(p3_gen(), start=1):
        res = p3_ref(s)
        w(3, idx, s+"\n", ("\n".join(res))+"\n" if res else "\n")
    for idx,(n,ops) in enumerate(p4_gen(), start=1):
        if n <= 2000:
            assert p4_ref(n, ops) == p4_ref_fast(n, ops), f"P4 mismatch n={n}"
            out = p4_ref(n, ops)
        else:
            out = p4_ref_fast(n, ops)
        lines = [f"{n} {len(ops)}"]
        for op in ops:
            if op[0]==1: lines.append(f"1 {op[1]} {op[2]}")
            else: lines.append(f"2 {op[1]}")
        inp = "\n".join(lines)+"\n"
        w(4, idx, inp, ("\n".join(map(str,out)))+"\n" if out else "\n")
    for idx,(a,b) in enumerate(p5_gen(), start=1):
        w(5, idx, a+"\n"+b+"\n", str(p5_ref(a,b))+"\n")
    for idx,(A,B) in enumerate(p6_gen(), start=1):
        w(6, idx, f"{A} {B}\n", p6_ref(A,B)+"\n")
    for idx,(expr,_) in enumerate(p7_gen(), start=1):
        w(7, idx, expr+"\n", str(p7_ref(expr))+"\n")
    for idx,(n,edges) in enumerate(p8_gen(), start=1):
        lines = [str(n)]
        for u,v,ww in edges:
            lines.append(f"{u} {v} {ww}")
        w(8, idx, "\n".join(lines)+"\n", str(p8_ref(n,edges))+"\n")
    for idx,a in enumerate(p9_gen(), start=1):
        ln, cnt = p9_ref(a)
        w(9, idx, f"{len(a)}\n" + " ".join(map(str,a)) + "\n", f"{ln} {cnt}\n")
    print("Exam 2 generated.")

if __name__ == "__main__":
    main()
