# Django 应用模板

这是一个基于 Python 3.12 和 Django 的现代化 Web 应用模板，集成了多个实用工具和最佳实践。

## 技术栈

- Python 3.12
- Django 5.0+
- Django REST Framework
- PostgreSQL
- Redis
- Supervisor
- Gunicorn
- Docker & Docker Compose
- GitLab CI/CD

## 特性

- 完整的 RESTful API 支持
- 容器化部署支持
- 自动化测试和部署流程
- 生产环境进程管理
- 缓存和会话管理
- 异步任务处理
- 环境变量配置

# 工程特性
- makefile 管理
- 使用 pre-commit 管理代码规范
- 使用 mypy 管理类型
- 使用 pytest 管理测试
- 使用 flake8 管理代码规范
- 使用 black 管理代码格式
- 使用 isort 管理代码导入
- 使用 sphinx 管理文档
- 使用 bandit 管理安全

## 快速开始

1. 克隆项目：

```bash
git clone <repository-url>
cd django_app_template
```

2. 创建环境变量文件：

```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

3. 使用 Docker Compose 启动项目：

```bash
docker-compose up --build
```

访问 http://localhost:8000 查看应用。

## 开发

1. 创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 运行迁移：

```bash
python manage.py migrate
```

4. 创建超级用户：

```bash
python manage.py createsuperuser
```

5. 启动开发服务器：

```bash
python manage.py runserver
```

## 部署

项目包含完整的 Docker 支持，可以轻松部署到任何支持 Docker 的环境。生产环境使用 Supervisor 管理 Gunicorn 进程。

1. 构建 Docker 镜像：

```bash
docker build -t django-app .
```

2. 运行容器：

```bash
docker run -d -p 8000:8000 django-app
```

## CI/CD

项目集成了 GitLab CI/CD 配置，包含以下阶段：

- 测试：运行单元测试
- 构建：构建 Docker 镜像
- 部署：部署到测试环境和生产环境

## 项目结构

```
.
├── core/                   # Django 项目核心配置
├── deploy/                 # 部署相关配置
│   └── supervisor/        # Supervisor 配置
├── requirements.txt       # Python 依赖
├── Dockerfile            # Docker 构建文件
├── docker-compose.yml    # Docker Compose 配置
├── .gitlab-ci.yml        # GitLab CI/CD 配置
└── .env.example          # 环境变量示例
```

## 许可证

MIT