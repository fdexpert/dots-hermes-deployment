# Public-release audit

[繁體中文](PUBLICATION_AUDIT.md) | **English**

Kit 0.4.0 | 2026-10-06 UTC

The public edition removes original host names, caller/target identities, service labels, and identifying parts of local execution markers. Historical evidence retains only architecture roles, dates, platform versions, HTTP status, HERMES_OK, duration, and tool-call counts. The actual reserved server identity is not published. Check it in compatible source; do not rename a security constant based on examples.

Before publication, all manifest files/ZIP are scanned for credential formats, real .env/registry, emails, non-example personal home paths, private IPv4/tailnet DNS, UUID/thread identifiers, backups/logs, symlinks, and extra files. Loopback addresses, instructions forbidding 0.0.0.0, official URLs, and clear example locations may remain. No internal conversations, memory, or hidden assistant rules are included; AGENTS is public project deployment policy. All new English files undergo the same scans.

Initial publication began with empty Git history and a scanned initial commit, using GitHub noreply author/committer identity rather than a private email. Version 0.2.0 was separately authorized, published publicly, and checked remotely. Changes accumulated from the preceding 0.3 source; uncommitted differences, new documents, and all publishable commit content/metadata are checked before this publication; ZIP excludes .git. If the remote acquires other content, inspect everything that will become public, including history. Scanning this kit does not authorize exposing an unrelated repository. Stop publication if the designated account lacks valid authentication.

See [delivery validation](DELIVERY_VALIDATION.en.md) for offline tests, language checks, and public scanning, and [NOTICE](NOTICE.en.md) for third-party/licensing boundaries. Release results are confirmed against actual remote visibility/commit/file list after push.

Version 0.4.0 includes new bridge/isolated installer and bilingual sanitized evidence of the real B task. The user explicitly requested updating the existing public repo using fdexpert/main; remote changes, full content/history, and ZIP are checked before normal commit/push. Prior release was 0.3.0; no force push, unrelated content, or deployment hook. Tests use synthetic tokens/self-owned mocks/temporary prefixes only. No actual config, token file, state receipts, venv, or test directories are packaged.

Later real B-task evidence retains sanitized summaries only. Actual caller/task/context/session IDs, token files, installed prefixes, receipts, and private case records are excluded from the public ZIP. Private Library attachments and GitHub source are separate deliveries; publication is checked against the exact remote commit.
