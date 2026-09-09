# PFFP 2026 — Project

## Disclaimer

- Simplest methods are used on purpose — the goal is a passing grade for the course.
- **AI usage:**
  - `src/` was written by me and cleaned up with AI
  - AI helped with generating plot code, `tests/`, and this README summary
- Calibration data comes from a Bloomberg terminal (screenshot in data folder)

## What is in the project

- CRR binomial trees
- Vasicek & CIR short-rate models (bond prices + simulation)
- Yield-curve calibration (Bloomberg EUR OIS or sample CSV)

## Layout

```
src/              # library
  trees/crr.py
  rates/vasicek.py, cir.py
  calibration/     # curve load + fit
tests/             # unit tests
notebooks/         # demos / experiments
data/              # yield curves (CSV)
figures/           # plots from notebooks
main.py            # tiny CRR smoke demo
```

## Setup

```bash
pip install -r requirements.txt
```

Run code with `PYTHONPATH=src` (or from notebooks after they add `src` to `sys.path`).

## Tests

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

## Notebooks

1. `01_tree_pricing_demo.ipynb` — CRR + BS convergence  
2. `02_short_rate_models.ipynb` — bonds, paths, CIR schemes  
3. `03_calibration.ipynb` — fit to `data/bloomberg_eur_ois_curve.csv`

## Quick usage

```python
from trees.crr import price_option
from rates import vasicek, cir
from calibration.yield_curve import YieldCurve
from calibration.calibrator import calibrate_vasicek

price = price_option(100, 100, 0.05, 0.2, 1.0, N=50, kind="call", style="european")
curve = YieldCurve.from_csv("data/bloomberg_eur_ois_curve.csv")
fit = calibrate_vasicek(curve)
```
