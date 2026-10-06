# 架構與角色

**繁體中文** | [English](ARCHITECTURE.en.md)

## A：中介 Mac 與遠端 Hermes

```text
Dots（協調工作）
  └─ 連接電腦權限 → example-caller Mac（案例：中介 Mac）
       └─ 本機 task 的 MCP client → Python stdio a2a_bridge.py
            └─ agents registry 指定 HTTPS URL + 原始 peer token
                 └─ tailnet-only Serve :10000（Hermes 主機）
                      └─ HTTP 127.0.0.1:9900 → Hermes A2A → gateway session
```

Dots 電腦連線、stdio MCP、A2A HTTP 是三個不同介面。stdio 由 client 啟動子程序並使用 stdin/stdout 通訊；不能把 `.py` 路徑或 Serve URL 填入另一種 transport 並期待相容。案例 bridge 曾在 Claude Desktop／Code 登錄；未作 Dots 全域 MCP 註冊，實際由本機 task 調用 `fleet_ask`。未取得來源前，無法保證新的 Dots task 已具備同一 MCP client／工具。

案例曾有中介機到 Hermes 主機的 SSH，供維運；它不是上述已驗證 A2A HTTPS 派工的替代入口。部署 HTTPS 路徑不要求另開 SSH。若管理需要 SSH，獨立授權、核對 host key、使用具名帳號，不借未授權主機取檔。

## B：直接連接 Hermes Mac

```text
Dots → example-target Mac 的已授權執行器
         ├─ 本機命令：證明執行位置
         └─ 經另行取得／驗證的本機 A2A client
              → HTTP 127.0.0.1:9900 → Hermes gateway
```

B 不需要 中介 Mac。只使用本機 A2A 時也不需要 Serve；若另有遠端 caller 才另外配置 tailnet Serve。直接執行 shell 成功不表示已向 Hermes agent 派工。本套件 `diagnose.py` 不是本機派工 client，也不提供 `fleet_ask`。

## C：曾評估、未成功

userspace Tailscale 可透過 SOCKS5／HTTP proxy 提供網路，不代表雲端執行器允許 daemon/socket、對外 egress 或持久 process／state。本案例無成功端到端驗證，因此不提供 C 的啟動腳本、不把代理設定視為通用部署解法。[官方 userspace 概念](https://tailscale.com/docs/concepts/userspace-networking)

## 連接電腦的選擇

依 Dots profile → Computers → Your computer → Allow access 完成使用者確認。官方當前說明只可連接一台個人電腦；雲端電腦仍保持連接。切換可能替換個人電腦選擇。既有 task 留在原執行環境；新建獨立 task，確認其實際 cwd／OS／host，再測 B。不要把 Codex Remote 配對流程當成 Dots 的電腦權限流程。[Dots 官方流程](https://learn.chatgpt.com/docs/dots/computers-and-apps)、[Remote 官方說明](https://learn.chatgpt.com/docs/remote-connections)
