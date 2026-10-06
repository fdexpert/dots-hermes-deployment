# Backup, recovery, and downtime risks

[繁體中文](OPERATIONS.md) | **English**

The kit is a shareable secret-free project, **not a complete backup for restoring an existing machine**. The user separately stores server secrets, client registry, model access, tailnet login, and app pairing in controlled encrypted storage. No such backup was read or created while making this kit.

## Before deployment

Locally record source version/installation owner, profile/data home, original config permissions, service owner, and Serve ports/paths. The user backs up files/credentials that will change; keep these outside the kit and external repositories. Do not package all of `~/.hermes` as a deployment kit: it contains conversations, model secrets, databases, and logs.

## Change window

Gateway start/stop/restart affects every platform on that gateway. Waiting A2A tasks may fail or have unknown results; do not replay automatically after startup. Closing the app or sleeping the Mac makes the Dots executor unavailable. Turning Serve off disconnects new A connections, without necessarily stopping B's local gateway. The kit describes risks and does not perform shutdown.

## Recovery on failure

1. Pause new task dispatch, mark incomplete/unknown outcomes, and prevent duplicate submissions.
2. Compare the change record locally and restore only the non-secret fields and original permissions changed in this deployment. The user handles secrets; the public kit cannot recover old tokens.
3. If only A's Serve entry was newly added and no other user shares its port/path, disable that entry with its original flags. For the guide's --bg/HTTPS-port configuration:

   ```sh
   tailscale serve --bg --https=10000 off
   ```

   Check current CLI `off` syntax and original flags first. Never run global `serve reset`. If this entry existed before, restore its original configuration instead of turning it off.
4. If gateway restart is required, recheck the downtime window/official supervisor and use the original installation owner's method. Do not start another dispatcher or force replacement.
5. Repeat configuration/process/HTTP + authentication acceptance. Actual task acceptance needs separate approval for one message. Resolve unknown old tasks manually before deciding to restart work.

When restoring clean source, preserve local_readonly restrictions and other platforms. Do not overwrite entire security files or blindly use `git reset --hard`. Machine migration means new deployment and renewed authorization, not copying existing tasks and every secret.
