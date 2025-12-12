#sg_series: Sequence Analyzer
#Author: Shivang Gupta
#Version: 1.0.0
#Description: A comprehensive sequence analyzer with polynomial, geometric, logarithmic, and custom pattern detection.

import math
import json
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np

EPS = 1e-12

# ---------------------------
# Helpers / formatting
# ---------------------------

class FractionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Fraction):
            if o.denominator == 1:
                return o.numerator
            return f"{o.numerator}/{o.denominator}"
        return super().default(o)

def _safe_frac(x, frac):
    if x is None:
        return None
    try:
        return Fraction(x).limit_denominator() if frac else float(f"{float(x):.5f}")
    except Exception:
        return x

# ---------------------------
# Polynomial (difference-based) analyzer (compact)
# ---------------------------

def _compute_certainty(std_coef, frac):
    if not std_coef:
        return 0.0
    cert = 0.0
    for c in std_coef:
        try:
            f = Fraction(c).limit_denominator(1000 if not frac else 10**9)
            cert += 1 / f.denominator
        except Exception:
            pass
    return cert / len(std_coef)

def _poly_analyze(seq, frac=False):
    seq = [float(x) for x in seq]
    n = len(seq)
    if n < 2:
        return {"deg": None, "nwt_coef": [], "std_coef": [], "nwt_str": "", "std_str": "", "next_term": None, "certainty": 0.0}
    table = [seq[:]]
    while len(table[-1]) > 1:
        prev = table[-1]
        diff = [prev[i+1] - prev[i] for i in range(len(prev)-1)]
        table.append(diff)

    deg = None
    for k, row in enumerate(table[1:], start=1):
        if all(abs(row[i] - row[0]) <= EPS for i in range(len(row))):
            deg = k
            break
    if deg is None:
        deg = len(seq) - 1 if len(seq) >= 2 else None

    ext = [r[:] for r in table]
    ext[deg].append(ext[deg][0])  
    for i in range(deg-1, -1, -1):
        ext[i].append(ext[i][-1] + ext[i+1][-1])
    next_term = ext[0][-1]

    nwt_coef = [r[0] for r in table[:deg+1]]

    std_coef = _newton_to_standard(nwt_coef) if len(nwt_coef) > 0 else []

    certainty = 0.0
    if std_coef:
        total = 0.0
        for c in std_coef:
            try:
                f = Fraction(c).limit_denominator(1000 if not frac else 10**9)
                total += 1 / f.denominator
            except Exception:
                pass
        certainty = total / len(std_coef)

    return {
        "deg": deg,
        "nwt_coef": [_safe_frac(c, frac) for c in nwt_coef],
        "std_coef": [_safe_frac(c, frac) for c in std_coef],
        "nwt_str": _newton_str(nwt_coef, frac),
        "std_str": _standard_str(std_coef, frac),
        "next_term": _safe_frac(next_term, frac),
        "certainty": float(f"{certainty:.5f}")
    }

def _poly_mul(p, q):
    if not p or not q:
        return []
    res = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            res[i+j] += a * b
    return res

def _newton_to_standard(coeffs):
    std = [0.0]
    for k, ck in enumerate(coeffs):
        if abs(ck) <= EPS:
            continue
        fall = [1.0]
        for i in range(k):
            fall = _poly_mul(fall, [-i, 1.0])
        fall = [c * ck / math.factorial(k) for c in fall]
        if len(fall) > len(std):
            std += [0.0] * (len(fall) - len(std))
        for idx, val in enumerate(fall):
            std[idx] += val
    while len(std) > 1 and abs(std[-1]) <= EPS:
        std.pop()
    return std

def _newton_str(coeffs, frac):
    terms = []
    for k, c in enumerate(coeffs):
        if abs(c) <= EPS:
            continue
        if k == 0:
            terms.append(_fmt(c, frac))
        else:
            prod = "".join([f"*(n - {i})" for i in range(k)])
            terms.append(f"{_fmt(c, frac)}{prod}")
    return " + ".join(terms) if terms else "0"

