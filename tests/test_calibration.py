import unittest
from pathlib import Path

import numpy as np

from calibration.calibrator import calibrate_cir, calibrate_vasicek
from calibration.yield_curve import YieldCurve, flat_curve, humped_curve
from rates import vasicek

DATA = Path(__file__).resolve().parents[1] / "data"


class TestYieldCurve(unittest.TestCase):
    def test_from_csv(self):
        curve = YieldCurve.from_csv(DATA / "sample_yield_curve.csv")
        self.assertEqual(len(curve.maturities), 8)
        self.assertAlmostEqual(curve.discount_factors[0], np.exp(-0.025 * 0.25), places=6)


class TestCalibration(unittest.TestCase):
    def test_vasicek(self):
        result = calibrate_vasicek(humped_curve())
        self.assertTrue(result.success)
        self.assertLess(result.rmse, 0.05)
        self.assertIn("a", result.params)

    def test_cir(self):
        result = calibrate_cir(humped_curve())
        self.assertTrue(result.success)
        self.assertLess(result.rmse, 0.05)

    def test_flat_recovery(self):
        flat = flat_curve(rate=0.04)
        fitted = calibrate_vasicek(flat, r0=0.04)
        p = fitted.params
        for T in flat.maturities:
            market = np.exp(-0.04 * T)
            model = vasicek.bond_price(p["a"], p["b"], p["sigma"], 0.04, 0.0, T)
            self.assertAlmostEqual(model, market, delta=0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
