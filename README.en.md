# Dots × Hermes Deployment Kit

[繁體中文](README.md) | **English**

Version: 0.4.0 | Compiled and checked: 2026-10-06 (UTC) | Languages: Traditional Chinese and English

This reusable project includes an original Python stdio MCP/CLI bridge, dry-run isolated installer, secret-free templates, and acceptance guides. Original intermediary source remains unavailable; this is not a port. No existing credentials, registry, backups, or logs are included. Start with [Mac mini installation](docs/MAC_MINI_BRIDGE.en.md). Clean-prefix installation and real Hermes CLI/standard stdio MCP health/card passed; one authenticated B local task also PASS: HERMES_OK, HTTP 200/completed, 7.69 seconds, zero agent tool calls. New hardware/accounts and native Dots MCP remain untested; see [acceptance](docs/ACCEPTANCE_2026-10-06.en.md). The local case separately authorized dedicated caller trust and required restart; the user personally configured credentials. Version 0.4.0 source is updated in the [existing GitHub project](https://github.com/fdexpert/dots-hermes-deployment); see [publication audit](PUBLICATION_AUDIT.en.md).

## Choose an architecture

| Path | Execution location and data flow | Evidence and use |
| --- | --- | --- |
| A: intermediary Mac | Dots → connected Mac executor (case: intermediary Mac) → Python stdio a2a-bridge → Tailscale Serve HTTPS :10000 → Hermes host (case: Hermes Mac), 127.0.0.1:9900 | One remote HERMES_OK task completed in the original case. New deployments can choose the kit bridge (mock passed, real path unverified); using the original bridge still requires authorized source/schema. |
| B: direct Mac | Dots → executor on the Mac running Hermes → local execution / local A2A client → 127.0.0.1:9900 | New bridge real CLI health/card and one named authenticated task passed: HERMES_OK, 7.69 seconds, zero tools. Native Dots MCP/new hardware/accounts/actual intermediary shutdown remain untested. |
| C: cloud runtime | Dots cloud environment → userspace networking / proxy → tailnet A2A | Socket, egress, and persistence limits were evaluated; implementation did not succeed. This is not a deployable option in this kit. |

Dots “connect a computer” provides an executor; it does not convert stdio MCP into an HTTP MCP endpoint. HTTPS :10000 in the case is **Hermes A2A HTTP**, not MCP HTTP. See [architecture and roles](docs/ARCHITECTURE.en.md). Official Dots documentation distinguishes cloud and personal computers; the personal computer must be online with the app open, and its access permission is separate from Codex connections: [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps).

## Quick start

1. Extract the ZIP into your own project directory. Read [prerequisites](docs/PREREQUISITES.en.md) and [security / credential handoff](docs/SECURITY.en.md). Deploy only to an authorized machine.
2. Fill in new identities, hostnames, ports, and paths using the [parameter table](docs/PARAMETERS.en.md). Replace every `example` / `REPLACE_` value in your deployment copy. Do not reuse the case identities or tokens.
3. Run the kit's offline checks first. They use owned mocks/temporary prefixes, without contacting existing services, dispatching real tasks, or reading real configuration:

   ```sh
   python3 -B -m unittest discover -s tests -v
   python3 -B scripts/validate_kit.py
   python3 -B scripts/diagnose.py preflight
   ```

4. Review the [Mac mini bridge installation](docs/MAC_MINI_BRIDGE.en.md) plan before explicit apply to a fresh private prefix. Prepare server/network through the [deployment guide](docs/DEPLOYMENT.en.md); for B establish the direct computer connection first. Installation does not dispatch tasks, configure server security, or register global MCP.
5. Record the [four-layer acceptance](docs/VALIDATION.en.md), then complete the [deployment checklist](DEPLOYMENT_CHECKLIST.en.md). HTTP 200 alone does not prove authentication or successful task dispatch.

Read-only connection examples (run on the target host or an authorized caller):

```sh
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target
```

The tools reject URL credentials, queries, fragments, non-root paths, and remote URLs outside the tailnet allowance. They do not follow redirects, disable TLS, or print complete responses. Optional `auth` probes an undefined RPC method without dispatching a task; verify the target Hermes rejection order first. It obtains a token through a local hidden prompt and accepts no command-line token. See [tool documentation](scripts/README.en.md).

## Documentation

- [Mac mini bridge / isolated installation / CLI and MCP](docs/MAC_MINI_BRIDGE.en.md)
- [0.4.0 acceptance matrix and private handoff](docs/ACCEPTANCE_2026-10-06.en.md), [structured evidence](docs/ACCEPTANCE_2026-10-06.json)
- [Architecture and roles](docs/ARCHITECTURE.en.md), [example topology](examples/topology.txt)
- [Prerequisites / installation sources / versions](docs/PREREQUISITES.en.md), [replaceable parameters](docs/PARAMETERS.en.md)
- [Deployment order](docs/DEPLOYMENT.en.md), [security / credential handoff](docs/SECURITY.en.md), [incremental configuration](docs/CONFIGURATION.en.md)
- [Bridge interface contract and missing source](docs/BRIDGE_CONTRACT.en.md)
- [Future dot entry point](AGENTS.en.md), [GitHub publication and deployment handoff](docs/GITHUB.en.md)
- [Four-layer acceptance](docs/VALIDATION.en.md), [troubleshooting](docs/TROUBLESHOOTING.en.md), [backup and recovery](docs/OPERATIONS.en.md)
- [Verified record and unverified items](docs/VERIFIED_RECORD.en.md), [source code and official references](docs/SOURCES.en.md)
- [Tools and tests](scripts/README.en.md), [checklist](DEPLOYMENT_CHECKLIST.en.md), [changelog](CHANGELOG.en.md), [delivery validation](DELIVERY_VALIDATION.en.md)
- [Complete file list](FILES.en.md), [ZIP allowlist](MANIFEST.json)
- [Public-release audit](PUBLICATION_AUDIT.en.md), [source and licensing boundaries](NOTICE.en.md)

## Delivery boundaries

The kit implements its own bridge, diagnostics, isolated installation, and package validation. YAML/environment files remain incremental templates. Original case bridge source/dependencies are still missing. The new bridge requires explicit SendMessage operation/confirmation; it does not deploy existing services, repair security, or dispatch during installation. The known `fleet_ask` synchronous wait is about 300 seconds, with no complete result-retrieval workflow after timeout; do not resend a task whose outcome is unknown. The direct executor requires the Hermes Mac to remain awake and online with the app running. Replacing the selected Dots personal computer does not migrate existing tasks. See [evidence and limitations](docs/VERIFIED_RECORD.en.md).

English and Traditional Chinese documents use the same technical keys, commands, and acceptance message. Example comments and the topology include both languages. CLI output remains in English.
