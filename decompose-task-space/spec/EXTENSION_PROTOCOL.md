# Specification Basis Extension Protocol

Specialized specifications must not extend the generic basis by simply appending industry vocabulary.

```text
SPECIALIZED CASE
      ↓
PROJECT ON GENERIC BASIS
      ↓
representable without decision-relevant loss?
   ┌───────┴────────┐
  YES               NO
   ↓                 ↓
instantiate      isolate residual
existing axes         ↓
                  DISTINCT
                     ↓
                   RELATE
                     ↓
                derive existing
                  composition?
                ┌────┴────┐
               YES        NO
                ↓          ↓
             compile    construct
              macro     minimal witness
                           ↓
                    add ONE candidate
                       primitive
                           ↓
                       re-derive
                           ↓
                    adversarial test
                           ↓
                     retain/collapse
```

## Admission rules
1. Project the specialized concept onto the existing generic basis first.
2. If representation is lossless for the relevant decision/verification/execution consequence, instantiate existing axes.
3. If not, preserve the missing concept as a residual; do not silently overload an existing term.
4. DISTINCT the residual against its nearest generic rivals.
5. RELATE it to existing distinctions and test whether it is a composition/macro.
6. Prefer a derived composition over a new primitive.
7. If non-derivable, construct the smallest witness that exposes a concrete consequence of collapse.
8. Add at most one candidate primitive per unresolved distinction step.
9. Re-derive the basis and rerun representative specs after every candidate addition.
10. Adversarially test the new primitive and its reversal/collapse condition.
11. Retain only if the witness survives and future work is reduced; otherwise collapse/archive it.

A specialized concept earns a new generic primitive only when unseeded specialized-domain runs repeatedly produce a non-derivable discriminating witness.

## Simulation product space
Use low-discrepancy/golden-angle traversal across:

`spec distinction × abstraction level × whole/part level × epistemic state × temporal regime × coupling × reversibility × verification regime × resource contention × objective form × representation × domain specialization`.

Every scheduled probe carries exactly one current classification:
- `DERIVED`
- `NEW_WITNESS`
- `NEW_COMPOSITION`
- `CANDIDATE_PRIMITIVE`
- `REDUNDANT`
- `RESIDUAL`

Unevaluated probes are `RESIDUAL` with empty evidence rather than being assigned synthetic discoveries.

## Saturation procedure
Run derive/distinct/relate/cultivate/RISING/golden-angle passes until the declared stopping rule fires. Then ablate every retained distinction and re-derive. Report: surviving distinctions, collapses, new compositions, candidate primitives, unresolved residuals, domain coverage, search budget, and the exact bounded saturation claim.
