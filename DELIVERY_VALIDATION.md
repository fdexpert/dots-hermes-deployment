# 交付驗證

日期：2026-10-06 UTC｜kit 0.2.0｜macOS 26.6.2 arm64｜Python 3.14.5

| 檢查 | 結果／證據 |
| --- | --- |
| 新增離線測試 | 27 tests，全部通過；fake transport／記憶體回應，未開socket、未連線派工。 |
| Python語法 | kit的6個Python檔案AST解析通過；另以preflight核對5個固定Hermes A2A source檔案syntax_ok。 |
| JSON | MANIFEST、非秘密規劃與2個合成fixture可解析。 |
| YAML | 3個example YAML以本機PyYAML safe_load解析通過；PyYAML不是kit runtime dependency。 |
| 內部連結／檔案 | 38個顯式manifest檔案、Markdown本機links通過；無symlink。 |
| dry-run | 同輸入冪等、保留輸入／使用者檔案、錯誤不改檔；A/B端點與port一致性測試通過。沒有apply模式。 |
| 秘密掃描 | 已檢查檔名與內容；只打包新建kit檔案，不讀取／複製現存.env、registry、憑證、備份或日誌全文。fixtures全部是合成資料。 |
| 公開掃描 | email／個人home路徑／私人IPv4／非example tailnet DNS／UUID掃描通過；原案例機器與身份識別已移除。沒有.git或既有commit歷史。 |
| ZIP | 顯式allowlist，archive名／byte內容／秘密模式驗證通過；不含真.env、.git、機器備份、日誌、Library helper或cache。 |

命令：

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py
python3 -B scripts/validate_kit.py --public
python3 -B scripts/diagnose.py preflight --hermes-source /path/to/hermes-source
python3 -B scripts/plan.py --spec examples/deployment-plan.example.json --dry-run
python3 -B scripts/validate_kit.py --zip /path/to/dots-hermes-deployment-kit.zip
```

ZIP SHA256與實際byte大小在交付訊息提供，避免把封包自己的hash放進封包形成循環。檔案清單見[FILES.md](FILES.md)。

套件製作／測試未執行新機部署、服務／安全／憑證變更或Hermes派工。GitHub公開發布另經條件授權，須確認指定帳戶的有效登入、公開內容／歷史及遠端結果。完整中介bridge未取得；B本機派工與中介Mac獨立性、C、其他OS仍未驗證。新kit的27tests不是Hermes完整pytest suite。
