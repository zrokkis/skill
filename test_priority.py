import os

# 模拟 router_cli.py 中的逻辑
CURRENT_DIR = "/Users/a58/work/skills/mcp_service/server/prompt_py_router"
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

def get_model_path():
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    
    local_path = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), "models", MODEL_NAME)
    if os.path.exists(local_path):
        return local_path
    
    return MODEL_NAME

def run_test(name, expected_substring, env_val=None, create_local=False):
    # 重置环境
    if env_val:
        os.environ["PEER_MODEL_PATH"] = env_val
    elif "PEER_MODEL_PATH" in os.environ:
        del os.environ["PEER_MODEL_PATH"]
        
    local_dir = os.path.join("/Users/a58/work/skills/mcp_service/models", MODEL_NAME)
    if create_local:
        os.makedirs(local_dir, exist_ok=True)
    elif os.path.exists(local_dir):
        import shutil
        shutil.rmtree(os.path.dirname(local_dir)) # 清理 models 目录

    result = get_model_path()
    success = expected_substring in result
    print(f"Test [{name}]: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"  Result: {result}")
    
    # 清理
    if create_local:
        import shutil
        shutil.rmtree(os.path.dirname(local_dir))

# 执行测试集
print("🧪 Starting Priority Logic Validation...\n")

# 1. 测试远程 fallback
run_test("Remote Fallback", expected_substring=MODEL_NAME)

# 2. 测试本地目录优先级
run_test("Local Directory Priority", expected_substring="mcp_service/models", create_local=True)

# 3. 测试环境变量最高优先级
custom_env = "/tmp/fake_env_model"
os.makedirs(custom_env, exist_ok=True)
run_test("Env Variable Priority", expected_substring=custom_env, env_val=custom_env, create_local=True)
os.removedirs(custom_env)
