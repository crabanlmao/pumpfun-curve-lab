"""curvelab: exact constant-product bonding-curve math, fill and latency simulation, tape validation."""
from .curve import Curve, INIT_VSOL, INIT_VTOK, LAMPORTS
from .fill import attempt_buy, random_flow, latency_study
from .clip import roundtrip_cost, best_clip_numeric, best_clip_closed_form
from .latency import simulate_backlog, profile_callable
from .tape import synthetic_tape, validate_tape

__all__ = [
    "Curve", "INIT_VSOL", "INIT_VTOK", "LAMPORTS",
    "attempt_buy", "random_flow", "latency_study",
    "roundtrip_cost", "best_clip_numeric", "best_clip_closed_form",
    "simulate_backlog", "profile_callable",
    "synthetic_tape", "validate_tape",
]
