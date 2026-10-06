# 前置需求、版本與安裝來源

**繁體中文** | [English](PREREQUISITES.en.md)

## 本套件驗證範圍

2026-10-06 的 Hermes Mac 為 macOS 26.6.2、arm64。套件工具以該機 Python 3.14.5 驗證；Tailscale CLI 為 1.102.4。本機 Hermes checkout 的 `requires-python` 為 `>=3.11,<3.15`，但這不是 中介 Mac bridge 的版本需求。Hermes 已運行版本／服務 owner 與 checkout 可能不同；不可把 checkout SHA 當成 gateway 正在執行的版本。

| 元件 | 新機要求／盤點 | 來源／限制 |
| --- | --- | --- |
| Dots／ChatGPT desktop | 具備 Dots、相同帳號／workspace、允許電腦存取；記錄 app 的實際版本 | [Dots 官方文件](https://learn.chatgpt.com/docs/dots/computers-and-apps)。本套件未取得案例 app build，不能宣稱最低版本。 |
| Hermes | 安裝與 A2A schema 相容、無 Git 衝突的官方來源；先確定 profile／runtime owner | [安裝](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)、[官方 repo](https://github.com/NousResearch/hermes-agent)、[A2A](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a/)。本套件不附 Hermes 程式碼。 |
| Python | 套件工具需 3.11 以上；Hermes 依其版本的 pyproject／PM 選擇 | [Python macOS 安裝來源](https://www.python.org/downloads/macos/)。不要為套件改現有 Hermes interpreter。 |
| Tailscale | A 路徑兩端同一授權 tailnet；CLI 支援 Serve HTTPS 與背景模式 | [macOS 下載](https://tailscale.com/download/mac)、[Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve)。不要重複安裝不同 macOS distribution。 |
| stdio bridge | 自製kit bridge：Python3.11–3.14、stdlib、明確JSON schema；按Mac mini手冊隔離安裝 | mock、真loopback health/card與單次B派工通過；新硬體／原生DotsMCP未測。原案例依賴／schema仍缺。 |
| 模型供應商 | Hermes 可工作的模型連線／授權，使用者在新機親自設定 | 依 Hermes 安裝流程與供應商私密介面，不放入此專案。 |

官方 Hermes 現有安裝頁提供 macOS desktop 與 CLI；desktop macOS 套件標示 Apple Silicon。Linux、Windows、WSL 等官方支持並不等於本案 Dots × bridge × Serve 已驗證。此套件只報告本案 macOS arm64 結果；Intel Mac、Windows、Linux、容器、無桌面主機均需另外核對與完整四層驗收，不能直接照搬 launchd 命令。[官方安裝頁](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)

## 新機安裝順序

1. 先在官方來源安裝／更新 ChatGPT desktop，由使用者登入並連接 Dots 電腦。
2. 依 Hermes 官方安裝頁選擇一種安裝方法，檢查下載來源與版本。不要把安裝腳本接到本套件自動執行；新機安裝與模型授權由操作者完成。
3. A 路徑依 Tailscale macOS 官方下載安裝並由使用者登入。管理者確認 HTTPS／MagicDNS 與 caller→target:10000 的最小 grants／ACL，不配置公開 Funnel。
4. 新kit bridge依 [Mac mini流程](MAC_MINI_BRIDGE.md) 建立無pip的隔離venv；不需猜mcp/httpx依賴。若使用原案例bridge，仍須先取得來源與lockfile；新實作不能冒稱原檔。

## 唯讀盤點

```sh
sw_vers
uname -m
python3 --version
tailscale version
tailscale serve --help
hermes gateway --help
```

從 app About 記錄 desktop build；從正式安裝 owner 記錄 Hermes runtime 版本。若使用 source checkout，可本機執行 `git -C /path/to/hermes-source rev-parse HEAD`，記錄是否有未提交修改與衝突。不要分享完整 config／environment／service 輸出；其中可能含秘密。

選用 `python3 -B scripts/diagnose.py preflight --hermes-source /path/to/hermes-source` 只讀固定 A2A 原始碼檔案做 AST／衝突標記檢查，不匯入 Hermes、不讀 config 或 `.env`。它不能證明執行中的 gateway 來自該 checkout。
