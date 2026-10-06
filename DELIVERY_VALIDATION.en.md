# Delivery validation

[繁體中文](DELIVERY_VALIDATION.md) | **English**

Date: 2026-10-06 UTC | Kit 0.3.0 | macOS 26.6.2 arm64 | Python 3.14.5

| Check | Result / evidence |
| --- | --- |
| Offline tests | All 27 tests passed with fake transport/in-memory responses; no sockets or task dispatch. |
| Python syntax | All five kit Python files passed AST parsing. Initial kit preflight also checked five fixed Hermes A2A source files as syntax_ok; the bilingual update did not retest existing services. |
| JSON | MANIFEST, non-secret plan, and two synthetic fixtures parse successfully. |
| YAML | Three example YAML files passed local PyYAML safe_load. PyYAML is not a kit runtime dependency. |
| Language consistency | All 22 document pairs have reciprocal language links; deployment commands/official links/template values match; both editions retain the same exact HERMES_OK acceptance input. |
| Internal links / files | All 60 explicit manifest files and local Markdown links passed; no symlinks. |
| Dry-run | Idempotent output; input/user files preserved; no file changes on failure; A/B endpoint/port consistency tests passed. No apply mode. |
| Secret scan | Filenames/content checked; only newly created kit files packaged. No reading/copying existing .env, registry, credentials, backups, or full logs. Fixtures are synthetic. |
| Public scan | Passed email/personal-home/private-IPv4/non-example-tailnet-DNS/UUID checks; case host/identity identifiers removed. Root .git is version-control metadata only and excluded from ZIP; publishable history scanned separately. |
| ZIP | Explicit allowlist; archive names/bytes/secret-pattern checks passed. No real .env, .git, machine backups, logs, Library helpers, or caches. |

Commands:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py
python3 -B scripts/validate_kit.py --public
python3 -B scripts/diagnose.py preflight
python3 -B scripts/plan.py --spec examples/deployment-plan.example.json --dry-run
python3 -B scripts/validate_kit.py --public --zip /path/to/dots-hermes-deployment-kit.zip
```

ZIP SHA256 and byte size are supplied in the delivery message, avoiding a circular self-hash inside the archive. See [FILES](FILES.en.md).

Kit creation/bilingual editing/testing did not deploy a machine, change services/security/credentials, or dispatch Hermes tasks. Public 0.2.0 GitHub publication was separately authorized and checked remotely. This edition uses the same authorized project, with content/history checks before publication. Complete intermediary bridge source remains missing. B local tasks/intermediary independence, C, and other OS deployments remain unverified. The kit's 27 tests are not the complete Hermes pytest suite.
