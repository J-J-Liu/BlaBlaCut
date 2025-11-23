# Titan-I: An Open-Source, High Performance RISC-V Vector Core 通俗讲解

### 0. 整体创新点通俗解读

**痛点直击 (The "Why")**

现代的向量处理器（Vector Processor）正处在一个尴尬的境地。一方面，像 **GP-GPU** 这样的设备虽然算力强大，但它们的 **SIMT** 编程模型极其复杂，程序员得操心 warp、shared memory 对齐这些底层细节，而且其控制逻辑（成千上万个线程前端）非常臃肿，浪费了大量面积和功耗。另一方面，传统的 **OoO CPU** 核心为了挖掘 **ILP**（指令级并行），塞满了庞大的 **ROB**（重排序缓冲区）、复杂的分支预测器和一致性协议，这些“投机”开销在处理结构化、高并行的向量负载时显得笨重且低效。

- 现有的 **RISC-V Vector **(RVV) 实现，比如 **SpacemiT X60** 或 **SiFive P870**，要么受限于 **flip-flop** 寄存器文件而无法扩展 **VLEN**（向量长度）和 **DLEN**（数据通路宽度），要么像 **ETH's Ara** 那样干脆放弃了 **ILP**，变成了一个简单的 in-order 流水线，导致硬件利用率低下。
- 当你试图把 **DLEN** 做宽（比如 1024-bit 甚至更宽）来提升 **DLP**（数据级并行）时，会立刻撞上两堵墙：一是 **跨 Lane 数据路由**（尤其是 permutation 指令）会产生巨大的延迟和布线拥塞；二是 **mask register **(v0) 的广播需求会让所有 Lane 互相争抢带宽，形成瓶颈。
- 更要命的是，即使你有了超宽的数据通路，如果缺乏精细的 **ILP** 调度能力，一条长向量指令就会独占整个核心几百甚至上千个周期，后面的指令只能干等着，硬件资源被严重浪费。

简而言之，业界缺少一个既能像 GPU 一样高效处理海量数据，又能像 CPU 一样聪明地乱序执行、榨干硬件利用率，并且还保持 RVV 简洁编程模型的“两全其美”的设计。

---

**通俗比方 (The Analogy)**

想象你要在一个巨大的仓库（**VRF**, Vector Register File）里处理成吨的货物（**vector elements**）。这个仓库被划分成很多个独立的区域（**Lanes**）。

- **GP-GPU 的做法**就像是雇了几千个工人（threads），每人负责一小堆货。但协调这几千人需要一个庞大的调度中心（warp scheduler），而且工人们经常因为要拿同一排货架上的东西而打架（bank conflict），效率并不高。
- **传统 OoO CPU 的做法**则像是只有一个超级工人，但他脑子里记着一张巨复杂的任务清单（ROB），时刻想着下一步该做什么、会不会出错。处理小包裹很灵活，但面对一整集装箱的同质货物时，他那套复杂的思考流程反而成了累赘。

**Titan-I **(T1) 的思路完全不同。它更像是建立了一套高度自动化的智能物流系统：
1.  它把仓库（VRF）本身设计得非常高效，并且给每个区域（Lane）配备了专用的、可并行工作的机器人（VFUs）。
2.  为了解决跨区域调货（permutation）的难题，它没有让机器人自己跑来跑去，而是在仓库中央建了一个超高速的 **分拣中心 **(Permutation Unit)，所有需要重组的货物都通过传送带送到这里，瞬间完成重新打包和分发。
3.  为了防止每次发货都要广播通知所有区域（mask broadcast），它在分拣中心旁边设了一个 **mask 缓存 **(Shadow Mask v0)，任何区域需要 mask 信息时直接去缓存拿就行，不用再惊动整个仓库。
4.  最关键的是，它的调度系统（Sequencer + Scoreboards）非常聪明，能将一连串相关的任务（比如 load -> compute -> store）像流水线一样 **精细地拆解和重叠 **(fine-grained chaining)，让不同区域的机器人可以同时处理任务的不同阶段，而不是傻等上一个任务完全结束。



