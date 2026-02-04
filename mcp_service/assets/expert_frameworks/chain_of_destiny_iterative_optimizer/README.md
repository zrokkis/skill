# Chain of Destiny 框架 (Chain of Destiny Framework)

Chain of Destiny (命运之链？注：此处Juuzt.ai命名可能为独创或是对 Chain of Density 的变体，根据内容其实质为迭代优化框架) 是一种强调迭代卓越的提示词工程方法。它不追求一步到位，而是通过“初始提示 -> 迭代 -> 反馈 -> 精炼”的循环过程，逐步将普通输出打磨成高质量的卓越成果。这是一种将“敏捷开发”思想引入 Prompt Engineering 的框架。

## 核心组成部分 (Core Components)

1. **初始提示 (Initial Prompt)**：从定义手头任务的基准提示词开始。
2. **迭代 (Iteration)**：实施反馈循环，允许根据 AI 的输出进行连续的改进。
3. **反馈 (Feedback)**：提供旨在提高响应的精准度、相关性和深度的具体反馈。
4. **精炼 (Refinement)**：通过迭代，逐步完善提示词和 AI 的输出，使其更好地与预期结果保持一致。

---

## 提示词示例 (Prompt Examples)

### 示例 1：博客文章优化 (Blog Post Optimization)
* **任务**：撰写一篇关于可持续生活实践的博客文章。
* **结构化迭代流程**：
    * **初始提示 (Initial Prompt)**：“写一篇关于可持续生活实践的博客文章。”
    * **迭代 (Iteration)**：“阅完初稿后，请建议更多具体的可持续实践例子。”
    * **反馈 (Feedback)**：“强调需要更深入的解释或更有说服力的证据的部分。”
    * **精炼 (Refinement)**：“整合上述反馈，专注于清晰度、引人入胜的故事讲述和可操作的建议，重写文章。”

### 示例 2：产品代码重构 (Code Refactoring)
* **任务**：重构一个遗留的 Python 函数。
* **结构化迭代流程**：
    * **初始提示 (Initial Prompt)**：“请重构这段代码，使其符合 PEP8 规范。”
    * **迭代 (Iteration)**：“代码现在符合规范了，但这部分的循环效率看起来很低。”
    * **反馈 (Feedback)**：“请指出具体的性能瓶颈，并解释为什么 vectorization 会比循环更好。”
    * **精炼 (Refinement)**：“应用 NumPy 的向量化操作重写该函数，并添加详细的文档字符串(docstring)。”

