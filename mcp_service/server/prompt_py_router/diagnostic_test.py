import os
import shutil

# 获取当前脚本所在目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'
MODELS_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../models"))

def get_model_path():
    """镜像 router_cli.py 中的路径逻辑"""
    env_path = os.environ.get("PEER_MODEL_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    
    local_path = os.path.join(MODELS_ROOT, MODEL_NAME)
    if os.path.exists(local_path):
        return local_path
    
    return MODEL_NAME

def run_test(name, expected_substring, env_val=None, create_local=False):
    # 环境清理与准备
    if env_val:
        os.environ["PEER_MODEL_PATH"] = env_val
    elif "PEER_MODEL_PATH" in os.environ:
        del os.environ["PEER_MODEL_PATH"]
        
    local_dir = os.path.join(MODELS_ROOT, MODEL_NAME)
    if create_local:
        os.makedirs(local_dir, exist_ok=True)
    elif os.path.exists(local_dir):
        shutil.rmtree(MODELS_ROOT) # 清理局部 models 文件夹

    result = get_model_path()
    success = expected_substring in result
    print(f"[{name}]: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"  -> Path: {result}")
    
    if create_local: shutil.rmtree(MODELS_ROOT)

if __name__ == "__main__":
    print("🧪 Starting PEER Path Priority Diagnostics...\n")
    
    # 1. Fallback to Remote
    run_test("Test 1: Remote Fallback", expected_substring=MODEL_NAME)

    # 2. Local Dir Priority
    run_test("Test 2: Local Directory Alignment", expected_substring="mcp_service/models", create_local=True)

    # 3. Env Var Priority
    fake_path = "/tmp/peer_test_model"
    os.makedirs(fake_path, exist_ok=True)
    run_test("Test 3: Environment Variable Override", expected_substring=fake_path, env_val=fake_path, create_local=True)
    os.removedirs(fake_path)
