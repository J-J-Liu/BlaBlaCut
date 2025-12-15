# 动态语言加速

本文主要针对动态语言的负载特征进行分析。受限于解释器模式下的低指令级并行度（ILP），以及动态类型分派和垃圾回收（GC）引入的大量间接跳转与不规则访存，动态语言在微架构层面面临严峻的性能瓶颈。此外，随着现代静态语言越来越多地引入自动内存管理与运行时多态机制，它们在底层行为上也表现出一定程度的特征趋同。

本页面共收录了 19 篇论文笔记，分为 5 个分类。

## 负载分析

**负载特征化与性能差距归因**：深入分析 Python、JavaScript、Java 等托管语言在真实应用场景下的运行时行为。重点考察其与静态编译语言（Native Code）在指令级并行度（ILP）、缓存局部性以及能效比上的量化差异，旨在揭示导致动态语言‘性能税’（Performance Tax）的关键瓶颈，为后续优化提供数据支撑。

*本分类包含 5 篇论文*

### An Empirical Study on the Performance and Energy Usage of Compiled Python Code
> **Authors:** Vincenzo Stoico, Andrei Calin Dragomir, Patricia Lago  
> **Affiliations:** Vrije Universiteit Amsterdam, The Netherlands  
> **Venue:** EASE 2025

该研究实证评估了8种Python编译器（如Codon、PyPy、Numba）相比CPython在性能与能耗上的提升。在7个基准测试中，Codon、PyPy和Numba平均实现超90%的执行时间和能耗优化，Nuitka显著降低内存使用。实验在固定频率和单核条件下进行，控制了代码特征与平台变量。

[📄 论文笔记](../../notes_repo/an-empirical-study-on-the-performance-and-energy-usage-of-compiled-python-code/paper_notes.md) | [📊 图表解析](../../notes_repo/an-empirical-study-on-the-performance-and-energy-usage-of-compiled-python-code/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/an-empirical-study-on-the-performance-and-energy-usage-of-compiled-python-code/ELI5_notes.md) | <a href="https://doi.org/10.1145/nnnnnnn.nnnnnnn" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Rethinking Java Performance Analysis
> **Authors:** Stephen M. Blackburn, Zixian Cai, Rui Chen, et al.  
> **Affiliations:** Google, Australian National University, ByteDance, IOP Systems, Canva, The University of Sydney  
> **Venue:** ASPLOS 2025

论文提出DaCapo Chopin基准套件，包含22个新/更新的工作负载，并引入新方法论评估Java性能。通过主成分分析验证工作负载多样性，揭示现代生产级垃圾回收器即使在最优情况下仍消耗15% CPU周期，在小堆内存下开销高达17倍。论文强调需持续改进性能分析方法以避免研究方向偏差。

[📄 论文笔记](../../notes_repo/rethinking-java-performance-analysis/paper_notes.md) | [📊 图表解析](../../notes_repo/rethinking-java-performance-analysis/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rethinking-java-performance-analysis/ELI5_notes.md) | <a href="https://doi.org/10.1145/3669940.3707217" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Investigating Managed Language Runtime Performance: Why JavaScript and Python are 8x and 29x slower than C++, yet Java and Go can be Faster?
> **Authors:** David Lion, Adrian Chiu, Michael Stumm, et al.  
> **Affiliations:** University of Toronto, YScope Inc.  
> **Venue:** USENIX ATC 2022

该论文对Java、Go、JavaScript和Python的运行时性能进行了深入分析，以C++为基线。通过自研的LangBench基准测试套件和对OpenJDK、V8、CPython运行时的深度插桩，量化了各语言的开销来源。研究发现CPython和V8/Node.js分别比C++慢29.5倍和8倍且难以并行扩展，而OpenJDK和Go仅慢1.43倍和1.3倍，并在部分场景下因GC改善缓存局部性或优化I/O而超越C++。

