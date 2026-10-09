import numpy as np

from .curve import Curve, INIT_VTOK, LAMPORTS


def synthetic_tape(n=300, seed=0):
    rng = np.random.default_rng(seed)
    c, tape = Curve(), []
    for i in range(n):
        if rng.random() < 0.6 or c.vtok > INIT_VTOK * 0.99:
            sol = int(rng.lognormal(np.log(0.3), 0.8) * LAMPORTS)
            tok, nxt = c.buy_exact_sol(sol)
            side = "buy"
        else:
            tok = int(c.vtok * rng.uniform(0.0005, 0.01))
            sol, nxt = c.sell(tok)
            side = "sell"
        tape.append({"i": i, "side": side, "sol": sol, "tok": tok,
                     "pre_vtok": c.vtok, "post_vtok": nxt.vtok, "pre_vsol": c.vsol, "post_vsol": nxt.vsol})
        c = nxt
    return tape


def validate_tape(tape):
    breaks, prev_v, prev_s = [], None, None
    for r in tape:
        if prev_v is not None and (r["pre_vtok"] != prev_v or r["pre_vsol"] != prev_s):
            breaks.append(r["i"])
        prev_v, prev_s = r["post_vtok"], r["post_vsol"]
    return {"n": len(tape), "breaks": breaks,
            "starts_at_launch": bool(tape) and tape[0]["pre_vtok"] == INIT_VTOK}
