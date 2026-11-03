# -*- coding: utf-8 -*-
"""Exam 3 test-data generator with verified reference solutions."""
import os, random
from collections import deque

BASE = os.path.dirname(os.path.abspath(__file__))
EXAM = os.path.join(BASE, "试卷三测试集")

def w(prob, idx, inp, out):
    d = os.path.join(EXAM, str(prob))
    with open(os.path.join(d, f"{idx:02d}.in"), "w", encoding="utf-8") as f:
        f.write(inp)
    with open(os.path.join(d, f"{idx:02d}.out"), "w", encoding="utf-8") as f:
        f.write(out)

# ================= P1: segment intersection =================
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
def on_seg(a, b, c):
    # b on segment ac (collinear assumed)
    return min(a[0],c[0])<=b[0]<=max(a[0],c[0]) and min(a[1],c[1])<=b[1]<=max(a[1],c[1])
def seg_intersect(p1,p2,p3,p4):
    d1=cross(p3,p4,p1); d2=cross(p3,p4,p2)
    d3=cross(p1,p2,p3); d4=cross(p1,p2,p4)
    if ((d1>0 and d2<0)or(d1<0 and d2>0)) and ((d3>0 and d4<0)or(d3<0 and d4>0)):
        return True
    if d1==0 and on_seg(p3,p1,p4): return True
    if d2==0 and on_seg(p3,p2,p4): return True
    if d3==0 and on_seg(p1,p3,p2): return True
    if d4==0 and on_seg(p1,p4,p2): return True
    return False
def p1_gen():
    tests = []
    # (0,0)-(2,2) and (0,2)-(2,0) cross at (1,1)
    tests.append(((0,0),(2,2),(0,2),(2,0)))
    # disjoint
    tests.append(((0,0),(1,1),(2,2),(3,3)))
    # touching endpoints
    tests.append(((0,0),(1,1),(1,1),(2,0)))
    # collinear overlap
    tests.append(((0,0),(4,0),(2,0),(6,0)))
    random.seed(3001)
    for _ in range(12):
        def rnd(): return random.randint(-5,5)
        tests.append((((rnd(),rnd()),(rnd(),rnd()),(rnd(),rnd()),(rnd(),rnd()))))
    return tests

# ================= P2: first missing positive =================
def p2_ref(a):
    a = a[:]
    n = len(a)
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i]-1] != a[i]:
            t = a[i]-1
            a[i], a[t] = a[t], a[i]
    for i in range(n):
        if a[i] != i+1:
            return i+1
    return n+1
def p2_gen():
    tests = []
    tests.append(([1,2,0],))
    tests.append(([3,4,-1,1],))
    tests.append(([7,8,9,11,12],))
    tests.append(([1,1,2,2],))
    tests.append(([1,2,3,4,5],))
    random.seed(3002)
    # ramp up sizes; the largest tests punish O(n^2) brute force
    for n in [10, 50, 100, 500, 1000, 5000, 20000, 50000, 100000, 200000]:
        a = [random.randint(-n, n+3) for _ in range(n)]
        tests.append((a,))
    return tests

# ================= P3: string decompression =================
def p3_ref(s):
    res = []
    i = 0
    while i < len(s):
        c = s[i]; i += 1
        num = 0
        while i < len(s) and s[i].isdigit():
            num = num*10 + int(s[i]); i += 1
        if num == 0: num = 1
        res.append(c*num)
    return "".join(res)
def p3_gen():
    tests = []
    tests.append(("a3",))
    tests.append(("a12b2",))
    tests.append(("abc",))
    tests.append(("a1b2c3",))
    random.seed(3003)
    for _ in range(12):
        parts = []
        for _ in range(random.randint(1,5)):
            parts.append(random.choice("abc"))
            if random.random()<0.7:
                parts.append(str(random.randint(1,15)))
        tests.append(("".join(parts),))
    return tests

# ================= P4: RPS max wins =================
def p4_ref(N, Sp, Ss, Sr, Pseq):
    cR = Pseq.count('R'); cP = Pseq.count('P'); cS = Pseq.count('S')
    # Q's Rock beats P's Scissors; Q's Scissors beats P's Paper; Q's Paper beats P's Rock
    return min(Sp, cS) + min(Ss, cP) + min(Sr, cR)
def p4_gen():
    tests = []
    tests.append((3,1,1,1,"RPS"))
    tests.append((4,2,2,0,"RRPP"))
    tests.append((5,0,0,5,"RRRRR"))
    random.seed(3004)
    for _ in range(12):
        N = random.randint(1, 12)
        Pseq = "".join(random.choice("RPS") for _ in range(N))
        Sp = random.randint(0,N); Ss = random.randint(0,N-Sp); Sr = N-Sp-Ss
        tests.append((N,Sp,Ss,Sr,Pseq))
    return tests

