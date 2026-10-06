# stdio bridge 介面契約與來源缺口

**繁體中文** | [English](BRIDGE_CONTRACT.en.md)

## 新 kit bridge（0.4.0實作）

本專案新寫的scripts/bridge.py採明確JSON設定，不載入原agents.yaml。已知input schema在MCP tools/list與[Mac mini手冊](MAC_MINI_BRIDGE.md)：預設fleet_health/card，另啟用fleet_send（必須confirm_send:true）、fleet_get_task、fleet_find_context。

已按同一非秘密checkout核對SendMessage同步回result.task、ROLE_USER/text parts/contextId/messageId；GetTask用params.id；ListTasks用contextId/pageSize/includeArtifacts。固定config URL，不跟card跨host；bearer只送該URL。原始碼與依賴均已包含（stdlib）；mock／隔離prefix及真Hermes loopback單次B派工通過。原生DotsMCP、新硬體與新bridge遠端A仍待驗收。

## 原案例契約（歷史紀錄，非完整 schema）

| 介面 | 已確認 | 未取得／應核對 |
| --- | --- | --- |
| process transport | Python stdio MCP `a2a_bridge.py` | Python／MCP SDK／依賴 lock、啟動 flags／cwd、stdout 清潔性 |
| registry | `agents.yaml`、`caller_id`、`agents.<target>.token` 原始 token | 完整 YAML loader、URL 欄位名稱、必要 peer 欄位、timeout 設定名 |
| MCP tool | 名稱 `fleet_ask`、遠端節點選擇、文字訊息、同步結果 | `tools/list` 的完整 input schema；不要猜 `agent`／`node`／`target` 的參數名 |
| HTTP | registry HTTPS 覆蓋案例 card 的 loopback URL，帶 bearer credential | 覆蓋優先序、card v1／legacy 相容性、TLS／redirect 處理 |
| 派工結果 | HTTP 200、TASK_STATE_COMPLETED、回覆文字、耗時、遠端 tool calls | schema／錯誤 mapping／task lookup完整流程 |
| timeout | 案例同步等待約 300 秒，未知結果缺完整查回 | 不假設 server 的 GetTask 等於 bridge 已提供查回功能 |

本套件不虛構原fleet_ask命令／schema，也不冒稱新MCP server是原檔。diagnose不派工；自製bridge只有明確確認才SendMessage。client registry 範本檔名明示 schema pending，不能直接當成已驗證 loader 輸入。

## 來源取得後的準入檢查

1. 確認所有者授權分享程式及依賴；去除內嵌秘密、真 registry、日誌／備份。
2. 固定來源 revision／SHA與授權條款，在新 caller 獨立環境測試，不修改現有服務。
3. 檢查只向明確 target 送出 credentials、拒絕 URL userinfo/query、驗證 TLS、redirect 不洩漏 token、stderr 與錯誤不印秘密。
4. 取得 MCP `tools/list`，記錄真實 input schema與去秘密 registry keys；據此更新待核對範本與 CHANGELOG。
5. 無 token／peer 缺項／保留身份／不被 trust 的 caller均拒絕；有逾時／重啟時不自動重送未知派工。
6. 本機 fixture/unit tests 與 syntax 通過後，另行授權一次 HERMES_OK，才可把「完整 A bridge 移植」標記完成。

中介 Mac 目前未授權，不能 SSH 到該機取來源。若選原檔而無來源，保留缺口；新kit bridge可依獨立schema安裝與驗收，不能聲稱移植原檔。
