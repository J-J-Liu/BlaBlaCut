# Recent Papers

最近收录的论文笔记，欢迎阅读~

本页面共收录了 21 篇论文笔记。

## APT-GET: Profile-Guided Timely Software Prefetching
> **Authors:** Saba Jamilan, Tanvir Ahmed Khan, Grant Ayers, et al.  
> **Affiliations:** University of California, Santa Cruz, University of Michigan, Google  
> **Venue:** EuroSys 2022

论文提出APT-GET，一种基于硬件性能计数器（如Intel LBR）的动态profile-guided软件预取技术，通过分析程序执行时间分布自动确定最优预取距离和注入位置，解决传统静态编译预取无法保证时效性的问题。在10个真实应用上平均加速1.30倍，相比现有软件预取方法提升25%。

[📄 论文笔记](../../notes_repo/apt-get-profile-guided-timely-software-prefetching/paper_notes.md) | [📊 图表解析](../../notes_repo/apt-get-profile-guided-timely-software-prefetching/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/apt-get-profile-guided-timely-software-prefetching/ELI5_notes.md) | <a href="https://doi.org/10.1145/3492321.3519583" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## ATR: Out-of-Order Register Release Exploiting Atomic Regions
> **Authors:** Yinyuan Zhao, Surim Oh, Mingsheng Xu, et al.  
> **Affiliations:** University of California, Santa Cruz  
> **Venue:** MICRO 2025

论文提出ATR技术，通过识别不含分支和异常指令的原子提交区域，实现寄存器的安全乱序释放。该方法无需影子寄存器或复杂恢复机制，在SPEC2017int上平均提升5.13%（64项寄存器文件）性能，或在保持性能损失<3%时减少27.1%寄存器文件大小。

