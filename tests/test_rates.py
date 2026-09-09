import unittest

import numpy as np

from rates import cir, vasicek


class TestVasicek(unittest.TestCase):
    def test_price_at_maturity(self):
        self.assertAlmostEqual(vasicek.bond_price(0.5, 0.04, 0.02, 0.03, 0.0, 0.0), 1.0)

    def test_longer_maturity_cheaper(self):
        p1 = vasicek.bond_price(0.5, 0.04, 0.02, 0.03, 0.0, 1.0)
        p5 = vasicek.bond_price(0.5, 0.04, 0.02, 0.03, 0.0, 5.0)
        self.assertGreater(p1, p5)

    def test_mean_reversion(self):
        paths = vasicek.simulate(0.5, 0.04, 0.02, 0.10, 5.0, 50, 5000, seed=42)
        self.assertLess(abs(paths[:, -1].mean() - 0.04), 0.05)


class TestCIR(unittest.TestCase):
    def test_feller(self):
        self.assertTrue(cir.feller_ok(1.0, 0.04, 0.10))

    def test_price_at_maturity(self):
        self.assertAlmostEqual(cir.bond_price(1.0, 0.04, 0.10, 0.03, 0.0, 0.0), 1.0)

    def test_nonneg_paths(self):
        paths = cir.simulate(1.0, 0.04, 0.10, 0.03, 2.0, 40, 1000, "exact", seed=7)
        self.assertGreaterEqual(paths.min(), -1e-10)

    def test_euler_vs_exact(self):
        exact = cir.simulate(1.0, 0.04, 0.10, 0.03, 1.0, 200, 5000, "exact", seed=1)[:, -1]
        euler = cir.simulate(1.0, 0.04, 0.10, 0.03, 1.0, 200, 5000, "euler", seed=1)[:, -1]
        self.assertAlmostEqual(exact.mean(), euler.mean(), delta=0.005)


class TestMC(unittest.TestCase):
    def test_vasicek_mc(self):
        a, b, sigma, r0, T = 0.8, 0.04, 0.015, 0.035, 2.0
        analytical = vasicek.bond_price(a, b, sigma, r0, 0.0, T)
        paths = vasicek.simulate(a, b, sigma, r0, T, 100, 8000, seed=99)
        dt = T / 100
        mc = np.exp(-np.sum(paths[:, :-1], axis=1) * dt).mean()
        self.assertAlmostEqual(analytical, mc, delta=0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
