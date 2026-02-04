# 文件名: ag_indexer.py
import os, pickle
import re
from sentence_transformers import SentenceTransformer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 扩展扫描路径：支持多个资产目录
ASSETS_PATHS = [
    os.path.abspath(os.path.join(CURRENT_DIR, "../../assets/expert_frameworks")),
    os.path.abspath(os.path.join(ROOT_DIR := os.path.dirname(os.path.dirname(CURRENT_DIR)), "精选知识库"))
]
CACHE_FILE = os.path.join(CURRENT_DIR, "skills_cache.pkl")

# 升级为 SOTA 级的 BGE-M3 模型 (1024 维度)
MODEL_NAME = 'BAAI/bge-m3'

def get_model_path():
    """优先级: 环境变量 -> 内置目录 -> 远程"""
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path): return env_path
    local_path = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), "models", MODEL_NAME.split('/')[-1])
    if os.path.exists(local_path): return local_path
    return MODEL_NAME

def build():
    model_path = get_model_path()
    print(f"🚀 [Upgrade] Indexing with 1024D Model: {model_path}")
    model = SentenceTransformer(model_path)
    
    skills_data, descriptions = [], []

    for base_path in ASSETS_PATHS:
        if not os.path.exists(base_path):
            print(f"⚠️ Skip missing path: {base_path}")
            continue
            
        print(f"📂 Scanning assets in: {base_path}")
        for root, _, files in os.walk(base_path):
            # 支持 SKILL.md (框架) 和普通的 .md (知识库文档)
            target_files = [f for f in files if f.endswith('.md')]
            
            for filename in target_files:
                path = os.path.join(root, filename)
                # 排除 README 等非核心内容
                if filename.lower() == 'readme.md' and "expert_frameworks" in path: continue
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 优先提取 YAML description 或开头摘要
                    match = re.search(r'description:\s*(.*?)\n', content)
                    if match:
                        desc = match.group(1).strip()
                    else:
                        # 截取前 100 个字符作为语义索引预览
                        clean_content = re.sub(r'[#*`\-]', '', content[:300]).strip()
                        desc = clean_content.split('\n')[0][:150]
                    
                    rel_path = os.path.relpath(path, CURRENT_DIR)
                    name = f"[{os.path.basename(os.path.dirname(path))}] {filename}"
                    
                    skills_data.append({'name': name, 'path': rel_path, 'type': 'framework' if 'SKILL.md' in filename else 'knowledge'})
                    descriptions.append(f"{name}: {desc}")

    print(f"🧠 Generating Embeddings for {len(descriptions)} assets...")
    embeddings = model.encode(descriptions, batch_size=16, show_progress_bar=True)
    
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump({'metadata': skills_data, 'embeddings': embeddings, 'model_ver': MODEL_NAME}, f)
    print(f"✅ Hybrid Index Completed: {len(descriptions)} assets -> {CACHE_FILE}")

if __name__ == "__main__": build()