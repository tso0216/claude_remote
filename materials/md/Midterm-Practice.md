# Midterm Practice（老師提供的練習卷）

> 來源：`Midterm Practice.pdf`（22 頁，題目後接紅字解答）。這份是出題風格的範本：英文題目、每題 (a)(b)(c) 小題、計算題為主。

---

## Q1. Computer Performance

A processor executes a program consisting of three instruction classes. The instruction counts and average CPI values are given below.

| Instruction Class | Instruction Count | CPI |
| --- | --- | --- |
| Arithmetic | 400 million | 1 |
| Load/Store | 300 million | 3 |
| Branch | 100 million | 2 |

The processor operates at a clock frequency of 2 GHz.

(a) Calculate the average CPI and the total CPU execution time of the program.

(b) A new processor design reduces the CPI of Load/Store instructions from 3 to 2, while all other parameters remain unchanged. Calculate the new CPU execution time and the overall speedup.

(c) Instead of improving Load/Store instructions, another design increases the clock frequency from 2 GHz to 2.5 GHz while keeping the original CPI values. Determine which design, (b) or (c), provides better performance and calculate the percentage difference in execution time relative to the slower design.

### Answer 1

- (a) IC = 400 + 300 + 100 = 800 million；CPI_avg = [400(1) + 300(3) + 100(2)] / 800 = **1.875**；T_CPU = IC × CPI / f = 800×10⁶ × 1.875 / 2×10⁹ = **0.75 s**
- (b) Cycles = 400(1) + 300(2) + 100(2) = 1200 million；T_b = 1200×10⁶ / 2×10⁹ = **0.60 s**；Speedup = 0.75 / 0.60 = **1.25**
- (c) T_c = 1500×10⁶ / 2.5×10⁹ = **0.60 s**；|T_b − T_c| / max(T_b, T_c) × 100% = **0%**

---

## Q2. MIPS Instructions and Machine Code

Consider the following MIPS instructions, starting at memory address 0x00400020.

```
Address       Instruction
0x00400020    add  $t0, $s1, $s2
0x00400024    lw   $t1, 12($t0)
0x00400028    beq  $t1, $zero, TARGET
0x0040002C    sub  $t2, $t1, $s3
0x00400030    addi $t3, $t3, 1
0x00400034    TARGET: or $t4, $t0, $t2
```

Assume standard 32-bit MIPS instruction encoding.

(a) Identify the instruction format (R-type, I-type, or J-type) of the add, lw, and beq instructions. For each instruction, specify the values of its encoding fields in decimal.

(b) Convert the following instruction into its 32-bit machine code in hexadecimal: `lw $t1, 12($t0)`

(c) Calculate the 16-bit branch offset of the beq instruction. Express the offset in decimal and hexadecimal. If $t1 = 0, determine the next instruction address executed after the branch.

### Answer 2

- (a) `add $t0, $s1, $s2`：R-type，opcode = 0, rs = 17 ($s1), rt = 18 ($s2), rd = 8 ($t0), shamt = 0, funct = 32
  `lw $t1, 12($t0)`：I-type，opcode = 35, rs = 8 ($t0), rt = 9 ($t1), immediate = 12
  `beq $t1, $zero, TARGET`：I-type，opcode = 4, rs = 9 ($t1), rt = 0 ($zero), immediate = 2
- (b) 100011 | 01000 | 01001 | 0000000000001100 → **0x8D09000C**
- (c) PC = 0x00400028，PC + 4 = 0x0040002C，TARGET = 0x00400034；Offset = (TARGET − (PC+4)) / 4 = (0x00400034 − 0x0040002C) / 4 = **2** = **0x0002**；$t1 = 0 → branch taken → next = **0x00400034**

---

## Q3. MIPS Program Analysis

```
        addi $t0, $zero, 0
        addi $t1, $zero, 4
        addi $t2, $zero, 0
LOOP:   lw   $t3, 0($a0)
        add  $t2, $t2, $t3
        addi $a0, $a0, 4
        addi $t0, $t0, 1
        bne  $t0, $t1, LOOP
        sw   $t2, 0($a1)
```

