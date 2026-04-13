#!/usr/bin/env python3
"""Plot perf counter run-time differences to baseline with error margins."""

import math
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

baseline_ssca2 = 31.673
baseline_ssca2_err = 0.862

baseline_npbbt = 76.766
baseline_npbbt_err = 0.122

ssca2_delta = [value - baseline_ssca2 for value in ssca2]
ssca2_delta_err = [math.hypot(err, baseline_ssca2_err) for err in ssca2_err]

npb_bt_delta = [value - baseline_npbbt for value in npb_bt_a]
npb_bt_delta_err = [math.hypot(err, baseline_npbbt_err) for err in npb_bt_a_err]

x = range(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(
    [pos - width / 2 for pos in x],
    ssca2_delta,
    width,
    yerr=ssca2_delta_err,
    capsize=4,
    label="SSCA2",
    color="#1f77b4",
    edgecolor="black",
)
ax.bar(
    [pos + width / 2 for pos in x],
    npb_bt_delta,
    width,
    yerr=npb_bt_delta_err,
    capsize=4,
    label="NPB-BT-A",
    color="#ff7f0e",
    edgecolor="black",
)

ax.axhline(0, color="gray", linestyle="--", linewidth=1)
ax.set_xticks(list(x))
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_ylabel("Time difference to baseline (seconds)")
ax.set_title("Perf Counter Run-Time Difference to Baseline with Error Margins")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
output_path = Path(__file__).resolve().parent / "perf_diff_to_baseline.png"
plt.savefig(output_path, dpi=200)
print(f"Saved plot to: {output_path}")
