# 教材索引（計算機組織，期中範圍 Ch1-1 ～ Ch4-3）

每份簡報都有兩個版本，頁碼與投影片編號一一對應：

- `md/ChX-Y.md`：逐張文字（標題、條列、表格、備忘稿）。出題時先讀這個。
- `pdf/ChX-Y.pdf`：逐頁圖像。`md` 中標示「［圖：見 PDF 第 N 頁］」或需要看 datapath／pipeline 圖時，讀 PDF 的第 N 頁。
- `md/Midterm-Practice.md`：老師的期中練習卷（題目 + 解答），是出題風格的範本。

## 課程慣例（出題時要照這些）

- 課程章節和課本不同：課程 **Ch3 = 課本 Ch4 處理器（4.1–4.4、4.10 exception）**，課程 **Ch4 = Pipelining（4.5–4.6 前半）**。投影片頁尾仍寫「Chapter 4 — The Processor」。
- **沒有教**：pipeline hazard（forwarding、stall、branch prediction）、課本 Ch3 的算術（乘除法、浮點數）。
- ALU control：AND = 0000、OR = 0001、add = 0010、subtract = 0110、slt = 0111、NOR = 1100；ALUOp：lw/sw = 00、beq = 01、R-type = 10。
- Exception：EPC 存「造成 exception 的那條指令位址」；Cause 用 1 bit（0 = undefined opcode、1 = overflow）；共用 handler 在 0x80000180；syscall 完成後從 EPC + 4 繼續，修正後重做則從 EPC 重新執行。
- Pipeline：N 條指令在 5-stage 需要 N + 4 個 cycle；clock = 最慢的 stage；練習題通常不考慮 pipeline register overhead。
- 每節最後都有 **Quick Questions** 和 **Exercises**（含答案），是最接近考題的素材。

## 各節內容

### Ch1-1（10 張）— [`md/Ch1-1.md`](md/Ch1-1.md) · [`pdf/Ch1-1.pdf`](pdf/Ch1-1.pdf)

電腦抽象層：C → 組合語言 → 機器碼；Compiler／OS／Processor 的分工；電腦基本元件（Processor、Memory、I/O）

- 練習：Quick Questions 第 7 張；Exercises 第 8–10 張
- 投影片：1 Chapter 1；2 Below Your Program；3 Levels of Program Code；4 Abstractions；5 Components of a Computer；6 Inside the Processor (CPU)；7 Section 1-1 Quick Questions；8 Exercise 1 | Who Does What?；9 Exercise 2 | Abstraction in Everyday Computing；10 Exercise 3 | Smartphone as a Computer

### Ch1-2（18 張）— [`md/Ch1-2.md`](md/Ch1-2.md) · [`pdf/Ch1-2.pdf`](pdf/Ch1-2.pdf)

效能定義：response time vs. throughput、relative performance（快 X% 與時間少 Y% 的差別）、elapsed time vs. CPU time；CPU／GPU／AI accelerator

- 練習：Quick Questions 第 11–12 張；Exercises 第 13–18 張
- 投影片：1 Chapter 1；2 Understanding Performance；3 Defining Performance；4 Response Time and Throughput；5 Relative Performance；6 Measuring Execution Time；7 The Rise of AI Computing；8 Why Does AI Need Specialized Hardware?；9 Computing Is Not the Only Bottleneck；10 Modern Computer Architecture；11 Section 1-2 Quick Questions；12 Section 1-2 Quick Questions (cont.)；13 Exercise 1 | Choosing Hardware for Different Workloads；14 Exercise 2 | Response Time vs. Throughput；15 Exercise 3 | Relative Performance；16 Exercise 4 | Elapsed Time vs. CPU Time；17 Exercise 5 | Integrated Performance Analysis；18 Exercise 5 | Integrated Performance Analysis — Answer

### Ch1-3（20 張）— [`md/Ch1-3.md`](md/Ch1-3.md) · [`pdf/Ch1-3.pdf`](pdf/Ch1-3.pdf)

CPU Time = IC × CPI / f；clock cycle、cycle time、clock rate；instruction mix 與 average CPI；compiler 對 IC 和 CPI 的影響

- 練習：Quick Questions 第 14–15 張；Exercises 第 16–20 張
- 投影片：1 Chapter 1；2 Measuring Execution Time；3 CPU Clocking；4 CPU Time；5 CPU Time Example；6 Instruction Count and CPI；7 CPI Example；8 CPI in More Detail；9–12 CPI Example；13 Performance Summary；14–15 Section 1-3 Quick Questions；16 Exercise 1 | Clock Rate and CPU Time；17 Exercise 2 | Clock Rate vs. Clock Cycles；18 Exercise 3 | Instruction Mix and Average CPI；19 Exercise 4 | Compiler Optimization and Instruction Mix；20 Exercise 5 | Integrated Performance Analysis

