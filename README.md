# Dots × Hermes 部署套件

**繁體中文** | [English](README.en.md)

> **2026-10-08 文件補充（軟體仍為 0.4.0）：[D：私人 MCP／Tunnel 常駐 worker CLI](docs/VERIFIED_RECORD.md)。** A 是歷史中介 Mac 路徑；B 是 0.4.0 桌面執行器 CLI → loopback A2A；D 是獨立的新路徑，不是仍未驗證的 C 雲端 tailnet 實驗。以下桌面／原生 MCP 限制按 2026-10-06 的 A/B 範圍解讀，不套用至 D。

版本：0.4.0｜整理與核對日期：2026-10-06（UTC）｜語言：繁體中文與英文

這是供其他機器重用的部署專案，現含自製 Python stdio MCP／CLI bridge、預設 dry-run 的隔離安裝器、無秘密範本與驗收手冊。原案例中介 bridge 仍未取得；新程式不是原檔移植。沒有現存憑證、registry、備份或日誌。[Mac mini 安裝與操作](docs/MAC_MINI_BRIDGE.md) 是新實作入口。乾淨 prefix 安裝、真 Hermes CLI／標準 stdio MCP health/card 已通過；B 本機單次認證派工亦 PASS：HERMES_OK、HTTP200、completed、7.69秒、0 agent tool calls。新硬體／新帳號與 Dots 原生 MCP 尚未驗收，見[本輪驗收](docs/ACCEPTANCE_2026-10-06.md)。本機個案另經授權加入專用 caller trust 與必要重啟，憑證由使用者親自配置。0.4.0來源更新至[既有GitHub專案](https://github.com/fdexpert/dots-hermes-deployment)，發布範圍見[公開檢查](PUBLICATION_AUDIT.md)。

## 2026-10-08：獨立通道與驗收邊界

目前證實路徑：`dot → private MCP plugin → Secure MCP Tunnel → host stdio MCP worker → local Hermes`。舊 A/B 路徑需要 desktop；此獨立通道不代表既有 installer 已具備 tunnel 安裝能力，不假設 plugin config schema。

主對話 web/macOS 直接透過 connector 送全新 nonce echo，實際結果匹配、exit 0、約 31 秒。使用者回報中介 Mac 與 Hermes Mac 的 ChatGPT desktop 均未開；閉桌面條件不是本次程序檢查獨立驗證，本次亦未重送測試。手機、新機、重啟恢復及長任務可靠性尚未驗收。

後續長文件任務已明確 TimeoutError：queue／accepted 不等於 done，必須取得 terminal state + actual result + return code；成功還須結果符合預期且 return code 0。未知先 query 原任務，不重送。本次只修文件，版本仍為 0.4.0，發布 manifest 維持 69 檔。

官方參考：[Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)、[Add custom MCP server](https://developers.openai.com/api/docs/guides/custom-mcp-server)。參考文件不是本套件安裝能力的證明。

## 先選架構

| 路徑 | 執行位置與資料流 | 證據與適用情境 |
| --- | --- | --- |
| A：中介 Mac | Dots → 已連線 Mac 執行器（案例 中介 Mac）→ Python stdio a2a-bridge → Tailscale Serve HTTPS :10000 → Hermes 主機（案例 Hermes Mac）127.0.0.1:9900 | 原案例已完成一次遠端 HERMES_OK。新機可選本套件的新 bridge（mock 通過，真實路徑待驗收）；若選原案例 bridge，仍需授權取得來源／schema。 |
| B：直接 Mac | Dots → Hermes 所在 Mac 執行器 → 本機執行／本機 A2A client → 127.0.0.1:9900 | 新 bridge 的 CLI 真 health/card 與單次具名認證派工已通過：HERMES_OK、7.69秒、0 tools。原生 Dots MCP、新硬體／帳號及實際關閉中介機實驗仍未驗收。 |
| C：雲端 runtime | Dots 雲端環境 → userspace 網路／代理 → tailnet A2A | 曾評估 socket、egress 與持續性限制，未實作成功。不列為可部署選項。 |
| D：私人 MCP／Tunnel | dot → private MCP plugin → Secure MCP Tunnel → host stdio MCP worker → local Hermes | 擁有者回報 2026-10-08 Web 測試通過，兩台 Mac 的 ChatGPT desktop 均未開啟；真實 Hermes 輸出含測試 nonce，約 31 秒、exit 0。未在本次文件更新重跑；行動端／新硬體未測。詳見已驗證紀錄。 |

Dots 的「連接電腦」提供執行器；不是把 stdio MCP 變成 HTTP MCP 的入口。案例中的 HTTPS :10000 是 **Hermes A2A HTTP**，不是 MCP HTTP。詳見 [架構與角色](docs/ARCHITECTURE.md)。官方 Dots 說明區分雲端與個人電腦，個人電腦需上線且 app 開啟；其存取權也與 Codex 連線分開：[Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)。

## 快速開始（A/B；D 證據見已驗證紀錄）

1. 解壓 ZIP 到自己的專案目錄，閱讀 [前置需求](docs/PREREQUISITES.md) 與 [安全／憑證交接](docs/SECURITY.md)。只在已獲授權的新機部署。
2. 在 [參數表](docs/PARAMETERS.md) 填入新機身份、主機名、連接埠及路徑。所有 `example`／`REPLACE_` 都必須替換；不要沿用案例的身份或 token。
3. 先執行套件自身離線測試。它們使用自製mock／暫存prefix，不連現有服務、不做真派工，也不讀真實設定：

   ```sh
   python3 -B -m unittest discover -s tests -v
   python3 -B scripts/validate_kit.py
   python3 -B scripts/diagnose.py preflight
   ```

4. 先按 [Mac mini bridge 安裝](docs/MAC_MINI_BRIDGE.md) 審閱計畫，再明確 apply 至新私人 prefix。依 [部署手冊](docs/DEPLOYMENT.md) 分別準備 server／網路；B 先建立直接電腦連線。安裝不派工、不配置 server 安全或全域 MCP。
5. 依 [四層驗收](docs/VALIDATION.md) 留下結果，再勾選 [部署檢查表](DEPLOYMENT_CHECKLIST.md)。單純 HTTP 200 不代表認證／派工完成。

唯讀連線範例（須在目標主機或已授權 caller 執行）：

```sh
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target
```

工具拒絕 URL 中的帳密、query、fragment、非根路徑與非 tailnet 的遠端 URL；不跟隨 redirect、不停用 TLS、不輸出回應全文。選用 `auth` 是不派工的未定義 RPC 方法探測，須先核對目標 Hermes 的拒絕順序；從本機隱藏輸入取得 token，不接受命令列 token，詳見 [工具說明](scripts/README.md)。

## 文件索引

- [Mac mini bridge／隔離安裝／CLI與MCP](docs/MAC_MINI_BRIDGE.md)
- [0.4.0本輪驗收矩陣與安全交接](docs/ACCEPTANCE_2026-10-06.md)、[結構化證據](docs/ACCEPTANCE_2026-10-06.json)
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

## 0.4.0 A/B 交付邊界（2026-10-06）

本套件提供自製 bridge、唯讀診斷、隔離安裝器與包裝驗證；YAML／環境設定仍是增量範本。原案例 bridge 來源與依賴仍待取得。新 bridge 的 SendMessage 必須明確操作並確認；沒有現有服務自動部署、安全修復或安裝時派工。已知 `fleet_ask` 同步等待約 300 秒，逾時後缺完整查回流程；未知結果不得重送。直接執行器需要 Hermes Mac 醒著、上線、app 運作。替換 Dots 個人電腦選擇不會搬遷既有 task。[證據與限制](docs/VERIFIED_RECORD.md)

每份文件都有完整英文對照與語言切換；兩版共用技術欄位、命令及驗收原文。範本註解與拓撲提供雙語說明，CLI 輸出維持英文。
