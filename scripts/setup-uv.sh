#!/bin/bash

# Manim MCP Server - UV 快速设置脚本
# 此脚本帮助用户快速设置 UV 开发环境

set -e  # 遇到错误时退出

echo "🚀 Manim MCP Server - UV 快速设置"
echo "=================================="

# 检查是否已安装 UV
if ! command -v uv &> /dev/null; then
    echo "📦 安装 UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # 添加到当前会话的 PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "✅ UV 安装完成"
else
    echo "✅ UV 已安装: $(uv --version)"
fi

# 检查 Python 版本
echo "🐍 检查 Python 版本..."
if ! python3 --version | grep -q "3.1[0-9]"; then
    echo "⚠️  警告: 推荐使用 Python 3.10 或更高版本"
    echo "当前版本: $(python3 --version)"
    echo "继续安装可能遇到兼容性问题"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Python 版本符合要求: $(python3 --version)"
fi

# 同步依赖
echo "📚 同步项目依赖..."
uv sync

echo "🧪 验证安装..."
# 基本导入测试
if uv run python -c "import src.server; print('✅ 服务器模块导入成功')" 2>/dev/null; then
    echo "✅ 项目依赖验证成功"
else
    echo "❌ 项目依赖验证失败"
    echo "请检查错误信息并手动解决"
fi

echo ""
echo "🎉 设置完成！"
echo ""
echo "📋 下一步操作:"
echo "1. 激活虚拟环境:"
echo "   source .venv/bin/activate"
echo ""
echo "2. 运行服务器:"
echo "   uv run python src/server.py"
echo ""
echo "3. 运行测试:"
echo "   uv run pytest tests/"
echo ""
echo "4. 查看更多 UV 用法:"
echo "   cat UV_GUIDE.md"
echo ""
echo "🔗 有问题? 查看文档:"
echo "   - README.md"
echo "   - INSTALL.md"
echo "   - UV_GUIDE.md" 