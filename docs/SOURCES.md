# 來源、核對日期與命令依據

**繁體中文** | [English](SOURCES.en.md)

核對日期：2026-10-06 UTC。未讀取真 `.env`、client registry、憑證值或日誌全文；未SSH 中介 Mac。來源程式不打包進kit。

## 本機非秘密來源

checkout：Hermes source installation 的 `hermes-agent`。本次檢查revision `d0288be5b3330d2442e3907185b8e9d0958297bb`；該checkout的A2A tracked diff為空。這是**本次文件核對checkout**，不是2026-10-05修復當下commit，也不是gateway runtime版本保證。

| 相對路徑 | 依據 |
| --- | --- |
| `plugins/platforms/a2a/security.py` | name:token parser、env trust優先、allow-all、token映射身份、loopback、保留身份、local_bridge_only |
| `plugins/platforms/a2a/adapter.py` | port/name/public-url、GEThealth/card、POST認證→trust→method順序、timeout、gateway session |
| `plugins/platforms/a2a/protocol.py` | supportedInterfaces、JSONRPC、protocolVersion1.0、securitySchemes、-32601／-32052 |
| `plugins/platforms/a2a/__init__.py` | enabled／port啟用、platform註冊 |
| `plugins/platforms/a2a/local_readonly.py` | 固定受限路由存在；不把它移除或冒充派工 |
| `gateway/config_loader.py` | gateway.platforms嵌套平台來源、extra傳遞 |
| `hermes_cli/subcommands/gateway.py` | setup/run/install/start/status/restart parser，install --no-start-now |
| `website/docs/user-guide/messaging/a2a.md`／`pyproject.toml` | server config、A2A接口與requires-python；A2A不宣稱需要不存在的extra |

SHA256（供追溯，並非要求其他新版本完全相同）：

```text
security.py c8f89aaed3530e6a41a77ace27d91aabe07d01ab688b6bf0de69bec5e5bd1248
adapter.py  07bf49f3f7afab47ddae946c14d991dbee34574b832cf2f48667161cba67dfed
__init__.py e74718adedde494c87c53f432a676c9e827302bee9187e6856eb7a21a62524bd
local_readonly.py ffde80a9f72c4d12e2216392c23b14c832faf6db3a369bff52719f924afb3296
```

`tailscale version`=1.102.4；`tailscale serve --help`確認--bg、--https與status旗標。沒有執行serve變更命令。kit工具只用Python stdlib，沒有import Hermes或啟動其CLI。

## 官方連結

- [Dots Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)：Dots電腦授權／線上與app需求。
- [Remote connections](https://learn.chatgpt.com/docs/remote-connections)：Remote host和環境，與Dots電腦權限分別說明。
- [Tailscale userspace](https://tailscale.com/docs/concepts/userspace-networking)：proxy概念；不當成功C部署證據。
- [Tailscale Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve)：HTTPS／bg／status與針對entry off。
- [Tailscale macOS](https://tailscale.com/download/mac)：官方安裝來源。
- [Hermes安裝](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)、[A2A](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a/)、[官方原始碼](https://github.com/NousResearch/hermes-agent)。
- [Python macOS](https://www.python.org/downloads/macos/)。

官方網站會更新；部署時按相容版本與實際--help核對，不用本文件掩蓋版本差異。bridge未取得的欄位與schema明列待來源，不能用通用MCP/A2A文件推定原bridge實作。
