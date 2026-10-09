from dataclasses import dataclass

import numpy as np

from .curve import Curve, LAMPORTS


@dataclass
class Fill:
    landed: bool
    tokens: int = 0
    cost: int = 0
    overpay: float = 0.0


def random_flow(curve, rate_per_s, seconds, rng, buy_prob=0.55, median_sol=0.5, sigma=1.0):
    flow, c = [], curve
    for _ in range(rng.poisson(rate_per_s * seconds)):
        lam = min(int(rng.lognormal(np.log(median_sol), sigma) * LAMPORTS), c.vsol // 2)
        if rng.random() < buy_prob:
            _, c = c.buy_exact_sol(lam)
            flow.append(("buy", lam))
        else:
            tok = c.vtok * lam // max(c.vsol - lam, 1)
            _, c = c.sell(tok)
            flow.append(("sell", tok))
    return flow


def apply_flow(curve, flow):
    c = curve
    for side, amt in flow:
        c = c.buy_exact_sol(amt)[1] if side == "buy" else c.sell(amt)[1]
    return c


def attempt_buy(decision_curve, spend, flow, cushion=0.2):
    tokens, _ = decision_curve.buy_exact_sol(spend)
    cost = apply_flow(decision_curve, flow).cost_for_tokens(tokens)
    if cost > spend * (1.0 + cushion):
        return Fill(False)
    return Fill(True, tokens, cost, cost / spend - 1.0)


def latency_study(latencies_s=(0.0, 0.2, 0.5, 1.0, 2.0, 4.0), spend_sol=0.25, rate_per_s=4.0,
                  n_trials=1500, cushion=0.2, seed=0, start=None):
    rng = np.random.default_rng(seed)
    start = start or Curve(vsol=50 * LAMPORTS, vtok=Curve().vtok * 30 // 50)
    spend = int(spend_sol * LAMPORTS)
    rows = []
    for lat in latencies_s:
        fails, over = 0, []
        for _ in range(n_trials):
            f = attempt_buy(start, spend, random_flow(start, rate_per_s, lat, rng), cushion)
            if f.landed:
                over.append(f.overpay)
            else:
                fails += 1
        rows.append({"latency_s": lat, "fail_rate": fails / n_trials,
                     "mean_overpay": float(np.mean(over)) if over else float("nan")})
    return rows
