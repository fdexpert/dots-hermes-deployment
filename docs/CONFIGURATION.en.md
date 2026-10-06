# Secret-free configuration and incremental updates

[繁體中文](CONFIGURATION.md) | **English**

The new bridge uses [bridge-config JSON](../examples/bridge-config.example.json), separate from the original registry below; see [Mac mini schema](MAC_MINI_BRIDGE.en.md). Installation does not modify the server; operators still merge server fields individually.

## Keep configuration separate

| Template | Type | Placement / update |
| --- | --- | --- |
| [Server config](../examples/server-config.fragment.example.yaml) | Fragment with actual Hermes fields | Merge only `gateway.platforms.a2a` into the new host's effective config; preserve other platforms. |
| [Server trust](../examples/server-trust.fragment.example.yaml) | Actual trust fields in the inspected security.py | Update only top-level `a2a.trusted_peers` / `local_bridge_only`; preserve other `a2a` keys. |
| [Non-secret environment](../examples/server-env.example.txt) | Template using actual variable names | User adds entries incrementally to the new host's private settings source; not a complete `.env`. |
| [Peer-token format](../examples/peer-token-format.example.txt) | Format illustration, not a usable secret | Do not load directly. User configures it outside the kit and preserves existing peers. |
| [Client registry](../examples/client-agents.schema-pending.example.yaml) | Some case fields known; complete schema awaits source | Only `caller_id` and `agents.<alias>.token` semantics are confirmed. The `url` loader is unavailable; this is not verified original bridge configuration. |

## Semantics and precedence

The inspected `security.py` splits `A2A_PEER_TOKENS` on commas, then the first colon separates name/token. Identities should not contain colons/commas; avoid commas and whitespace in tokens, and never reuse one value for multiple identities. No file provides a valid token.

Non-empty `A2A_TRUSTED_PEERS` takes precedence over YAML `a2a.trusted_peers`. Even a stale non-secret placeholder in `.env` overrides YAML. The user checks launchd/shell/profile/`.env` sources **locally**, keeping one explicit trust authority. Do not print the full environment. The case removed a stale override and used YAML; this kit has no automatic modification script.

Non-empty `A2A_PORT` overrides `extra.port`. `A2A_HOST` defaults to loopback; the kit explicitly keeps `127.0.0.1`. `A2A_AGENT_NAME` is the card's displayed identity. `A2A_PUBLIC_URL` can advertise a reachable card URL when supported and verified in that version; it does not create a route or grant access.

`local_bridge_only: false` does not remove the reserved identity restriction. Tokens mapped to the actual server's reserved local bridge identity remain denied general RPC. The public kit omits the case's private fixed identity; check the constant in compatible source. Do not remove `local_readonly.py` or turn the reserved identity into a full-access caller.

## Safe incremental procedure

1. The user backs up effective configuration and permissions locally under controlled access; do not upload secret backups.
2. Check the released version's loader and active profile/`HERMES_HOME`. Do not guess config paths across installation types.
3. Merge needed fields individually in a private editor. Preserve other platforms, models, tools, Serve, and peers. Fragments are not complete config; never use `cp fragment config.yaml`.
4. Check duplicate YAML keys, indentation, types (booleans are not arbitrary strings), peer-name mapping, and port precedence. Use the official loader's local validation method without publishing config output.
5. Restart the new gateway only in the planned downtime window. The adapter captures settings at startup; editing a file may not take effect immediately. [Downtime and recovery](OPERATIONS.en.md)

Do not resolve Git conflicts by choosing entire `ours` / `theirs` files blindly or treat the case's twelve-block repair as a standard installation step. Prefer compatible, conflict-free source. When a merge is needed, review security behavior block by block and test it.
