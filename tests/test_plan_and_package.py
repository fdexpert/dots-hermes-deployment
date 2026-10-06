import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import plan
import validate_kit as v
from diagnose import DiagnosticError

ROOT = Path(__file__).resolve().parents[1]


class PlanTests(unittest.TestCase):
    def spec(self):
        return json.loads((ROOT / "examples/deployment-plan.example.json").read_text())

    def test_dry_run_idempotent_and_preserves_input(self):
        spec = self.spec()
        original = copy.deepcopy(spec)
        first, second = plan.build_plan(spec), plan.build_plan(spec)
        self.assertEqual(first, second)
        self.assertEqual(spec, original)
        self.assertFalse(first["will_write"])
        self.assertFalse(first["will_execute"])
        first["requested"]["caller_id"] = "changed"
        self.assertEqual(spec, original)
        self.assertIn("existing_serve_and_funnel_routes", first["preserve"])

    def test_rejects_secret_unknown_caller_and_unsafe_bind_without_mutation(self):
        for change in [{"token": "PRIVATE_TEST_VALUE"}, {"listen_host": "0.0.0.0"},
                       {"architecture": "C"}, {"caller_id": "EXAMPLE-LOCAL-BRIDGE"}, {"a2a_port": True}]:
            spec = self.spec()
            spec.update(change)
            original = copy.deepcopy(spec)
            with self.assertRaises(DiagnosticError):
                plan.build_plan(spec)
            self.assertEqual(spec, original)

    def test_dry_run_and_failure_leave_operator_files_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = root / "deployment-plan.example.json"
            user_config = root / "operator-config.txt"
            user_config.write_text("existing routes and user settings\n")
            spec.write_text(json.dumps(self.spec()))
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(plan.main(["--spec", str(spec), "--dry-run"]), 0)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            spec.write_text("invalid-json PRIVATE_TEST_VALUE")
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(plan.main(["--spec", str(spec), "--dry-run"]), 1)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            self.assertNotIn("PRIVATE_TEST_VALUE", output.getvalue())

    def test_b_plan_does_not_require_serve(self):
        spec = self.spec()
        spec.update(architecture="B", base_url="http://127.0.0.1:9900")
        spec.pop("serve_https_port")
        result = plan.build_plan(spec)
        self.assertNotIn("operator_add_tailnet_only_serve_if_needed", result["steps"])

    def test_route_ports_and_architecture_must_match(self):
        for change in [{"serve_https_port": 443}, {"architecture": "B"},
                       {"base_url": "http://127.0.0.1:9900"}]:
            spec = self.spec()
            spec.update(change)
            with self.assertRaises(DiagnosticError):
                plan.build_plan(spec)


class PackageTests(unittest.TestCase):
    def test_paths_reject_secret_backup_git_escape_and_actual_registry(self):
        for name in [".env", ".env.local", ".git/config", "backups/x.md", "logs/x.txt", "agents.yaml",
                     "../x", "/x", "x\\y", "x.pyc"]:
            self.assertFalse(v.safe_relative(name), name)
        self.assertTrue(v.safe_relative("examples/client-agents.schema-pending.example.yaml"))
        self.assertTrue(v.safe_relative(".gitignore"))

    def test_scan_detects_synthetic_secret_and_allows_placeholder(self):
        synthetic = "gh" + "p_" + "A" * 30
        self.assertIn("secret_pattern", v.content_issues("x.md", synthetic))
        self.assertIn("non_placeholder_credential", v.content_issues("x.yaml", "token: PRIVATE_TEST_VALUE"))
        self.assertEqual(v.content_issues("x.yaml", "token: REPLACE_WITH_PRIVATE_TOKEN"), [])
        self.assertIn("non_placeholder_credential", v.content_issues("x.json", '{"token":"PRIVATE_TEST_VALUE"}'))

    def test_public_scan_rejects_synthetic_personal_data(self):
        samples = ["example-person" + "@" + "mail.invalid", "/" + "Users/real-user/project",
                   "10" + ".2.3.4", "100" + ".100.1.2", "real-node.private-tailnet." + "ts.net"]
        for sample in samples:
            self.assertTrue(v.public_content_issues(sample))

    def test_public_scan_allows_loopback_and_example_locations(self):
        for sample in ["http://127.0.0.1:9900", "0.0.0.0 must not be used", "/Users/example/.hermes",
                       "https://example-hermes.example-tailnet.ts.net:10000"]:
            self.assertEqual(v.public_content_issues(sample), [])

    def test_internal_link_and_syntax_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("")
            self.assertEqual(v.markdown_links(root, "README.md", "[ok](README.md)"), [])
            self.assertTrue(v.markdown_links(root, "README.md", "[bad](absent.md)"))
        self.assertIn("invalid_python", v.content_issues("x.py", "if :"))

    def test_archive_exact_bytes_and_rejects_extra_secret_duplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "kit"
            root.mkdir()
            (root / "README.md").write_text("safe example")
            archive = Path(temp) / "kit.zip"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("kit/README.md", b"safe example")
            self.assertEqual(v.validate_archive(archive, root, ["README.md"]), [])
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("kit/README.md", b"changed")
                z.writestr("kit/.env", b"PRIVATE_TEST_VALUE")
            errors = v.validate_archive(archive, root, ["README.md"])
            self.assertIn("zip_file_set_mismatch", errors)
            self.assertIn("zip_unsafe_entry", errors)
            self.assertIn("zip_content_mismatch:README.md", errors)

    def test_tree_requires_exact_manifest_and_no_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            names = ["README.md", "MANIFEST.json"]
            (root / "README.md").write_text("safe")
            (root / "MANIFEST.json").write_text(json.dumps({"files": names}))
            self.assertEqual(v.validate_tree(root)[0], [])
            (root / ".git").mkdir()
            (root / ".git/config").write_text("synthetic local repo metadata")
            self.assertEqual(v.validate_tree(root)[0], [])
            (root / ".env").write_text("PRIVATE_TEST_VALUE")
            self.assertIn("file_set_mismatch", v.validate_tree(root)[0])
            (root / ".env").unlink()
            (root / "README.md").unlink()
            (root / "README.md").symlink_to(root / "MANIFEST.json")
            self.assertIn("README.md:symlink_or_escape", v.validate_tree(root)[0])


if __name__ == "__main__":
    unittest.main()
