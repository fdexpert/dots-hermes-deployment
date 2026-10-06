# 備份、還原與停機風險

**繁體中文** | [English](OPERATIONS.en.md)

kit是可分享的無秘密專案，**不是可還原現有機器的完整備份**。server秘密、client registry、模型授權、tailnet登入與 app 配對由使用者另存受控加密位置；本次未讀取或建立此類備份。

## 部署前

在受控本機記錄來源版本／安裝owner、profile／data home、原配置檔權限、service owner與Serve port/path；使用者自行備份需變動的檔案與憑證，備份不放kit或外部repo。不要將 `~/.hermes` 整個打包為部署套件；其中有對話、模型秘密、database與日誌。

## 變更窗口

gateway start/stop/restart影響同gateway的所有平台；正在等待的A2A任務可能失敗／結果未知，啟動後不自動重放。app結束／Mac睡眠會讓Dots執行器不可用。Serve停用會切斷A的新連線；不必因此停止B的本機gateway。套件只描述風險，不會做任何停機。

## 出錯回復

1. 暫停新派工，標記未完成／未知結果，避免重複送任務。
2. 本機逐項比對變更記錄，還原本次修改的非秘密欄位與原權限。由使用者處理秘密值；不能從公開kit回復舊token。
3. 如果只新增了A的Serve，且確認同port/path無其他使用者，依最初的旗標只關掉該entry，例如（原配置是本手冊的--bg／https port）：

   ```sh
   tailscale serve --bg --https=10000 off
   ```

   先核對目前CLI `off`語法與原flags，禁止全域`serve reset`。原已有此entry時應恢復原entry，不能直接off。
4. 需要重新啟動gateway才生效時，重新確認停機窗口／正式supervisor，沿原安裝owner方式處理，不啟第二個dispatcher或強制替換。
5. 重跑設定／程序／HTTP＋認證；實際派工驗收另授權一次。未知舊任務先人工查明再決定是否重啟工作。

還原乾淨來源時保留local_readonly限制與其他平台設定；不要整份覆寫安全檔或盲目`git reset --hard`。機器遷移是新部署與重新授權，不是將既有task與所有secret一起複製。
