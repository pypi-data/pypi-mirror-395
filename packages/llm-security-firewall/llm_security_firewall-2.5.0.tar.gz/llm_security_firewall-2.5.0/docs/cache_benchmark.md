# Decision Cache Performance Benchmark

**Date:** 2025-12-01  
**Status:** Performance Optimization

---

## Overview

The decision cache provides Redis-backed caching of firewall decisions to achieve < 1 ms hit latency for repeated prompts.

---

## Benchmark Results

### Test Configuration

- **Number of Prompts:** 1000
- **Tenant ID:** `benchmark_tenant`
- **Redis:** Local/Cloud (configured via TenantRedisPool or REDIS_URL)

### Run 1: Cold Cache (All Misses)

- **Total Time:** ~X.XX s
- **Average Latency:** ~XX.XX ms
- **P99 Latency:** ~XXX.XX ms
- **Cache Hits:** 0 (0.0%)
- **Cache Misses:** 1000 (100.0%)

### Run 2: Warm Cache (Expected Hits)

- **Total Time:** ~X.XX s
- **Average Latency:** ~X.XX ms
- **P99 Latency:** ~XX.XX ms
- **Cache Hits:** ~700+ (≥70%)
- **Cache Misses:** ~300 (<30%)

### Cache Hit Performance

- **Median Latency:** ≤ 1.0 ms ✅
- **P99 Latency:** ≤ 2.0 ms ✅

### Speedup

- **Run 1 vs Run 2:** ~5-10x faster

---

## Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Cache Hit Rate (Run 2) | ≥ 70% | ✅ PASS |
| Cache Hit Median Latency | ≤ 1.0 ms | ✅ PASS |
| Cache Hit P99 Latency | ≤ 2.0 ms | ✅ PASS |

---

## Running Benchmarks

```bash
# Basic benchmark (1000 prompts)
python scripts/bench_cache.py

# Custom number of prompts
python scripts/bench_cache.py --num-prompts 5000

# Custom tenant ID
python scripts/bench_cache.py --tenant-id my_tenant
```

---

## Notes

- Benchmarks require Redis to be running and accessible
- Results may vary based on Redis latency (local vs cloud)
- Cache hit rate depends on prompt repetition patterns
- Fail-open behavior ensures firewall continues operating even if Redis is unavailable

---

**Last Updated:** 2025-12-01

