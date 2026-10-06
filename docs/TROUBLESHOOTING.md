# 故障排查

| 症狀 | 核對順序 | 安全處置 |
| --- | --- | --- |
| Connection refused | task 是否跑在正確機器；loopback 9900是否監聽；gateway/profile／port；Serve target | 先做唯讀診斷；不改0.0.0.0、不kill未知程序、不盲目重啟。 |
| health/card/RPC 403 或 `only /local-readonly is available` | local_bridge_only、部署版本GET/POST 行為、使用的token是否保留身份 | 核對安全契約；完成具名token/trust交接並授權後才改模式；不移除local_readonly。 |
| RPC401 | peer-token name:token格式、client原始token、啟動profile/secret來源、server是否重載 | 使用者本機核對；不貼token、不加Bearer到registry值。 |
| RPC403 peer not trusted | 認證映射的caller是否在trust；保留身份限制；env覆寫 | 不開allow_all_users；保留身份改用合法獨立caller credential。 |
| peer缺項／找不到 target | registry target alias、必需欄位、caller_id、URL與token | 取得原loader／schema；無來源就停止bridge步驟，不猜鍵名。 |
| YAML改了trust仍錯 | A2A_TRUSTED_PEERS非空環境覆寫、launchd／shell／profile來源、服務啟動時擷取 | 只由使用者本機檢查；保留一個權威來源並規劃重啟，避免印整份env。 |
| Git衝突或SyntaxError | 固定A2A py檔衝突標記／syntax、相容來源與local-readonly客製 | 優先乾淨相容版本；逐塊合併與安全測試，不盲選ours/theirs，不套用案例修復到所有新機。 |
| stdio工具沒出現／HTTP MCP失敗 | MCP client是否啟動Python stdio bridge、cwd／依賴、tools/list | Dots電腦連線不會自動註冊bridge；Serve是A2A，非MCP。 |
| Agent Card URL是127.0.0.1 | A的registry URLoverride是否正確；版本是否支援A2A_PUBLIC_URL | 不讓遠端client照card連caller自身；增量更新公告URL並驗證TLS，不假設通用client會覆蓋。 |
| TLS／DNS錯誤 | .ts.net完整DNS、tailnet登入、HTTPS授權／憑證、port ACL | 不用-k或insecure；修正實際路由／官方HTTPS配置，先做授權確認。 |
| fleet_ask約300秒逾時 | server是否仍執行、是否有已知task參照、bridge是否有查回 | 結果未知不重送；伺服器有GetTask不代表bridge已有可用查回。 |
| B顯示offline／無法續作 | Hermes Mac醒著、網路、ChatGPT app、Dots自己的電腦權限 | 恢復可用狀態；新連線／切換電腦不會搬遷原task。 |

目前checkout的local_bridge_only對GET回403，但POST可能先因認證回401；案例觀察曾全403。這是版本／修復狀態差異，應看語意與實際原始碼，不能只依單一status猜設定。[來源與日期](SOURCES.md)

不要附完整日誌作回報。先在本機確認錯誤類別與必要行號，再摘錄去秘密短句；診斷工具只輸出固定欄位，不印任意response或exception內容。
