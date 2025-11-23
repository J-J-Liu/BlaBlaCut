# MICRO 2025

MICRO 2025 论文

本页面共收录了 2 篇论文笔记。

## RICH Prefetcher: Storing Rich Information in Memory to Trade Capacity and Bandwidth for Latency Hiding
> **Authors:** Ningzhi Ai, Wenjian He, Hu He, et al.  
> **Affiliations:** Huawei Technologies Co., Ltd, Tsinghua University  
> **Venue:** MICRO 2025

针对高带宽/大容量但高延迟的未来内存系统，提出RICH预取器。其核心创新是利用丰富的元数据，通过多尺度区域（2KB/4KB/16KB）和多偏移触发机制协同工作，在保持高精度的同时提升覆盖率和及时性。为控制开销，采用片上/片下分层存储元数据。实验表明，在传统系统中性能优于Bingo 3.4%，在增加120ns延迟的高延迟系统中优势扩大至8.3%。

[📄 论文笔记](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/paper_notes.md) | [📊 图表解析](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rich-prefetcher-storing-rich-information-in-memory-to-trade-capacity-and-bandwidth-for-latency-hiding/ELI5_notes.md)

---

## Titan-I: An Open-Source, High Performance RISC-V Vector Core
> **Authors:** Jiuyang Liu, Qinjun Li, Yunqian Luo, et al.  
> **Affiliations:** Huazhong University of Science and Technology, Institute of Software, Chinese Academy of Sciences, Tsinghua University, Xinpian Technology Co., Ltd.  
> **Venue:** MICRO 2025

提出Titan-I (T1)，一个开源、高性能的乱序RISC-V向量核，通过粗粒度布局规划器、数据通路级置换单元和掩码寄存器缓存解决VLEN/DLEN扩展难题，并采用细粒度链接、提交即发射等技术提升ILP。在密码学 workload 上，T1以40%面积实现对Nvidia 3090/5090最高2.41倍/1.85倍加速；在HPC上，以19%面积达到HiSilicon TaiShan V120性能，并在4倍数据通路扩展下获得4.59倍加速。

[📄 论文笔记](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/paper_notes.md) | [📊 图表解析](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/titan-i-an-open-source-high-performance-risc-v-vector-core/ELI5_notes.md)

---
