#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🚀 Starting PEER Service Setup..."

# 1. 创建虚拟环境 (如果不存在)
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. 激活并安装依赖
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. 执行首次索引 (预下载模型)
echo "🔍 Building initial index (this may take a few minutes for model download)..."
python ag_indexer.py

echo "✅ Setup Complete!"
echo "------------------------------------------------"
echo "Your Python Path: $SCRIPT_DIR/venv/bin/python"
echo "Your Script Path: $SCRIPT_DIR/router_cli.py"
echo "------------------------------------------------"
echo "Please copy the paths above to your MCP config file."