[📄 论文笔记](../../notes_repo/investigating-managed-language-runtime-performance-why-javascript-and-python-are-8x-and-29x-slower-than-c-yet-java-and-go-can-be-faster/paper_notes.md) | [📊 图表解析](../../notes_repo/investigating-managed-language-runtime-performance-why-javascript-and-python-are-8x-and-29x-slower-than-c-yet-java-and-go-can-be-faster/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/investigating-managed-language-runtime-performance-why-javascript-and-python-are-8x-and-29x-slower-than-c-yet-java-and-go-can-be-faster/ELI5_notes.md)

---

### Porting a JIT Compiler to RISC-V: Challenges and Opportunities
> **Authors:** Quentin Ducasse, Guillermo Polito, Pablo Tesone, et al.  
> **Affiliations:** Laboratoire Lab-STICC - ENSTA Bretagne, France, CNRS, INRIA - Centrale Lille, UMR 9189 CRIStAL, France  
> **Venue:** MPLR 2022

本文研究将Pharo的x86架构JIT编译器Cogit移植到RISC-V所面临的挑战与机遇。针对RISC-V缺乏条件码、立即数加载复杂等特性，提出了IR重构、使用离线字面量管理及开发仿真调试工具等解决方案。实现了开源的RISC-V后端，并构建了ISA无关的测试框架和自定义指令仿真机制，为在RISC-V上探索VM硬件加速（如GC、安全）奠定基础。

[📄 论文笔记](../../notes_repo/porting-a-jit-compiler-to-risc-v-challenges-and-opportunities/paper_notes.md) | [📊 图表解析](../../notes_repo/porting-a-jit-compiler-to-risc-v-challenges-and-opportunities/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/porting-a-jit-compiler-to-risc-v-challenges-and-opportunities/ELI5_notes.md)

---

### A Comprehensive Java Benchmark Study on Memory and Garbage Collection Behavior of DaCapo, DaCapo Scala, and SPECjvm2008
> **Authors:** Philipp Lengauer, Verena Bitto, Hanspeter Mössenböck, et al.  
> **Affiliations:** Institute for System Software, Johannes Kepler University Linz, Austria, Christian Doppler Laboratory MEVSS, Johannes Kepler University Linz, Austria  
> **Venue:** ICPE 2017

本文对DaCapo、DaCapo Scala和SPECjvm2008三大Java基准套件进行了全面的内存与垃圾回收（GC）行为分析。利用低开销监控工具AntTracks，在现代JVM上量化了各基准的分配强度、GC频率、暂停时间等关键指标，并对比了ParallelOld GC与G1 GC的性能差异。研究揭示了如factorie和sunflow等基准高达137GB的内存分配，以及G1在多数场景下显著降低GC时间（如factorie从41%降至1.4%）和暂停时间的优势，为研究人员选择合适基准提供了实证指南。

[📄 论文笔记](../../notes_repo/a-comprehensive-java-benchmark-study-on-memory-and-garbage-collection-behavior-of-dacapo-dacapo-scala-and-specjvm2008/paper_notes.md) | [📊 图表解析](../../notes_repo/a-comprehensive-java-benchmark-study-on-memory-and-garbage-collection-behavior-of-dacapo-dacapo-scala-and-specjvm2008/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/a-comprehensive-java-benchmark-study-on-memory-and-garbage-collection-behavior-of-dacapo-dacapo-scala-and-specjvm2008/ELI5_notes.md) | <a href="https://doi.org/http://dx.doi.org/10.1145/3030207.3030211" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## 动态类型检查与分派

**动态类型检查与分派**：由于变量类型在运行时可变，解释器或JIT编译器必须在每次操作前检查操作数的类型标签（Tag），并根据类型动态分派（Dispatch）到相应的处理函数。这一过程引入了大量的数据依赖性条件跳转和间接跳转指令。

*本分类包含 3 篇论文*

### ShortCut: Architectural Support for Fast Object Access in Scripting Languages
> **Authors:** Jiho Choi, Thomas Shull, Maria J. Garzaran, et al.  
> **Affiliations:** University of Illinois at Urbana-Champaign  
> **Venue:** ISCA 2017

