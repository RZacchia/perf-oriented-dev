#!/usr/bin/env python3
"""Plot relative perf metrics from the first table in solution.md with error margins."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

labels = [
    "L1-dcache-load-misses",
    "L1-dcache-store-misses",
    "L1-dcache-prefetch-misses",
    "L1-icache-load-misses",
    "LLC-load-misses",
    "LLC-store-misses",
    "LLC-prefetch-misses",
    "dTLB-load-misses",
    "dTLB-store-misses",
    "iTLB-load-misses",
    "node-load-misses",
    "node-store-misses",
    "node-prefetch-misses",
    "branch-load-misses",
]

ssca2 = [38.54, 24.75, 74.07, 0.00, 10.38, 2.11, 21.45, 13.50, 10.85, 0.00, 0.0006, 0.00, 0.008, 200.40]
ssca2_err_pct = [0.02, 0.00, 0.08, 7.41, 0.51, 0.94, 3.64, 0.23, 0.24, 8.01, 40.91, 0.00, 87.61, 0.29]

npb_bt_a = [3.98, 3.20, 37.95, 0.04, 49.23, 6.24, 62.39, 0.00, 0.0005, 0.00, 0.0015, 0.00, 0.0004, 74.33]
npb_bt_a_err_pct = [0.11, 0.04, 0.24, 1.60, 0.32, 3.28, 0.73, 0.78, 0.38, 8.95, 14.33, 0.00, 337.91, 0.33]

ssca2_err = [value * pct / 100.0 for value, pct in zip(ssca2, ssca2_err_pct)]
npb_bt_a_err = [value * pct / 100.0 for value, pct in zip(npb_bt_a, npb_bt_a_err_pct)]

x = np.arange(len(labels))
bar_width = 0.35

fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(
    x - bar_width / 2,
    ssca2,
    bar_width,
    yerr=ssca2_err,
    capsize=4,
    label="SSCA2",
    color="#1f77b4",
    edgecolor="black",
)
ax.bar(
    x + bar_width / 2,
    npb_bt_a,
    bar_width,
    yerr=npb_bt_a_err,
    capsize=4,
    label="NPB-BT-A",
    color="#ff7f0e",
    edgecolor="black",
)

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_ylabel("Relative metric (%)")
ax.set_title("Relative Perf Metrics with Error Margins")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
output_path = Path(__file__).resolve().parent / "perf_relative_metrics.png"
plt.savefig(output_path, dpi=200)
print(f"Saved plot to: {output_path}")
