#!/usr/bin/env python3
"""Bounded diagnostics. Never send an agent task or print arbitrary remote data."""
from __future__ import annotations

import argparse
import ast
import getpass
import ipaddress
import json
import platform
import shutil
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import warnings
from pathlib import Path

MAX_BODY = 65536
PROBE_ID = "deployment-kit-auth-probe"
PROBE_METHOD = "DeploymentKitAuthProbe"
A2A_FILES = ("__init__.py", "security.py", "adapter.py", "protocol.py", "local_readonly.py")


class DiagnosticError(Exception):
    pass


def validate_base_url(value: str) -> str:
    """Only literal loopback HTTP(S), or HTTPS at a tailnet DNS name."""
    if not isinstance(value, str) or not value or any(ord(c) < 33 or ord(c) > 126 for c in value):
        raise DiagnosticError("unsafe_url")
    if any(c in value for c in ("%", "\\", "?", "#", "@")):
        raise DiagnosticError("unsafe_url")
    try:
        parsed = urllib.parse.urlsplit(value)
        host, port = parsed.hostname or "", parsed.port
    except ValueError:
        raise DiagnosticError("unsafe_url") from None
    if parsed.username is not None or parsed.password is not None or parsed.path not in ("", "/"):
        raise DiagnosticError("unsafe_url")
    if parsed.query or parsed.fragment or parsed.scheme not in ("http", "https"):
        raise DiagnosticError("unsafe_url")
    try:
        loopback = ipaddress.ip_address(host).is_loopback
    except ValueError:
        loopback = False
    tailnet = host.endswith(".ts.net") and all(c.isalnum() or c in "-." for c in host)
    if not loopback and not (parsed.scheme == "https" and tailnet):
        raise DiagnosticError("remote_requires_tailnet_https")
    if port is not None and not 1 <= port <= 65535:
        raise DiagnosticError("unsafe_url")
    return value.rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(base: str, path: str, *, timeout: float = 10, token: str | None = None,
                 payload: dict | None = None) -> tuple[int, object]:
    base = validate_base_url(base)
    if path not in ("/health", "/.well-known/agent-card.json", "/"):
        raise DiagnosticError("unsupported_diagnostic_path")
    if not 0 < timeout <= 30:
        raise DiagnosticError("invalid_timeout")
    if payload is not None and (path != "/" or payload != auth_payload()):
        raise DiagnosticError("unsupported_diagnostic_payload")
    if token is not None and (not token or token != token.strip() or any(ord(c) < 33 or ord(c) > 126 for c in token)):
        raise DiagnosticError("invalid_private_credential")
    headers = {"Accept": "application/json"}
    if token is not None:
        headers["Authorization"] = "Bearer " + token
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base + path, data=data, headers=headers,
                                 method="POST" if data is not None else "GET")
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), NoRedirect(),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    try:
        try:
            response = opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            status = response.code
            if 300 <= status < 400:
                raise DiagnosticError("redirect_refused")
            content_type = response.headers.get_content_type()
            raw = response.read(MAX_BODY + 1)
    except DiagnosticError:
        raise
    except (urllib.error.URLError, OSError, ValueError):
        raise DiagnosticError("network_or_tls_error") from None
    if len(raw) > MAX_BODY:
        raise DiagnosticError("response_too_large")
    if content_type != "application/json":
        raise DiagnosticError("non_json_response")
    try:
        return status, json.loads(raw)
    except (ValueError, UnicodeError):
        raise DiagnosticError("invalid_json_response") from None


def health_summary(status: int, body: object, expected: str) -> dict:
    matched = isinstance(body, dict) and body.get("status") == "ok" and body.get("agent") == expected
    return {"check": "health", "http_status": status, "ok": status == 200 and matched,
            "expected_name_match": matched, "authentication_proven": False}


def card_summary(status: int, body: object, expected: str) -> dict:
    if not isinstance(body, dict):
        return {"check": "card", "http_status": status, "ok": False, "error": "invalid_card"}
    interfaces = body.get("supportedInterfaces")
    urls = [body.get("url")] if isinstance(body.get("url"), str) else []
    if isinstance(interfaces, list):
        urls += [i["url"] for i in interfaces if isinstance(i, dict) and isinstance(i.get("url"), str)]
    loopback, unsafe = False, False
    for url in urls:
        try:
            validate_base_url(url)
            host = urllib.parse.urlsplit(url).hostname or ""
            try:
                loopback = ipaddress.ip_address(host).is_loopback or loopback
            except ValueError:
                pass
        except DiagnosticError:
            unsafe = True
    scheme = body.get("securitySchemes")
    bearer = isinstance(scheme, dict) and any(
        isinstance(v, dict) and v.get("type") == "http" and isinstance(v.get("scheme"), str)
        and v["scheme"].lower() == "bearer"
        for v in scheme.values())
    compatible = isinstance(interfaces, list) and any(
        isinstance(i, dict) and i.get("protocolBinding") == "JSONRPC"
        and i.get("protocolVersion") in ("1.0", "1.0.0") for i in interfaces)
    matched = body.get("name") == expected
    return {"check": "card", "http_status": status,
            "ok": status == 200 and matched and compatible and bool(urls) and not unsafe,
            "expected_name_match": matched, "hermes_v1_interface": compatible,
            "bearer_advertised": bearer, "loopback_url_advertised": loopback,
            "registry_override_required_for_remote": loopback,
            "unsafe_or_non_root_card_url": unsafe, "authentication_proven": False}