def _standard_str(std, frac):
    terms = []
    for i, c in enumerate(std):
        if abs(c) <= EPS:
            continue
        if i == 0:
            terms.append(_fmt(c, frac))
        elif i == 1:
            terms.append(f"{_fmt(c, frac)}*n")
        else:
            terms.append(f"{_fmt(c, frac)}*n^{i}")
    return " + ".join(terms) if terms else "0"

def _fmt(c, frac=False):
    if frac:
        f = Fraction(c).limit_denominator()
        if f.denominator == 1:
            return f"({f.numerator})"
        return f"({f.numerator}/{f.denominator})"
    return f"{float(c):.5f}"

# ---------------------------
# Geometric analyzer 
# ---------------------------

def _geometric_ratios(seq):
    r = []
    for i in range(1, len(seq)):
        if abs(seq[i-1]) <= EPS:
            r.append(float("nan"))
        else:
            r.append(seq[i] / seq[i-1])
    return r

def _geometric_analyze(seq, frac=False):
    ratios = _geometric_ratios(seq)
    clean = [x for x in ratios if not math.isnan(x)]
    if len(clean) < 2:
        return {"deg": None, "nwt_coef": [], "std_coef": [], "nwt_str": "", "std_str": "", "next_term": None, "certainty": 0.0}

    poly = _poly_analyze(clean, frac)
    try:
        pred_ratio = float(poly["next_term"])
    except Exception:
        pred_ratio = None

    if pred_ratio is None:
        next_term = None
    else:
        next_term = seq[-1] * pred_ratio

    certainty = poly.get("certainty", 0.0)

    return {
        "deg": poly["deg"],
        "nwt_coef": poly["nwt_coef"],
        "std_coef": poly["std_coef"],
        "nwt_str": poly["nwt_str"],
        "std_str": poly["std_str"],
        "next_term": _safe_frac(next_term, frac),
        "certainty": float(f"{certainty:.5f}")
    }

# ---------------------------
# Log analyzer
# ---------------------------

def _log_analyze(seq, frac=False):
    log_seq = [math.log(v) if v > 0 else float("nan") for v in seq]
    clean = [x for x in log_seq if not math.isnan(x)]
    if len(clean) < 2:
        return {"deg": None, "nwt_coef": [], "std_coef": [], "nwt_str": "", "std_str": "", "next_term": None, "certainty": 0.0}
    coeffs_newton = []
    poly = _poly_analyze(clean, frac)
    if poly["next_term"] is None:
        return {"deg": None, "nwt_coef": [], "std_coef": [], "nwt_str": "", "std_str": "", "next_term": None, "certainty": 0.0}
    try:
        next_log = float(poly["next_term"])
        next_term = math.exp(next_log)
    except Exception:
        return {"deg": None, "nwt_coef": [], "std_coef": [], "nwt_str": "", "std_str": "", "next_term": None, "certainty": 0.0}

    return {
        "deg": poly["deg"],
        "nwt_coef": poly["nwt_coef"],
        "std_coef": poly["std_coef"],
        "nwt_str": poly["nwt_str"],
        "std_str": poly["std_str"],
        "next_term": _safe_frac(next_term, frac),
        "certainty": poly.get("certainty", 0.0)
    }

# ---------------------------
# CUSTOM detectors (prime, fibonacci, agp, alternating, harmonic)
# ---------------------------

def _is_prime(n):
    if n <= 1 or n != int(n):
        return False
    n = int(n)
    if n <= 3:
        return n > 1
    if n % 2 == 0:
        return False
    r = int(math.isqrt(n))
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

def _detect_fibonacci(seq):
    if len(seq) < 3:
        return {"name": "Fibonacci", "certainty": 0.0, "next_term": None}
    matches = 0
    for i in range(2, len(seq)):
        if abs(seq[i] - (seq[i-1] + seq[i-2])) <= 1e-9:
            matches += 1
    certainty = matches / (len(seq) - 2)
    next_term = seq[-1] + seq[-2] if certainty > 0 else None
    return {"name": "Fibonacci", "certainty": float(f"{certainty:.5f}"), "next_term": _safe_frac(next_term, False)}