![](images/8e182bd2d0d71541e047f16294d69aa3d3923d4b22e4c7793877fbe9c78d3caa.jpg)

*Figure 3: Architecture of T1*



---

**关键一招 (The "How")**

作者并没有从零开始造一个全新的轮子，而是在经典的 **lane-based** 向量架构基础上，精准地插入了几个关键的“微创新”，一举打通了 **ILP** 和 **DLP** 的任督二脉。

- **为 DLP 扫清障碍**:
  - **Datapath-wide Permutation Unit**: 用一个专用的、与数据通路同宽的硬件单元来处理所有 permutation 操作，彻底绕开了跨 Lane 路由的性能悬崖。
  - **Shadow Mask v0**: 将分布式的 mask register `v0` 在 permutation unit 中做一份缓存，消除了 predicated execution 时的全局广播瓶颈。
  - **Coarse-grained Floor-planning Solver**: 通过一个启发式布局算法，优化物理上 Lane 的摆放位置，最小化 widen/narrow 等操作中最坏情况下的跨 Lane 延迟。

- **为 ILP 注入灵魂**:
  - **Fine-grained Chaining**: 这是最核心的一招。T1 的依赖追踪不是以整个向量寄存器为单位，而是细化到 **ELEN × ScaleFactor** 的粒度。这意味着，只要一个向量中的一部分元素计算完成了，后续依赖这些元素的指令就可以立即开始执行，而不用等整个向量都算完。这极大地提升了硬件的并发利用率。
  - **Issue-as-commit for Scalar-Vector OoO**: 允许标量和向量流水线在没有真实数据依赖的情况下各自独立前进。向量指令一旦发出（issue），标量核心就认为它已经提交（commit），可以继续执行后续的标量指令，从而避免了不必要的停顿。
  - **Memory Interleaving & Delay Slots**: 通过分离的 Load/Store 单元和冲突检测表（CRT），允许不冲突的 load 和 store 指令同时进行；对于高延迟的 indexed access，则利用 delay slot 让独立的计算指令在其后并发执行，有效隐藏了内存延迟。

正是这些看似微小但极其精准的设计，让 T1 能够在 **40%** 的面积下击败 **Nvidia 3090/5090**，并在 HPC 负载上展现出远超现有 RVV 核心的性能和能效。它证明了，在正确的微架构设计下，一个开放的、可编程的向量核心完全可以成为 GP-GPU 在特定领域的一个强大替代品。

### 1. Coarse-Grained Floor-Planning Solver (ELI5)

**痛点直击**
- 在传统的 **lane-based** 向量处理器设计中，当数据需要在不同 **Lane** 之间移动时（比如执行 **widen** 或 **narrow** 指令），物理布线就成了大问题。想象一下，如果32个 **Lane** 像棋盘一样简单地从左到右、从上到下排列，那么位于对角线两端的 **Lane**（比如 **Lane 3** 和 **Lane 17**）要通信，信号就得横穿整个芯片。
- 这种“最坏情况”下的长距离通信会带来巨大的 **延迟** 和 **功耗**，并且会成为整个设计的性能瓶颈。随着 **DLEN**（数据通路宽度）和 **Lane** 数量的增加，这个问题会指数级恶化，最终让设计师不敢再扩大规模。

**通俗比方**
- 这就像规划一个大型物流仓库。如果你把所有货架（**Lane**）按顺序一排排摆好，那么从A区最左边取货送到Z区最右边，叉车（数据信号）就得跑完整个仓库，效率极低。
- 一个好的仓库经理（**Coarse-Grained Floor-Planning Solver**）不会这么干。他会把经常需要互相调货的区域（比如处理相同类型数据的 **Lane**）尽量安排在一起，形成一个个小集群。这样，大部分内部调货都在小范围内完成，只有少数跨集群的调货才需要跑远路，从而大大降低了平均和最坏情况下的运输时间。

