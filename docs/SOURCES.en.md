# Sources, inspection dates, and command evidence

[繁體中文](SOURCES.md) | **English**

Inspection date: 2026-10-06 UTC. No real `.env`, client registry, credential values, or full logs were read. No SSH to the intermediary Mac. Inspected source is not packaged in the kit.

## Local non-secret source

Checkout: `hermes-agent` from a Hermes source installation. Inspected revision: `d0288be5b3330d2442e3907185b8e9d0958297bb`; tracked A2A diff was empty. This is the **checkout used to verify documentation**, not the commit at the 2026-10-05 repair or proof of the gateway runtime version.

| Relative path | Evidence |
| --- | --- |
| `plugins/platforms/a2a/security.py` | name:token parser; environment trust precedence; allow-all; token-mapped identity; loopback; reserved identity; local_bridge_only |
| `plugins/platforms/a2a/adapter.py` | port/name/public-url; GET health/card; POST authentication→trust→method order; timeout; gateway session |
| `plugins/platforms/a2a/protocol.py` | supportedInterfaces; JSONRPC; protocolVersion 1.0; securitySchemes; -32601/-32052 |
| `plugins/platforms/a2a/__init__.py` | enabled/port activation and platform registration |
| `plugins/platforms/a2a/local_readonly.py` | Fixed restricted route exists; preserve it and do not treat it as task dispatch |
| `gateway/config_loader.py` | Nested gateway.platforms source and extra propagation |
| `hermes_cli/subcommands/gateway.py` | setup/run/install/start/status/restart parser; install --no-start-now |
| `website/docs/user-guide/messaging/a2a.md` / `pyproject.toml` | Server config, A2A interfaces, and requires-python; no claim that A2A needs a nonexistent extra |

SHA256 for traceability, not a requirement that every new version match:

```text
security.py c8f89aaed3530e6a41a77ace27d91aabe07d01ab688b6bf0de69bec5e5bd1248
adapter.py  07bf49f3f7afab47ddae946c14d991dbee34574b832cf2f48667161cba67dfed
__init__.py e74718adedde494c87c53f432a676c9e827302bee9187e6856eb7a21a62524bd
local_readonly.py ffde80a9f72c4d12e2216392c23b14c832faf6db3a369bff52719f924afb3296
```

`tailscale version` reported 1.102.4. `tailscale serve --help` confirmed --bg, --https, and status flags. No Serve mutation command was executed. Kit tools use Python stdlib without importing Hermes or launching its CLI.

## Official references

- [Dots Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps): computer authorization and online/app requirements.
- [Remote connections](https://learn.chatgpt.com/docs/remote-connections): remote hosts/environments; separate from Dots computer permission.
- [Tailscale userspace](https://tailscale.com/docs/concepts/userspace-networking): proxy concepts, not evidence of successful C deployment.
- [Tailscale Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve): HTTPS/bg/status and entry-specific off.
- [Tailscale macOS](https://tailscale.com/download/mac): official installation source.
- [Hermes installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation/), [A2A](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a/), [official source](https://github.com/NousResearch/hermes-agent).
- [Python macOS](https://www.python.org/downloads/macos/).

Official sites change. Check compatible versions and actual --help during deployment rather than hiding version differences. Bridge fields/schema remain pending source; generic MCP/A2A documents do not establish the original bridge implementation.
