# /verify-token-handoff

Test pre-emptive context expansion and reactive 429 rate limit token-limit handoffs.

## Steps
1. Initialize `CascadingRouter` with `TokenLimitHandoffManager`.
2. Dispatch a prompt larger than 8,192 tokens to verify pre-emptive handoff to 32k/131k tier.
3. Simulate an HTTP 429 RateLimitExceeded error to verify reactive handoff to a fuller quota bucket.
4. Verify cooldown recovery and return execution telemetry.
