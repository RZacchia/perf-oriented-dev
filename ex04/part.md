## Overview of Hardware cache event counters

### L1 Data Cache (L1-dcache)

- L1-dcache-loads: Number of loads (reads) from main memory into the L1 data cache
- L1-dcache-load-misses: Data cache misses on load operations (data not in L1, must fetch from higher cache levels)
- L1-dcache-stores: Number of stores (writes) to the L1 data cache
- L1-dcache-store-misses: Data cache misses on store operations
- L1-dcache-prefetches: Hardware prefetch requests for the L1 data cache (automatic data fetching ahead of time)
- L1-dcache-prefetch-misses: Prefetch requests that failed to find data in L1
- L1 Instruction Cache (L1-icache)
- L1-icache-loads: Number of instruction fetches from the L1 instruction cache
- L1-icache-load-misses: Instruction cache misses (instruction not in L1, must fetch from higher cache levels)

### Last-Level Cache (LLC) — typically L3 cache

- LLC-loads: Loads from the last-level cache (when L1 misses)
- LLC-load-misses: Misses in the last-level cache (must go to main memory)
- LLC-stores: Stores to the last-level cache
- LLC-store-misses: Store misses in the last-level cache
- LLC-prefetches: Hardware prefetch requests for the LLC
- LLC-prefetch-misses: LLC prefetch requests that failed

### Data TLB (dTLB) — Translation Lookaside Buffer for data access

- dTLB-loads: Virtual-to-physical address translations for loads
- dTLB-load-misses: Address translation misses on loads (must walk page tables)
- dTLB-stores: Virtual-to-physical address translations for stores
- dTLB-store-misses: Address translation misses on stores

### Instruction TLB (iTLB)

- iTLB-loads: Virtual-to-physical address translations for instruction fetches
- iTLB-load-misses: Address translation misses for instructions

### NUMA Node Counters — for multi-socket systems

- node-loads: Memory loads from the local NUMA node
- node-load-misses: Loads that had to access remote NUMA nodes
- node-stores: Memory stores to the local NUMA node
- node-store-misses: Stores to remote NUMA nodes
- node-prefetches: Prefetch requests on local node
- node-prefetch-misses: Prefetches that missed locally

### Branch Prediction

- branch-loads: Total branch instructions executed
- branch-load-misses: Branch prediction misses (incorrect predictions requiring pipeline flushes)
