# BlogWeb

全栈博客系统，基于 Django + DRF 和 Vue 3。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Django 6 + Django REST Framework |
| 前端 | Vue 3 + Vite |
| 数据库 | SQLite（开发）/ MySQL 8.0 或 PostgreSQL 15（部署） |
| 后端包管理 | uv |
| 前端包管理 | npm |

## 功能

- 用户注册、登录、个人信息管理
- 文章发布、编辑、删除（软删除）、分类筛选、分页浏览
- 文章评论
- 管理员后台：用户管理、文章管理、评论管理

## 项目结构

```
blogweb/
  dev.sh              # 一键启动脚本
  backend/
    config/           # Django 项目配置
    users/            # 用户模块（User 模型、认证 API、管理命令）
    articles/         # 文章模块（Article、Category 模型、文章 API）
    comments/         # 评论模块（Comment 模型、评论 API）
    manage.py
  frontend/
    src/
      api/            # API 请求模块（auth、articles、comments、admin）
      stores/         # Pinia 状态管理（auth）
      router/         # Vue Router 路由配置
      views/          # 页面组件
      components/     # 可复用组件
```

## 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — Python 包管理器
- Node.js 20+

### 安装 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 快速开始

### 一键启动

```bash
./dev.sh
```

首次运行会自动安装依赖、迁移数据库、创建默认管理员 `admin / admin123`。

### 手动启动

**后端：**

```bash
cd backend
uv sync
cp .env.example .env
uv run python manage.py migrate
uv run python manage.py initadmin
uv run python manage.py runserver
```

**前端：**

```bash
cd frontend
npm install
npm run dev
```

浏览器访问 `http://localhost:5173`。

## 创建管理员

```bash
cd backend

# 默认账号 admin / admin123
uv run python manage.py initadmin

# 自定义
uv run python manage.py initadmin --username myadmin --password mypass
```

## 运行测试

```bash
# 后端
cd backend && uv run python manage.py test

# 前端
cd frontend && npm run test
```

## Docker Compose 部署

推荐在 VPS 上使用 Docker Compose 部署生产环境：

```bash
git clone https://github.com/ClathW/blogweb.git /opt/blogweb
cd /opt/blogweb
cp .env.production.example .env.production
```

编辑 `.env.production`：

```env
SECRET_KEY=替换为随机长密钥
DEBUG=False
ALLOWED_HOSTS=你的域名,服务器IP
CORS_ALLOWED_ORIGINS=https://你的域名
CSRF_TRUSTED_ORIGINS=https://你的域名
POSTGRES_PASSWORD=替换为强密码
DJANGO_SUPERUSER_PASSWORD=替换为强密码
```

启动：

```bash
docker compose --env-file .env.production build
docker compose --env-file .env.production up -d
```

服务组成：

| 服务 | 说明 |
|---|---|
| `nginx` | 托管 Vue 静态文件，并反代 `/api/`、`/admin/` |
| `backend` | Django + Gunicorn |
| `db` | PostgreSQL |

默认暴露 `HTTP_PORT=80`。如果使用 HTTPS，建议在 VPS 外层再放 Caddy、Nginx Proxy Manager 或云厂商负载均衡做 TLS 终止，并把 `.env.production` 中的 `CSRF_COOKIE_SECURE`、`SESSION_COOKIE_SECURE` 设为 `True`。

手动部署更新：

```bash
APP_DIR=/opt/blogweb BRANCH=main sh deploy/deploy.sh
```

## CI/CD

本仓库包含两个 GitHub Actions workflow：

| 文件 | 触发 | 作用 |
|---|---|---|
| `.github/workflows/ci.yml` | PR、`main` push | 后端测试、前端测试、前端构建、npm audit |
| `.github/workflows/deploy.yml` | `main` 上 CI 成功后 | SSH 到 VPS 执行 `deploy/deploy.sh` |

在 GitHub 仓库 `Settings -> Secrets and variables -> Actions` 中配置：

| Secret | 示例 | 说明 |
|---|---|---|
| `VPS_HOST` | `1.2.3.4` | VPS IP 或域名 |
| `VPS_PORT` | `22` | SSH 端口，可省略 |
| `VPS_USER` | `deploy` | SSH 用户 |
| `VPS_SSH_KEY` | 私钥内容 | 能登录 VPS 的私钥 |
| `VPS_APP_DIR` | `/opt/blogweb` | VPS 上项目目录，可省略 |

首次部署前，需要先在 VPS 上安装 Docker 和 Docker Compose，并把仓库 clone 到 `VPS_APP_DIR`。后续 `main` 分支 CI 通过后会自动部署。

## 环境变量

`backend/.env` 中可配置：

| 字段 | 说明 | 默认值 |
|---|---|---|
| `SECRET_KEY` | Django 密钥 | 内置值（仅开发） |
| `DEBUG` | 调试模式 | `True` |
| `ALLOWED_HOSTS` | 允许访问的域名（逗号分隔） | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | 允许跨域的前端地址 | `http://localhost:5173` |

## API 概览

| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | `/api/auth/register/` | 用户注册 | - |
| POST | `/api/auth/login/` | 用户登录 | - |
| POST | `/api/auth/logout/` | 用户登出 | Session |
| GET | `/api/auth/check/` | 登录状态检查 | Session |
| GET | `/api/user/profile/` | 获取个人信息 | Session |
| PUT | `/api/user/profile/` | 修改个人信息 | Session |
| PUT | `/api/user/password/` | 修改密码 | Session |
| GET | `/api/articles/` | 文章列表 | - |
| POST | `/api/articles/create/` | 发布文章 | Session |
| GET | `/api/articles/{id}/` | 文章详情 | - |
| PUT | `/api/articles/{id}/edit/` | 编辑文章 | Session |
| DELETE | `/api/articles/{id}/edit/` | 删除文章 | Session |
| GET | `/api/articles/my/` | 我的文章 | Session |
| GET | `/api/articles/{id}/comments/` | 文章评论列表 | - |
| POST | `/api/articles/{id}/comments/create/` | 发表评论 | Session |
| DELETE | `/api/comments/{id}/` | 删除评论 | Session |
| GET | `/api/categories/` | 分类列表 | - |
| GET | `/api/admin/users/` | 用户管理列表 | Admin |
| PUT | `/api/admin/users/{id}/status/` | 用户状态变更 | Admin |
| GET | `/api/admin/articles/` | 文章管理列表 | Admin |
| DELETE | `/api/admin/articles/{id}/` | 强制删除文章 | Admin |
| GET | `/api/admin/comments/` | 评论管理列表 | Admin |
| DELETE | `/api/admin/comments/{id}/` | 强制删除评论 | Admin |

## 协作流程

`main` 分支受保护，需通过 Pull Request 提交：

```bash
git checkout main && git pull
git checkout -b 分支名
# 开发、提交
git push origin 分支名
```

然后在 GitHub 创建 Pull Request 等待合并。
