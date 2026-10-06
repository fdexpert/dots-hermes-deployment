# 0.4.0 acceptance matrix — 2026-10-06

[繁體中文](ACCEPTANCE_2026-10-06.md) | **English**

**Real authentication and one B-path local task PASS.** Installed 0.4 bridge CLI sent the single authorized message to loopback Hermes and returned exactly `HERMES_OK`: HTTP 200, `TASK_STATE_COMPLETED`, 7.69 seconds. Task-matched server audit and A2A session confirm the named caller; session tool use was zero. New hardware/accounts and native Dots MCP remain NOTTESTED.

All dates are UTC. Actual inbound: 2026-10-06 22:18:09.628; completion: 22:18:17.311. The 09:44 read-only/clean-prefix checks and credential BLOCKED state remain in initial_readonly_acceptance in [structured evidence](ACCEPTANCE_2026-10-06.json). The user personally completed credential handoff before the evening follow-up resolved that blocker. These are separate test windows.

## Version and environment

- Kit/bridge/installer: Acceptance used 0.4.0 source. Base Git commit `b2f4011589d40818f2eb01a75d78bd2a04dfdfa0` is the preceding 0.3.0. Acceptance preceded publication; later 0.4.0 source updates the existing public main, with exact revision in delivery.
- Bridge/installer implementation did not change for this acceptance; installed copies match source SHA. Exact hashes are in [structured evidence](ACCEPTANCE_2026-10-06.json).
- macOS 26.6.2, arm64, Python 3.14.5; stdlib-only isolated venv, no pip/system-site-packages/dependency downloads.
- Local Hermes: `http://127.0.0.1:9900`. Private host/caller/task/context/session identifiers are retained in the local result and delivery message, omitted from the public ZIP.

## Results

| Item | Status | Evidence and scope | Still needs acceptance |
| --- | --- | --- | --- |
| 0.4.0 source/version | PASS | Installed SHA match; MCP serverInfo.version=0.4.0; original fleet_ask not used | Independently check versions on new hosts |
| Same-host clean prefix | PASS | Zero-write plan→apply, actual isolated venv, changed:false repeat, preserved config, temporary uninstall/cleanup passed; separate private case client prepared | Not new hardware/account |
| CLI→real health/card | PASS | HTTP 200, expected identity match; passed again after restart; card advertises JSONRPC v1/bearer/loopback | GET alone does not prove authentication |
| Local task→standard stdio client→new bridge | PASS | initialize/initialized/tools-list/call, MCP 2025-11-25/server 0.4.0, only fleet_health/card, two real HTTP 200 calls | No MCP dispatch; not native Dots MCP |
| 51 mock/installer tests | PASS | Passed again at 09:44 in 1.460 seconds; synthetic tokens, owned mocks/temp prefixes; source unchanged since | Not complete Hermes pytest or real dispatch evidence |
| User credential handoff/minimal trust | PASS | User personally configured independent named peer/owner-only raw-token file; non-secret structure/permissions and bridge validation passed. Only new caller trust appended, preserving other YAML and identity restrictions | New hosts still need private handoff; no secrets in kit |
| Required gateway restart | PASS | Fresh runtime aggregate active work zero; approved restart, then new runtime PID/loopback listener/health/card matched. CLI returned zero before readiness; no blind second restart | In-flight/long tasks and restart recovery untested |
| Real authentication/one HERMES_OK task | PASS | One SendMessage, HTTP 200/completed/exact HERMES_OK/7.69 seconds; audit confirms authenticated caller | Other tasks/tools/profiles untested |
| Agent tool usage | PASS | Matched session tool_call_count=0, tool-role messages=0, persisted tool-call entries=0; read-only aggregates, no message content/tool arguments copied | Not acceptance of every tool feature |
| New hardware/new account | NOTTESTED | Authorized local Mac and new prefix only | Authorize another machine and repeat four layers |
| Native Dots MCP registration/dispatch | NOTTESTED | Connected local task launched CLI; stdio verified GET only. No new global registration/persistent access | Confirm supported native connection and scope |
| New bridge remote A/C/intermediary shutdown/long tasks | NOTTESTED | Bridge requests pinned to loopback; intermediary not used, but not actually shut down for an experiment | Separate path/reliable-retrieval acceptance |

## One real task record

The exact and only authorized input actually sent:

> 請只回覆 HERMES_OK，不使用工具、不修改檔案、不對外聯絡

Meaning: reply only HERMES_OK, without tools/file changes/external contact. Both editions retain the same Traditional Chinese input.

Exact reply: `HERMES_OK`. SendMessage attempts **1**, authenticated RPC attempts **1**, resends **0**, unknown outcome **false**. Task/context/request/session IDs and actual caller are in the private local result; the public edition retains sanitized evidence only. Earlier A-case success is not substituted for this 0.4 result.

## Authentication and restart boundaries

Hermes requires Bearer authentication, not a particular storage file. Version 0.4 accepts a user-private raw-token file or CLI `--prompt-token` hidden input; stdio has no interactive prompt. This case used the user's personally configured file, without exporting server secrets or rewriting the old registry. Reserved local-readonly identity cannot dispatch general tasks.

Non-empty A2A_TRUSTED_PEERS environment values override YAML; an empty string falls back to YAML. This case retained a non-empty named list, allow-all false, and loopback. An unmatched sentinel blocks existing legitimate callers and the new caller; do not blindly replace an approved list to restore an older restriction. The reserved identity retains its independent code restriction.

Default gateway restart affects platforms in the same process. Check fresh runtime and aggregate active work zero first; work may arrive afterward, so retain normal supervisor/drain rather than force/all-profile restart. Exit zero is not readiness: verify new PID/runtime/listener/HTTP before dispatch. Serve/Funnel were not changed.

## Reproduction and references

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py --public
```

See [Mac mini guide](MAC_MINI_BRIDGE.en.md) for installer/CLI/MCP commands; repeat [four-layer acceptance](VALIDATION.en.md) on another host. Do not automatically replay the completed task. Official Dots computer/plugin permissions are managed separately; local CLI success does not prove native MCP registration. [Dots computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)
