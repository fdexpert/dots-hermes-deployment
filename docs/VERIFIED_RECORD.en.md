# Verified deployment record and unverified items

[繁體中文](VERIFIED_RECORD.md) | **English**

> **2026-10-08 documentation supplement: [D: private MCP / Tunnel persistent-worker CLI](VERIFIED_RECORD.en.md).** Version remains 0.4.0. A is historical intermediary Mac; B is desktop CLI → loopback A2A; D is a new route, not unverified C. Do not extend B limitations to D.

Historical dates for 2026-10-05–06 are UTC; the D date of 2026-10-08 is owner-supplied without an assumed timezone. The public edition retains only anonymized summaries. “Intermediary Mac / Hermes Mac” are generic roles. Original host names, identities, service labels, and identifying parts of local execution markers are omitted; they are not new-deployment defaults.

| Date | Evidence / result | Scope |
| --- | --- | --- |
| 2026-10-05–06 | Python stdio MCP bridge and agents registry on intermediary Mac; caller=intermediary Mac, node=Hermes Mac; SSH maintenance path to target existed | Original bridge source not obtained. It was registered only in Claude Desktop / Code, not globally in Dots. |
| 2026-10-05 | Twelve conflict blocks in security.py + adapter.py repaired, preserving security and local_readonly; six syntax checks and five focused security tests passed | pytest unavailable then; no complete suite, commit, or push. This is not a mandatory repair for every new deployment. |
| 2026-10-05–06 | Gateway service; loopback 9900; tailnet-only Serve HTTPS 10000→127.0.0.1:9900 | Other Serve/Funnel entries unchanged; not modified by this kit. |
| 2026-10-05–06 | Original local_bridge_only:true denied general routes with only/local-readonly restriction. User personally configured caller credentials, named caller trust, local_bridge_only:false, and removed stale .env trust override | No token values retained. Preserved the server's independent local bridge identity restrictions; the public edition omits its fixed identity string. |
| 2026-10-06 06:33 | One A task with the specified exact message returned HERMES_OK: 8.8 seconds, HTTP 200, TASK_STATE_COMPLETED, zero remote tool calls | One successful A task. No task ID retained; this does not verify retrieval of unknown outcomes. |
| 2026-10-06 | Hermes Mac: macOS 26.6.2 arm64; separate Dots local task returned an execution marker with exit 0; health/card 200 with matching identity (identifying marker/identity parts omitted) | B computer connection/HTTP verified. Local Hermes task and testing with the intermediary shut down were not performed. |
| 2026-10-06 | Original card advertised loopback; A bridge overrode it with registry HTTPS | Generic A2A clients may not override automatically. |
| 2026-10-06 (kit) | Non-secret checkout inspection, Python/Tailscale inventory, new offline kit validation | No task dispatch or service changes. See SOURCES and DELIVERY_VALIDATION. |
| 2026-10-06 (0.2.0 publication) | Separately authorized sanitized kit published to a public GitHub repository; remote visibility, main commit, and 38-file tree checked | Publication of kit source only; no deployment, credential configuration, or new Hermes acceptance. |
| 2026-10-06 (0.3.0 bilingual edition) | Complete English document counterparts, bilingual navigation/example comments, offline and package checks | Documentation update; technical commands and runtime behavior unchanged. See [delivery validation](../DELIVERY_VALIDATION.en.md). |
| 2026-10-06 (0.4.0 implementation) | Original CLI/MCP against self-owned mocks, real venv temporary-prefix installation/idempotence/config preservation/rollback/uninstall; 51 tests passed | No real Hermes task or actual Dots MCP-client integration; other hardware/accounts pending; not committed/pushed at that time. |
| 2026-10-06 09:44 (0.4.0 acceptance) | Same-host clean-prefix plan/apply/repeat/uninstall passed; new-bridge CLI and standard stdio MCP real Hermes health/card returned HTTP 200 with matching identity; all 51 tests passed again | Real authentication/single dispatch BLOCKED by unconfirmed compatible credentials; native Dots MCP registration BLOCKED. No real message or existing service changes; not new hardware/account. See [acceptance matrix](ACCEPTANCE_2026-10-06.en.md). |
| 2026-10-06 22:18 (0.4.0 real B task) | User personally handed off distinct named credentials; only caller trust appended, idle work zero checked then gateway restarted. CLI→loopback Hermes one SendMessage returned HERMES_OK, HTTP 200/TASK_STATE_COMPLETED, 7.69 seconds; matched audit/session confirm caller and zero tool calls | Intermediary not used; new hardware/accounts/native Dots MCP/shutdown experiment/long tasks untested. Private case IDs stay local, public ZIP sanitized; no commit/push at acceptance time. See [matrix](ACCEPTANCE_2026-10-06.en.md). |
| 2026-10-06 (0.4.0 public update) | New bridge/isolated installer, 24 document pairs and sanitized completed-B evidence update existing public main; 69-file allowlist with pre-publication offline/syntax/language/secret checks | Kit source only, no new tasks/server changes; new hardware/accounts/native Dots MCP remain untested. Exact commit/CI checked in delivery. |

