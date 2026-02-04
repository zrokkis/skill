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

## 4. 极致部署 (Two-Step Deployment)

为了实现真正的一站式体验，请按以下步骤操作：

### Step 1: 自动化环境初始化
在终端运行以下命令：
```bash
cd mcp_service/server/prompt_py_router/
chmod +x setup.sh
./setup.sh
```
该脚本会自动完成：虚拟环境创建 -> 依赖安装 -> 模型检测 -> 环境索引。

### Step 2: 注入 IDE 配置
脚本运行结束时会输出一段 **JSON 配置**。请将其直接粘贴到您的 `mcp_config.json` 或 IDE 的 MCP 服务器设置中。

---

## 5. 离线模式 (Offline Support)

若您的开发环境无法访问 Hugging Face，请遵循以下步骤手动配置模型：

### 5.1 手动下载模型 (推荐)
1.  在有网环境下载模型。
2.  在项目根目录下创建 `mcp_service/models/` 文件夹。
3.  将模型完整文件夹放入其中，路径结构应为：`mcp_service/models/paraphrase-multilingual-mpnet-base-v2/config.json` 等。

### 5.2 环境变量指定 (高级)
若不想在项目内放置模型，可使用环境变量。**注意：必须使用系统绝对路径**，以确保在不同工作目录下启动时均能正确加载。
```bash
# MacOS/Linux 示例
export PEER_MODEL_PATH="/Users/yourname/models/paraphrase-multilingual-mpnet-base-v2"
```

---

## 6. 常见问题 (FAQ)

*   **Q: 如何确认我的模型路径配置是否生效？**
    *   A: 运行 `python3 mcp_service/server/prompt_py_router/diagnostic_test.py`。该脚本会自动模拟不同场景，验证系统是否能正确识别您的本地模型或环境变量。

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
