"""Synthetic credentials and a self-owned loopback mock only; never Hermes."""
import contextlib
import copy
import io
import json
import os
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
import bridge as b
import install as installer
from test_diagnostics import Response

NAME = "hermes-example-target"
FIXTURE_TOKEN = "synthetic-fixture-credential"


@contextlib.contextmanager
def mock_server():
    state = {"posts": [], "mode": "ok", "tasks": {}, "name": NAME}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, body):
            raw = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            if self.path == "/health":
                self.reply(200, {"status": "ok", "agent": state["name"]})
            else:
                card = json.loads((ROOT/"tests/fixtures/card.example.json").read_text())
                card["name"] = state["name"]
                self.reply(200, card)

        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            state["posts"].append(request)
            if self.headers.get("Authorization") != "Bearer " + FIXTURE_TOKEN:
                return self.reply(401, {"error": {"message": FIXTURE_TOKEN}})
            if state["mode"] in ("403", "429", "500"):
                return self.reply(int(state["mode"]), {"error": {"message": FIXTURE_TOKEN}})
            method, params = request["method"], request["params"]
            if state["mode"] == "slow":
                time.sleep(0.25)
            if state["mode"] == "wrong_id":
                return self.reply(200, {"jsonrpc": "2.0", "id": "wrong", "result": {}})
            if state["mode"] == "missing_method":
                return self.reply(200, {"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32601}})
            if method == "SendMessage":
                task = {"id": "task-fixture", "contextId": params["message"]["contextId"],
                        "status": {"state": "TASK_STATE_COMPLETED"},
                        "artifacts": [{"parts": [{"text": "HERMES_OK " + FIXTURE_TOKEN}]}]}
                if state["mode"] == "echo_id":
                    task["id"] = FIXTURE_TOKEN
                state["tasks"][task["id"]] = task
                result = {"task": task}
            elif method == "GetTask":
                if params["id"] not in state["tasks"]:
                    return self.reply(200, {"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32001}})
                result = state["tasks"][params["id"]]
            elif method == "ListTasks":
                result = {"tasks": [t for t in state["tasks"].values() if t["contextId"] == params["contextId"]], "nextPageToken": ""}
            else:
                result = None
            self.reply(200, {"jsonrpc": "2.0", "id": request["id"], "result": result})

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(server.server_port), state
    finally:
        server.shutdown()
        server.server_close()  # Waits for our non-daemon request threads.
        thread.join(timeout=2)
        assert not thread.is_alive()


def config(base, token_file=None, timeout=2):
    target = {"base_url": base, "expected_name": NAME, "timeout_seconds": timeout, "contract": b.CONTRACT}
    if token_file:
        target["token_file"] = str(token_file)
    return {"schema_version": 1, "caller_id": "example-caller", "targets": {"example-target": target}}


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.token = self.root/"fixture-token.local"
        self.token.write_text(FIXTURE_TOKEN)
        self.token.chmod(0o600)
        self.state_dir = self.root/"receipts"

    def client(self, base, **kwargs):
        return b.Bridge(config(base, self.token), state_dir=self.state_dir, **kwargs)

    def test_config_schema_and_unsafe_urls(self):
        path = self.root/"bridge-config.json"
        data = config("http://127.0.0.1:9900")
        path.write_text(json.dumps(data))
        self.assertEqual(b.load_config(path), data)
        for update in [{"token": FIXTURE_TOKEN}, {"base_url": "https://user:" + FIXTURE_TOKEN + "@example.ts.net"},
                       {"base_url": "https://example.ts.net?credential=x"}, {"timeout_seconds": True}, {"contract": "guess"}]:
            bad = copy.deepcopy(data)
            bad["targets"]["example-target"].update(update)
            path.write_text(json.dumps(bad))
            with self.assertRaises(b.BridgeError):
                b.load_config(path)

    def test_private_token_permissions_symlink_placeholder(self):
        self.assertEqual(b.token_from_file(self.token), FIXTURE_TOKEN)
        self.token.chmod(0o644)
        with self.assertRaises(b.BridgeError):
            b.token_from_file(self.token)
        self.token.chmod(0o600)
        link = self.root/"link"
        link.symlink_to(self.token)
        with self.assertRaises(b.BridgeError):
            b.token_from_file(link)
        self.token.write_text("REPLACE_WITH_PRIVATE_TOKEN")
        with self.assertRaises(b.BridgeError):
            b.token_from_file(self.token)

    def test_default_health_card_no_credentials_or_post(self):
        with mock_server() as (base, state), patch.object(b, "token_from_file", side_effect=AssertionError("must not read")):
            client = self.client(base)
            self.assertTrue(client.inspect("example-target", "health")["ok"])
            card = client.inspect("example-target", "card")
            self.assertTrue(card["ok"])
            self.assertFalse(card["authentication_proven"])
            self.assertTrue(card["endpoint_pinned_to_config"])
            self.assertEqual(state["posts"], [])
            with self.assertRaises(b.BridgeError):
                client.send("example-target", "fixture task", confirm=True)
            self.assertFalse(self.state_dir.exists())

    def test_send_confirmation_required_before_network(self):
        with mock_server() as (base, state):
            client = self.client(base, enable_send=True)
            with self.assertRaises(b.BridgeError):
                client.send("example-target", "fixture task")
            self.assertEqual(state["posts"], [])

    def test_identity_mismatch_no_token_or_post(self):
        with mock_server() as (base, state), patch.object(b, "token_from_file", side_effect=AssertionError("must not read")):
            state["name"] = "wrong-target"
            with self.assertRaises(b.BridgeError):
                self.client(base, enable_send=True).send("example-target", "fixture task", confirm=True)
            self.assertEqual(state["posts"], [])

    def test_credential_and_contract_required_no_post(self):
        with mock_server() as (base, state):
            client = b.Bridge(config(base), state_dir=self.state_dir, enable_send=True)
            with self.assertRaises(b.BridgeError) as caught:
                client.send("example-target", "fixture task", confirm=True)
            self.assertEqual(caught.exception.code, "credential_required")
            client.config["targets"]["example-target"].pop("contract")
            with self.assertRaises(b.BridgeError):
                client.send("example-target", "fixture task", confirm=True)
            self.assertEqual(state["posts"], [])

    def test_send_receipts_redacted_and_known_task_query(self):
        with mock_server() as (base, state):
            client = self.client(base, enable_send=True, enable_query=True)
            result = client.send("example-target", "private fixture input", confirm=True)
            self.assertTrue(result["ok"])
            self.assertEqual(result["task_state"], "TASK_STATE_COMPLETED")
            self.assertNotIn("reply", result)
            self.assertEqual(len(state["posts"]), 1)
            wire = state["posts"][0]
            self.assertEqual(wire["params"]["message"]["role"], "ROLE_USER")
            self.assertFalse(wire["params"]["configuration"]["returnImmediately"])
            saved = "\n".join(p.read_text() for p in self.state_dir.iterdir())
            self.assertNotIn(FIXTURE_TOKEN, saved)
            self.assertNotIn("private fixture input", saved)
            self.assertNotIn("HERMES_OK", saved)
            self.assertIn("message_id", saved)
            query = client.rpc("example-target", "GetTask", {"id": result["task_id"], "historyLength": 0}, include_reply=True)
            self.assertIn("HERMES_OK", query["reply"])
            self.assertNotIn(FIXTURE_TOKEN, query["reply"])
            lookup = client.rpc("example-target", "ListTasks", {"contextId": result["context_id"], "pageSize": 20})
            self.assertEqual(lookup["tasks"][0]["task_id"], result["task_id"])
            state["tasks"].clear()
            missing = client.rpc("example-target", "GetTask", {"id": result["task_id"]})
            self.assertEqual(missing["error"], "task_not_found")
            self.assertEqual(sum(p["method"] == "SendMessage" for p in state["posts"]), 1)

    def test_timeout_unknown_no_resend_receipt_recover_by_context(self):
        with mock_server() as (base, state):
            client = self.client(base, enable_send=True, enable_query=True)
            client.config["targets"]["example-target"]["timeout_seconds"] = 0.05
            state["mode"] = "slow"
            result = client.send("example-target", "fixture task", confirm=True)
            self.assertEqual(result["error"], "timeout")
            self.assertTrue(result["outcome_unknown"])
            self.assertTrue(result["do_not_resend"])
            self.assertFalse(result["automatic_retry"])
            self.assertEqual(len(state["posts"]), 1)
            time.sleep(0.3)  # Only the self-owned mock's short delay.
            state["mode"] = "ok"
            client.config["targets"]["example-target"]["timeout_seconds"] = 2
            lookup = client.rpc("example-target", "ListTasks", {"contextId": result["context_id"], "pageSize": 20})
            self.assertEqual(len(lookup["tasks"]), 1)
            self.assertEqual(sum(p["method"] == "SendMessage" for p in state["posts"]), 1)

    def test_http_errors_method_missing_wrong_id_no_secret_echo(self):
        with mock_server() as (base, state):
            client = self.client(base, enable_send=True)
            for mode, error in [("403", "forbidden"), ("429", "rate_limited"), ("500", "http_error"),
                                ("missing_method", "method_not_supported"), ("wrong_id", "rpc_response_mismatch")]:
                state["mode"] = mode
                result = client.send("example-target", "fixture task", confirm=True)
                self.assertEqual(result["error"], error)
                self.assertNotIn(FIXTURE_TOKEN, json.dumps(result))
            self.token.write_text("invalid-fixture-credential")
            result = client.send("example-target", "fixture task", confirm=True)
            self.assertEqual(result["error"], "unauthorized")

    def test_transport_default_tls_no_proxy_redirect_bounded(self):
        with patch.object(b.urllib.request, "build_opener") as opener:
            opener.return_value.open.return_value = Response(b'{}')
            b.transport("https://example-target.example-tailnet.ts.net:10000", "/health", timeout=2)
            handlers = opener.call_args.args
            tls = next(h for h in handlers if isinstance(h, b.urllib.request.HTTPSHandler))
            self.assertEqual(tls._context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(tls._context.check_hostname)
            self.assertEqual(next(h for h in handlers if isinstance(h, b.urllib.request.ProxyHandler)).proxies, {})
            self.assertTrue(any(isinstance(h, b.NoRedirect) for h in handlers))
        for response in [Response(status=302), Response(b'x'*(b.LIMIT+1)), Response(b'not-json')]:
            with patch.object(b.urllib.request, "build_opener") as opener:
                opener.return_value.open.return_value = response
                with self.assertRaises(b.BridgeError):
                    b.transport("http://127.0.0.1:9900", "/health", timeout=2)

    def test_states_and_invalid_task(self):
        for state in b.STATES:
            self.assertEqual(b.task_summary({"id":"task-fixture","contextId":"ctx-fixture","status":{"state":state}})["terminal"],
                             state in b.TERMINAL)
        with self.assertRaises(b.BridgeError):
            b.task_summary({"id":"task-fixture","contextId":"ctx-fixture","status":{"state":"made-up"}})

    def test_credential_echo_in_metadata_never_printed_or_saved(self):
        with mock_server() as (base,state):
            state["mode"]="echo_id"
            result=self.client(base,enable_send=True).send("example-target","fixture task",confirm=True)
            self.assertEqual(result["error"],"credential_echo_refused")
            self.assertTrue(result["outcome_unknown"])
            self.assertNotIn(FIXTURE_TOKEN,json.dumps(result))
            self.assertNotIn(FIXTURE_TOKEN,"".join(p.read_text() for p in self.state_dir.iterdir()))

    def test_mcp_lifecycle_default_tools_and_confirmation_gate(self):
        client = b.Bridge(config("http://127.0.0.1:9900"), enable_send=False)
        messages = [{"jsonrpc":"2.0","id":1,"method":"tools/list"},
                    {"jsonrpc":"2.0","id":2,"method":"initialize","params":{"protocolVersion":"2025-11-25"}},
                    {"jsonrpc":"2.0","method":"notifications/initialized"},
                    {"jsonrpc":"2.0","id":3,"method":"tools/list"},
                    {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"fleet_send","arguments":{"target":"example-target","message":"x","confirm_send":True}}}]
        out = io.StringIO()
        b.serve_mcp(client,io.BytesIO(("\n".join(json.dumps(m) for m in messages)+"\n").encode()),out)
        replies=[json.loads(line) for line in out.getvalue().splitlines()]
        self.assertIn("error", replies[0])
        self.assertEqual(replies[1]["result"]["protocolVersion"],"2025-11-25")
        self.assertEqual([t["name"] for t in replies[2]["result"]["tools"]],["fleet_health","fleet_card"])
        self.assertTrue(replies[3]["result"]["isError"])
        self.assertTrue(next(t for t in b.tools(self.client("http://127.0.0.1:9900",enable_send=True)) if t["name"]=="fleet_send")["annotations"]["destructiveHint"])
        class ClosedOutput:
            def write(self,value):
                raise BrokenPipeError()
        b.serve_mcp(client,io.BytesIO((json.dumps(messages[1])+"\n").encode()),ClosedOutput())

    def test_actual_cli_and_stdio_subprocess(self):
        with mock_server() as (base,state):
            path=self.root/"bridge-config.json"
            path.write_text(json.dumps(config(base,self.token)))
            command=[sys.executable,"-B",str(ROOT/"scripts/bridge.py"),"--config",str(path)]
            health=subprocess.run(command+["health","--target","example-target"],capture_output=True,text=True,timeout=10)
            self.assertEqual(health.returncode,0,health.stderr)
            self.assertTrue(json.loads(health.stdout)["ok"])
            msg=self.root/"message.txt"
            msg.write_text("fixture-only task")
            send=subprocess.run(command+["--state-dir",str(self.state_dir),"send","--target","example-target",
                                         "--message-file",str(msg),"--confirm-send"],capture_output=True,text=True,timeout=10)
            self.assertEqual(send.returncode,0,send.stderr)
            self.assertEqual(json.loads(send.stdout)["task_id"],"task-fixture")
            packets=[{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25"}},
                     {"jsonrpc":"2.0","method":"notifications/initialized"},
                     {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"fleet_health","arguments":{"target":"example-target"}}}]
            mcp=subprocess.run(command+["mcp"],input="\n".join(json.dumps(p) for p in packets)+"\n",
                               capture_output=True,text=True,timeout=10)
            self.assertEqual(mcp.returncode,0,mcp.stderr)
            self.assertEqual(len(mcp.stdout.splitlines()),2)
            self.assertNotIn(FIXTURE_TOKEN,mcp.stdout+mcp.stderr+send.stdout+send.stderr)
            self.assertEqual(len(state["posts"]),1)

    def test_actual_mcp_send_query_and_argument_rejection(self):
        with mock_server() as (base,state):
            path=self.root/"bridge-config.json"
            path.write_text(json.dumps(config(base,self.token)))
            packets=[{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25"}},
                     {"jsonrpc":"2.0","method":"notifications/initialized"},
                     {"jsonrpc":"2.0","id":2,"method":"tools/list"},
                     {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"fleet_send","arguments":{"target":"example-target","message":"fixture task","confirm_send":False}}},
                     {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"fleet_send","arguments":{"target":"example-target","message":"fixture task","confirm_send":True}}},
                     {"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"fleet_get_task","arguments":{"target":"example-target","task_id":"task-fixture","include_reply":True}}},
                     {"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"fleet_health","arguments":{"target":"example-target","token":FIXTURE_TOKEN}}}]
            command=[sys.executable,"-B",str(ROOT/"scripts/bridge.py"),"--config",str(path),
                     "--state-dir",str(self.state_dir),"mcp","--enable-send","--enable-query"]
            result=subprocess.run(command,input="\n".join(json.dumps(p) for p in packets)+"\n",
                                  capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            replies=[json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(len(replies[1]["result"]["tools"]),5)
            self.assertTrue(replies[2]["result"]["isError"])
            self.assertFalse(replies[3]["result"]["isError"])
            queried=json.loads(replies[4]["result"]["content"][0]["text"])
            self.assertIn("HERMES_OK",queried["reply"])
            self.assertTrue(replies[5]["result"]["isError"])
            self.assertNotIn(FIXTURE_TOKEN,result.stdout+result.stderr)
            self.assertEqual(sum(p["method"]=="SendMessage" for p in state["posts"]),1)

    def test_state_permission_or_initial_write_failure_prevents_dispatch(self):
        with mock_server() as (base,state):
            self.state_dir.mkdir(mode=0o755)
            with self.assertRaises(b.BridgeError):
                self.client(base,enable_send=True).send("example-target","fixture task",confirm=True)
            self.assertEqual(state["posts"],[])
            self.state_dir.chmod(0o700)
            with patch.object(b,"save_receipt",side_effect=OSError("fixture-only failure")), self.assertRaises(OSError):
                self.client(base,enable_send=True).send("example-target","fixture task",confirm=True)
            self.assertEqual(state["posts"],[])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        self.prefix=self.root/"prefix with spaces"

    def snapshot(self,path):
        return {p.relative_to(path).as_posix():p.read_bytes() for p in path.rglob("*") if p.is_file() and not p.is_symlink()}

    def test_plan_zero_writes_and_unsupported_platform(self):
        before=self.snapshot(self.root)
        result=installer.install(ROOT,self.prefix)
        self.assertFalse(result["will_write"])
        self.assertEqual(self.snapshot(self.root),before)
        self.assertFalse(self.prefix.exists())
        with patch.object(installer.platform,"system",return_value="Linux"), self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="install",apply=True)
        self.assertFalse(self.prefix.exists())

    def test_real_venv_install_idempotence_preserved_config_uninstall(self):
        result=installer.install(ROOT,self.prefix,action="install",apply=True)
        self.assertTrue(result["venv_created"])
        runtime=self.prefix/"venv/bin/python"
        probe=subprocess.run([str(runtime),"-B","-c","import sys; assert sys.prefix != sys.base_prefix"],capture_output=True,timeout=10)
        self.assertEqual(probe.returncode,0)
        user_config=self.prefix/"config/bridge-config.json"
        user_config.write_text("preserve this private user config; do not parse")
        before=self.snapshot(self.prefix)
        self.assertFalse(installer.install(ROOT,self.prefix,action="install",apply=True)["changed"])
        self.assertEqual(self.snapshot(self.prefix),before)
        dry=installer.install(ROOT,self.prefix,action="uninstall")
        self.assertFalse(dry["will_write"])
        self.assertEqual(self.snapshot(self.prefix),before)
        removed=installer.install(ROOT,self.prefix,action="uninstall",apply=True)
        self.assertTrue(removed["config_preserved"])
        self.assertEqual(user_config.read_text(),"preserve this private user config; do not parse")
        self.assertFalse((self.prefix/"venv").exists())
        self.assertFalse((self.prefix/"app").exists())
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="install",apply=True)

    def test_unknown_prefix_and_symlink_no_overwrite(self):
        self.prefix.mkdir()
        user=self.prefix/"important.txt"
        user.write_text("keep")
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="install",apply=True)
        self.assertEqual(user.read_text(),"keep")
        link=self.root/"link"
        link.symlink_to(self.prefix)
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,link,action="install",apply=True)

    def test_modified_or_added_managed_files_refuse_uninstall(self):
        installer.install(ROOT,self.prefix,action="install",apply=True)
        extra=self.prefix/"app/user-added.txt"
        extra.write_text("keep")
        before=self.snapshot(self.prefix)
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="uninstall",apply=True)
        self.assertEqual(self.snapshot(self.prefix),before)
        extra.unlink()
        (self.prefix/"app/bridge.py").write_text("user modified")
        before=self.snapshot(self.prefix)
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="install",apply=True)
        self.assertEqual(self.snapshot(self.prefix),before)

    def test_rollback_preserves_config_and_unknown_files(self):
        def fail(prefix):
            (prefix/"config/bridge-config.json").write_text("user config survives")
            raise RuntimeError("fixture failure")
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="install",apply=True,after_create=fail)
        self.assertEqual((self.prefix/"config/bridge-config.json").read_text(),"user config survives")
        self.assertFalse((self.prefix/"app").exists())
        self.assertFalse((self.prefix/"venv").exists())
        second=self.root/"second"
        def unknown(prefix):
            (prefix/"app/user-added.txt").write_text("keep")
            raise RuntimeError("fixture failure")
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,second,action="install",apply=True,after_create=unknown)
        self.assertEqual((second/"app/user-added.txt").read_text(),"keep")
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,second,action="uninstall",apply=True)

    def test_partial_builder_failure_preserved_for_manual_inspection(self):
        class FailedBuilder:
            def create(self,path):
                path.mkdir()
                (path/"partial").write_text("partial fixture")
                raise RuntimeError("fixture failure")
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT,self.prefix,action="install",apply=True,builder=FailedBuilder())
        self.assertEqual((self.prefix/"venv/partial").read_text(),"partial fixture")
        self.assertTrue((self.prefix/installer.MARKER).exists())

    def test_installed_bridge_cli_mock_and_clean_resources(self):
        installer.install(ROOT,self.prefix,action="install",apply=True)
        with mock_server() as (base,state):
            path=self.prefix/"config/bridge-config.json"
            path.write_text(json.dumps(config(base)))
            command=[str(self.prefix/"venv/bin/python"),"-B",str(self.prefix/"app/bridge.py"),"--config",str(path)]
            result=subprocess.run(command+["health","--target","example-target"],capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])
            self.assertEqual(state["posts"],[])
        installer.install(ROOT,self.prefix,action="uninstall",apply=True)

    def test_installer_cli_plan_apply_repeat_and_uninstall(self):
        command=[sys.executable,"-B",str(ROOT/"scripts/install.py"),"--prefix",str(self.prefix)]
        def run(args):
            result=subprocess.run(command+args,capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            return json.loads(result.stdout)
        self.assertFalse(run([])["will_write"])
        self.assertFalse(self.prefix.exists())
        self.assertTrue(run(["--action","install","--apply"])["changed"])
        self.assertFalse(run(["--action","install","--apply"])["changed"])
        self.assertFalse(run(["--action","uninstall"])["will_write"])
        self.assertTrue(run(["--action","uninstall","--apply"])["config_preserved"])
        self.assertFalse((self.prefix/"venv").exists())
