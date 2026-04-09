# Performance Comparison: SSCA2 vs NPB-BT-A

| Metric | SSCA2 | NPB-BT-A |
|--------|-------|----------|
| L1-dcache-load-misses | 38.54% (±0.02%) | 3.98% (±0.11%) |
| L1-dcache-store-misses | 24.75% (±0.00%) | 3.20% (±0.04%) |
| L1-dcache-prefetch-misses | 74.07% (±0.08%) | 37.95% (±0.24%) |
| L1-icache-load-misses | 0.00% (±7.41%) | 0.04% (±1.60%) |
| LLC-load-misses | 10.38% (±0.51%) | 49.23% (±0.32%) |
| LLC-store-misses | 2.11% (±0.94%) | 6.24% (±3.28%) |
| LLC-prefetch-misses | 21.45% (±3.64%) | 62.39% (±0.73%) |
| dTLB-load-misses | 13.50% (±0.23%) | 0.00% (±0.78%) |
| dTLB-store-misses | 10.85% (±0.24%) | 0.0005% (±0.38%) |
| iTLB-load-misses | 0.00% (±8.01%) | 0.00% (±8.95%) |
| node-load-misses | 0.0006% (±40.91%) | 0.0015% (±14.33%) |
| node-store-misses | 0.00% (±0%) | 0.00% (±0%) |
| node-prefetch-misses | 0.008% (±87.61%) | 0.0004% (±337.91%) |
| branch-load-misses | 200.40% (±0.29%) | 74.33% (±0.33%) |


## Execution Time Comparison

| Run / Counter group | SSCA2 | NPB-BT-A |
|---|---|---|
| L1-dcache | `32.1512 ±0.0514 s` | `76.023 ±0.146 s` |
| L1-icache | `32.317 ±0.179 s` | `76.382 ±0.502 s` |
| LLC | `32.213 ±0.252 s` | `76.476 ±0.135 s` |
| LLC-prefetch | `32.093 ±0.313 s` | `76.002 ±0.118 s` |
| dTLB | `32.2115 ±0.0336 s` | `76.037 ±0.178 s` |
| iTLB | `29.18 ±1.85 s` | `76.947 ±0.724 s` |
| node | `32.4932 ±0.0339 s` | `76.597 ±0.132 s` |
| node-prefetch | `30.25 ±2.03 s` | `75.965 ±0.106 s` |
| branch | `31.431 ±0.734 s` | `76.035 ±0.234 s` |
| baseline (no counters) | `31.673 ±0.862 s` | `76.766 ±0.122 s` |

> The bottom lines are the no-counter baseline times you added: `31.673 ±0.862 s` for SSCA2 and `76.766 ±0.122 s` for NPB-BT-A.