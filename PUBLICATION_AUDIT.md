# 可公開版本檢查

kit 0.2.0｜2026-10-06 UTC

公開版已移除原案例的機器名稱、caller／target身份、特定服務標籤及本機執行標記中的識別。歷史紀錄僅保留架構角色、日期、平台版本、HTTP狀態、HERMES_OK、耗時與tool-call數。實際server保留身份字串不公開，部署者須從相容原始碼核對，不能據範例重新命名安全常數。

公開前掃描所有manifest檔案與ZIP，包括：憑證格式、真.env／registry、email、非example的個人home路徑、私人IPv4／tailnet DNS、UUID/thread識別、備份／日誌、symlink与額外檔案。loopback地址、禁止使用0.0.0.0的說明、官方來源URL与明顯example位置可保留。沒有內部對話、記憶或隱藏助手規則；AGENTS是專案公開部署政策。

公開準備掃描時，套件尚未初始化`.git`或存在既有commit歷史，沒有任何已推送歷史。首次發布只建立經掃描內容的初始commit，作者／提交者使用GitHub noreply身份而非私人email；commit前後再核對檔案與歷史。若遠端已有內容，必須先讀取並檢查所有將公開內容與歷史，不得只掃此套件就把整個既有repo公開。指定帳戶尚未有效登入時停止發布。

新建離線測試与public掃描結果見[交付驗證](DELIVERY_VALIDATION.md)。第三方來源与授權邊界見[NOTICE](NOTICE.md)。此報告不宣稱GitHub已建立、已公開或已推送；遠端結果以發布後實際visibility／commit核對為準。
