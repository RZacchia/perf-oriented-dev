#!/usr/bin/env python3
"""Builds (optional) and runs a sample executable, appending timing/output to CSV.

Usage examples:
  # build + run once, write to results.csv
  python3 run_and_csv.py --build --runs 1 --output results.csv

  # just run 5 times
  python3 run_and_csv.py --runs 5 --output results.csv
"""
from __future__ import annotations

import argparse
import csv
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict


def run_cmd(cmd, cwd: Path, env=None, check=True):
    return subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, check=check)


def ensure_build(build_dir: Path) -> None:
    build_dir.mkdir(parents=True, exist_ok=True)
    print(f"Configuring in {build_dir}")
    subprocess.run(["cmake", "..", "-G", "Ninja", "-DCMAKE_BUILD_TYPE=Release"], cwd=str(build_dir), check=True)
    print("Building...")
    subprocess.run(["ninja"], cwd=str(build_dir), check=True)


def run_and_record(exe_path: Path, build_dir: Path, out_csv: Path, runs: int, env_vars: Dict[str, str]):
    header = ["timestamp_utc", "hostname", "exe", "run_index", "elapsed_s", "returncode", "stdout", "stderr"]
    file_exists = out_csv.exists()

    with out_csv.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writeheader()

        for i in range(1, runs + 1):
            ts = datetime.utcnow().isoformat() + "Z"
            hostname = socket.gethostname()
            start = time.perf_counter()
            try:
                proc = run_cmd([str(exe_path)], cwd=build_dir, env=env_vars, check=False)
                elapsed = time.perf_counter() - start
                row = {
                    "timestamp_utc": ts,
                    "hostname": hostname,
                    "exe": exe_path.name,
                    "run_index": i,
                    "elapsed_s": f"{elapsed:.6f}",
                    "returncode": proc.returncode,
                    "stdout": proc.stdout.strip(),
                    "stderr": proc.stderr.strip(),
                }
            except Exception as e:  # unexpected failure
                elapsed = time.perf_counter() - start
                row = {
                    "timestamp_utc": ts,
                    "hostname": hostname,
                    "exe": exe_path.name,
                    "run_index": i,
                    "elapsed_s": f"{elapsed:.6f}",
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"exception: {e}",
                }

            writer.writerow(row)
            print(f"Run {i}/{runs}: elapsed={row['elapsed_s']}s code={row['returncode']}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--build", action="store_true", help="Run CMake + ninja before executing")
    p.add_argument("--runs", type=int, default=1, help="Number of times to run the executable")
    p.add_argument("--exe", default="mmul", help="Executable name in the build dir")
    p.add_argument("--build-dir", default=None, help="Path to build dir (default: ./build)")
    p.add_argument("--output", default="mmul_results.csv", help="CSV output path")
    p.add_argument("--threads", type=int, default=1, help="Set OMP_NUM_THREADS")
    args = p.parse_args()

    script_dir = Path(__file__).resolve().parent
    build_dir = Path(args.build_dir) if args.build_dir else script_dir / "build"
    out_csv = Path(args.output)
    exe_path = build_dir / args.exe

    env = dict(**subprocess.os.environ)
    env["OMP_NUM_THREADS"] = str(args.threads)

    if args.build:
        ensure_build(build_dir)

    if not exe_path.exists() or not exe_path.is_file():
        print(f"Executable not found: {exe_path}", file=sys.stderr)
        sys.exit(2)

    run_and_record(exe_path, build_dir, out_csv, args.runs, env)


if __name__ == "__main__":
    main()