论文提出ShortCut架构，通过硬件支持加速动态脚本语言中的对象访问。其Plain设计绕过分发器直接调用处理器，Aggressive设计进一步将调用转化为简单load/store操作。在V8 JIT编译器和模拟器上评估，Plain ShortCut在基线编译器下平均减少30%执行时间，在最高优化级别下仍提升11%。

[📄 论文笔记](../../notes_repo/shortcut-architectural-support-for-fast-object-access-in-scripting-languages/paper_notes.md) | [📊 图表解析](../../notes_repo/shortcut-architectural-support-for-fast-object-access-in-scripting-languages/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/shortcut-architectural-support-for-fast-object-access-in-scripting-languages/ELI5_notes.md) | <a href="https://doi.org/10.1145/3079856.3080237" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Checked Load: Architectural Support for JavaScript Type-Checking on Mobile Processors
> **Authors:** Owen Anderson, Emily Fortuna, Luis Ceze, et al.  
> **Affiliations:** Computer Science and Engineering, University of Washington  
> **Venue:** HPCA 2011

提出Checked Load架构扩展，通过4条新ISA指令将动态类型检查从软件移至硬件，结合动态类型预测，在移动处理器上JavaScript基准测试平均加速11.2%，最高达44.6%。

[📄 论文笔记](../../notes_repo/checked-load-architectural-support-for-javascript-type-checking-on-mobile-processors/paper_notes.md) | [📊 图表解析](../../notes_repo/checked-load-architectural-support-for-javascript-type-checking-on-mobile-processors/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/checked-load-architectural-support-for-javascript-type-checking-on-mobile-processors/ELI5_notes.md)

---

### Typed Architectures: Architectural Support for Lightweight Scripting
> **Authors:** Channoh Kim, Jaehyeok Kim, Sungmin Kim, et al.  
> **Affiliations:** Sungkyunkwan University, Suwon, Korea, Seoul National University, Seoul, Korea  
> **Venue:** ASPLOS 2017

论文提出Typed Architectures，通过ISA级硬件支持动态类型检查，引入多态指令和灵活的类型标签提取/插入机制。在RISC-V上实现，对JavaScript和Lua解释器分别取得11.2%和9.9%的平均加速，EDP提升19.3%和16.5%，面积开销仅1.6%。

[📄 论文笔记](../../notes_repo/typed-architectures-architectural-support-for-lightweight-scripting/paper_notes.md) | [📊 图表解析](../../notes_repo/typed-architectures-architectural-support-for-lightweight-scripting/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/typed-architectures-architectural-support-for-lightweight-scripting/ELI5_notes.md) | <a href="https://doi.org/http://dx.doi.org/10.1145/3037697.3037726" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## 解释器开销

**解释器开销**：在未被JIT编译之前，代码运行在解释器模式下，存在大量的解码-分派循环，导致极低的指令级并行度（ILP）。

*本分类包含 4 篇论文*

### Short-Circuit Dispatch: Accelerating Virtual Machine Interpreters on Embedded Processors
> **Authors:** Channoh Kim, Sungmin Kim, Hyeon Gyu Cho, et al.  
> **Affiliations:** Sungkyunkwan University, Suwon, Korea  
> **Venue:** ISCA 2016

提出Short-Circuit Dispatch (SCD)，一种低成本硬件扩展，通过将字节码跳转表叠加到BTB上，消除解释器分派循环中的冗余计算。在RISC-V嵌入式处理器上，SCD为Lua和JavaScript解释器分别带来19.9%和14.1%的平均加速，并提升24.2%的能量延迟积(EDP)，仅增加0.72%芯片面积。

[📄 论文笔记](../../notes_repo/short-circuit-dispatch-accelerating-virtual-machine-interpreters-on-embedded-processors/paper_notes.md) | [📊 图表解析](../../notes_repo/short-circuit-dispatch-accelerating-virtual-machine-interpreters-on-embedded-processors/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/short-circuit-dispatch-accelerating-virtual-machine-interpreters-on-embedded-processors/ELI5_notes.md) | <a href="https://doi.org/10.1109/ISCA.2016.34" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Branch Prediction and the Performance of Interpreters – Don’t Trust Folklore
> **Authors:** Erven Rohou, Bharath Narasimha Swamy, Andre Seznec  
> **Affiliations:** Inria, France  
> **Venue:** CGO 2015

