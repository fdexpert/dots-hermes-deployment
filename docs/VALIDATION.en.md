# Four-layer acceptance matrix

[繁體中文](VALIDATION.md) | **English**

| Layer | Purpose | Method / pass criteria | Does not prove |
| --- | --- | --- | --- |
| 1: configuration | Correct identity and minimum trust | Private local review: named caller, distinct peer tokens, non-empty trust, allow-all false, loopback, no environment trust override, all placeholders replaced | The process has loaded new settings |
| 2: process | Correct host/version/single listener | Correct Dots task environment; gateway awake/running; lsof confirms loopback 9900; A Serve has the intended port/target and is tailnet-only; correct bridge `tools/list` schema | Successful local shell execution does not prove a Hermes task |
| 3: HTTP + authentication | Reachable DNS/TLS/card; effective general RPC authentication/trust | Matching health/card names; reachable or explicitly overridden card URL; unauthenticated safe probe rejected; valid named-token probe returns expected method-not-found; reserved identity denied general RPC | GET 200 may be publicly available and does not prove identity, trust, or task dispatch |
| 4: actual task | Authorized end-to-end path | After separate user approval, send the exact message below once to one target; obtain HERMES_OK/completed/no tool calls and record duration/status | Long tasks, all tools, or all operating systems |

## New bridge acceptance boundary

The 51 tests include CLI/MCP subprocesses against self-owned mocks, actual isolated venv installation, idempotence, config preservation, rollback, and uninstall. This is not layer-4 real-agent acceptance. [This acceptance run](ACCEPTANCE_2026-10-06.en.md) passed real Hermes CLI/standard stdio MCP health/card; one authenticated B task also passed that evening; native Dots MCP/fresh accounts/other hardware remain untested. Retrieval is limited to GetTask/context ListTasks, without durable queue or automatic resend. [Operation guide](MAC_MINI_BRIDGE.en.md)

## Layer 3 commands

Run against target loopback and, for A, the caller's tailnet URL:

```sh
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target
```

Diagnostics warn about a loopback card URL. For A, verify registry override or supported `A2A_PUBLIC_URL`; following the card URL must not connect the caller to itself.

### Optional authentication probe without task dispatch

First check that the deployed version retains the `do_POST` order in [source records](SOURCES.en.md): authentication → reserved identity denial → trust → undefined-method rejection. Method `DeploymentKitAuthProbe` **must not be registered**. Do not run against a server that lacks this contract.

```sh
python3 -B scripts/diagnose.py auth --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target --confirm-hermes-contract
```

The tool first GETs health to check the target, then sends a fixed unauthenticated probe. Only after rejection does it ask the operator for the caller's raw token through a hidden prompt. It sends the same undefined method and accepts only HTTP 200, JSON-RPC `-32601`, and a matching request id. On the inspected Hermes contract, this means authentication/trust passed before rejection ahead of task dispatch. No SendMessage, task, tool, or callback is invoked. The server may count rate limits/audit events; the probe is not free of side effects. Other behavior is reported as a contract mismatch without guessing or retrying.

A suitably authorized operator checks the reserved identity separately. It is not the deployment caller and should fail with 403. This does not require automatically dispatching a task with an incorrect identity.

## Layer 4: the exact message, once

> 請只回覆 HERMES_OK，不使用工具、不修改檔案、不對外聯絡

Meaning: “Reply only HERMES_OK; do not use tools, modify files, or contact anyone externally.” The Traditional Chinese text above remains the exact acceptance input in both editions; do not substitute the English explanation.

Use explicit new-kit send (message-file/confirm-send) or the acquired original fleet_ask with verified schema and separate operator authorization. Default installation/MCP does not enable dispatch. This edition separately completed one authorized real Hermes B task; see [acceptance matrix](ACCEPTANCE_2026-10-06.en.md). Do not replay completed acceptance automatically.

Keep a redacted record: date, A/B, versions, self-chosen anonymous caller/target labels, HTTP status, completed state, exact reply, seconds, and tool-call count. Do not include tokens, full registry, task input history, or logs. If a 300-second timeout/disconnection leaves the result unknown, retain the local task reference and check server/client state manually first. Do not resend. Without a complete retrieval tool, mark the result pending.

One B local CLI task passed; the intermediary was not used, but an actual intermediary-shutdown experiment remains untested and needs explicit approval/impact assessment. Do not shut down original services for this document. Every new host still needs its own four-layer acceptance.