def auth_payload() -> dict:
    return {"jsonrpc": "2.0", "id": PROBE_ID, "method": PROBE_METHOD, "params": {}}


def auth_summary(status: int, body: object) -> dict:
    expected = (status == 200 and isinstance(body, dict) and body.get("jsonrpc") == "2.0"
                and body.get("id") == PROBE_ID and isinstance(body.get("error"), dict)
                and body["error"].get("code") == -32601 and "result" not in body)
    return {"check": "auth", "http_status": status, "ok": expected,
            "hermes_auth_and_trust_contract_passed": expected, "task_sent": False}


def auth_probe(base: str, expected: str, timeout: float, *, fetch=request_json,
               read_token=None) -> dict:
    status, body = fetch(base, "/health", timeout=timeout)
    if not health_summary(status, body, expected)["ok"]:
        raise DiagnosticError("target_health_mismatch")
    status, body = fetch(base, "/", timeout=timeout, payload=auth_payload())
    if status not in (401, 403):
        raise DiagnosticError("unauthenticated_rpc_not_denied")
    token = (read_token or private_token_prompt)()
    try:
        status, body = fetch(base, "/", timeout=timeout, token=token, payload=auth_payload())
        return auth_summary(status, body)
    finally:
        # Drop the reference; Python cannot promise zeroisation of immutable strings.
        token = None


def private_token_prompt() -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        try:
            return getpass.getpass("Private caller token (hidden; never echoed): ")
        except (getpass.GetPassWarning, EOFError):
            raise DiagnosticError("private_prompt_unavailable") from None


def preflight(source: Path | None = None) -> dict:
    result = {"check": "preflight", "os": platform.system(), "arch": platform.machine(),
              "python": platform.python_version(), "python_supported": sys.version_info >= (3, 11),
              "commands_present": {n: bool(shutil.which(n)) for n in ("hermes", "tailscale", "git")},
              "service_state_checked": False, "secrets_read": False}
    if source is not None:
        files = {}
        for name in A2A_FILES:
            path = source / "plugins" / "platforms" / "a2a" / name
            try:
                if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()):
                    files[name] = "symlink_or_escape"
                    continue
                raw = path.read_text(encoding="utf-8")
                if any(line.startswith(("<<<<<<<", "=======", ">>>>>>>")) for line in raw.splitlines()):
                    files[name] = "conflict_markers"
                else:
                    ast.parse(raw, filename=name)
                    files[name] = "syntax_ok"
            except OSError:
                files[name] = "missing_or_unreadable"
            except (SyntaxError, UnicodeError):
                files[name] = "invalid_source"
        result["source_files"] = files
        result["source_syntax_ok"] = all(v == "syntax_ok" for v in files.values())
    result["ok"] = result["python_supported"] and result.get("source_syntax_ok", True)
    return result


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # Argument values could contain credentials. Never echo argparse's message.
        self.exit(2, "Invalid arguments; use --help. Values were not printed.\n")


def main(argv=None) -> int:
    parser = SafeParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True, parser_class=SafeParser)
    p = subs.add_parser("preflight")
    p.add_argument("--hermes-source", type=Path)
    for name in ("health", "card", "auth"):
        p = subs.add_parser(name)
        p.add_argument("--base-url", required=True)
        p.add_argument("--expected-name", required=True)
        p.add_argument("--timeout", type=float, default=10)
        if name == "auth":
            p.add_argument("--confirm-hermes-contract", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "preflight":
            result = preflight(args.hermes_source)
        else:
            base = validate_base_url(args.base_url)
            if not 0 < args.timeout <= 30:
                raise DiagnosticError("invalid_timeout")
            if args.command == "auth":
                if not args.confirm_hermes_contract:
                    raise DiagnosticError("hermes_contract_confirmation_required")
                result = auth_probe(base, args.expected_name, args.timeout)
            else:
                path = "/health" if args.command == "health" else "/.well-known/agent-card.json"
                status, body = request_json(base, path, timeout=args.timeout)
                summary = health_summary if args.command == "health" else card_summary
                result = summary(status, body, args.expected_name)
    except DiagnosticError as exc:
        result = {"ok": False, "error": str(exc)}
    except KeyboardInterrupt:
        result = {"ok": False, "error": "interrupted"}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
