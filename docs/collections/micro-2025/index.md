# MICRO 2025

MICRO 2025 论文

本页面共收录了 6 篇论文笔记。

## RICH Prefetcher: Storing Rich Information in Memory to Trade Capacity and Bandwidth for Latency Hiding
> **Authors:** Ningzhi Ai, Wenjian He, Hu He, et al.  
> **Affiliations:** Huawei Technologies Co., Ltd, Tsinghua University  
> **Venue:** MICRO 2025

针对高带宽高容量但高延迟的未来内存系统，提出RICH预取器。其核心创新是利用多尺度空间局部性（2KB/4KB/16KB区域）和多偏移触发机制，在提升覆盖率和及时性的同时保持高准确率。通过片上/片下分层存储元数据以控制开销。实验表明，在常规系统中性能优于Bingo 3.4%；当内存延迟增加120ns时，优势扩大至8.3%。

[📄 论文笔记](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/paper_notes.md) | [📊 图表解析](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/figs_notes.md) | [👶 通俗解释](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756081" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Titan-I: An Open-Source, High Performance RISC-V Vector Core
> **Authors:** Jiuyang Liu, Qinjun Li, Yunqian Luo, et al.  
> **Affiliations:** Huazhong University of Science and Technology, Institute of Software, Chinese Academy of Sciences, Tsinghua University, Xinpian Technology Co., Ltd.  
> **Venue:** MICRO 2025

提出Titan-I (T1)，一个开源、高性能的乱序RISC-V向量核，通过粗粒度布局求解器、全数据通路置换单元和掩码寄存器缓存解决扩展VLEN/DLEN时的布线瓶颈。结合细粒度链接、提交即发射等技术优化ILP。在密码学 workload 上比Nvidia 3090/5090快2.41x/1.85x，在HPC上比HiSilicon KP920快4.59x（4倍数据通路），面积仅为其19%。

[📄 论文笔记](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/paper_notes.md) | [📊 图表解析](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/figs_notes.md) | [👶 通俗解释](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756059" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Drishti: Do Not Forget Slicing While Designing Last-Level Cache Replacement Policies for Many-Core Systems
> **Authors:** Sweta, Prerna Priyadarshini, Biswabandan Panda  
> **Affiliations:** Indian Institute of Technology Bombay  
> **Venue:** MICRO 2025

论文指出在多核系统的切片LLC中，现有先进替换策略（如Hawkeye、Mockingjay）因局部预测器导致短视决策且采样缓存利用率低。为此提出Drishti，包含两项增强：(1) 每核全局重用预测器与每片局部采样缓存结合；(2) 动态选择高缺失率的LLC集合作为采样缓存。在32核系统上，Drishti使Hawkeye和Mockingjay相比LRU的性能提升从3.3%/6.7%提高到5.6%/13.2%，同时减少存储开销。

[📄 论文笔记](../../notes_repo/drishti-do-not-forget-slicing-while-designing-last-level-cache-replacement-policies-for-many-core-systems/paper_notes.md) | [📊 图表解析](../../notes_repo/drishti-do-not-forget-slicing-while-designing-last-level-cache-replacement-policies-for-many-core-systems/figs_notes.md) | [👶 通俗解释](../../notes_repo/drishti-do-not-forget-slicing-while-designing-last-level-cache-replacement-policies-for-many-core-systems/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756028" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## Learning to Walk: Architecting Learned Virtual Memory Translation
> **Authors:** Kaiyang Zhao, Yuang Chen, Xenia Xu, et al.  
> **Affiliations:** Carnegie Mellon University, Meta, Intel  
> **Venue:** MICRO 2025

论文提出Learned Virtual Memory (LVM)，一种基于学习型索引的页表结构，旨在实现高效的单次访问地址翻译。LVM通过动态适应应用虚拟地址空间的规律性，使用轻量级线性模型构建索引，解决了传统页表多级遍历和哈希页表高冲突率的问题。实验表明，LVM相比基数页表平均减少44%的地址翻译开销，提升应用执行速度2-27%，性能接近理想页表（差距<1%）。

[📄 论文笔记](../../notes_repo/learning-to-walk-architecting-learned-virtual-memory-translation/paper_notes.md) | [📊 图表解析](../../notes_repo/learning-to-walk-architecting-learned-virtual-memory-translation/figs_notes.md) | [👶 通俗解释](../../notes_repo/learning-to-walk-architecting-learned-virtual-memory-translation/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756093" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## SHADOW: Simultaneous Multi-Threading Architecture with Asymmetric Threads
> **Authors:** Ishita Chaturvedi, Bhargav Reddy Godala, Abiram Gangavaram, et al.  
> **Affiliations:** Princeton University, University of British Columbia, Microsoft, University of California Santa Cruz, AheadComputing  
> **Venue:** MICRO 2025

论文提出SHADOW，首个支持乱序（OoO）与顺序（InO）线程并发执行的非对称SMT架构，动态平衡指令级并行（ILP）与线程级并行（TLP）。通过软件工作窃取机制自适应分配负载，在9个基准测试中相比传统OoO CPU最高提速3.16倍，平均提升1.33倍，仅增加1%面积与功耗开销。

[📄 论文笔记](../../notes_repo/shadow-simultaneous-multi-threading-architecture-with-asymmetric-threads/paper_notes.md) | [📊 图表解析](../../notes_repo/shadow-simultaneous-multi-threading-architecture-with-asymmetric-threads/figs_notes.md) | [👶 通俗解释](../../notes_repo/shadow-simultaneous-multi-threading-architecture-with-asymmetric-threads/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756070" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## ATR: Out-of-Order Register Release Exploiting Atomic Regions
> **Authors:** Yinyuan Zhao, Surim Oh, Mingsheng Xu, et al.  
> **Affiliations:** University of California, Santa Cruz  
> **Venue:** MICRO 2025

论文提出ATR技术，通过识别不含分支和异常指令的原子提交区域，实现寄存器的安全乱序释放。该方法无需影子寄存器或复杂恢复机制，在SPEC2017int上平均提升5.13%（64项寄存器文件）性能，或在保持性能损失<3%时减少27.1%寄存器文件大小。

[📄 论文笔记](../../notes_repo/atr-out-of-order-register-release-exploiting-atomic-regions/paper_notes.md) | [📊 图表解析](../../notes_repo/atr-out-of-order-register-release-exploiting-atomic-regions/figs_notes.md) | [👶 通俗解释](../../notes_repo/atr-out-of-order-register-release-exploiting-atomic-regions/ELI5_notes.md) | <a href="https://doi.org/10.1145/3725843.3756135" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---
