import time

import numpy as np


def simulate_backlog(arrival_rate, service_s, seconds=300.0, seed=0):
    rng = np.random.default_rng(seed)
    t, free_at, lags = 0.0, 0.0, []
    while t < seconds:
        t += rng.exponential(1.0 / arrival_rate)
        free_at = max(t, free_at) + service_s
        lags.append(free_at - t)
    lags = np.array(lags)
    return {"utilisation": arrival_rate * service_s, "events": len(lags),
            "median_lag_s": float(np.median(lags)), "p99_lag_s": float(np.quantile(lags, 0.99)),
            "final_lag_s": float(lags[-1])}


def profile_callable(fn, events, warmup=20):
    for e in events[:warmup]:
        fn(e)
    times = []
    for e in events:
        t0 = time.perf_counter()
        fn(e)
        times.append((time.perf_counter() - t0) * 1000.0)
    a = np.array(times)
    return {"n": len(a), "p50_ms": float(np.quantile(a, 0.5)), "p95_ms": float(np.quantile(a, 0.95)),
            "p99_ms": float(np.quantile(a, 0.99)), "mean_ms": float(a.mean())}
