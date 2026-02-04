# Prompt Engineering Expert Router (PEER)

![System Status](https://img.shields.io/badge/Status-Operational-success)
![Asset Count](https://img.shields.io/badge/Expert_Frameworks-56-blueviolet)
![Architecture](https://img.shields.io/badge/Architecture-MCP_Service-blue)

## 1. 核心定义 (Core Definition)

**Prompt Engineering Expert Router (PEER)** 是一套基于 **模型上下文协议 (Model Context Protocol, MCP)** 构建的认知增强引擎。它通过 **检索增强生成 (Retrieval-Augmented Generation, RAG)** 技术，将零散的用户需求与结构化的高阶提示词框架进行动态映射，旨在实现指令集从“草稿级”到“专家级”的自动化跃迁。

## 2. 架构设计 (System Architecture)

本项目遵循**职能解耦 (Functional Decoupling)** 原则，采用三层目录体系：

| 模块 | 路径 | 核心职能 |
| :--- | :--- | :--- |
| **Logic Engine** | `mcp_service/server/prompt_py_router/` | 负责语义搜索、向量编码及 MCP 协议分发。 |
| **Asset Library** | `mcp_service/assets/expert_frameworks/` | 存储 50+ 套包含 YAML 元数据的原子化 Prompt 框架。 |
| **Knowledge Base**| `精选知识库/` | 收录由 Erin 亲自调研产出的“第一手业务资产”。 |

## 3. 技术路线 (Technical Stack)

*   **向量模型 (Embedding Model)**: 使用 `paraphrase-multilingual-mpnet-base-v2`，支持多语言语义对齐。
*   **计算框架 (Compute Framework)**: 优先调用 Mac 本地 **Metal Performance Shaders (MPS)** 进行 GPU 加速。
*   **路由算法 (Routing Algorithm)**: 基于余弦相似度 (Cosine Similarity) 的 Top-K 检索算法。

## 4. 快速安装 (Quick Start)

为了确保环境隔离与模型自动下载，请执行以下命令完成一键初始化：

```bash
cd mcp_service/server/prompt_py_router/
chmod +x setup.sh
./setup.sh
```

> **注意**: 首次运行 `./setup.sh` 会从 Hugging Face 下载约 1GB 的向量模型，请保持网络畅通。

## 5. IDE 集成配置 (IDE Integration)

初始化完成后，脚本会输出两个关键路径。请将它们填入您的 MCP 配置文件中（如 `mcp_config.json` 或 Cursor 设置）：

### 5.1 配置模板 (JSON)
```json
"prompt_format": {
  "command": "[PASTE_PYTHON_PATH_HERE]",
  "args": ["[PASTE_ROUTER_CLI_PATH_HERE]"]
}
```

## 6. 常见问题 (FAQ)

*   **Q: 运行失败，提示 `ModuleNotFoundError`？**
    *   A: 请确保您使用的是虚拟环境中的 Python 路径（即 `venv/bin/python`），而非系统自带的 Python。
*   **Q: 下载模型太慢？**
    *   A: 首次运行需要连接外网。若在中国境内，建议配置镜像源或使用科学上网工具。
*   **Q: 如何更新 Prompt 框架资产？**
    *   A: 直接在 `mcp_service/assets/expert_frameworks/` 中增删文件，系统在下次启动时会自动触发增量索引同步。

## 7. 交互协议 (Interaction Protocol)

本项目提供两大核心 MCP 工具，极大提升 Prompt 编写效率：

1.  **`search_skill(query)`**: 输出语义最接近的 Top-3 框架及其应用场景说明。
2.  **`prompt(query)`**: **[闭环工具]**。自动检索 Top-1 框架并在内存中完成模板编译，直接输出可直接交付给 LLM 的终极指令。

---

> **⚠ 资产保护协议 (Knowledge Asset Protection)**:
> 严禁执行任何概括性或抽象化的合并操作。请保持文档的‘原子化’（Atomicity），确保每一个具体的业务 ID 和 Key 对照表处于随时可被全局搜索的状态。

**Maintainer**: Erin
**Last Updated**: 2026-02-04
