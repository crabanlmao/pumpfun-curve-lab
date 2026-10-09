# pumpfun-curve-lab

Exact constant-product bonding-curve math (pump.fun style) and the costs around it. Synthetic data only: no network, keys or wallets, and no strategy.

| | |
|---|---|
| `curve.py` | integer buy/sell/quote, rounding in the pool's favour |
| `fill.py` | token amount fixed at decision, SOL capped, other trades land in between |
| `clip.py` | round-trip cost vs position size, closed-form optimum `sqrt(F*V/2)` |
| `latency.py` | queue model for whether a decision loop keeps up, plus a per-event profiler |
| `tape.py` | continuity check that finds a missing trade without outside data |

```bash
pip install -e ".[dev]"
python -m pytest
python examples/01_latency_costs_money.py
```

Example output (seeded):

- ~4 other trades/s around a 0.25 SOL buy: 0% of buys fail at 0 s latency, 4.3% at 1 s, 21.9% at 4 s. Landed buys look better at long latency only because the ones where price ran away failed.
- At 50 virtual SOL, 0.002 SOL flat cost, 1% per side: round trip costs 12.1% at 0.02 SOL, 3.8% at 0.22 SOL, 9.95% at 2 SOL. Both optima come out at 0.224 SOL.
- 11.8 events/s: a loop taking 219 ms/event (utilisation 2.58) falls hundreds of seconds behind; 37 ms (0.44) stays at 0.04 s median lag. Both timings are from a real loop whose scoring competed with a training job for CPU threads.
- One trade removed from 300 is found at its index.

Fee and cost parameters are illustrative. Measurements from the real venue are in [docs/FINDINGS.md](docs/FINDINGS.md).
