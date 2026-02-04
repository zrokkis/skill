import os
import pickle
import re
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer, util

mcp = FastMCP("Prompt Router Service (V2 Optimized)")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(CURRENT_DIR, "skills_cache.pkl")
# 升级为 1024 维度模型
MODEL_NAME = 'BAAI/bge-m3'

_model = None
_data = None

def get_model_path():
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path): return env_path
    local_path = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), "models", MODEL_NAME.split('/')[-1])
    if os.path.exists(local_path): return local_path
    return MODEL_NAME

def get_resources():
    global _model, _data
    if _model is None:
        model_path = get_model_path()
        print(f"📦 Loading SOTA Model [1024D]: {model_path}")
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
    """
    语义检索 Expert 框架及精选知识库文档。
    支持跨域资产调度。
    """
    model, data = get_resources()
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, data['embeddings'], top_k=top_k)
    top_results = hits[0]
    
    results = []
    for hit in top_results:
        score = hit['score']
        meta = data['metadata'][hit['corpus_id']]
        abs_path = os.path.abspath(os.path.join(CURRENT_DIR, meta['path']))
        asset_type = meta.get('type', 'unknown').upper()
        
        results.append(f"[{asset_type}] 分数: {score:.4f}\n名称: {meta['name']}\n路径: {abs_path}\n" + "-"*20)
    return "\n".join(results)

@mcp.tool()
def prompt(query: str) -> str:
    """
    基于混合索引自动化生成增强提示词。
    如果检索到的是知识库文档，将作为 Context 注入；
    如果检索到的是 Framework，将作为 Logic 指令注入。
    """
    model, data = get_resources()
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, data['embeddings'], top_k=1)
    best_hit = hits[0][0]
    meta = data['metadata'][best_hit['corpus_id']]
    
    prompt_file = os.path.abspath(os.path.join(CURRENT_DIR, meta['path']))
    if not os.path.exists(prompt_file):
        return f"错误：找不到资产文件 {prompt_file}"
        
    with open(prompt_file, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    is_framework = meta.get('type') == 'framework'
    
    optimized_response = f"""
### 🎯 匹配资产：{meta['name']}
**匹配置信度**: {best_hit['score']:.4f}
**资产类型**: {"框架逻辑 (Logic)" if is_framework else "背景知识 (Context)"}

---

# 🚀 增强提示词 (Augmented Prompt)

你现在的角色是一位具备深厚背景的**行业领域专家**。请基于以下{"指令体系" if is_framework else "事实依据"}，处理我的核心需求。

### 1. 核心需求 (User Query)
{query}

### 2. {"框架指令" if is_framework else "背景参考"} (Expert Content)
{full_content}

---
**[PEER V2]**: 以上输出已完成跨域资产对齐。
"""
    return optimized_response

if __name__ == "__main__":
    mcp.run()