# Deployment checklist

[繁體中文](DEPLOYMENT_CHECKLIST.md) | **English**

Date: ______ Operator: ______ Anonymous new-host label: ______ Path: A / B Kit version: ______

- [ ] Named host authorized and correct environment; dot login alone is not deployment approval.
- [ ] OS/architecture/app/Hermes runtime owner/versions/Tailscale version recorded.
- [ ] Compatible, conflict-free source; local-readonly customization and fixed identity restriction checked.
- [ ] Non-secret parameters complete; every example/REPLACE_ replaced in the deployment copy.
- [ ] Dry-run plan reviewed; existing working routes/other platforms preserved; downtime/recovery planned.
- [ ] Required service/security/route changes within authorization; outstanding approvals obtained.
- [ ] User personally configured new peer tokens/model/tailnet/app access; secrets outside kit/repository.
- [ ] Named caller matches trust; allow-all false; no environment trust override; reserved identity has a distinct token.
- [ ] Port 9900 loopback-only with one correct gateway; no forced second dispatcher.
- [ ] A: tailnet-only Serve HTTPS 10000→loopback 9900, minimum ACL, no Funnel, other entries untouched.
- [ ] A: full bridge/lockfile/loader/tools-list schema obtained and checked; incomplete if source is missing.
- [ ] B: new direct Dots task runs on target; target awake, network and app available.
- [ ] Configuration-layer acceptance passed.
- [ ] Process-layer acceptance passed.
- [ ] HTTP/card/TLS and authentication-layer acceptance passed; GET 200 not treated as authentication proof; card loopback handled.
- [ ] Separately authorized, one exact HERMES_OK message passed with zero tool calls; no unknown-result resend.
- [ ] B: evidence of local Hermes task and independence without intermediary participation; otherwise still unverified.
- [ ] Redacted results/changes/recovery plan saved; user keeps secret backups separately.
- [ ] If publishing GitHub: owner/repository/visibility authorized; all content and publishable history sanitized/scanned; safe kit files only; no automatic deployment trigger.

Incomplete items / blockers: ______ Next step and owner: ______