Assume the initial register values are $a0 = 0x10010000, $a1 = 0x10020000.

| Memory Address | Value |
| --- | --- |
| 0x10010000 | 5 |
| 0x10010004 | 8 |
| 0x10010008 | 3 |
| 0x1001000C | 6 |

Assume that branch delay slots are not used.

(a) Determine the number of iterations executed by the loop and the final values of registers $t0, $t2, and $a0.

(b) Determine the memory address and value written by the sw instruction. Also calculate the total number of dynamically executed instructions, including the final sw.

(c) Suppose the instruction addi $a0, $a0, 4 is changed to addi $a0, $a0, 8. Assume that memory locations 0x10010010 and 0x10010018 contain the values 10 and 12, respectively. Determine the new final value of $t2.

### Answer 3

- (a) 4 iterations（loaded 5, 8, 3, 6；$t2 = 5, 13, 16, 22）；**$t0 = 4, $t2 = 22, $a0 = 0x10010010**
- (b) sw $t2, 0($a1)：address **0x10020000**，value **22**；IC = 3 + (5 × 4) + 1 = **24**
- (c) Accesses 0x10010000, 0x10010008, 0x10010010, 0x10010018 → $t2 = 5 + 3 + 10 + 12 = **30**

---

## Q4. C-to-MIPS Code Translation

```c
int A[5] = {3, 7, 2, 8, 4};
int sum = 0;

for (int i = 0; i < 5; i++)
    if (A[i] > 4)
        sum += A[i];
```

Assume: $s0 stores the base address of array A; $s1 stores sum, initially 0; $t0 stores the loop variable i, initially 0; each array element occupies 4 bytes; all array elements are signed 32-bit integers; branch delay slots are not used.

Complete the following MIPS assembly code by filling in blanks (1)–(8). Each blank represents one instruction or operand.

```
        addi $t0, $zero, 0
LOOP:   slti $t1, $t0, (1)
        beq  $t1, $zero, END
        sll  $t2, $t0, (2)
        add  $t3, $s0, $t2
        (3)
        addi $t5, $zero, 4
        slt  $t6, $t5, $t4
        (4)
        (5)
SKIP:   addi $t0, $t0, (6)
        (7)
END:    (8)
```

(a) Fill in blanks (1)–(4) to implement the loop condition, array addressing, and conditional branch.

(b) Fill in blanks (5)–(8) to complete the program. For blank (8), use nop to mark the end of the program.

(c) Determine the final value stored in $s1 after executing the program.

### Answer 4

| Blank | Answer | Purpose |
| --- | --- | --- |
| (1) | 5 | Loop condition: i < 5 |
| (2) | 2 | Multiply array index by 4 |
| (3) | lw $t4, 0($t3) | Load A[i] |
| (4) | beq $t6, $zero, SKIP | Skip addition if A[i] ≤ 4 |
| (5) | add $s1, $s1, $t4 | Update sum |
| (6) | 1 | Increment loop index |
| (7) | j LOOP | Repeat loop |
| (8) | nop | No operation |

- (c) Only elements greater than 4 are added：sum = 7 + 8 = **15** → **$s1 = 15**

---

## Q5. Single-Cycle Datapath Analysis

Consider a standard MIPS single-cycle datapath supporting R-type, lw, sw, beq, and addi instructions. Assume the following initial register values:

| Register | Value |
| --- | --- |
| $s0 | 100 |
| $s1 | 20 |
| $s2 | 5 |
| $t0 | 0 |
| $t1 | 0 |

The following instructions are executed using the initial register values.

```
I1: add  $t0, $s0, $s1
I2: lw   $t1, 8($s0)
I3: beq  $s1, $s2, TARGET
```

Assume Mem[108] = 75 and that all memory addresses are byte addresses.

(a) Complete the following two tables for instructions I1–I3. Some control signal values are provided as hints. Use X for don't-care values.

