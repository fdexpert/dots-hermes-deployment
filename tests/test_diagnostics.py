import contextlib
import copy
import io
import json
import ssl
import sys
import tempfile
import unittest
import urllib.error
from email.message import Message
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import diagnose as d

FIXTURES = Path(__file__).parent / "fixtures"
BASE = "https://example-hermes.example-tailnet.ts.net:10000"
NAME = "hermes-example-target"


class Response:
    def __init__(self, raw=b'{}', status=200, content_type="application/json"):
        self.raw, self.code = raw, status
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        self.limit = None

    def read(self, limit):
        self.limit = limit
        return self.raw[:limit]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class DiagnosticsTests(unittest.TestCase):
    def fixture(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_safe_urls(self):
        for url in [BASE, "http://127.0.0.1:9900", "http://[::1]:9900/"]:
            self.assertEqual(d.validate_base_url(url), url.rstrip("/"))

    def test_unsafe_urls_never_echo_value(self):
        for url in ["https://" + "user:PRIVATE_TEST_VALUE" + "@example.ts.net", BASE + "?token=PRIVATE_TEST_VALUE",
                    BASE + "#PRIVATE_TEST_VALUE", BASE + "/rpc", "http://example.ts.net", "https://example.com",
                    "http://localhost:9900", BASE + "%2f", BASE + "\\rpc", BASE + "/\n", "https://example.ts.net:99999"]:
            with self.subTest(url=url), self.assertRaises(d.DiagnosticError) as caught:
                d.validate_base_url(url)
            self.assertNotIn("PRIVATE_TEST_VALUE", str(caught.exception))

    def test_health_is_not_auth(self):
        summary = d.health_summary(200, self.fixture("health.example.json"), NAME)
        self.assertTrue(summary["ok"])
        self.assertFalse(summary["authentication_proven"])
        self.assertFalse(d.health_summary(200, self.fixture("health.example.json"), "wrong")["ok"])
        self.assertFalse(d.health_summary(403, {"error": "PRIVATE_TEST_VALUE"}, NAME)["ok"])

    def test_card_loopback_warning_and_redaction(self):
        card = self.fixture("card.example.json")
        card["description"] = "PRIVATE_TEST_VALUE"
        summary = d.card_summary(200, card, NAME)
        self.assertTrue(summary["ok"])
        self.assertTrue(summary["registry_override_required_for_remote"])
        self.assertNotIn("PRIVATE_TEST_VALUE", json.dumps(summary))

    def test_card_rejects_credential_url_and_incompatible_interface(self):
        card = self.fixture("card.example.json")
        card["url"] = BASE + "?credential=PRIVATE_TEST_VALUE"
        self.assertFalse(d.card_summary(200, card, NAME)["ok"])
        card = self.fixture("card.example.json")
        card["supportedInterfaces"][0]["protocolBinding"] = "OTHER"
        self.assertFalse(d.card_summary(200, card, NAME)["ok"])

    def test_transport_bounds_tls_no_proxy_and_no_redirect(self):
        response = Response(b'{"status":"ok"}')
        with patch.object(d.urllib.request, "build_opener") as builder:
            builder.return_value.open.return_value = response
            status, body = d.request_json(BASE, "/health")
            args = builder.call_args.args
            proxy = next(h for h in args if isinstance(h, d.urllib.request.ProxyHandler))
            tls = next(h for h in args if isinstance(h, d.urllib.request.HTTPSHandler))
            self.assertEqual(proxy.proxies, {})
            self.assertEqual(tls._context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(tls._context.check_hostname)
            self.assertTrue(any(isinstance(h, d.NoRedirect) for h in args))
            req = builder.return_value.open.call_args.args[0]
            self.assertEqual(req.get_method(), "GET")
            self.assertEqual(status, 200)
            self.assertEqual(body, {"status": "ok"})
            self.assertEqual(response.limit, d.MAX_BODY + 1)
        self.assertIsNone(d.NoRedirect().redirect_request(None, None, 302, "", {}, BASE))

    def test_redirect_large_body_bad_json_and_non_json_fail(self):
        for response in [Response(status=302), Response(b"x" * (d.MAX_BODY + 1)),
                         Response(b"PRIVATE_TEST_VALUE"), Response(b"PRIVATE_TEST_VALUE", content_type="text/html")]:
            with self.subTest(status=response.code), patch.object(d.urllib.request, "build_opener") as builder:
                builder.return_value.open.return_value = response
                with self.assertRaises(d.DiagnosticError) as caught:
                    d.request_json(BASE, "/health")
                self.assertNotIn("PRIVATE_TEST_VALUE", str(caught.exception))

    def test_arbitrary_payload_or_path_cannot_dispatch(self):
        with patch.object(d.urllib.request, "build_opener") as builder:
            for path, payload in [("/", {"method": "SendMessage"}), ("/local-readonly", None)]:
                with self.assertRaises(d.DiagnosticError):
                    d.request_json(BASE, path, payload=payload)
            builder.assert_not_called()

    def test_token_header_not_printed_or_placed_in_url(self):
        with patch.object(d.urllib.request, "build_opener") as builder:
            builder.return_value.open.return_value = Response()
            d.request_json(BASE, "/", token="PRIVATE_TEST_VALUE", payload=d.auth_payload())
            req = builder.return_value.open.call_args.args[0]
            self.assertEqual(req.get_header("Authorization"), "Bearer PRIVATE_TEST_VALUE")
            self.assertNotIn("PRIVATE_TEST_VALUE", req.full_url)
            self.assertEqual(json.loads(req.data), d.auth_payload())

    def test_auth_only_after_denial_and_no_task(self):
        calls = []
        def fetch(base, path, **kwargs):
            calls.append((path, kwargs))
            if path == "/health":
                return 200, self.fixture("health.example.json")
            if "token" not in kwargs:
                return 401, {"error": {"code": -32050}}
            return 200, {"jsonrpc": "2.0", "id": d.PROBE_ID, "error": {"code": -32601, "message": "PRIVATE_TEST_VALUE"}}
        result = d.auth_probe(BASE, NAME, 10, fetch=fetch, read_token=lambda: "PRIVATE_TEST_VALUE")
        self.assertTrue(result["ok"])
        self.assertFalse(result["task_sent"])
        self.assertNotIn("PRIVATE_TEST_VALUE", json.dumps(result))
        self.assertEqual([p for p, _ in calls], ["/health", "/", "/"])
        self.assertTrue(all(k.get("payload", d.auth_payload()) == d.auth_payload() for _, k in calls))

    def test_unauthenticated_open_or_wrong_target_never_requests_token(self):
        for case in ("open", "wrong"):
            def fetch(base, path, **kwargs):
                if path == "/health":
                    body = self.fixture("health.example.json")
                    if case == "wrong":
                        body["agent"] = "wrong"
                    return 200, body
                return 200, {}
            with patch.object(d, "private_token_prompt") as prompt, self.assertRaises(d.DiagnosticError):
                d.auth_probe(BASE, NAME, 10, fetch=fetch)
            prompt.assert_not_called()

    def test_auth_result_rejects_success_payload_wrong_id_or_untrusted(self):
        for status, body in [(403, {"error": {"code": -32052}}), (200, {"result": "HERMES_OK"}),
                             (200, {"jsonrpc": "2.0", "id": "other", "error": {"code": -32601}})]:
            self.assertFalse(d.auth_summary(status, body)["ok"])

    def test_preflight_only_fixed_sources_no_config_import(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            directory = source / "plugins/platforms/a2a"
            directory.mkdir(parents=True)
            for name in d.A2A_FILES:
                (directory / name).write_text("raise RuntimeError('must not be imported')\n")
            (source / ".env").write_text("PRIVATE_TEST_VALUE")
            result = d.preflight(source)
            self.assertTrue(result["source_syntax_ok"])
            self.assertFalse(result["secrets_read"])
            (directory / "security.py").write_text("<<<<<<< current\n")
            self.assertFalse(d.preflight(source)["ok"])

    def test_cli_error_redacts_argument_values(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = d.main(["health", "--base-url", BASE + "?token=PRIVATE_TEST_VALUE", "--expected-name", NAME])
        self.assertEqual(code, 1)
        self.assertNotIn("PRIVATE_TEST_VALUE", output.getvalue())

    def test_auth_requires_explicit_contract(self):
        with patch.object(d, "auth_probe") as probe, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(d.main(["auth", "--base-url", BASE, "--expected-name", NAME]), 1)
        probe.assert_not_called()


if __name__ == "__main__":
    unittest.main()
