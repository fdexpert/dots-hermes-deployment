# Prerequisites, versions, and installation sources

[繁體中文](PREREQUISITES.md) | **English**

## Validation scope

On 2026-10-06, the Hermes Mac ran macOS 26.6.2 on arm64. Kit tools were verified with Python 3.14.5; Tailscale CLI was 1.102.4. The local Hermes checkout declared `requires-python >=3.11,<3.15`; that is not the intermediary bridge's requirement. The running Hermes version/service owner may differ from the checkout. Do not treat the checkout SHA as the gateway's running version.

| Component | Requirement / inventory for a new machine | Source / limit |
| --- | --- | --- |
| Dots / ChatGPT desktop | Dots available; correct account/workspace; computer access allowed; record actual app version | [Official Dots docs](https://learn.chatgpt.com/docs/dots/computers-and-apps). The case app build was not recorded, so no minimum version is claimed. |
| Hermes | Compatible A2A schema and conflict-free official source; identify profile/runtime owner first | [Installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation/), [official repo](https://github.com/NousResearch/hermes-agent), [A2A](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a/). Hermes code is not included. |
| Python | Kit tools require 3.11+; select Hermes Python according to its version's pyproject/package manager | [Python macOS downloads](https://www.python.org/downloads/macos/). Do not change the existing Hermes interpreter for this kit. |
| Tailscale | For A, both ends in an authorized tailnet; CLI supports Serve HTTPS and background mode | [macOS download](https://tailscale.com/download/mac), [Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve). Do not install multiple macOS distributions. |
| stdio bridge | New kit bridge: Python 3.11–3.14/stdlib/explicit JSON schema; isolated installation per Mac mini guide | Mocks, real loopback health/card and one B task passed; new hardware/native Dots MCP untested. Original dependencies/schema still missing. |
| Model provider | Working Hermes model access; user configures it personally on the new host | Use the Hermes installation flow and provider's private interface; keep credentials outside this project. |

The Hermes installation page checked for this kit offers macOS desktop and CLI installation; the macOS desktop package is marked Apple Silicon. Official Linux, Windows, WSL, or other support does not verify this case's Dots × bridge × Serve path. This kit reports macOS arm64 case results only. Intel Mac, Windows, Linux, containers, and headless hosts need separate compatibility checks and all four acceptance layers. Do not copy launchd commands to another OS. [Official installation page](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)

## Installation order

1. Install/update ChatGPT desktop from official sources; the user signs in and connects the Dots computer.
2. Choose one Hermes installation method from its official page. Check download source and version. Do not wire an installer into this kit for automatic execution; the operator performs installation and model authorization.
3. For A, install Tailscale from its official macOS source and let the user sign in. The administrator checks HTTPS/MagicDNS and minimal caller→target:10000 grants/ACL. Do not configure public Funnel.
4. Install the new kit bridge in a pip-free isolated venv using the [Mac mini guide](MAC_MINI_BRIDGE.en.md); no guessed mcp/httpx dependency. Original case use still requires source/lockfile. The new implementation must not be presented as the original file.

## Read-only inventory

```sh
sw_vers
uname -m
python3 --version
tailscale version
tailscale serve --help
hermes gateway --help
```

Record the desktop build from About and the Hermes runtime version from the installation owner. For a source checkout, run `git -C /path/to/hermes-source rev-parse HEAD` locally and record uncommitted changes/conflicts. Do not share complete configuration, environment, or service output; it may contain secrets.

Optional `python3 -B scripts/diagnose.py preflight --hermes-source /path/to/hermes-source` reads only fixed A2A source files for AST/conflict-marker checks. It does not import Hermes or read config/`.env`, and cannot prove the running gateway uses that checkout.
