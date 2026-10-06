# 已驗證部署紀錄與未驗證清單

**繁體中文** | [English](VERIFIED_RECORD.en.md)

日期均為UTC。公開版只保存去識別摘要；「中介 Mac／Hermes Mac」是通用角色，原機器名稱、身份、服務標籤與本機執行標記中的識別已省略，不是新部署預設值。

| 日期 | 證據／結果 | 範圍 |
| --- | --- | --- |
| 2026-10-05～06 | 中介 Mac 的Python stdio MCP bridge與agents registry，caller=中介 Mac、node=Hermes Mac；曾存在到target的SSH維運路徑 | 原bridge未取得；當時只在Claude Desktop／Code登錄，未作Dots全域MCP註冊。 |
| 2026-10-05 | security.py＋adapter.py共12衝突塊修復，保留安全與local_readonly；6檔語法＋5聚焦安全測試通過 | 當次沒pytest，未跑完整套件、未commit/push；不是所有新部署的前置修復。 |
| 2026-10-05～06 | gateway服務；loopback9900；Serve tailnet-only HTTPS10000→127.0.0.1:9900 | 其他Serve/Funnel未動；本套件未修改。 |
| 2026-10-05～06 | 原local_bridge_only:true造成general路由only/local-readonly拒絕；使用者親自配置caller credential後trust列具名caller、local_bridge_only:false；去除.env過期trust覆寫 | token值不保存；保留原server的local bridge身份獨立限制，公開版省略固定身份字串。 |
| 2026-10-06 06:33 | A單次指定原文回HERMES_OK，8.8秒、HTTP200、TASK_STATE_COMPLETED、遠端0 tool calls | 完成一次A派工；不保存task ID，不能推出未知任務查回已完成。 |
| 2026-10-06 | Hermes Mac：macOS26.6.2 arm64；獨立Dots本機task回固定執行標記、exit0；health/card200且identity吻合（原標記與identity中的識別已省略） | B電腦直連／HTTP已驗證；未測本機Hermes派工，未真正關中介 Mac再測。 |
| 2026-10-06 | 原card宣告loopback；A bridge用registry HTTPS覆蓋 | 通用A2A client不一定自動覆蓋。 |
| 2026-10-06（本套件） | 非秘密checkout原始碼核對、Python/Tailscale盤點、新增套件離線驗證 | 未連線派工／修改服務；詳見SOURCES與DELIVERY_VALIDATION。 |
| 2026-10-06（0.2.0發布） | 去識別kit另經授權發布至公開GitHub；已核對遠端visibility、main commit與38檔tree | 只發布套件來源，未部署／配置憑證或新增Hermes驗收。 |
| 2026-10-06（0.3.0雙語版） | 每份文件加入完整英文對照、雙語導覽／範本註解與離線／包裝檢查 | 文件更新，技術命令與runtime行為不變；見[交付驗證](../DELIVERY_VALIDATION.md)。 |
| 2026-10-06（0.4.0實作） | 自製CLI/MCP對自製mock、真venv暫存prefix安裝／冪等／config保留／rollback/uninstall，51tests通過 | 新bridge未對真Hermes派工，未整合真Dots MCP client；其他新硬體／帳號待驗收，當時未commit/push。 |
| 2026-10-06 09:44（0.4.0驗收） | 同主機乾淨prefix plan/apply／重跑／卸載通過；新bridge CLI與標準stdio MCP對真Hermes health/card均HTTP200、身份吻合；51tests再次通過 | 真認證／單次派工因未確認相容憑證BLOCKED；原生Dots MCP註冊BLOCKED。未送真訊息、未改既有服務，非新硬體／帳號；見[驗收矩陣](ACCEPTANCE_2026-10-06.md)。 |

| 2026-10-06 22:18（0.4.0 B真派工） | 使用者親自交接獨立具名credential；僅新增caller trust、idle工作0後重啟，CLI→loopback Hermes一次SendMessage回HERMES_OK，HTTP200／TASK_STATE_COMPLETED、7.69秒；audit與session核對caller，保存工具呼叫0 | 不經中介Mac；新硬體／帳號、原生DotsMCP、關中介機與長任務未測。私有case IDs留本機，公開ZIP去識別，驗收時尚未commit/push；見[矩陣](ACCEPTANCE_2026-10-06.md)。 |

| 2026-10-06（0.4.0公開更新） | 新bridge／隔離安裝器、24組雙語文件與已完成B驗收去識別證據更新至既有公開main；69檔allowlist，發布前離線／語法／雙語／秘密掃描 | 只更新本套件來源，無新派工／server變更；新硬體／帳號與原生DotsMCP仍未測。exact commit及CI由交付紀錄核對。 |

## 尚未驗證

- 完整中介 Mac bridge的來源、依賴、registry loader、MCP input schema與移植後端到端結果。
- B實際關閉中介Mac的實驗；單次本機CLI派工已通過且未使用中介機。
- 原生DotsMCP註冊／派工，以及每台新硬體／帳號；本機CLI單次真認證派工已通過，不能代替其他部署。
- 雲端C的持久runtime/socket/egress可行性；曾評估但未成功。
- Linux／Windows／Intel Mac／其他OS或架構的整套部署。
- 長任務、所有工具、複合profile、多caller、服務重啟後task恢復與完整pytest suite。
- fleet_ask逾時後可靠查回／去重；server GetTask存在不等於bridge已提供此流程。
- Dots app的固定最低build。本套件不承諾只登入dot就無人值守部署。

既有紀錄與目前原始碼觀察分開；本次沒有重演原A修復／派工；新增B證據獨立列日期，不用舊成功代替新驗收。[原始碼來源](SOURCES.md)
