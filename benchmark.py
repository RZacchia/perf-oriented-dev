"""Build + run C benchmarks and emit a CSV for violin plots.

This is designed to match the style of `job.sh` in this repo:
- One build step for everything (e.g. `cmake && ninja`).
- Repeated runs of each benchmark using `/bin/time -f "%e %U %S %P %M"`.
- Outputs a CSV suitable for downstream plotting.

Config example (bench.json):

{
  "build": [
    "cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release",
    "ninja"
  ],
  "benchmarks": [
    {"name": "delannoy", "cmd": ["./delannoy", "13"], "cwd": "small_samples/build"},
    {"name": "filegen", "cmd": ["./filegen", "3", "40", "1024", "1048576"], "cwd": "small_samples/build"},
    {"name": "mmul", "cmd": "./mmul", "cwd": "small_samples/build"}
  ]
}

Usage:
  python benchmark.py --config bench.json --out results.csv --runs 15 --warmups 1

Output CSV columns:
  benchmark, run, wall_s, user_s, sys_s, cpu_pct, max_rss_kb, command
"""

from __future__ import annotations

import argparse
import csv
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

TimeOutputValues = Tuple[float, float, float, float, int]
VarianceValues = Tuple[float, float, float, float, float]
StdDeviationValues = Tuple[float, float, float, float, float]


def _parse_time_output(output: str) -> TimeOutputValues:
    """Parse `/bin/time -f "%e %U %S %P %M"` output.

    Returns (real_s, user_s, sys_s, cpu_pct, max_rss_kb).
    """

    parts = output.strip().split()
    if len(parts) < 5:
        raise ValueError(f"Unexpected /bin/time output: {output!r}")

    real_s, user_s, sys_s, cpu_s, mem_s = parts[-5:]
    cpu_pct = float(cpu_s.rstrip("%"))
    return float(real_s), float(user_s), float(sys_s), cpu_pct, int(mem_s)


def _run_cmd(
    cmd: Union[str, Sequence[str]],
    cwd: Optional[Path] = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess:
    if isinstance(cmd, str):
        return subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            check=True,
            capture_output=capture_output,
            text=True,
        )

    return subprocess.run(
        list(cmd),
        cwd=cwd,
        shell=False,
        check=True,
        capture_output=capture_output,
        text=True,
    )


def _build_all(build_cmds: List[Union[str, Sequence[str]]], cwd: Optional[Path]) -> None:
    if not build_cmds:
        return

    print("[build] Running build steps...")
    for cmd in build_cmds:
        print(f"[build] $ {cmd}")
        _run_cmd(cmd, cwd=cwd)

def _compute_percent_dev(values: List[float]) -> float:
    
    n = len(values)
    if n == 0:
        return (0.0, 0.0, 0.0, 0.0, 0.0)

    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    stddev = variance ** 0.5
    cv_percent = (stddev / mean * 100) if mean != 0 else 0
    return cv_percent

def _run_benchmark(
    name: str,
    cmd: Union[str, Sequence[str]],
    cwd: Optional[Path],
    target_std_dev: float,
    warmups: int,
) -> Tuple[List[Dict[str, Any]], VarianceValues]:
    if warmups > 0:
        print(f"[{name}] Warmup: {warmups} run(s)")
        for _ in range(warmups):
            _run_once(name, cmd, cwd, record=False)

    minimum_runs = 10
    rows: List[Dict[str, Any]] = []
    running_var: VarianceValues = (0.0, 0.0, 0.0, 0.0, 0.0)
    target_std_devs: VarianceValues = (target_std_dev,) * 5 

    i = 1
    max_i = 15
    while i <= max_i:  # hard cap to prevent infinite loops
        print(f"[{name}] Run {i}")
        row = _run_once(name, cmd, cwd, record=True)
        if row:
            row["run"] = i
            rows.append(row)

            wall_s_values = [r["wall_s"] for r in rows]
            user_s_values = [r["user_s"] for r in rows]
            sys_s_values = [r["sys_s"] for r in rows]
            cpu_pct_values = [r["cpu_pct"] for r in rows]
            max_rss_kb_values = [r["max_rss_kb"] for r in rows]

            running_var = (
                _compute_percent_dev(wall_s_values),
                _compute_percent_dev(user_s_values),
                _compute_percent_dev(sys_s_values),
                _compute_percent_dev(cpu_pct_values),
                _compute_percent_dev(max_rss_kb_values),
            )

            print(f"[{name}] Variance after {i} runs: {running_var}")

            # Check if we've met the target variance for all metrics.
            if all(
                running_var[j] <= target_std_devs[j] for j in range(5)
            ) and i >= minimum_runs:
                print(f"[{name}] Target variance met after {i} runs.")
                break
            i += 1
    if i >= 100:
        print(f"[{name}] WARNING: Reached maximum runs without meeting target variance.")

    return rows, running_var



