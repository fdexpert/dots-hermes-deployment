# 部署檢查表

**繁體中文** | [English](DEPLOYMENT_CHECKLIST.en.md)

日期：______　操作者：______　新機匿名代號：______　路徑：A / B　kit版本：______

- [ ] 指定主機已授權且執行環境正確；確認dot登入不等於部署授權。
- [ ] 已記錄OS／架構／app／Hermes runtime owner／版本／Tailscale版本。
- [ ] 來源相容無衝突；local-readonly安全客製與固定身份限制已核對。
- [ ] 非秘密參數完成，所有example／REPLACE_已在部署副本中替換。
- [ ] dry-run變更計畫已審閱；既有正常route／其他平台保留，停機／回復已規劃。
- [ ] 必要服務／安全／route變更在授權範圍內，未授權項已確認。
- [ ] 使用者親自配置新peer token／模型／tailnet／app授權；秘密在kit與repo之外。
- [ ] 具名caller與trust一致、allow-all false、無env trust覆寫、保留身份token獨立。
- [ ] 9900只監聽loopback且只有一個正確gateway；沒有強制啟第二個dispatcher。
- [ ] A：Serve tailnet-only HTTPS10000→loopback9900、ACL最小化、未啟Funnel、其他entry未動。
- [ ] 選新kit bridge或原案例bridge並記錄。新kit plan/apply／隔離測試／config／手動client設定完成；原檔選項仍須來源／lockfile／loader／schema。
- [ ] B：Dots直接新task確實在target；target醒著、網路與app可用。
- [ ] 設定層驗收通過。
- [ ] 程序層驗收通過。
- [ ] HTTP/card/TLS與認證層驗收通過；GET200不當認證證據；card loopback已處理。
- [ ] 另獲授權後單次HERMES_OK原文驗收通過，0 tool calls；無未知結果重送。
- [ ] B：本機Hermes派工與中介 Mac不參與驗收有證據，否則仍標未驗證。
- [ ] 去秘密結果／變更／回復計畫已保存，秘密備份另由使用者保管。
- [ ] 若發布GitHub：owner/repo/visibility已授權；公開前全部檔案與可推送歷史已去識別／掃描，僅安全kit內容；無自動部署trigger。

未完成／blocker：______　下一步與負責人：______
