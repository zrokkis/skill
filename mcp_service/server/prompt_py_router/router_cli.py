
# Triggering reload for high-dimensional model
import os
import pickle
import re
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer, util

# 初始化 MCP Server
mcp = FastMCP("Prompt Router Service")

# 路径配置
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(CURRENT_DIR, "skills_cache.pkl")
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

# 全局变量，懒加载
_model = None
_data = None

def get_resources():
    global _model, _data
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    if _data is None:
        if not os.path.exists(CACHE_FILE):
            print(f"⚠️ Index not found at {CACHE_FILE}. Building index now...")
            from ag_indexer import build
            build()
        with open(CACHE_FILE, 'rb') as f:
            _data = pickle.load(f)
    return _model, _data

@mcp.tool()
def search_skill(query: str, top_k: int = 3) -> str:
    """
    根据用户需求语义，从 50+ 个 Prompt 框架中检索最匹配的框架。
    输入 query 为用户的原始需求（如：帮我制定计划、我想写议论文）。
    返回值包含匹配度、框架名称及 SKILL.md 路径。
    """
    model, data = get_resources()
    
    # 1. 向量化查询
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # 2. 语义搜索
    hits = util.semantic_search(query_embedding, data['embeddings'], top_k=top_k)
    top_results = hits[0]
    
    results = []
    for hit in top_results:
        score = hit['score']
        meta = data['metadata'][hit['corpus_id']]
        
        # 尝试提取描述预览
        desc = "No description available"
        if os.path.exists(meta['path']):
            with open(meta['path'], 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'description:\s*(.*?)\n', content)
                if match:
                    desc = match.group(1).strip()
        
        results.append(f"分数: {score:.4f}\n名称: {meta['name']}\n路径: {meta['path']}\n描述: {desc}\n" + "-"*20)
    
    return "\n".join(results)

@mcp.tool()
def prompt(query: str) -> str:
    """
    语义匹配最合适的 Prompt 框架，并根据该框架的核心逻辑，将用户的输入自动化编译为高阶提示词。
    输入 query 为您的原始业务或写作需求。
    返回值是经过框架加持后的、即开即用的终极提示词。
    """
    model, data = get_resources()
    
    # 1. 寻找最强匹配 (Top-1)
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, data['embeddings'], top_k=1)
    best_hit = hits[0][0]
    meta = data['metadata'][best_hit['corpus_id']]
    
    # 2. 读取框架核心规则
    prompt_file = meta['path']
    if not os.path.exists(prompt_file):
        return f"错误：找不到框架文件 {prompt_file}"
        
    with open(prompt_file, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    # 3. 构造编译后的全量提示词 (Prompt Compilation)
    # 我们将框架的指令体系与用户的原始需求进行强绑定
    optimized_response = f"""
### 🎯 推荐框架：{meta['name'].replace('_', ' ').upper()}
**匹配置信度**: {best_hit['score']:.4f}

---

# 🚀 优化后的提示词 (Copy & Paste below)

你现在是一位在该领域具备深厚造诣的**行业专家**。请基于以下结构化框架，处理我的核心需求。

### 1. 核心任务 (The Task)
{query}

### 2. 执行逻辑与思考准则 (Framework Directives)
请严格遵循以下由 **[{meta['name']}]** 框架定义的执行标准进行输出：

{full_content}

---
**[使用说明]**: 以上内容已由于其内部包含完整的框架逻辑，请直接发送给 AI 即可获得专家级响应。
"""
    return optimized_response

if __name__ == "__main__":
    mcp.run()