from curvelab import simulate_backlog

for service in (0.219, 0.037):
    r = simulate_backlog(arrival_rate=11.8, service_s=service, seconds=300, seed=1)
    print(f"{service * 1000:4.0f} ms/event  utilisation {r['utilisation']:.2f}  "
          f"median lag {r['median_lag_s']:7.2f} s  p99 {r['p99_lag_s']:7.2f} s")
