# pomo-i18n Benchmark Suite

This document summarizes benchmark methodology and results related to plural-rule evaluation and translation lookup performance.

Benchmarks can be executed in two ways:

- `make bench` — microbench (timeit)
- `make bench-pytest` — pytest-benchmark suite

---

## Table of Contents

- [Purpose](#purpose)
- [Benchmark Environment](#benchmark-environment)
- [Micro Benchmark](#micro-benchmark)
- [Pytest Benchmark](#pytest-benchmark)
- [Plural Rule Evaluation](#plural-rule-evaluation)
- [Cache Backend Comparison](#cache-backend-comparison)
- [How to Reproduce](#how-to-reproduce)

---

## Purpose

The objective of these benchmarks is to measure:

- speed of plural-rule evaluation
- overhead of cache backend implementations
- cost of translation lookups (`gettext`, `ngettext`)

Plural evaluation is a hot path in gettext systems, and optimizing it
matters for large translation-heavy applications.

---

## Benchmark Environment

Default environment used for official measurements:

| Component        | Version          |
| ---------------- | ---------------- |
| Python           | 3.10.19          |
| OS               | macOS Tahoe 26.1 |
| Hardware         | Apple Silicon M4 |
| pytest-benchmark | 5.2.3            |

---

## Micro Benchmark

Run with:

```bash
make bench
```

Measures raw plural evaluation using timeit.

Example output format:

```
simple rule: 2.53 µs
complex rule: 4.84 µs
```

---

## Pytest Benchmark

```bash
make Pytest Benchmark
```

Generates full statistical results:

- mean / median
- IQR
- outliers
- ops/sec

Example table:

| Backend | Simple (µs) | Complex (µs) |
| ------- | ----------- | ------------ |
| none    | ~2.54       | ~4.83        |
| weak    | ~2.69       | ~4.89        |
| lru     | ~2.49       | ~4.92        |

---

## Plural Rule Evaluation

Plural rules are parsed and transformed into safe Python expressions,
then evaluated inside a controlled environment.

The benchmark covers:

- simple expressions (e.g. n != 1)
- complex ternary expressions

---

## Cache Backend Comparison

The default backend is LRU cache, implemented using functools.lru_cache.

Backends:

| Backend  | Notes                   |
| -------- | ----------------------- |
| **none** | no caching, slowest     |
| **weak** | dict-based, lightweight |
| **lru**  | fastest overall         |

Switch via:

```bash
export PYPOMO_CACHE=lru
export PYPOMO_PLURAL_CACHE_SIZE=512
```

---

## How to Reproduce

```bash
make bench
make bench-pytest
```

---

## End of document
