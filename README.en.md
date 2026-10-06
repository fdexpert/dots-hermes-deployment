# Dots × Hermes Deployment Kit

[繁體中文](README.md) | **English**

Version: 0.3.0 | Compiled and checked: 2026-10-06 (UTC) | Languages: Traditional Chinese and English

This reusable project provides architecture decisions, an operator deployment guide, secret-free templates, read-only diagnostics, offline tests, and acceptance checklists for other machines. It does not include the complete intermediary bridge, existing credentials, a real registry, backups, or logs. Building this kit did not deploy a new machine or change existing services. GitHub publication was separately authorized; see the [publication audit](PUBLICATION_AUDIT.en.md).

## Choose an architecture

| Path | Execution location and data flow | Evidence and use |
| --- | --- | --- |
| A: intermediary Mac | Dots → connected Mac executor (case: intermediary Mac) → Python stdio a2a-bridge → Tailscale Serve HTTPS :10000 → Hermes host (case: Hermes Mac), 127.0.0.1:9900 | One remote HERMES_OK task completed in the case. A new deployment needs authorized original bridge source, dependencies, and registry schema. This kit does not present a substitute as the original implementation. |
| B: direct Mac | Dots → executor on the Mac running Hermes → local execution / local A2A client → 127.0.0.1:9900 | Local execution and health/card were verified on the Hermes Mac. A local Hermes task and independence with the intermediary unavailable have not been tested. Suitable when an intermediary is unnecessary. |
| C: cloud runtime | Dots cloud environment → userspace networking / proxy → tailnet A2A | Socket, egress, and persistence limits were evaluated; implementation did not succeed. This is not a deployable option in this kit. |

Dots “connect a computer” provides an executor; it does not convert stdio MCP into an HTTP MCP endpoint. HTTPS :10000 in the case is **Hermes A2A HTTP**, not MCP HTTP. See [architecture and roles](docs/ARCHITECTURE.en.md). Official Dots documentation distinguishes cloud and personal computers; the personal computer must be online with the app open, and its access permission is separate from Codex connections: [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps).

## Quick start

1. Extract the ZIP into your own project directory. Read [prerequisites](docs/PREREQUISITES.en.md) and [security / credential handoff](docs/SECURITY.en.md). Deploy only to an authorized machine.
2. Fill in new identities, hostnames, ports, and paths using the [parameter table](docs/PARAMETERS.en.md). Replace every `example` / `REPLACE_` value in your deployment copy. Do not reuse the case identities or tokens.
3. Run the kit's offline checks first. They do not connect, dispatch tasks, or read real configuration:

   ```sh
   python3 -B -m unittest discover -s tests -v
   python3 -B scripts/validate_kit.py
   python3 -B scripts/diagnose.py preflight
   ```

4. Follow the [deployment guide](docs/DEPLOYMENT.en.md) in order. Until bridge source is obtained, path A can only complete server and network preparation. For B, establish the direct computer connection first.
5. Record the [four-layer acceptance](docs/VALIDATION.en.md), then complete the [deployment checklist](DEPLOYMENT_CHECKLIST.en.md). HTTP 200 alone does not prove authentication or successful task dispatch.

Read-only connection examples (run on the target host or an authorized caller):

```sh
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target
```

The tools reject URL credentials, queries, fragments, non-root paths, and remote URLs outside the tailnet allowance. They do not follow redirects, disable TLS, or print complete responses. Optional `auth` probes an undefined RPC method without dispatching a task; verify the target Hermes rejection order first. It obtains a token through a local hidden prompt and accepts no command-line token. See [tool documentation](scripts/README.en.md).

## Documentation

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

This kit implements diagnostics and package validation. YAML and environment files are incremental templates. Complete stdio bridge source, MCP client registration instructions, and dependency locks are still needed. There is no automatic deployment, security repair, or automatic HERMES_OK script. The known `fleet_ask` synchronous wait is about 300 seconds, with no complete result-retrieval workflow after timeout; do not resend a task whose outcome is unknown. The direct executor requires the Hermes Mac to remain awake and online with the app running. Replacing the selected Dots personal computer does not migrate existing tasks. See [evidence and limitations](docs/VERIFIED_RECORD.en.md).

English and Traditional Chinese documents use the same technical keys, commands, and acceptance message. Example comments and the topology include both languages. CLI output remains in English.
