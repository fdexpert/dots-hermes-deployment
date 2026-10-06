# Mac mini bridge 與隔離安裝

**繁體中文** | [English](MAC_MINI_BRIDGE.en.md)

0.4.0 提供本專案新寫的 `scripts/bridge.py` 與 `scripts/install.py`。這不是原案例未取得的 bridge，也沒有拷貝第三方實作。以本機非秘密 Hermes A2A 原始碼及官方 A2A/MCP 契約核對；只使用 Python stdlib，不需 MCP SDK、pip 或網路下載依賴。

已在這台 macOS26.6.2 arm64、Python3.14.5 的**暫存隔離prefix**實測安裝與CLI/MCP對自製mock呼叫。[本輪驗收](ACCEPTANCE_2026-10-06.md)另通過真Hermes CLI／標準stdio MCP health/card，以及B本機單次具名認證派工：HERMES_OK、HTTP200、completed、7.69秒、0工具。使用者親自配置憑證，批准後增量加入caller trust並完成必要gateway重啟。新帳號／其他新硬體／原生DotsMCP仍未驗收。安裝器只支援macOS arm64、Python3.11–3.14，不宣稱其他OS已部署。

## 1. 先測套件，再審閱安裝計畫

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py --public
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action install
```

測試會自行建立並清理 loopback 隨機 port mock／暫存 venv，用合成憑證，不連真 Hermes。測試環境需允許本機 socket；不能為通過測試改現有服務。安裝器不加 `--apply` 時只回傳計畫，不建立 prefix、venv 或設定。prefix 必須是絕對路徑、無 symlink、parent 已存在，且不能位於 kit 內或包住 kit。

## 2. 明確 apply 到全新私人 prefix

確認主機與目錄授權後：

```sh
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action install --apply
```

只產生 prefix 內的 `app/bridge.py`、`app/diagnose.py`、`venv/`、`config/bridge-config.json` 與 `.kit-install.json`。venv 使用目前 Python、無 pip、無 system-site-packages；不改全域 Python、Hermes、launchd、Serve、trust 或 MCP 註冊。不啟動服務、不生成／搬運 token。

同版本／同 source hash 重跑且 managed 檔案沒變時，回 `changed:false`，不讀／覆寫 config。未知 prefix、symlink、已改或多出的 managed 區檔案一律拒絕；不同版本／hash 需新 prefix，沒有原地升級。用下方完整 interpreter 路徑呼叫，不需 activate；base Python 被移除時需在新 prefix 重建。

## 3. 在私密本機編輯非秘密 config

安裝器配置預設沒有 token、也沒有派工契約確認。以 [範本](../examples/bridge-config.example.json) 為起點：

| 欄位 | 語意 |
| --- | --- |
| `schema_version` | 固定 1；未知欄位拒絕 |
| `caller_id` | 預期 caller 的標籤；不代替 bearer 認證，也不證明 server 的映射 |
| `targets.<alias>.base_url` | 明確 pin 的 loopback HTTP(S) 或 tailnet HTTPS 根 URL；不跟隨 card URL或 redirect |
| `expected_name` | health 的 agent／card 的 name 必須相同 |
| `timeout_seconds` | 0.05–360 秒；RPC 預設30，範本330；health/card上限30。這是 socket I/O timeout，不是硬性全程截止 |
| `contract` | RPC 前由操作者核對 server 後設 `hermes-a2a-v1-inspected`；範本刻意省略 |
| `token_file` | 選用：使用者自行準備、kit 外的絕對路徑，僅 RPC 時讀單一原始 token；不得把 token 值放 config |

不提供舊 registry 自動匯入。A 使用實際新機 `.ts.net` HTTPS URL；B 使用 loopback，不需中介 Mac或 Serve。[安全交接](SECURITY.md) 仍需具名獨立 token／非空 trust、loopback、allow-all false、保留身份限制，不修改原 server 安全常數。

## 4. 先唯讀 health/card

```sh
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json health --target example-target
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json card --target example-target
```

不讀 token、不 POST、不派工；GET200不是認證證據。固定輸出呈現 send/query是否啟用、card相容性與 loopback警告。RPC 前會重新核對 health/card身份、JSONRPC1.0、bearer公告。固定URL覆蓋card的loopback；不支援 tenant、多profile非根路徑、legacy v0.3、SSE／push／取消或通用Message回覆。

## 5. 憑證與 stdio MCP

使用者在私密介面親自建立 caller 的原始 token 檔，owner為目前使用者、權限600或400、普通檔案非symlink、最多8192bytes；範本占位／Bearer前綴／空白值拒絕。建議放在安裝 prefix與kit之外。不將值貼聊天、命令列、env或MCP tool參數。CLI也可選 `--prompt-token` 使用隱藏輸入；stdio MCP不提供互動 token prompt。

在所選 MCP client 手動設定 command為安裝 interpreter、args為下方命令的其餘部分，按該client的實際格式配置：

```sh
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json mcp
```

預設 `tools/list` 只列 `fleet_health`、`fleet_card`。支援 newline JSON-RPC、initialize／initialized／ping／tools/list／tools/call；MCP版本2025-11-25、2025-06-18、2025-03-26。stdout只寫MCP訊息。沒有 HTTP MCP listener或全域自動註冊；Dots的電腦存取與MCP client連線需各自取得權限，不承諾每個task已有此client。

## 6. 授權後明確派工／查詢

CLI派工須 `--confirm-send`、私人訊息檔與 kit 外的私人 state dir（parent已存在）。不要把真人工作訊息或state交付到repo。以下僅為經授權後的操作範例，不是安裝步驟：

```sh
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json --state-dir /Users/example/dots-hermes-state send --target example-target --message-file /path/to/private-message.txt --confirm-send
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json get-task --target example-target --task-id task-example
/Users/example/dots-hermes-bridge/venv/bin/python -B /Users/example/dots-hermes-bridge/app/bridge.py --config /Users/example/dots-hermes-bridge/config/bridge-config.json find-context --target example-target --context-id ctx-example
```

MCP另需啟動 `mcp --enable-send --enable-query` 並在啟動前提供 `--state-dir`。派工工具 `fleet_send` 要 `target`、`message`、`confirm_send:true`；具destructive標示。查詢工具 `fleet_get_task` 要 `target/task_id`，`fleet_find_context` 要 `target/context_id`。未知參數／token參數拒絕。旗標與確認布林是操作界線，不能取代人類授權；client仍須保留使用者可拒絕的確認流程。

預設只回傳狀態／IDs，不顯示任務文字。另選 CLI `--show-reply` 或 MCP `include_reply:true` 才輸出回覆；會遮蔽目前token與已知secret格式，不能保證偵測任意未知秘密。state快照600、目錄700，只保存request/message/context/task ID、caller標籤、HTTP／state／錯誤類別／耗時，**不保存訊息、回覆、token或回應全文**。

Hermes本版本的 `SendMessage` 同步等待，並未實作提前回ID；送出前先保存fresh context參照，後保存非秘密結果。逾時／不匹配回應／中斷表示結果未知，不自動重試或重送。已知task可用真正的 `GetTask`；沒有task ID可明確以context呼叫 `ListTasks`（最多20、只提示更多頁，不自動翻頁）。store在記憶體，有重啟／過期／scope／權限限制；查不到不等於任務沒執行，不構成可靠佇列／去重。查詢不能發SendMessage。

真實首次驗收另授權一次[HERMES_OK原文](VALIDATION.md)，不能用mock通過代替。

## 7. 卸載與失敗回復

```sh
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action uninstall
python3 -B scripts/install.py --prefix /Users/example/dots-hermes-bridge --action uninstall --apply
```

先dry-run，再明確apply。只有owner marker完整且所有managed fingerprint吻合才逐檔刪除app／venv／marker；保留整個config與prefix，不遞迴刪整個prefix。未知或改動檔案會拒絕，先人工審查，不force。

新安裝失敗且managed snapshot未改時移除本次managed項目、保留config。venv建置中斷／新增或改動未知檔案時，保留私人partial prefix與不完整marker供人工檢查，後續apply/uninstall拒絕；選新prefix或由擁有者核對後處理。即使測試失敗也不改真服務來修復。
