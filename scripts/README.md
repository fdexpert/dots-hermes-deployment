# 工具與離線測試

**繁體中文** | [English](README.en.md)

只使用Python stdlib、3.11以上；不安裝dependency、不讀有效server/client config、不執行Hermes CLI。network工具只接受明確URL，不自動掃描tailnet，不發SendMessage或任何派工。

## diagnose.py

- `preflight`：OS／arch／Python與命令是否存在；未檢查service存活。可用`--hermes-source`讀固定5個A2A `.py`做AST／衝突檢查，不匯入程式。
- `health --base-url … --expected-name …`：GET `/health`，只報固定狀態／名稱匹配，不印body。
- `card --base-url … --expected-name …`：GET canonical Agent Card；核對Hermes v1 JSONRPC、bearer公告與loopback URL警告。legacy card或multi-tenant非根path需另行核對，工具不擅自擴大URL允許範圍。
- `auth … --confirm-hermes-contract`：選用安全未定義方法probe。先確認目標health→無credential拒絕→隱藏token prompt→固定未定義method回-32601，沒有task。僅可用於已核對拒絕順序且probe方法未註冊的Hermes版本。[驗收契約](../docs/VALIDATION.md)

HTTP只允許數字loopback，遠端只允許HTTPS `.ts.net`；預設timeout10秒，上限30秒、body64KiB；拒絕URL帳密/query/fragment、redirect與所有非診斷payload。停用環境proxy的自動使用；保持系統TLS驗證。拒絕任意response／exception全文輸出，避免server回顯秘密。無token命令列／環境／檔案讀取選項，不支援`.env`或registry導入。

`health`／`card`的`authentication_proven=false`是刻意保留的語意。`card.ok`仍需搭配loopback警告；遠端以registry覆蓋或支援的PUBLIC_URL解決。不把通過工具等同整套部署完成。auth可能產生rate-limit計數／audit，不能代替安全設定的本機審查；Python string無法保證記憶體抹除。

## plan.py（永遠dry-run）

```sh
python3 -B scripts/plan.py --spec examples/deployment-plan.example.json --dry-run
```

只讀kit專用非秘密JSON規劃格式；固定allowlist拒絕未知欄位（含secret欄位），不讀真配置、不產生設定檔、不呼叫部署命令、沒有apply模式。返回明確保留項目、確認與回復步驟；同輸入得到同計畫，不改寫輸入與使用者設定。部署由授權操作者按手冊增量執行。

## validate_kit.py

```sh
python3 -B scripts/validate_kit.py
python3 -B scripts/validate_kit.py --public
python3 -B scripts/validate_kit.py --zip /absolute/path/dots-hermes-deployment-kit.zip
```

檢查manifest完整／顯式檔名、symlink、禁止路徑、Python AST、JSON、Markdown內部連結與秘密模式。ZIP採相同allowlist，拒絕多餘／缺少／重複／越界項目；內容與kit逐檔比對。掃描只是輔助，不能保證所有未知秘密格式都能識別；本次來源本就不讀秘密且只納入新建檔案。

`--public`額外拒絕email、個人home路徑、私人IPv4／非example tailnet DNS與UUID。工作樹檢查忽略根目錄Git管理的`.git`metadata，以支援正常clone；ZIP永遠排除`.git`。發布前的tracked／commit歷史仍需單獨全量掃描，這個選項不代替歷史審查。

## tests

```sh
python3 -B -m unittest discover -s tests -v
```

fixtures均是新建合成資料；tests用fake transport／in-memory response，不開socket、不接真服務、不發派工。涵蓋URL拒絕、TLS/redirect政策、回應大小／語法、無body或token輸出、健康名稱、card loopback、auth拒絕順序、dry-run冪等／保留輸入／無寫入與失敗不變更、包裝／連結／秘密掃描。套件單元測試不是Hermes原完整pytest suite。
