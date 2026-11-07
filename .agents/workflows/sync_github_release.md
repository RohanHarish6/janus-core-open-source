# /sync-github-release

Audit candidate open-source patches, verify 90 unit tests, and deploy zero-touch release to GitHub.

## Steps
1. Scan upstream open-source radar via `AutonomousGitHubIngestionEngine`.
2. Run AST static security analysis on all candidate patches (verifying 0 eval/exec/ssrf).
3. Execute preflight test suite (`python run_tests.py`) ensuring all 90 unit tests pass.
4. Generate `GitHubSyncManifest` and sync release package.
5. Deploy to GitHub via `deploy_to_github.bat` or `.github/workflows/sync_drive_to_github.yml`.
