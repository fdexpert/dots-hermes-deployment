#!/usr/bin/env python3
"""Validate only this newly created kit and its allowlisted archive."""
from __future__ import annotations

import argparse
import ast
import json
import ipaddress
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|tskey-[A-Za-z0-9_-]{20,})\b"),
    re.compile(r"https?://[^\s/@]+:[^\s/@]+@"),
)
BLOCKED_PARTS = {".git", ".venv", "__pycache__", "backups", "logs", "secrets", "local", "node_modules"}
BLOCKED_NAMES = {".env", "agents.yaml", "registry.yaml", "registry.json", ".DS_Store"}
BLOCKED_SUFFIXES = {".log", ".jsonl", ".db", ".pem", ".key", ".pyc", ".zip", ".sqlite"}


def public_content_issues(text: str) -> list[str]:
    errors = []
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        errors.append("email_address")
    personal_prefix = "/" + "Users/"
    if re.search(re.escape(personal_prefix) + r"(?!example(?:/|\b))[^/\s\"']+", text):
        errors.append("personal_home_path")
    for raw in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text):
        try:
            address = ipaddress.ip_address(raw)
        except ValueError:
            continue
        if not address.is_loopback and not address.is_unspecified and (address.is_private or address in ipaddress.ip_network("100" + ".64.0.0/10")):
            errors.append("private_network_address")
    for hostname in re.findall(r"[A-Za-z0-9.-]+\.ts\.net\b", text):
        if "example" not in hostname.lower():
            errors.append("non_example_tailnet_hostname")
    if re.search(r"\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b", text, re.I):
        errors.append("identifier_uuid")
    return sorted(set(errors))


def safe_relative(name: str) -> bool:
    p = PurePosixPath(name)
    return (bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name
            and p.as_posix() == name and not any(part in BLOCKED_PARTS for part in p.parts)
            and p.name not in BLOCKED_NAMES and not p.name.startswith(".env.")
            and p.suffix not in BLOCKED_SUFFIXES)


def content_issues(name: str, text: str) -> list[str]:
    errors = []
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        errors.append("secret_pattern")
    if name.endswith((".txt", ".yaml")):
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                continue
            m = re.match(r"\s*(A2A_(?:PEER_TOKENS|BEARER_TOKEN|PUSH_SECRET)|token)\s*[:=]\s*(.+)", line)
            if m and "REPLACE_" not in m.group(2):
                errors.append("non_placeholder_credential")
    if name.endswith(".json"):
        try:
            data = json.loads(text)
        except ValueError:
            errors.append("invalid_json")
        else:
            def walk(value):
                if isinstance(value, dict):
                    for key, v in value.items():
                        if key.lower() in {"token", "password", "secret", "private_key", "api_key"}:
                            if not isinstance(v, str) or not v.startswith("REPLACE_"):
                                errors.append("non_placeholder_credential")
                        walk(v)
                elif isinstance(value, list):
                    for v in value:
                        walk(v)
            walk(data)
    if name.endswith(".py"):
        try:
            ast.parse(text, filename=name)
        except SyntaxError:
            errors.append("invalid_python")
    return sorted(set(errors))


def markdown_links(root: Path, name: str, text: str) -> list[str]:
    errors = []
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        target = target.split("#", 1)[0]
        resolved = (root / name).parent.joinpath(target).resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
            errors.append("broken_or_external_local_link")
    return sorted(set(errors))


def validate_tree(root: Path, *, public: bool = False) -> tuple[list[str], list[str]]:
    errors = []
    try:
        manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        names = manifest["files"]
        if not isinstance(names, list) or any(not isinstance(n, str) for n in names):
            return ["invalid_manifest"], []
    except (OSError, ValueError, KeyError):
        return ["invalid_manifest"], []
    if len(set(names)) != len(names) or any(not safe_relative(n) for n in names):
        return ["unsafe_manifest"], []
    actual = {str(p.relative_to(root)) for p in root.rglob("*")
              if (p.is_file() or p.is_symlink()) and p.relative_to(root).parts[0] != ".git"}
    if actual != set(names):
        errors.append("file_set_mismatch")
    for name in names:
        p = root / name
        if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()):
            errors.append(name + ":symlink_or_escape")
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(name + ":unreadable_or_nontext")
            continue
        errors.extend(name + ":" + error for error in content_issues(name, text))
        if public:
            errors.extend(name + ":" + error for error in public_content_issues(text))
        if name.endswith(".md"):
            errors.extend(name + ":" + error for error in markdown_links(root, name, text))
    return errors, names


def validate_archive(path: Path, root: Path, names: list[str]) -> list[str]:
    errors = []
    prefix = root.name + "/"
    expected = {prefix + name for name in names}
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            actual = [i.filename for i in infos]
            if len(actual) != len(set(actual)) or set(actual) != expected:
                errors.append("zip_file_set_mismatch")
            for item in infos:
                if not item.filename.startswith(prefix) or not safe_relative(item.filename[len(prefix):]):
                    errors.append("zip_unsafe_entry")
                    continue
                if item.filename not in expected:
                    continue
                if (item.external_attr >> 16) & 0o170000 == 0o120000:
                    errors.append("zip_symlink")
                    continue
                if item.file_size > 2_000_000:
                    errors.append("zip_oversized_entry")
                    continue
                raw = archive.read(item)
                name = item.filename[len(prefix):]
                if raw != (root / name).read_bytes():
                    errors.append("zip_content_mismatch:" + name)
                try:
                    errors.extend(name + ":" + e for e in content_issues(name, raw.decode("utf-8")))
                except UnicodeError:
                    errors.append("zip_nontext_entry")
    except (OSError, zipfile.BadZipFile):
        errors.append("invalid_zip")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--public", action="store_true", help="Also reject personal identifiers and private network locations")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    errors, names = validate_tree(root, public=args.public)
    if args.zip and not errors:
        errors.extend(validate_archive(args.zip, root, names))
    print(json.dumps({"ok": not errors, "files": len(names), "errors": sorted(set(errors)),
                      "zip_checked": args.zip is not None, "public_scan": args.public}, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
