import math
import unittest
from statistics import NormalDist

from trees.crr import crr_params, price_option


def bs_call(S, K, r, sigma, T):
    cdf = NormalDist().cdf
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * cdf(d1) - K * math.exp(-r * T) * cdf(d2)


class TestCRR(unittest.TestCase):
    def test_ud(self):
        u, d, q = crr_params(0.2, 0.25, 0.05)
        self.assertAlmostEqual(u * d, 1.0, places=12)
        self.assertTrue(0.0 < q < 1.0)

    def test_one_step(self):
        S, K, r, sigma, T = 100.0, 100.0, 0.05, 0.20, 1.0
        u, d, q = crr_params(sigma, T, r)
        expected = math.exp(-r * T) * (q * max(S * u - K, 0) + (1 - q) * max(S * d - K, 0))
        self.assertAlmostEqual(
            price_option(S, K, r, sigma, T, 1, "call", "european"), expected, places=12
        )

    def test_bermudan_like_european(self):
        kw = dict(S=100.0, K=100.0, r=0.05, sigma=0.2, T=1.0, N=10, kind="put")
        euro = price_option(**kw, style="european")
        berm = price_option(**kw, style="bermudan", exercise_dates={10})
        self.assertAlmostEqual(berm, euro, places=10)

    def test_bermudan_like_american(self):
        kw = dict(S=100.0, K=100.0, r=0.05, sigma=0.2, T=1.0, N=10, kind="put")
        amer = price_option(**kw, style="american")
        berm = price_option(**kw, style="bermudan", exercise_dates=set(range(11)))
        self.assertAlmostEqual(berm, amer, places=10)

    def test_american_put_ge_european(self):
        kw = dict(S=100.0, K=100.0, r=0.05, sigma=0.2, T=1.0, N=50, kind="put")
        self.assertGreaterEqual(
            price_option(**kw, style="american"),
            price_option(**kw, style="european") - 1e-12,
        )

    def test_parity(self):
        S, K, r, sigma, T = 100.0, 95.0, 0.05, 0.2, 1.0
        c = price_option(S, K, r, sigma, T, 50, "call", "european")
        p = price_option(S, K, r, sigma, T, 50, "put", "european")
        self.assertAlmostEqual(c - p, S - K * math.exp(-r * T), places=8)

    def test_bs_limit(self):
        S, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
        tree = price_option(S, K, r, sigma, T, 200, "call", "european")
        self.assertAlmostEqual(tree, bs_call(S, K, r, sigma, T), delta=0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
