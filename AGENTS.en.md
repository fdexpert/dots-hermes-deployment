# For dots / agents working in this project

[繁體中文](AGENTS.md) | **English**

This is a deployment kit, not an installed bridge. Read README, docs/VERIFIED_RECORD, and docs/BRIDGE_CONTRACT in your chosen language first. Report in Traditional Chinese or English according to the user's choice.

## Deployment entry point

Start deployment only when the user **explicitly requests deployment to a named host** and that host is connected and authorized. Logging into a dot or opening the repository does not authorize automatic execution. Do not set up persistent login triggers, GitHub Actions remote deployment, automatic authentication, credential synchronization, or default task dispatch.

1. Check the host and cwd. Inventory versions, sources, listeners, and existing routes read-only; run the kit's offline tests and `diagnose.py preflight`.
2. Confirm A or B, parameters, profile, bridge-source gaps, and authorization scope. C is unverified. Do not claim a complete bridge port without its full source.
3. Use `examples/deployment-plan.example.json` and `scripts/plan.py` to produce a **secret-free dry-run change plan with no writes**. List existing routes and settings to preserve, steps, downtime, and recovery. The planner cannot read real config or replace actual inventory.
4. Complete a concrete, reviewable plan before obtaining explicit confirmation for service/security changes, downtime, or route replacement that has not already been authorized. Do not repeat approval requests within existing authorization. Without approval, continue independent read-only/offline work only.
5. The user configures every secret through a trusted private local interface. Do not read or copy an old `.env`, real registry, or token into the repository; request tokens in chat or command arguments; or generate or move secrets automatically.
6. The operator follows docs/DEPLOYMENT incrementally. Preserve other platforms, trust entries, Serve, and Funnel configuration. Do not overwrite whole files, reset configuration, choose git ours/theirs blindly, enable Funnel/allow-all/0.0.0.0, or bypass TLS.
7. Four-layer acceptance: the first three layers allow safe probes within authorization; actual task dispatch requires separate approval before sending the specified HERMES_OK message once. Do not resend unknown results. B still lacks complete evidence for local task dispatch and independence from the intermediary Mac.
8. Keep redacted changes and results, then hand off the kit. On failure, pause new tasks and let the original owner recover this change. Do not change real services to test scripts.

## Modifying and publishing this project

New tools default to read-only/dry-run. Before adding any deployment tool that can write, cover idempotence, dry-run, preservation of user settings, failure recovery, and offline fake-runner tests. Do not test against existing services or write automatic security-repair scripts.

Run `python3 -B -m unittest discover -s tests -v` and `python3 -B scripts/validate_kit.py` first. The ZIP uses an explicit allowlist and secret scanning. Do not package a real `.env`, registry, `.git`, backups, logs, or Library helpers.

GitHub publication requires user approval of owner/repository and visibility. An email is not a GitHub login. Publish publicly only within authorization after scanning all content and publishable history. If an existing repository contains unrelated content or questionable history, stop public publication without widening this kit's scope. The kit has no CI deployment hook or automatic secret-reading workflow.
