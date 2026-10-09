from curvelab import roundtrip_cost, best_clip_numeric, best_clip_closed_form

V, F, FEE = 50.0, 0.002, 100.0
for c in (0.02, 0.05, 0.1, 0.22, 0.5, 1.0, 2.0):
    print(f"{c:6.2f} SOL  {roundtrip_cost(c, V, F, FEE):7.2%}")
print(f"best size, numeric:  {best_clip_numeric(V, F, FEE):.3f} SOL")
print(f"best size, closed:   {best_clip_closed_form(V, F):.3f} SOL")