def _run_once(
    name: str,
    cmd: Union[str, Sequence[str]],
    cwd: Optional[Path],
    record: bool,
) -> Optional[Dict[str, Any]]:
    if isinstance(cmd, list):
        cmd_str = " ".join(shlex.quote(str(p)) for p in cmd)
    else:
        cmd_str = cmd

    def _find_time_line(proc: subprocess.CompletedProcess) -> Optional[str]:
        candidates: List[str] = []
        if proc.stderr:
            candidates.extend(proc.stderr.strip().splitlines())
        if proc.stdout:
            candidates.extend(proc.stdout.strip().splitlines())

        for line in candidates:
            line = line.strip()
            if not line:
                continue
            try:
                _parse_time_output(line)
                return line
            except ValueError:
                continue
        return None

    base_time_cmd: List[Union[str, Sequence[str]]] = [
        "/bin/time",
        "-f",
        "%e %U %S %P %M",
    ]

    if isinstance(cmd, list):
        base_time_cmd.extend(cmd)
    else:
        base_time_cmd.append(cmd)

    try:
        proc = _run_cmd(base_time_cmd, cwd=cwd, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"[{name}] ERROR: {e}", file=sys.stderr)
        return None

    line = _find_time_line(proc)

  
    if not line:
        # Provide the first few lines we saw to help debugging.
        seen = []
        if proc.stderr:
            seen.extend(proc.stderr.strip().splitlines())
        if proc.stdout:
            seen.extend(proc.stdout.strip().splitlines())
        raise RuntimeError(f"[{name}] /bin/time produced no recognizable output (saw: {seen!r})")

    wall_s, user_s, sys_s, cpu_pct, max_rss_kb = _parse_time_output(line)
    if not record:
        return None

    return {
        "benchmark": name,
        "wall_s": wall_s,
        "user_s": user_s,
        "sys_s": sys_s,
        "cpu_pct": cpu_pct,
        "max_rss_kb": max_rss_kb,
    }




def _write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fieldnames = [
        "benchmark",
        "run",
        "wall_s",
        "user_s",
        "sys_s",
        "cpu_pct",
        "max_rss_kb",
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def _write_vars(path: Path,names: List[str], runs: List[int], vars: List[VarianceValues]) -> None:
    
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["benchmark", "runs", "wall_s_var_pct", "user_s_var_pct", "sys_s_var_pct", "cpu_pct_var_pct", "max_rss_kb_var_pct"])
        for name, run, var in zip(names, runs, vars, strict=False):
            var_wall_s, var_user_s, var_sys_s, var_cpu_pct, var_max_rss_kb = var
            writer.writerow([name, run, var_wall_s, var_user_s, var_sys_s, var_cpu_pct, var_max_rss_kb])



def _load_config(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build + run C benchmarks and emit a CSV suitable for violin plots."
    )
    p.add_argument("--config", "-c", required=True, help="Path to JSON config file")
    p.add_argument("--out", "-o", required=True, help="Output CSV path")
    p.add_argument(
        "--std_dev",
        type=float,
        default=5.0,
        help="Target standard deviation in percent for each metric (after warmups)",
    )
    p.add_argument(
        "--warmups",
        type=int,
        default=1,
        help="Number of warmup runs per benchmark (not recorded)",
    )
    p.add_argument(
        "--no-build",
        action="store_true",
        help="Skip running the build steps (useful if already built)",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    opts = _parse_args(argv)
    cfg = _load_config(Path(opts.config))

    build_cmds = cfg.get("build") or []
    if isinstance(build_cmds, str):
        build_cmds = [build_cmds]

    global_cwd = cfg.get("cwd")
    global_cwd_path = Path(global_cwd) if global_cwd else None

    benches = cfg.get("benchmarks")
    if not isinstance(benches, list) or not benches:
        print("Config file must have a 'benchmarks' list", file=sys.stderr)
        return 2

    out_path = Path(opts.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not opts.no_build and build_cmds:
        _build_all(build_cmds, global_cwd_path)

    names: List[str] = []
    vars: List[VarianceValues] = []
    runs: List[int] = []
    all_rows: List[Dict[str, Any]] = []
    for bench in benches:
        name = bench.get("name")
        if not name:
            raise ValueError("Each benchmark needs a 'name'")
        names.append(name)

        cmd = bench.get("cmd")
        if cmd is None:
            raise ValueError(f"Benchmark {name!r} missing 'cmd'")

        bench_cwd = bench.get("cwd")
        cwd_path = Path(bench_cwd) if bench_cwd else global_cwd_path
        rows, var = _run_benchmark(name, cmd, cwd_path, target_std_dev=opts.std_dev, warmups=opts.warmups)
        all_rows.extend(rows)
        vars.append(var)
        runs.append(len(rows))


    _write_csv(out_path, all_rows)
    print(f"Wrote {len(all_rows)} rows to {out_path}")
    vars_out_path = out_path.with_suffix(".vars.csv")
    _write_vars(vars_out_path, names, runs, vars)
    print(f"Wrote {len(runs)} variance rows to {vars_out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
