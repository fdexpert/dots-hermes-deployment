# Delivery validation

[繁體中文](DELIVERY_VALIDATION.md) | **English**

Date: 2026-10-06 UTC | Kit 0.4.0 | macOS 26.6.2 arm64 | Python 3.14.5

| Check | Result / evidence |
| --- | --- |
| Tests | All 51 passed: original 27 plus 24 new tests. Self-owned loopback mocks, fake transport, synthetic tokens, temporary prefixes; no real Hermes/credentials. |
| CLI / MCP | Actual subprocess tests for initialize/tools-list/call/health/dispatch confirmation/mock SendMessage/GetTask. Default tools omit dispatch; unknown/token arguments rejected. |
| HTTP / security | Identity mismatch/missing token/no confirmation prevents POST; classifies 401/403/429/500/missing method; TLS verification/no proxy/redirect; token echoes redacted/refused; receipts exclude input/reply/token. |
| Timeout / state | Mock timeout has no resend, stores context, then explicit ListTasks retrieval; GetTask/all known states parsed; cleared store gives task_not_found. Not proof of real durable recovery. |
| Installation lifecycle | Actual venv and CLI: zero-write plan, explicit apply/idempotent repeat, config unread/unmodified, uninstall preserves config; unknown/modified prefixes refused; snapshot rollback/partial and unknown-file preservation. |
| Real read-only acceptance | Fresh-prefix 0.4.0 CLI and standard stdio MCP real Hermes health/card returned HTTP 200 with matching identity. Local task/standard client only, not native Dots registration. [Full matrix](docs/ACCEPTANCE_2026-10-06.en.md) |
| Real dispatch / native Dots | Real B authentication/dispatch PASS: one HTTP 200/completed/HERMES_OK in 7.69 seconds; matched audit/session verify named caller and zero tools. Native Dots MCP/new hardware/accounts NOTTESTED. |
| Syntax / formats | Eight Python AST checks, six JSON parses; three YAML files passed existing local PyYAML safe_load (not a runtime dependency). |
| Languages / files | 24 reciprocal document pairs; matching commands/official URLs; 69 explicit manifest entries with valid internal links and no symlinks. |
| Public / secret scans | Credential formats, real env/registry/config, personal email/home, private IPv4/tailnet DNS/UUID, and extra-file checks passed. Only kit files; no real credentials/state/venv/test directories/backups/logs. |
| ZIP | 69-file allowlist, byte-for-byte worktree match; no .git/cache/Library helper/secrets. SHA256/size supplied in delivery message. |
| Publication | Version 0.4.0 source updates the existing public main after 0.3.0. Exact commit/remote tree/CI are verified after push, with commit URL in delivery. No new task or server changes for publication. |

Reproducible checks:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py --public
python3 -B scripts/diagnose.py preflight
python3 -B scripts/validate_kit.py --public --zip /path/to/dots-hermes-deployment-kit.zip
```

See the [Mac mini guide](docs/MAC_MINI_BRIDGE.en.md) for actual installation trial/plan/apply/uninstall commands, and [FILES](FILES.en.md) for the complete inventory. New tests need local sockets. If bind is prohibited, obtain test permission instead of changing existing listeners/services.

Mocks/temporary test resources were cleaned. A later separately authorized case client remains; the user personally configured a distinct peer. Only caller trust was appended, aggregate active work checked zero, required restart performed, and one B task completed. No credentials/config/receipts/case IDs/venv/backups/logs are packaged. Original source remains unavailable; this is independent implementation. Native Dots MCP/new hardware/accounts/intermediary-shutdown experiment/C/other OS remain untested. The 51 mock tests last passed at 09:44 with unchanged source since; real-task evidence is separate, not complete Hermes pytest.

Before publication, all 51 offline tests passed again at 2026-10-06 22:39 UTC (1.557 seconds); two existing commits/89 blobs and 69 allowlisted files passed scans, with no new real task.
