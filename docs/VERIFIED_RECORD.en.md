# Verified deployment record and unverified items

[繁體中文](VERIFIED_RECORD.md) | **English**

All dates are UTC. The public edition retains only anonymized summaries. “Intermediary Mac / Hermes Mac” are generic roles. Original host names, identities, service labels, and identifying parts of local execution markers are omitted; they are not new-deployment defaults.

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

## Still unverified

- Full intermediary bridge source, dependencies, registry loader, MCP input schema, and end-to-end results after a new port.
- B local Hermes task and independence with the intermediary not participating.
- Persistent cloud C runtime/socket/egress feasibility; evaluated without success.
- Complete deployment on Linux, Windows, Intel Mac, or other OS/architectures.
- Long tasks, every tool, combined profiles, multiple callers, task recovery after service restart, and the full Hermes pytest suite.
- Reliable fleet_ask result retrieval/deduplication after timeout; server GetTask does not establish that bridge workflow.
- A fixed minimum Dots app build. The kit does not promise unattended deployment merely by logging into a dot.

Historical records remain separate from current source observations. Documentation work did not repeat the original repair or task; prior success is not represented as fresh acceptance. [Source records](SOURCES.en.md)
