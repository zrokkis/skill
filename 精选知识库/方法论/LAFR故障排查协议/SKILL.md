---
name: lafr_fault_troubleshooting_protocol
description: L.A.F.R. (Locate, Analyze, Fix, Record) 故障排查协议，旨在通过对齐“文档”与“代码”解决逻辑失调问题，并实现知识资产的闭环管理。
---

# L.A.F.R. 故障排查协议 (L.A.F.R. Fault Troubleshooting Protocol)

## 1. 核心定义 (Core Definition)
**Bug 的本质**：代码 (Code) 实现与设计规格 (Specification/Documentation) 之间的**对齐失败 (Alignment Failure)**。
**操作哲学**：禁止在未明确根因的情况下直接执行代码变更。Bug 的修复过程本质上是“信息熵”的消除过程。

## 2. 操作流程 (Operational Workflow)

### 2.1 定位 (Locate): 构建“案发现场” (Reconstructing the Scene)
在启动任何修复动作前，必须构建**黄金三角 (Golden Triangle)** 上下文：
1.  **规格文档 (Spec Document)**：明确原始设计意图、业务边界与逻辑约束。
2.  **关联源码 (Relevant Source Code)**：提取涉及报错逻辑的最小可行代码片段。
3.  **异常遥测 (Exception Telemetry)**：包含堆栈轨迹 (Stack Trace)、运行时上下文 (Runtime Context) 及错误复现步骤。

### 2.2 分析 (Analyze): 根因判别 (Category Identification)
通过 AI 辅助或手动审计，将故障归类为以下两种属性之一：
*   **执行层故障 (Implementation Failure)**：代码逻辑偏离了文档定义的预期行为（代码实现错误）。
*   **设计层故障 (Design Deficit)**：文档定义缺失、逻辑自相矛盾或未能覆盖极端边界场景（文档定义错误）。

### 2.3 修复 (Fix): 强制一致性恢复 (Enforced Consistency Recovery)
修复动作必须严格遵循以下分支路径：
*   **分支 A：执行层故障**
    - 直接生成并应用针对源码的 **修复补丁 (Patch)**。
*   **分支 B：设计层故障**（**严禁直接改代码**）
    1.  **文档重构 (Doc Refinement)**：首先修正或补全相关的规格文档。
    2.  **代码重生成 (Code Generation)**：基于更新后的文档，重新推导并实施代码变更。
    - **核心禁令**：禁止“黑盒修复” (Black-box Fix)，所有代码变更必须在文档层面获得逻辑支撑。

### 2.4 留痕 (Record): 知识闭环 (Knowledge Loop)
*   **协议演进**：将本次故障暴露的判定准则、特殊边界或规避策略更新至所属模块的 `SKILL.md`。
*   **预防复发**：通过知识资产的持续积累，将单一故障修复转化为系统性的 **风险对冲 (Risk Hedging)**。

## 3. 免责与约束 (Constraints)
*   **完整性原则**：在 Record 阶段严禁执行概括性合并，必须保留原子化的业务 ID 和关键逻辑映射。
*   **可追溯性**：每次 F 分支的操作必须能在版本控制系统中找到对应的文档变更关联。
