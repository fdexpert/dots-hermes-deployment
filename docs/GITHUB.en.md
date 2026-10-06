# GitHub and future dot entry point

[繁體中文](GITHUB.md) | **English**

The project can be stored on GitHub so a dot can obtain its steps and tools. Logging into a dot does not start deployment. A new host still needs an appropriate connected Mac executor, authorization for file/service operations, compatible-version inventory, and credentials configured personally by the user. Start with [AGENTS](../AGENTS.en.md) and [README](../README.en.md).

Before initial publication, confirm GitHub owner/login, repository name, and visibility with the user. An email does not identify a GitHub account; verify login through normal authentication with a read-only call. Do not claim an email match if it is hidden. The ZIP contains no personal GitHub login details, configured git remote, or existing git settings. Version 0.2.0 was separately authorized and published publicly; see [verified records](VERIFIED_RECORD.en.md).

## Suggested request for a future dot

```text
Prepare deployment using this repository's Dots × Hermes kit on my specified,
connected, authorized Mac.
Read AGENTS.md first. Confirm A or B, actual host, and parameters; run read-only
preflight and offline tests.
Provide an incremental change plan, dry-run, credential handoff, downtime,
and recovery steps first.
For new services or security changes, obtain any confirmation required outside
the existing authorization before execution.
Do not copy old secrets or dispatch tasks automatically. List the source gap
if the complete bridge has not been obtained.
```

## Manual publication checks

- Review git diff and every file to be staged; do not git-add the entire task workspace.
- Use only safe `dots-hermes-deployment-kit` content as repository root. Keep real secrets/deployment copies outside it.
- Run offline tests, internal link/syntax/content checks, and ZIP scanning. Verify source/version documentation.
- Create/commit/push only after confirming the target account, repository, and authorized visibility. Before public release, scan all content and publishable history. Stop if an existing repository has unrelated content or unresolved sensitive material.
- Do not set up GitHub Actions deployment or add repository secrets/PATs, SSH keys, or tailnet keys.

A repository is not a secret vault. The dry-run planner outputs a plan only; it does not execute, read, or rewrite actual user configuration. [Deployment guide](DEPLOYMENT.en.md)