## 2026-10-08 D: owner-reported Web evidence

The owner reports a successful Web test with ChatGPT desktop closed on both Macs; real Hermes output contained the test nonce, about 31 seconds, exit 0. This is case evidence for D private MCP / Tunnel persistent-worker CLI, not C cloud-tailnet success or an independent rerun during this documentation edit. Public documents retain no nonce, hostnames, identities, private paths, usernames, or dialogue. Mobile and new hardware remain untested; see the acceptance conditions below for limitations. This does not claim publication or full-validation PASS for this update.

### 2026-10-08 acceptance conditions and timeout lesson

Currently evidenced route: `dot → private MCP plugin → Secure MCP Tunnel → host stdio MCP worker → local Hermes`. Historical A/B require desktop; the independent channel does not mean the old installer can install tunnels. No plugin configuration schema is assumed.

The main web/macOS conversation sent a fresh nonce echo directly through the connector: actual result matched, exit 0, about 31 seconds. The user reported ChatGPT desktop was not open on either Mac; this condition is user-reported, not independently verified by process inspection. Mobile, new machines, restart recovery, and long-task reliability remain unaccepted.

A subsequent long documentation task explicitly ended in TimeoutError. Queue/accepted is not done: require terminal state + actual result + return code; success requires the expected result and return code 0. Query an existing task with unknown outcome first; do not resend. A short echo success does not establish long-task reliability or successful GitHub publication. No nonce values, task IDs, host identifiers, private paths, or credentials are published. This publication retains version 0.4.0 and the 69-file manifest.

Official references: [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels), [Add custom MCP server](https://developers.openai.com/api/docs/guides/custom-mcp-server). Official guides do not substitute for acceptance of this kit's installer.

## Still unverified (separated by route)

- Full intermediary bridge source, dependencies, registry loader, MCP input schema, and end-to-end results after a new port.
- B actual intermediary-shutdown experiment; one local CLI task passed without using it.
- Native Dots MCP registration/dispatch for B on 2026-10-06 and every new hardware/account; one local authenticated CLI task passed without proving those deployments. D Web evidence is recorded separately and does not close mobile/new-hardware acceptance gaps.
- Persistent cloud C runtime/socket/egress feasibility; evaluated without success.
- Complete deployment on Linux, Windows, Intel Mac, or other OS/architectures.
- Long tasks, every tool, combined profiles, multiple callers, task recovery after service restart, and the full Hermes pytest suite.
- Reliable fleet_ask result retrieval/deduplication after timeout; server GetTask does not establish that bridge workflow.
- A fixed minimum Dots app build. The kit does not promise unattended deployment merely by logging into a dot.

Historical records remain separate from current source observations. Original A repair/task was not repeated; new B evidence has its own date and does not reuse old success as fresh acceptance. [Source records](SOURCES.en.md)
