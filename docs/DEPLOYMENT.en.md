# Detailed deployment order

[繁體中文](DEPLOYMENT.md) | **English**

These are operator steps **not performed while creating this kit**. Commands were checked against the local parser/official documentation; check `--help` again for a newer version. Assess downtime before changes to existing services. Do not apply these steps directly to the case machines.

## 1. Record architecture and authorization

Fill in the [parameter table](PARAMETERS.en.md), choose A or B, and list permissions. Confirm the new target host, downtime window, backup, and rollback owner. [Prerequisites](PREREQUISITES.en.md), [security](SECURITY.en.md)

## 2. Prepare official software and clean source

Install ChatGPT and Hermes from official sources; add Tailscale for A. Record versions/SHA and installation owner. Do not run unknown bootstraps in an active Hermes home or install a full set of outdated dependencies. Stop if source has conflict markers or expected local-readonly security customization is absent; check compatible source.

## 3. Prepare the Hermes gateway

First confirm the profile has a working model. On the new machine only, run:

```sh
hermes gateway setup
```

Select A2A and compare the result with the [server config fragment](../examples/server-config.fragment.example.yaml). Setup can configure several platforms and secrets. The user operates its private interface; do not include complete wizard output in the deliverable.

Add named trust, loopback, and display name through [incremental configuration](CONFIGURATION.en.md). Prepare restricted mode before Serve. The user completes [peer-token handoff](SECURITY.en.md), checks caller/reserved identity mapping, and removes conflicting non-empty environment trust overrides. Once named remote access is ready, set `a2a.local_bridge_only: false`.

## 4. Start and verify one gateway

For first startup on the new host, foreground mode is available (keep the terminal open):

```sh
hermes gateway run
```

If an official macOS background service is needed and installation is authorized, the inspected parser supports:

```sh
hermes gateway install --no-start-now
hermes gateway start
```

Check `hermes gateway --help` first. Do not run foreground and service modes together or use `--force` / `--replace` to bypass an existing supervisor. Use the new installation's label; do not copy the case label or create a hardcoded plist. Startup/restart affects the gateway's other platforms too, not only A2A.

Read-only local checks:

```sh
lsof -nP -iTCP:9900 -sTCP:LISTEN
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
```

`lsof` checks listeners without printing full process argv/environment. Expect only the intended gateway on loopback 9900. Investigate port conflicts; do not kill unknown processes.

## 5A. Configure tailnet Serve for A only

Both users sign into the authorized tailnet. The administrator checks caller→target:10000 grants/ACL and MagicDNS/HTTPS. Inspect existing `tailscale serve status` and `tailscale funnel status` locally without publishing full output. If the port/path already exists, assess and back it up first; do not overwrite it.

After token/trust checks and authorization to add this service:

```sh
tailscale serve --bg --https=10000 http://127.0.0.1:9900
tailscale serve status
```

This changes Serve and is not executed automatically by the kit. It should report tailnet-only access with loopback 9900 as its target. Do not change it to Funnel. Do not reset or overwrite global configuration; preserve other Serve/Funnel entries. [Official Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve)

Run health/card on the caller Mac using the new host's actual DNS. Verify TLS, agent name, and card URL first. [Acceptance](VALIDATION.en.md)

## 6A. Install the new kit bridge or obtain the original case bridge

New deployments may use this project's original bridge. Follow the [Mac mini installation guide](MAC_MINI_BRIDGE.en.md): plan, explicit apply to a fresh private prefix, and manual pinned URL/expected_name configuration. Start with health/card, without automatic dispatch. MCP transport is stdio; configure the chosen client using its actual format, without global automatic registration.

The user personally prepares a new raw caller token outside kit/prefix. Use explicit send/query only after server named trust, reserved-identity checks, compatible-contract review, and separate authorization. The new implementation passed mocks/isolated installation but has no real Hermes acceptance and is not a port of the original bridge.

Original case fleet_ask use still requires owner-authorized non-secret source/lockfile/registry loader/tools-list schema. Stop that original-file path until obtained. Do not retrieve from unauthorized hosts or guess parameters. [Contracts and differences](BRIDGE_CONTRACT.en.md)

## 5B. Connect Dots directly to the Hermes Mac

In that machine's ChatGPT app, use dot profile → Computers → Your computer → Allow access. The user reviews and confirms access. Keep the machine awake/online with the app open. Create a separate local task and check its actual environment. A separately authorized `printf 'EXAMPLE_LOCAL_EXEC_OK\n'` can establish local execution; this is not Hermes task dispatch.

B can use the new kit bridge: isolated installation per the Mac mini guide, then real-path acceptance with loopback/new named caller credential. Local-only B does not need Serve. Do not remove token/trust for convenience. If reusing verified bridge source, recheck local paths, registry URL, and identities; this kit does not include that source.

## 7. Acceptance and handoff

Complete the [acceptance matrix](VALIDATION.en.md) and [checklist](../DEPLOYMENT_CHECKLIST.en.md). Actual task dispatch on the new machine requires separate user authorization and only one specified HERMES_OK message. Keep redacted results and versions. If a timeout leaves the outcome unknown, stop and check manually; do not resend. Hand off the guide and kit ZIP; keep secrets/backups separately under controlled access.