### Ch1-4（17 張）— [`md/Ch1-4.md`](md/Ch1-4.md) · [`pdf/Ch1-4.pdf`](pdf/Ch1-4.pdf)

Power wall（P ∝ C·V²·f）、電壓與頻率；ILP vs. multicore；SPEC 幾何平均；MIPS pitfall；Amdahl's Law 與 multicore

- 練習：Quick Questions 第 11–12 張；Exercises 第 13–17 張
- 投影片：1 Chapter 1；2 How Can We Further Improve Performance?；3 Power Trends；4 Reducing Power；5 Uniprocessor Performance；6 Multiprocessors；7 SPEC CPU Benchmark；8 Pitfall: MIPS as a Performance Metric；9 Pitfall: Amdahl’s Law；10 Concluding Remarks；11–12 Section 1-4 Quick Questions；13 Exercise 1 | Power Consumption；14 Exercise 2 | Voltage and Clock Frequency；15 Exercise 3 | SPEC Benchmark；16 Exercise 4 | MIPS Pitfall；17 Exercise 5 | Amdahl’s Law and Multicore

### Ch2-1（20 張）— [`md/Ch2-1.md`](md/Ch2-1.md) · [`pdf/Ch2-1.pdf`](pdf/Ch2-1.pdf)

MIPS 運算元：算術指令、暫存器、memory operand（lw／sw、byte offset = index × 4）、immediate、$zero

- 練習：Quick Questions 第 14–15 張；Exercises 第 16–20 張
- 投影片：1 Chapter 2；2 Instruction Set；3 The MIPS Instruction Set；4 Arithmetic Operations；5 Arithmetic Example；6 Register Operands；7 Register Operand Example；8 Memory Operands；9 Memory Operand Example 1；10 Memory Operand Example 2；11 Registers vs. Memory；12 Immediate Operands；13 The Constant Zero；14–15 Section 2-1 Quick Questions；16 Exercise 1 | Arithmetic & Register Operands；17 Exercise 2 | Register Value Tracking；18 Exercise 3 | Array Addressing and Memory Access；19 Exercise 4 | Load–Operate–Store；20 Exercise 5 | Integrated MIPS Analysis

### Ch2-2（27 張）— [`md/Ch2-2.md`](md/Ch2-2.md) · [`pdf/Ch2-2.pdf`](pdf/Ch2-2.pdf)

Unsigned 與二補數、sign extension／zero extension、hex；R-format／I-format 編碼與解碼

- 練習：Quick Questions 第 21–22 張；Exercises 第 23–27 張
- 投影片：1 Chapter 2；2–3 Unsigned Binary Integers；4–7 2s-Complement Signed Integers；8–9 Signed Negation；10–11 Sign Extension；12 Representing Instructions；13–14 Hexadecimal；15–16 MIPS R-format Instructions；17–18 R-format Example；19–20 MIPS I-format Instructions；21–22 Section 2-2 Quick Questions；23 Exercise 1 | Two’s-Complement Arithmetic；24 Exercise 2 | Representation & Sign Extension；25 Exercise 3 | Decode a Machine Instruction；26 Exercise 4 | Encode an R-format Instruction；27 Exercise 5 | Integrated R/I-format Analysis

### Ch2-3（34 張）— [`md/Ch2-3.md`](md/Ch2-3.md) · [`pdf/Ch2-3.pdf`](pdf/Ch2-3.pdf)

邏輯運算（and／or／nor、shift、mask）；條件分支（beq／bne／slt／sltu／j）；if-else、while、array loop

- 練習：Quick Questions 第 27–28 張；Exercises 第 29–34 張
- 投影片：1 Chapter 2；2–4 Stored Program Computers；5–6 Logical Operations；7–9 Shift Operations；10–11 AND Operations；12 OR Operations；13 NOT Operations；14–15 Conditional Operations；16–17 Compiling If Statements；18–19 Compiling Loop Statements；20–21 More Conditional Operations；22–23 Branch Instruction Design；24–25 Signed vs. Unsigned；26 Concluding Remarks；27–28 Section 2-3 Quick Questions；29 Exercise 1 | Bitwise Masking & Modification；30 Exercise 2 | Signed Shift Operations；31 Exercise 3 | Conditional Execution Trace；32 Exercise 4 | If–Else with Comparison；33 Exercise 5 | Array Loop Analysis；34 Exercise 5 | Array Loop Analysis — Answer

