# /run-validation

Execute the full Janus Core automated test suite and generate a health report.

## Steps
1. Run the test suite:
   ```bash
   python run_tests.py
   ```
2. Verify all 79 unit tests pass with 0 errors and 0 failures.
3. Check code security with `preflight_audit.py` to confirm zero AST or injection vulnerabilities.
4. Report pass count, total test duration, and status.
