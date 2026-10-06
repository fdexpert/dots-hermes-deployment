# GitHub與未來dot入口

**繁體中文** | [English](GITHUB.en.md)

此專案可放在GitHub供dot取得步驟與工具，但「登入dot」不會自動部署。新主機仍須連接適合的Mac執行器、授權檔案／服務操作、盤點相容版本，並由使用者親自配置憑證。入口是 [AGENTS.md](../AGENTS.md) 與 [README](../README.md)。

首次發布前需使用者確認GitHub owner/login、repo名稱與可見性。提供email不能確定GitHub帳號；應經正常認證唯讀查核login，email隱藏時不可假稱已比對。ZIP不包含個人GitHub登入資訊、已配置git remote或現有git設定。0.2.0已另經授權公開發布，見[已驗證紀錄](VERIFIED_RECORD.md)。

## 建議未來交給dot的要求

```text
請在我已連接並授權的指定Mac，使用此repo的Dots × Hermes套件準備部署。
先讀AGENTS.md，確認A或B、實際主機與參數，做唯讀preflight與離線測試。
先提出增量變更計畫、dry-run、秘密交接與停機／回復步驟。
需要新增服務或安全設定變更時，依既有授權範圍取得確認後才執行。
不要複製舊秘密，不自動派工；完整bridge未取得時明列缺口。
```

## 發布時的人工檢查

- 檢查git diff與所有待stage檔；不要`git add`整個任務工作目錄。
- 只將`dots-hermes-deployment-kit`的安全內容作repo root；真秘密／部署副本在repo外。
- 跑離線測試、內部links／syntax／內容掃描與ZIP掃描；確認來源／版本文件。
- 確認目的帳號、repo名稱與授權可見性後才建立／commit／push。公開前掃描所有待發布內容與可推送歷史；既有repo有無關內容或未確認敏感項就停止公開。
- 不設GitHub Actions自動部署、不放repository secret／PAT、SSH key或tailnet key。

任何repo都不是secret vault。dry-run planner僅輸出計畫、不執行、讀取或重寫實際使用者配置。[部署步驟](DEPLOYMENT.md)
