# Architecture and roles

[繁體中文](ARCHITECTURE.md) | **English**

## A: intermediary Mac and remote Hermes

```text
Dots (coordinates work)
  └─ Computer-access permission → example-caller Mac (case: intermediary Mac)
       └─ Local task's MCP client → Python stdio a2a_bridge.py
            └─ Agents registry: HTTPS URL + raw peer token
                 └─ Tailnet-only Serve :10000 (Hermes host)
                      └─ HTTP 127.0.0.1:9900 → Hermes A2A → gateway session
```

Dots computer access, stdio MCP, and A2A HTTP are three different interfaces. A stdio client launches a subprocess and communicates through stdin/stdout. A `.py` path or Serve URL cannot be substituted into a different transport and expected to work. The case bridge was registered in Claude Desktop / Code, not globally in Dots; a local task called `fleet_ask`. Until source is obtained, a new Dots task cannot be assumed to have the same MCP client or tools.

The case also had SSH from the intermediary to the Hermes host for maintenance. It is separate from the verified A2A HTTPS task path. HTTPS deployment does not require opening SSH. If SSH is needed for administration, authorize it separately, verify the host key, and use a named account. Do not retrieve files from an unauthorized host.

## B: direct connection to the Hermes Mac

```text
Dots → authorized executor on example-target Mac
         ├─ Local command: establish execution location
         └─ Separately obtained and verified local A2A client
              → HTTP 127.0.0.1:9900 → Hermes gateway
```

B does not need the intermediary Mac. A local-only A2A path does not need Serve; configure tailnet Serve separately if remote callers are also required. Successful shell execution does not prove a task was sent to the Hermes agent. This kit's `diagnose.py` is not a local task client and does not provide `fleet_ask`.

## C: evaluated, unsuccessful

Userspace Tailscale can provide networking through SOCKS5 / HTTP proxies. That does not establish that a cloud executor permits a daemon/socket, outbound egress, or persistent process/state. This case has no successful end-to-end result, so the kit provides no startup script for C and does not treat proxy settings as a universal deployment solution. [Official userspace concepts](https://tailscale.com/docs/concepts/userspace-networking)

## Selecting a connected computer

Use Dots profile → Computers → Your computer → Allow access, with user confirmation. The official documentation checked for this kit permits one personal computer; the cloud computer remains connected. Switching can replace the selected personal computer. Existing tasks remain in their original execution environment. Create a separate task, check its actual cwd/OS/host, then test B. Do not substitute Codex Remote pairing for Dots computer permission. [Dots workflow](https://learn.chatgpt.com/docs/dots/computers-and-apps), [Remote documentation](https://learn.chatgpt.com/docs/remote-connections)