### Ch2-4（26 張）— [`md/Ch2-4.md`](md/Ch2-4.md) · [`pdf/Ch2-4.pdf`](pdf/Ch2-4.pdf)

Procedure：jal／jr、$a／$v／$t／$s／$ra／$sp、stack frame、leaf 與 non-leaf、遞迴（fact）

- 練習：Quick Questions 第 22 張；Exercises 第 23–26 張
- 投影片：1 Chapter 2；2–3 Procedure Calling；4–7 Register Usage；8–10 Procedure Call Instructions；11–12 Leaf Procedure Example；13 Register Operand Example；14 Leaf Procedure Example；15 Non-Leaf Procedures；16–18 Non-Leaf Procedure Example；19–21 Local Data on the Stack；22 Section 2-4 Quick Questions；23 Exercise 1 | Procedure Calling and Register Usage；24 Exercise 2 | Trace a Leaf Procedure；25 Exercise 3 | Complete a Non-Leaf Procedure；26 Exercise 4 | Trace Recursive Stack Usage

### Ch2-5（22 張）— [`md/Ch2-5.md`](md/Ch2-5.md) · [`pdf/Ch2-5.pdf`](pdf/Ch2-5.pdf)

Byte 存取（lb／lbu／sb）、32-bit 常數（lui／ori）、branch addressing（以 PC+4 為基準）、jump addressing（pseudodirect，能否跳到）

- 練習：Quick Questions 第 19 張；Exercises 第 20–22 張
- 投影片：1 Chapter 2；2–3 Memory Layout；4–5 Character Data；6–7 Filling the Byte；8–9 Branch Addressing；10–11 32-bit Constants；12–13 Target Addressing Example；14–15 Jump Addressing；16 Branching Far Away；17–18 Addressing Mode Summary；19 Section 2-5 Quick Questions；20 Exercise 1 | Byte Memory Operations；21 Exercise 2 | Branch Addressing and Encoding；22 Exercise 3 | Can the Jump Reach the Target?

### Ch2-6（31 張）— [`md/Ch2-6.md`](md/Ch2-6.md) · [`pdf/Ch2-6.pdf`](pdf/Ch2-6.pdf)

Translating／linking／loading（resolve labels、patch references）、pseudoinstruction 與 $at、swap／sort 範例、ARM vs. MIPS、指令總表

- 練習：Quick Questions 第 27 張；Exercises 第 28–31 張
- 投影片：1 Chapter 2；2–3 Translation and Startup；4–5 Assembler Pseudoinstructions；6 Producing an Object Module；7 （無標題）；8 Linking Object Modules；9 （無標題）；10 Q2. Suppose main.o contains a reference to addTwo, which is defined in another object mo…；11 C Sort Example；12–13 The Procedure Swap；14–16 ARM & MIPS Similarities；17 MIPS vs. Other ISAs；18–19 Fallacies；20–21 Concluding Remarks；22 （無標題）；23–26 Q5. Complete the following table. For each MIPS operation, write its full name/meaning, …；27 Section 2-6 Quick Questions；28 Exercise 1 | Pseudoinstruction Expansion；29 Exercise 2 | Procedure Swap Analysis；30 Exercise 3 | Trace a MIPS Loop；31 Exercise 4 | Integrated Instruction Analysis

### Ch3-1（23 張）— [`md/Ch3-1.md`](md/Ch3-1.md) · [`pdf/Ch3-1.pdf`](pdf/Ch3-1.pdf)

處理器概論（課本 4.1–4.2）：指令執行步驟、datapath 元件、MUX 與 control 的角色

- 練習：Quick Questions 第 20 張；Exercises 第 21–23 張
- 投影片：1 Chapter 3；2 （無標題）；3–4 Instruction Execution；5–11 CPU Overview；12–13 Multiplexers；14–16 Control；17–19 （無標題）；20 Section 3-1 Quick Questions；21 Exercise 1 | Trace an Instruction；22 Exercise 2 | Compare Instruction Paths；23 Exercise 3 | Datapath Selection and Control

### Ch3-2（26 張）— [`md/Ch3-2.md`](md/Ch3-2.md) · [`pdf/Ch3-2.pdf`](pdf/Ch3-2.pdf)

邏輯設計基礎：combinational vs. state element、half adder、register file、clocking methodology、clock period 與延遲

