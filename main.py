from trees.crr import price_option

if __name__ == "__main__":
    price = price_option(100, 100, 0.05, 0.2, 1.0, N=3, kind="call", style="european")
    print(f"European call (N=3): {price:.4f}")