def _detect_primes(seq):
    int_flags = [abs(x - round(x)) <= 1e-9 for x in seq]
    if not all(int_flags):
        primes = 0
        total = len(seq)
        for x in seq:
            if _is_prime(x):
                primes += 1
        certainty = primes / total
        return {"name": "Primes", "certainty": float(f"{certainty:.5f}"), "next_term": None}
    else:
        primes = [int(x) for x in seq if _is_prime(x)]
        certainty = len(primes) / len(seq)
        next_term = None
        if certainty == 1.0:
            candidate = int(seq[-1]) + 1
            while not _is_prime(candidate):
                candidate += 1
            next_term = candidate
        return {"name": "Primes", "certainty": float(f"{certainty:.5f}"), "next_term": next_term}

def _cus_fibonacci(seq, frac=False):
    return _detect_fibonacci(seq)

def _cus_prime(seq, frac=False):
    return _detect_primes(seq)

def _cus_agp(seq, frac=False):
    """
    Detect arithmetic-geometric progression (AGP):
    a_n = a*r^(n-1) + d*(n-1)
    """
    if len(seq) < 3:
        return {"name": "AGP", "certainty": 0.0, "next_term": None}

    diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    ratios = [diffs[i+1]/diffs[i] if abs(diffs[i])>EPS else 0 for i in range(len(diffs)-1)]

    avg_ratio = sum(ratios)/len(ratios)
    if all(abs(r - avg_ratio) < 1e-3 for r in ratios):
        r = avg_ratio

        next_diff = diffs[-1]*r
        next_term = seq[-1] + next_diff
        return {"name": "AGP", "certainty": 0.9, "next_term": _safe_frac(next_term, frac)}

    return {"name": "AGP", "certainty": 0.0, "next_term": None}


def _cus_alternating(seq, frac=False):
    if len(seq) < 4:
        return {"name": "Alternating", "certainty": 0.0, "next_term": None}

    even = seq[0::2]
    odd = seq[1::2]

    res_even = analyze(even, frac)
    res_odd  = analyze(odd, frac)

    be = res_even["Cus"]["best"] if "Cus" in res_even else {"certainty": 0.0, "next_term": None}
    bo = res_odd["Cus"]["best"]  if "Cus" in res_odd  else {"certainty": 0.0, "next_term": None}

    if be.get("certainty", 0) > 0.7 and bo.get("certainty", 0) > 0.7:

        nxt = be["next_term"] if len(seq) % 2 == 0 else bo["next_term"]
        certainty = (be['certainty'] + bo['certainty']) / 2
        return {"name": "Alternating", "certainty": float(f"{certainty:.5f}"), "next_term": _safe_frac(nxt, frac)}

    return {"name": "Alternating", "certainty": 0.0, "next_term": None}

def _cus_harmonic(seq, frac=False):
    if any(x == 0 for x in seq):
        return {"name": "Harmonic", "certainty": 0.0, "next_term": None}
    inv = [1.0/x for x in seq]
    poly = _poly_analyze(inv, frac)
    nxt_inv = poly.get("next_term", None)
    if nxt_inv in (None, 0):
        return {"name": "Harmonic", "certainty": 0.0, "next_term": None}
    try:
        return {"name": "Harmonic", "certainty": poly.get("certainty", 0.0), "next_term": _safe_frac(1.0 / float(nxt_inv), frac)}
    except Exception:
        return {"name": "Harmonic", "certainty": 0.0, "next_term": None}

def _cus_detect(seq, frac=False):
    detectors = [
        _cus_fibonacci,
        _cus_prime,
        _cus_agp,
        _cus_alternating,
        _cus_harmonic
    ]
    detections = []
    best = {"name": None, "certainty": 0.0, "next_term": None}
    for d in detectors:
        out = d(seq, frac)
        detections.append(out)
        if out.get("certainty", 0.0) > best.get("certainty", 0.0):
            best = out
    return {"detections": detections, "best": best}

# ---------------------------
# Public analyze 
# ---------------------------