![](images/5f5b8c9d4e3a2f1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7.jpg)

*图：论文中的 **Figure 5** 清晰地展示了这一点。左边是“**Trivial Floorplan**”（朴素布局），最大通信延迟高达 **7** 个单位；右边是他们的“**Novel Floorplan**”（新式布局），通过智能摆放，将最大延迟降到了 **4** 个单位。*

**关键一招**
- 作者没有采用计算复杂度极高的全局最优算法（那在工程上不现实），而是设计了一个聪明的 **启发式（heuristic）求解器**。
- 这个求解器的核心逻辑是：
  - 它知道哪些 **Lane** 对之间通信最频繁（比如执行 **widen/narrow** 时，`i` 号 **Lane** 需要和 `(2i mod n)` 及 `(2i+1 mod n)` 号 **Lane** 通信）。
  - 在放置一个新的 **Lane** 时，如果它已经有邻居被放置了，求解器就把它放在能 **最小化到这些已放置邻居的最大距离** 的位置上。
  - 如果还没有邻居，就随机放在现有布局的旁边。
- 通过这种 **局部优化驱动全局布局** 的策略，它用很低的计算成本，就找到了一个能让 **最坏情况路由距离** 显著缩短的物理布局方案，从而直接将 **widen/narrow** 操作的延迟降低了近 **20%**。

### 2. Datapath-Wide Permutation Unit (ELI5)

**痛点直击**
- 在传统的 **lane-based** 向量处理器里，做 **permutation**（比如 `VRGATHER`、`VCOMPRESS`）是个老大难问题。因为数据是分散在各个 **lane** 里的，要重组就得跨 **lane** 搬运。
- 最朴素的办法是什么？把数据从所有 **lane** 的 **VRF**（向量寄存器堆）里读出来，写到一块共享的 **local memory** 里，排好队再读回去。这叫 **memory-swap emulation**。
- 这个过程有多“难受”？
  - **性能杀手**：一次 **permutation** 变成了两次昂贵的 **VRF** 读写外加一次 **local memory** 访问，**latency** 飞涨。
  - **带宽黑洞**：宝贵的 **VRF** 和 **local memory** 带宽被这种“内部调度”给占满了，真正的计算指令只能干等着。
  - **扩展性差**：**lane** 越多，跨 **lane** 通信越复杂，这个瓶颈就越严重，直接限制了 **DLEN**（数据通路宽度）的扩展。

**通俗比方**
- 想象一个大型物流仓库（**VRF**），被分成了很多个独立的区域（**lane**）。现在你需要把散落在各个区域的包裹（**vector elements**）按照一个新的订单（**permutation pattern**）重新打包。
- 旧方法就像：让每个区域的工人先把包裹搬到中央分拣大厅（**local memory**），等所有包裹都到齐了，再由另一批工人按新订单重新分拣，最后送回各个区域。整个过程慢、占地、还容易堵。
- **Titan-I** 的 **Datapath-Wide Permutation Unit** 相当于在仓库内部架设了一套**全自动、全覆盖的空中传送带系统**（**crossbar**）。这套系统能直接连通任意两个区域，包裹可以在区域内直接通过传送带飞到目标区域，完全不需要经过中央大厅。整个过程又快又高效，还不占用地面空间。

**关键一招**
- 作者没有去优化那个低效的“搬进搬出”流程，而是**从根本上绕开了它**。
- 他们在芯片物理布局的中心位置，**硬生生地塞进去一个与整个数据通路同宽（DLEN-sized）的 crossbar 开关矩阵**，这就是 **Permutation Unit**。
- 这个单元如何工作？
  - 当一条 **permutation** 指令到来时，**Sequencer** 会通知所有 **lane** 准备好它们的数据。
  - 所有 **lane** 同时将数据发送到这个中央 **Permutation Unit**。
  - **Permutation Unit** 内部的 **crossbar** 根据指令要求（静态或动态的索引），**在一个周期内**就完成了所有数据的重排和路由。
  - 重排后的数据直接从 **Permutation Unit** 广播回各个 **lane**。
