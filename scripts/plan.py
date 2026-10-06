#!/usr/bin/env python3
"""Print an immutable, non-secret deployment plan. There is no apply mode."""
from __future__ import annotations

import argparse
import copy
import json
import re
import ipaddress
import urllib.parse
from pathlib import Path

from diagnose import DiagnosticError, SafeParser, validate_base_url

FIELDS = {"architecture", "caller_id", "target_alias", "target_identity", "reserved_local_identity", "base_url",
          "listen_host", "a2a_port", "serve_https_port", "hermes_data_home", "hermes_source",
          "bridge_path", "registry_path"}
REQUIRED = {"architecture", "caller_id", "target_alias", "target_identity", "reserved_local_identity", "base_url", "listen_host", "a2a_port"}


def build_plan(config: dict) -> dict:
    if not isinstance(config, dict) or set(config) - FIELDS or not REQUIRED <= set(config):
        raise DiagnosticError("invalid_non_secret_plan_schema")
    if config["architecture"] not in ("A", "B") or config["listen_host"] != "127.0.0.1":
        raise DiagnosticError("unsupported_architecture_or_bind")
    for field in ("caller_id", "target_alias", "target_identity", "reserved_local_identity"):
        if not isinstance(config[field], str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", config[field]):
            raise DiagnosticError("invalid_identity")
    if config["caller_id"].casefold() == config["reserved_local_identity"].casefold():
        raise DiagnosticError("reserved_caller_identity")
    validate_base_url(config["base_url"])
    for field in ("a2a_port", "serve_https_port"):
        if field in config and (type(config[field]) is not int or not 1 <= config[field] <= 65535):
            raise DiagnosticError("invalid_port")
    if config["architecture"] == "A" and "serve_https_port" not in config:
        raise DiagnosticError("missing_serve_port")
    endpoint = urllib.parse.urlsplit(config["base_url"])
    endpoint_port = endpoint.port or (443 if endpoint.scheme == "https" else 80)
    if config["architecture"] == "A":
        if endpoint.scheme != "https" or not (endpoint.hostname or "").endswith(".ts.net") or endpoint_port != config["serve_https_port"]:
            raise DiagnosticError("a_route_endpoint_mismatch")
    else:
        try:
            local = ipaddress.ip_address(endpoint.hostname or "").is_loopback
        except ValueError:
            local = False
        if not local or endpoint.scheme != "http" or endpoint_port != config["a2a_port"]:
            raise DiagnosticError("b_route_endpoint_mismatch")
    # Paths are accepted only as non-secret planning metadata; never read or execute them.
    for field in FIELDS - REQUIRED - {"serve_https_port"}:
        if field in config and (not isinstance(config[field], str) or not config[field].startswith("/")
                                or any(ord(c) < 32 for c in config[field])):
            raise DiagnosticError("invalid_planning_path")
    steps = ["verify_connected_host_and_authorization", "read_only_preflight_and_offline_tests",
             "inventory_existing_routes_and_prepare_incremental_diff", "user_private_credential_handoff",
             "confirm_service_security_changes_and_downtime", "operator_apply_reviewed_incremental_settings"]
    steps += (["operator_add_tailnet_only_serve_if_needed", "obtain_and_validate_original_stdio_bridge"]
              if config["architecture"] == "A" else ["verify_direct_dots_target_executor_and_local_client"])
    steps += ["validate_config_process_http_and_auth", "separate_authorization_for_one_HERMES_OK",
              "record_redacted_result_and_rollback_owner"]
    return {"mode": "dry-run-only", "will_execute": False, "will_write": False,
            "requested": copy.deepcopy(config), "steps": steps,
            "preserve": ["other_user_settings", "existing_peers_and_reserved_identity",
                         "other_platforms", "existing_serve_and_funnel_routes"],
            "rollback": "operator_restore_only_reviewed_changes_after_stopping_new_tasks",
            "source_gap": "original_bridge_not_in_kit"}


def main(argv=None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True,
                        help="Only the non-secret deployment-plan JSON, never real config or registry")
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        if args.spec.suffix != ".json" or "deployment-plan" not in args.spec.name:
            raise DiagnosticError("planning_file_name_required")
        with args.spec.open("rb") as handle:
            raw = handle.read(32769)
        if len(raw) > 32768:
            raise DiagnosticError("planning_file_too_large")
        config = json.loads(raw)
        result = build_plan(config)
    except (OSError, UnicodeError, ValueError):
        result = {"ok": False, "error": "invalid_planning_file"}
    except DiagnosticError as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result.get("ok") is False else 0


if __name__ == "__main__":
    raise SystemExit(main())