def analyze(seq, frac=False, format=False, precise=False, cutoff=0.9):
    if len(seq) < 2:
        return {"Error": "sequence too short"}
    seqf = [float(x) for x in seq]

    Ply = _poly_analyze(seqf, frac)
    Geo = _geometric_analyze(seqf, frac)
    Log = _log_analyze(seqf, frac)
    Cus = _cus_detect(seqf, frac)

    result = {"Ply": Ply, "Geo": Geo, "Log": Log, "Cus": Cus}

    if not precise:
        if format:
            return json.dumps(result, indent=2, cls=FractionEncoder)
        return result

    filtered = {}
    for key in ["Ply", "Geo", "Log"]:
        block = result[key]
        if isinstance(block, dict) and block.get("certainty", 0) >= cutoff:
            filtered[key] = block

    det = [d for d in Cus["detections"] if d.get("certainty", 0) == 1.0]
    if det:
        filtered["Cus"] = {"detections": det}

    if format:
        return json.dumps(filtered, indent=2, cls=FractionEncoder)
    return filtered

# ---------------------------
# Public single-mode wrappers 
# ---------------------------

def ply_analyze(seq, frac=False, format=False):
    if len(seq) < 2:
        return {"Error": "sequence too short"}
    res = _poly_analyze([float(x) for x in seq], frac)
    if format:
        return json.dumps(res, indent=2, cls=FractionEncoder)
    return res

def geo_analyze(seq, frac=False, format=False):
    if len(seq) < 2:
        return {"Error": "sequence too short"}
    res = _geometric_analyze([float(x) for x in seq], frac)
    if format:
        return json.dumps(res, indent=2, cls=FractionEncoder)
    return res

def log_analyze(seq, frac=False, format=False):
    if len(seq) < 2:
        return {"Error": "sequence too short"}
    res = _log_analyze([float(x) for x in seq], frac)
    if format:
        return json.dumps(res, indent=2, cls=FractionEncoder)
    return res

def cus_analyze(seq, frac=False, format=False):
    if len(seq) < 2:
        return {"Error": "sequence too short"}
    res = _cus_detect([float(x) for x in seq], frac)
    if format:
        return json.dumps(res, indent=2, cls=FractionEncoder)
    return res

# ---------------------------
# helper utilities: best_next, extend
# ---------------------------

def best_next(seq, frac=False):
    out = analyze(seq, frac=frac)
    # when analyze returns error
    if isinstance(out, dict) and out.get("Error"):
        return None
    candidates = []
    for k in ["Ply", "Geo", "Log"]:
        block = out.get(k)
        if isinstance(block, dict) and block.get("next_term") is not None:
            candidates.append((block.get("certainty", 0.0), block.get("next_term")))
    # cus best
    cus = out.get("Cus")
    if cus and "best" in cus and cus["best"].get("next_term") is not None:
        candidates.append((cus["best"].get("certainty", 0.0), cus["best"].get("next_term")))

    if not candidates:
        return None
    # choose highest certainty; if tie pick first
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]

def extend(seq, num=1, frac=False):
    s = list(seq)
    for _ in range(num):
        nxt = best_next(s, frac=frac)
        if nxt is None:
            return None
        if frac and isinstance(nxt, Fraction):
            s.append(nxt)         # keep fraction
        else:
            s.append(float(nxt))  # fallback to float
    return s

def ply_plot(seq, num=0, frac=False, smooth=100):
    res = _poly_analyze(seq, frac)
    if res.get("deg") is None:
        print("Cannot analyze sequence as polynomial.")
        return

    # Original points
    n_vals = np.arange(len(seq))
    y_vals = np.array(seq, dtype=float)

    # Predicted next points using polynomial coefficients
    poly_coeffs = res["std_coef"]
    next_n = np.arange(len(seq), len(seq)+num)
    next_y = []
    for n in next_n:
        val = sum(c * n**i for i, c in enumerate(poly_coeffs))
        next_y.append(val)

    # Full x and y for plotting smooth curve
    x_full = np.linspace(0, len(seq)+num-1, smooth)
    y_full = np.polyval(list(reversed(poly_coeffs)), x_full)  # np.polyval expects highest degree first

    plt.figure(figsize=(8,5))
    plt.plot(x_full, y_full, label="Polynomial Fit", color="blue")
    plt.scatter(n_vals, y_vals, color="red", label="Original Points")
    plt.scatter(next_n, next_y, color="green", marker='x', s=80, label="Predicted Points")

    # Annotate points
    for n, y in zip(n_vals, y_vals):
        plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=9, color="red")
    for n, y in zip(next_n, next_y):
        plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=9, color="green")

    plt.title("Polynomial Plot")
    plt.xlabel("n")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

