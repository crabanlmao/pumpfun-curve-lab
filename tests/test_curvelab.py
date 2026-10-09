import numpy as np
import pytest

from curvelab import (
    Curve, LAMPORTS, attempt_buy, random_flow, latency_study, roundtrip_cost, best_clip_numeric,
    best_clip_closed_form, simulate_backlog, profile_callable, synthetic_tape, validate_tape,
)


def test_buy_then_sell_never_returns_more_than_was_spent():
    c = Curve()
    spend = int(1.5 * LAMPORTS)
    tok, c2 = c.buy_exact_sol(spend)
    out, c3 = c2.sell(tok)
    assert out <= spend and spend - out <= 2          # rounding favours the pool, by at most lamports
    assert c3.vsol * c3.vtok >= c.vsol * c.vtok       # the invariant never decreases


def test_entry_slippage_equals_size_over_virtual_sol():
    c = Curve(vsol=50 * LAMPORTS, vtok=Curve().vtok * 30 // 50)
    for sol in (0.05, 0.25, 1.0):
        lam = int(sol * LAMPORTS)
        assert c.entry_slippage(lam) == pytest.approx(lam / c.vsol, rel=1e-6)


def test_cost_for_tokens_is_the_inverse_of_buy():
    c = Curve()
    tok, _ = c.buy_exact_sol(LAMPORTS)
    assert c.cost_for_tokens(tok) <= LAMPORTS
    assert c.cost_for_tokens(tok + 1) > c.cost_for_tokens(tok) - 1


def test_zero_latency_always_lands_and_high_latency_fails_more():
    rows = latency_study(latencies_s=(0.0, 4.0), n_trials=400, seed=1)
    assert rows[0]["fail_rate"] == 0.0
    assert rows[0]["mean_overpay"] == pytest.approx(0.0, abs=1e-9)
    assert rows[1]["fail_rate"] > rows[0]["fail_rate"] or rows[1]["mean_overpay"] > 0.02


def test_a_tight_cushion_fails_where_a_loose_one_lands():
    rng = np.random.default_rng(3)
    c = Curve(vsol=50 * LAMPORTS, vtok=Curve().vtok * 30 // 50)
    flow = [("buy", 8 * LAMPORTS)]                    # someone buys 8 SOL first
    tight = attempt_buy(c, int(0.25 * LAMPORTS), flow, cushion=0.01)
    loose = attempt_buy(c, int(0.25 * LAMPORTS), flow, cushion=0.5)
    assert not tight.landed and loose.landed


def test_closed_form_clip_matches_numeric_optimum():
    for V in (30, 50, 80):
        closed, num = best_clip_closed_form(V), best_clip_numeric(V)
        assert abs(closed - num) / num < 0.08
    assert roundtrip_cost(0.01, 50) > roundtrip_cost(0.22, 50) < roundtrip_cost(5.0, 50)   # U-shape


def test_a_loop_slower_than_the_feed_falls_behind_and_a_fast_one_does_not():
    slow = simulate_backlog(arrival_rate=11.8, service_s=0.219, seconds=120, seed=1)
    fast = simulate_backlog(arrival_rate=11.8, service_s=0.037, seconds=120, seed=1)
    assert slow["utilisation"] > 1 and slow["final_lag_s"] > 30
    assert fast["utilisation"] < 1 and fast["p99_lag_s"] < 1.0


def test_profile_callable_reports_percentiles():
    out = profile_callable(lambda e: sum(range(100)), list(range(200)))
    assert out["n"] == 200 and out["p50_ms"] <= out["p99_ms"]


def test_synthetic_tape_is_continuous_and_a_missing_trade_is_found():
    tape = synthetic_tape(300, seed=5)
    assert validate_tape(tape) == {"n": 300, "breaks": [], "starts_at_launch": True}
    broken = tape[:100] + tape[101:]
    out = validate_tape(broken)
    assert out["breaks"] == [101]
    assert validate_tape(tape[5:])["starts_at_launch"] is False
