# 文件名: ag_indexer.py
import os, pickle
from sentence_transformers import SentenceTransformer


# 获取当前脚本所在目录的父级目录下的 prompt 文件夹
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../assets/expert_frameworks"))
CACHE_FILE = os.path.join(CURRENT_DIR, "skills_cache.pkl")

MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

def get_model_path():
    """优先级: 环境变量 -> 内置目录 -> 远程"""
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path): return env_path
    
    local_path = os.path.join(os.path.dirname(CURRENT_DIR), "../../models", MODEL_NAME)
    if os.path.exists(local_path): return local_path
    
    return MODEL_NAME

def build():
    # 优先加载本地模型
    model_path = get_model_path()
    print(f"📦 Indexing with model from: {model_path}")
    model = SentenceTransformer(model_path)
    skills_data, descriptions = [], []

    for root, _, files in os.walk(SKILLS_DIR):
        if 'SKILL.md' in files:
            path = os.path.join(root, 'SKILL.md')
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 使用正则提取 YAML frontmatter 中的 description
                # 匹配 key: value 格式，支持多行（虽然通常是一行，但正则兼容性更好）
                import re
                match = re.search(r'^---\s+.*?description:\s*(.*?)\s+---', content, re.DOTALL | re.VERBOSE)
                
                if match:
                    desc = match.group(1).strip()
                else:
                    # 如果没有 yaml 头，尝试回退到旧逻辑或设为文件名
                    parts = content.split('## Description')
                    if len(parts) > 1:
                        desc = parts[-1].split('##')[0].strip()
                    else:
                        print(f"⚠️ Warning: No description found for {os.path.basename(root)}")
                        desc = os.path.basename(root)
                
                skills_data.append({'name': os.path.basename(root), 'path': path})
                descriptions.append(desc)

    embeddings = model.encode(descriptions)
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump({'metadata': skills_data, 'embeddings': embeddings}, f)
    print(f"✅ 已索引 {len(descriptions)} 个框架至 {CACHE_FILE}")

if __name__ == "__main__": build()