def geo_plot(seq, num=0, frac=False, smooth=100):
    if len(seq) < 2:
        print("Sequence too short for geometric analysis.")
        return

    ratios = [seq[i+1]/seq[i] for i in range(len(seq)-1)]
    indices = np.arange(len(ratios))

    # Fit polynomial to ratios
    poly_res = _poly_analyze(ratios, frac)
    coeffs = [float(c) for c in poly_res["std_coef"]]

    # Smooth x values for plotting
    x_smooth = np.linspace(0, len(ratios)-1 + num, smooth)

    # Evaluate polynomial at smooth points
    def eval_poly(c, x):
        y = np.zeros_like(x, dtype=float)
        for i, ci in enumerate(c):
            y += ci * x**i
        return y
    y_smooth = eval_poly(coeffs, x_smooth)

    # Plot the ratio points
    plt.scatter(indices, ratios, color='red', label='Original ratios')

    # Annotate each point with (index, ratio, term)
    for i, r in enumerate(ratios):
        plt.text(indices[i], r, f"({i},{r:.3f},{seq[i+1]:.3f})", fontsize=9, ha='right')

    # Plot the polynomial curve
    plt.plot(x_smooth, y_smooth, label='Fitted ratio curve', color='blue')

    # Predict next ratios
    seq_ext = seq[:]
    pred_points = []
    for _ in range(num):
        nxt_ratio = eval_poly(coeffs, len(seq_ext)-1)
        pred_points.append(nxt_ratio)
        seq_ext.append(seq_ext[-1]*nxt_ratio)

    # Mark predicted ratios
    plt.scatter(range(len(ratios), len(ratios)+num), pred_points, color='green', label='Predicted ratios')
    for i, r in enumerate(pred_points):
        term = seq_ext[len(ratios)+i]
        plt.text(len(ratios)+i, r, f"({len(ratios)+i},{r:.3f},{term:.3f})", fontsize=9, ha='right')

    plt.xlabel("Index")
    plt.ylabel("Ratio a[i+1]/a[i]")
    plt.title("Geometric Analysis - Ratios & Fitted Curve")
    plt.legend()
    plt.grid(True)
    plt.show()