- 練習：Quick Questions 第 23 張；Exercises 第 24–26 張
- 投影片：1 Chapter 3；2 CPU Overview (Recap)；3 Control (Recap)；4 Logic Design Basics；5 Binary in Hardware；6 Combinational Logic；7–8 State Elements；9–10 Combinational Elements；11 Logic Foundations in Disguise；12–13 Combinational Elements；14–16 Sequential Elements；17 Sequential Logic Design；18 Sequential Elements；19 Register File；20 Clocking Methodology；21–22 Clocking Methodology (Cont.)；23 Section 3-2 Quick Questions；24 Exercise 1 — Combinational Circuit Design；25 Exercise 2 — Register File Operation；26 Exercise 3 — Clock Period & Delay

### Ch3-3（30 張）— [`md/Ch3-3.md`](md/Ch3-3.md) · [`pdf/Ch3-3.pdf`](pdf/Ch3-3.pdf)

建立 datapath：R-format、lw／sw、beq 在 datapath 上的數值追蹤（PC+4、sign-extend、ALU result、branch target）

- 練習：Quick Questions 第 27 張；Exercises 第 28–30 張
- 投影片：1 Chapter 3；2 CPU Overview (Recap)；3 Control (Recap)；4 Building a Datapath；5 Instruction Fetch；6–7 Tracing the Instruction Fetch；8 R-Format Instructions；9–10 Tracing R-Format Inst.；11 Values in R-Format Inst.；12 Number vs. Data；13 Load/Store Instructions；14 Tracing Load Instruction；15 Tracing Store Instruction；16 Values in Load/Store Inst.；17–18 Three Highlights；19–20 Branch Instructions；21 Tracing Branch Instructions；22–23 Values in Branch Instructions；24 R-Type/Load/Store Datapath；25–26 Full Datapath；27 Section 3-3 Quick Questions；28 Exercise 1 — Comparing Datapath Usage；29 Exercise 2 — Debug the Datapath；30 Exercise 3 — Complete Branch Tracing

### Ch3-4（22 張）— [`md/Ch3-4.md`](md/Ch3-4.md) · [`pdf/Ch3-4.pdf`](pdf/Ch3-4.pdf)

Control：各 control signal 的功能、ALU control（ALUOp + funct → 4-bit）、don't care (X)、MUX 的選擇

- 練習：Quick Questions 第 19 張；Exercises 第 20–22 張
- 投影片：1 Chapter 3；2 Multiple Controls；3 Different Control Signals；4–6 Control Signals in the CPU；7 Controlling the ALU；8–10 ALU Control；11–12 Understanding Don't Care (X)；13–14 Control Signals for MUX；15–16 Control for Reg. & Memory；17 The Main Control Unit；18 Datapath With Control；19 Section 3-4 Quick Questions；20 Exercise 1 — Decode the ALU Control；21 Exercise 2 — Determine R-Type Control Signals；22 Exercise 3 — Find the Control Error

### Ch3-5（32 張）— [`md/Ch3-5.md`](md/Ch3-5.md) · [`pdf/Ch3-5.pdf`](pdf/Ch3-5.pdf)

用 control signal 追蹤 R／lw／sw／beq／jump；control 故障分析；由結果反推 control；jump target 組合

- 練習：Quick Questions 第 26 張；Exercises 第 27–32 張
- 投影片：1 Chapter 3；2 Tracing with Control Signals；3 R-Type Instruction；4 R-Format Inst. (Recap)；5 R-Format Instruction Controls；6–7 Controls in R-Format Inst.；8 Load Instruction；9 Load Instruction Controls；10–11 Controls in Load Instructions；12 Store Instruction Controls；13–14 Controls in Store Instructions；15 Branch-on-Equal Instruction；16 Branch Instruction Controls；17–18 Controls in Branch Instruction；19 Implementing Jumps；20 Datapath With Jumps Added；21 Implementing Jump Control；22 Jump Instruction Controls；23–24 Controls in Jump Instruction；25 Performance Issues；26 Section 3-5 Quick Questions；27–28 Exercise 1 — Control Signal Completion；29 Exercise 2 — Control Signal Fault Analysis；30 Exercise 3 — Reverse Control Signal Tracing；31 Exercise 4 — Reverse Branch Control Analysis；32 Exercise 5 — Jump Target Reconstruction

### Ch3-6（31 張）— [`md/Ch3-6.md`](md/Ch3-6.md) · [`pdf/Ch3-6.pdf`](pdf/Ch3-6.pdf)

