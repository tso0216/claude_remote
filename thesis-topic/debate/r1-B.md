# 立場 B「群體軌跡派」第一回合立論

**查證方式**：這個 sandbox 不讓 WebFetch／curl 直接連 arxiv.org、sites.google.com、ptt.cc、figshare、data.gov.tw、huggingface.co（連線被拒或 ENOTFOUND）。所以文獻和多數來源是用 WebSearch 結果查證的。GitHub raw 可以直接連，tour-cikm16、Massive-STEPS、TourismQA 我讀的是 README 原文，tour-cikm16 另外下載資料實際算過。
標記：✔＝已查證；△＝確認存在，但授權或細節沒查到；✘＝未查證。

## 1. 題目與主張
- 中：**從網路群體軌跡回答旅客時空問題——京都旅客軌跡庫與可驗證問答基準**
- 英：**CrowdTraj-QA: Answering Travelers' Spatio-Temporal Questions with Crowd Trajectories Mined from Web Photos and Travelogues**
- 一句話主張：旅客最常問的「要待多久、幾點人少、看完接著去哪、我的行程排得完嗎」，本質上是**群體行為的統計量**，地圖和知識庫裡沒有這種資料。Google 的熱門時段和停留時間，就是從使用者自願開啟的定位紀錄匯總算出來的（[官方說明](https://support.google.com/business/answer/6263531)），但不開放。本論文用開放的網路資料重建這一層，並把答案做成程式能重算、附樣本數 n 和信賴區間 CI 的標準答案。

## 2. 研究問題與貢獻
1. **軌跡重建**：從 CC 授權照片的 metadata 和遊記，重建「旅客」的軌跡。要處理的問題有：居民混在裡面、少數人上傳量特別大、只拍一張照片的造訪、相機時鐘錯誤。停留時間用區間設限（interval-censoring）估計，並量化 LLM 從遊記抽軌跡的誤差。
2. **可驗證基準**：8 類互斥、經頻率驗證的題型。每題的答案由程式從軌跡庫算出，附 n、bootstrap CI 和資料期間。用「統計可答性過濾」刪掉答案不穩定的題目。
3. **系統**：比較「軌跡統計工具＋LLM」的代理，是否勝過 closed-book、文本 RAG、地圖／知識庫工具，以及把原始軌跡直接塞進 prompt。也評估模型在證據不足時，會不會改給區間或拒答。

## 3. 資料集設計
**地區**：主體是京都市；跨城泛化用大阪；台北放第二階段。理由如下：
- 京都的景點以觀光客為主，而且擁擠問題嚴重。2024 年觀光客 5,606 萬人，其中外國人 1,088 萬（[京都市 R6 報告](https://www.city.kyoto.lg.jp/sankan/cmsfiles/contents/0000341/341863/R6hodo.pdf)）。
- 2024 年台灣旅客訪日 604.4 萬人次（[JNTO 數據](https://honichi.com/news/2025/02/26/inbound-taiwan-2024)），繁中提問量大。題目以繁中為主，另附英文平行子集。
- 京都已有用 Flickr 照片研究旅客的先例：
  - [Hidaka & Isoda 2010](https://gisa-japan.org/content/files/conferences/proceedings/2010cd/papers/3F-2.pdf) 用官方統計驗證照片推估的旅客分布。
  - [Togiya et al. 2023](https://a-a-r-s.org/proceeding/ACRS2023/Spatial%20Information%20Sciences/ACRS2023147.pdf) 區分了居民、國內旅客和外國旅客。
- 京都還有獨立的外部驗證來源：京都観光快適度マップ（見第 4 節來源表）。
- 其他候選地區的問題：
  - 東京的 Foursquare 資料以居民通勤為主，Massive-STEPS 的東京子集只有 764 位使用者。
  - 台北有捷運分時 OD，但不分旅客和居民；旅客層級的開放軌跡很少。

**資料層次**：
- **L0 地名庫（gazetteer）**：OSM 多邊形和 opening_hours、Wikidata QID（中日英名稱）、FSQ 類別。
- **L1 原始觀測**：
  - YFCC（2004–2014）
  - Flickr API（2015–2026）
  - 遊記（2019，以及 2023–2026）
- **L2 造訪與旅遊日**：
  - 照片落在 POI 多邊形內就算造訪；沒有多邊形的 POI 用 150 m 半徑。
  - 同一天、間隔小於 8 小時的造訪算同一段（沿用 Lim 2015 和 Semantic Trails 的做法）。
  - 判定為旅客的條件：在京阪活動跨度少於 21 天，且主要拍攝地不在京阪。這是本研究自訂的規則，之後用遊記自述的居住地校驗。
- **L3 統計 cube**：POI×季節×星期×時段的造訪量、轉移矩陣、區域內的常見序列。
  - 一律以「每位旅客每天」（user-day）為計數單位，避免上傳量大的少數人主導結果。
  - 每格都附 n，以及按旅客重抽樣的 bootstrap CI。
- **L4 QA**：模板產生題目，LLM 改寫，人工審自然度。答案由程式從 L3 算出，每題記錄有效期間和資料來源組成。

**規模目標**：
- 京都 POI（至少 30 個 user-day）150–250 個。這個數字還沒實算，第 1 個月用 YFCC 算出來。
- 遊記 2,000–3,000 篇。
- QA 3,000–4,000 題，外加 300 題由真實提問改寫的測試集。
- 主測試集用 2015 年以後的資料算答案；YFCC 時期另外做成「時效漂移子集」。

**Pilot（本回合實算，資料是 [tour-cikm16](https://github.com/computationalmedia/tour-cikm16) 公開的 Flickr 軌跡）**：

| 城市 | 使用者 | 只有一張照片的造訪 | 至少 30 人造訪的 POI | 「下一站」有明確答案的錨點* |
|---|---|---|---|---|
| 大阪 | 450 | 50% | 11/27 | 1/2 |
| 愛丁堡 | 1,454 | 53% | 25/28 | 11/19 |
| 多倫多 | 1,395 | 56% | 24/29 | 9/16 |

\*條件：從該錨點出發的轉移至少 30 次，且第一名次數至少是第二名的 1.5 倍。

其他發現：
- 時間戳最早出現 1864 年。
- 大阪的檔案裡混進一個東京座標的 POI，有 72 位使用者。
- 大阪城公園停留中位數 35.5 分鐘，但 80% CI 是 20.7–53.9 分鐘，跨了兩個時長區間。
- USJ 的照片跨度中位數只有 4.4 小時。照片跨度只是停留時間的下界。

結論：現成整理好的資料集太小，偏差也確實存在。所以必須從 YFCC 全量加上新資料自己建，並做可答性過濾和停留時間校正。這正是本論文的方法貢獻，不是致命傷。

## 4. 資料來源表

### 知識／資料來源

| 來源 | 內容／欄位 | 範圍 | 取得方式 | 授權／再散布 | 限制 | 查證 |
|---|---|---|---|---|---|---|
| YFCC100M（[arXiv:1503.01817](https://arxiv.org/abs/1503.01817)、[AWS](https://registry.opendata.aws/multimedia-commons)） | photo ID、user、拍攝與上傳時間、經緯度、定位精度、tags、CC 授權類型 | 全球 2004–2014，約 4,800 萬筆有座標 | S3 下載 metadata（61.1 GiB SQLite，可用 [yfcc100m](https://pypi.org/project/yfcc100m/) 工具）；大量下載需 AWS 帳號 | 每張照片各自 CC（含 NC）；釋出 photo ID 和衍生統計 | 資料舊；攝影者偏差 | ✔ |
| Flickr API（[ToS](https://www.flickr.com/services/api/tos/)） | photos.search（bbox、min_taken_date、geo、date_taken、owner） | 2015–2026 | API；2025 年起 key 只開放給付費 Pro 帳號（[Flickr Help](https://www.flickrhelp.com/hc/en-us/articles/4404070036884-Flickr-API)） | ToS 限制長期快取 → 只存 ID 和匯總結果 | 近年上傳量可能不足；Pro 價格未查 | ✔／△ |
| [tour-cikm16](https://github.com/computationalmedia/tour-cikm16) | userID、trajID、poiID、startTime、endTime、照片數、poiDuration | 大阪、多倫多、愛丁堡、格拉斯哥、墨爾本（源自 YFCC） | 直接下載 | 沒有 LICENSE 檔，README 要求引用論文 | 規模小 | ✔（已實算） |
| Foursquare Global-scale Check-in（Yang，[頁面](https://sites.google.com/site/yangdingqi/home/foursquare-dataset)） | 3,328 萬筆打卡、26.7 萬使用者、415 城 | 2012/04–2013/09 | 下載 | 沒看到授權，只要求引用 | 京都是否在 415 城內未查證 | △ |
| Massive-STEPS（[arXiv:2505.11239](https://arxiv.org/abs/2505.11239)、[GitHub](https://github.com/cruiseresearchgroup/Massive-STEPS)） | 15 城的打卡軌跡 | 2012–13、2017–18；日本只有東京（764 使用者、13,839 筆），沒有京都、大阪、台北 | Hugging Face | Apache-2.0 | 只能當東京的對照 | ✔ |
| [FSQ OS Places](https://huggingface.co/datasets/foursquare/fsq-os-places) | POI 名稱、類別、座標 | 全球 | Hugging Face（需同意分享聯絡資訊） | Apache-2.0 | 沒有造訪紀錄 | ✔ |
| OSM（ODbL）／Wikidata（CC0）／[Wikivoyage Kyoto/Higashiyama](https://en.wikivoyage.org/wiki/Kyoto/Higashiyama)（CC BY-SA） | POI 多邊形和營業時間；多語名稱；專家建議路線（給 G5 當「專家 vs 群體」對照） | 全球 | dump／API | 可再散布；ODbL 和 CC BY-SA 要分開標示（[OSM wiki](https://wiki.openstreetmap.org/wiki/Import/ODbL_Compatibility)） | OSM 營業時間不完整 | ✔（Wikivoyage 是透過鏡像站確認） |
| [京都観光快適度マップ](https://ja.kyoto.travel/comfort/kyoto/) | 主要觀光區分時段的 5 級擁擠預測（KDDI 位置資料加 Prophet；每月更新；2023/10 起納入外國人資料） | 京都主要區域 | 網頁 | 授權未查證 → 只用來做外部驗證，不散布 | 是預測值，不是實測 | △ |
| Google 熱門時段／停留時間（[說明](https://support.google.com/business/answer/6263531)） | 從自願開啟的定位紀錄匯總 | — | 只能人工查看 | 不爬取、不收錄 | — | ✔（只做人工抽查） |
| 遊記：PTT Japan_Travel［遊記］、[Dcard japan_travel](https://www.dcard.tw/f/japan_travel)、部落格、[4travel.jp](https://4travel.jp/travelogue/10782474) | 逐日行程、交通、自述停留時間 | 2019、2023–2026 | 爬蟲（遵守 robots） | 著作權屬作者 → 只釋出 URL 和抽出的 POI 序列（TP-RAG 也是只釋出轉寫後的軌跡） | ToS 未查證；ptt.cc 這次連不上，靠[郭家豪 2019 碩論](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsndl,edsndl.TW.107CHPI0112001)（爬了 7,001 篇）間接確認存在 | △ |
| （選用）[臺北捷運分時 OD](https://data.gov.tw/dataset/128506) | 每日分時的站間進出量 | 2017 年起 | CSV，每月更新 | 政府資料開放授權第 1 版 | 不分旅客和居民 | ✔ |
| （選用）[MLIT 人流オープンデータ](https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto) | 1 km 網格，分時間帶 | 2019–2021 | 註冊後下載 | 未查證 | 涵蓋疫情期間 | △ |

### 題目來源

| 來源 | 內容 | 取得方式 | 授權／用途 | 查證 |
|---|---|---|---|---|
| PTT Japan_Travel［問題］［行程］ | 繁中真實提問（含「行程健檢」） | 爬蟲 | 不散布原文，只用來統計題型頻率和改寫 | △ |
| Dcard japan_travel | 同上 | 爬蟲 | 同上；ToS 未查證 | △ |
| TourismQA（[GitHub](https://github.com/dair-iitd/TourismQA)、[arXiv:1909.03527](https://arxiv.org/abs/1909.03527)） | 47,124 筆 TripAdvisor 論壇 QA，50 城，答案是 POI | 要自己重新爬 | 沒有 LICENSE 檔；多半是住宿、餐廳推薦 → 用來界定排除類 | ✔ |
| Travel Stack Exchange（[2025-12-31 dump](https://archive.org/details/stackexchange_20251231)） | 英文旅遊問答 | 下載 | CC BY-SA，但 2024 年起官方另加限制 | ✔／△ |
| Reddit r/JapanTravel | 英文提問 | 要申請研究用存取 | 據二手資料不得再散布 | ✘ |
| 模板題 | 由 L3 統計自動產生後改寫 | — | 自有 | — |

## 5. 題目類型分類
**符號**：一次造訪 v=(u,d,p,t_in,t_out,src)，u 是去識別後的旅客，d 是旅遊日，p 是地點。統計單位是 user-day，所有統計都附 n 和 90% bootstrap CI。不符合可答條件的題目不收。

| 類別 | 給定 → 問什麼 → 答案型別 | 標準答案怎麼算 ／ 可答條件 ／ 判分 | 例題 |
|---|---|---|---|
| G1 停留時長 | 地點 p（POI、區域或城市）＋可選條件（季節、平日或假日）→ 一般待多久 → 時長 | POI 層：區間設限中位數（下界＝照片或打卡跨度；上界＝前後兩站的間隔減最短交通時間；用 Turnbull 估計）。城市層：每趟旅程在該城有活動的天數中位數。可答：n≥30。判分：答案落在 CI 內算對，另報 log-MAE | 清水寺一般逛多久？ |
| G2 尖峰／離峰時段 | p＋時間粒度（2 小時段、星期或月份）或候選時段 → 哪個時段人最多／最少 → 時段 | 營業時段內，各時段 user-day 數（依時段長度正規化）取最大或最小。可答：n≥50，且 bootstrap 中第一名維持第一的比例 ≥0.8。判分：完全一致才算對 | 伏見稻荷幾點去人最少？ |
| G3 指定時段擁擠度 | p＋一個具體時段 → 擠不擠 → 1–5 級 | r＝該時段的造訪量 ÷ 該地點最忙時段的造訪量，分成 5 級。可答：CI 跨越不超過 1 級。判分：完全命中、差 1 級內，以及 QWK | 週六下午兩點去金閣寺會很擠嗎？ |
| G4 下一站 | 錨點 p（可附候選）→ 看完 p 大家通常接著去哪 → POI | 同一旅遊日、間隔 ≤3 小時的直接下一站，次數最多者。可答：從 p 出發的轉移至少 30 次，且第一名至少是第二名的 1.5 倍。判分：Hit@1、MRR | 金閣寺看完通常接哪裡？ |
| G5 熱門路線 | 區域 A＋時間預算（半日或一日）→ 大家怎麼走 → 3–5 站的有序序列 | 用 PrefixSpan 找 A 內旅遊日序列中最常見的前 3 名走法。可答：第一名至少有 15 個 user-day。判分：與前 3 名中最接近者比 pairs-F1（Chen et al. 2016），另報 POI 集合 F1 | 嵐山半天大家都怎麼走？ |
| G6 人氣比較 | 2–5 個候選 POI（沒有先後關係）→ 哪個去的人最多 → POI | 不重複旅客數最多者。可答：第一、二名占比差的 90% CI 不含 0。判分：accuracy | 金閣寺和銀閣寺哪個比較多人去？ |
| P1 行程可行性 | 使用者自己的行程（出發時刻、至少 2 站有序、可選截止時間）→ 幾點結束、來不來得及 → 時刻或是／否 | 出發時刻＋各站 G1 停留中位數＋群體實測的站間移動時間中位數（不足 30 筆時改用 OSM 路網，並標註）。同時檢查 OSM 營業時間。是／否題刪掉預估結束時間與截止時間相差不到 30 分鐘的題。判分：accuracy、結束時間 MAE | 9 點從京都站出發→伏見稻荷→清水寺→祇園，18 點前逛得完嗎？ |
| P2 行程擁擠暴露 | 使用者行程（給定或可推算各站抵達時刻）→ 哪一站會碰到人潮 → 行程中的某一站 | 用 P1 的方法模擬各站抵達時段，查 G3 的 r 值取最大。可答：第一、二名的 r 差 ≥0.15。判分：accuracy | 照這樣排，哪一站最可能遇到人潮？ |

**依序決策規則**（取第一個成立的規則，所以一題只會落入一類）：
- R0：只問靜態事實（營業時間、票價、地址、怎麼搭車、時刻表、距離）或主觀評價 → 不收。這些屬於地圖／知識庫題。
- R1：題目包含使用者自己至少 2 站的行程嗎？
  - 問結束時刻或來不來得及 → P1。
  - 問哪一站或什麼時候會擠 → P2。
  - 其他 → 不收。
- R2：答案是至少 3 站的有序序列 → G5。
- R3：答案是一段時長 → G1。
- R4：答案是一個時段（包含「早上還是下午」這種二選一）→ G2。
- R5：時段已經給定，答案是擁擠程度 → G3。
- R6：答案是一個 POI，且題目有錨點和「之後、接著、順路」的關係 → G4。
- R7：答案是一個 POI，依造訪人數在候選中比較 → G6。
- 其他 → 不收。

**憑什麼說「常見」**：
1. **產品證據**：Google 特地提供熱門時段和停留時間；京都的官方觀光組織專門做分時段的擁擠預測，2023/10 起還加入外國人資料；「京都要待幾天」這類攻略非常多（例如 [Rough Guides](https://www.roughguides.com/japan/how-many-days-do-you-need-in-kyoto/)）。
2. **文獻**：已有論壇提問分類的研究（[Oriade & Robinson 2019](https://eprints.leedsbeckett.ac.uk/id/eprint/5444)），但沒有軌跡題型的統計，所以必須自己測。
3. **操作化門檻（第 1 個月 pilot）**：
   - 抽 PTT／Dcard 京都相關提問 600 則，加英文 200 則。
   - 兩人依 R0–R7 獨立標註，κ≥0.8 才定稿。
   - 某類佔京都提問至少 3%，且 Wilson 95% 下界至少 1.5%，才保留；不到門檻就刪除或合併。

**刻意排除的題型**：
- 即時題（「現在人多嗎」）。
- 特定日期的事件（祭典當天、點燈排隊）。
- 天候、停駛。
- 造訪少於 30 個 user-day 的冷門點。
- 交通方式占比：遊記樣本太稀疏，列為延伸工作。
- 住宿、餐廳推薦：TourismQA 已涵蓋。
- 個人行蹤回憶（lifelog）：MobQA 已涵蓋。

## 6. 系統設計與評估
**架構**：
1. LLM 解析器：依 R0–R7 分類並抽出槽位，POI 連結到 Wikidata／OSM。
2. 軌跡統計庫：用 DuckDB／PostGIS 預先算好 L3 cube。
3. 工具：dwell()、profile()、crowd_level()、next_stop()、routes()、popularity()、simulate_itinerary()，每個都回傳數值、n、CI 和資料期間。
4. LLM 根據工具結果作答並引用證據；CI 太寬時改給區間或拒答。
5. 可選擇加遊記 RAG 補充敘述。
6. 可用 Qwen2.5-7B 加 LoRA 學習呼叫工具，單張 GPU 就能跑。

**Baselines**：
- B0：closed-book（商用 API 模型，加開源 7–8B 模型）。
- B1：遊記／論壇文本 RAG（相當於立場 C）。
- B2：地圖／知識庫工具，沒有軌跡（相當於立場 A）。
- B3：把原始軌跡樣本放進 prompt（MobQA 的做法）。
- B4：Text-to-SQL 直接查軌跡庫。
- B5：不用 LLM 的人氣排序和 Markov 模型（Chen et al. 2016）。

**指標**：
- 各類別用上表的判分方式，總分用 macro accuracy。
- 選擇性準確率對覆蓋率的曲線、ECE：看模型知不知道自己不確定。
- 證據忠實度：答案引用的 n 和 CI 是否與工具輸出一致。
- 繁中與英文改寫版本的答案一致性。
- 時效漂移：YFCC 時期和 2015 年後的答案差異，以及模型在兩期的表現差。
- 外部效度：G3 與快適度等級的 Spearman 相關；G1 與遊記自述停留時間的相關。

**遊記抽取評估**：
- 150 篇由兩人分別標註，測 POI 的 P／R／F1、順序 pairs-F1、日期歸屬正確率、自述停留時間的誤差。
- 沒達門檻的欄位（例如 POI F1 低於 0.9）不用來算答案。
- 規模估計：3,000 篇 × 約 8k tokens，約 2,400 萬個 input tokens。TP-RAG 自述建構時用了約 10 億 GPT-4o tokens，我們小兩個數量級。

## 7. 與既有研究的差異

| 研究 | 做什麼 | 與本案的差異 |
|---|---|---|
| TP-RAG（[2504.08694](https://arxiv.org/abs/2504.08694)，EMNLP 2025） | 中國 30 城，用 18,784 條從網路遊記整理出的軌跡當 RAG 參考，生成行程 | 最接近的前作。但軌跡只當檢索文本用，停留時間是 LLM 從文件抽出來的，不是算出來的群體統計；評估的是行程品質，不是可驗證的答案 |
| MobQA（[2508.11163](https://arxiv.org/abs/2508.11163)）、TravelBehaviorQA（[Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1604/)）、POI-QA（[2505.10928](https://arxiv.org/abs/2505.10928)） | 對個人 GPS 軌跡（GeoLife）或車輛軌跡（GAIA）做 QA | 問的是個人行為或 POI 事實，不是旅客群體統計；沒有旅客題型，也不檢查個人行程 |
| TravelPlanner（[2402.01622](https://arxiv.org/abs/2402.01622)）、ChinaTravel（[2412.13682](https://arxiv.org/abs/2412.13682)）、TripCraft（[ACL 2025](https://aclanthology.org/2025.acl-long.834)）、TripTailor（[2508.01432](https://arxiv.org/abs/2508.01432)）、TravelEval（[2606.01046](https://arxiv.org/abs/2606.01046)） | 行程規劃的 sandbox 和約束評估 | 停留時間來自 sandbox 設定或類別層級的統計，不是從群體軌跡估計；也不評估答案的統計不確定性 |
| MapEval（[2501.00316](https://arxiv.org/abs/2501.00316)，ICML 2025） | 地圖推理：距離、方向、路徑 | 沒有行為資料，屬於立場 A 的範圍 |
| TourismQA（[1909.03527](https://arxiv.org/abs/1909.03527)） | TripAdvisor 論壇的 POI 推薦 QA | 沒有時空或軌跡成分 |
| LLM4POI（[2404.17591](https://arxiv.org/abs/2404.17591)）、Massive-STEPS（[2505.11239](https://arxiv.org/abs/2505.11239)）、和歌山城旅客軌跡（[2608.20830](https://arxiv.org/abs/2608.20830)） | 預測「某一個人」的下一站 | 我們回答群體層的問題；G4 問的是多數人怎麼走，不是預測某個人 |
| VIR-Bench（[2509.19002](https://arxiv.org/abs/2509.19002)，AAAI 2026） | 從日本旅遊 vlog 重建行程 | 它發現站與站之間的轉移最難重建，這支持我們必須先量化抽取誤差 |
| Lim et al.（[IJCAI 2015](https://www.ijcai.org/Abstract/15/253)）、Chen et al.（[CIKM 2016](https://arxiv.org/abs/1608.07051)） | 用 Flickr 軌跡做行程推薦 | 我們沿用它們的造訪定義和 pairs-F1；它們不做 QA，也不涉及 LLM |

**新意**（「首個」只限本回合查到的文獻範圍）：
1. 首個把群體軌跡統計轉成「可用程式驗證、附 CI」的旅客 QA。
2. 可答性過濾，加上每題的時效標註。
3. 用群體統計檢查個人行程的題型。
4. 從遊記抽取軌跡的誤差實證。

## 8. 最大風險，以及為什麼仍優於 A、C

**最大風險**：2015 年以後京都的開放照片量可能不夠（Flickr 使用者在減少，API key 也要付費 Pro 帳號），以及遊記抽取的誤差。

**緩解方式**：
- 第 1 個月做繼續／放棄判斷：如果至少 30 個 user-day 的 POI 少於 100 個，就改成京阪合併，或放寬門檻並改用較寬的時長區間。
- 多來源一致性：Flickr 和遊記的統計互相矛盾時，題目標為「依來源而定」或直接刪除。
- 舊資料不當主測試集，改用來研究時效漂移。
- 白天、上鏡景點的偏差：G2、G3 只算營業時段，並用快適度マップ驗證。
- 法律與隱私：只釋出 ID 和衍生統計（做法同 TP-RAG）；每格至少 10 人才公布。

**時程**：
- M1：pilot（題型頻率，加上 YFCC 京都的實際數量）。
- M2–M4：軌跡管線和遊記抽取。
- M5–M6：產生 QA 並人工審核。
- M7–M9：系統和 baselines。
- M10–M12：實驗和寫作。

**預判 A 的攻擊：「統計答案不精確」**
- 我們的答案一樣由程式重算、完全可重現，只是多附了 n 和 CI。
- A 能精確回答的是營業時間、時刻表這類靜態屬性。旅客真正卡關的是「要待多久、幾點人少、排得完嗎」，A 只能給常數或類別平均，TripCraft 就是這樣處理的。
- A 的知識庫在我們的系統裡可以當工具用；反過來，A 沒有軌跡，G1–G6 都答不了。

**預判 C 的攻擊：「模板題不真實」**
- 題型保不保留由論壇抽樣決定，另外還有 300 題真實提問的測試集。
- C 如果用論壇回覆當標準答案，那是單一意見，回覆之間常互相矛盾，也無法重算。
- 我們把 C 的資料（遊記）轉成可計算的軌跡，等於吸收了 C 的資料優勢，同時給出 C 給不出的可驗證答案。

**辨識度**：地圖 QA 和旅遊文本 RAG 已經有大量前作（MapEval、TravelPlanner 系列、TourismQA）。「群體軌跡統計 QA」在本回合查到的文獻裡沒有直接對應；最接近的 TP-RAG 也只是把軌跡當檢索文本。

（Pilot 的程式與資料在 /tmp/claude-0/-home-user-claude-remote/4cfe03c7-2f55-4151-9d26-a384ae52e556/scratchpad/scripts/pilot.py 和 /tmp/claude-0/-home-user-claude-remote/4cfe03c7-2f55-4151-9d26-a384ae52e556/scratchpad/dl_tour/。沒有動 repo，也沒有寫報告檔。）
