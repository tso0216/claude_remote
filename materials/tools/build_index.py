import os, re, sys

md_dir, out = sys.argv[1], sys.argv[2]

TOPICS = {
    "1-1": "電腦抽象層：C → 組合語言 → 機器碼；Compiler／OS／Processor 的分工；電腦基本元件（Processor、Memory、I/O）",
    "1-2": "效能定義：response time vs. throughput、relative performance（快 X% 與時間少 Y% 的差別）、elapsed time vs. CPU time；CPU／GPU／AI accelerator",
    "1-3": "CPU Time = IC × CPI / f；clock cycle、cycle time、clock rate；instruction mix 與 average CPI；compiler 對 IC 和 CPI 的影響",
    "1-4": "Power wall（P ∝ C·V²·f）、電壓與頻率；ILP vs. multicore；SPEC 幾何平均；MIPS pitfall；Amdahl's Law 與 multicore",
    "2-1": "MIPS 運算元：算術指令、暫存器、memory operand（lw／sw、byte offset = index × 4）、immediate、$zero",
    "2-2": "Unsigned 與二補數、sign extension／zero extension、hex；R-format／I-format 編碼與解碼",
    "2-3": "邏輯運算（and／or／nor、shift、mask）；條件分支（beq／bne／slt／sltu／j）；if-else、while、array loop",
    "2-4": "Procedure：jal／jr、$a／$v／$t／$s／$ra／$sp、stack frame、leaf 與 non-leaf、遞迴（fact）",
    "2-5": "Byte 存取（lb／lbu／sb）、32-bit 常數（lui／ori）、branch addressing（以 PC+4 為基準）、jump addressing（pseudodirect，能否跳到）",
    "2-6": "Translating／linking／loading（resolve labels、patch references）、pseudoinstruction 與 $at、swap／sort 範例、ARM vs. MIPS、指令總表",
    "3-1": "處理器概論（課本 4.1–4.2）：指令執行步驟、datapath 元件、MUX 與 control 的角色",
    "3-2": "邏輯設計基礎：combinational vs. state element、half adder、register file、clocking methodology、clock period 與延遲",
    "3-3": "建立 datapath：R-format、lw／sw、beq 在 datapath 上的數值追蹤（PC+4、sign-extend、ALU result、branch target）",
    "3-4": "Control：各 control signal 的功能、ALU control（ALUOp + funct → 4-bit）、don't care (X)、MUX 的選擇",
    "3-5": "用 control signal 追蹤 R／lw／sw／beq／jump；control 故障分析；由結果反推 control；jump target 組合",
    "3-6": "單週期效能問題（clock 由 lw 決定、浪費的時間）；Exception vs. interrupt、EPC、Cause、handler、vectored interrupt、Restart／Continue／Terminate",
    "4-1": "Pipelining 概論：五個 stage、pipeline 執行時間 (n + k − 1) × T、throughput vs. latency、stage 延遲不平均、pipeline register",
    "4-2": "Pipelined datapath：各 stage 與 IF/ID、ID/EX、EX/MEM、MEM/WB 存的內容；destination register 編號錯誤問題；lw／R-format 追蹤",
    "4-3": "Store 追蹤、load vs. store、multi-cycle pipeline diagram、stage occupancy、single-cycle pipeline diagram（某 CC 各 pipeline register 屬於哪條指令）",
}

def ranges(nums):
    out, start, prev = [], None, None
    for n in nums:
        if start is None: start = prev = n
        elif n == prev + 1: prev = n
        else: out.append((start, prev)); start = prev = n
    if start is not None: out.append((start, prev))
    return ", ".join(f"{a}" if a == b else f"{a}–{b}" for a, b in out)

lines = []
lines.append("# 教材索引（計算機組織，期中範圍 Ch1-1 ～ Ch4-3）\n")
lines.append("每份簡報都有兩個版本，頁碼與投影片編號一一對應：\n")
lines.append("- `md/ChX-Y.md`：逐張文字（標題、條列、表格、備忘稿）。出題時先讀這個。")
lines.append("- `pdf/ChX-Y.pdf`：逐頁圖像。`md` 中標示「［圖：見 PDF 第 N 頁］」或需要看 datapath／pipeline 圖時，讀 PDF 的第 N 頁。")
lines.append("- `md/Midterm-Practice.md`：老師的期中練習卷（題目 + 解答），是出題風格的範本。\n")
lines.append("## 課程慣例（出題時要照這些）\n")
lines.append("- 課程章節和課本不同：課程 **Ch3 = 課本 Ch4 處理器（4.1–4.4、4.10 exception）**，課程 **Ch4 = Pipelining（4.5–4.6 前半）**。投影片頁尾仍寫「Chapter 4 — The Processor」。")
lines.append("- **沒有教**：pipeline hazard（forwarding、stall、branch prediction）、課本 Ch3 的算術（乘除法、浮點數）。")
lines.append("- ALU control：AND = 0000、OR = 0001、add = 0010、subtract = 0110、slt = 0111、NOR = 1100；ALUOp：lw/sw = 00、beq = 01、R-type = 10。")
lines.append("- Exception：EPC 存「造成 exception 的那條指令位址」；Cause 用 1 bit（0 = undefined opcode、1 = overflow）；共用 handler 在 0x80000180；syscall 完成後從 EPC + 4 繼續，修正後重做則從 EPC 重新執行。")
lines.append("- Pipeline：N 條指令在 5-stage 需要 N + 4 個 cycle；clock = 最慢的 stage；練習題通常不考慮 pipeline register overhead。")
lines.append("- 每節最後都有 **Quick Questions** 和 **Exercises**（含答案），是最接近考題的素材。\n")
lines.append("## 各節內容\n")

files = sorted(f for f in os.listdir(md_dir) if re.match(r"Ch\d-\d\.md$", f))
for f in files:
    sec = f[2:-3]
    text = open(os.path.join(md_dir, f), encoding="utf-8").read()
    slides = re.findall(r"^## Slide (\d+)(?: — (.*))?$", text, re.M)
    titles = [(int(n), (t or "").strip()) for n, t in slides]
    qq = [n for n, t in titles if "Quick Questions" in t]
    ex = [n for n, t in titles if t.startswith("Exercise")]
    lines.append(f"### Ch{sec}（{len(titles)} 張）— [`md/{f}`](md/{f}) · [`pdf/Ch{sec}.pdf`](pdf/Ch{sec}.pdf)\n")
    lines.append(f"{TOPICS.get(sec, '')}\n")
    if qq or ex:
        lines.append(f"- 練習：Quick Questions 第 {ranges(qq) or '—'} 張；Exercises 第 {ranges(ex) or '—'} 張")
    # collapse consecutive identical titles
    groups, prev = [], None
    for n, t in titles:
        label = t or "（無標題）"
        if prev and prev[1] == label and prev[0][1] == n - 1:
            prev[0][1] = n
        else:
            prev = [[n, n], label]; groups.append(prev)
    parts = [f"{a if a == b else f'{a}–{b}'} {lab}" for (a, b), lab in groups]
    lines.append("- 投影片：" + "；".join(parts) + "\n")

open(out, "w", encoding="utf-8").write("\n".join(lines))
print("index written", len(files), "sections")