單週期效能問題（clock 由 lw 決定、浪費的時間）；Exception vs. interrupt、EPC、Cause、handler、vectored interrupt、Restart／Continue／Terminate

- 練習：Quick Questions 第 25 張；Exercises 第 26–31 張
- 投影片：1 Chapter 3；2–4 Performance Issues；5 Exceptions and Interrupts；6 What’s the Difference；7–9 Common Exception Types；10–12 Handling Exceptions；13 An Alternate Mechanism；14 Common vs. Vectored；15 Handler Actions；16–18 Handler Action Flow；19–21 Exception Properties；22 Exception Example；23 Other Examples；24 Concluding Remarks；25 Section 3-6 Quick Questions；26–27 Exercise 1 — Single-Cycle Processor Performance；28–29 Exercise 2 — Exception Handling Procedure；30–31 Exercise 3 — Complete Exception Execution Tracing

### Ch4-1（24 張）— [`md/Ch4-1.md`](md/Ch4-1.md) · [`pdf/Ch4-1.pdf`](pdf/Ch4-1.pdf)

Pipelining 概論：五個 stage、pipeline 執行時間 (n + k − 1) × T、throughput vs. latency、stage 延遲不平均、pipeline register

- 練習：Quick Questions 第 21 張；Exercises 第 22–24 張
- 投影片：1 Chapter 4；2 From Processor to Pipelining；3 Pipelining Analogy；4 MIPS Pipeline；5 What Happens in Each Stage?；6–7 Five Stages in Different Inst.；8–10 Pipeline Performance；11–12 Pipeline Execution Time；13 Pipeline Speedup；14–15 Throughput vs. Latency；16 Pipelining and ISA Design；17 MIPS Pipelined Datapath；18–19 Pipeline registers；20 Summary；21 Section 4-1 Quick Questions；22 Exercise 1 — Pipeline Timing Analysis；23 Exercise 2 — Pipeline Performance Comparison；24 Exercise 3 — Pipeline Register Error Analysis

### Ch4-2（25 張）— [`md/Ch4-2.md`](md/Ch4-2.md) · [`pdf/Ch4-2.pdf`](pdf/Ch4-2.pdf)

Pipelined datapath：各 stage 與 IF/ID、ID/EX、EX/MEM、MEM/WB 存的內容；destination register 編號錯誤問題；lw／R-format 追蹤

- 練習：Quick Questions 第 22 張；Exercises 第 23–25 張
- 投影片：1 Chapter 4；2 Pipeline Operation；3 IF for Load, Store, …；4–5 Instruction fetch (Cont.)；6 ID for Load, Store, …；7 Instruction Decode (Cont.)；8 EX for Load；9–10 Execute (Cont.)；11 MEM for Load；12–13 Memory Access (Cont.)；14 WB for Load；15–16 Wrong Register Number；17 Write Back (Cont.)；18 Corrected Datapath for Load；19–20 Complete Load Inst. Tracing；21 Complete R-format Instruction；22 Section 4-2 Quick Questions；23 Exercise 1 — Pipeline Register Consistency；24 Exercise 2 — Pipeline Stage Timing；25 Exercise 3 — Reverse Pipeline Reasoning

### Ch4-3（27 張）— [`md/Ch4-3.md`](md/Ch4-3.md) · [`pdf/Ch4-3.pdf`](pdf/Ch4-3.pdf)

Store 追蹤、load vs. store、multi-cycle pipeline diagram、stage occupancy、single-cycle pipeline diagram（某 CC 各 pipeline register 屬於哪條指令）

- 練習：Quick Questions 第 23 張；Exercises 第 24–27 張
- 投影片：1 Chapter 4；2 Pipeline Operation (Recap)；3 Complete Load Inst. Tracing；4 Complete Store Inst. Tracing；5 EX for Store；6 Execute for Store (Cont.)；7 MEM for Store；8 Memory Access Store (Cont.)；9 WB for Store；10–11 Write Back Store (Cont.)；12–13 Load vs. Store；14 Multi-Cycle Pipeline Overview；15–17 Multi-Cycle Pipeline Diagram；18–19 Pipeline Stage Occupancy；20–21 Single-Cycle Pipeline Diagram；22 Summary；23 Section 4-3 Quick Questions；24 Exercise 1 — Load and Store Datapath Tracing；25 Exercise 2 — Multi-Cycle Pipeline Diagram；26 Exercise 3 — Single-Cycle Pipeline Analysis；27 Exercise 3 — Answer
