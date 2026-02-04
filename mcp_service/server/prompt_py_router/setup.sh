#!/bin/bash

# 获取脚本所在目录的绝对路径
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." && pwd )"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
CLI_PATH="$SCRIPT_DIR/router_cli.py"

cd "$SCRIPT_DIR"

echo "🚀 Starting PEER Service One-Stop Setup..."

# 1. 基础 Python 检查
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. 请先安装 Python 3.10+ (https://www.python.org/)"
    exit 1
fi

# 2. Pip 模块检查 (使用 python3 -m pip 以确保路径匹配)
if ! python3 -m pip --version &> /dev/null; then
    echo "⚠️  Pip not found. Attempting to install pip..."
    python3 -m ensurepip --default-pip || {
        echo "❌ Error: 无法自动安装 pip。请手动执行: curl https://bootstrap.pypa.io/get-pip.py | python3"
        exit 1
    }
fi

# 3. 创建虚拟环境 (对 venv 模块进行防御性检查)
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv || {
        echo "❌ Error: venv module missing."
        echo "💡 如果您在 Ubuntu/Debian 上，请执行: sudo apt update && sudo apt install python3-venv"
        exit 1
    }
fi

# 4. 依赖安装 (使用虚拟环境内的 pip)
echo "📥 Installing dependencies..."
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt || {
    echo "❌ Error: Dependency installation failed."
    exit 1
}

# 5. 初始化索引
echo "🔍 Initializing cognitive index..."
./venv/bin/python ag_indexer.py

echo -e "\n✅ Setup Complete! PEER is ready to serve."
echo "------------------------------------------------"
echo "💡 STEP 2: Add this to your MCP Config (Cursor/IDE):"
echo ""
echo "{"
echo "  \"mcpServers\": {"
echo "    \"prompt_format\": {"
echo "      \"command\": \"$PYTHON_BIN\","
echo "      \"args\": [\"$CLI_PATH\"]"
echo "    }"
echo "  }"
echo "}"
echo ""
echo "------------------------------------------------"
echo "🔗 Project Root: $ROOT_DIR"
