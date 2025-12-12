#!/bin/bash
set -e

VERSION_TYPE=${1:-patch}  # 默认 patch

# 检查环境变量
if [ -z "$TWINE_USERNAME" ] || [ -z "$TWINE_PASSWORD" ]; then
    echo "❌ 错误: 请先设置 TWINE_USERNAME 和 TWINE_PASSWORD 环境变量"
    echo "在 ~/.zshrc 中添加:"
    echo "export TWINE_USERNAME=__token__"
    echo "export TWINE_PASSWORD=pypi-your-token"
    exit 1
fi

echo "📦 开始发布流程..."

# 更新版本
echo "🔢 更新版本号: $VERSION_TYPE"
hatch version $VERSION_TYPE
NEW_VERSION=$(hatch version)
echo "✅ 新版本: $NEW_VERSION"

# 构建
echo "🔨 清理并构建包..."
rm -rf dist/
python -m build

# 上传
echo "🚀 上传到 PyPI..."
twine upload dist/*

echo "✅ 发布成功: v$NEW_VERSION"
echo "📍 查看: https://pypi.org/project/rag-agent-mcp/$NEW_VERSION/"
