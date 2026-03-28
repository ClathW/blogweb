# BlogWeb

全栈博客项目，后端使用 Django + DRF，前端使用 Vue + Vite。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Django 6 + Django REST Framework |
| 后端包管理 | uv |
| Python 版本 | 3.12 |
| 前端框架 | Vue 3 + Vite |
| 前端包管理 | npm |

## 项目结构

```
blogweb/
├── backend/        # Django 后端
│   ├── config/     # 项目配置（settings、urls、wsgi）
│   ├── manage.py
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .env.example
└── frontend/       # Vue 前端
    ├── src/
    ├── public/
    └── package.json
```

## 环境要求

- [uv](https://astral.sh/uv) — Python 包管理器
- [Node.js](https://nodejs.org) >= 18

### 安装 uv（未安装时）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 快速开始

### 1. 克隆仓库

```bash
git clone <仓库地址>
cd blogweb
```

### 2. 配置后端

```bash
cd backend

# 安装依赖（自动读取 uv.lock，版本完全一致）
uv sync

# 配置环境变量
cp .env.example .env
# 用编辑器打开 .env，按需修改
```

`.env` 各字段说明：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Django 密钥，生产环境必须替换 | 内置不安全值 |
| `DEBUG` | 调试模式，生产环境设为 `False` | `True` |
| `ALLOWED_HOSTS` | 允许访问的域名，逗号分隔 | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | 允许跨域的前端地址，逗号分隔 | `http://localhost:3000,http://127.0.0.1:3000` |

```bash
# 初始化数据库
uv run python manage.py migrate

# 启动开发服务器
uv run python manage.py runserver
# → http://localhost:8000
```

### 3. 配置前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# → http://localhost:5173
```

## 常用命令

### 后端

```bash
# 创建超级用户（用于登录 Django Admin）
uv run python manage.py createsuperuser

# 新增 app
uv run python manage.py startapp <app名>

# 生成数据库迁移文件
uv run python manage.py makemigrations

# 执行迁移
uv run python manage.py migrate

# 添加依赖
uv add <包名>
```

### 前端

```bash
# 构建生产包
npm run build

# 预览生产包
npm run preview
```
