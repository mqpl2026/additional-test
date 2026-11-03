# -*- coding: utf-8 -*-
"""Test runner for the C++ mock exams.

Usage:
  python runner.py --exam <1|2|3> --probs <n[,n...]|all> --code <file.cpp> [--mode sample|test|submit]

Modes:
  sample : run only the sample tests (01,02) and show full I/O + verdict.
  test   : run every test in the folder, show per-test verdict and failure detail.
  submit : run every test, print ONLY overall AC / NOT AC per problem (no data, no reason).
"""
import argparse, os, subprocess, sys, tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
EXAM_DIRS = {1: "试卷一测试集", 2: "试卷二测试集", 3: "试卷三测试集"}
GXX = "g++"
DEFAULT_TIME = 1.0  # seconds; per-problem overrides below
# Per-problem runtime limits (seconds), matching the HTML exam pages.
TIME_LIMITS = {
    (1,4):2.0,(1,5):2.0,(1,8):2.0,
    (2,1):2.0,(2,2):2.0,(2,4):2.0,(2,5):2.0,(2,8):2.0,(2,9):2.0,
    (3,3):2.0,(3,5):2.0,(3,6):2.0,(3,9):2.0,
}
def tlimit(exam, prob):
    return TIME_LIMITS.get((exam, prob), DEFAULT_TIME)

def norm(s):
    # normalize: strip trailing spaces per line, drop trailing blank lines
    lines = s.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines = [ln.rstrip() for ln in lines]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)

def compile_code(code_path):
    exe = os.path.join(tempfile.gettempdir(), "dsh_runner_exe.exe")
    cmd = [GXX, "-std=c++17", "-O2", "-w", code_path, "-o", exe]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return None, f"compile invocation failed: {e}"
    if p.returncode != 0:
        return None, p.stderr
    return exe, None

def run_one(exe, in_path, out_path, tlim=DEFAULT_TIME):
    with open(in_path, "r", encoding="utf-8", errors="replace") as f:
        stdin_data = f.read()
    try:
        p = subprocess.run([exe], input=stdin_data, capture_output=True,
                           text=True, timeout=tlim)
    except subprocess.TimeoutExpired:
        return "RE", "", "time limit exceeded"
    except Exception as e:
        return "RE", "", str(e)
    if p.returncode < 0:
        return "RE", p.stdout, f"signal {-p.returncode}"
    with open(out_path, "r", encoding="utf-8", errors="replace") as f:
        expected = f.read()
    got = p.stdout
    if norm(got) == norm(expected):
        return "AC", got, ""
    return "WA", got, expected

def list_tests(prob_dir):
    if not os.path.isdir(prob_dir):
        return []
    files = [f for f in os.listdir(prob_dir) if f.endswith(".in")]
    tests = []
    for f in files:
        idx = f[:-3]
        tests.append((idx, os.path.join(prob_dir, f), os.path.join(prob_dir, idx + ".out")))
    tests.sort()
    return tests

def run_problem(exam, prob, exe, mode):
    prob_dir = os.path.join(BASE, EXAM_DIRS[exam], str(prob))
    tests = list_tests(prob_dir)
    if not tests:
        return None, f"no tests found for exam{exam} problem {prob}"
    if mode == "sample":
        tests = [t for t in tests if t[0] in ("01", "02")] or tests[:2]
    results = []
    for idx, in_path, out_path in tests:
        verdict, got, expected = run_one(exe, in_path, out_path, tlimit(exam, prob))
        results.append((idx, verdict, got, expected, in_path))
    return results, None

def cmd_sample(exam, prob, exe):
    results, err = run_problem(exam, prob, exe, "sample")
    if err:
        print(err); return
    print(f"=== 试卷{exam} 第{prob}题 样例测试 ===")
    for idx, verdict, got, expected, in_path in results:
        with open(in_path, "r", encoding="utf-8") as f:
            inp = f.read()
        print(f"\n----- 样例 {idx} : {verdict} -----")
        print("[输入]\n" + inp.rstrip("\n"))
        print("[你的输出]\n" + got.rstrip("\n"))
        if verdict != "AC":
            print("[期望输出]\n" + expected.rstrip("\n"))

def cmd_test(exam, prob, exe):
    results, err = run_problem(exam, prob, exe, "test")
    if err:
        print(err); return
    print(f"=== 试卷{exam} 第{prob}题 测试集结果 ===")
    ac = 0
    for idx, verdict, got, expected, in_path in results:
        mark = "OK" if verdict == "AC" else "XX"
        print(f"  [{mark}] test {idx} : {verdict}")
        if verdict != "AC":
            with open(in_path, "r", encoding="utf-8") as f:
                inp = f.read()
            print("      [input]\n" + "\n".join("        "+l for l in inp.rstrip("\n").split("\n")))
            print("      [your output]\n" + "\n".join("        "+l for l in got.rstrip("\n").split("\n")))
            print("      [expected]\n" + "\n".join("        "+l for l in expected.rstrip("\n").split("\n")))
        else:
            ac += 1
    total = len(results)
    print(f"\n通过 {ac}/{total}")

def cmd_submit(exam, probs, code_path):
    exe, cerr = compile_code(code_path)
    if exe is None:
        # CE: must not reveal test data or reason beyond a compile notice
        for prob in probs:
            print(f"试卷{exam} 第{prob}题: NOT AC")
        return
    all_ac = True
    for prob in probs:
        results, err = run_problem(exam, prob, exe, "test")
        if err:
            print(f"试卷{exam} 第{prob}题: NOT AC")
            all_ac = False
            continue
        ok = all(v == "AC" for _, v, _, _, _ in results)
        if ok:
            print(f"试卷{exam} 第{prob}题: AC")
        else:
            print(f"试卷{exam} 第{prob}题: NOT AC")
            all_ac = False
    print("\n总体: " + ("AC" if all_ac else "NOT AC"))

def parse_probs(s):
    if s == "all":
        return list(range(1, 10))
    out = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b)+1))
        elif part:
            out.append(int(part))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exam", type=int, required=True)
    ap.add_argument("--probs", type=str, default="1")
    ap.add_argument("--code", type=str, required=True)
    ap.add_argument("--mode", type=str, default="test", choices=["sample","test","submit"])
    args = ap.parse_args()
    probs = parse_probs(args.probs)

    if args.mode == "submit":
        cmd_submit(args.exam, probs, args.code)
        return

    exe, cerr = compile_code(args.code)
    if exe is None:
        print("编译失败 (Compile Error):")
        print(cerr)
        return
    for prob in probs:
        if args.mode == "sample":
            cmd_sample(args.exam, prob, exe)
        else:
            cmd_test(args.exam, prob, exe)

if __name__ == "__main__":
    main()
