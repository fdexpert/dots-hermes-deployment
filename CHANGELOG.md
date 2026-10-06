# 變更紀錄

## 0.2.0 — 2026-10-06（可公開修訂）

- 依公開發布需求移除案例機器／身份／服務識別，歷史證據保留非識別結果。
- 保留身份改為必填的非秘密規劃參數，實際值由安裝來源核對；未改server固定安全身份。
- 加入public掃描與合成個資／內網測試；未擴充登入或部署權限。
- Library ZIP將以同一檔案identity更新；GitHub發布仍取決於指定帳戶的有效登入。

## 0.1.0 — 2026-10-06

- 建立繁中可重用專案，區分A已派工、B部分驗證與C未成功。
- 核對本機非秘密A2A原始碼、gateway parser、Tailscale CLI與官方文件。
- 提供server／trust／env片段與明示schema pending的bridge registry範本。
- 加入唯讀preflight／health／card與選用不派工auth probe、非秘密dry-run計畫、離線fixtures與tests。
- 加入GitHub-ready AGENTS入口與發布前授權界線，沒有自動部署／登入trigger。
- 交付ZIP與Library附件；沒有部署、改現有服務、安全、憑證、commit或push。

後續需授權取得bridge來源才更新其依賴／schema與完整移植驗證。新版本保留來源日期、測試與已知限制。