- 这个设计的精妙之处在于：
  - **原生支持**：把 **permutation** 从一个需要多次内存访问的“软件模拟”操作，变成了一个**单周期硬件原语**。
  - **带宽无损**：数据只在 **lane** 和 **Permutation Unit** 之间流动一次，**VRF** 和 **local memory** 的带宽得以完全释放给计算任务。
  - **可扩展**：通过增加 **crossbar** 的流水线级数，可以很好地控制其延迟和面积开销，使其能随着 **DLEN** 的增大而线性扩展，如 

![](images/46a530743c1b53db2bcd8a0209fb28091509950010deb733536533ab34d1b06c.jpg)

*(a) VLEN*

 (b) 所示。

### 3. Shadow Cache for Mask Register (v0) (ELI5)

**痛点直击**
- 在传统的 **lane-based** RISC-V Vector 设计中，**mask register (v0)** 被物理地切分并**均匀分布**到所有 **Lane** 上。
- 当一条 **predicated instruction**（带掩码的指令）需要使用 **v0** 时，它往往需要从**多个不同的 Lane** 中实时收集对应的掩码位。例如，处理一个 32-bit 元素可能需要从 3 个甚至 4 个 Lane 里“拼凑”出完整的掩码信息。
- 这种跨 Lane 的数据请求会产生海量的**点对点广播流量**，在 Lane 数量很多（即 **DLEN** 很宽）时，会瞬间**塞爆片上互连网络**，形成严重的性能瓶颈，也就是论文里说的 “**wiring bottleneck**”。

**通俗比方**
- 想象一下，你是一家大型连锁超市（Vector Core）的经理，要给所有分店（Lane）发一个“今日特价商品清单”（mask v0）。
- 旧方法是：每当某个分店要搞促销（执行 predicated instruction），它就得打电话给总部，然后总部再挨个问其他所有分店：“你们那部分清单是什么？”，最后把信息拼起来告诉它。这个过程极其低效，电话线（片上互连）全被占满了。
- T1 的做法是：总部（Permutation Unit）自己维护一份**完整、最新的特价清单副本**（Shadow Cache）。任何分店需要时，直接找总部拿就行，**避免了分店之间互相打电话骚扰**，整个系统流畅多了。

**关键一招**
- 作者没有改变 mask register 的物理分布方式，而是在 **Permutation Unit** 这个中心枢纽里，增加了一个专门的 **Shadow Mask (v0) Cache**。
- 这个缓存会**被动地**被各个 Lane 更新：当任何一条指令修改了 **v0** 的一部分，对应的 Lane 就会通过一个专用的数据通道，将更新同步到 Permutation Unit 的 Shadow Cache 里。
- 同时，**Sequencer**（调度器）扮演了“交通警察”的角色，它会跟踪所有对 **v0** 的写操作，确保在所有 pending 的写操作完成之前，依赖 **v0** 的新指令不会被执行，从而保证了数据一致性。
- 通过这个设计，所有需要读取 **v0** 的指令都变成了**本地读取**（从 Permutation Unit 到自己的 Lane），彻底**消除了跨 Lane 的广播风暴**。论文提到，这能减少高达 **4 × VLEN/ELEN** 次的 VRF 读操作，从而将带宽提升了约 **50%**，而面积开销仅为 **8%**。



![](images/46a530743c1b53db2bcd8a0209fb28091509950010deb733536533ab34d1b06c.jpg)

*(a) VLEN*



### 4. Fine-Grained Chaining Microarchitecture (ELI5)

