# 文件名: ag_router.py
import sys, pickle, numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def route(user_input):
    with open("skills_cache.pkl", 'rb') as f:
        data = pickle.load(f)
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    emb = model.encode([user_input])
    sims = cosine_similarity(emb, data['embeddings'])[0]
    idx = np.argmax(sims)
    score, skill = sims[idx], data['metadata'][idx]

    if score < 0.5: return user_input # 低于阈值不干预

    with open(skill['path'], 'r') as f:
        template = f.read()

    # 高密度 Markdown 审计模版输出
    return f"""### [ROUTED_SKILL: {skill['name'].upper()} | SCORE: {score:.2f}]
---
{template}
---
**USER_INTENT**: {user_input}
**AUDIT_NOTE**: 确认上述框架逻辑符合需求后，请按 Enter 发送。"""

if __name__ == "__main__":
    print(route(sys.stdin.read()))