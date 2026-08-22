# Data

- `canonical/`: authoritative repository datasets.
- `raw/`: provenance-preserving inputs; do not silently normalize in place.
- `derived/`: reproducible transforms from declared inputs.

Schema is distinct from instance; identity from attributes; null from absent; duplicate from independently corroborating instance; logical identity from byte identity. Every lossy transform must say what information is discarded.