**痛点直击**
- 传统的向量处理器在处理长向量时，就像一条僵硬的流水线：一个指令必须等前一个指令把**整个**超宽结果（可能几千位）完全写回 **VRF (Vector Register File)** 后，自己才能开始。这造成了两个“很难受”的问题：
  - **巨大的延迟气泡**：即使新指令只依赖旧指令结果的一小部分，也得干等着全部写完。
  - **VRF 带宽浪费**：VRF 的读写端口很宽，但因为写入是“整块”进行的，无法被后续不相关的、只需要部分数据的指令充分利用，导致硬件资源闲置。

**通俗比方**
- 想象你在组装一台复杂的机器，需要用到一个由100个零件组成的大型预制模块A。传统做法是：工人1必须把模块A的**所有100个零件**都放到工作台上并固定好后，工人才能开始用其中的几个零件去组装下一个模块B。
- **Fine-Grained Chaining**的做法则聪明得多：工作台被划分成很多小格子（对应 **lane datapath granularity**）。工人1每放好一个零件到对应的小格子里，系统就立刻通知所有等待的工人：“嘿，A模块的第5号零件好了！”。如果工人2正好需要这个零件，他就可以立刻拿走开工，根本不用等剩下的99个零件。这就像是把一个笨重的整体交接，拆解成了灵活的、按需的“零件级”交接。

**关键一招**
- 作者并没有改变向量指令的基本执行流程，而是在 **VRF 写回阶段**和**指令调度逻辑**之间，巧妙地插入了一个**细粒度的依赖追踪器**（即文中提到的 **Chaining Scoreboard**）。
  - 这个追踪器不再以“整个向量寄存器”为单位记录写完成状态，而是将其拆分成更小的块（**ELEN × ScaleFactor-bit**，例如64位或128位）。
  - 当一个向量指令的部分结果（比如某个 lane 的计算结果）准备好后，它会立即更新追踪器中对应小块的状态为“可用”。
  - 调度器在派发后续指令时，会检查其所有输入依赖的小块是否都已“可用”。只要满足，该指令就可以**立即启动**，甚至可以在前一个指令的其他部分还在计算时就开始执行。
  - 这直接实现了 **Out-of-Order Writebacks**，让 VRF 的多个读写端口能被不同指令的、不相关的数据块同时使用，从而**最大化 VRF 带宽利用率**。



![](images/8e182bd2d0d71541e047f16294d69aa3d3923d4b22e4c7793877fbe9c78d3caa.jpg)

*Figure 3: Architecture of T1*



这种设计的核心思想就是“**化整为零，按需供给**”，将粗粒度的、阻塞式的向量处理，转变为细粒度的、流水线式的高效协作，从根本上解决了长向量处理中的延迟和带宽瓶颈问题。

### 5. Issue-as-Commit for Scalar-Vector OoO Execution (ELI5)

**痛点直击 (The "Why")**
- 传统的 **Scalar-Vector OoO Execution** 模型里，**scalar core** 和 **vector core** 虽然物理上分开，但逻辑上耦合得很死。只要 vector pipeline 开始干活，scalar core 就得在旁边干等着，直到这个 vector 指令**完全执行完、写回寄存器、正式 commit** 之后，scalar core 才敢继续。
- 这种“全有或全无”的等待策略非常低效。因为大部分 vector 指令（比如 `vadd.vv`）根本不会修改 scalar registers 或影响控制流，它们只是在自己的 **VRF (Vector Register File)** 里捣鼓数据。让 scalar core 为这种“井水不犯河水”的操作白白 stall 几十个甚至上百个周期，简直是巨大的资源浪费。
- 简单说，痛点就是：**不必要的序列化**。系统明明有足够的并行能力（scalar 和 vector 的功能单元都闲着），却被一个过于保守的提交模型给锁死了。

