# -*- coding: utf-8 -*-
"""Exam 1 test-data generator with verified reference solutions."""
import os, random, sys

BASE = os.path.dirname(os.path.abspath(__file__))
EXAM = os.path.join(BASE, "试卷一测试集")

def w(prob, idx, inp, out):
    d = os.path.join(EXAM, str(prob))
    with open(os.path.join(d, f"{idx:02d}.in"), "w", encoding="utf-8") as f:
        f.write(inp)
    with open(os.path.join(d, f"{idx:02d}.out"), "w", encoding="utf-8") as f:
        f.write(out)

def fmt(x):
    return "\n".join(str(x)) + "\n"

# ---------------- Problem 1: type inference ----------------
# rank: char<int<float<double<longlong ; answer = highest rank token present
RANK = {"char":1,"int":2,"float":3,"double":4,"longlong":5}
def p1_ref(expr):
    best = "char"
    for k in RANK:
        if k in expr and RANK[k] > RANK[best]:
            best = k
    return best
def p1_gen():
    toks = list(RANK.keys())
    tests = []
    # hand samples
    tests.append(("int+float", "int+float"))
    tests.append(("char+int+double", "char+int+double"))
    tests.append(("(int+float)+char", "(int+float)+char"))
    tests.append(("longlong+int", "longlong+int"))
    random.seed(101)
    for _ in range(8):
        n = random.randint(3, 10)
        parts = [random.choice(toks) for _ in range(n)]
        expr = ("+".join(parts))
        # add some parentheses randomly
        expr = expr.replace("+", "+", 1)
        tests.append((expr, expr))
    return tests

# ---------------- Problem 2: HP simulation (regularized) ----------------
def p2_ref(H, D, springs):
    # springs: list of (X,V); positions distinct in [1,D]
    heal = {}
    for x,v in springs:
        heal[x] = v
    hp = H
    for pos in range(1, D+1):
        hp -= 1
        if hp <= 0:
            return -1
        if pos in heal:
            hp = min(H, hp + heal[pos])
    return hp
def p2_gen():
    tests = []
    # hand samples
    tests.append((10, 5, [(3,4),(5,2)]))
    tests.append((5, 10, [(2,3),(7,3)]))
    random.seed(202)
    for _ in range(10):
        H = random.randint(3, 30)
        D = random.randint(3, 30)
        n = random.randint(0, min(6, D))
        xs = random.sample(range(1, D+1), n)
        springs = [(x, random.randint(1, H+2)) for x in xs]
        springs.sort()
        tests.append((H, D, springs))
    return tests

# ---------------- Problem 3: zigzag rows ----------------
def p3_ref(S, R):
    if R == 1:
        return [S]
    rows = [[] for _ in range(R)]
    r, step = 0, 1
    for ch in S:
        rows[r].append(ch)
        if r == 0:
            step = 1
        elif r == R-1:
            step = -1
        r += step
    return ["".join(x) for x in rows]
def p3_gen():
    tests = []
    tests.append(("abcdefg", 3))
    tests.append(("ABCDE", 2))
    random.seed(303)
    for _ in range(11):
        L = random.randint(1, 20)
        S = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(L))
        R = random.randint(1, 5)
        tests.append((S, R))
    return tests

# ---------------- Problem 4: max (R-L) over intervals sharing a point ----------------
def p4_ref(intervals):
    # brute O(n^2): max over intersecting pairs (a,b) of R_a - L_b
    n = len(intervals)
    best = 0
    for i in range(n):
        for j in range(n):
            La, Ra = intervals[i]
            Lb, Rb = intervals[j]
            if max(La, Lb) <= min(Ra, Rb):  # intersect
                best = max(best, Ra - Lb)
    return best
def p4_ref_fast(intervals):
    # sweep line, O(n log n): at each coordinate, active = {i: L_i<=c<=R_i},
    # track maxR - minL via two lazy heaps (index-based, handles duplicates).
    import heapq
    from collections import defaultdict
    add = defaultdict(list); rem = defaultdict(list)
    for idx, (L, R) in enumerate(intervals):
        add[L].append(idx); rem[R].append(idx)
    coords = sorted(set(list(add) + list(rem)))
    active = [False] * len(intervals)
    maxR = []; minL = []
    best = 0
    for c in coords:
        for idx in add[c]:
            active[idx] = True
            L, R = intervals[idx]
            heapq.heappush(maxR, (-R, idx))
            heapq.heappush(minL, (L, idx))
        while maxR and not active[maxR[0][1]]:
            heapq.heappop(maxR)
        while minL and not active[minL[0][1]]:
            heapq.heappop(minL)
        if maxR and minL:
            best = max(best, -maxR[0][0] - minL[0][0])
        for idx in rem[c]:
            active[idx] = False
    return best
