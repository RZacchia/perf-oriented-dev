#!/usr/bin/env python3
"""Plot benchmark medians from results_*.csv files grouped by process name."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt


def get_sort_key(opt_name: str) -> tuple[int, str]:
    if opt_name == "O2":
        return (0, "")
    elif opt_name == "O3":
        return (2, "")
    else:
        return (1, opt_name)


def collect_results(source_dir: Path) -> tuple[List[str], List[str], Dict[str, Dict[str, float]]]:
    paths = sorted(source_dir.glob("results_*.csv"), key=lambda p: get_sort_key(p.stem.replace("results_", "")))
    if not paths:
        raise FileNotFoundError("No results_*.csv files found in the current directory.")

    opt_labels: List[str] = []
    results: Dict[str, Dict[str, float]] = {}

    for path in paths:
        opt_name = path.stem.replace("results_", "")
        opt_labels.append(opt_name)

        with path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            if "name" not in reader.fieldnames or "median" not in reader.fieldnames:
                raise ValueError(f"{path.name} must include columns 'name' and 'median'.")

            for row in reader:
                name = row["name"].strip()
                median = float(row["median"])
                results.setdefault(name, {})[opt_name] = median

    return opt_labels, sorted(results.keys()), results


def plot_results(opt_labels: List[str], process_names: List[str], results: Dict[str, Dict[str, float]], output_path: Path) -> None:
    num_processes = len(process_names)
    ncols = 2 if num_processes > 4 else 1
    nrows = math.ceil(num_processes / ncols)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10 * ncols, 4 * nrows), squeeze=False)
    axes_flat = [ax for row in axes for ax in row]

    colors = plt.get_cmap("tab20")(range(len(opt_labels)))

    for index, process_name in enumerate(process_names):
        ax = axes_flat[index]
        values = [results[process_name].get(opt, float("nan")) for opt in opt_labels]
        ax.bar(opt_labels, values, color=colors, edgecolor="black")
        ax.set_title(process_name)
        ax.set_xlabel("Optimization flag")
        ax.grid(axis="y", linestyle="--", alpha=0.7, linewidth=0.5)
        ax.set_xticklabels(opt_labels, rotation=45, ha='right')

        # Set ylim to make differences visible
        valid_values = [v for v in values if not math.isnan(v)]
        if valid_values:
            ax.set_ylim(bottom=min(valid_values) * 0.9)

        if index % ncols == 0:
            ax.set_ylabel("Median execution time")

    for ax in axes_flat[num_processes:]:
        ax.axis("off")

    fig.suptitle("Benchmark medians by optimization flag", fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=200)
    print(f"Saved plot to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot results_O*.csv files by benchmark process name.")
    parser.add_argument("--dir", default=".", help="Directory containing results_O*.csv files.")
    parser.add_argument("--output", default="results_optimization_flags_2.png", help="Output image path.")
    args = parser.parse_args()

    source_dir = Path(args.dir).resolve()
    output_path = Path(args.output).resolve()

    opt_labels, process_names, results = collect_results(source_dir)
    plot_results(opt_labels, process_names, results, output_path)


if __name__ == "__main__":
    main()
