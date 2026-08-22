# Evaluator lock repair

This change corrects the stored SHA-256 for the unchanged frozen simulator. It does not modify `sim/simulator.py` or any test. Promotion requires the existing CI to execute and pass against the corrected lock.
