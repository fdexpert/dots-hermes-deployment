# 非秘密設定與增量更新

## 分開配置

| 範本 | 性質 | 放置／更新方式 |
| --- | --- | --- |
| [server config](../examples/server-config.fragment.example.yaml) | 真實 Hermes 欄位的片段 | 在新機有效 config 只合併 `gateway.platforms.a2a`，保留其他平台。 |
| [server trust](../examples/server-trust.fragment.example.yaml) | 所核對 security.py 的真實 trust 欄位 | 只更新頂層 `a2a.trusted_peers`／`local_bridge_only`；保留其他 `a2a` 欄位。 |
| [非秘密環境設定](../examples/server-env.example.txt) | 真實環境變數名稱的範本 | 使用者在新機私密設定來源增量加入；不是完整 `.env`。 |
| [peer token 格式](../examples/peer-token-format.example.txt) | 格式示意，非有效 secret | 不直接載入。由使用者在 kit 外配置；不覆蓋已有 peer。 |
| [client registry](../examples/client-agents.schema-pending.example.yaml) | 部分案例已知欄位；完整 schema 待來源 | 只證實 `caller_id` 與 `agents.<alias>.token` 的意義；`url` loader 尚未取得，不能直接當原 bridge 設定。 |

## 語意與優先序

所核對 `security.py`：`A2A_PEER_TOKENS` 用逗號切項、首個冒號分隔 name/token。身份不應含冒號／逗號；token 避免逗號及空白，禁止重用同值給多個身份。檔案不提供有效 token。

`A2A_TRUSTED_PEERS` 非空時優先於 YAML `a2a.trusted_peers`。即使 `.env` 中只有一個過期的非秘密占位值，也會覆蓋 YAML。請使用者在**本機**檢查 launchd／shell／profile／`.env` 的同名來源，只保留一個明確 trust 權威；不要輸出整份 environment。案例移除過期覆寫並由 YAML 管理，套件沒有自動修改腳本。

port 的非空 `A2A_PORT` 優先於 `extra.port`。`A2A_HOST` 預設 loopback；本套件明確維持 `127.0.0.1`。`A2A_AGENT_NAME` 是 card 身份顯示名稱。`A2A_PUBLIC_URL` 可指定 card 的可達 URL，需此版本支援並經核對；它不會替你建立路由或授權。

`local_bridge_only: false` 不取消保留身份限制。只要 token 映射到實際 server 的保留 local bridge 身份，general RPC 仍拒絕。公開版不刊出原案例的私人身份字串；先核對相容來源的固定常數。不要移除 `local_readonly.py` 或把保留身份改成全權 caller。

## 安全增量流程

1. 使用者在受控本機備份有效配置／權限，不上傳秘密備份。
2. 對照正式版本 loader，確定正在使用的 profile／`HERMES_HOME`，不同安裝不可猜 config 路徑。
3. 在私密編輯器逐項合併所需欄位，保留其他平台、模型、工具、serve 與 peer。範本不是整份 config，禁止 `cp fragment config.yaml`。
4. 檢查重複 YAML keys、縮排、型別（布林不是任意字串）、peer 名稱對應與端口優先序。使用正式設定載入器的本機驗證方式，避免公開 config 輸出。
5. 只在已規劃停機窗口重啟新機 gateway。設定擷取於 adapter 啟動，改檔不保證立刻生效。[停機與回復](OPERATIONS.md)

不得為排解 Git 衝突盲選整份 `ours`／`theirs`，也不把案例十二衝突修復當標準安裝步驟。新機優先取得無衝突且相容來源；需要合併時按安全行為逐塊審查與測試。