# ================= P5: dynamic islands (union-find) =================
class DSU:
    def __init__(self,n):
        self.p=list(range(n)); self.rk=[0]*n; self.cnt=0
    def find(self,x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra==rb: return False
        if self.rk[ra]<self.rk[rb]: ra,rb=rb,ra
        self.p[rb]=ra
        if self.rk[ra]==self.rk[rb]: self.rk[ra]+=1
        return True
def p5_ref(N,M,grid,queries):
    dsu=DSU(N*M)
    land=[[False]*M for _ in range(N)]
    def idx(x,y): return x*M+y
    for i in range(N):
        for j in range(M):
            if grid[i][j]=='#':
                land[i][j]=True; dsu.cnt+=1
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    ni,nj=i+dx,j+dy
                    if 0<=ni<N and 0<=nj<M and land[ni][nj]:
                        if dsu.union(idx(i,j),idx(ni,nj)):
                            dsu.cnt-=1
    out=[]
    for x,y in queries:
        x-=1; y-=1
        if not land[x][y]:
            land[x][y]=True; dsu.cnt+=1
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                ni,nj=x+dx,y+dy
                if 0<=ni<N and 0<=nj<M and land[ni][nj]:
                    if dsu.union(idx(x,y),idx(ni,nj)):
                        dsu.cnt-=1
        out.append(dsu.cnt)
    return out
def p5_gen():
    tests = []
    tests.append((3,3,["#..","...","..#"],[(1,2),(2,2),(3,2)]))
    tests.append((2,2,["..",".."],[(1,1),(2,2),(1,2)]))
    random.seed(3005)
    # large tests: grid up to ~700x700, Q up to 30000, so O(Q*N*M) flood-fill TLEs
    for N,M,Q in [(700,700,30000),(500,500,20000),(300,300,10000)]:
        grid=["".join('#' if random.random()<0.4 else '.' for _ in range(M)) for _ in range(N)]
        queries=[(random.randint(1,N),random.randint(1,M)) for _ in range(Q)]
        tests.append((N,M,grid,queries))
    for _ in range(6):
        N=random.randint(2,8); M=random.randint(2,8)
        grid=["".join('#' if random.random()<0.4 else '.' for _ in range(M)) for _ in range(N)]
        Q=random.randint(1,10)
        queries=[(random.randint(1,N),random.randint(1,M)) for _ in range(Q)]
        tests.append((N,M,grid,queries))
    return tests

# ================= P6: matrix rotation query =================
def p6_ref(N, mat, ops):
    orig = [row[:] for row in mat]
    def f(x,y):
        # 0-indexed current -> original after one CW
        return (N-1-y, x)
    r = 0
    out = []
    for op in ops:
        if op[0]==1:
            _,x,y = op
            x-=1; y-=1
            cx,cy = x,y
            for _ in range(r%4):
                cx,cy = f(cx,cy)
            out.append(orig[cx][cy])
        else:
            r += op[1]
    return out
def p6_gen():
    tests = []
    tests.append((3,[[1,2,3],[4,5,6],[7,8,9]],[(2,1),(1,1,1),(1,3,3),(2,1),(1,2,2)]))
    tests.append((2,[[1,2],[3,4]],[(1,1,1),(1,2,2),(1,1,2)]))
    random.seed(3006)
    # large tests: N up to 1000, K up to 100000, so O(K*N^2) real rotation TLEs
    for N,K in [(1000,100000),(700,70000),(300,30000)]:
        mat=[[random.randint(0,99) for _ in range(N)] for _ in range(N)]
        ops=[]
        for _ in range(K):
            if random.random()<0.5:
                ops.append((2,1))
            else:
                ops.append((1,random.randint(1,N),random.randint(1,N)))
        tests.append((N,mat,ops))
    for _ in range(4):
        N=random.randint(2,8)
        mat=[[random.randint(0,99) for _ in range(N)] for _ in range(N)]
        Q=random.randint(1,10)
        ops=[]
        for _ in range(Q):
            if random.random()<0.5:
                ops.append((2,1))
            else:
                ops.append((1,random.randint(1,N),random.randint(1,N)))
        tests.append((N,mat,ops))
    return tests

# ================= P7: trailing zeros of N! in base B =================
def legendre(n,p):
    c=0
    pk=p
    while pk<=n:
        c+=n//pk
        pk*=p
    return c
def p7_ref(N,B):
    # factor B
    b=B; factors={}
    d=2
    while d*d<=b:
        while b%d==0:
            factors[d]=factors.get(d,0)+1; b//=d
        d+=1
    if b>1: factors[b]=factors.get(b,0)+1
    ans=None
    for p,e in factors.items():
        z=legendre(N,p)//e
        ans=z if ans is None else min(ans,z)
    return ans
def p7_gen():
    tests=[]
    tests.append((5,10))
    tests.append((10,2))
    tests.append((100,16))
    tests.append((25,12))
    tests.append((1000,10))
    random.seed(3007)
    for _ in range(10):
        N=random.randint(1,2000)
        B=random.randint(2,20)
        tests.append((N,B))
    return tests

# ================= P8: bit-ops BFS =================
def p8_ref(S,T):
    LIMIT=1<<20
    if S==T: return 0
    from collections import deque
    dq=deque([S])
    dist={S:0}
    while dq:
        x=dq.popleft()
        d=dist[x]
        for nx in (x*2, x^1, x<<3):
            if nx<0 or nx>LIMIT: continue
            if nx==T: return d+1
            if nx not in dist:
                dist[nx]=d+1
                dq.append(nx)
    return -1
def p8_gen():
    tests=[]
    tests.append((0,0))
    tests.append((1,2))
    tests.append((2,3))
    tests.append((5,10))
    tests.append((1,10))
    random.seed(3008)
    for _ in range(10):
        S=random.randint(0,200); T=random.randint(0,200)
        tests.append((S,T))
    return tests

# ================= P9: interval point coverage (min points) =================
def p9_ref(intervals):
    ivs=sorted(intervals, key=lambda x:x[1])
    cnt=0
    last=None
    for L,R in ivs:
        if last is None or L>last:
            cnt+=1
            last=R
    return cnt
def p9_gen():
    tests=[]
    tests.append([(1,3),(2,4),(5,6)])
    tests.append([(1,2),(2,3),(3,4)])
    tests.append([(1,10),(2,3),(4,5)])
    random.seed(3009)
    # ramp up sizes; the largest tests punish O(n^2)/O(n^3) brute force
    for n in [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 200000]:
        ivs=[]
        for _ in range(n):
            L=random.randint(0, 1000000); R=L+random.randint(0, 1000000)
            ivs.append((L,R))
        tests.append(ivs)
    return tests

# ================= run =================
def main():
    for idx,(p1,p2,p3,p4) in enumerate(p1_gen(), start=1):
        inp=f"{p1[0]} {p1[1]} {p2[0]} {p2[1]}\n{p3[0]} {p3[1]} {p4[0]} {p4[1]}\n"
        w(1, idx, inp, ("YES" if seg_intersect(p1,p2,p3,p4) else "NO")+"\n")
    for idx,(a,) in enumerate(p2_gen(), start=1):
        inp=f"{len(a)}\n"+" ".join(map(str,a))+"\n"
        w(2, idx, inp, str(p2_ref(a))+"\n")
    for idx,(s,) in enumerate(p3_gen(), start=1):
        w(3, idx, s+"\n", p3_ref(s)+"\n")
    for idx,(N,Sp,Ss,Sr,Pseq) in enumerate(p4_gen(), start=1):
        inp=f"{N} {Sp} {Ss} {Sr}\n{Pseq}\n"
        w(4, idx, inp, str(p4_ref(N,Sp,Ss,Sr,Pseq))+"\n")
    for idx,(N,M,grid,q) in enumerate(p5_gen(), start=1):
        lines=[f"{N} {M}"]+grid+[str(len(q))]
        lines+= [f"{x} {y}" for x,y in q]
        inp="\n".join(lines)+"\n"
        out=p5_ref(N,M,grid,q)
        w(5, idx, inp, ("\n".join(map(str,out)))+"\n" if out else "\n")
    for idx,(N,mat,ops) in enumerate(p6_gen(), start=1):
        lines=[f"{N} {len(ops)}"]
        lines+=[" ".join(map(str,row)) for row in mat]
        for op in ops:
            if op[0]==1: lines.append(f"1 {op[1]} {op[2]}")
            else: lines.append(f"2 {op[1]}")
        inp="\n".join(lines)+"\n"
        out=p6_ref(N,mat,ops)
        w(6, idx, inp, ("\n".join(map(str,out)))+"\n" if out else "\n")
    for idx,(N,B) in enumerate(p7_gen(), start=1):
        w(7, idx, f"{N} {B}\n", str(p7_ref(N,B))+"\n")
    for idx,(S,T) in enumerate(p8_gen(), start=1):
        w(8, idx, f"{S} {T}\n", str(p8_ref(S,T))+"\n")
    for idx,ivs in enumerate(p9_gen(), start=1):
        inp=f"{len(ivs)}\n"+"\n".join(f"{L} {R}" for L,R in ivs)+"\n"
        w(9, idx, inp, str(p9_ref(ivs))+"\n")
    print("Exam 3 generated.")

if __name__=="__main__":
    main()