该论文挑战了“解释器中switch语句的间接跳转因高误预测率而严重损害性能”的传统观点。作者通过在Nehalem、Sandy Bridge和Haswell处理器上对Python、JavaScript和CLI解释器进行实验，发现分支预测准确率已大幅提升：全局分支误预测率（MPKI）从Nehalem上的12-20降至Haswell上的0.5-2。研究表明，在现代处理器上，间接跳转的预测开销已不再是性能瓶颈。

[📄 论文笔记](../../notes_repo/branch-prediction-and-the-performance-of-interpreters--dont-trust-folklore/paper_notes.md) | [📊 图表解析](../../notes_repo/branch-prediction-and-the-performance-of-interpreters--dont-trust-folklore/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/branch-prediction-and-the-performance-of-interpreters--dont-trust-folklore/ELI5_notes.md) | <a href="https://doi.org/10.1109/CGO.2015.7054191" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Virtual Program Counter (VPC) Prediction: Very Low Cost Indirect Branch Prediction Using Conditional Branch Prediction Hardwar
> **Authors:** Hyesoon Kim, José A. Joao, Onur Mutlu, et al.  
> **Affiliations:** Georgia Institute of Technology, University of Texas at Austin, Carnegie Mellon University, Intel Corporation  
> **Venue:** IEEE Transactions on Computers 2009

论文提出虚拟程序计数器（VPC）预测技术，利用现有条件分支预测硬件低成本地预测间接分支目标，避免了专用存储结构。该方法在C/C++和Java应用上分别平均提升性能26.7%和21.9%，并显著降低能耗，且可与任意条件分支预测器协同工作。

[📄 论文笔记](../../notes_repo/virtual-program-counter-vpc-prediction-very-low-cost-indirect-branch-prediction-using-conditional-branch-prediction-hardware/paper_notes.md) | [📊 图表解析](../../notes_repo/virtual-program-counter-vpc-prediction-very-low-cost-indirect-branch-prediction-using-conditional-branch-prediction-hardware/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/virtual-program-counter-vpc-prediction-very-low-cost-indirect-branch-prediction-using-conditional-branch-prediction-hardware/ELI5_notes.md) | <a href="https://doi.org/10.1109/TC.2008.227" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Bungee Jumps: Accelerating Indirect Branches Through HW/SW Co-Design
> **Authors:** Daniel S. McFarlin, Craig Zilles  
> **Affiliations:** Carnegie Mellon University, University of Illinois at Urbana-Champaign  
> **Venue:** MICRO 2015

论文提出Bungee Jumps技术，通过HW/SW协同设计将间接分支的预测点与解析点分离，使顺序处理器能利用现代高准确率的间接分支预测器。该方法在SPEC、PHP和Python基准上分别实现了11%、23%和14%的平均加速，且代码体积仅增加1-3%。

[📄 论文笔记](../../notes_repo/bungee-jumps-accelerating-indirect-branches-through-hwsw-co-design/paper_notes.md) | [📊 图表解析](../../notes_repo/bungee-jumps-accelerating-indirect-branches-through-hwsw-co-design/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/bungee-jumps-accelerating-indirect-branches-through-hwsw-co-design/ELI5_notes.md) | <a href="https://doi.org/http://dx.doi.org/10.1145/2830772.2830781" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## 垃圾回收开销

**自动内存管理与硬件加速**：垃圾回收（GC）产生的‘全停顿’（Stop-The-World）和高内存带宽占用是制约系统响应能力的主要因素，尤其在多核环境下，原子操作和锁竞争进一步加剧了开销。本部分探讨如何利用硬件事务内存（HTM）、近数据处理（PIM）或专用加速器来卸载对象扫描、引用计数更新等操作，以实现低延迟、高吞吐的并发垃圾回收。

*本分类包含 5 篇论文*

