# Mac mini bridge and isolated installation

[繁體中文](MAC_MINI_BRIDGE.md) | **English**

Version 0.4.0 includes original project implementations `scripts/bridge.py` and `scripts/install.py`. This is not the unavailable case bridge and copies no third-party implementation. Contracts were checked against local non-secret Hermes A2A source and official A2A/MCP documentation. Python stdlib only: no MCP SDK, pip, or network dependency downloads.

Installation and CLI/MCP calls to owned mocks passed in **temporary isolated prefixes** on macOS 26.6.2 arm64/Python 3.14.5. [This acceptance](ACCEPTANCE_2026-10-06.en.md) also passed real Hermes CLI/standard stdio MCP health/card and one named authenticated B local task: HERMES_OK, HTTP 200/completed, 7.69 seconds, zero tools. The user personally configured credentials; approved caller trust was appended and required gateway restart completed. New accounts/hardware/native Dots MCP remain untested. Installer supports macOS arm64/Python 3.11–3.14 only; no other OS deployment is claimed.

## 1. Test the kit and review the installation plan

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py --public
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action install
```

Tests create and clean up loopback mocks on random ports and temporary venvs with synthetic credentials, never real Hermes. Local sockets must be allowed in the test environment; do not change existing services to pass tests. Without `--apply`, the installer only returns a plan and creates no prefix, venv, or configuration. The prefix must be absolute, without symlink components, with an existing parent, and outside/not enclosing the kit.

## 2. Apply explicitly to a new private prefix

After host/directory authorization:

```sh
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action install --apply
```

Creates only `app/bridge.py`, `app/diagnose.py`, `venv/`, `config/bridge-config.json`, and `.kit-install.json` inside the prefix. The venv uses current Python without pip or system-site-packages. It does not change global Python, Hermes, launchd, Serve, trust, or MCP registration, start a service, or generate/move tokens.

Rerunning the same version/source hashes with unchanged managed files returns `changed:false` without reading/overwriting config. Unknown prefixes, symlinks, changed/extra managed-area entries are refused. Different versions/hashes require a new prefix; no in-place upgrade. Invoke the full interpreter path below without activation. Removing base Python requires rebuilding in a new prefix.

## 3. Edit non-secret config privately

Installed defaults contain neither a token nor dispatch-contract confirmation. Start from the [template](../examples/bridge-config.example.json):

| Field | Meaning |
| --- | --- |
| `schema_version` | Exactly 1; unknown fields rejected |
| `caller_id` | Expected caller label; does not replace bearer authentication or prove the server mapping |
| `targets.<alias>.base_url` | Explicit pinned loopback HTTP(S) or tailnet HTTPS root URL; card URLs/redirects are not followed |
| `expected_name` | Must match health agent and card name |
| `timeout_seconds` | 0.05–360 seconds; RPC default 30, template 330; health/card capped at 30. Socket I/O timeout, not a hard total deadline |
| `contract` | Set `hermes-a2a-v1-inspected` only after checking the server contract; deliberately absent from template |
| `token_file` | Optional absolute path outside the kit to a user-created raw-token file, read only for RPC. Never put token values in config |

There is no automatic old-registry import. A uses the new host's actual .ts.net HTTPS URL. B uses loopback without intermediary/Serve. [Security handoff](SECURITY.en.md) still requires distinct named tokens/non-empty trust, loopback, allow-all false, and reserved-identity restrictions; do not change server security constants.

## 4. Read-only health/card first

```sh
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json health --target example-target
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json card --target example-target
```

No token reading, POST, or task dispatch. GET 200 is not authentication proof. Fixed output shows send/query enablement, card compatibility, and loopback warnings. RPC rechecks health/card identity, JSONRPC 1.0, and bearer advertisement. The pinned URL overrides card loopback. Tenant/non-root profile routes, legacy v0.3, SSE/push/cancel, and generic Message responses are unsupported.

## 5. Credentials and stdio MCP

The user personally creates a raw caller-token file through a private interface: current-user owner, permissions 600/400, regular file without symlink, maximum 8192 bytes. Placeholders/Bearer prefixes/whitespace values are rejected. Prefer storage outside both prefix and kit. No token values in chat, command arguments, environment, or MCP tool arguments. CLI can use `--prompt-token` for hidden input; stdio MCP has no interactive token prompt.

Manually configure the chosen MCP client with the installed interpreter as command and the remaining arguments below, using that client's actual configuration format:

```sh
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json mcp
```

Default `tools/list` exposes only `fleet_health` and `fleet_card`. Implements newline JSON-RPC, initialize/initialized/ping/tools-list/tools-call, with MCP versions 2025-11-25, 2025-06-18, and 2025-03-26. stdout contains MCP messages only. No HTTP MCP listener or automatic global registration. Dots computer permission and MCP-client access require separate setup; not every task is guaranteed to have this client.

## 6. Explicit authorized dispatch/query

CLI dispatch requires `--confirm-send`, a private message file, and a private state directory outside the kit whose parent exists. Do not publish real messages/state in the repository. These are separately authorized operation examples, not installation steps:

```sh
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json --state-dir /Users/example/dots-hermes-state send --target example-target --message-file /path/to/private-message.txt --confirm-send
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json get-task --target example-target --task-id task-example
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json find-context --target example-target --context-id ctx-example
```

For MCP, explicitly start `mcp --enable-send --enable-query` with `--state-dir` before the subcommand. `fleet_send` requires `target`, `message`, and `confirm_send:true`, and has a destructive annotation. `fleet_get_task` takes target/task_id; `fleet_find_context` takes target/context_id. Unknown/token arguments are rejected. Flags/booleans enforce operation gates but cannot replace human authorization; the client must retain a confirmation flow the user can deny.

Default output contains status/IDs, not task text. CLI `--show-reply` or MCP `include_reply:true` opts into reply output, redacting the current token and known secret formats without guaranteeing arbitrary-secret detection. State snapshots have permissions 600 in a 700 directory. They store only request/message/context/task IDs, caller label, HTTP/state/error category/duration, **never message/reply/token/full response**.

This Hermes version waits synchronously for SendMessage rather than returning a task ID early. A fresh context reference is saved before sending, with a non-secret result snapshot afterward. Timeout/mismatched response/interruption leaves an unknown outcome: no automatic retry/resend. Known tasks use actual GetTask. Without a task ID, explicitly call ListTasks by context (maximum 20; flags further pages without following them). The in-memory store is limited by restart/expiry/scope/permissions. Missing results do not prove non-execution; this is not a durable queue or deduplication system. Queries cannot send SendMessage.

First real acceptance still needs separate approval for one [exact HERMES_OK input](VALIDATION.en.md). Mock success does not replace it.

## 7. Uninstall and failure recovery

```sh
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action uninstall
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action uninstall --apply
```

Dry-run first, explicit apply second. Only a complete owner marker and matching managed fingerprints permit per-entry app/venv/marker removal. The entire config directory and prefix remain; no recursive deletion of the whole prefix. Unknown/changed entries are refused; review manually without force.

A failed new install with unchanged managed snapshot removes those managed entries and preserves config. Interrupted venv construction/unknown additions or edits retain the private partial prefix and incomplete marker for inspection; subsequent apply/uninstall refuse. Use a new prefix or let the owner inspect before cleanup. Never repair real services to pass a test.
