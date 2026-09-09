"""CIR: dr = a(b - r)dt + sigma*sqrt(r) dW

Feller: 2ab >= sigma^2
Bond: P(t,T) = exp(A - B*r)
"""

from math import exp, log, sqrt

import numpy as np
from scipy.stats import ncx2


def feller_ok(a, b, sigma):
    return 2.0 * a * b >= sigma**2


def B(a, sigma, tau):
    g = sqrt(a * a + 2.0 * sigma * sigma)
    num = exp(g * tau) - 1.0
    den = (g + a) * (exp(g * tau) - 1.0) + 2.0 * g
    return 2.0 * num / den


def A(a, b, sigma, tau):
    g = sqrt(a * a + 2.0 * sigma * sigma)
    num = 2.0 * g * exp((a + g) * tau / 2.0)
    den = (g + a) * (exp(g * tau) - 1.0) + 2.0 * g
    return (2.0 * a * b / (sigma * sigma)) * log(num / den)


def bond_price(a, b, sigma, r, t, T):
    if abs(T - t) < 1e-14:
        return 1.0
    tau = T - t
    return exp(A(a, b, sigma, tau) - B(a, sigma, tau) * r)


def simulate(a, b, sigma, r0, T, n_steps, n_paths, scheme="exact", seed=None):
    """scheme: exact / euler / milstein"""
    dt = T / n_steps
    rng = np.random.default_rng(seed)
    paths = np.empty((n_paths, n_steps + 1))
    paths[:, 0] = r0

    for n in range(n_steps):
        z = rng.standard_normal(n_paths)
        r = np.maximum(paths[:, n], 0.0)

        if scheme == "exact":
            c = sigma**2 * (1.0 - exp(-a * dt)) / (4.0 * a)
            d = 4.0 * a * b / sigma**2
            lam = 4.0 * a * exp(-a * dt) / (sigma**2 * (1.0 - exp(-a * dt))) * r
            paths[:, n + 1] = c * ncx2.rvs(d, lam, size=n_paths, random_state=rng)
        elif scheme == "euler":
            paths[:, n + 1] = r + a * (b - r) * dt + sigma * np.sqrt(r) * sqrt(dt) * z
        elif scheme == "milstein":
            sqrt_r = np.sqrt(r)
            paths[:, n + 1] = (
                r
                + a * (b - r) * dt
                + sigma * sqrt_r * sqrt(dt) * z
                + 0.25 * sigma**2 * dt * (z**2 - 1.0)
            )
        else:
            raise ValueError("scheme must be exact, euler, or milstein")

        paths[:, n + 1] = np.maximum(paths[:, n + 1], 0.0)

    return paths
