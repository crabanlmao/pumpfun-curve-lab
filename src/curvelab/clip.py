import math


def roundtrip_cost(c, V, flat_fee_sol=0.002, fee_bps_per_side=100.0):
    return c / V + c / (V + c) + 2 * fee_bps_per_side / 10_000 + flat_fee_sol / c


def best_clip_closed_form(V, flat_fee_sol=0.002):
    return math.sqrt(flat_fee_sol * V / 2.0)


def best_clip_numeric(V, flat_fee_sol=0.002, fee_bps_per_side=100.0, lo=0.005, hi=5.0, steps=20000):
    sizes = (lo + (hi - lo) * i / steps for i in range(steps + 1))
    return min(sizes, key=lambda c: roundtrip_cost(c, V, flat_fee_sol, fee_bps_per_side))
