# Concurrent Copying Garbage Collection with Hardware Transactional Memory 论文解析

## 0. 论文基本信息

**作者 (Authors)**: Zixian Cai

**发表期刊/会议 (Journal/Conference)**: unknown

**发表年份 (Publication Year)**: 2020

**研究机构 (Affiliations)**: The Australian National University

---

## 1. 摘要

**目的**
- 探索利用 **Hardware Transactional Memory (HTM)** 来实现 **concurrent copying garbage collection (GC)**，旨在解决现有方案（如 **read barriers** 或 **page protection**）带来的高 **mutator overhead** 问题，从而为延迟敏感型应用提供更低暂停时间的垃圾回收方案。

**方法**
- **HTM 容量研究**：
  - 系统性地复现并分析了文献中关于 **Intel TSX** 容量的矛盾报告。
  - 设计并执行了一系列实验，探究不同因素对 HTM 有效容量的影响，包括：
    - **内存区域复用** vs. 使用独立内存区域。
    - **缓存状态**的影响，具体测试了 **缓存无效化 (cache invalidation)** 和 **缓存预热 (cache warmup)** 两种策略。
  - 采用 **success rate curves** 作为评估指标，并在多种 Intel 微架构（Haswell, Broadwell, Skylake, Coffee Lake）上进行测试。
- **HTM-GC 算法设计与实现**：
  - 提出了一种新颖的并发复制 GC 算法，其核心思想是让 **mutator** 在关键时期短暂地 **transactionally execute**，以获得堆的一致性视图。
  - 该算法仅使用一个廉价的 **write barrier** 来维护 **remembered set**，避免了昂贵的 read barrier。
  - 引入了一个 **monotonic counter** 机制和 **yieldpoints** 来协调 collector 与 mutator，解决了 collector 事务提交后、mutator 栈上引用更新前的 **problematic gap**。
  - 基于对 HTM 容量的理解，提出了两项优化：
    - **Optimistic Copying**：将对象复制操作移出事务，仅在事务内进行验证，以减少事务内的写操作数量。
    - **Cache Warmup**：在执行 collector 事务前预热缓存，以提高大事务的成功率。
  - 在 **MMTk** 框架中实现了该算法，并通过一系列精心设计的 **linked-list** 测试程序验证其核心机制。

