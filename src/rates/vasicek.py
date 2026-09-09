"""Vasicek: dr = a(b - r)dt + sigma dW

Bond: P(t,T) = exp(A - B*r)
"""

from math import exp, sqrt

import numpy as np


def B(a, tau):
    return (1.0 - exp(-a * tau)) / a


def A(a, b, sigma, tau):
    Bt = B(a, tau)
    return (Bt - tau) * (a * a * b - 0.5 * sigma * sigma) / (a * a) - (
        sigma * sigma * Bt * Bt
    ) / (4.0 * a)


def bond_price(a, b, sigma, r, t, T):
    if abs(T - t) < 1e-14:
        return 1.0
    tau = T - t
    return exp(A(a, b, sigma, tau) - B(a, tau) * r)


def simulate(a, b, sigma, r0, T, n_steps, n_paths, seed=None):
    """Exact Gaussian transition."""
    dt = T / n_steps
    rng = np.random.default_rng(seed)
    paths = np.empty((n_paths, n_steps + 1))
    paths[:, 0] = r0

    for n in range(n_steps):
        z = rng.standard_normal(n_paths)
        r = paths[:, n]
        mean = b + (r - b) * exp(-a * dt)
        std = sigma * sqrt((1.0 - exp(-2.0 * a * dt)) / (2.0 * a))
        paths[:, n + 1] = mean + std * z

    return paths
