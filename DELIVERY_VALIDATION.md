# 交付驗證

**繁體中文** | [English](DELIVERY_VALIDATION.en.md)

日期：2026-10-06 UTC｜kit 0.4.0｜macOS 26.6.2 arm64｜Python 3.14.5

| 檢查 | 結果／證據 |
| --- | --- |
| 測試 | 全51項通過：原27項與新增24項。自製loopback mock、fake transport、合成token、暫存prefix；沒有接真Hermes或讀真憑證。 |
| CLI／MCP | 真子程序測initialize、tools/list/call、health、派工確認、mock SendMessage／GetTask；預設不曝派工工具，拒絕未知／token參數。 |
| HTTP／安全 | 身份不符／缺token／未確認不POST；401/403/429/500與method missing分類；TLS驗證、無proxy/redirect；token回顯遮蔽或拒絕，receipt不含input/reply/token。 |
| 逾時／狀態 | 自製mock逾時不重送、保存context、後明確ListTasks查回；GetTask與所有已知state解析，store清空後task_not_found。不代表真server持久恢復。 |
| 安裝生命週期 | 真venv、CLI plan零寫入、明確apply／重跑冪等、config不讀不覆寫、uninstall保留config；未知／修改prefix拒絕、失敗snapshot回復／partial與未知檔案保留。 |
| 本輪真唯讀驗收 | 新prefix安裝的0.4.0 CLI與標準stdio MCP對真Hermes health/card均HTTP200；身份匹配。這是本機task／標準client，非原生Dots註冊。[完整矩陣](docs/ACCEPTANCE_2026-10-06.md) |
| 真派工／原生Dots | B真認證派工PASS：一次HTTP200／completed／HERMES_OK，7.69秒；audit與對應session核對具名caller及0工具。原生DotsMCP、新硬體／帳號NOTTESTED。 |
| 語法／格式 | 8個Python檔案AST、6個JSON解析；3個YAML以既有本機PyYAML safe_load通過（不是runtime依賴）。 |
| 雙語／檔案 | 24組雙向語言導覽，命令／官方連結一致；69個顯式manifest檔案，內部連結通過，無symlink。 |
| 公開／秘密掃描 | 憑證格式、真env/registry/config、個人email/home、私人IPv4／tailnetDNS／UUID、額外檔案掃描通過。只包新建kit；真憑證／state／venv／測試資料夾／備份／日誌不納入。 |
| ZIP | 69檔allowlist、逐檔bytes與工作樹一致；無.git、cache、Library helper或秘密。SHA256／大小在交付訊息提供。 |
| 發布狀態 | 0.4.0來源更新至既有公開repo main；先前為0.3.0。exact commit、遠端tree與CI結果於push後核對，交付訊息提供commit URL；無新派工或server變更。 |

可重現測試：

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py --public
python3 -B scripts/diagnose.py preflight
python3 -B scripts/validate_kit.py --public --zip /path/to/dots-hermes-deployment-kit.zip
```

安裝試跑／plan/apply/uninstall的實際指令見[Mac mini流程](docs/MAC_MINI_BRIDGE.md)，完整檔案見[FILES](FILES.md)。新測試需允許本機socket；遇到環境禁止bind應取得測試權限，不改現有listener或真服務。

mock／暫存測試已清理。後續另經授權保留個案client，使用者親自配置獨立peer；只增量加入caller trust、確認工作總數0後必要重啟並完成一次B派工。實際credential、config、receipt／case IDs、venv、備份與日誌均不打包。原bridge未取得；新程式是獨立實作。原生DotsMCP、新硬體／帳號、關閉中介機實驗、C與其他OS未測。51tests為09:44的mock suite，來源之後未變；真派工證據另列，不是Hermes完整pytest。

發布前2026-10-06 22:39 UTC重新跑51項離線測試，全數通過（1.557秒）；既有2個commit／89個blob與69檔待提交內容掃描通過，沒有新增真派工。