**通俗比方 (The Analogy)**
- 想象你和你的同事在一个开放式办公室里工作。你的任务是处理一堆文件（scalar work），他的任务是用一台大型打印机批量打印图纸（vector work）。
- 旧的做法是：只要他按下“开始打印”按钮，你就必须立刻放下手里的所有活，站在他旁边盯着打印机，直到最后一张纸吐出来、他签完字确认无误（commit）后，你才能回去干自己的事。这显然很蠢，因为你俩的工作完全不冲突。
- **Issue-as-Commit** 的做法是：他一按下“开始打印”按钮（issue），你就知道“哦，他要忙一阵子了，但这事儿跟我没关系”，于是你立刻回到自己工位继续处理文件。同时，办公室里有个简单的白板（**compact scoreboards**）记录着“打印机任务已启动，预计还需要X分钟”。只有当他打印的图纸里包含了你需要签字的封面页（即 vector 指令真的要写 scalar register 时），你才会被通知暂停一下。这就是高效的并行协作。

**关键一招 (The "How")**
- 作者没有改变整个 OoO 引擎的核心，而是巧妙地**重新定义了 vector 指令的“提交”时刻**。
- **核心逻辑转换**：对于绝大多数只在 VRF 内部操作的 vector 指令，它们的“提交”不再是等到写回完成，而是在它们被成功分发（**issue**）到 vector pipeline 的那一刻就算完成了。
- 为了支撑这个大胆的假设，作者引入了一个轻量级的 **vector scoreboard**。这个 scoreboard 不负责追踪复杂的依赖关系，它的唯一作用就是告诉 scalar core：“放心，这个 vector 指令已经安全地进入流水线了，它不会影响你，你可以继续往前跑”。
- 当然，这个策略有例外。如果一个 vector 指令确实需要写 scalar register（比如 `vmv.x.s`）或者可能抛出异常，那么它还是会走传统的、更严格的提交流程，确保正确性。但对于占绝大多数的纯 vector 计算指令，这个“**issue-as-commit**”的策略极大地解放了 scalar core，让它能与 vector core 真正地 **overlap execution**，从而显著提升了整体吞吐量。正如文中所说，这套机制只给 scalar core 增加了约 **3%** 的面积开销，却换来了巨大的性能收益。

![](images/60122021119a97f1361bb7dfdeba64da96d256850b9ec88b66255c7d3c530fac.jpg)

*Figure 6: Different ILP Technology in T1. Chaining interleaves V0, V1, and V2. Memory Interleaving mitigates the VSW-VLD dependency. Vector-Scalar OoO interleaves the vector and scalar pipelines until a true dependency v16-s64-v15 occurs. Memory Delay Slot parallelizes vector index load/store (VIDX0) with independent vector executions (VEX0).*



### 6. Dual LSU with Memory Interleaving and Delay Slots (ELI5)

**痛点直击 (The "Why")**
- 传统的 Vector Core 通常只有一个 LSU（Load-Store Unit），它必须处理所有类型的内存访问模式：简单的 **unit-stride**（连续地址）、复杂的 **indexed/strided**（非连续、跳跃式）以及 **segment**（一次操作多个寄存器）。
- 这导致了两个核心矛盾：
  - **带宽浪费**：对于最高效的 **unit-stride** 访问，由于 load 和 store 操作不能同时进行（通常是交替执行），宝贵的内存总线带宽被浪费了一半。想象一下，你有一条双向八车道的高速公路，但每次只允许一个方向通车。
  - **延迟灾难**：对于 **indexed** 访问，每个元素的地址都需要从向量寄存器中读取，这会产生海量的、随机的内存请求。这些请求的延迟极高（可能成千上万个周期），而传统的顺序执行会让整个向量流水线完全卡死，直到所有数据都返回，CPU 只能干等。

