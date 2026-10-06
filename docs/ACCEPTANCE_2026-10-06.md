# 0.4.0 驗收矩陣 — 2026-10-06

**繁體中文** | [English](ACCEPTANCE_2026-10-06.en.md)

**本機B路徑的真認證與單次派工已PASS。** 新版0.4 bridge經本機CLI向loopback Hermes送出唯一授權訊息，回覆原文`HERMES_OK`，HTTP200、`TASK_STATE_COMPLETED`、7.69秒。server audit與對應A2A session核對具名caller；該session工具使用為0。新硬體／新帳號部署與Dots原生MCP仍NOTTESTED。

日期均為UTC。實際接收2026-10-06 22:18:09.628、完成22:18:17.311。上午09:44的唯讀／乾淨prefix驗收與當時憑證BLOCKED，保留於[結構化證據](ACCEPTANCE_2026-10-06.json)的initial_readonly_acceptance；晚間使用者親自完成憑證交接後解決該阻礙，不能將兩個時段混為同一測試。

## 版本與環境

- kit／bridge／installer：驗收使用0.4.0來源；base Git commit `b2f4011589d40818f2eb01a75d78bd2a04dfdfa0`是先前0.3.0。驗收發生於發布前；後續0.4.0來源更新至既有公開main，exact revision見交付紀錄。
- bridge／installer實作未因本輪派工變更；安裝副本與來源SHA吻合。精確hash見[結構化證據](ACCEPTANCE_2026-10-06.json)。
- macOS26.6.2、arm64、Python3.14.5；stdlib-only、隔離venv、無pip／system-site-packages或下載依賴。
- 本機Hermes位於`http://127.0.0.1:9900`。私有個案中的主機、caller、task/context/session識別保存在本機結果紀錄與交付訊息；公開ZIP省略這些識別。

## 驗收結果

| 項目 | 狀態 | 證據與範圍 | 仍需驗收 |
| --- | --- | --- | --- |
| 0.4.0來源／版本 | PASS | 安裝副本SHA吻合；MCP serverInfo.version=0.4.0，未使用舊fleet_ask | 新機版本仍須獨立核對 |
| 同主機乾淨prefix安裝 | PASS | plan零寫入→apply、真隔離venv；重跑changed:false、config保留；暫存版uninstall與清理通過，另準備個案私人client | 不代表新硬體／新帳號 |
| CLI→真health/card | PASS | HTTP200、預期身份匹配；重啟後再次通過，card公告JSONRPC v1／bearer／loopback | GET成功本身不證明認證 |
| 本機task→標準stdio client→新bridge | PASS | initialize/initialized/tools-list/call，MCP2025-11-25、server0.4.0，只列fleet_health/card，真GET兩次200 | 未用MCP派工；不是原生DotsMCP |
| 51項mock／安裝測試 | PASS | 09:44再次通過、1.460秒；合成token、自製mock與暫存prefix，來源之後未變 | 不是Hermes完整pytest或真派工證據 |
| 使用者憑證交接／最小信任 | PASS | 使用者親自配置獨立具名peer與owner-only原始token檔；非秘密結構／權限與bridge原生validation通過。只增量加入新caller trust，保留其他YAML值與原身份限制 | 新機仍須親自交接，套件不帶秘密 |
| 必要gateway重啟 | PASS | 新鮮runtime工作總數0；批准後重啟，等待新runtime PID、loopback listener與health/card吻合。CLI回0時尚未ready，沒有盲目再重啟 | 在途／長任務與重啟查回未測 |
| 真認證／唯一HERMES_OK派工 | PASS | 一次SendMessage、HTTP200、completed、原文HERMES_OK、7.69秒；audit核對實際認證caller | 其他任務／工具／profile未測 |
| 遠端工具使用 | PASS | 對應session的tool_call_count=0、tool-role messages=0、persisted tool-call entries=0；唯讀aggregate，不複製訊息內容／工具參數 | 不代表所有工具功能已驗證 |
| 真新硬體／新帳號 | NOTTESTED | 只有已授權本機Mac及新prefix | 指定並授權其他機器後四層驗收 |
| Dots原生MCP註冊／派工 | NOTTESTED | 本輪是已連線本機task啟動CLI；stdio只驗GET。沒有新全域MCP註冊或持續權限 | 確認支持的原生連接方式與授權範圍 |
| 新bridge遠端A／C／關閉中介機／長任務 | NOTTESTED | 本輪所有bridge請求pin在loopback，沒有使用中介Mac；沒有真的關閉它來做實驗 | 各路徑與可靠查回仍須獨立驗收 |

## 單次真派工紀錄

唯一授權且實際送出的原文：

> 請只回覆 HERMES_OK，不使用工具、不修改檔案、不對外聯絡

回覆原文：`HERMES_OK`。SendMessage次數**1**，認證RPC次數**1**，重送**0**，結果未知**false**。task/context/request/session識別與實際caller已記錄於本機私有結果；公開版僅保留去識別證據。沒有引用舊A案例成功來代替這次0.4驗收。

## 認證與重啟邊界

Hermes要求Bearer認證，不要求特定的檔案儲存方式。0.4可從使用者私人原始token檔取得，或CLI `--prompt-token`隱藏輸入；stdio不提供互動prompt。本案例採使用者親自配置的檔案，未匯出server秘密或改寫舊registry。一般派工不能使用保留local-readonly身份。

非空A2A_TRUSTED_PEERS環境值會覆蓋YAML；空字串回退至YAML。本次YAML維持非空具名名單，allow-all false、loopback。不存在的sentinel會阻擋原合法caller與新增caller；不應為還原舊限制而盲目覆蓋已批准名單。保留身份仍受程式的獨立唯讀限制。

default gateway重啟影響同process平台，應先確認runtime新鮮且工作總數0；工作可能在檢查後進入，因此仍使用正常supervisor與drain，不force或all-profile重啟。回0不等於ready；先驗新PID、runtime、listener與HTTP，才派工。原Serve／Funnel沒有改動。

## 可重現與依據

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_kit.py --public
```

安裝／CLI／MCP命令見[Mac mini流程](MAC_MINI_BRIDGE.md)，更換機器依[四層驗收](VALIDATION.md)重新核對。已完成的單次驗收不應自動重播。官方Dots電腦權限與插件權限分開管理；本機CLI成功不構成原生MCP註冊證據。[Dots電腦與apps](https://learn.chatgpt.com/docs/dots/computers-and-apps)