def p4_gen():
    tests = []
    tests.append([(1,5),(2,6),(3,4)])
    tests.append([(1,2),(3,4),(5,6)])
    random.seed(404)
    # ramp up sizes; the largest tests punish O(n^2) brute force
    sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 5000, 20000, 50000, 100000, 200000]
    for n in sizes:
        ivs = []
        if n <= 1000:
            for _ in range(n):
                L = random.randint(0, 20)
                R = L + random.randint(0, 15)
                ivs.append((L, R))
        else:
            for _ in range(n):
                L = random.randint(0, 1000000)
                R = L + random.randint(0, 1000000)
                ivs.append((L, R))
        tests.append(ivs)
    return tests

# ---------------- Problem 5: maze min cost with row/col-end teleport ----------------
def p5_ref(N, M, grid):
    # grid: list of strings, '.' open '#' blocked; (0,0) and (N-1,M-1) open
    from collections import deque
    INF = float('inf')
    dist = [[INF]*M for _ in range(N)]
    dist[0][0] = 0
    dq = deque([(0,0)])
    while dq:
        x,y = dq.popleft()
        d = dist[x][y]
        cand = []
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny = x+dx,y+dy
            if 0<=nx<N and 0<=ny<M and grid[nx][ny]=='.':
                cand.append((nx,ny,d+1))
        for nx,ny in ((x,0),(x,M-1),(0,y),(N-1,y)):
            if (nx,ny)!=(x,y) and grid[nx][ny]=='.':
                cand.append((nx,ny,d+1))
        for nx,ny,nd in cand:
            if nd < dist[nx][ny]:
                dist[nx][ny] = nd
                dq.append((nx,ny))
    return -1 if dist[N-1][M-1]==INF else dist[N-1][M-1]
def p5_gen():
    tests = []
    # sample 1
    g1 = ["..",
          ".."]
    tests.append((2,2,g1))
    g2 = [".#.",
          ".#.",
          "..."]
    tests.append((3,3,g2))
    random.seed(505)
    for _ in range(10):
        N = random.randint(2,6); M = random.randint(2,6)
        g = []
        for i in range(N):
            row = "".join('.' if random.random()>0.3 else '#' for _ in range(M))
            g.append(row)
        g[0] = '.'+g[0][1:] if M>1 else '.'
        g[N-1] = '.'+g[N-1][1:] if M>1 else '.'
        # ensure start open
        g[0] = list(g[0]); g[0][0]='.'; g[0]="".join(g[0])
        gl = [list(r) for r in g]; gl[N-1][M-1]='.'; g=["".join(r) for r in gl]
        tests.append((N,M,g))
    return tests

# ---------------- Problem 6: decimal string -> base K ----------------
DIG = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def to_base_int(x, K):
    if x == 0: return "0"
    res = []
    while x:
        res.append(DIG[x % K]); x //= K
    return "".join(reversed(res))
def p6_ref(D, K):
    if '.' in D:
        ip, fp = D.split('.')
    else:
        ip, fp = D, ""
    ip = ip.lstrip('0') or '0'
    iv = int(ip)
    intpart = to_base_int(iv, K)
    if not fp:
        return intpart
    denom = 10 ** len(fp)
    frac = int(fp)
    digits = []
    seen = set()
    while frac != 0:
        if frac in seen:
            break
        seen.add(frac)
        frac *= K
        d = frac // denom
        digits.append(DIG[d])
        frac = frac % denom
        if len(digits) > 40:
            break
    if frac == 0:
        return intpart + "." + "".join(digits)
    else:
        return intpart + "." + "".join(digits[:8])
def p6_gen():
    tests = []
    tests.append(("0.5", 2))
    tests.append(("3.14159", 16))
    random.seed(606)
    for _ in range(11):
        ip = random.randint(0, 1000)
        flen = random.randint(0, 8)
        fp = "".join(random.choice("0123456789") for _ in range(flen))
        D = str(ip) + ("."+fp if fp else "")
        K = random.randint(2,16)
        tests.append((D,K))
    return tests

# ---------------- Problem 7: min average waiting time ----------------
def p7_ref(T):
    T = sorted(T)
    total = 0
    s = 0
    for t in T:
        s += t
        total += s
    return total / len(T)
