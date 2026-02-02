# Prompt Format MCP Server

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-Supported-orange.svg)

## 1. 概述 (Overview)

`prompt_format` 是一个基于 **模型上下文协议 (Model Context Protocol, MCP)** 的高阶提示词路由服务。其核心逻辑是通过 **语义搜索 (Semantic Search)** 技术，从包含 50+ 种专家级提示词框架的知识库中，为用户的原始需求匹配最适配的逻辑框架，并自动编译为开箱即用的**深度增强提示词 (Enhanced Prompts)**。

## 2. 核心架构 (Architecture)

*   **/prompt**: 知识库目录，包含专家级提示词框架的 `SKILL.md` 定义。
*   **/prompt_py_router**: 逻辑路由引擎。

## 3. 安装指南 (Installation)

### 3.1 项目获取
```bash
git clone https://github.com/zrokkis/skills.git
cd skills/prompt_py_router
```

### 3.2 依赖安装 (二选一)

#### 方案 A: 全局安装 (推荐：配置简单)
直接将依赖安装至系统全局 Python 环境中：
```bash
pip3 install mcp sentence-transformers torch scikit-learn numpy
```

#### 方案 B: 虚拟环境安装 (推荐：环境隔离)
在项目目录下创建独立环境，避免干扰其他项目：
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install mcp sentence-transformers torch scikit-learn numpy
```

### 3.3 构建索引
在首次运行前，需对知识库进行向量化处理：
```bash
# 若使用虚拟环境，请先激活或使用 venv/bin/python3
python3 ag_indexer.py
```

## 4. IDE 与 MCP 集成 (Integration)

请将下文中的 `/path/to/project` 替换为您本地仓库的**实际绝对路径**。

### 4.1 Cursor 配置
1.  进入 `Settings` -> `Models` -> `MCP`。
2.  点击 `+ Add New MCP Server`。
3.  根据您的安装方案选择配置：

**方案 A (全局 Python):**
```json
{
  "mcpServers": {
    "prompt_format": {
      "command": "python3",
      "args": ["/path/to/project/prompt_py_router/router_cli.py"]
    }
  }
}
```

**方案 B (虚拟环境 - 推荐):**
```json
{
  "mcpServers": {
    "prompt_format": {
      "command": "/path/to/project/prompt_py_router/venv/bin/python3",
      "args": ["/path/to/project/prompt_py_router/router_cli.py"]
    }
  }
}
```

### 4.2 Antigravity 配置
在您的 MCP 配置文件中添加以下内容：

**方案 A (全局 Python):**
```json
{
  "mcpServers": {
    "prompt_format": {
      "command": "python3",
      "args": ["/path/to/project/prompt_py_router/router_cli.py"],
      "env": {
        "PYTHONPATH": "/path/to/project/prompt_py_router"
      }
    }
  }
}
```

**方案 B (虚拟环境 - 推荐):**
```json
{
  "mcpServers": {
    "prompt_format": {
      "command": "/path/to/project/prompt_py_router/venv/bin/python3",
      "args": ["/path/to/project/prompt_py_router/router_cli.py"],
      "env": {
        "PYTHONPATH": "/path/to/project/prompt_py_router"
      }
    }
  }
}
```

### 4.3 Claude Desktop 配置
编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`:

**方案 A (全局 Python):**
```json
{
  "mcpServers": {
    "prompt_format": {
      "command": "python3",
      "args": ["/path/to/project/prompt_py_router/router_cli.py"]
    }
  }
}
```

**方案 B (虚拟环境 - 推荐):**
```json
{
  "mcpServers": {
    "prompt_format": {
      "command": "/path/to/project/prompt_py_router/venv/bin/python3",
      "args": ["/path/to/project/prompt_py_router/router_cli.py"]
    }
  }
}
```

## 5. 使用方式 (Usage)

成功集成 MCP 后，您可以在 IDE (如 Cursor, Antigravity) 的辅助对话栏中直接通过工具调用（Tools/Plugins）或自然语言唤起以下功能：

### 🛠️ 工具 1: `search_skill`
**场景**：当您不确定哪个框架最适合您的任务时，先进行检索。
*   **输入参数**: `query` (您的原始需求，如：“我想写一篇关于 AI 伦理的反驳文”)。
*   **效果**: AI 将返回前 3 个最匹配的 Prompt 框架名称、置信度以及该框架的核心逻辑描述。

### 🛠️ 工具 2: `prompt` (核心推荐)
**场景**：直接获取经过框架增强后的终极提示词。
*   **输入参数**: `query` (您的业务需求)。
*   **效果**: AI 将自动执行以下逻辑：
    1.  语义识别您的需求。
    2.  从 50+ 框架中选出最优解。
    3.  **自动编译**：将框架的指令体系、专家角色设定与您的需求进行深度融合。
    4.  生成一段**即开即用**的专家级提示词全文。

---
