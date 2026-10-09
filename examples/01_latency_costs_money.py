from curvelab import latency_study

print("latency   fail rate   mean overpay (landed buys)")
for r in latency_study(n_trials=1500, seed=7):
    print(f"{r['latency_s']:5.1f} s   {r['fail_rate']:8.1%}   {r['mean_overpay']:+.2%}")
