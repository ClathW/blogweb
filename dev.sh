#!/bin/bash
set -e

# BlogWeb 一键开发启动脚本
# 同时启动 Django 后端 (8000) 和 Vue 前端 (5173)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cleanup() {
    echo ""
    echo "正在停止服务..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "已停止"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 检查依赖
check_deps() {
    if ! command -v uv &>/dev/null; then
        echo "[ERR] 未安装 uv，请先安装: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    if ! command -v node &>/dev/null; then
        echo "[ERR] 未安装 Node.js"
        exit 1
    fi
}

# 每次启动自动检查
auto_init() {
    cd "$SCRIPT_DIR/backend"
    uv sync --quiet 2>/dev/null
    uv run python manage.py migrate --run-syncdb 2>/dev/null
    uv run python manage.py initadmin 2>/dev/null
    cd "$SCRIPT_DIR"

    if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
        echo "安装前端依赖..."
        cd "$SCRIPT_DIR/frontend"
        npm install --silent
        cd "$SCRIPT_DIR"
    fi
}

echo "BlogWeb 启动中..."
echo ""
check_deps
auto_init

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  后端:  http://localhost:8000"
echo "  前端:  http://localhost:5173"
echo "  API:   http://localhost:8000/api/"
echo "  Admin: http://localhost:8000/admin/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "按 Ctrl+C 停止所有服务"
echo ""

# 启动后端
cd "$SCRIPT_DIR/backend"
uv run python manage.py runserver 2>&1 &
BACKEND_PID=$!

# 启动前端
cd "$SCRIPT_DIR/frontend"
npm run dev 2>&1 &
FRONTEND_PID=$!

wait
