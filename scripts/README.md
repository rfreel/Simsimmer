# Scripts

Operational procedures. Prefer idempotent, retry-safe, fail-visible scripts. A script succeeding is distinct from its downstream objective succeeding; doctor/verification steps should test the latter where possible.

## Reproducible local verification

The project has no third-party Python dependencies. `.python-version` selects the
development interpreter; `uv.lock` records the real project resolution. With uv:

```sh
uv sync --locked
uv run --locked python scripts/check.py
```

With an existing supported Python (3.11 or newer), run `python scripts/check.py`.
The same entry point runs all seven checks in CI, stops on the first failure,
keeps generated smoke receipts temporary, and never enables autoresearch writes.
Use `python scripts/check.py --list` to inspect the check set.
CI continues to test both supported Python minor versions through its matrix.
The aggregate `test` job remains the branch's required check.
