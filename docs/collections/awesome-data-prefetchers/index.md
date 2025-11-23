# Awesome Data Prefetchers

数据预取器相关论文

本页面共收录了 7 篇论文笔记。

## Feedback Directed Prefetching: Improving the Performance and Bandwidth-Efficiency of Hardware Prefetchers
> **Authors:** Santhosh Srinath, Onur Mutlu, Hyesoon Kim, et al.  
> **Affiliations:** Microsoft, Microsoft Research, The University of Texas at Austin  
> **Venue:** MICRO 2007

提出反馈导向预取（FDP）机制，通过动态监控预取准确率、及时性和缓存污染来调整硬件预取器的激进程度和预取块在缓存LRU栈中的插入位置。在SPEC CPU2000上，相比最佳传统流式预取器，平均性能提升6.5%，内存带宽消耗降低18.7%。

[📄 论文笔记](../../notes_repo/feedback-directed-prefetching-improving-the-performance-and-bandwidth-efficiency-of-hardware-prefetchers/paper_notes.md) | [📊 图表解析](../../notes_repo/feedback-directed-prefetching-improving-the-performance-and-bandwidth-efficiency-of-hardware-prefetchers/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/feedback-directed-prefetching-improving-the-performance-and-bandwidth-efficiency-of-hardware-prefetchers/ELI5_notes.md)

---

## Limoncello: Prefetchers for Scale
> **Authors:** Akanksha Jain, Hannah Lin, Carlos Villavieja, et al.  
> **Affiliations:** Google, University of Washington  
> **Venue:** ASPLOS 2024

论文提出Limoncello，一种无需硬件修改的软硬协同预取系统。它在高内存带宽利用率时动态关闭硬件预取器以降低15%内存延迟，并通过大规模硬件消融研究识别出数据中心税函数（如memcpy、压缩、哈希）作为软件预取目标，精准插入软件预取指令。在Google生产集群部署后，系统在高负载下将应用吞吐量提升10%，同时减少15%的socket内存带宽。

[📄 论文笔记](../../notes_repo/limoncello-prefetchers-for-scale/paper_notes.md) | [📊 图表解析](../../notes_repo/limoncello-prefetchers-for-scale/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/limoncello-prefetchers-for-scale/ELI5_notes.md)

---

## Prodigy: Improving the Memory Latency of Data-Indirect Irregular Workloads Using Hardware-Software Co-Design
> **Authors:** Nishil Talati, Kyle May, Armand Behroozi, et al.  
> **Affiliations:** University of Michigan, University of Wisconsin, Madison, University of Edinburgh  
> **Venue:** MICRO 2021

提出Prodigy，一种软硬件协同设计的低开销预取方案，用于加速具有数据间接访问模式（单值和范围间接）的不规则工作负载。其核心是数据间接图（DIG）表示，由编译器自动生成并指导硬件预取器。在仅0.8KB存储开销下，相比无预取基线平均提速2.6倍、节能1.6倍，并显著优于现有先进预取器。

[📄 论文笔记](../../notes_repo/prodigy-improving-the-memory-latency-of-data-indirect-irregular-workloads-using-hardware-software-co-design/paper_notes.md) | [📊 图表解析](../../notes_repo/prodigy-improving-the-memory-latency-of-data-indirect-irregular-workloads-using-hardware-software-co-design/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/prodigy-improving-the-memory-latency-of-data-indirect-irregular-workloads-using-hardware-software-co-design/ELI5_notes.md)

---

## Profile-Guided Temporal Prefetching
> **Authors:** Mengming Li, Qijun Zhang, Yichuan Gao, et al.  
> **Affiliations:** Hong Kong University of Science and Technology (HKUST), Intel  
> **Venue:** ISCA 2025

提出Prophet，一个软硬协同的Profile-Guided时序预取框架，通过轻量级计数器分析和动态提示注入，优化片上元数据表管理。相比SOTA硬件预取器Triangel，性能提升14.23%，显著优于软件方案RPG2（仅0.1%增益），且能自适应不同输入，开销可忽略。

[📄 论文笔记](../../notes_repo/profile-guided-temporal-prefetching/paper_notes.md) | [📊 图表解析](../../notes_repo/profile-guided-temporal-prefetching/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/profile-guided-temporal-prefetching/ELI5_notes.md)

---

## RICH Prefetcher: Storing Rich Information in Memory to Trade Capacity and Bandwidth for Latency Hiding
> **Authors:** Ningzhi Ai, Wenjian He, Hu He, et al.  
> **Affiliations:** Huawei Technologies Co., Ltd, Tsinghua University  
> **Venue:** MICRO 2025

针对高带宽/大容量但高延迟的未来内存系统，提出RICH预取器。其核心创新是利用丰富的元数据，通过多尺度区域（2KB/4KB/16KB）和多偏移触发机制协同工作，在保持高精度的同时提升覆盖率和及时性。为控制开销，采用片上/片下分层存储元数据。实验表明，在传统系统中性能优于Bingo 3.4%，在增加120ns延迟的高延迟系统中优势扩大至8.3%。

[📄 论文笔记](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/paper_notes.md) | [📊 图表解析](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/ELI5_notes.md)

---

## RnR: A Software-Assisted Record-and-Replay Hardware Prefetcher
> **Authors:** Chao Zhang, Yuan Zeng, John Shalf, et al.  
> **Affiliations:** Lehigh University, Lawrence Berkeley National Lab  
> **Venue:** HPCA 2023

论文提出RnR，一种软硬件协同的记录-回放式硬件预取器，用于处理具有重复性不规则访存模式的应用（如图计算、稀疏矩阵运算）。通过轻量级编程接口，程序员指定数据结构和迭代边界，硬件记录首次缓存未命中序列并后续回放预取。该方法在PageRank等图应用上平均提速2.16倍，在稀疏迭代求解器上提速2.91倍，预取准确率和覆盖率均超95%。

[📄 论文笔记](../../notes_repo/rnr-a-software-assisted-record-and-replay-hardware-prefetcher/paper_notes.md) | [📊 图表解析](../../notes_repo/rnr-a-software-assisted-record-and-replay-hardware-prefetcher/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rnr-a-software-assisted-record-and-replay-hardware-prefetcher/ELI5_notes.md)

---

## RPG2: Robust Profile-Guided Runtime Prefetch Generation
> **Authors:** Yuxuan Zhang, Nathan Sobotka, Soyoon Park, et al.  
> **Affiliations:** University of Pennsylvania, University of California, Santa Cruz, Columbia University, University of Washington, Google, Intel  
> **Venue:** ASPLOS 2024

RPG2 是一个纯软件的运行时系统，用于动态注入和调优数据预取。它通过在线分析程序行为，自动插入预取指令并实时调整预取距离，以应对不同输入和微架构下的性能敏感性。当预取有害时，RPG2 能回滚到原始代码。实验表明，RPG2 在多种负载上可获得最高2.15倍的加速，并有效避免了静态编译器无法处理的性能下降问题。

[📄 论文笔记](../../notes_repo/rpg2-robust-profile-guided-runtime-prefetch-generation/paper_notes.md) | [📊 图表解析](../../notes_repo/rpg2-robust-profile-guided-runtime-prefetch-generation/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rpg2-robust-profile-guided-runtime-prefetch-generation/ELI5_notes.md)

---
