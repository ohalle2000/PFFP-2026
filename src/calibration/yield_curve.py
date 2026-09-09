"""Load a yield curve from CSV (maturity + zero_rate or discount_factor)."""

import numpy as np
import pandas as pd


class YieldCurve:
    def __init__(self, maturities, zero_rates):
        self.maturities = np.asarray(maturities, dtype=float)
        self.zero_rates = np.asarray(zero_rates, dtype=float)
        if len(self.maturities) != len(self.zero_rates):
            raise ValueError("maturities and zero_rates must have the same length")
        if np.any(self.maturities <= 0):
            raise ValueError("maturities must be positive")

    @property
    def discount_factors(self):
        # P(0,T) = exp(-z(T) * T)
        return np.exp(-self.zero_rates * self.maturities)

    @classmethod
    def from_csv(cls, path):
        df = pd.read_csv(path, comment="#")
        if "maturity" not in df.columns:
            raise ValueError("CSV needs a maturity column")

        T = df["maturity"].to_numpy(dtype=float)

        if "zero_rate" in df.columns:
            z = df["zero_rate"].to_numpy(dtype=float)
            if np.nanmax(np.abs(z)) > 1.0:
                z = z / 100.0  # Bloomberg-style percent
        elif "discount_factor" in df.columns:
            dfs = df["discount_factor"].to_numpy(dtype=float)
            z = -np.log(dfs) / T
        else:
            raise ValueError("CSV needs zero_rate or discount_factor")

        return cls(T, z)


def flat_curve(rate=0.03, maturities=None):
    if maturities is None:
        maturities = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0])
    return YieldCurve(maturities, np.full(len(maturities), rate))


def humped_curve():
    T = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0])
    z = np.array([0.025, 0.028, 0.032, 0.038, 0.036, 0.033, 0.031, 0.029])
    return YieldCurve(T, z)
