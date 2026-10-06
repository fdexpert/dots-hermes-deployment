# 詳細部署順序

**繁體中文** | [English](DEPLOYMENT.en.md)

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

## 6A. 安裝自製 kit bridge，或取得原案例 bridge

新部署可選本專案的自製 bridge，依 [Mac mini 安裝流程](MAC_MINI_BRIDGE.md) 先 plan、再明確 apply 至新私人 prefix，手動配置 pinned URL／expected_name。先做 health/card，不自動派工。MCP transport是stdio；依所選client實際格式配置，無全域自動註冊。

使用者在kit與prefix外親自配置新caller原始token；只有完成server具名trust、保留身份限制、版本契約核對及另行授權，才使用明確send／query功能。新程式已經mock／隔離安裝驗證，尚未對真Hermes驗收，不冒稱原bridge已移植。

若選原案例fleet_ask路徑，仍須由擁有者授權提供非秘密來源／lockfile／registry loader／tools/list schema；未取得便停止這條原檔路徑。不能借未授權主機取檔，也不猜工具參數。[兩套契約與差異](BRIDGE_CONTRACT.md)

## 5B. Dots 直接連接 Hermes Mac

在該機 ChatGPT app 的 dot profile → Computers → Your computer → Allow access，由使用者審閱並確認。維持機器醒著、上線、app 開啟。新建獨立本機 task，檢查實際環境；可授權只執行 `printf 'EXAMPLE_LOCAL_EXEC_OK\n'` 確認本機執行，這不是 Hermes 派工。

B可用本套件自製bridge，按Mac mini流程隔離安裝、再驗收真實路徑，使用loopback與新具名caller credential。B 只做本機派工不需 Serve；不要為方便移除 token／trust。若重用已驗證 bridge 原始碼，必須重新核對本機路徑、registry URL 與身份，不能宣稱本套件已附它。

## 7. 四層驗收與交接

完成 [驗收矩陣](VALIDATION.md) 與 [檢查表](../DEPLOYMENT_CHECKLIST.md)。新機實際派工需使用者單獨授權，僅一次指定 HERMES_OK 訊息。保留去秘密結果與版本；若逾時結果未知，停止並人工確認，不重送。交接操作手冊與 kit ZIP；秘密／備份透過獨立受控方式保管。
