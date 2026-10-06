# 角色與可替換參數

先填 [非秘密部署計畫](../examples/deployment-plan.example.json)。這是套件規劃格式，不是 Hermes／bridge 可直接載入的設定。

| 參數／角色 | example 值 | 實際用途／核對 |
| --- | --- | --- |
| `caller_id` | `example-caller` | bridge registry 的 caller；server peer token 解析後的身份與 `trusted_peers` 必須一致。body 中的 caller 不能代替認證身份。 |
| `target_alias` | `example-target` | client registry 的節點鍵；不是 server 的安全身份。 |
| `target_identity` | `hermes-example-target` | `A2A_AGENT_NAME`、health 的 `agent`、card 的 `name`；診斷用來驗證目標。 |
| `target_hostname` | `example-hermes.example-tailnet.ts.net` | 取自新機 Tailscale 的實際完整 DNS；example 不能解析。 |
| `listen_host` | `127.0.0.1` | Hermes A2A loopback。不可改為 `0.0.0.0`。 |
| `a2a_port` | `9900` | `gateway.platforms.a2a.extra.port`／`A2A_PORT`；若已有監聽者先調查。 |
| `serve_https_port` | `10000` | A 的 tailnet TLS 入口；grants／ACL 與 registry URL 同步更新。 |
| `base_url` | `https://example-hermes.example-tailnet.ts.net:10000` | A 的 registry 覆蓋 URL；B 本機可用 `http://127.0.0.1:9900`。不含帳密／query／fragment。 |
| `hermes_data_home` | `/Users/example/.hermes` | 以新機有效 `HERMES_HOME`／profile 為準；不是 source checkout。 |
| `hermes_source` | `/path/to/hermes-source` | 用於非秘密原始碼核對；不同 installation 不一定有此資料夾。 |
| `bridge_path` | `/Users/example/.hermes-fleet/a2a_bridge.py` | A 需授權取得原程式後替換；不存在即停止 bridge 步驟。 |
| `registry_path` | `/Users/example/.hermes-fleet/agents.yaml` | 真實 registry 含 token，保持在 kit 外。 |
| `python_path` | `/path/to/bridge-venv/bin/python` | 使用取得 bridge 時驗證的 Python／依賴。 |
| `gateway_service_label` | `example.gateway.label` | 以新機正式安裝產生的 label 為準；案例 label 不可硬套。 |
| `reserved_local_identity` | `example-local-bridge` | 這只是公開規劃範例；必須在部署副本填入實際 server `security.py` 的保留身份常數。不可因新主機改名而擅改 server 的固定身份／放寬限制。它不是派工 caller。 |

每台 caller 配置獨立 token；每個 target/client 配對要確定持有的原始 token 對應同一具名 caller。複製身份表時不要複製其他機器的 token。新機改 port 必須同步 server、Serve target、URL 與測試；改 caller 必須同步 peer-token 名稱、trust 與 registry caller。

公開版省略原案例的私人保留身份字串。`REPLACE_WITH_ACTUAL_RESERVED_IDENTITY` 是格式範本占位，不是 server 可自行重命名的設定欄位；實際固定值仍須按相容來源核對。planner的`reserved_local_identity`只供拒絕誤用 caller，不會修改 server 身份常數。
