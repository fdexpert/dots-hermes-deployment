# Tools and offline tests

[繁體中文](README.md) | **English**

Python stdlib only, 3.11+. Tools do not install dependencies, read effective server/client configuration, or execute the Hermes CLI. Diagnostics require explicit URLs without scanning/dispatch. The new bridge requires explicit confirmation for SendMessage. CLI output is English in both document editions.

## bridge.py / install.py

See the [complete Mac mini guide](../docs/MAC_MINI_BRIDGE.en.md): original stdlib stdio MCP/CLI, explicitly confirmed dispatch and GetTask/ListTasks queries; installer defaults to plan, applies only to a fresh private prefix, and creates no services/security/global MCP.

## diagnose.py

- `preflight`: OS/architecture/Python and command availability; does not check service liveness. Optional `--hermes-source` reads five fixed A2A `.py` files for AST/conflict checks without importing code.
- `health --base-url … --expected-name …`: GET `/health`; reports fixed status/name-match fields, not the body.
- `card --base-url … --expected-name …`: GET canonical Agent Card; checks Hermes v1 JSONRPC, advertised bearer authentication, and loopback URL warnings. Legacy cards/multi-tenant non-root paths need separate review; the tool does not widen URL permissions.
- `auth … --confirm-hermes-contract`: optional undefined-method probe. Target health → unauthenticated rejection → hidden token prompt → fixed undefined method returns -32601, without a task. Use only with a Hermes version whose rejection order is checked and probe method is unregistered. [Acceptance contract](../docs/VALIDATION.en.md)

HTTP is allowed only for numeric loopback; remote URLs require HTTPS `.ts.net`. Default timeout is 10 seconds, maximum 30 seconds; body limit 64 KiB. Credentials/query/fragment in URLs, redirects, and non-diagnostic payloads are rejected. Automatic environment proxies are disabled; system TLS verification remains active. Arbitrary response/exception contents are not printed, preventing echoed secrets. There are no token arguments, environment/file token input, `.env`, or registry import options.

`health` / `card` deliberately report `authentication_proven=false`. Interpret `card.ok` with its loopback warning; remote access needs registry override or supported PUBLIC_URL. Passing a tool is not complete deployment acceptance. Auth can affect rate-limit counters/audit records and cannot replace private local security review. Python strings cannot guarantee memory erasure.

## plan.py (always dry-run)

```sh
python3 -B scripts/plan.py --spec examples/deployment-plan.example.json --dry-run
```

Reads only the kit's non-secret JSON planning format. A fixed allowlist rejects unknown keys, including secret fields. It does not read real config, generate config files, or call deployment commands; there is no apply mode. Output names preservation items, confirmations, and recovery steps. Identical input produces an identical plan without changing input/user settings. An authorized operator deploys incrementally using the guide.

## validate_kit.py

```sh
python3 -B scripts/validate_kit.py
python3 -B scripts/validate_kit.py --public
python3 -B scripts/validate_kit.py --zip /absolute/path/dots-hermes-deployment-kit.zip
```

Checks manifest completeness/explicit filenames, symlinks, forbidden paths, Python AST, JSON, local Markdown links, and secret patterns. ZIP uses the same allowlist, rejects extra/missing/duplicate/out-of-bounds entries, and compares content with the kit byte for byte. Scanning helps but cannot identify every unknown secret format; the kit was created without reading secrets and includes newly created files only.

`--public` additionally rejects emails, personal home paths, private IPv4 addresses, non-example tailnet DNS, and UUIDs. Tree validation ignores root Git-managed `.git` metadata to support normal clones; ZIP always excludes it. Tracked content and commit history need separate full scanning before publication; this option does not review history.

## Tests

```sh
python3 -B -m unittest discover -s tests -v
```

Fixtures are newly created synthetic data. The original 27 tests use fake transport/in-memory responses. The 24 new tests use self-owned loopback mocks, isolated venvs, CLI/MCP subprocesses, and synthetic tokens. They never call real Hermes/read real credentials/dispatch to real services, and clean up their sockets/processes/temporary directories. Coverage includes URL rejection, TLS/redirect policy, response size/syntax, no body/token output, health names, loopback cards, auth rejection order, dry-run idempotence/input preservation/no writes/unchanged state on failure, packaging, links, and secret scanning. These tests are not the complete Hermes pytest suite.
