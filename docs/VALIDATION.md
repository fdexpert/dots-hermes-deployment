# 四層驗收矩陣

**繁體中文** | [English](VALIDATION.en.md)

| 層 | 目的 | 測法／通過條件 | 不能推論 |
| --- | --- | --- | --- |
| 1 設定 | 身份／最小信任正確 | 本機私密核對：具名 caller、獨立 peer token、非空 trust、allow-all false、loopback、無 env trust 覆寫、placeholder 全替換 | 不能證明 process 已載入新設定 |
| 2 程序 | 正確主機／版本／單一 listener | Dots task 環境正確；gateway awake／運行；lsof 確認 loopback 9900；A 的 Serve 對指定 port／target且 tailnet-only；bridge `tools/list` schema正確 | 本機 shell success 不證明 Hermes 派工 |
| 3 HTTP＋認證 | DNS/TLS/card 可達且 general RPC 認證／trust生效 | health/card 名稱吻合；card URL可達或已明確覆蓋；無認證安全 probe被拒絕；具名正確 token 的 probe回預期 method-not-found；保留身份general RPC拒絕 | GET 200 可公開取得，不足以證明身份、trust或派工 |
| 4 實際派工 | 授權路徑端到端 | 使用者另外授權後，向單一目標只傳一次下列原文；回 HERMES_OK、completed、無 tool calls並記錄耗時／狀態 | 不能推論長任務、所有工具或所有 OS 均已通過 |

## 第三層命令

在 target loopback 與 A caller 的 tailnet URL分別執行：

```sh
python3 -B scripts/diagnose.py health --base-url http://127.0.0.1:9900 --expected-name hermes-example-target
python3 -B scripts/diagnose.py card --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target
```

本機診斷遇到 card loopback URL會警告，A 必須確認 registry override或受支持的 `A2A_PUBLIC_URL`，不是追隨 card URL連到 caller 自己。

### 選用、不派工的認證 probe

先確認部署版本維持本套件 [來源紀錄](SOURCES.md) 的 `do_POST` 順序：認證 → 保留身份拒絕 → trust → 未定義方法拒絕，且方法 `DeploymentKitAuthProbe` **沒有被註冊**。在不符此契約的 server 上不可執行。

```sh
python3 -B scripts/diagnose.py auth --base-url https://example-hermes.example-tailnet.ts.net:10000 --expected-name hermes-example-target --confirm-hermes-contract
```

工具先 GET health 確認目標，再送無認證的固定 probe，必須拒絕才請操作者在隱藏 prompt輸入該 caller的原始 token。再送同一未定義方法，僅接受 HTTP200、JSON-RPC `-32601` 且匹配 request id的結果。這在已核對 Hermes 上表示認證／trust 通過後於派工 dispatch前被拒絕；沒有 SendMessage、task、工具或 callback。伺服器可能計入 rate limit／audit；不是零副作用。其他版本只回「不符合契約」，不猜原因或重試。

保留身份驗證須由具該權限的操作者另次執行，不把它當部署caller；預期失敗403。測試不需對錯誤身份自動派工。

## 第四層：僅一次原文

> 請只回覆 HERMES_OK，不使用工具、不修改檔案、不對外聯絡

兩個語言版本均使用上方繁體中文作為唯一驗收輸入；英文版另附意思說明，不替換原文。

透過經核對 schema的 `fleet_ask`／本機 client，由操作者另外授權。預設腳本不提供此功能。本次建立文檔沒有派工驗證。

去秘密紀錄：日期、A/B、版本／caller與target 的自定匿名標籤、HTTP狀態、completed、原文結果、秒數、tool-call數。不要附 token、完整registry、任務輸入歷史或日誌。300秒逾時／連線中斷結果未知：保留本機task參照，先人工查 server／client狀態，不重送；未取得完整查回工具時標為待確認。

B 仍需未完成兩項：本機 Hermes派工；在明確授權且評估其他使用者影響後，讓 中介 Mac 不參與再驗證獨立性。不要為這份文件關掉原服務。
