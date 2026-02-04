#!/bin/bash

# 获取脚本所在目录的绝对路径
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." && pwd )"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
CLI_PATH="$SCRIPT_DIR/router_cli.py"

cd "$SCRIPT_DIR"

echo "🚀 Starting PEER Service One-Stop Setup..."

# 1. 环境校验
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3.10+"
    exit 1
fi

# 2. 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 3. 安装依赖
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. 初始化索引
echo "🔍 Initializing cognitive index..."
python ag_indexer.py

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
