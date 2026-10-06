# 詳細部署順序

以下是**未在本次執行**的操作者步驟。命令已核對本機 parser／官方文件；新版本先執行 `--help` 核對。所有既有服務變更先評估停機，不能直接在案例機套用。

## 1. 記錄架構與授權

填 [參數表](PARAMETERS.md)、確定 A 或 B、列所需權限。確認目標是新機、可停機窗口、備份與 rollback owner。[前置需求](PREREQUISITES.md)、[安全](SECURITY.md)

## 2. 準備官方軟體與乾淨版本

依官方來源安裝 ChatGPT app、Hermes，A 再安裝 Tailscale。記錄版本／SHA與安裝 owner。不在已運行 Hermes home 執行不明 bootstrap；不安裝全套過期依賴。原始碼有衝突標記或 local-readonly 安全客製不存在時，停止並核對相容版本。

## 3. 準備 Hermes gateway

先確定 profile 有可工作模型；只在新機執行：

```sh
hermes gateway setup
```

選 A2A，核對結果與 [server config 片段](../examples/server-config.fragment.example.yaml)。setup 可配置多個平台與秘密，由使用者操作私密介面；不要把 wizard 完整輸出放入交付。

依 [增量設定](CONFIGURATION.md) 加入具名 trust／loopback／顯示名稱。先以限制模式準備，不急於 Serve。由使用者完成 [peer token 交接](SECURITY.md)，確認 token 對應 caller／保留身份，無非空環境 trust 覆寫。具名遠端呼叫準備完成後，再設定 `a2a.local_bridge_only: false`。

## 4. 啟動且核對只有一個 gateway

新機首次可採前景模式（終端保持開啟）：

```sh
hermes gateway run
```

需要 macOS 正式 background service，且操作者已授權安裝時，可依目前 parser 分步操作：

```sh
hermes gateway install --no-start-now
hermes gateway start
```

先核對 `hermes gateway --help`；不要同時 run 與 service，不用 `--force`／`--replace` 繞過現有 supervisor。label 取自新機安裝結果，不沿用案例 service label 或建立硬編碼 plist。啟動／重啟影響整個 gateway 的其他平台，不是只 A2A。

本機唯讀核對：

```sh
lsof -nP -iTCP:9900 -sTCP:LISTEN
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
```

`lsof` 只看 listener，不印完整 process argv／env。成功應只有預期 gateway 對 loopback 9900 監聽；port 衝突先調查，不 kill 不明程序。

## 5A. 只在 A 配置 tailnet Serve

兩端使用者登入授權 tailnet；管理者核對 caller→target:10000 grants／ACL、MagicDNS／HTTPS。先在本機檢視現有 `tailscale serve status` 與 `tailscale funnel status`，不把完整結果公開。若已有同 port／path，先評估與備份，不覆蓋。

已確認 token／trust 且授權新增此服務時：

```sh
tailscale serve --bg --https=10000 http://127.0.0.1:9900
tailscale serve status
```

這會修改 Serve，命令不是 kit 的自動行為。應顯示只在 tailnet 可用，target 為 loopback 9900，不能改成 Funnel。不使用 `reset` 或全域覆寫，保留既有其他 Serve／Funnel 配置。[官方 Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve)

在 caller Mac 依實際新機 DNS 執行 health/card，先確認 TLS、agent name 與 card URL。[驗收](VALIDATION.md)

## 6A. 取得、核對並安裝原 bridge

由擁有者授權提供 中介 Mac 非秘密 bridge 原始碼／依賴／去秘密 schema。尚未取得，**目前不能完成新機 A 端到端 bridge 部署**；server／HTTP 準備不等於完整 bridge 已移植。

取得後先核對 caller_id、URL override、原始 token 讀取、MCP `tools/list` 的 `fleet_ask` 輸入 schema與逾時行為；依官方／原始 lockfile 建立獨立環境，不猜 dependency 版本。使用者在 kit 外新建真 registry，更新 target alias／URL／原始 peer token。

依取得 bridge 的實際 MCP client 使用方式配置 **stdio** command／args（Python 路徑與 `.py` 路徑）；不把 A2A HTTPS URL當 HTTP MCP server 註冊。只 `tools/list` 核對 schema，避免自動呼叫派工。Dots 的連接電腦不自動讓所有 task 擁有此 tool；確認新 task 的 client／bridge 能力，才進行授權驗收。[契約](BRIDGE_CONTRACT.md)

## 5B. Dots 直接連接 Hermes Mac

在該機 ChatGPT app 的 dot profile → Computers → Your computer → Allow access，由使用者審閱並確認。維持機器醒著、上線、app 開啟。新建獨立本機 task，檢查實際環境；可授權只执行 `printf 'EXAMPLE_LOCAL_EXEC_OK\n'` 確認本機執行，這不是 Hermes 派工。

B 的本機 A2A client 需另外取得與驗證，使用 loopback URL／新具名 caller credential。B 只做本機派工不需 Serve；不要為方便移除 token／trust。若重用已驗證 bridge 原始碼，必須重新核對本機路徑、registry URL 與身份，不能宣稱本套件已附它。

## 7. 四層驗收與交接

完成 [驗收矩陣](VALIDATION.md) 與 [檢查表](../DEPLOYMENT_CHECKLIST.md)。新機實際派工需使用者單獨授權，僅一次指定 HERMES_OK 訊息。保留去秘密結果與版本；若逾時結果未知，停止並人工確認，不重送。交接操作手冊與 kit ZIP；秘密／備份透過獨立受控方式保管。
