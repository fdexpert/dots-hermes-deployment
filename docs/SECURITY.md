# 安全與憑證交接

## 最小信任

- Hermes 只監聽 `127.0.0.1`；A 用 Tailscale Serve tailnet-only HTTPS 反向代理。tailnet grants／ACL 只允許所需 caller 到 target 的 HTTPS port；不要配置 Funnel、公開 ingress 或寬泛全員放行。
- `a2a.trusted_peers` 必須列具名 caller，`A2A_ALLOW_ALL_USERS=false`。所核對原始碼在 trust 為空時會接受已認證 peer，**空清單不是拒絕全部**。
- 用 `A2A_PEER_TOKENS`；不以共享 bearer／caller IP 代替具名 peer 信任。未配置 token 的 localhost-only 模式不能當成遠端認證證據；Serve 代理會從本機連入，所以啟用 Serve 前必須先完成 token／trust。
- 按實際 server 原始碼核對保留 local bridge 身份，保留它的獨立 token 與 `/local-readonly` 限制，不能用它做 general RPC 或把其他 caller 的 token 指到保留身份。公開範本的 `REPLACE_WITH_ACTUAL_RESERVED_IDENTITY` 不能直接載入。
- `local_bridge_only: true` 是限制 general surface 的模式。需要具名遠端 A2A 時，先完成獨立 peer token 與 trust，再由授權操作者將它改為 `false`，不是遇到 403 就直接放寬。
- 不使用 TLS 忽略旗標，不把憑證置於 URL、聊天、命令參數、stdout、截圖或公開文件。不開 debug HTTP tracing。

## 使用者親自配置的交接

1. 操作者確定新機／caller 與受控設定檔的位置，先建立只有擁有者可讀的秘密儲存位置（kit 之外）。
2. 由使用者在可信密碼管理工具／本機私密介面建立並放入新 token。本套件不生成、讀取、搬運或輪替現有 secret。
3. server 需要逗號分隔 `name:token` 的 `A2A_PEER_TOKENS`；每個身份有獨立值。它不是 JSON。只在本機私密編輯器中更新，保留已有合法項目。
4. client registry 的 `agents.<target_alias>.token` 放同一配對的**原始 token**，不可加 `Bearer `、不可加 `caller:`。registry 留在 kit 外，擁有者權限應為 600 或等效限制。
5. 不貼值回報；只回報「caller 已配置、trust 已核對、權限已確認」。如需認證診斷，工具用本機隱藏 prompt；若 getpass 無法隱藏輸入便拒絕。
6. 使用者自己在新機設定 Hermes 模型供應商、Tailscale 登入與 app 帳號。不要將舊機 `.env`／整個 home 搬進可分享 kit。

秘密格式只見 [增量設定說明](CONFIGURATION.md)；範本有明顯 placeholder，不能直接當可用憑證。`.gitignore` 是防誤納工具，不是秘密保管機制；本次 ZIP 另外採顯式 allowlist／內容掃描。

## 權限邊界

安裝 app、允許 Dots 電腦存取、加入 tailnet、調整 grants／HTTPS 與啟動服務均需各自授權。macOS 的檔案存取／自動化／Computer Use 權限只按任務需要開啟；純 shell／A2A 不推定需要全磁碟、螢幕或全域 automation。既有服务／安全設定／憑證不屬於本次套件建立的修改範圍。
