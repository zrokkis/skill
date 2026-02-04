# 文件名: ag_indexer.py
import os, pickle
import re
from sentence_transformers import SentenceTransformer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../assets/expert_frameworks"))
CACHE_FILE = os.path.join(CURRENT_DIR, "skills_cache.pkl")
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

def get_model_path():
    """优先级: 环境变量 -> 内置目录 -> 远程"""
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path): return env_path
    local_path = os.path.join(os.path.dirname(CURRENT_DIR), "models", MODEL_NAME)
    if os.path.exists(local_path): return local_path
    return MODEL_NAME

def build():
    model_path = get_model_path()
    print(f"📦 Indexing with model from: {model_path}")
    model = SentenceTransformer(model_path)
    skills_data, descriptions = [], []

    for root, _, files in os.walk(SKILLS_DIR):
        if 'SKILL.md' in files:
            path = os.path.join(root, 'SKILL.md')
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'^---\s+.*?description:\s*(.*?)\s+---', content, re.DOTALL | re.VERBOSE)
                if match:
                    desc = match.group(1).strip()
                else:
                    desc = os.path.basename(root)
                
                # 关键：存储相对于 CURRENT_DIR 的路径
                rel_path = os.path.relpath(path, CURRENT_DIR)
                skills_data.append({'name': os.path.basename(root), 'path': rel_path})
                descriptions.append(desc)

    embeddings = model.encode(descriptions)
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump({'metadata': skills_data, 'embeddings': embeddings}, f)
    print(f"✅ Indexed {len(descriptions)} frameworks into {CACHE_FILE}")

if __name__ == "__main__": build()