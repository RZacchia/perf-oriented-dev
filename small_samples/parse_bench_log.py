#!/usr/bin/env python3
import csv
import re
import sys
import math
from collections import defaultdict
from statistics import mean

CPU_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)%\s*$")

def pop_variance(xs):
    if not xs:
        return 0.0
    mu = mean(xs)
    return sum((x - mu) ** 2 for x in xs) / len(xs)

def pop_stddev(xs):
    return math.sqrt(pop_variance(xs))

def pct_stddev(xs):
    """(stddev/mean)*100; returns 0 if empty or mean==0."""
    if not xs:
        return 0.0
    mu = mean(xs)
    if mu == 0:
        return 0.0
    return (pop_stddev(xs) / mu) * 100.0

def parse_cpu_pct(s: str) -> float:
    m = CPU_RE.match(s)
    if not m:
        raise ValueError(f"Bad cpu field (expected like '99%'): {s!r}")
    return float(m.group(1))

def read_log(path: str):
    """
    Reads lines:
      name,elapsed,user,system,cpu%,peakmem
    Returns dict name -> dict of lists.
    """
    data = defaultdict(lambda: {"wall": [], "cpu": [], "mem": []})

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 6:
                raise ValueError(f"{path}:{lineno}: expected 6 comma-separated fields, got {len(parts)}: {line!r}")

            name, wall_s, user_s, sys_s, cpu_s, mem_kb = parts

            try:
                wall = float(wall_s)
                # user/system are present but not needed for output; parse to validate
                _user = float(user_s)
                _sys = float(sys_s)
                cpu = parse_cpu_pct(cpu_s)
                mem = float(mem_kb)
            except ValueError as e:
                raise ValueError(f"{path}:{lineno}: {e}") from e

            data[name]["wall"].append(wall)
            data[name]["cpu"].append(cpu)
            data[name]["mem"].append(mem)

    return data

def write_summary(data, out_csv: str):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "program",
            "avg_wall",
            "var_wall",
            "pct_std_wall",
            "avg_cpu_pct",
            "avg_peak_mem_kb",
        ])

        for name in sorted(data.keys()):
            wall = data[name]["wall"]
            cpu = data[name]["cpu"]
            mem = data[name]["mem"]

            avg_wall = mean(wall) if wall else 0.0
            var_wall = pop_variance(wall)
            pct_wall = pct_stddev(wall)

            avg_cpu = mean(cpu) if cpu else 0.0
            avg_mem = mean(mem) if mem else 0.0

            w.writerow([
                name,
                f"{avg_wall:.6f}",
                f"{var_wall:.6f}",
                f"{pct_wall:.6f}",
                f"{avg_cpu:.2f}",
                f"{avg_mem:.2f}",
            ])

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_bench_log.py <input_log.log> <output.csv>", file=sys.stderr)
        sys.exit(2)

    inp, outp = sys.argv[1], sys.argv[2]
    data = read_log(inp)

    if not data:
        print("Warning: no data parsed (empty file?)", file=sys.stderr)

    write_summary(data, outp)

if __name__ == "__main__":
    main()