| Instruction | RegDst | ALUSrc | MemtoReg | RegWrite |
| --- | --- | --- | --- | --- |
| I1: add | **1** | ? | ? | **1** |
| I2: lw | ? | **1** | ? | ? |
| I3: beq | ? | ? | **X** | ? |

| Instruction | MemRead | MemWrite | Branch | ALUOp |
| --- | --- | --- | --- | --- |
| I1: add | ? | **0** | ? | ? |
| I2: lw | **1** | ? | ? | **00** |
| I3: beq | ? | ? | **1** | ? |

(b) For instructions I1 and I2, determine: 1. The two ALU input values. 2. The ALU result. 3. The destination register and the value written to it.

### Answer 5

| Instruction | RegDst | ALUSrc | MemtoReg | RegWrite | MemRead | MemWrite | Branch | ALUOp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1: add | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 10 |
| I2: lw | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 00 |
| I3: beq | X | 0 | X | 0 | 0 | 0 | 1 | 01 |

- (b) I1：ALU inputs A = 100, B = 20；result 100 + 20 = **120**；**$t0 = 120**
  I2：ALU inputs A = 100, B = 8；effective address 100 + 8 = **108**；Mem[108] = 75 → **$t1 = 75**

---

## Q6. Single-Cycle Datapath Performance

Consider a MIPS single-cycle processor supporting R-type (add, sub), Load (lw), Store (sw), and Branch (beq) instructions. The delays of the datapath components are given below.

| Component | Delay (ps) |
| --- | --- |
| Instruction Memory | 200 |
| Register File Read | 100 |
| ALU | 150 |
| Data Memory | 250 |
| Register File Write | 100 |
| Sign Extension | 50 |
| Multiplexer (MUX) | 30 |

Assume the following critical paths for each instruction type.

| Instruction | Components on Critical Path |
| --- | --- |
| R-type | Instruction Memory → Register File Read → MUX → ALU → MUX → Register File Write |
| lw | Instruction Memory → Register File Read → MUX → ALU → Data Memory → MUX → Register File Write |
| sw | Instruction Memory → Register File Read → MUX → ALU → Data Memory |
| beq | Instruction Memory → Register File Read → ALU → MUX |

For this exercise, calculate each path delay by summing the listed component delays. Ignore other delays and parallel execution effects.

(a) Datapath Execution Flow — Based on Table 2, briefly explain the function of each datapath component involved in executing the following three instruction types: 1. R-type (add) 2. Load (lw) 3. Store (sw). For each instruction, describe how data flows through the datapath and how the final result is handled.

(b) Critical Path and Clock Cycle Time — Calculate the critical path delay for each instruction type (R-type, lw, sw, and beq). Determine the minimum clock cycle time of the single-cycle processor and identify the instruction that determines it.

(c) Datapath Improvement and Speedup — Suppose the Data Memory delay is reduced from 250 ps to 150 ps, while all other component delays remain unchanged. Calculate: 1. The new minimum clock cycle time. 2. The overall processor speedup.

### Answer 6

- (a) R-type (add)：Instruction Memory fetches the instruction → Register File reads two source registers → MUX selects the second register value as the ALU input → ALU performs addition → MUX selects the ALU result for write-back → Register File writes the result into the destination register.
  Load (lw)：Instruction Memory fetches → Register File reads the base address register → MUX selects the sign-extended immediate → ALU calculates the effective address → Data Memory reads data → MUX selects the memory data for write-back → Register File writes the loaded value.
  Store (sw)：Instruction Memory fetches → Register File reads the base address register and the register containing the data to store → MUX selects the sign-extended immediate → ALU calculates the effective address → Data Memory writes the register value to the calculated address.
- (b) T_R = 200 + 100 + 30 + 150 + 30 + 100 = **610 ps**；T_lw = 200 + 100 + 30 + 150 + 250 + 30 + 100 = **860 ps**；T_sw = 200 + 100 + 30 + 150 + 250 = **730 ps**；T_beq = 200 + 100 + 150 + 30 = **480 ps**；T_clock = max = **860 ps**；critical instruction: **lw**
- (c) New delays：R-type 610, lw 760, sw 630, beq 480 → T_clock,new = **760 ps**；Speedup = 860 / 760 ≈ **1.132**（約 13.2% higher performance）

