# Security and credential handoff

[繁體中文](SECURITY.md) | **English**

## Minimum trust

- Hermes listens only on `127.0.0.1`; A uses Tailscale Serve as a tailnet-only HTTPS reverse proxy. Grants/ACL allow only necessary callers to the target HTTPS port. Do not configure Funnel, public ingress, or broad all-user access.
- List named callers in `a2a.trusted_peers` and use `A2A_ALLOW_ALL_USERS=false`. The inspected source accepts authenticated peers when trust is empty; **an empty list does not deny everyone**.
- Use `A2A_PEER_TOKENS`; a shared bearer or caller IP does not replace named peer trust. A token-free localhost-only mode cannot prove remote authentication. Serve connects from localhost, so complete tokens/trust before enabling it.
- Check the reserved local bridge identity in the actual server source. Preserve its distinct token and `/local-readonly` restriction. Do not use it for general RPC or map another caller's token to it. Do not load the public `REPLACE_WITH_ACTUAL_RESERVED_IDENTITY` placeholder directly.
- `local_bridge_only: true` restricts the general surface. For named remote A2A, complete distinct peer tokens and trust first; an authorized operator can then change it to `false`. A 403 alone is not a reason to relax it.
- Do not bypass TLS or put credentials in URLs, chat, command arguments, stdout, screenshots, or public documents. Do not enable debug HTTP tracing.

## User-operated credential handoff

1. Identify the new host/caller and controlled settings location. Prepare owner-readable secret storage outside the kit.
2. The user creates and enters new tokens through a trusted password manager/private local interface. The kit does not generate, read, move, or rotate existing secrets.
3. The server needs comma-separated `name:token` pairs in `A2A_PEER_TOKENS`, with distinct values for each identity. This is not JSON. Edit locally in a private editor and preserve existing valid entries.
4. Store the paired **raw token** in client registry `agents.<target_alias>.token`; no `Bearer ` or `caller:` prefix. Keep the registry outside the kit with owner-only permissions such as 600.
5. Do not report values. Report only “caller configured, trust checked, permissions confirmed.” Authentication diagnostics use a hidden local prompt and refuse if getpass cannot hide input.
6. The user configures the Hermes model provider, Tailscale sign-in, and app account on the new host. Do not move an old `.env` or entire home into the shareable kit.

See [incremental configuration](CONFIGURATION.en.md) for format details. Templates contain clear placeholders and are not usable credentials. `.gitignore` helps prevent accidental inclusion; it does not store secrets safely. ZIP packaging separately uses an explicit allowlist and content scans.

## Permission boundaries

App installation, Dots computer access, tailnet membership, grants/HTTPS changes, and service startup each require appropriate authorization. Enable macOS file access/automation/Computer Use permissions only as needed for the task. Shell/A2A alone does not imply full-disk, screen, or global automation access. Existing services, security settings, and credentials are outside the changes made to create this kit.
