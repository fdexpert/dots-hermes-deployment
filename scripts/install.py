#!/usr/bin/env python3
"""Install this kit only in a fresh, explicit prefix. Default: plan, no writes."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import stat
import sys
import venv
from pathlib import Path

from diagnose import SafeParser

VERSION = "0.4.0"
MARKER = ".kit-install.json"
OWNER = "dots-hermes-kit-install-v1"
SOURCE_FILES = ("scripts/bridge.py", "scripts/diagnose.py", "examples/bridge-config.example.json")


class InstallError(Exception):
    pass


def platform_check():
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise InstallError("only_macos_arm64_supported")
    if not (3, 11) <= sys.version_info[:2] < (3, 15):
        raise InstallError("python_requires_3_11_through_3_14")


def prefix_check(prefix, source):
    if not prefix.is_absolute() or any(p.is_symlink() for p in [prefix, *prefix.parents]):
        raise InstallError("absolute_non_symlink_prefix_required")
    prefix, source = prefix.resolve(), source.resolve()
    if prefix in (Path("/"), Path.home(), source) or source.is_relative_to(prefix) or prefix.is_relative_to(source):
        raise InstallError("unsafe_prefix")
    if not prefix.parent.is_dir():
        raise InstallError("prefix_parent_must_exist")
    if prefix.exists():
        meta = prefix.stat()
        if not prefix.is_dir() or meta.st_uid != os.getuid() or meta.st_mode & 0o077:
            raise InstallError("prefix_must_be_private_and_owned")
    return prefix


def source_hashes(source):
    result = {}
    for name in SOURCE_FILES:
        path = source/name
        if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()) or not path.is_file():
            raise InstallError("unsafe_or_missing_kit_source")
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def inventory(prefix):
    result = {}
    for path in sorted(prefix.rglob("*")):
        name = path.relative_to(prefix).as_posix()
        if name == MARKER or name.split("/")[0] == "config":
            continue  # Never read, hash, overwrite, or remove user configuration.
        meta = path.lstat()
        if stat.S_ISLNK(meta.st_mode):
            result[name] = {"kind": "symlink", "target": os.readlink(path)}
        elif stat.S_ISDIR(meta.st_mode):
            result[name] = {"kind": "directory"}
        elif stat.S_ISREG(meta.st_mode):
            result[name] = {"kind": "file", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "mode": stat.S_IMODE(meta.st_mode)}
        else:
            raise InstallError("unsupported_installation_entry")
    return result


def marker_read(prefix):
    path = prefix/MARKER
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1_000_000:
        raise InstallError("unknown_prefix_refused")
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        raise InstallError("invalid_install_marker") from None
    if not isinstance(data, dict) or data.get("owner") != OWNER or data.get("phase") != "complete":
        raise InstallError("unknown_or_incomplete_prefix_refused")
    expected = data.get("managed")
    if not isinstance(expected, dict) or inventory(prefix) != expected:
        raise InstallError("modified_or_unknown_installation_entries")
    for name in expected:
        p = Path(name)
        if p.is_absolute() or ".." in p.parts or name == MARKER or p.parts[0] == "config":
            raise InstallError("unsafe_install_marker")
    return data


def marker_write(prefix, data, *, initial=False):
    mode = "x" if initial else "w"
    with (prefix/MARKER).open(mode) as stream:
        json.dump(data, stream, sort_keys=True)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(prefix/MARKER, 0o600)


def remove_managed(prefix, managed):
    for name, entry in sorted(managed.items(), key=lambda item: len(Path(item[0]).parts), reverse=True):
        path = prefix/name
        if entry["kind"] == "directory":
            path.rmdir()
        else:
            path.unlink()


def apply_install(prefix, source, *, builder=None, after_create=None):
    hashes = source_hashes(source)
    if prefix.exists():
        data = marker_read(prefix)
        if data.get("version") != VERSION or data.get("source_hashes") != hashes:
            raise InstallError("upgrade_requires_new_prefix")
        return {"ok": True, "action": "apply", "changed": False, "config_preserved": True}
    prefix.mkdir(mode=0o700)
    receipt = {"owner": OWNER, "phase": "installing", "version": VERSION, "source_hashes": hashes}
    marker_write(prefix, receipt, initial=True)
    rollback_snapshot = {}
    try:
        (prefix/"app").mkdir(mode=0o700)
        (prefix/"config").mkdir(mode=0o700)
        for name in ("bridge.py", "diagnose.py"):
            shutil.copyfile(source/"scripts"/name, prefix/"app"/name)
            os.chmod(prefix/"app"/name, 0o600)
        shutil.copyfile(source/"examples"/"bridge-config.example.json", prefix/"config"/"bridge-config.json")
        os.chmod(prefix/"config"/"bridge-config.json", 0o600)
        rollback_snapshot = inventory(prefix)
        (builder or venv.EnvBuilder(with_pip=False, symlinks=True)).create(prefix/"venv")
        rollback_snapshot = inventory(prefix)
        if after_create:
            after_create(prefix)
        receipt.update(phase="complete", managed=inventory(prefix))
        marker_write(prefix, receipt)
        return {"ok": True, "action": "apply", "changed": True, "venv_created": True,
                "dependencies": "stdlib_only_no_pip", "config_created_without_secrets": True,
                "services_changed": False, "mcp_registered": False}
    except BaseException:
        # Only rollback our newly created app and venv. Preserve config and any
        # unrelated top-level entry; never recursively delete the whole prefix.
        if inventory(prefix) == rollback_snapshot:
            remove_managed(prefix, rollback_snapshot)
            (prefix/MARKER).unlink(missing_ok=True)
        # Partial/changed venv or unknown files remain for manual inspection.
        # An incomplete marker is refused on subsequent apply/uninstall.
        raise InstallError("installation_failed_private_prefix_preserved") from None


def uninstall(prefix):
    data = marker_read(prefix)
    remove_managed(prefix, data["managed"])
    (prefix/MARKER).unlink()
    # config survives even if it is unchanged. The prefix is intentionally kept.
    return {"ok": True, "action": "uninstall", "managed_files_removed": True,
            "config_preserved": True, "prefix_preserved": True, "services_changed": False}


def install(source, prefix, *, action="plan", apply=False, **testing):
    platform_check()
    prefix = prefix_check(prefix, source)
    hashes = source_hashes(source)
    if action == "uninstall":
        marker_read(prefix)  # Detect modifications before any removal.
    elif prefix.exists():
        data = marker_read(prefix)
        if data.get("version") != VERSION or data.get("source_hashes") != hashes:
            raise InstallError("upgrade_requires_new_prefix")
    if not apply:
        return {"ok": True, "action": action, "mode": "dry-run", "will_write": False,
                "platform": "macos_arm64", "python_supported": True, "dependencies": "stdlib_only_no_pip",
                "operations": ["preserve_user_config", "remove_only_verified_managed_entries"] if action == "uninstall" else
                              ["create_private_prefix_if_absent", "copy_two_kit_scripts", "create_isolated_venv",
                               "create_secret_free_config_only_if_new", "record_owned_files"],
                "services_changed": False, "credentials_read": False, "mcp_registered": False}
    return uninstall(prefix) if action == "uninstall" else apply_install(prefix, source, **testing)


def main(argv=None):
    parser = SafeParser(description=__doc__)
    parser.add_argument("--prefix", required=True, type=Path)
    parser.add_argument("--action", choices=("plan", "install", "uninstall"), default="plan")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.apply and args.action == "plan":
            raise InstallError("apply_requires_install_or_uninstall_action")
        result = install(Path(__file__).resolve().parent.parent, args.prefix, action=args.action, apply=args.apply)
    except InstallError as exc:
        result = {"ok": False, "error": str(exc), "no_services_changed": True}
    except (OSError, ValueError, KeyboardInterrupt):
        result = {"ok": False, "error": "installation_io_or_interrupted", "no_services_changed": True}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