---

## Q7. Pipeline Timing and Performance

Consider a processor with a standard five-stage MIPS pipeline: IF → ID → EX → MEM → WB. The processor executes the following instructions:

```
I1: lw   $t0, 0($s0)
I2: add  $t1, $s1, $s2
I3: sub  $t2, $s3, $s4
I4: sw   $t1, 4($s0)
I5: and  $t3, $t4, $t5
```

Assume that each stage takes one clock cycle, the pipeline is initially empty, and instructions are issued in program order without stalls. For timing purposes, every instruction passes through all five stages.

(a) Pipeline Stage Analysis — For Cycle 3 and Cycle 5, identify which instruction occupies each pipeline stage (IF, ID, EX, MEM, and WB). Write "None" if a stage is empty.

(b) Pipeline Performance — Assume each pipeline stage takes 200 ps, and ignore pipeline register overhead. Calculate: 1. The total execution time for five instructions using a single-cycle processor. 2. The total execution time using a five-stage pipelined processor. 3. The speedup achieved by pipelining.

### Answer 7

| Pipeline Stage | Cycle 3 | Cycle 5 |
| --- | --- | --- |
| IF | I3 (sub) | I5 (and) |
| ID | I2 (add) | I4 (sw) |
| EX | I1 (lw) | I3 (sub) |
| MEM | None | I2 (add) |
| WB | None | I1 (lw) |

- (b) T_single = 5 × 200 = 1000 ps per instruction → T_total,single = 5 × 1000 = **5000 ps**；Cycles = k + n − 1 = 5 + 5 − 1 = 9 → T_total,pipeline = 9 × 200 = **1800 ps**；Speedup = 5000 / 1800 = **2.78**

---

## Q8. Pipelined Datapath and Control Signals

Consider a standard five-stage MIPS pipelined processor: IF → ID → EX → MEM → WB. The processor supports R-type, lw, sw, and beq instructions. The control signals are generated during the ID stage and passed through the appropriate pipeline registers.

```
I1: lw   $t0, 8($s0)
I2: add  $t1, $s1, $s2
I3: sw   $t1, 12($s0)
```

Assume that the pipeline operates without stalls or hazards, and that each instruction advances one stage per clock cycle.

(a) Pipeline Control Signal Classification — Complete the following table by identifying the pipeline stage in which each control signal is used. Use EX, MEM, or WB.

| Control Signal | Pipeline Stage |
| --- | --- |
| RegDst | ? |
| ALUSrc | EX |
| ALUOp | ? |
| Branch | ? |
| MemRead | ? |
| MemWrite | MEM |
| RegWrite | ? |
| MemtoReg | ? |

(b) Pipeline Register and Control Signal Analysis — For instruction I1 (lw $t0, 8($s0)), answer: 1. Which pipeline register carries the control signals from ID to EX? 2. Which pipeline register carries the memory control signals from EX to MEM? 3. Which pipeline register carries the write-back control signals from MEM to WB? For each pipeline register, identify the relevant control signals and their values for the lw instruction.

### Answer 8

| Control Signal | Pipeline Stage |
| --- | --- |
| RegDst | EX |
| ALUSrc | EX |
| ALUOp | EX |
| Branch | MEM |
| MemRead | MEM |
| MemWrite | MEM |
| RegWrite | WB |
| MemtoReg | WB |

- (b) 1. **ID/EX**：carries the control signals required by EX, MEM, and WB. For lw — EX: RegDst = 0, ALUSrc = 1, ALUOp = 00；MEM: Branch = 0, MemRead = 1, MemWrite = 0；WB: RegWrite = 1, MemtoReg = 1
  2. **EX/MEM**：carries the MEM and WB control signals. For lw — MEM: Branch = 0, MemRead = 1, MemWrite = 0；WB: RegWrite = 1, MemtoReg = 1
  3. **MEM/WB**：carries the WB control signals. For lw — WB: RegWrite = 1, MemtoReg = 1