def log_plot(seq, num=2, frac=False, smooth=100):
    if len(seq) < 2:
        print("Sequence too short for log analysis.")
        return

    # Perform log analysis
    res = _log_analyze(seq, frac)
    if res.get("deg") is None:
        print("Cannot analyze sequence as logarithmic.")
        return

    n_vals = np.arange(len(seq))
    y_vals = np.array(seq, dtype=float)

    log_seq = [math.log(v) if v > 0 else float("nan") for v in seq]
    log_coeffs = [float(c) for c in res["std_coef"]]

    # Predict next points in original scale
    next_n = np.arange(len(seq), len(seq)+num)
    next_y = []
    for n in next_n:
        log_val = sum(c * n**i for i, c in enumerate(log_coeffs))
        val = math.exp(log_val)
        next_y.append(val)

    # Smooth curve
    x_full = np.linspace(0, len(seq)+num-1, smooth)
    y_full = np.exp(np.polyval(list(reversed(log_coeffs)), x_full))

    plt.figure(figsize=(8,5))
    plt.plot(x_full, y_full, label="Logarithmic Fit", color="blue")
    plt.scatter(n_vals, y_vals, color="red", label="Original Points")
    plt.scatter(next_n, next_y, color="green", marker='x', s=80, label="Predicted Points")

    # Annotate points
    for n, y in zip(n_vals, y_vals):
        plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=9, color="red")
    for n, y in zip(next_n, next_y):
        plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=9, color="green")

    plt.title("Logarithmic Plot")
    plt.xlabel("n")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot(seq, num=2, frac=False, smooth=100):

    n_orig = len(seq)
    if n_orig < 2:
        print("Sequence too short to plot.")
        return

    # ---------------------------
    # Polynomial
    # ---------------------------
    ply = _poly_analyze(seq, frac)
    if ply.get("deg") is not None:
        coeffs_ply = ply["std_coef"]
        x_int = np.arange(n_orig + num)
        y_int = np.array([sum(c * n**i for i, c in enumerate(coeffs_ply)) for n in x_int])

        # Smooth curve
        x_smooth = np.linspace(0, n_orig + num - 1, smooth)
        y_smooth = np.polyval(list(reversed(coeffs_ply)), x_smooth)
    else:
        x_int, y_int, x_smooth, y_smooth = [], [], [], []

    # ---------------------------
    # Logarithmic
    # ---------------------------
    log_seq = [math.log(v) if v > 0 else float('nan') for v in seq]
    log_clean = [x for x in log_seq if not math.isnan(x)]
    log_offset = log_seq.index(log_clean[0]) if log_clean else 0
    if len(log_clean) >= 2:
        log_poly = _poly_analyze(log_clean, frac)
        coeffs_log = log_poly["std_coef"]
        x_int_log = np.arange(n_orig + num)
        y_int_log = np.array([math.exp(sum(c * (n - log_offset)**i for i, c in enumerate(coeffs_log))) for n in x_int_log])
        x_smooth_log = np.linspace(0, n_orig + num - 1, smooth)
        y_smooth_log = np.array([math.exp(np.polyval(list(reversed(coeffs_log)), n - log_offset)) for n in x_smooth_log])
    else:
        x_int_log, y_int_log, x_smooth_log, y_smooth_log = [], [], [], []

    # ---------------------------
    # Geometric ratios
    # ---------------------------
    ratios = [seq[i+1]/seq[i] for i in range(n_orig-1)]
    if len(ratios) >= 2:
        poly_ratio = _poly_analyze(ratios, frac)
        coeffs_ratio = poly_ratio["std_coef"]

        # Smooth curve for ratios
        x_smooth_ratio = np.linspace(0, n_orig-2 + num, smooth)
        y_smooth_ratio = np.array([sum(c * n**i for i, c in enumerate(coeffs_ratio)) for n in x_smooth_ratio])

        # Predicted ratios
        seq_ext = seq[:]
        pred_ratios = []
        for i in range(num):
            nxt_ratio = sum(c * (len(seq_ext)-1)**i for i, c in enumerate(coeffs_ratio))
            pred_ratios.append(nxt_ratio)
            seq_ext.append(seq_ext[-1] * nxt_ratio)
    else:
        x_smooth_ratio, y_smooth_ratio, pred_ratios = [], [], []

    # ---------------------------
    # Plotting
    # ---------------------------
    plt.figure(figsize=(10,6))

    # Polynomial
    if x_smooth.any():
        plt.plot(x_smooth, y_smooth, color='blue', label='Polynomial Fit')
        plt.scatter(np.arange(n_orig), seq, color='blue', marker='o', label='Poly Original')
        plt.scatter(np.arange(n_orig, n_orig+num), y_int[n_orig:], color='cyan', marker='x', s=80, label='Poly Predicted')
        for n, y in zip(np.arange(n_orig), seq):
            plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=8, color='blue')
        for n, y in zip(np.arange(n_orig, n_orig+num), y_int[n_orig:]):
            plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=8, color='cyan')

    # Log
    if x_smooth_log.any():
        plt.plot(x_smooth_log, y_smooth_log, color='orange', label='Log Fit')
        plt.scatter(np.arange(n_orig), seq, color='orange', marker='o', label='Log Original')
        plt.scatter(np.arange(n_orig, n_orig+num), y_int_log[n_orig:], color='yellow', marker='x', s=80, label='Log Predicted')
        for n, y in zip(np.arange(n_orig, n_orig+num), y_int_log[n_orig:]):
            plt.text(n, y, f"({n},{float(Fraction(y).limit_denominator()) if frac else y:.3f})", fontsize=8, color='yellow')

    # Geometric ratios
    if x_smooth_ratio.any():
        plt.plot(x_smooth_ratio, y_smooth_ratio, color='green', label='Geo Ratio Fit')
        plt.scatter(np.arange(len(ratios)), ratios, color='red', marker='o', label='Original Ratios')
        plt.scatter(np.arange(len(ratios), len(ratios)+num), pred_ratios, color='purple', marker='x', s=80, label='Predicted Ratios')
        for i, r in enumerate(ratios):
            plt.text(i, r, f"({i},{r:.3f},{seq[i+1]:.3f})", fontsize=8, color='red')
        for i, r in enumerate(pred_ratios):
            plt.text(len(ratios)+i, r, f"({len(ratios)+i},{r:.3f},{seq_ext[len(ratios)+i]:.3f})", fontsize=8, color='purple')

    plt.title("Sequence Analysis Plot (Poly, Log, Geo)")
    plt.xlabel("Index")
    plt.ylabel("Value / Ratio")
    plt.legend()
    plt.grid(True)
    plt.show()

