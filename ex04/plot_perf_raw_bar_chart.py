#!/usr/bin/env python3
"""Plot raw perf counter run times with error margins as grouped bars."""

from pathlib import Path
import matplotlib.pyplot as plt

labels = [
    "L1-dcache",
    "L1-icache",
    "LLC",
    "LLC-prefetch",
    "dTLB",
    "iTLB",
    "node",
    "node-prefetch",
    "branch",
    "baseline (no counters)",
]

ssca2 = [32.1512, 32.317, 32.213, 32.093, 32.2115, 29.18, 32.4932, 30.25, 31.431, 31.673]
ssca2_err = [0.0514, 0.179, 0.252, 0.313, 0.0336, 1.85, 0.0339, 2.03, 0.734, 0.862]

npb_bt_a = [76.023, 76.382, 76.476, 76.002, 76.037, 76.947, 76.597, 75.965, 76.035, 76.766]
npb_bt_a_err = [0.146, 0.502, 0.135, 0.118, 0.178, 0.724, 0.132, 0.106, 0.234, 0.122]

x = range(len(labels))
bar_width = 0.35

fig, ax = plt.subplots(figsize=(14, 7))
ax.bar(
    [pos - bar_width / 2 for pos in x],
    ssca2,
    bar_width,
    yerr=ssca2_err,
    capsize=4,
    label="SSCA2",
    color="#1f77b4",
    edgecolor="black",
)
ax.bar(
    [pos + bar_width / 2 for pos in x],
    npb_bt_a,
    bar_width,
    yerr=npb_bt_a_err,
    capsize=4,
    label="NPB-BT-A",
    color="#ff7f0e",
    edgecolor="black",
)

ax.set_xticks(list(x))
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_ylabel("Execution time (seconds)")
ax.set_title("Perf Counter Run Times with Error Margins")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
output_path = Path(__file__).resolve().parent / "perf_raw_bar_chart.png"
plt.savefig(output_path, dpi=200)
print(f"Saved plot to: {output_path}")