**结果**
- **HTM 容量研究发现**：
  - 文献中报告的 HTM 容量差异主要源于不同的实验方法。**内存访问模式**和**缓存状态**对有效容量有显著影响。
  - **复用内存区域**、**无效化缓存**和**预热缓存**均能显著提升 **read-only transaction** 的容量。
  - 实验结果表明，**write-set** 容量稳定在 **20-25KB** 左右（接近 L1 cache 大小），而 **read-set** 容量则受缓存状态影响巨大。
  - 关键图表如下：
    ![](images/fca77d7a9e12d5dad7efe61d5344235db8aeb939383bcc018089466fd3496ab0.jpg) *Figure 5.1: Success rate curves on Haswell.*
    ![](images/5e6c6cb543e2599d4e8c5f0989ed846ab5137bcd7a6d78dd13489e494445c681.jpg) *Figure 5.9: Success rate curves on Coffee Lake when invalidating caches.*
    ![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*
- **HTM-GC 算法验证**：
  - 实现的测试程序成功验证了算法的核心功能，包括：
    - 正确更新 **stack roots** 上的引用。
    - 在并发写入场景下，通过事务保证 **atomicity**，防止 **lost updates**。
    - 正确追踪和更新 **transitively reachable** 对象的堆内引用。
  - 结果证明，该算法在概念上是 **viable** 的，能够利用 HTM 实现低开销的并发复制。

**结论**
- 利用 **HTM** 实现低 mutator 开销的 **concurrent copying GC** 是可行的。
- 该工作不仅提出了一种新颖的 GC 算法，还通过深入的实验分析，**澄清了关于 HTM 容量的文献矛盾**，并揭示了 **缓存状态** 对 HTM 性能的关键影响。
- 所提出的 **optimistic copying** 和 **cache warmup** 优化策略，为未来设计更高效的 HTM 应用提供了重要指导。
- 该研究为在支持 HTM 的硬件上构建高性能、低延迟的垃圾回收器奠定了基础。

---

## 2. 背景知识与核心贡献

**研究背景**
- 现代许多**latency-critical**（延迟敏感）应用（如视频、交易系统）越来越多地采用**managed languages**（如 Java, C#）开发，以提升生产力和可靠性。
- **Garbage Collection **(GC) 是托管语言的核心特性，但其执行过程会引入**pauses**（停顿），严重影响用户体验和系统性能。
- **Concurrent copying GC** 是一种理想的解决方案，它既能通过并发执行减少停顿，又能通过对象复制（copying）改善内存**locality**（局部性）并减少**heap fragmentation**（堆碎片）。
- 然而，实现并发复制 GC 需要复杂的同步机制来保证 mutator（应用程序）在 collector（回收器）移动对象时能获得**consistent view**（一致的堆视图）。现有方案主要依赖**read barriers**（读屏障）或**page protections**（页保护），但这些机制会给 mutator 带来**high overhead**（高开销）。

**研究动机**
- **Hardware Transactional Memory **(HTM)，特别是 Intel 的 TSX，提供了一种硬件级的乐观并发控制机制，能够在事务提交时保证一系列内存操作的原子性和隔离性。
- 作者提出核心假设：利用 HTM 可以让 mutator 在关键时期**transactionally**（事务性地）执行，从而自然地获得堆的一致性视图，同时避免传统 read barrier 或 page protection 带来的持续性高开销。
- 在探索该假设的过程中，作者发现 HTM 的实际效能高度依赖于其**transaction capacity**（事务容量），而文献中关于 Intel TSX 容量的报告存在**apparent contradiction**（明显矛盾），这阻碍了 HTM-GC 算法的有效设计。

**核心贡献**
- **对 HTM 容量的深入分析与澄清**：
  - 系统性地复现并对比了文献中关于 Intel TSX 容量的矛盾结果。
  - 通过精心设计的实验，揭示了**cache status**（缓存状态）是影响 HTM 有效容量的关键因素。实验表明，无论是**invalidating caches**（清空缓存）还是**warming up caches**（预热缓存），都能显著提升大型只读事务的成功率，这解释了先前研究结果的差异。
  - ![](images/5e6c6cb543e2599d4e8c5f0989ed846ab5137bcd7a6d78dd13489e494445c681.jpg) *Figure 5.9: Success rate curves on Coffee Lake when invalidating caches.*
  - ![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*
- **提出并实现了一种新颖的 HTM-based Concurrent Copying GC 算法**：
  - 该算法仅使用一个廉价的**write barrier**（写屏障）来维护**remembered set**（记忆集），用于追踪跨区域引用。
  - 为了解决 collector 事务提交后、mutator 栈上引用更新前的**problematic gap**（问题间隙），创新性地让 mutator 在此期间**execute transactionally**（事务性地执行）。
  - 如果 mutator 的事务在 gap 期间执行，它会因检测到全局状态变化或与 collector 事务冲突而**abort**（中止），从而回滚错误的执行，确保了正确性。
  - 这种方法将高昂的、持续性的 read barrier 开销，转变为仅在 GC 活动期间才可能发生的、一次性的事务启动和潜在中止开销。
- **基于 HTM 容量洞察的算法优化**：
  - **Optimistic Copying**（乐观复制）：将对象复制的实际写操作移出 collector 事务，在事务内仅进行验证性读取，从而大幅减少事务内的**write-set**大小，规避了 HTM 写容量远小于读容量的限制。
  - **Cache Warmup**（缓存预热）：在启动 collector 事务前，预先执行一遍事务逻辑（丢弃结果），以将所需数据预热到缓存中，减少因**pseudo-LRU**替换策略导致的非必要容量中止。

---

## 3. 核心技术和实现细节

### 0. 技术架构概览

**整体技术架构**

本文提出了一种利用 **Hardware Transactional Memory (HTM)** 来实现低开销 **concurrent copying garbage collection (GC)** 的新型算法。其核心思想是，让 **mutator**（应用程序线程）在垃圾回收器（collector）进行对象移动的关键窗口期内，以事务性方式执行，从而保证堆视图的一致性，同时避免了传统方案中高开销的 **read barrier** 或 **page protection**。

- **基础组件**:
  - **Region-based Heap Organization**: 将堆划分为多个 **region**，使得 GC 可以针对单个 region 进行独立的并发回收，而非全局停顿。
  - **Write Barrier**: 使用一个轻量级的 **write barrier** 来动态维护每个 region 的 **remembered set**。该 barrier 仅记录从 region 外部指向内部的引用（inter-region references），为后续的并发复制提供必要的根集信息。
  - **Yieldpoints**: 利用运行时系统中已有的 **yieldpoint** 机制，作为 mutator 与 collector 之间进行协调和状态同步的安全点。

- **核心 HTM GC 算法流程**:
  - **Collector Side**:
    - Collector 在开始复制前，将一个全局的 **CollectorCopyingState** 计数器设为奇数，并通过 **handshake** 机制通知所有 mutator 线程。
    - Collector 在一个 **HTM transaction** 内执行 `copyRegion` 操作：将 fromspace 中的存活对象复制到 tospace，并原子地更新 remembered set 中的所有引用。
    - 如果事务成功提交，则将 `CollectorCopyingState` 计数器加一变为偶数，宣告本次复制完成；如果失败，则同样更新计数器但不改变堆状态。
  - **Mutator Side**:
    - Mutator 在 yieldpoint 处通过 handshake 检查 `CollectorCopyingState`。
    - 如果发现计数器为奇数（表示 collector 正在尝试复制），mutator 会将其下一段应用代码（直到下一个 yieldpoint）包裹在一个 **HTM transaction** 中执行。
    - 在事务提交前，mutator 会再次检查 `CollectorCopyingState`。如果在此期间 collector 已完成复制（计数器变为偶数），则 mutator 的事务会主动 **abort**，从而回滚任何可能基于过时堆状态（stale reference）的错误执行。
    - 事务成功提交后，mutator 继续正常执行。

- **关键优化**:
  - **Optimistic Copying**: 为了减少 collector 事务中的写操作（因为 HTM 的 **write-set capacity** 远小于 read-set capacity），collector 首先在事务外将对象复制到一个 **shadow region** 作为快照。然后在事务内，仅比较原对象与快照是否一致。若一致，则说明复制有效；否则事务 abort。这将大量的事务性写操作转换为事务性读操作。
  - **Cache Warmup**: 基于对 HTM 容量的深入分析（见下文），发现 **cache 状态** 对事务成功率有显著影响。因此，在启动 collector 事务前，会预先执行一次“预热”操作（执行事务逻辑但丢弃结果），将相关数据加载到 cache 中，以减少因 **pseudo-LRU** 替换策略导致的非必要事务 abort。

**HTM 容量分析与洞察**

本文的第一部分对 **Intel TSX** 的 HTM 容量进行了详尽的实验分析，为上述 GC 算法的设计和优化提供了理论基础。

- **核心发现**:
  - HTM 的 **read-set capacity** 和 **write-set capacity** 并非固定值，而是受到多种因素的显著影响。
  - **Write-set capacity** 相对稳定，主要受限于 **L1 data cache** 的大小（约 20-25KB）。
  - **Read-set capacity** 变化极大，其有效容量高度依赖于 **cache 的初始状态** 和 **内存访问模式**。

- **影响容量的关键因素**:
  - **Memory Reuse**: 重用同一块内存区域进行测试，相比使用全新内存，能显著提升 read-set 容量。这是因为之前的访问已经将数据预热到 cache 中。
  - **Cache State**: 实验表明，无论是 **invalidating the cache**（清空缓存）还是 **warming up the cache**（预热缓存），都能比 baseline（冷缓存）获得更大的 read-set 容量。这揭示了 **pseudo-LRU** 替换策略的局限性：在缓存未满或已预热的情况下，事务所需的数据更不容易被错误地驱逐。

![](images/fca77d7a9e12d5dad7efe61d5344235db8aeb939383bcc018089466fd3496ab0.jpg) *Figure 5.1: Success rate curves on Haswell.*
![](images/573ff1d98148715e9ecdc109fc6fd39d4c0e260749622f993a571e0e8399bb0b.jpg) *Figure 5.2: Success rate curves on Broadwell.*
![](images/3e7ac435f47b2ee0991a4572a95522ad9c5ba4bbd81f69f34cc88f178b219055.jpg) *Figure 5.3: Success rate curves on Skylake.*
![](images/06532af4750ccb7976030552dd6e5c5ebfcd550dc236c7c0eb5fc12de7760f0d.jpg) *Figure 5.4: Success rate curves on Coffee Lake.*

- **解决文献矛盾**: 通过上述实验，本文解释了为何先前研究中报告的 HTM 容量存在巨大差异（从 22KB 到 7.5MB）。这些差异主要源于不同的 **实验方法论**（如是否重用内存、是否控制 cache 状态）。

**实现与验证**

- **实现平台**: 算法在 **MMTk**（Memory Management Toolkit）框架中实现。
- **验证方法**: 由于工程复杂度高，作者设计了一系列精巧的 **handcrafted test programs**（基于链表结构）来验证算法的核心机制：
  - 验证栈上引用（stack roots）能否被正确更新。
  - 验证在并发复制期间，mutator 对对象的写入不会丢失（lost update）。
  - 验证非直接可达的对象也能被正确追踪和复制。
- **结论**: 测试结果证明了该 HTM-based concurrent copying GC 算法的 **viability**（可行性）。

### 1. 基于HTM的并发复制垃圾回收算法

**核心观点**

- 该论文提出了一种新颖的 **并发复制垃圾回收 (Concurrent Copying GC)** 算法，其核心思想是利用 **硬件事务内存 (HTM)** 来协调 **mutator**（应用程序线程）和 **collector**（垃圾回收器线程）之间的操作，从而在保证堆一致性的前提下，显著降低传统方案（如读屏障或页保护）带来的 **mutator开销**。
- 该算法的关键创新在于，它不要求 mutator 在整个 GC 周期都处于某种特殊状态，而是在 collector 完成对象移动后的一个**极短且关键的时间窗口**内，让 mutator 的执行被包裹在一个 HTM 事务中。这个事务充当了一个“安全网”，确保任何在此窗口期内发生的、基于旧引用（fromspace reference）的错误操作都会被自动回滚。

**算法设计与流程**

- **基础设置**：
    - 算法基于一个简单的 **stop-the-world 复制式GC**（如 semispace），但将其应用于堆的一个**连续子区域 (region)**，而非整个堆，以适应 HTM 的容量限制。
    - 引入一个轻量级的 **写屏障 (write barrier)**。当 mutator 创建一个从 region 外部指向内部的引用时，该屏障会将这个引用的位置记录到该 region 的 **remembered set** 中。这是唯一需要的屏障，开销远低于读屏障。

- **解决丢失更新问题 (Avoiding Lost Updates)**：
    - Collector 在一个 HTM 事务中执行 `copyRegion` 操作。
    - 该事务包含两个原子步骤：
        1. 将 fromspace 中所有存活对象复制到 tospace，并在原对象头中设置 **forwarding pointer**。
        2. 遍历 remembered set，将所有指向 fromspace 对象的引用更新为指向 tospace 的新对象。
    - 由于 HTM 的原子性，这两个步骤要么全部成功，要么全部失败，从而避免了 mutator 在复制过程中向 fromspace 对象写入数据而导致的 **丢失更新 (lost update)** 问题。

- **处理栈上引用的“问题间隙” (The Problematic Gap)**：
    - 上述 collector 事务只能更新堆内的引用，无法处理 **mutator 栈上的引用**，因为扫描栈需要暂停 mutator，这违背了并发GC的初衷。
    - 这就产生了一个 **“问题间隙”**：从 collector 事务提交（发布新对象）到 mutator 下次有机会修复其栈上引用之间的时间窗口。在此间隙内，mutator 可能会使用栈上的旧引用，导致读取过时数据或写入丢失。

- **覆盖“问题间隙”的机制 (Covering the Gap)**：
    - **全局状态信号**：引入一个全局单调递增的计数器 **`CollectorCopyingState`**。collector 在开始事务前将其设为奇数，在事务成功提交或失败后将其设为偶数。**奇偶变化**（特别是变为偶数）即向 mutator 发出信号：一个潜在的“问题间隙”已经出现。
    - **握手协议 (Handshaking)**：
        - Collector 在启动事务前，通过 **yieldpoint** 机制请求所有 mutator 线程进行一次同步。
        - Mutator 在 yieldpoint 中执行 `mutatorHandshake`，检查 `CollectorCopyingState`。如果发现自上次检查以来计数器变为过偶数，则立即调用 `fixStack()` 来修复其栈上的所有 fromspace 引用。
    - **Mutator 事务化执行 (Transactional Execution)**：
        - 在 `mutatorHandshake` 之后，如果当前 `CollectorCopyingState` 是奇数（意味着 collector 即将或正在尝试一个事务），mutator 会将其接下来的执行（直到下一个 yieldpoint）包裹在一个 HTM 事务中。
        - 在事务提交前，mutator 会再次检查 `CollectorCopyingState`。如果发现计数器已改变（意味着 collector 事务已提交，间隙已发生），则显式中止 (`XABORT`) 当前事务。
        - **正确性保证**：通过这种方式，任何在“问题间隙”内发生的 mutator 执行都会导致其事务中止并回滚。mutator 随后会在重试中通过 handshake 修复栈引用，从而保证了执行的正确性。

**关键优化策略**

- **乐观复制 (Optimistic Copying)**：
    - **动机**：HTM 的 **写集 (write-set) 容量**（约20-25KB）远小于读集容量。直接在事务中复制对象会产生大量写操作，极易超出容量限制导致中止。
    - **方法**：将实际的对象复制操作移出事务。在事务外，先在 **shadow region** 中创建一个源对象的快照，然后基于快照创建目标对象。在 HTM 事务中，仅比较源对象和快照是否一致。如果一致，说明复制期间无并发修改，事务提交；否则，事务中止。
    - **效果**：将事务内的大量 **写操作** 转化为 **读操作**，极大地降低了因超出写容量而中止的概率。

- **缓存预热 (Cache Warmup)**：
    - **动机**：实验（见下文）表明，HTM 的有效容量受 **缓存状态** 影响巨大。即使事务工作集小于 L1 缓存，**伪LRU (pseudo-LRU)** 替换策略也可能错误地驱逐事务所需的缓存行，导致不必要的容量中止。
    - **方法**：在启动 collector 事务前，预先执行一遍事务的核心逻辑（如快照比较），但丢弃结果。这会将相关数据 **预热 (warm up)** 到缓存中。
    - **效果**：提高了事务执行时所需数据在缓存中的命中率，减少了因缓存抖动导致的中止，从而提升了大事务的成功率。

**HTM容量实验洞察**

- 论文首先对 Intel TSX 的 HTM 容量进行了详尽的基准测试，以指导算法设计。实验揭示了文献中关于容量报告相互矛盾的原因。
- **关键发现**：
    - **写集容量** 相对稳定，受限于 **L1 数据缓存**（约20-25KB）。
    - **读集容量** 变化极大，受 **内存访问模式** 和 **缓存初始状态** 影响显著。
    - **复用内存区域**、**无效化缓存** 或 **预热缓存** 都能显著提升读事务的成功率和最大容量。

![](images/fca77d7a9e12d5dad7efe61d5344235db8aeb939383bcc018089466fd3496ab0.jpg) *Figure 5.1: Success rate curves on Haswell.*
![](images/573ff1d98148715e9ecdc109fc6fd39d4c0e260749622f993a571e0e8399bb0b.jpg) *Figure 5.2: Success rate curves on Broadwell.*
![](images/3e7ac435f47b2ee0991a4572a95522ad9c5ba4bbd81f69f34cc88f178b219055.jpg) *Figure 5.3: Success rate curves on Skylake.*
![](images/06532af4750ccb7976030552dd6e5c5ebfcd550dc236c7c0eb5fc12de7760f0d.jpg) *Figure 5.4: Success rate curves on Coffee Lake.*

- 特别地，在 **Coffee Lake** 平台上，无论是 **无效化缓存** 还是 **预热缓存**，都能使最大读事务容量远超基线，接近文献中报告的较高值（如几MB）。

![](images/5e6c6cb543e2599d4e8c5f0989ed846ab5137bcd7a6d78dd13489e494445c681.jpg) *Figure 5.9: Success rate curves on Coffee Lake when invalidating caches.*
![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*

**输入输出关系及整体作用**

- **输入**：
    - **Mutator**：正常的应用程序代码，带有轻量级的写屏障。
    - **Collector**：需要被回收的堆区域 (fromspace)，及其 remembered set。
- **输出**：
    - **Mutator**：在无 GC 干扰时，以接近原生的速度运行；在 GC 关键窗口期，其执行被 HTM 事务保护，确保一致性。
    - **Collector**：成功地将 fromspace 区域中的存活对象原子地移动到 tospace，并更新了所有堆内和栈上的引用。
- **在整体系统中的作用**：
    - 该算法提供了一种 **低开销** 的并发复制GC实现路径。它通过将高成本的持续性屏障（如读屏障）替换为低成本的、仅在必要时触发的 HTM 事务，有效降低了 **mutator的性能损耗**。
    - 其设计充分利用了现代 CPU 的 HTM 特性，并通过深入理解 HTM 的底层行为（如缓存交互）来指导优化，使得该方案在支持 HTM 的硬件上具有很高的实用潜力。

### 2. Collector-Mutator协调协议

**Collector-Mutator协调协议的核心目标**
- 解决**并发复制垃圾回收**（Concurrent Copying GC）中的一个根本性难题：在收集器（collector）完成对象移动（即提交事务）后，到mutator线程感知到这一变化并修正其栈上引用之前的这段时间窗口（称为“**问题间隙**”或“problematic gap”）内，mutator可能使用过时的**fromspace引用**，导致读取陈旧数据或写入丢失。
- 该协议通过一种巧妙的、基于**硬件事务内存**（HTM）的机制，避免了传统方案中高开销的**读屏障**（read barrier），仅在必要时让mutator短暂地在事务中执行，从而以较低的代价保证了堆的一致性。

**协议的关键组件与数据结构**
- **全局单调计数器 `CollectorCopyingState`**:
  - 这是一个全局共享的整型变量，用于向所有mutator线程广播收集器的当前状态。
  - 其值的**奇偶性**具有特定语义：
    - **奇数值**：表示收集器**正在尝试**进行一个复制事务。mutator看到此状态时，必须在其下一次执行中进入事务模式。
    - **偶数值**：表示一个（或多个）收集器事务**已经完成**（无论成功或失败）。mutator看到从奇数变为偶数的变化，就知道“问题间隙”可能已经发生，需要采取行动。
- **线程本地快照 `t.copyingState`**:
  - 每个mutator线程都维护一个本地副本，记录它最后一次观察到的`CollectorCopyingState`的值。
  - 通过比较本地快照和全局计数器，mutator可以判断是否有新的收集器事务在自己上次检查后完成。
- **Yieldpoint**:
  - 这是运行时系统中预设的安全点，如方法入口、循环回边等，允许mutator在此处被安全地中止或执行额外逻辑。
  - 在本协议中，yieldpoint是mutator与收集器进行**握手**（handshake）和执行栈修复（`fixStack`）的唯一场所。

**收集器端的协议流程**
- 收集器在启动一个新的复制事务前，会执行以下步骤：
  1. **递增计数器**：将全局`CollectorCopyingState`加1，使其变为**奇数**，向世界宣告一个新事务即将开始。
  2. **发起握手**：通过设置一个全局标志，请求所有活跃的mutator线程在下一个**yieldpoint**处执行`mutatorHandshake`。
  3. **等待确认**：收集器会**自旋等待**，直到所有mutator线程都更新了它们的本地`copyingState`快照，确认已知晓新的奇数状态。这确保了在事务开始前，所有mutator都已进入“警戒”状态。
  4. **执行事务**：在HTM事务中执行`copyRegion`操作，原子地移动对象并更新堆中的引用。
  5. **发布结果**：如果事务**成功提交**，再次将`CollectorCopyingState`加1，使其变为**偶数**，宣告事务完成。如果事务**中途中止**（abort），同样会将计数器加1（变为偶数），但此时堆并未发生实际变化。

**Mutator端的协议流程**
- Mutator的执行被组织成一系列由**yieldpoint**分隔的片段。在每个yieldpoint，mutator会执行`mutatorHandshake`，然后根据状态决定是否在事务中执行下一段代码。
- **`mutatorHandshake` 的逻辑**:
  - 获取当前的全局`CollectorCopyingState`快照（`csSnapshot`）。
  - 如果`csSnapshot`大于本地`copyingState`，说明有新事件发生。
  - 检查`(t.copyingState, csSnapshot]`这个区间内是否包含**偶数**。如果包含，则意味着至少有一个收集器事务**已经完成**。
  - 如果检测到已完成的事务，mutator会立即调用`fixStack()`，遍历自己的调用栈，将任何指向**fromspace**的引用更新为指向**tospace**的新地址。
  - 最后，用`csSnapshot`更新本地的`copyingState`。
- **Mutator主执行协议** (`mutator`):
  - 在`mutatorHandshake`之后，检查本地`copyingState`是否为**奇数**。
  - 如果是奇数，mutator会将其接下来的执行（直到下一个yieldpoint）包裹在一个HTM事务中。
  - 在事务提交前，会再次检查全局`CollectorCopyingState`。如果发现其值已大于本地`copyingState`（即计数器已被收集器再次递增，变为偶数），则**显式中止**（`XABORT`）当前mutator事务。
  - 这个显式中止或由HTM硬件检测到的冲突中止，会**回滚**mutator在“问题间隙”内的所有错误执行，并强制其回到yieldpoint重新执行`mutatorHandshake`，从而安全地修复栈并继续。

**输入输出关系及在整体中的作用**
- **输入**:
  - 对于**收集器**：需要回收的**region**（堆区域）及其**remembered set**（记录了所有从外部指向该区域的引用）。
  - 对于**mutator**：普通的应用程序字节码/指令流。
- **输出**:
  - 对于**收集器**：一个被清空的**fromspace region**，以及一个包含所有存活对象的**tospace region**。全局`CollectorCopyingState`被更新以反映操作结果。
  - 对于**mutator**：正确、一致的程序执行。其栈上的所有引用始终指向有效的对象（**tospace**版本），且不会丢失任何在对象移动期间发生的写入。
- **在整体中的作用**:
  - 该协议是整个HTM GC算法的**核心同步机制**，它优雅地解决了并发复制中最棘手的“**问题间隙**”难题。
  - 它成功地将保证一致性的重担，从对**每一次堆读取**都施加开销的**读屏障**，转移到了仅在**收集器活跃时**才触发的、相对低频的**事务性执行**和**yieldpoint握手**上。
  - 这种设计极大地**降低了mutator的常规执行开销**，使得低暂停时间的并发复制GC在通用硬件上变得更为可行。![](images/8b375db05156e9ea8aed0dff8505f95304e194664632086d16ecd5828f5cebc3.jpg) *Table 4.1: Machines used in the evaluation.*

### 3. 乐观复制优化 (Optimistic Copying)

**乐观复制优化 (Optimistic Copying) 的实现原理与流程**

- **核心动机**：Intel TSX 等 HTM 实现的 **写集 (write-set) 容量** 远小于 **读集 (read-set) 容量**（如论文第5章实验所示，写容量通常被限制在 L1 cache 大小，约20-30KB）。在 collector transaction 中直接执行对象复制会产生大量事务性写操作，极易因超出写容量而 abort。
- **核心思想**：将耗时的、产生大量写操作的 **实际复制 (actual copying)** 步骤移出 HTM 事务，在事务外完成。HTM 事务仅负责一个轻量级的 **验证 (validation)** 步骤，该步骤主要由读操作构成，从而极大地降低了对 HTM 写容量的需求。

*   **算法详细流程**：
    - **阶段一：事务外的乐观复制**
        - 对于 fromspace 中每一个待回收的可达对象 **O**，Collector 在一个专用的 **影子区域 (shadow region)** 中创建其逐字节的副本 **Os**。**Os** 充当了 **O** 在复制开始时刻的快照。
        - 接着，Collector 使用 **Os** 作为源数据，在 tospace 中创建目标对象 **O'**。这一步完成了所有繁重的内存写入工作，但完全在 HTM 事务之外进行，因此不消耗任何 HTM 写容量。
    - **阶段二：事务内的验证与提交**
        - Collector 启动一个 HTM 事务。
        - 在事务内，Collector **逐字节比较** 原始对象 **O** 和其影子副本 **Os**。
        - **验证成功**：如果 **O** 和 **Os** 完全一致，说明在事务外的复制过程中，Mutator **没有修改 O**。此时，**O'** 是 **O** 的一个有效且完整的副本。Collector 可以安全地在事务内执行以下原子操作：
            - 将 **O** 的 **转发指针 (forwarding pointer)** 设置为指向 **O'**。
            - 遍历 **O** 的 **remembered set**，将所有指向 **O** 的堆内引用更新为指向 **O'**。
        - **验证失败**：如果 **O** 和 **Os** 不一致，说明 Mutator 在复制过程中修改了 **O**，导致 **O'** 是一个过时的、不正确的副本。此时，Collector **显式中止 (XABORT)** 当前事务。整个过程可以重试，或者采用更复杂的修复策略（如论文所述，可以在事务内通过比较差异来修补 **O'**）。

**输入输出关系及在整体系统中的作用**

- **输入**：
    - **fromspace** 中的一组待移动的可达对象。
    - 一个空闲的 **影子区域 (shadow region)** 用于存放快照。
- **输出**：
    - **tospace** 中正确、完整的新对象副本。
    - **fromspace** 对象头中的 **转发指针** 被原子地设置。
    - 所有相关的 **堆内引用** 被原子地更新。
    - **fromspace** 的原始区域被释放。
- **在整体 GC 算法中的作用**：
    - **降低 HTM 事务负载**：这是该优化最直接的作用。通过将写密集型操作移出事务，显著提高了 collector transaction 的 **成功率 (success rate)**，尤其是在需要移动大量或大型对象时。
    - **维持并发安全性**：该方案巧妙地利用了 HTM 的原子性和隔离性来解决 **lost update problem**。验证步骤确保了只有在对象未被 Mutator 并发修改的情况下，引用更新才是安全的。如果发生并发修改，事务会 abort，保证了系统的强一致性。
    - **提升吞吐量**：更高的事务成功率意味着 Collector 能够更高效地完成区域回收工作，减少了因事务反复 abort 而造成的 CPU 周期浪费，从而提升了整体的 GC 吞吐量和应用性能。

---
![](images/6cfaa4e583958ba2970f31ac7b07255d9be2c8e86ed9ace96340668c8b1117e5.jpg) *Figure 5.8: Success rate curves on Coffee Lake when reusing memory.*
![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*

**关键参数与设计考量**

- **影子区域 (shadow region) 管理**：需要一个高效的机制来分配和回收影子区域的内存。其生命周期很短，仅在一个 collector transaction 的上下文中存在。
- **比较粒度**：逐字节比较虽然简单可靠，但可能不是最高效的。未来可以考虑基于对象字段或缓存行的比较，以减少不必要的内存访问。
- **修复策略**：论文提到了一种高级优化，即在验证失败时，不是简单地 abort，而是在事务内根据 **O** 和 **Os** 的差异来 **修复 (repair)** **O'**。这可以避免一次完整的重试，但会增加事务内的逻辑复杂度和潜在的写操作。

### 4. 缓存预热优化 (Cache Warmup)

**缓存预热优化 (Cache Warmup) 的实现原理与作用**

- **核心动机**：该优化旨在解决 **HTM (Hardware Transactional Memory)** 事务因 **伪LRU (pseudo-LRU)** 缓存替换策略而导致的非必要中止。如论文第5.3节所述，即使事务的工作集小于缓存容量，伪LRU算法也可能错误地驱逐最近访问过的、属于当前事务的缓存行，从而触发 **容量中止 (capacity abort)**。
- **根本洞察**：论文通过实验（图5.10）发现，**预热缓存 (warming up the cache)** 能显著提升大型只读事务的成功率。其原理在于，通过预先将事务所需的数据加载到缓存中，可以避免在事务执行期间因缓存未命中而触发伪LRU替换逻辑，从而保护事务的关键数据不被意外驱逐。

**算法流程与具体实现**

- **触发时机**：该优化在 **收集器事务 (collector transaction)** 正式启动之前执行。
- **执行内容**：
    - 预先执行一遍 **收集器事务的主体代码逻辑**，特别是那些涉及大量内存读取的操作（例如，在“乐观复制”优化中，对 **shadow objects** 与原始对象的比较操作）。
    - **关键约束**：此预热执行阶段产生的所有计算结果和内存修改都会被 **丢弃 (discarded)**，它唯一的目的就是产生内存访问，以填充CPU缓存。
- **重复执行**：为了确保高概率命中，预热代码通常会 **执行多次**。这能最大化地将事务所需的所有相关 **缓存行 (cache lines)** 提升到缓存层次结构的高层（如L1/L2），并更新它们在伪LRU状态机中的“新鲜度”。

![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*

**输入输出关系及在整体系统中的作用**

- **输入**：待执行的 **收集器事务** 的代码路径及其所要访问的内存区域（主要是 **fromspace** 对象和 **shadow region** 中的副本）。
- **输出**：一个被 **预热 (warmed-up)** 的CPU缓存状态，其中包含了即将在事务中被频繁访问的数据。
- **在整体GC算法中的作用**：
    - **提升事务成功率**：通过减少由缓存子系统引起的非冲突性中止，使得 **收集器事务** 能够成功提交，从而顺利完成对象的并发复制和指针更新。
    - **增强算法实用性**：更高的事务成功率意味着 **HTM-based GC** 算法在真实硬件上更加稳定和可靠，这是证明其 **可行性 (viability)** 的关键一步。
    - **与“乐观复制”协同**：此优化特别适用于第8.6节提出的 **乐观复制 (Optimistic Copying)** 优化。因为乐观复制将事务内的大量写操作转换为读操作（用于比较），使得事务变成了一个大型的只读工作负载，而这正是 **缓存预热** 最能发挥效用的场景。

---
**与其他缓存策略的对比**

| 策略 | 操作 | 对HTM事务成功率的影响 | 对系统整体性能的副作用 |
| :--- | :--- | :--- | :--- |
| **无操作 (Baseline)** | 无 | 基准水平，易受伪LRU影响 | 无 |
| **缓存无效化 (Invalidation)** | 使用 `wbinvd` 指令清空所有缓存 | **提升**（图5.9） | **极高**，会清空指令和数据缓存，导致所有线程性能严重下降 |
| **缓存预热 (Warmup)** | 预执行事务代码（丢弃结果） | **显著提升**（图5.10） | **较低**，仅在GC线程上增加一次性的、可预测的预热开销 |

**结论**：**缓存预热** 是一种巧妙且实用的优化手段。它利用了对底层硬件（特别是缓存替换策略）的深刻理解，以一种低成本的方式，有效规避了 **Intel TSX** 等HTM实现中的一个关键限制，从而为构建低开销的 **并发复制垃圾回收器 (concurrent copying GC)** 铺平了道路。

### 5. HTM容量特性分析

**HTM容量特性分析的核心发现**

- 论文通过一系列精心设计的实验，揭示了 **Intel TSX** 的有效容量并非一个固定值，而是受到 **缓存状态 (cache status)** 和 **内存访问模式 (memory access pattern)** 的显著影响。
- 这一发现成功解释了为何先前文献中关于 **读集 (read-set)** 容量的报告存在巨大差异（从22KB到7.5MB不等），而 **写集 (write-set)** 容量则相对稳定（约20-25KB），始终受限于 **L1数据缓存** 的大小。

**基线实验与跨平台验证**

- 实验复现了 `rtm-bench` 基准测试，在 **Haswell** 平台上观察到读/写事务的成功率在 **16KB** 附近急剧下降，最大成功事务大小约为22-25KB，与Ritson和Barnes的早期结果一致。
- 在更新的微架构（**Broadwell**, **Skylake**, **Coffee Lake**）上重复实验，发现 **读集容量随微架构演进而增大**，但依然远未达到L3缓存的理论上限。这表明Intel对TSX的实现进行了改进，但其容量仍受硬件限制。
- ![](images/fca77d7a9e12d5dad7efe61d5344235db8aeb939383bcc018089466fd3496ab0.jpg) *Figure 5.1: Success rate curves on Haswell.*
- ![](images/573ff1d98148715e9ecdc109fc6fd39d4c0e260749622f993a571e0e8399bb0b.jpg) *Figure 5.2: Success rate curves on Broadwell.*
- ![](images/3e7ac435f47b2ee0991a4572a95522ad9c5ba4bbd81f69f34cc88f178b219055.jpg) *Figure 5.3: Success rate curves on Skylake.*
- ![](images/06532af4750ccb7976030552dd6e5c5ebfcd550dc236c7c0eb5fc12de7760f0d.jpg) *Figure 5.4: Success rate curves on Coffee Lake.*

**内存重用实验：揭示文献矛盾的关键**

- 大多数先前研究在测试不同大小的事务时，**重用同一块内存区域**。论文通过修改基准测试来模拟此行为。
- 结果显示，**重用内存区域能显著提升读事务的容量**。这是因为无论事务是否提交，其执行过程都会影响缓存内容。后续在同一区域上的事务更可能命中缓存，从而避免因缓存行被驱逐而导致的 **容量中止 (capacity abort)**。
- 这直接解释了为何一些报告了超大读容量（如数MB）的研究得出了看似矛盾的结论：他们的测试方法无意中利用了缓存预热效应。
- ![](images/285727733597f3a323012def6824b75ad555152879fa5c9c96af26f0cf96d698.jpg) *Fig. 5.5, Fig. 5.6, Fig. 5.7, and Fig. 5.8 for Haswell, Broadwell, Skylake and Coffee Lake respectively. Figure 5.5: Success rate curves on Haswell when reusing memory.*
- ![](images/ed375a170dc9add684be03c249f0760793d4cccae22ac348f32adbe664a98a69.jpg) *Figure 5.6: Success rate curves on Broadwell when reusing memory.*
- ![](images/ba35df4a1299a082ce069a3573c97208ee02b02f4a3d61c595d565f158b3644f.jpg) *Figure 5.7: Success rate curves on Skylake when reusing memory.*
- ![](images/6cfaa4e583958ba2970f31ac7b07255d9be2c8e86ed9ace96340668c8b1117e5.jpg) *Figure 5.8: Success rate curves on Coffee Lake when reusing memory.*

**缓存状态操控实验：深入机理**

- 为验证缓存状态是根本原因，论文在 **Coffee Lake** 平台上进行了更直接的操控实验：
  - **缓存清空 (Invalidation)**: 在每次事务前使用 `wbinvd` 指令清空所有级别的缓存。
  - **缓存预热 (Warmup)**: 在每次事务前，将事务将要读取的内存区域预先读取五次，以确保其驻留在缓存中。
- 实验结果出人意料：**无论是清空缓存还是预热缓存，都比基线（无操作）获得了更大的最大事务容量**，甚至接近了文献中报告的最大值。
- ![](images/5e6c6cb543e2599d4e8c5f0989ed846ab5137bcd7a6d78dd13489e494445c681.jpg) *Figure 5.9: Success rate curves on Coffee Lake when invalidating caches.*
- ![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*

**根本原因：伪LRU替换策略**

- 论文提出假说，认为这一现象的根本原因在于现代CPU普遍采用的 **伪LRU (pseudo-LRU)** 缓存替换策略，而非理想的 **LRU (Least Recently Used)**。
  - 在理想LRU下，只要事务工作集小于缓存，其访问的缓存行就不会被驱逐。
  - 但在 **伪LRU** 下，由于硬件实现的近似性，即使一个缓存行最近被访问过，也可能在缓存压力下被错误地驱逐，从而触发HTM的容量中止。
- **缓存清空** 之所以有效，是因为它清除了所有无效或无关的缓存行，为事务的工作集提供了“干净”的空间，避免了伪LRU算法的错误决策。
- **缓存预热** 之所以有效，是因为它提前将事务所需的数据加载到缓存中，并通过多次访问“巩固”了它们在伪LRU年龄队列中的位置，降低了在事务执行期间被驱逐的概率。

---
**对HTM-GC算法设计的指导意义**

- 这些关于HTM容量的深刻洞察，直接指导了后续 **HTM-GC** 算法的优化设计。
- 论文提出的 **缓存预热 (Cache Warmup)** 优化（见8.7节）正是基于此发现：在启动关键的 **收集器事务 (collector transaction)** 之前，先非事务性地执行一遍事务主体（特别是对象比较逻辑），以预热相关缓存行，从而**显著降低因缓存驱逐导致的事务中止率**，提升大事务的成功概率。
- 这种将底层硬件特性（HTM容量、缓存行为）与上层算法（垃圾回收）紧密结合的设计思路，是本研究的重要贡献之一。


---

## 4. 实验方法与实验结果

**实验设置**

- **硬件平台**: 实验在多种 Intel 微架构上进行，包括 **Haswell**, **Broadwell**, **Skylake**, 和 **Coffee Lake**。所有机器均关闭频率缩放（Intel Turbo Boost），但开启超线程（Hyper-Threading）。
- **软件平台**: 统一使用 **Ubuntu 18.04.5** (内核 5.4.0-47-generic) 和 **GCC 7.5.0** (编译标志 `-O2`)。系统在测试期间保持尽可能空闲。
- **基准测试**: 主要基于 **rtm-bench** 基准测试，并对其进行了修改以探究不同因素对 HTM 容量的影响。
- **GC 算法实现**: 在 **MMTk** 框架中实现。为了简化，一次只允许一个 **region** 进行并发复制回收，并通过 `System.gc()` 手动触发。只有带有 `@ConcurrentCollection` 注解的类的对象才会被分配到该 region 中，便于精确控制和调试。

**结果数据分析**

- **HTM 容量基线测量**:
    - 在 **Haswell** 上复现了 rtm-bench 的结果，读/写事务的成功率在 **16KB** 左右急剧下降，最大成功读/写事务分别约为 **22KB** 和 **25KB**。
    - 在更新的微架构（Broadwell, Skylake, Coffee Lake）上，**读容量**有所增加，但**写容量**始终稳定在 **20-25KB** 范围内，与 L1 数据缓存大小一致。
    - 这些结果解释了文献中看似矛盾的报告：早期工作（如 Ritson & Barnes）使用隔离内存区域，测得较低容量；而后期工作可能无意中利用了缓存效应，测得了更高容量。

- **影响 HTM 容量的关键因素**:
    - **内存区域复用**: 当为不同大小的事务重用同一块内存区域时，**读容量**在所有平台上都显著增加。这表明先前的事务（无论成功与否）会影响缓存状态，从而有利于后续大事务的提交。
        ![](images/285727733597f3a323012def6824b75ad555152879fa5c9c96af26f0cf96d698.jpg) *Fig. 5.5, Fig. 5.6, Fig. 5.7, and Fig. 5.8 for Haswell, Broadwell, Skylake and Coffee Lake respectively. Figure 5.5: Success rate curves on Haswell when reusing memory.*
        ![](images/ed375a170dc9add684be03c249f0760793d4cccae22ac348f32adbe664a98a69.jpg) *Figure 5.6: Success rate curves on Broadwell when reusing memory.*
        ![](images/ba35df4a1299a082ce069a3573c97208ee02b02f4a3d61c595d565f158b3644f.jpg) *Figure 5.7: Success rate curves on Skylake when reusing memory.*
        ![](images/6cfaa4e583958ba2970f31ac7b07255d9be2c8e86ed9ace96340668c8b1117e5.jpg) *Figure 5.8: Success rate curves on Coffee Lake when reusing memory.*
    - **缓存状态操作**: 在 **Coffee Lake** 上的实验表明，无论是**无效化缓存** (`wbinvd`) 还是**预热缓存**（在事务前多次读取目标内存），都能大幅提升**读容量**，使其更接近文献中报告的较高值（如接近 L3 缓存大小）。
        ![](images/5e6c6cb543e2599d4e8c5f0989ed846ab5137bcd7a6d78dd13489e494445c681.jpg) *Figure 5.9: Success rate curves on Coffee Lake when invalidating caches.*
        ![](images/3205642b8258cabc26576371092cc40f6fe045f106fec3d6a9e56798a14eb2d6.jpg) *Figure 5.10: Success rate curves on Coffee Lake when warming up caches.*
    - **根本原因**: 作者推测这与 CPU 使用的 **pseudo-LRU** 缓存替换策略有关。在完美 LRU 下，小于缓存的事务数据不会被驱逐，但 pseudo-LRU 可能会错误地驱逐最近使用的行。**无效化**确保了缓存完全为空，而**预热**则确保了所需数据已在缓存中，两者都避免了因替换策略不佳而导致的非必要驱逐和事务中止。

- **GC 算法可行性验证**:
    - 通过三个精心设计的手工测试程序验证了核心机制：
        1.  **栈根引用更新**: 验证了当对象直接从栈根可达时，GC 后其引用能被正确更新。
        2.  **避免更新丢失**: 验证了在 GC 过程中对对象的并发写入不会丢失，证明了收集器事务的原子性。
        3.  **传递可达对象处理**: 验证了非直接栈根可达的对象也能被正确追踪、复制，且堆内引用被正确更新。
    - 这些测试成功证明了所提出算法的核心机制——**通过 mutator 事务覆盖“问题间隙”**——是**可行**的。

**消融实验**

论文并未进行传统意义上的、针对最终 GC 性能的完整消融研究（例如，移除某个优化后测量吞吐量或暂停时间的变化）。然而，在 HTM 容量分析部分，其实验设计本身就构成了一系列关键的“消融”或对比实验，用于分离不同变量的影响：

- **内存访问模式的影响**:
    - **对照组**: 使用**隔离的、对齐的**内存区域进行每次事务测试（基线）。
    - **实验组**: **重用**同一块内存区域进行不同大小的事务测试。
    - **结论**: 内存访问模式（特别是缓存行的复用）对观测到的 HTM **读容量**有巨大影响。

- **缓存初始状态的影响**:
    - **对照组**: **No-op**（即基线设置）。
    - **实验组 1**: 在每次事务前执行 **`wbinvd`** 以**无效化**所有缓存。
    - **实验组 2**: 在每次事务前**预热**缓存（多次读取目标内存）。
    - **结论**: 缓存的初始状态（空、满但无关、满且相关）是决定大读事务能否成功的关键因素，这解释了文献中的差异并为优化提供了依据。

- **针对 GC 算法本身的优化**:
    - 论文提出了两项基于 HTM 容量洞察的优化：**Optimistic Copying**（将事务内大量写操作转为读操作）和 **Cache Warmup**（在收集器事务前预热缓存）。
    - **未来工作**部分明确指出，需要对这些优化进行**性能评估**，以量化它们对单次事务可处理对象数量的影响。这表明这些优化尚未经过严格的消融实验验证其在完整 GC 工作负载下的实际效益。

---

