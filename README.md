# Dots × Hermes 部署套件

**繁體中文** | [English](README.en.md)

版本：0.3.0｜整理與核對日期：2026-10-06（UTC）｜語言：繁體中文與英文

這是供其他機器重用的部署專案：包含架構決策、逐步部署手冊、無秘密範本、唯讀診斷工具、離線測試與驗收表。它不包含完整中介 bridge，也不包含任何現存憑證、registry、備份或日誌。套件製作沒有部署到新機或修改現有服務；GitHub發布是另外授權的步驟，見[公開檢查](PUBLICATION_AUDIT.md)。

## 先選架構

| 路徑 | 執行位置與資料流 | 證據與適用情境 |
| --- | --- | --- |
| A：中介 Mac | Dots → 已連線 Mac 執行器（案例 中介 Mac）→ Python stdio a2a-bridge → Tailscale Serve HTTPS :10000 → Hermes 主機（案例 Hermes Mac）127.0.0.1:9900 | 案例已完成一次遠端 HERMES_OK。新機需要取得經授權的原 bridge、依賴與 registry schema，套件沒有假冒替代實作。 |
| B：直接 Mac | Dots → Hermes 所在 Mac 執行器 → 本機執行／本機 A2A client → 127.0.0.1:9900 | Hermes Mac 的本機執行與 health/card 已驗證；本機 Hermes 派工與關閉 中介 Mac 後的獨立驗收尚未做。適合不需要中介機的環境。 |
| C：雲端 runtime | Dots 雲端環境 → userspace 網路／代理 → tailnet A2A | 曾評估 socket、egress 與持續性限制，未實作成功。不列為可部署選項。 |

Dots 的「連接電腦」提供執行器；不是把 stdio MCP 變成 HTTP MCP 的入口。案例中的 HTTPS :10000 是 **Hermes A2A HTTP**，不是 MCP HTTP。詳見 [架構與角色](docs/ARCHITECTURE.md)。官方 Dots 說明區分雲端與個人電腦，個人電腦需上線且 app 開啟；其存取權也與 Codex 連線分開：[Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)。

## 快速開始

1. 解壓 ZIP 到自己的專案目錄，閱讀 [前置需求](docs/PREREQUISITES.md) 與 [安全／憑證交接](docs/SECURITY.md)。只在已獲授權的新機部署。
2. 在 [參數表](docs/PARAMETERS.md) 填入新機身份、主機名、連接埠及路徑。所有 `example`／`REPLACE_` 都必須替換；不要沿用案例的身份或 token。
3. 先執行套件自身離線測試。它們不連線、不派工，也不讀真實設定：

   ```sh
   python3 -B -m unittest discover -s tests -v
   python3 -B scripts/validate_kit.py
   python3 -B scripts/diagnose.py preflight
   ```

4. 依序完成 [部署手冊](docs/DEPLOYMENT.md)。A 路徑在 bridge 來源取得前只能完成 server／網路準備；B 路徑先建立直接電腦連線。
5. 依 [四層驗收](docs/VALIDATION.md) 留下結果，再勾選 [部署檢查表](DEPLOYMENT_CHECKLIST.md)。單純 HTTP 200 不代表認證／派工完成。

唯讀連線範例（須在目標主機或已授權 caller 執行）：

```sh
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target
```

工具拒絕 URL 中的帳密、query、fragment、非根路徑與非 tailnet 的遠端 URL；不跟隨 redirect、不停用 TLS、不輸出回應全文。選用 `auth` 是不派工的未定義 RPC 方法探測，須先核對目標 Hermes 的拒絕順序；從本機隱藏輸入取得 token，不接受命令列 token，詳見 [工具說明](scripts/README.md)。

## 文件索引

- [架構與角色](docs/ARCHITECTURE.md)、[example 拓撲文字圖](examples/topology.txt)
- [前置需求／安裝來源／版本](docs/PREREQUISITES.md)、[可替換參數](docs/PARAMETERS.md)
- [部署順序](docs/DEPLOYMENT.md)、[安全／憑證交接](docs/SECURITY.md)、[增量設定](docs/CONFIGURATION.md)
- [bridge 介面契約與來源缺口](docs/BRIDGE_CONTRACT.md)
- [未來 dot 入口](AGENTS.md)、[GitHub 發布與部署交接](docs/GITHUB.md)
- [四層驗收](docs/VALIDATION.md)、[故障排查](docs/TROUBLESHOOTING.md)、[備份與還原](docs/OPERATIONS.md)
- [已驗證紀錄與未驗證清單](docs/VERIFIED_RECORD.md)、[原始碼與官方來源](docs/SOURCES.md)
- [工具與測試](scripts/README.md)、[檢查表](DEPLOYMENT_CHECKLIST.md)、[變更紀錄](CHANGELOG.md)、[交付驗證](DELIVERY_VALIDATION.md)
- [完整檔案清單](FILES.md)、[ZIP allowlist](MANIFEST.json)
- [可公開版本檢查](PUBLICATION_AUDIT.md)、[來源與授權邊界](NOTICE.md)

## 交付邊界

本套件實作的是安全診斷與包裝驗證；YAML／環境設定是增量範本。完整 stdio bridge、其 MCP client 登錄方式與依賴鎖定待取得來源。沒有自動部署、修安全設定或自動發出 HERMES_OK 的腳本。已知 `fleet_ask` 同步等待約 300 秒，逾時後缺完整查回流程；未知結果不得重送。直接執行器需要 Hermes Mac 醒著、上線、app 運作。替換 Dots 個人電腦選擇不會搬遷既有 task。[證據與限制](docs/VERIFIED_RECORD.md)

每份文件都有完整英文對照與語言切換；兩版共用技術欄位、命令及驗收原文。範本註解與拓撲提供雙語說明，CLI 輸出維持英文。