### Charon: Specialized Near-Memory Processing Architecture for Clearing Dead Objects in Memory
> **Authors:** Jaeyoung Jang, Jun Heo, Yejin Lee, et al.  
> **Affiliations:** Sungkyunkwan University, Suwon, Korea, Seoul National University, Seoul, Korea  
> **Venue:** MICRO 2019

论文提出Charon，首个基于3D堆叠内存的垃圾回收（GC）加速器。通过分析HotSpot JVM，识别出Copy、Search、Scan&Push和Bitmap Count等关键GC原语，并在近内存逻辑层设计专用处理单元进行卸载。在Spark和GraphChi上的评估表明，相比8核乱序CPU基线，Charon实现了3.29倍的GC平均加速比和60.7%的能耗节省。

[📄 论文笔记](../../notes_repo/charon-specialized-near-memory-processing-architecture-for-clearing-dead-objects-in-memory/paper_notes.md) | [📊 图表解析](../../notes_repo/charon-specialized-near-memory-processing-architecture-for-clearing-dead-objects-in-memory/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/charon-specialized-near-memory-processing-architecture-for-clearing-dead-objects-in-memory/ELI5_notes.md) | <a href="https://doi.org/10.1145/3352460.3358297" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### HOOP: Efficient Hardware-Assisted Out-of-Place Update for Non-Volatile Memory
> **Authors:** Miao Cai, Chance C. Coats, Jian Huang  
> **Affiliations:** Nanjing University, University of Illinois at Urbana-Champaign  
> **Venue:** unknown 2020

论文提出HOOP，一种透明的硬件辅助异地更新机制，用于非易失内存（NVM）以实现原子持久性。其核心是通过内存控制器中的轻量级间接层进行地址重映射和自适应垃圾回收，避免了日志等方案的额外写入和关键路径开销。实验表明，相比SOTA技术，HOOP性能提升最高1.7倍，写放大降低最高2.1倍。

[📄 论文笔记](../../notes_repo/hoop-efficient-hardware-assisted-out-of-place-update-for-non-volatile-memory/paper_notes.md) | [📊 图表解析](../../notes_repo/hoop-efficient-hardware-assisted-out-of-place-update-for-non-volatile-memory/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/hoop-efficient-hardware-assisted-out-of-place-update-for-non-volatile-memory/ELI5_notes.md)

---

### MemLiner: Lining up Tracing and Application for a Far-Memory-Friendly Runtime
> **Authors:** Chenxi Wang, Haoran Ma, Shi Liu, et al.  
> **Affiliations:** University of California, Los Angeles, University of Chicago  
> **Venue:** OSDI 2022

MemLiner通过“对齐”应用程序与垃圾回收（GC）的内存访问路径，解决远内存系统中GC干扰导致的本地内存工作集膨胀和预取失效问题。其核心是优先追踪应用近期访问的对象，并基于对象指针中的时间戳估计位置以减少远程页错误。在G1和Shenandoah GC上实现，端到端性能最高提升2.5倍，并显著提高预取准确率。

[📄 论文笔记](../../notes_repo/memliner-lining-up-tracing-and-application-for-a-far-memory-friendly-runtime/paper_notes.md) | [📊 图表解析](../../notes_repo/memliner-lining-up-tracing-and-application-for-a-far-memory-friendly-runtime/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/memliner-lining-up-tracing-and-application-for-a-far-memory-friendly-runtime/ELI5_notes.md)

---

### Flexible Reference-Counting-Based Hardware Acceleration for Garbage Collection
> **Authors:** José A. Joao, Onur Mutlu, Yale N. Patt  
> **Affiliations:** ECE Department, The University of Texas at Austin, Computer Architecture Laboratory, Carnegie Mellon University  
> **Venue:** ISCA 2009

提出HAMM，一种软硬件协同的垃圾回收加速机制。通过硬件实现的引用计数（带RCCB缓冲）高效检测死亡对象，并通过ABT快速重用内存块，从而减少软件GC频率。在DaCapo基准测试中，平均减少31%的GC时间，对应用性能（mutator）影响可忽略（仅0.38%开销）。

