import os
import pickle
import re
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer, util

mcp = FastMCP("Prompt Router Service")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(CURRENT_DIR, "skills_cache.pkl")
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

_model = None
_data = None

def get_model_path():
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path): return env_path
    # 统一探测项目根目录下的 mcp_service/models/
    local_path = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), "models", MODEL_NAME)
    if os.path.exists(local_path): return local_path
    return MODEL_NAME

def get_resources():
    global _model, _data
    if _model is None:
        model_path = get_model_path()
        _model = SentenceTransformer(model_path)
    if _data is None:
        if not os.path.exists(CACHE_FILE):
            from ag_indexer import build
            build()
        with open(CACHE_FILE, 'rb') as f:
            _data = pickle.load(f)
    return _model, _data

@mcp.tool()
def search_skill(query: str, top_k: int = 3) -> str:
    model, data = get_resources()
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, data['embeddings'], top_k=top_k)
    top_results = hits[0]
    
    results = []
    for hit in top_results:
        score = hit['score']
        meta = data['metadata'][hit['corpus_id']]
        rel_path = meta['path']
        abs_path = os.path.abspath(os.path.join(CURRENT_DIR, rel_path))
        
        desc = "No description available"
        if os.path.exists(abs_path):
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'description:\s*(.*?)\n', content)
                if match: desc = match.group(1).strip()
        
        results.append(f"分数: {score:.4f}\n名称: {meta['name']}\n路径: {abs_path}\n描述: {desc}\n" + "-"*20)
    return "\n".join(results)

@mcp.tool()
def prompt(query: str) -> str:
    model, data = get_resources()
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, data['embeddings'], top_k=1)
    best_hit = hits[0][0]
    meta = data['metadata'][best_hit['corpus_id']]
    
    # 还原绝对路径
    rel_path = meta['path']
    prompt_file = os.path.abspath(os.path.join(CURRENT_DIR, rel_path))
    
    if not os.path.exists(prompt_file):
        return f"错误：找不到框架文件 {prompt_file}"
        
    with open(prompt_file, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
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