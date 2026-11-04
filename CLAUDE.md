# 計算機組織 — 出題用 repo

這個 repo 放上課簡報（根目錄的 `Chapter X-Y.ppt`）、老師的練習卷和考卷模板。簡報已經轉好，**出題時不要再轉檔**，直接讀 `materials/`。

## 教材在哪裡

- `materials/INDEX.md`：先讀這個。各節主題、投影片標題、Quick Questions／Exercises 在第幾張，以及課程慣例（EPC、ALU control、哪些沒教）。
- `materials/md/ChX-Y.md`：每份簡報的逐張文字。
- `materials/pdf/ChX-Y.pdf`：每份簡報的逐頁圖，頁碼 = 投影片編號。md 裡標「［圖：見 PDF 第 N 頁］」或需要看 datapath／pipeline 圖時，用 Read 讀該 PDF 的 `pages: "N"`。
- `materials/md/Midterm-Practice.md`：老師的期中練習卷（題目 + 解答），出題風格以它為準。

## 出題流程

1. 讀 `materials/INDEX.md` 決定範圍；範圍以簡報實際教的為準，沒教的（例如 hazard）不要出。
2. 題型仿 `materials/md/Midterm-Practice.md`：英文題目、(a)(b)(c) 小題、計算與追蹤為主；數字和情境要換過，不能照抄練習卷或簡報的 Exercise。
3. 用小程式驗算所有數字（CPI、機器碼、offset、pipeline cycle 等）。
4. 輸出：複製 `模板.html`，只改其中「設定區」的 CONFIG 和 QUESTIONS，照模板開頭註解的規則寫（答案只寫得分要點）。範例成品：`期中模擬考.html`。

## 新增簡報時

把新的 `Chapter X-Y.ppt(x)` 放到根目錄後執行：

```bash
bash materials/tools/convert.sh "Chapter X-Y.ppt"
```

再把該節的主題摘要補進 `materials/tools/build_index.py` 的 `TOPICS`，重跑一次 `python3 materials/tools/build_index.py materials/md materials/INDEX.md`。
