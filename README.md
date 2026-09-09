# PFFP 2026 —  Project

Disclaimer: 
-> Simpliest methods implemented in the project, the main goal is to have any positive grade that pass the course :)
-> AI usage and impact clarification: 
  >> src/ was written by me and modified by AI to the convinient format 
  >> AI used for generating code that is making plots code and doing tests + inspiring examples, ReadMe summary
-> Data for Calibration has been taken from Bbg terminal, attached screenshot



Project contain:

- CRR binomial 
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


