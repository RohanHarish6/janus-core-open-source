# /optimize-engine

Scan for performance bottlenecks, check token budgets, and apply architecture optimizations.

## Steps
1. Review `janus_core_engine_v1_1_8.py` for token compaction, cache hit rates, and model routing efficiency.
2. Verify progressive disclosure schemas and delta state reducer logic.
3. Run `python run_tests.py` to ensure all tests pass cleanly.
4. Record metrics in `CHANGELOG.md` and update `USER_MANUAL.md`.
