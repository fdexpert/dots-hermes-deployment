# Troubleshooting

[繁體中文](TROUBLESHOOTING.md) | **English**

| Symptom | Check in order | Safe response |
| --- | --- | --- |
| Connection refused | Correct task host; loopback 9900 listener; gateway/profile/port; Serve target | Diagnose read-only first. Do not bind 0.0.0.0, kill unknown processes, or restart blindly. |
| health/card/RPC 403 or `only /local-readonly is available` | local_bridge_only; deployed version's GET/POST behavior; token mapped to reserved identity | Check the security contract. Complete named-token/trust handoff and obtain authorization before changing mode. Do not remove local_readonly. |
| RPC 401 | Peer-token name:token format; client raw token; startup profile/secret source; server reload | User checks locally. Do not paste tokens or add Bearer to the registry value. |
| RPC 403 peer not trusted | Authenticated caller in trust; reserved identity restriction; environment override | Do not enable allow_all_users. Use a valid distinct caller credential instead of the reserved identity. |
| Missing peer fields / target not found | Registry alias, required keys, caller_id, URL, token | Obtain original loader/schema. Without source, stop bridge setup rather than guessing key names. |
| Trust still wrong after YAML edit | Non-empty A2A_TRUSTED_PEERS override; launchd/shell/profile sources; capture at service startup | User reviews locally, keeps one authority, and plans restart. Do not print full environment. |
| Git conflict / SyntaxError | Conflict markers/syntax in fixed A2A source files; compatible source and local-readonly customization | Prefer clean compatible source; merge block by block with security tests. Do not blindly choose ours/theirs or apply the case repair to all machines. |
| stdio tool absent / HTTP MCP fails | MCP client launches Python stdio bridge; cwd/dependencies; tools/list | Dots computer connection does not register the bridge automatically. Serve exposes A2A, not MCP. |
| Agent Card URL is 127.0.0.1 | A registry URL override; version's A2A_PUBLIC_URL support | Do not follow the card back to the caller. Update advertised URL incrementally and verify TLS; generic clients may not override it. |
| TLS / DNS error | Full .ts.net DNS; tailnet sign-in; HTTPS authorization/certificate; port ACL | Do not use -k/insecure. Correct routes/official HTTPS configuration within authorization. |
| fleet_ask timeout around 300 seconds | Server still running; known task reference; bridge result retrieval | Do not resend unknown outcomes. Server GetTask does not prove bridge retrieval exists. |
| B offline / cannot continue | Hermes Mac awake/networked; ChatGPT app; Dots computer permission | Restore availability. Connecting/switching a computer does not migrate the original task. |

The inspected checkout's local_bridge_only returns 403 for GET, but POST may reject authentication first with 401. The earlier case observed 403 throughout. This reflects version/repair-state differences; check semantics and actual source rather than inferring settings from one status. [Sources and dates](SOURCES.en.md)

Do not attach full logs. Check the error category and necessary line numbers locally, then provide a short redacted excerpt. Diagnostics output fixed fields without arbitrary response or exception contents.
