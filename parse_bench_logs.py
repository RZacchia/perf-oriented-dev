#!/usr/bin/env python3
"""Parse benchmark log files and produce a Markdown table and plots.

Usage:
  python3 parse_bench_logs.py local1.log -o out.md -p plots

Generates:
  - Markdown table with medians per container per block
  - PNG plots per `split` and a combined plot
"""
import re
import argparse
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt


SPLIT_RE = re.compile(r"split:\s*(?P<split>\d+)%?,\s*size:\s*(?P<size>\d+)\s*bytes,\s*elements:\s*(?P<elements>\d+)")
LINE_RE = re.compile(r"(?P<name>\S+)\s+median=(?P<median>[0-9.eE+-]+)\s*ms\s+stDev=(?P<stdev>[0-9.eE+-]+)\s*ms\s+operations=(?P<ops>\d+)")


def parse_log(path):
    entries = []
    cur = None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = SPLIT_RE.search(line)
            if m:
                if cur:
                    entries.append(cur)
                cur = {
                    "split": int(m.group("split")),
                    "size": int(m.group("size")),
                    "elements": int(m.group("elements")),
                    "containers": {},
                    "raw_lines": [],
                }
                continue
            if cur is None:
                continue
            m2 = LINE_RE.search(line)
            if m2:
                name = m2.group("name")
                median = float(m2.group("median"))
                stdev = float(m2.group("stdev"))
                ops = int(m2.group("ops"))
                cur["containers"][name] = {"median": median, "stdev": stdev, "ops": ops}
            else:
                cur.setdefault("raw_lines", []).append(line)
    if cur:
        entries.append(cur)
    return entries


def write_markdown(entries, outpath):
    # collect container names
    containers = sorted({c for e in entries for c in e["containers"].keys()})
    lines = []
    hdr = ["Split", "Size", "Elements"] + containers
    lines.append("| " + " | ".join(hdr) + " |")
    lines.append("|" + " --- |" * len(hdr))
    for e in entries:
        row = [str(e["split"]), str(e["size"]), str(e["elements"])]
        for c in containers:
            v = e["containers"].get(c)
            row.append(f"{v['median']:.6g}" if v else "")
        lines.append("| " + " | ".join(row) + " |")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text("\n".join(lines) + "\n")


def plot_entries(entries, plots_dir):
    plots_dir.mkdir(parents=True, exist_ok=True)
    # group by split
    by_split = defaultdict(list)
    for e in entries:
        by_split[e["split"]].append(e)

    containers = sorted({c for e in entries for c in e["containers"].keys()})

    # Combined plot: one line per container, points for all splits
    plt.figure(figsize=(10, 6))
    for c in containers:
        xs = []
        ys = []
        for e in entries:
            v = e["containers"].get(c)
            if v:
                xs.append(e["elements"])
                ys.append(v["median"])
        if xs:
            plt.scatter(xs, ys, label=c, s=30)
            # connect sorted by x
            xs_sorted, ys_sorted = zip(*sorted(zip(xs, ys)))
            plt.plot(xs_sorted, ys_sorted)
    plt.xscale("log")
    plt.xlabel("elements (log scale)")
    plt.ylabel("median (ms)")
    plt.title("Median latency vs elements (all splits)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    combined = plots_dir / "combined_plot.png"
    plt.tight_layout()
    plt.savefig(combined)
    plt.close()

    # Per-split plots
    for split, group in sorted(by_split.items()):
        plt.figure(figsize=(10, 6))
        for c in containers:
            xs = [e["elements"] for e in group if c in e["containers"]]
            ys = [e["containers"][c]["median"] for e in group if c in e["containers"]]
            if xs:
                xs_s, ys_s = zip(*sorted(zip(xs, ys)))
                plt.plot(xs_s, ys_s, marker='o', label=c)
        plt.xscale("log")
        plt.xlabel("elements (log scale)")
        plt.ylabel("median (ms)")
        plt.title(f"Median vs elements — split={split}%")
        plt.legend()
        plt.grid(True, which="both", ls="--", alpha=0.5)
        out = plots_dir / f"plot_split_{split}.png"
        plt.tight_layout()
        plt.savefig(out)
        plt.close()


def main():
    p = argparse.ArgumentParser(description="Parse benchmark log and produce MD + plots")
    p.add_argument("files", nargs="+", help="log file(s) to parse")
    p.add_argument("-o", "--output", default="bench_results.md", help="Markdown output path")
    p.add_argument("-p", "--plots", default="plots", help="Directory to save plots")
    args = p.parse_args()

    all_entries = []
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"Warning: {f} not found, skipping")
            continue
        entries = parse_log(path)
        if not entries:
            print(f"No benchmark blocks found in {f}")
        else:
            all_entries.extend(entries)

    if not all_entries:
        print("No data parsed. Exiting.")
        return

    outpath = Path(args.output)
    write_markdown(all_entries, outpath)
    print(f"Wrote Markdown table to {outpath}")

    plots_dir = Path(args.plots)
    plot_entries(all_entries, plots_dir)
    print(f"Saved plots to {plots_dir}")


if __name__ == "__main__":
    main()