def p7_gen():
    tests = []
    tests.append([3,1,4,2])
    tests.append([5,5,5,5])
    random.seed(707)
    for _ in range(11):
        n = random.randint(1, 12)
        T = [random.randint(1, 20) for _ in range(n)]
        tests.append(T)
    return tests

# ---------------- Problem 8: max xor path (set DP) ----------------
def p8_ref(mat):
    N = len(mat); M = len(mat[0])
    dp = [[set() for _ in range(M)] for _ in range(N)]
    dp[0][0].add(mat[0][0])
    for i in range(N):
        for j in range(M):
            if i==0 and j==0: continue
            cur = set()
            if i>0:
                for v in dp[i-1][j]: cur.add(v ^ mat[i][j])
            if j>0:
                for v in dp[i][j-1]: cur.add(v ^ mat[i][j])
            dp[i][j] = cur
    return max(dp[N-1][M-1])
def p8_gen():
    tests = []
    tests.append([[1,2],[3,4]])
    tests.append([[5]])
    random.seed(808)
    for _ in range(11):
        N = random.randint(1,6); M = random.randint(1,6)
        mat = [[random.randint(0, 63) for _ in range(M)] for _ in range(N)]
        tests.append(mat)
    return tests

# ---------------- Problem 9: big A / small B, K decimals ----------------
def p9_ref(A, B, K):
    # A string, B int, K decimals, truncate
    rem = 0
    intpart = []
    for ch in A:
        rem = rem*10 + int(ch)
        intpart.append(str(rem // B))
        rem = rem % B
    ip = "".join(intpart).lstrip('0') or '0'
    if K == 0:
        return ip
    digits = []
    for _ in range(K):
        rem *= 10
        digits.append(str(rem // B))
        rem = rem % B
    return ip + "." + "".join(digits)
def p9_gen():
    tests = []
    tests.append(("100", 3, 5))
    tests.append(("7", 2, 4))
    random.seed(909)
    for _ in range(11):
        L = random.randint(1, 30)
        A = "".join(random.choice("0123456789") for _ in range(L)).lstrip('0') or "0"
        B = random.randint(1, 1000000)
        K = random.randint(0, 20)
        tests.append((A,B,K))
    return tests

# ================= run =================
def main():
    # P1
    for idx,(expr,_) in enumerate(p1_gen(), start=1):
        w(1, idx, expr+"\n", p1_ref(expr)+"\n")
    # P2
    for idx,(H,D,sp) in enumerate(p2_gen(), start=1):
        lines = [f"{H} {D} {len(sp)}"]
        lines.append(" ".join(f"{x} {v}" for x,v in sp))
        inp = "\n".join(lines)+"\n"
        w(2, idx, inp, str(p2_ref(H,D,sp))+"\n")
    # P3
    for idx,(S,R) in enumerate(p3_gen(), start=1):
        rows = p3_ref(S,R)
        w(3, idx, f"{S}\n{R}\n", ("\n".join(rows))+"\n")
    # P4
    for idx,ivs in enumerate(p4_gen(), start=1):
        if len(ivs) <= 1000:
            assert p4_ref(ivs) == p4_ref_fast(ivs), f"P4 mismatch {ivs}"
        inp = f"{len(ivs)}\n" + "\n".join(f"{L} {R}" for L,R in ivs) + "\n"
        w(4, idx, inp, str(p4_ref_fast(ivs))+"\n")
    # P5
    for idx,(N,M,g) in enumerate(p5_gen(), start=1):
        inp = f"{N} {M}\n" + "\n".join(g) + "\n"
        w(5, idx, inp, str(p5_ref(N,M,g))+"\n")
    # P6
    for idx,(D,K) in enumerate(p6_gen(), start=1):
        w(6, idx, f"{D}\n{K}\n", p6_ref(D,K)+"\n")
    # P7
    for idx,T in enumerate(p7_gen(), start=1):
        inp = f"{len(T)}\n" + " ".join(map(str,T)) + "\n"
        w(7, idx, inp, f"{p7_ref(T):.2f}\n")
    # P8
    for idx,mat in enumerate(p8_gen(), start=1):
        N=len(mat); M=len(mat[0])
        inp = f"{N} {M}\n" + "\n".join(" ".join(map(str,row)) for row in mat) + "\n"
        w(8, idx, inp, str(p8_ref(mat))+"\n")
    # P9
    for idx,(A,B,K) in enumerate(p9_gen(), start=1):
        w(9, idx, f"{A}\n{B}\n{K}\n", p9_ref(A,B,K)+"\n")
    print("Exam 1 generated.")

if __name__ == "__main__":
    main()
