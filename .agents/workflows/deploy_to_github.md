# /deploy-to-github

Stage, package, and deploy Janus Core updates to the GitHub repository.

## Steps
1. Run preflight audit and tests:
   ```bash
   python run_tests.py
   python preflight_audit.py
   ```
2. Check Git status and stage changes:
   ```bash
   git status
   git add -A
   ```
3. Commit with semantic versioning tag:
   ```bash
   git commit -m "Janus Core update: architecture optimization and test verification"
   ```
4. Push to remote:
   ```bash
   git push origin main
   ```
