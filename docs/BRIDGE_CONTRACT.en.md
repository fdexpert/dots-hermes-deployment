# stdio bridge interface contract and missing source

[繁體中文](BRIDGE_CONTRACT.md) | **English**

## Known contract (case record, not a complete schema)

| Interface | Confirmed | Missing / must be checked |
| --- | --- | --- |
| Process transport | Python stdio MCP `a2a_bridge.py` | Python/MCP SDK/dependency lock; startup flags/cwd; clean stdout |
| Registry | `agents.yaml`, `caller_id`, raw token at `agents.<target>.token` | Full YAML loader, URL key name, required peer fields, timeout setting name |
| MCP tool | Name `fleet_ask`, remote-node selection, text message, synchronous result | Complete `tools/list` input schema; do not guess parameter names such as `agent` / `node` / `target` |
| HTTP | Registry HTTPS overrides the case card's loopback URL and sends a bearer credential | Override precedence; card v1/legacy compatibility; TLS/redirect handling |
| Task result | HTTP 200, TASK_STATE_COMPLETED, reply text, elapsed time, remote tool calls | Schema/error mapping/complete task lookup workflow |
| Timeout | Case synchronous wait about 300 seconds; no complete retrieval of unknown outcomes | Server GetTask does not establish that the bridge exposes result retrieval |

The kit does not invent a `fleet_ask(...)` command or include a substitute MCP server. Diagnostics only provide health/card and a constrained auth probe; they cannot dispatch tasks. The client registry filename explicitly says schema pending and must not be treated as verified loader input.

## Admission checks after source is obtained

1. Verify the owner's permission to share source/dependencies. Remove embedded secrets, real registry data, logs, and backups.
2. Record source revision/SHA and license terms. Test in a separate environment on the new caller without changing existing services.
3. Check that credentials go only to the explicit target; URL userinfo/query is rejected; TLS is verified; redirects cannot leak tokens; stderr/errors do not print secrets.
4. Obtain MCP `tools/list`; record the actual input schema and redacted registry keys. Update the pending template and CHANGELOG from that evidence.
5. Reject missing tokens/peer fields, reserved identities, and callers outside trust. Do not automatically resend unknown tasks after timeout/restart.
6. Pass fixture/unit tests and syntax checks first. Separately authorize one HERMES_OK task before marking a complete A bridge port as validated.

The intermediary Mac is not currently authorized for source retrieval. Do not SSH to it to obtain source. Without source, retain this gap and complete only the server, computer connection, and diagnostic work that is available.
