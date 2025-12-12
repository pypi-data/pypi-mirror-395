# sg_series

**sg_series** is a Python sequence analyzer for detecting polynomial, geometric, logarithmic, and custom patterns (Fibonacci, Primes, AGP, Alternating, Harmonic). It can predict the next terms, extend sequences, and visualize patterns.

---

## Installation

```bash
pip install sg_series
```

---

## Features

- Polynomial pattern detection
- Geometric pattern detection
- Logarithmic pattern detection
- Custom pattern detection (Fibonacci, Primes, AGP, Alternating, Harmonic)
- Next-term prediction
- Sequence extension
- Sequence visualization
- Gap filling for incomplete sequences

---

## Usage

```python
from sg_series import *

seq = [1, 2, 3, 4, 5]

# Master analysis
res = analyze(seq, frac=False, format=True)
print(res)

# Single-mode analysis
poly_res = ply_analyze(seq)
geo_res = geo_analyze(seq)
log_res = log_analyze(seq)
cus_res = cus_analyze(seq)

# Predict next term
next_term = best_next(seq)

# Extend sequence
extended_seq = extend(seq, num=3)

# Fill missing gaps
seq_with_gaps = [1, None, 3, None, 5]
filled_seq = fill_gaps(seq_with_gaps)

# Visualization
plot(seq, num=3)
ply_plot(seq)
geo_plot(seq)
log_plot(seq)
```

---

### Public Functions Summary

| Function | Role |
|----------|------|
| `analyze` | Master function: runs polynomial, geometric, logarithmic, and custom analyzers. |
| `ply_analyze` | Detects polynomial pattern using finite differences. |
| `geo_analyze` | Detects geometric patterns using ratio-difference logic. |
| `log_analyze` | Detects logarithmic patterns. |
| `cus_analyze` | Runs custom pattern detectors (Fibonacci, Primes, AGP, Alternating, Harmonic). |
| `best_next` | Chooses the next term based on highest certainty analysis. |
| `extend` | Appends predicted terms to a sequence. |
| `fill_gaps` | Fills missing values (`None`) in a sequence. |
| `plot` | Overlays polynomial, logarithmic, and geometric plots. |
| `ply_plot` | Plots polynomial fit. |
| `geo_plot` | Plots geometric ratio fit. |
| `log_plot` | Plots logarithmic fit. |
| `help` | Returns help dictionary for all public functions.