[📄 论文笔记](../../notes_repo/atr-out-of-order-register-release-exploiting-atomic-regions/paper_notes.md) | [📊 图表解析](../../notes_repo/atr-out-of-order-register-release-exploiting-atomic-regions/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/atr-out-of-order-register-release-exploiting-atomic-regions/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756135" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Berti: an Accurate Local-Delta Data Prefetcher
> **Authors:** Agustín Navarro-Torres, Biswabandan Panda, Jesus Alastruey-Benedé, et al.  
> **Affiliations:** Universidad de Zaragoza, Indian Institute of Technology Bombay, University of Murcia  
> **Venue:** 10.1109/MICRO56248.2022.00072 2022

论文提出Berti，一种基于本地及时性delta的L1数据缓存预取器。其核心创新在于为每个指令指针(IP)学习高覆盖率的及时性本地delta，而非使用全局delta，从而显著提升准确率。实验表明，Berti仅用2.55KB存储开销，在SPEC CPU2017和GAP负载上相比IP-stride和SOTA预取器IPCP分别提升性能8.5%和3.5%，并减少内存层次动态能耗33.6%。

[📄 论文笔记](../../notes_repo/berti-an-accurate-local-delta-data-prefetcher/paper_notes.md) | [📊 图表解析](../../notes_repo/berti-an-accurate-local-delta-data-prefetcher/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/berti-an-accurate-local-delta-data-prefetcher/ELI5_notes.md)

---

## BOLT: A Practical Binary Optimizer for Data Centers and Beyond
> **Authors:** Maksim Panchenko, Rafael Auler, Bill Nell, et al.  
> **Affiliations:** Facebook, Inc.  
> **Venue:** CGO 2019

论文提出了BOLT，一个基于LLVM的静态二进制优化器，利用采样分析在链接后优化代码布局。其核心创新在于证明了链接后优化能更精准地利用性能分析数据，与编译期FDO/LTO互补。在Facebook数据中心应用上获得最高7.0%加速，在GCC/Clang编译器上获得最高20.4%（启用FDO/LTO时）和52.1%（未启用时）的性能提升。

[📄 论文笔记](../../notes_repo/bolt-a-practical-binary-optimizer-for-data-centers-and-beyond/paper_notes.md) | [📊 图表解析](../../notes_repo/bolt-a-practical-binary-optimizer-for-data-centers-and-beyond/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/bolt-a-practical-binary-optimizer-for-data-centers-and-beyond/ELI5_notes.md)

---

## Drishti: Do Not Forget Slicing While Designing Last-Level Cache Replacement Policies for Many-Core Systems
> **Authors:** Sweta, Prerna Priyadarshini, Biswabandan Panda  
> **Affiliations:** Indian Institute of Technology Bombay  
> **Venue:** MICRO 2025

论文指出在多核系统的切片LLC中，现有先进替换策略（如Hawkeye、Mockingjay）因局部预测器导致短视决策且采样缓存利用率低。为此提出Drishti，包含两项增强：(1) 每核全局重用预测器与每片局部采样缓存结合；(2) 动态选择高缺失率的LLC集合作为采样缓存。在32核系统上，Drishti使Hawkeye和Mockingjay相比LRU的性能提升从3.3%/6.7%提高到5.6%/13.2%，同时减少存储开销。

[📄 论文笔记](../../notes_repo/drishti-do-not-forget-slicing-while-designing-last-level-cache-replacement-policies-for-many-core-systems/paper_notes.md) | [📊 图表解析](../../notes_repo/drishti-do-not-forget-slicing-while-designing-last-level-cache-replacement-policies-for-many-core-systems/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/drishti-do-not-forget-slicing-while-designing-last-level-cache-replacement-policies-for-many-core-systems/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756028" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Feedback Directed Prefetching: Improving the Performance and Bandwidth-Efficiency of Hardware Prefetchers
> **Authors:** Santhosh Srinath, Onur Mutlu, Hyesoon Kim, et al.  
> **Affiliations:** Microsoft, Microsoft Research, The University of Texas at Austin  
> **Venue:** MICRO 2007

论文提出反馈导向预取（FDP）机制，通过动态监控预取准确率、及时性和缓存污染来调整硬件预取器的激进程度和预取块在缓存中的插入位置。该方法在SPEC CPU2000上平均性能提升6.5%，同时减少18.7%内存带宽消耗，消除了传统激进预取在部分基准测试中的严重性能下降问题。

[📄 论文笔记](../../notes_repo/feedback-directed-prefetching-improving-the-performance-and-bandwidth-efficiency-of-hardware-prefetchers/paper_notes.md) | [📊 图表解析](../../notes_repo/feedback-directed-prefetching-improving-the-performance-and-bandwidth-efficiency-of-hardware-prefetchers/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/feedback-directed-prefetching-improving-the-performance-and-bandwidth-efficiency-of-hardware-prefetchers/ELI5_notes.md)

---

## Integrating Prefetcher Selection with Dynamic Request Allocation Improves Prefetching Efficiency
> **Authors:** Mengming Li, Qijun Zhang, Yongqing Ren, et al.  
> **Affiliations:** Hong Kong University of Science and Technology, Intel  
> **Venue:** HPCA 2025

论文提出Alecto，一种结合动态请求分配（DDRA）与细粒度预取器选择的框架，解决了现有方案中需求请求分配不准确和选择标准粗糙的问题。Alecto通过为每个内存访问指令动态分配合适的预取器，显著提升了预取效率。实验表明，Alecto在单核和八核上分别比SOTA的Bandit算法提升2.76%和7.56%，并减少48%的预取器表访问能耗，存储开销小于1KB。

[📄 论文笔记](../../notes_repo/integrating-prefetcher-selection-with-dynamic-request-allocation-improves-prefetching-efficiency/paper_notes.md) | [📊 图表解析](../../notes_repo/integrating-prefetcher-selection-with-dynamic-request-allocation-improves-prefetching-efficiency/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/integrating-prefetcher-selection-with-dynamic-request-allocation-improves-prefetching-efficiency/ELI5_notes.md)

---

## Learning to Walk: Architecting Learned Virtual Memory Translation
> **Authors:** Kaiyang Zhao, Yuang Chen, Xenia Xu, et al.  
> **Affiliations:** Carnegie Mellon University, Meta, Intel  
> **Venue:** MICRO 2025

论文提出Learned Virtual Memory (LVM)，一种基于学习型索引的页表结构，旨在实现高效的单次访问地址翻译。LVM通过动态适应应用虚拟地址空间的规律性，使用轻量级线性模型构建索引，解决了传统页表多级遍历和哈希页表高冲突率的问题。实验表明，LVM相比基数页表平均减少44%的地址翻译开销，提升应用执行速度2-27%，性能接近理想页表（差距<1%）。

[📄 论文笔记](../../notes_repo/learning-to-walk-architecting-learned-virtual-memory-translation/paper_notes.md) | [📊 图表解析](../../notes_repo/learning-to-walk-architecting-learned-virtual-memory-translation/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/learning-to-walk-architecting-learned-virtual-memory-translation/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756093" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Limoncello: Prefetchers for Scale
> **Authors:** Akanksha Jain, Hannah Lin, Carlos Villavieja, et al.  
> **Affiliations:** Google, University of Washington  
> **Venue:** ASPLOS 2024

论文提出Limoncello，一种无需硬件修改的软件系统，在高内存带宽利用率时动态关闭硬件预取器以降低15%内存延迟，并通过大规模硬件消融研究识别出数据中心税函数（如memcpy、压缩、哈希）作为软件预取目标，插入精准软件预取指令。在Google生产集群部署后，应用吞吐量提升10%，同时显著提高CPU利用率。

[📄 论文笔记](../../notes_repo/limoncello-prefetchers-for-scale/paper_notes.md) | [📊 图表解析](../../notes_repo/limoncello-prefetchers-for-scale/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/limoncello-prefetchers-for-scale/ELI5_notes.md) | <a href="https://doi.org/10.1145/3620666.3651373" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## OCOLOS: Online COde Layout OptimizationS
> **Authors:** Yuxuan Zhang, Tanvir Ahmed Khan, Gilles Pokam, et al.  
> **Affiliations:** University of Pennsylvania, University of Michigan, Intel Corporation, University of California, Santa Cruz  
> **Venue:** MICRO 2022

提出了OCOLOS，首个面向非托管语言（如C/C++）的在线代码布局优化系统。它在运行时对进程进行Profile-Guided Optimization（PGO），解决了离线PGO中配置文件过时和代码变更导致映射失效的问题。通过安全的在线代码替换技术，无需修改应用即可加速复杂多线程程序，在MySQL、Verilator和Clang构建上分别实现了最高1.41×、2.20×和1.14×的加速比。

[📄 论文笔记](../../notes_repo/ocolos-online-code-layout-optimizations/paper_notes.md) | [📊 图表解析](../../notes_repo/ocolos-online-code-layout-optimizations/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/ocolos-online-code-layout-optimizations/ELI5_notes.md) | <a href="https://doi.org/10.1109/MICRO56248.2022.00045" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Prodigy: Improving the Memory Latency of Data-Indirect Irregular Workloads Using Hardware-Software Co-Design
> **Authors:** Nishil Talati, Kyle May, Armand Behroozi, et al.  
> **Affiliations:** University of Michigan, University of Edinburgh, University of Wisconsin, Madison  
> **Venue:** HPCA 2021

论文提出Prodigy，一种软硬件协同设计的低开销预取方案，用于加速具有数据间接访问模式（如图计算、稀疏线性代数）的不规则工作负载。其核心是数据间接图（DIG）表示法，结合编译器静态分析与硬件动态预取，仅用0.8KB存储开销，平均性能提升2.6倍，能效提升1.6倍，并优于多种前沿预取器。

[📄 论文笔记](../../notes_repo/prodigy-improving-the-memory-latency-of-data-indirect-irregular-workloads-using-hardware-software-co-design/paper_notes.md) | [📊 图表解析](../../notes_repo/prodigy-improving-the-memory-latency-of-data-indirect-irregular-workloads-using-hardware-software-co-design/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/prodigy-improving-the-memory-latency-of-data-indirect-irregular-workloads-using-hardware-software-co-design/ELI5_notes.md) | <a href="https://doi.org/10.1109/HPCA51647.2021.00061" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Profile-Guided Temporal Prefetching
> **Authors:** Mengming Li, Qijun Zhang, Yichuan Gao, et al.  
> **Affiliations:** Hong Kong University of Science and Technology (HKUST), Intel  
> **Venue:** ISCA 2025

提出Prophet，一种软硬协同的Profile-Guided时序预取框架，通过轻量级计数器分析和动态提示注入，优化片上元数据表管理。相比SOTA硬件预取器Triangel，性能提升14.23%，且能自适应不同输入，开销可忽略。

[📄 论文笔记](../../notes_repo/profile-guided-temporal-prefetching/paper_notes.md) | [📊 图表解析](../../notes_repo/profile-guided-temporal-prefetching/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/profile-guided-temporal-prefetching/ELI5_notes.md) | <a href="https://doi.org/10.1145/3695053.3731070" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Pythia: A Customizable Hardware Prefetching Framework Using Online Reinforcement Learning
> **Authors:** Rahul Bera, Konstantinos Kanellopoulos, Anant V. Nori, et al.  
> **Affiliations:** ETH Zürich, Processor Architecture Research Labs, Intel Labs, TU Delft  
> **Venue:** MICRO 2021

提出Pythia，一个基于在线强化学习的可定制硬件预取框架，能同时利用多种程序特征和系统级反馈（如内存带宽）进行决策。相比MLOP和Bingo，在单核、12核及带宽受限配置下性能分别提升最高3.8%、9.6%和20.2%，且仅增加1.03%面积开销。

[📄 论文笔记](../../notes_repo/pythia-a-customizable-hardware-prefetching-framework-using-online-reinforcement-learning/paper_notes.md) | [📊 图表解析](../../notes_repo/pythia-a-customizable-hardware-prefetching-framework-using-online-reinforcement-learning/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/pythia-a-customizable-hardware-prefetching-framework-using-online-reinforcement-learning/ELI5_notes.md) | <a href="https://doi.org/10.1145/3466752.3480114" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## RICH Prefetcher: Storing Rich Information in Memory to Trade Capacity and Bandwidth for Latency Hiding
> **Authors:** Ningzhi Ai, Wenjian He, Hu He, et al.  
> **Affiliations:** Huawei Technologies Co., Ltd, Tsinghua University  
> **Venue:** MICRO 2025

针对高带宽高容量但高延迟的未来内存系统，提出RICH预取器。其核心创新是利用多尺度空间局部性（2KB/4KB/16KB区域）和多偏移触发机制，在提升覆盖率和及时性的同时保持高准确率。通过片上/片下分层存储元数据以控制开销。实验表明，在常规系统中性能优于Bingo 3.4%；当内存延迟增加120ns时，优势扩大至8.3%。

[📄 论文笔记](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/paper_notes.md) | [📊 图表解析](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756081" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## RnR: A Software-Assisted Record-and-Replay Hardware Prefetcher
> **Authors:** Chao Zhang, Yuan Zeng, John Shalf, et al.  
> **Affiliations:** Lehigh University, Lawrence Berkeley National Lab  
> **Venue:** MICRO 2020

论文提出RnR，一种软件辅助的记录-回放硬件预取器，用于处理具有重复性不规则内存访问模式的应用（如图算法和稀疏迭代求解器）。通过轻量级编程接口，程序员指定数据结构和记录/回放时机，RnR记录首次缓存未命中序列并在后续迭代中回放预取。该方法在图应用上平均加速2.16倍，在稀疏矩阵向量乘法核上加速2.91倍，预取准确率和覆盖率均超95%。

[📄 论文笔记](../../notes_repo/rnr-a-software-assisted-record-and-replay-hardware-prefetcher/paper_notes.md) | [📊 图表解析](../../notes_repo/rnr-a-software-assisted-record-and-replay-hardware-prefetcher/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rnr-a-software-assisted-record-and-replay-hardware-prefetcher/ELI5_notes.md) | <a href="https://doi.org/10.1109/MICRO50266.2020.00057" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## RPG2: Robust Profile-Guided Runtime Prefetch Generation
> **Authors:** Yuxuan Zhang, Nathan Sobotka, Soyoon Park, et al.  
> **Affiliations:** University of Pennsylvania, University of California, Santa Cruz, Columbia University, University of Washington, Google, Intel  
> **Venue:** ASPLOS 2024

RPG2 是一个纯软件的动态预取系统，能在程序运行时自动注入、调优并回滚预取指令。它解决了传统静态预取对输入和微架构敏感的问题，通过在线性能反馈自适应调整预取距离，在CRONO等基准测试中最高获得2.15倍加速，并能有效避免因预取不当导致的性能下降。

[📄 论文笔记](../../notes_repo/rpg2-robust-profile-guided-runtime-prefetch-generation/paper_notes.md) | [📊 图表解析](../../notes_repo/rpg2-robust-profile-guided-runtime-prefetch-generation/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rpg2-robust-profile-guided-runtime-prefetch-generation/ELI5_notes.md) | <a href="https://doi.org/10.1145/3620665.3640396" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## SHADOW: Simultaneous Multi-Threading Architecture with Asymmetric Threads
> **Authors:** Ishita Chaturvedi, Bhargav Reddy Godala, Abiram Gangavaram, et al.  
> **Affiliations:** Princeton University, University of British Columbia, Microsoft, University of California Santa Cruz, AheadComputing  
> **Venue:** MICRO 2025

论文提出SHADOW，首个支持乱序（OoO）与顺序（InO）线程并发执行的非对称SMT架构，动态平衡指令级并行（ILP）与线程级并行（TLP）。通过软件工作窃取机制自适应分配负载，在9个基准测试中相比传统OoO CPU最高提速3.16倍，平均提升1.33倍，仅增加1%面积与功耗开销。

[📄 论文笔记](../../notes_repo/shadow-simultaneous-multi-threading-architecture-with-asymmetric-threads/paper_notes.md) | [📊 图表解析](../../notes_repo/shadow-simultaneous-multi-threading-architecture-with-asymmetric-threads/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/shadow-simultaneous-multi-threading-architecture-with-asymmetric-threads/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756070" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## TEA: Time-Proportional Event Analysis
> **Authors:** Björn Gottschall, Lieven Eeckhout, Magnus Jahre  
> **Affiliations:** Norwegian University of Science and Technology (NTNU), Ghent University  
> **Venue:** ISCA 2023

提出时间比例事件分析（TEA），通过为每条指令构建时间比例的周期栈（PICS）来解释性能瓶颈。TEA仅追踪9个关键事件，相比AMD IBS、Arm SPE和IBM RIS，平均误差从~55.6%降至2.1%，开销极低（功耗+0.1%，性能-1.1%）。在SPEC CPU2017的lbm和nab上分别实现1.28倍和2.45倍加速。

[📄 论文笔记](../../notes_repo/tea-time-proportional-event-analysis/paper_notes.md) | [📊 图表解析](../../notes_repo/tea-time-proportional-event-analysis/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/tea-time-proportional-event-analysis/ELI5_notes.md) | <a href="https://doi.org/10.1145/3579371.3589058" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## TIP: Time-Proportional Instruction Profiling
> **Authors:** Björn Gottschall, Lieven Eeckhout, Magnus Jahre  
> **Affiliations:** Norwegian University of Science and Technology, Ghent University  
> **Venue:** MICRO 2021

论文提出Oracle作为性能分析的黄金标准，并揭示现有硬件分析器（如Intel PEBS、AMD IBS）因非时间比例采样导致平均指令级误差高达9.3%-61.8%。为此，作者设计了TIP（Time-Proportional Instruction Profiling），结合Oracle的时间归因策略与统计采样，在BOOM处理器上实现仅1.6%的平均误差。TIP成功定位SPEC CPU2017中Imagick的CSR指令性能瓶颈，优化后获得1.93倍加速。

[📄 论文笔记](../../notes_repo/tip-time-proportional-instruction-profiling/paper_notes.md) | [📊 图表解析](../../notes_repo/tip-time-proportional-instruction-profiling/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/tip-time-proportional-instruction-profiling/ELI5_notes.md) | <a href="https://doi.org/10.1145/3466752.3480058" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Titan-l: An Open-Source, High Performance RISC-V Vector Core
> **Authors:** Jiuyang Liu, Qinjun Li, Yunqian Luo, et al.  
> **Affiliations:** Huazhong University of Science and Technology, Institute of Software, Chinese Academy of Sciences, Tsinghua University, Xinpian Technology Co., Ltd.  
> **Venue:** MICRO 2025

论文提出了Titan-I (T1)，一个开源、高性能、乱序执行的RISC-V向量处理器。其通过粗粒度布局规划器、全数据通路置换单元和掩码寄存器缓存解决扩展性问题，并采用细粒度链接、提交即发射等技术优化ILP。在密码学 workload 上，T1性能比Nvidia 3090高2.41倍，面积仅为其40%；在HPC workload上，以19%的面积实现与HiSilicon TaiShan V120相当的性能。

[📄 论文笔记](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/paper_notes.md) | [📊 图表解析](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756059" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Tolerate It if You Cannot Reduce It: Handling Latency in Tiered Memory
> **Authors:** Musa Unal, Vishal Gupta, Yueyang Pan, et al.  
> **Affiliations:** EPFL  
> **Venue:** HOTOS 2025

论文提出Linden系统，结合延迟减少（页迁移）与延迟容忍（预取）策略优化分层内存性能。指出传统硬件预取在CXL内存上因带宽竞争可导致19%性能下降，而软件预取需采用层级感知的预取距离（如CXL需距离7而非DRAM的4）。实验显示对热点且可预取区域迁移到慢速层可提升7%性能。

[📄 论文笔记](../../notes_repo/tolerate-it-if-you-cannot-reduce-it-handling-latency-in-tiered-memory/paper_notes.md) | [📊 图表解析](../../notes_repo/tolerate-it-if-you-cannot-reduce-it-handling-latency-in-tiered-memory/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/tolerate-it-if-you-cannot-reduce-it-handling-latency-in-tiered-memory/ELI5_notes.md) | <a href="https://doi.org/10.1145/3713082.3730376" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---