**通俗比方 (The Analogy)**
- 把 T1 的内存子系统想象成一个现代化的物流中心。
  - **HBLSU (High Bandwidth LSU)** 就像一条高度自动化的 **“集装箱专线”**。它专门处理大批量、规则堆放的货物（**unit-stride** 数据）。这条专线有独立的 **进货（load）和出货（store）通道**，可以同时工作，互不干扰，效率拉满。
  - **HOLSU (High Outstanding LSU)** 则像是一个灵活的 **“快递分拣站”**。它处理的是地址分散、包裹各异的订单（**indexed/strided** 数据）。这个分拣站不会因为一个偏远地区的包裹没到就停止所有工作，而是会先处理手头其他能处理的订单，并且允许后台继续接收新订单，把等待时间（延迟）隐藏起来。
- **Memory Interleaving** 就是让“集装箱专线”的进货和出货通道 **同时运转**。
- **Delay Slots** 就是给“快递分拣站”配备了 **智能调度系统**，让它在等待慢速包裹时，能立刻切换去处理其他不相关的任务。

**关键一招 (The "How")**
- 作者没有试图用一个“全能”但平庸的 LSU 去应付所有场景，而是进行了 **功能解耦**，设计了两个高度专业化的 LSU。
- **对于高带宽场景 (HBLSU + Memory Interleaving)**：
  - 作者引入了一个 **Conflict Region Table (CRT)**。当一个 load 或 store 指令进入 HBLSU 时，CRT 会记录下它要访问的内存区域。
  - 后续的指令在发射前会查询 CRT。如果它的访问区域与正在处理的指令 **不冲突**，那么它就可以 **立即发射**，即使前一个指令还没完成。
  - 这样，load 和 store 指令就能 **真正并发** 地使用各自的内存通道，将理论带宽利用率从 50% 提升到接近 100%。

![](images/60122021119a97f1361bb7dfdeba64da96d256850b9ec88b66255c7d3c530fac.jpg)

*Figure 6: Different ILP Technology in T1. Chaining interleaves V0, V1, and V2. Memory Interleaving mitigates the VSW-VLD dependency. Vector-Scalar OoO interleaves the vector and scalar pipelines until a true dependency v16-s64-v15 occurs. Memory Delay Slot parallelizes vector index load/store (VIDX0) with independent vector executions (VEX0).*


- **对于高延迟场景 (HOLSU + Delay Slots)**：
  - HOLSU 被设计成可以维持 **大量（High Outstanding）** 的未完成内存请求。
  - 更关键的是，作者利用了 RVV 的特性，通过一个 **CSR “chicken bit”** 来告诉硬件：对于某些已知安全的 **indexed** 操作，可以 **忽略精确异常**。
  - 一旦这个开关打开，后续 **不依赖于该 indexed 操作结果** 的指令就可以被 **立即发射和执行**，就像在指令流中人为开辟了一个 **“延迟槽（Delay Slot）”**，让计算单元在等待内存数据时也能保持忙碌，从而将漫长的内存延迟完美地“藏”在了有用的计算工作之下。

![](images/60122021119a97f1361bb7dfdeba64da96d256850b9ec88b66255c7d3c530fac.jpg)

*Figure 6: Different ILP Technology in T1. Chaining interleaves V0, V1, and V2. Memory Interleaving mitigates the VSW-VLD dependency. Vector-Scalar OoO interleaves the vector and scalar pipelines until a true dependency v16-s64-v15 occurs. Memory Delay Slot parallelizes vector index load/store (VIDX0) with independent vector executions (VEX0).*



这种双管齐下的策略，让 T1 在面对不同 workload 时都能发挥出极致的内存子系统性能，这也是它能在 HPC 和 Cryptography 等内存密集型任务上大幅领先的关键。如 Table 1 所示，仅 **Memory Interleaving** 一项技术就能带来 **32%** 的性能提升。

| 配置 | Cycles | Slow Down |
| :--- | :--- | :--- |
| Standard T1 | 14817 | - |
| Disable Chaining | 23862 | 61% |
| **Disable Memory Interleaving** | **19514** | **32%** |
