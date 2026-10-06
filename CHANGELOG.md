# 變更紀錄

**繁體中文** | [English](CHANGELOG.en.md)

## 0.4.0 — 2026-10-06（自製bridge與隔離安裝）

- 新增獨立stdlib CLI／stdio MCP bridge、明確JSON schema；預設health/card，SendMessage要確認，GetTask／context ListTasks只讀查詢。
- RPC前核對身份／版本／bearer公告；pinned loopback/tailnetHTTPS、TLS驗證、無redirect／proxy繼承／自動重試；已知token回顯拒絕。
- 使用者私密token檔／隱藏CLI輸入；非秘密receipt保存request/message/context/task ID與狀態，不保存訊息／回覆／token。
- 安裝器預設dry-run、明確apply/uninstall；只管理新私人prefix、無pip的venv，保留config，拒絕未知／改動／不完整prefix。
- 新增24項mock／子程序／隔離安裝測試；總51項通過。更新24組雙語文件與69檔allowlist。
- 補本輪雙語驗收矩陣／結構化證據：乾淨prefix與真Hermes CLI／標準stdio MCP health/card通過；晚間B真認證派工PASS，原生DotsMCP與新硬體／帳號NOTTESTED。
- 本版bridge／隔離安裝器與雙語驗收文件更新至既有公開GitHub main；公開內容不含秘密或私人case IDs。初次僅唯讀；後續使用者親自配置獨立peer，另批准僅新增caller trust、必要gateway重啟與一次HERMES_OK，7.69秒、0工具。

## 0.3.0 — 2026-10-06（雙語版）

- 為每份繁體中文文件加入完整英文對照與雙向語言切換。
- 範本註解與拓撲補上雙語，不改設定值、工具程式或CLI行為。
- 保持技術命令、安全界線及繁體中文HERMES_OK驗收原文一致。
- 更新檔案allowlist、交付證據與另經授權的0.2.0公開GitHub發布紀錄。
- 更新同一份Library ZIP；未部署、改服務／安全／憑證或派工。

## 0.2.0 — 2026-10-06（可公開修訂）

- 依公開發布需求移除案例機器／身份／服務識別，歷史證據保留非識別結果。
- 保留身份改為必填的非秘密規劃參數，實際值由安裝來源核對；未改server固定安全身份。
- 加入public掃描與合成個資／內網測試；未擴充登入或部署權限。
- Library ZIP以同一檔案identity更新；指定帳戶有效登入且另經授權後，安全kit已發布GitHub並核對公開visibility／main內容。

## 0.1.0 — 2026-10-06

- 建立繁中可重用專案，區分A已派工、B部分驗證與C未成功。
- 核對本機非秘密A2A原始碼、gateway parser、Tailscale CLI與官方文件。
- 提供server／trust／env片段與明示schema pending的bridge registry範本。
- 加入唯讀preflight／health／card與選用不派工auth probe、非秘密dry-run計畫、離線fixtures與tests。
- 加入GitHub-ready AGENTS入口與發布前授權界線，沒有自動部署／登入trigger。
- 交付ZIP與Library附件；沒有部署、改現有服務、安全、憑證、commit或push。

後續需授權取得bridge來源才更新其依賴／schema與完整移植驗證。新版本保留來源日期、測試與已知限制。
