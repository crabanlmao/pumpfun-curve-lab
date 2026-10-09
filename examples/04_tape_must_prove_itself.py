from curvelab import synthetic_tape, validate_tape

tape = synthetic_tape(300, seed=5)
print("intact:   ", validate_tape(tape))
print("one gone: ", validate_tape(tape[:100] + tape[101:]))
print("late start:", validate_tape(tape[5:]))
