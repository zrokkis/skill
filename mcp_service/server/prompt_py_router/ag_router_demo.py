
import pickle
import os
from sentence_transformers import SentenceTransformer, util

# 加载索引
CACHE_FILE = "skills_cache.pkl"
if not os.path.exists(CACHE_FILE):
    print(f"❌ 找不到索引文件 {CACHE_FILE}，请先运行 ag_indexer.py")
    exit()

print("⏳ 正在加载模型和索引 (首次运行可能稍慢)...")
with open(CACHE_FILE, 'rb') as f:
    data = pickle.load(f)
    stored_metadata = data['metadata']
    stored_embeddings = data['embeddings']

# 加载同一个模型
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def find_match(query, top_k=3):
    print(f"\n🔍 查询: '{query}'")
    
    # 1. 将查询转化为向量
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # 2. 计算余弦相似度
    # util.cos_sim 会自动高效地计算 query 与所有 stored_embeddings 的相似度
    hits = util.semantic_search(query_embedding, stored_embeddings, top_k=top_k)
    
    # hits 结构: [[{'corpus_id': 0, 'score': 0.85}, ...]]
    top_results = hits[0]
    
    # 3. 输出结果
    print(f"{'排名':<4} {'得分':<8} {'技能名称':<30} {'描述片段'}")
    print("-" * 80)
    for i, hit in enumerate(top_results):
        score = hit['score']
        meta = stored_metadata[hit['corpus_id']]
        # 读取描述的前50个字用于展示
        with open(meta['path'], 'r', encoding='utf-8') as f:
            content = f.read()
            import re
            match = re.search(r'^---\s+.*?description:\s*(.*?)\s+---', content, re.DOTALL | re.VERBOSE)
            desc_preview = match.group(1).strip()[:30] + "..." if match else "No desc"
            
        print(f"{i+1:<4} {score:.4f}   {meta['name']:<30} {desc_preview}")

if __name__ == "__main__":
    # 预设几个测试用例
    test_queries = [
        "在这个问题上，我想听听反面的意见，进行批判性思考",  # 应该匹配 6 Hats 或 Socratic 等
        "帮我把这个大目标拆解成可执行的小计划",           # 应该匹配 SMART
        "我想写一篇逻辑清晰的议论文"                     # 应该匹配 PEE 或 PREP
    ]
    
    for q in test_queries:
        find_match(q)
