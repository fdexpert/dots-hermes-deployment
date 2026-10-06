# 可公開版本檢查

**繁體中文** | [English](PUBLICATION_AUDIT.en.md)

kit 0.3.0｜2026-10-06 UTC

公開版已移除原案例的機器名稱、caller／target身份、特定服務標籤及本機執行標記中的識別。歷史紀錄僅保留架構角色、日期、平台版本、HTTP狀態、HERMES_OK、耗時與tool-call數。實際server保留身份字串不公開，部署者須從相容原始碼核對，不能據範例重新命名安全常數。

公開前掃描所有manifest檔案與ZIP，包括：憑證格式、真.env／registry、email、非example的個人home路徑、私人IPv4／tailnet DNS、UUID/thread識別、備份／日誌、symlink與額外檔案。loopback地址、禁止使用0.0.0.0的說明、官方來源URL與明顯example位置可保留。沒有內部對話、記憶或隱藏助手規則；AGENTS是專案公開部署政策。雙語版對所有英文新增檔案做同樣掃描。

首次發布從空白Git歷史建立已掃描內容的初始commit，作者／提交者使用GitHub noreply身份而非私人email；0.2.0另經授權發布至公開repo並核對遠端結果。本版修改前工作樹乾淨，新增文件與所有可發布commit內容／metadata重新檢查，ZIP排除.git。若遠端出現其他內容，必須先讀取並檢查所有將公開內容與歷史，不得只掃此套件就把無關repo公開。指定帳戶無有效登入時停止發布。

離線測試、雙語與public掃描結果見[交付驗證](DELIVERY_VALIDATION.md)。第三方來源與授權邊界見[NOTICE](NOTICE.md)。版本發布結果以push後實際遠端visibility／commit／檔案清單核對為準。