[📄 论文笔记](../../notes_repo/flexible-reference-counting-based-hardware-acceleration-for-garbage-collection/paper_notes.md) | [📊 图表解析](../../notes_repo/flexible-reference-counting-based-hardware-acceleration-for-garbage-collection/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/flexible-reference-counting-based-hardware-acceleration-for-garbage-collection/ELI5_notes.md)

---

### Gray-in-Young: A Generational Garbage Collection for Processing-in-Memory
> **Authors:** Ryu Morimoto, Kazuki Ichinose, Tomoharu Ugawa  
> **Affiliations:** The University of Tokyo  
> **Venue:** ISMM 2025

针对UPMEM PIM架构的DPU设计了一种并行分代垃圾回收器（GC）。其创新点包括：将新生代置于快速SPM中，通过Gray-in-Young算法在对象晋升前于SPM内更新指针，并静态缓存对象布局信息。这些技术减少了85.9%的DRAM访问，性能提升46.2%，且GC代码仅占4.3KB，可扩展至11个线程。

[📄 论文笔记](../../notes_repo/gray-in-young-a-generational-garbage-collection-for-processing-in-memory/paper_notes.md) | [📊 图表解析](../../notes_repo/gray-in-young-a-generational-garbage-collection-for-processing-in-memory/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/gray-in-young-a-generational-garbage-collection-for-processing-in-memory/ELI5_notes.md) | <a href="https://doi.org/10.1145/3735950.3735961" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

## 存储层次设计

**存储层次设计**：传统 CPU 的缓存层次结构是以“缓存行”（Cache Line，通常 64 字节）为单位管理的，而托管语言是以“对象”为单位的。这种粒度失配导致了严重的碎片化和带宽浪费。

*本分类包含 2 篇论文*

### Rethinking the Memory Hierarchy for Modern Languages
> **Authors:** Po-An Tsai, Yee Ling Gan, Daniel Sanchez  
> **Affiliations:** Massachusetts Institute of Technology  
> **Venue:** MICRO 2018

论文提出Hotpads，一种为内存安全语言（如Java、Go）设计的新型内存层次结构。它摒弃传统扁平地址空间，通过硬件管理的直接寻址存储（pads）和指针重写技术，避免了关联缓存查找。Hotpads将垃圾回收与数据放置统一，显著提升了性能和能效。实验表明，相比传统缓存，Hotpads平均性能提升34%，内存层次能耗降低2.6倍，并将GC开销减少8倍。

[📄 论文笔记](../../notes_repo/rethinking-the-memory-hierarchy-for-modern-languages/paper_notes.md) | [📊 图表解析](../../notes_repo/rethinking-the-memory-hierarchy-for-modern-languages/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/rethinking-the-memory-hierarchy-for-modern-languages/ELI5_notes.md) | <a href="https://doi.org/10.1109/micro.2018.00025" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---

### Compress Objects, Not Cache Lines: An Object-Based Compressed Memory Hierarchy
> **Authors:** Po-An Tsai, Daniel Sanchez  
> **Affiliations:** MIT CSAIL  
> **Venue:** ASPLOS 2019

针对传统缓存行压缩在面向对象程序中效果不佳的问题，提出Zippads——首个面向对象的压缩内存层次结构，以对象为压缩单元，并设计COCO跨对象压缩算法。在混合工作负载上，相比现有技术，平均压缩率提升1.63倍，内存流量减少56%，性能提升17%。

[📄 论文笔记](../../notes_repo/compress-objects-not-cache-lines-an-object-based-compressed-memory-hierarchy/paper_notes.md) | [📊 图表解析](../../notes_repo/compress-objects-not-cache-lines-an-object-based-compressed-memory-hierarchy/figs_notes.md) | [👶 ELI5 解释](../../notes_repo/compress-objects-not-cache-lines-an-object-based-compressed-memory-hierarchy/ELI5_notes.md) | <a href="https://doi.org/10.1145/3297858.3304006" target="_blank" rel="noopener noreferrer">🔗 直达原文</a>

---
