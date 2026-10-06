# Roles and replaceable parameters

[繁體中文](PARAMETERS.md) | **English**

Start with the [secret-free deployment plan](../examples/deployment-plan.example.json). It is the kit's planning format, not configuration that Hermes or the bridge can load directly.

| Parameter / role | Example value | Purpose / check |
| --- | --- | --- |
| `caller_id` | `example-caller` | Caller in the bridge registry; the server identity resolved from the peer token must match `trusted_peers`. A caller in the request body does not replace authentication identity. |
| `target_alias` | `example-target` | Node key in the client registry; not the server's security identity. |
| `target_identity` | `hermes-example-target` | `A2A_AGENT_NAME`, health `agent`, and card `name`; diagnostics use this to check the target. |
| `target_hostname` | `example-hermes.example-tailnet.ts.net` | The new machine's actual full Tailscale DNS name. The example does not resolve. |
| `listen_host` | `127.0.0.1` | Hermes A2A loopback binding. Do not change to `0.0.0.0`. |
| `a2a_port` | `9900` | `gateway.platforms.a2a.extra.port` / `A2A_PORT`. Investigate any existing listener first. |
| `serve_https_port` | `10000` | Tailnet TLS entry for A; keep grants/ACL and registry URL consistent. |
| `base_url` | `https://example-hermes.example-tailnet.ts.net:10000` | Registry override URL for A; B can use `http://127.0.0.1:9900` locally. No credentials/query/fragment. |
| `hermes_data_home` | `/Users/example/.hermes` | Use the new machine's effective `HERMES_HOME` / profile. This is not the source checkout. |
| `hermes_source` | `/path/to/hermes-source` | For non-secret source inspection; not every installation has this directory. |
| `bridge_path` | `/Users/example/.hermes-fleet/a2a_bridge.py` | Replace after obtaining authorized original source for A; stop bridge setup if it is absent. |
| `registry_path` | `/Users/example/.hermes-fleet/agents.yaml` | Real registry contains a token and stays outside the kit. |
| `python_path` | `/path/to/bridge-venv/bin/python` | Use Python and dependencies verified with the acquired bridge. |
| `gateway_service_label` | `example.gateway.label` | Use the label produced by the new installation; do not copy the case service label. |
| `reserved_local_identity` | `example-local-bridge` | Public planning example only. In the deployment copy, enter the reserved identity constant from the actual server's `security.py`. Do not rename that fixed identity or relax its restrictions to match a new hostname. It is not a task caller. |

Give every caller a distinct token. For every target/client pair, confirm the raw token maps to the same named caller. Do not copy other machines' tokens with an identity table. Changing a port requires matching changes to the server, Serve target, URL, and tests. Changing the caller requires matching peer-token names, trust, and registry caller.

The public kit omits the case's private reserved identity string. `REPLACE_WITH_ACTUAL_RESERVED_IDENTITY` is a format placeholder, not a configurable field for renaming the server identity. Check the fixed value in compatible source. The planner's `reserved_local_identity` only rejects misuse as a caller; it does not modify server identity constants.
