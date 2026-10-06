# 給在此專案工作的 dot／agent

**繁體中文** | [English](AGENTS.en.md)

這是含自製bridge與隔離安裝器的部署套件，本機B單次驗收已有紀錄，不代表其他新機已安裝或通過派工。先讀docs/MAC_MINI_BRIDGE.md。先讀README、docs/VERIFIED_RECORD.md、docs/BRIDGE_CONTRACT.md或其英文版。依使用者選擇的繁體中文或英文回報。

## 部署入口

只有使用者**明確要求在指定主機部署**，且該主機已連接／授權，才能開始部署。登入dot／打開repo不是自動執行授權。不得設置常駐登入觸發、GitHub Actions遠端部署、自動認證、憑證同步或預設派工。

1. 核對主機與cwd，唯讀盤點版本／來源／listener／既有route；執行kit離線測試與`diagnose.py preflight`。
2. 確認A或B、參數、profile、新kit bridge或原案例bridge與授權範圍。C未驗證。新程式是獨立實作；原案例來源仍缺，不能宣稱移植原檔。
3. 以`examples/deployment-plan.example.json`及`scripts/plan.py`產出**非秘密、無寫入dry-run變更計畫**；明列現有route／設定需要保留項目、步驟、停機與回復。該planner不能讀真config，也不能代替實際盤點。
4. 完成具體可審閱計畫後，對未曾授權的服務／安全設定變更、停機或route替換取得明確確認；已授權範圍不重複詢問。未獲授權只做獨立唯讀／離線工作。
5. secret全部由使用者在可信本機私密介面配置；不讀／複製舊`.env`、真registry或token到repo、不要求在聊天／命令參數貼token、不自動生成／搬運secret。
6. 隔離安裝依docs/MAC_MINI_BRIDGE.md先plan，再明確apply至已授權新prefix。不可改未知config、全域環境或常駐權限。server由操作者按docs/DEPLOYMENT.md逐項增量操作。保留其他平台／trust／Serve／Funnel；不整份覆寫、不reset、不盲選git ours/theirs，不開Funnel／allow-all／0.0.0.0或忽略TLS。
7. 四層驗收：前3層可在授權範圍做安全探測；實際派工另外獲授權才送一次指定HERMES_OK原文。結果未知不重送。B本機CLI單次派工已有紀錄；新機、原生DotsMCP及關閉中介Mac的實驗仍須獨立驗收。
8. 留去秘密變更紀錄與結果，移交kit；故障先停新派工、依原owner回復本次變更，不修改真實服務來測試腳本。新增測試只能使用自製loopback mock／合成credential／暫存prefix並清理。原51tests含隔離CLI/MCP與安裝生命週期，不是正式派工證據。

## 本專案修改與發布

新工具預設唯讀／dry-run；新增任何可寫部署工具前需涵蓋冪等、dry-run、保留使用者設定、失敗回復與離線fake runner測試，禁止用現有服務做測試。不寫自動修security腳本。

先跑`python3 -B -m unittest discover -s tests -v`及`python3 -B scripts/validate_kit.py`。套件ZIP採顯式allowlist與秘密掃描；不要打包真`.env`、registry、`.git`、備份、日誌或Library helper。

GitHub發布須使用者確認owner/repo與visibility。email不是GitHub login。只有已獲授權且全量內容／歷史掃描乾淨時才公開；既有repo含無關內容或可疑歷史就停止公開，不擴大本套件的發布範圍。本套件無CI部署hook與自動secret讀取流程。
