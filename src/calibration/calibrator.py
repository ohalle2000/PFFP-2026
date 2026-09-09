"""Fit Vasicek / CIR to market discount bond prices P(0,T)."""

import numpy as np
from scipy.optimize import minimize

from rates import cir, vasicek


class FitResult:
    """Just a bag of calibration outputs used by notebooks/tests."""

    def __init__(self, model_name, params, rmse, fitted, market, maturities, success, message):
        self.model_name = model_name
        self.params = params
        self.rmse = rmse
        self.fitted_prices = fitted
        self.market_prices = market
        self.maturities = maturities
        self.success = success
        self.message = message


def _fit(model, bond_price, curve, r0, guess, bounds):
    T = curve.maturities
    market = curve.discount_factors
    r0 = float(curve.zero_rates[0]) if r0 is None else r0

    def mse(x):
        a, b, sigma = x
        if a <= 0 or sigma <= 0 or (model == "CIR" and b <= 0):
            return 1e6
        pred = np.array([bond_price(a, b, sigma, r0, 0.0, t) for t in T])
        return float(np.mean((pred - market) ** 2))

    opt = minimize(mse, x0=np.array(guess), method="L-BFGS-B", bounds=bounds)
    a, b, sigma = opt.x
    fitted = np.array([bond_price(a, b, sigma, r0, 0.0, t) for t in T])
    rmse = float(np.sqrt(np.mean((fitted - market) ** 2)))

    return FitResult(
        model_name=model,
        params={"a": a, "b": b, "sigma": sigma, "r0": r0},
        rmse=rmse,
        fitted=fitted,
        market=market,
        maturities=T,
        success=bool(opt.success),
        message=str(opt.message),
    )


def calibrate_vasicek(curve, r0=None, x0=None):
    guess = x0 or (0.5, float(np.mean(curve.zero_rates)), 0.02)
    bounds = [(1e-4, 10.0), (1e-4, 0.20), (1e-4, 0.50)]
    return _fit("Vasicek", vasicek.bond_price, curve, r0, guess, bounds)


def calibrate_cir(curve, r0=None, x0=None):
    guess = x0 or (0.8, float(np.mean(curve.zero_rates)), 0.10)
    bounds = [(1e-4, 10.0), (1e-4, 0.20), (1e-4, 1.0)]
    return _fit("CIR", cir.bond_price, curve, r0, guess, bounds)
