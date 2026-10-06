# Public-release audit

[繁體中文](PUBLICATION_AUDIT.md) | **English**

Kit 0.3.0 | 2026-10-06 UTC

The public edition removes original host names, caller/target identities, service labels, and identifying parts of local execution markers. Historical evidence retains only architecture roles, dates, platform versions, HTTP status, HERMES_OK, duration, and tool-call counts. The actual reserved server identity is not published. Check it in compatible source; do not rename a security constant based on examples.

Before publication, all manifest files/ZIP are scanned for credential formats, real .env/registry, emails, non-example personal home paths, private IPv4/tailnet DNS, UUID/thread identifiers, backups/logs, symlinks, and extra files. Loopback addresses, instructions forbidding 0.0.0.0, official URLs, and clear example locations may remain. No internal conversations, memory, or hidden assistant rules are included; AGENTS is public project deployment policy. All new English files undergo the same scans.

Initial publication began with empty Git history and a scanned initial commit, using GitHub noreply author/committer identity rather than a private email. Version 0.2.0 was separately authorized, published publicly, and checked remotely. Before this edition, the worktree was clean. New documents and all publishable commit content/metadata are checked again; ZIP excludes .git. If the remote acquires other content, inspect everything that will become public, including history. Scanning this kit does not authorize exposing an unrelated repository. Stop publication if the designated account lacks valid authentication.

See [delivery validation](DELIVERY_VALIDATION.en.md) for offline tests, language checks, and public scanning, and [NOTICE](NOTICE.en.md) for third-party/licensing boundaries. Release results are confirmed against actual remote visibility/commit/file list after push.
