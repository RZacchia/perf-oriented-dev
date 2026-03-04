#!/usr/bin/env python3
import re
import csv
import sys
from statistics import mean

# Matches your banner lines like:
# echo ============ Delannoy ================
BANNER_RE = re.compile(r"=+\s*([A-Za-z0-9_.-]+)\s*=+")

# GNU time default includes "... 0:00.12elapsed ..."
GNU_ELAPSED_RE = re.compile(r"(?P<t>\d+:\d+(?::\d+)?(?:\.\d+)?)\s*elapsed")

# POSIX time format includes:
# real 0m0.123s
POSIX_REAL_RE = re.compile(r"^\s*real\s+(?P<m>\d+)m(?P<s>\d+(?:\.\d+)?)s\s*$")

def parse_hms_like_to_seconds(t: str) -> float:
    """
    Converts:
      - M:SS(.sss)
      - H:MM:SS(.sss)
    to seconds.
    """
    parts = t.split(":")
    if len(parts) == 2:
        m = int(parts[0])
        s = float(parts[1])
        return m * 60.0 + s
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
        return h * 3600.0 + m * 60.0 + s
    # Fallback: try float
    return float(t)

def population_variance(xs):
    if not xs:
        return 0.0
    mu = mean(xs)
    return sum((x - mu) ** 2 for x in xs) / len(xs)

def extract_times(log_path: str):
    times = {}  # program -> [seconds]
    current_prog = None

    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            # Detect program section banner
            m = BANNER_RE.search(line)
            if m:
                current_prog = m.group(1)
                times.setdefault(current_prog, [])
                continue

            if current_prog is None:
                continue

            # Try GNU elapsed style first: "... 0:00.12elapsed ..."
            g = GNU_ELAPSED_RE.search(line)
            if g:
                sec = parse_hms_like_to_seconds(g.group("t"))
                times[current_prog].append(sec)
                continue

            # Try POSIX real style: "real 0m0.123s"
            p = POSIX_REAL_RE.match(line)
            if p:
                sec = int(p.group("m")) * 60.0 + float(p.group("s"))
                times[current_prog].append(sec)
                continue

    return times

def write_csv(times_by_prog, out_csv_path: str):
    with open(out_csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["programname", "avg_time_seconds", "variance_time_seconds2"])

        for prog in sorted(times_by_prog.keys()):
            xs = times_by_prog[prog]
            if xs:
                avg = mean(xs)
                var = population_variance(xs)
            else:
                avg = 0.0
                var = 0.0
            w.writerow([prog, f"{avg:.6f}", f"{var:.6f}"])

def main():
    if len(sys.argv) < 3:
        print("Usage: python parse_bench_log.py <logfile.txt> <output.csv>", file=sys.stderr)
        sys.exit(2)

    log_path = sys.argv[1]
    out_csv = sys.argv[2]

    times_by_prog = extract_times(log_path)

    # Helpful warning if nothing was parsed
    total = sum(len(v) for v in times_by_prog.values())
    if total == 0:
        print("Warning: No timings found. Ensure your log contains GNU '...elapsed' or POSIX 'real XmY.s' lines.",
              file=sys.stderr)

    write_csv(times_by_prog, out_csv)

if __name__ == "__main__":
    main()