#!/bin/bash
# 图片批量格式转换 MCP 服务器启动脚本

# 切换到项目目录
cd "$(dirname "$0")"

echo "================================================"
echo "  图片批量格式转换 MCP 服务器"
echo "================================================"
echo ""
echo "正在启动 MCP 服务器..."
echo ""

# 运行 MCP 服务器
python -m image_batch_converter

echo ""
echo "MCP 服务器已停止"
