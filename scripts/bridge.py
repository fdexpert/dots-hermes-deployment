#!/usr/bin/env python3
"""Original kit implementation: bounded Hermes A2A v1 CLI and stdio MCP."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import ssl
import stat
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from diagnose import (DiagnosticError, NoRedirect, SafeParser, card_summary,
                      health_summary, private_token_prompt, validate_base_url)

VERSION = "0.4.0"
LIMIT = 65536
CONTRACT = "hermes-a2a-v1-inspected"
STATES = {"TASK_STATE_" + s for s in
          ("SUBMITTED", "WORKING", "INPUT_REQUIRED", "AUTH_REQUIRED", "COMPLETED", "FAILED", "CANCELED", "REJECTED")}
TERMINAL = {"TASK_STATE_" + s for s in ("COMPLETED", "FAILED", "CANCELED", "REJECTED")}
VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26")


class BridgeError(Exception):
    def __init__(self, code, *, unknown=False):
        self.code, self.unknown = code, unknown
        super().__init__(code)


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", value):
        raise BridgeError("invalid_identifier")
    return value


def json_file(path):
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > LIMIT:
            raise BridgeError("unsafe_or_oversized_config")
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise BridgeError("invalid_config") from None


def load_config(path):
    data = json_file(path)
    if not isinstance(data, dict) or set(data) != {"schema_version", "caller_id", "targets"} or data["schema_version"] != 1:
        raise BridgeError("invalid_config_schema")
    identifier(data["caller_id"])
    targets = data["targets"]
    if not isinstance(targets, dict) or not 1 <= len(targets) <= 20:
        raise BridgeError("invalid_targets")
    for alias, target in targets.items():
        identifier(alias)
        if not isinstance(target, dict) or set(target) - {"base_url", "expected_name", "timeout_seconds", "token_file", "contract"}:
            raise BridgeError("unknown_target_field")
        if not {"base_url", "expected_name"} <= set(target):
            raise BridgeError("missing_target_field")
        try:
            validate_base_url(target["base_url"])
        except DiagnosticError:
            raise BridgeError("unsafe_base_url") from None
        identifier(target["expected_name"])
        timeout = target.get("timeout_seconds", 30)
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0.05 <= timeout <= 360:
            raise BridgeError("invalid_timeout")
        if "contract" in target and target["contract"] != CONTRACT:
            raise BridgeError("unsupported_contract")
        if "token_file" in target and (not isinstance(target["token_file"], str) or not Path(target["token_file"]).is_absolute()):
            raise BridgeError("token_path_must_be_absolute")
    return data


def outside_kit(path):
    root = Path(__file__).resolve().parent.parent
    if (root / "MANIFEST.json").exists() and path.resolve().is_relative_to(root):
        raise BridgeError("private_data_must_be_outside_kit")


def token_from_file(path):
    outside_kit(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            meta = os.fstat(stream.fileno())
            if not stat.S_ISREG(meta.st_mode) or meta.st_uid != os.getuid() or meta.st_mode & 0o077 or meta.st_size > 8192:
                raise BridgeError("unsafe_token_file")
            raw = stream.read(8193)
        return validate_token(raw.decode("ascii").strip())
    except (OSError, UnicodeError):
        raise BridgeError("token_file_unavailable") from None


def validate_token(token):
    if not isinstance(token, str) or not token or len(token) > 8192 or token.startswith(("Bearer ", "REPLACE_")) or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise BridgeError("invalid_raw_token")
    return token


def refuse_credential_echo(value, token, *, unknown=False):
    if isinstance(value, str) and token in value:
        raise BridgeError("credential_echo_refused", unknown=unknown)
    if isinstance(value, dict):
        for child in value.values():
            refuse_credential_echo(child, token, unknown=unknown)
    if isinstance(value, list):
        for child in value:
            refuse_credential_echo(child, token, unknown=unknown)


def transport(base, path, *, timeout, token=None, payload=None):
    """One request only: no retries, inherited proxy, redirects, or TLS bypass."""
    base = validate_base_url(base)
    if path not in ("/", "/health", "/.well-known/agent-card.json"):
        raise BridgeError("unsupported_path")
    headers = {"Accept": "application/json"}
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        if len(body) > LIMIT:
            raise BridgeError("request_too_large")
        headers.update({"Content-Type": "application/json", "A2A-Version": "1.0"})
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(base + path, data=body, headers=headers)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect(),
                                        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    try:
        try:
            response = opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            status = response.code
            if 300 <= status < 400:
                raise BridgeError("redirect_refused", unknown=payload is not None)
            raw = response.read(LIMIT + 1)
            if len(raw) > LIMIT:
                raise BridgeError("response_too_large", unknown=payload is not None)
            if response.headers.get_content_type() != "application/json":
                raise BridgeError("non_json_response", unknown=payload is not None)
        try:
            return status, json.loads(raw)
        except (ValueError, UnicodeError):
            raise BridgeError("invalid_json_response", unknown=payload is not None) from None
    except BridgeError:
        raise
    except (socket.timeout, TimeoutError):
        raise BridgeError("timeout", unknown=payload is not None) from None
    except urllib.error.URLError as exc:
        code = "timeout" if isinstance(exc.reason, (socket.timeout, TimeoutError)) else "network_or_tls_error"
        raise BridgeError(code, unknown=payload is not None) from None
    except (OSError, ValueError):
        raise BridgeError("network_or_tls_error", unknown=payload is not None) from None


def receipt_directory(path):
    outside_kit(path)
    if not path.is_absolute() or any(p.is_symlink() for p in [path, *path.parents]):
        raise BridgeError("unsafe_state_directory")
    if not path.exists():
        path.mkdir(mode=0o700, parents=False)
    meta = path.stat()
    if not path.is_dir() or meta.st_uid != os.getuid() or meta.st_mode & 0o077:
        raise BridgeError("unsafe_state_directory")
    return path


def save_receipt(directory, record):
    # Unique append-only snapshots, no input/reply/token/response body on disk.
    path = directory / (record["request_id"] + "-" + uuid.uuid4().hex + ".json")
    raw = json.dumps(record, sort_keys=True).encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def task_summary(task):
    if not isinstance(task, dict) or not isinstance(task.get("status"), dict):
        raise BridgeError("invalid_task_response", unknown=True)
    task_id = identifier(task.get("id"))
    context = identifier(task.get("contextId"))
    state = task["status"].get("state")
    if state not in STATES:
        raise BridgeError("unsupported_task_state", unknown=True)
    return {"task_id": task_id, "context_id": context, "task_state": state,
            "terminal": state in TERMINAL}


def reply_text(task, token):
    chunks = []
    for artifact in task.get("artifacts", []):
        if isinstance(artifact, dict):
            chunks += [p["text"] for p in artifact.get("parts", []) if isinstance(p, dict) and isinstance(p.get("text"), str)]
    if not chunks:
        message = task.get("status", {}).get("message", {})
        if isinstance(message, dict):
            chunks = [p["text"] for p in message.get("parts", []) if isinstance(p, dict) and isinstance(p.get("text"), str)]
    text = "\n".join(chunks)[:16000].replace(token, "[REDACTED]")
    text = re.sub(r"\b(?:gh[pousr]_|github_pat_|sk-|tskey-)[A-Za-z0-9_-]{20,}", "[REDACTED]", text)
    return text  # Arbitrary unknown secrets cannot be reliably detected; opt-in only.


class Bridge:
    def __init__(self, config, *, state_dir=None, enable_send=False, enable_query=False, fetch=transport, prompt=False):
        self.config, self.state_dir = config, state_dir
        self.enable_send, self.enable_query, self.fetch, self.prompt = enable_send, enable_query, fetch, prompt

    def target(self, alias):
        try:
            return self.config["targets"][alias]
        except (KeyError, TypeError):
            raise BridgeError("unknown_target") from None

    def inspect(self, alias, kind):
        target = self.target(alias)
        path = "/health" if kind == "health" else "/.well-known/agent-card.json"
        status, body = self.fetch(target["base_url"], path, timeout=min(target.get("timeout_seconds", 30), 30))
        summary = health_summary if kind == "health" else card_summary
        result = summary(status, body, target["expected_name"])
        result.update({"send_enabled": self.enable_send, "query_enabled": self.enable_query,
                       "client_contract": CONTRACT, "endpoint_pinned_to_config": True})
        return result

    def credential(self, target):
        if target.get("token_file"):
            return token_from_file(Path(target["token_file"]))
        if self.prompt:
            try:
                token = private_token_prompt()
            except DiagnosticError:
                raise BridgeError("private_prompt_unavailable") from None
            return validate_token(token)
        raise BridgeError("credential_required")

    def rpc(self, alias, method, params, *, confirm=False, include_reply=False):
        send = method == "SendMessage"
        if method not in ("SendMessage", "GetTask", "ListTasks"):
            raise BridgeError("unsupported_method")
        if (send and (not self.enable_send or confirm is not True)) or (not send and not self.enable_query):
            raise BridgeError("explicit_operation_authorization_required")
        target = self.target(alias)
        if target.get("contract") != CONTRACT:
            raise BridgeError("contract_confirmation_required")
        card = self.inspect(alias, "card")
        if not self.inspect(alias, "health")["ok"] or not card["ok"] or not card.get("bearer_advertised"):
            raise BridgeError("target_identity_or_contract_mismatch")
        token = self.credential(target)
        request_id = "req_" + uuid.uuid4().hex
        record = {"schema_version": 1, "request_id": request_id, "target_alias": alias,
                  "caller_label": self.config["caller_id"], "method": method, "outcome": "prepared"}
        directory = receipt_directory(self.state_dir) if self.state_dir else None
        if send and directory is None:
            raise BridgeError("state_directory_required_for_send")
        record.update({"context_id": params["message"]["contextId"], "message_id": params["message"]["messageId"]} if send else
                      ({"task_id": params["id"]} if method == "GetTask" else {"context_id": params["contextId"]}))
        refuse_credential_echo(record, token)  # Never persist a credential disguised as an ID/label.
        if directory:
            save_receipt(directory, record)  # Failure here prevents network dispatch.
        started = time.monotonic()
        post_started = False
        try:
            post_started = True
            status, body = self.fetch(target["base_url"], "/", timeout=target.get("timeout_seconds", 30), token=token,
                                      payload={"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
            record["http_status"] = status
            if status != 200:
                code = {401: "unauthorized", 403: "forbidden", 429: "rate_limited"}.get(status, "http_error")
                raise BridgeError(code, unknown=send and status not in (401, 403, 429))
            if not isinstance(body, dict) or body.get("jsonrpc") != "2.0" or body.get("id") != request_id:
                raise BridgeError("rpc_response_mismatch", unknown=send)
            if "error" in body:
                error = body["error"]
                code = error.get("code") if isinstance(error, dict) else None
                label = {-32601: "method_not_supported", -32001: "task_not_found",
                         -32050: "unauthorized", -32051: "rate_limited", -32052: "forbidden"}.get(code, "rpc_error")
                raise BridgeError(label, unknown=send and label == "rpc_error")
            result = body.get("result")
            if method == "ListTasks":
                if not isinstance(result, dict) or not isinstance(result.get("tasks"), list):
                    raise BridgeError("invalid_list_response")
                tasks = [task_summary(t) for t in result["tasks"][:20]]
                if any(t["context_id"] != params["contextId"] for t in tasks):
                    raise BridgeError("context_mismatch")
                refuse_credential_echo(tasks, token)
                output = {"ok": True, "tasks": tasks, "more_results": bool(result.get("nextPageToken")),
                          "retrieval_is_not_durable": True}
            else:
                task = result.get("task") if send and isinstance(result, dict) else result
                output = {"ok": True, **task_summary(task), "retrieval_is_not_durable": True}
                refuse_credential_echo(output, token, unknown=send)
                if send and output["context_id"] != params["message"]["contextId"]:
                    raise BridgeError("context_mismatch", unknown=True)
                if not send and output["task_id"] != params["id"]:
                    raise BridgeError("task_id_mismatch")
                record.update({k: output[k] for k in ("task_id", "context_id", "task_state")})
                if include_reply:
                    output["reply"] = reply_text(task, token)
            record["outcome"] = "response_received"
        except (BridgeError, DiagnosticError) as exc:
            code = exc.code if isinstance(exc, BridgeError) else "network_or_tls_error"
            unknown = send and (getattr(exc, "unknown", False) or code in ("invalid_identifier",))
            record.update(outcome="unknown_do_not_resend" if unknown else "rejected_or_failed", error=code)
            output = {"ok": False, "error": code, "outcome_unknown": unknown, "do_not_resend": send}
        except KeyboardInterrupt:
            record.update(outcome="unknown_do_not_resend" if send and post_started else "interrupted", error="interrupted")
            output = {"ok": False, "error": "interrupted", "outcome_unknown": send, "do_not_resend": send}
        except (TypeError, KeyError, ValueError):
            record.update(outcome="unknown_do_not_resend" if send else "rejected_or_failed", error="invalid_response_shape")
            output = {"ok": False, "error": "invalid_response_shape", "outcome_unknown": send, "do_not_resend": send}
        finally:
            token = None
        record["elapsed_seconds"] = round(time.monotonic() - started, 3)
        if directory:
            try:
                save_receipt(directory, record)
            except OSError:
                output["receipt_write_failed"] = True
        output.update({"request_id": request_id, "context_id": record.get("context_id"),
                       "elapsed_seconds": record["elapsed_seconds"], "automatic_retry": False})
        return output

    def send(self, alias, text, *, confirm=False, include_reply=False):
        if not isinstance(text, str) or not text.strip() or len(text.encode()) > 16000:
            raise BridgeError("invalid_message")
        context_id = "ctx_" + uuid.uuid4().hex
        params = {"message": {"role": "ROLE_USER", "messageId": "msg_" + uuid.uuid4().hex,
                              "contextId": context_id, "parts": [{"text": text, "mediaType": "text/plain"}]},
                  "configuration": {"returnImmediately": False}}
        return self.rpc(alias, "SendMessage", params, confirm=confirm, include_reply=include_reply)


def tools(bridge):
    defs = []
    for name in ("fleet_health", "fleet_card", "fleet_get_task", "fleet_find_context", "fleet_send"):
        if name in ("fleet_get_task", "fleet_find_context") and not bridge.enable_query:
            continue
        if name == "fleet_send" and not bridge.enable_send:
            continue
        props = {"target": {"type": "string"}}
        required = ["target"]
        for key in (["task_id"] if name == "fleet_get_task" else ["context_id"] if name == "fleet_find_context" else
                    ["message", "confirm_send"] if name == "fleet_send" else []):
            props[key] = {"type": "boolean" if key == "confirm_send" else "string"}
            required.append(key)
        if name in ("fleet_send", "fleet_get_task"):
            props["include_reply"] = {"type": "boolean", "default": False}
        defs.append({"name": name, "description": "Hermes A2A v1 " + name + "; no automatic retries.",
                     "inputSchema": {"type": "object", "properties": props, "required": required, "additionalProperties": False},
                     "annotations": {"readOnlyHint": name != "fleet_send", "destructiveHint": name == "fleet_send",
                                     "idempotentHint": name != "fleet_send", "openWorldHint": True}})
    return defs


def call_tool(bridge, params):
    if not isinstance(params, dict) or set(params) - {"name", "arguments"}:
        raise BridgeError("invalid_tool_params")
    name, args = params.get("name"), params.get("arguments", {})
    definition = next((t for t in tools(bridge) if t["name"] == name), None)
    if not definition or not isinstance(args, dict):
        raise BridgeError("tool_unavailable")
    schema = definition["inputSchema"]
    if set(args) - set(schema["properties"]) or not set(schema["required"]) <= set(args):
        raise BridgeError("invalid_tool_arguments")
    for key, value in args.items():
        expected = bool if schema["properties"][key]["type"] == "boolean" else str
        if not isinstance(value, expected):
            raise BridgeError("invalid_tool_arguments")
    alias = args["target"]
    if name in ("fleet_health", "fleet_card"):
        return bridge.inspect(alias, name.removeprefix("fleet_"))
    if name == "fleet_send":
        return bridge.send(alias, args["message"], confirm=args["confirm_send"], include_reply=args.get("include_reply", False))
    method = "GetTask" if name == "fleet_get_task" else "ListTasks"
    query = {"id": identifier(args["task_id"]), "historyLength": 0} if method == "GetTask" else {
        "contextId": identifier(args["context_id"]), "pageSize": 20, "includeArtifacts": False}
    return bridge.rpc(alias, method, query, include_reply=args.get("include_reply", False))


def serve_mcp(bridge, inp=None, out=None):
    inp, out = inp or sys.stdin.buffer, out or sys.stdout
    initialized = ready = False
    while True:
        raw = inp.readline(LIMIT + 1)
        if not raw:
            return
        response_id = None
        try:
            if len(raw) > LIMIT:
                while raw and not raw.endswith(b"\n"):
                    raw = inp.readline(LIMIT + 1)
                raise BridgeError("message_too_large")
            msg = json.loads(raw)
            if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
                raise BridgeError("invalid_request")
            response_id = msg.get("id")
            method, params = msg.get("method"), msg.get("params", {})
            if "id" not in msg:
                if method == "notifications/initialized" and initialized:
                    ready = True
                continue
            if not isinstance(response_id, (int, str)) or isinstance(response_id, bool):
                raise BridgeError("invalid_request_id")
            if method == "initialize":
                if initialized or not isinstance(params, dict) or params.get("protocolVersion") not in VERSIONS:
                    raise BridgeError("unsupported_initialize")
                initialized = True
                result = {"protocolVersion": params["protocolVersion"], "serverInfo": {"name": "dots-hermes-kit-bridge", "version": VERSION},
                          "capabilities": {"tools": {"listChanged": False}}}
            elif method == "ping" and initialized:
                result = {}
            elif not ready:
                raise BridgeError("initialize_required")
            elif method == "tools/list":
                if params not in ({}, None):
                    raise BridgeError("pagination_not_supported")
                result = {"tools": tools(bridge)}
            elif method == "tools/call":
                try:
                    value = call_tool(bridge, params)
                except BridgeError as exc:
                    value = {"ok": False, "error": exc.code}
                except (DiagnosticError, OSError):
                    value = {"ok": False, "error": "tool_operation_failed"}
                result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}],
                          "isError": not value["ok"]}
            else:
                raise BridgeError("method_not_found")
            reply = {"jsonrpc": "2.0", "id": response_id, "result": result}
        except (BridgeError, ValueError, UnicodeError):
            reply = {"jsonrpc": "2.0", "id": response_id, "error": {"code": -32600, "message": "Invalid or unsupported request"}}
        try:
            out.write(json.dumps(reply, ensure_ascii=False) + "\n")
            out.flush()
        except (BrokenPipeError, ConnectionResetError):
            return  # RPC outcome was already recorded; never replay after client disconnect.


def main(argv=None):
    parser = SafeParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--state-dir", type=Path)
    subs = parser.add_subparsers(dest="command", required=True, parser_class=SafeParser)
    for kind in ("health", "card", "send", "get-task", "find-context", "mcp"):
        sub = subs.add_parser(kind)
        if kind != "mcp":
            sub.add_argument("--target", required=True)
        if kind in ("send", "get-task", "find-context"):
            sub.add_argument("--prompt-token", action="store_true")
        if kind in ("send", "get-task"):
            sub.add_argument("--show-reply", action="store_true")
        if kind == "send":
            sub.add_argument("--confirm-send", action="store_true")
            sub.add_argument("--message-file", required=True, type=Path)
        if kind == "get-task":
            sub.add_argument("--task-id", required=True)
        if kind == "find-context":
            sub.add_argument("--context-id", required=True)
        if kind == "mcp":
            sub.add_argument("--enable-send", action="store_true")
            sub.add_argument("--enable-query", action="store_true")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        bridge = Bridge(config, state_dir=args.state_dir, enable_send=args.command == "send" or getattr(args, "enable_send", False),
                        enable_query=args.command in ("get-task", "find-context") or getattr(args, "enable_query", False),
                        prompt=getattr(args, "prompt_token", False))
        if args.command == "mcp":
            serve_mcp(bridge)
            return 0
        if args.command in ("health", "card"):
            result = bridge.inspect(args.target, args.command)
        elif args.command == "send":
            if not args.confirm_send:
                raise BridgeError("confirm_send_required")
            if args.message_file.is_symlink() or not args.message_file.is_file() or args.message_file.stat().st_size > 16000:
                raise BridgeError("unsafe_message_file")
            result = bridge.send(args.target, args.message_file.read_text(), confirm=True, include_reply=args.show_reply)
        else:
            method = "GetTask" if args.command == "get-task" else "ListTasks"
            query = {"id": identifier(args.task_id), "historyLength": 0} if method == "GetTask" else {
                "contextId": identifier(args.context_id), "pageSize": 20, "includeArtifacts": False}
            result = bridge.rpc(args.target, method, query, include_reply=getattr(args, "show_reply", False))
    except (BridgeError, DiagnosticError) as exc:
        result = {"ok": False, "error": exc.code if isinstance(exc, BridgeError) else "diagnostic_failure"}
    except (OSError, ValueError, KeyboardInterrupt):
        result = {"ok": False, "error": "local_io_or_interrupted"}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