def fill_gaps(seq, round_to=6):
    n = len(seq)
    xs = []
    ys = []

    for i, v in enumerate(seq):
        if v is not None:
            xs.append(i)
            ys.append(v)

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)

    # Degree = number of known points – 1 (so the polynomial fits exactly)
    deg = len(xs) - 1

    coeffs = np.polyfit(xs, ys, deg)
    poly = np.poly1d(coeffs)

    result = []
    for i in range(n):
        if seq[i] is not None:
            result.append(seq[i])
        else:
            val = float(poly(i))
            result.append(round(val, round_to))

    return result


def help(format=False):
    info = {
        "analyze": {
            "signature": "analyze(seq: list, frac: bool=False, format: bool=False, cutoff: float=0.9) -> dict|str",
            "role": "Master function. Runs polynomial, geometric, logarithmic and custom analyzers and returns combined result."
        },
        "ply_analyze": {
            "signature": "ply_analyze(seq: list, frac: bool=False, format: bool=False) -> dict|str",
            "role": "Detects polynomial pattern using finite differences. Returns degree, coefficients, next term, certainty."
        },
        "geo_analyze": {
            "signature": "geo_analyze(seq: list, frac: bool=False, format: bool=False) -> dict|str",
            "role": "Detects geometric-type patterns using ratio-difference logic. Returns coefficients, next term, certainty."
        },
        "log_analyze": {
            "signature": "log_analyze(seq: list, frac: bool=False, format: bool=False) -> dict|str",
            "role": "Detects logarithmic transformations (log(n), log^2(n), etc). Uses polynomial fit on transformed domain."
        },
        "cus_analyze": {
            "signature": "cus_analyze(seq: list, frac: bool=False, format: bool=False) -> dict|str",
            "role": "Runs custom detectors (Fibonacci, Primes, AGP, Alternating, Harmonic). Returns best detection."
        },
        "best_next": {
            "signature": "best_next(seq: list, frac: bool=False) -> number|Fraction|None",
            "role": "Chooses the next term from the analyzer with highest certainty."
        },
        "extend": {
            "signature": "extend(seq: list, num: int=1, frac: bool=False) -> list",
            "role": "Appends the next `num` predicted terms to seq using best_next()."
        },
        "ply_plot": {
            "signature": "ply_plot(seq: list, num: int=2, frac: bool=False, smooth: int=100)",
            "role": "Plots the polynomial fit from ply_analyze. Shows predicted points and annotations. `smooth` controls curve resolution."
        },
        "geo_plot": {
            "signature": "geo_plot(seq: list, num: int=2, frac: bool=False, smooth: int=100)",
            "role": "Plots the geometric ratio fit from geo_analyze. Shows predicted ratios and annotations. `smooth` controls curve resolution."
        },
        "log_plot": {
            "signature": "log_plot(seq: list, num: int=2, frac: bool=False, smooth: int=100)",
            "role": "Plots the logarithmic fit from log_analyze. Shows predicted points and annotations. `smooth` controls curve resolution."
        },
        "plot": {
            "signature": "plot(seq: list, num: int=2, frac: bool=False, smooth: int=100)",
            "role": "Overlays Polynomial, Logarithmic, and Geometric ratio plots. Shows original points, predicted points, and annotations. `smooth` controls curve resolution."
        },
        "fill_gaps": {
            "signature": "fill_gaps(seq: list, frac: bool=False) -> list",
            "role": "Fills missing values (`None`) in a sequence using exact Newton interpolation based on surrounding known points."
        },
        "help": {
            "signature": "help(format: bool=False) -> dict|str",
            "role": "Returns this help dictionary."
        }
    }
    if format:
        import json
        return json.dumps(info, indent=2)
    return info