"""Cox–Ross–Rubinstein tree (slides p.78–81).

u = exp(sigma * sqrt(dt))
d = exp(-sigma * sqrt(dt))
q = (exp(r * dt) - d) / (u - d)
"""

from math import exp, sqrt


def crr_params(sigma, dt, r):
    u = exp(sigma * sqrt(dt))
    d = exp(-sigma * sqrt(dt))
    q = (exp(r * dt) - d) / (u - d)
    return u, d, q


def payoff(S, K, kind):
    if kind == "call":
        return max(S - K, 0.0)
    if kind == "put":
        return max(K - S, 0.0)
    raise ValueError("kind must be call or put")


def price_option(S, K, r, sigma, T, N, kind="call", style="european", exercise_dates=None):
    """European / American / Bermudan call or put on a CRR tree."""
    if N < 1:
        raise ValueError("N must be >= 1")
    if T <= 0:
        raise ValueError("T must be > 0")
    if style not in ("european", "american", "bermudan"):
        raise ValueError(f"unknown style: {style!r}")
    if style == "bermudan" and exercise_dates is None:
        raise ValueError("bermudan needs exercise_dates")

    dt = T / N
    u, d, q = crr_params(sigma, dt, r)
    disc = exp(-r * dt)

    # values at maturity for each down-count i = 0..N
    values = [payoff(S * (u ** (N - i)) * (d ** i), K, kind) for i in range(N + 1)]

    for n in range(N - 1, -1, -1):
        for i in range(n + 1):
            cont = disc * (q * values[i] + (1.0 - q) * values[i + 1])
            spot = S * (u ** (n - i)) * (d ** i)
            if style == "american" or (style == "bermudan" and n in exercise_dates):
                values[i] = max(cont, payoff(spot, K, kind))
            else:
                values[i] = cont
        values = values[: n + 1]

    return values[0]
