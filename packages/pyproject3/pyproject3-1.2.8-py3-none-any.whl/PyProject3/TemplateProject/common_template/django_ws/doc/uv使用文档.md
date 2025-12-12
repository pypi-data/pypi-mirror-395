# UV 使用文档

## 简介

UV 是一个快速的 Python 包管理器和项目管理工具，由 Astral 开发。它提供了类似 pip 和 pip-tools 的功能，但速度更快。

## 安装

### 方法一：使用安装脚本（推荐）

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后，重启终端或运行 `source ~/.bashrc`（或相应的 shell 配置文件）。

### 方法二：使用 pip 安装

```bash
pip install uv
```

**注意**：虽然可以使用 pip 安装，但官方更推荐使用安装脚本，因为：
- 安装脚本会安装预编译的二进制文件，性能更好
- 通过 pip 安装的是 Python 包，可能性能略低
- 安装脚本会自动配置环境变量

### 方法三：使用包管理器

#### macOS (Homebrew)

```bash
brew install uv
```

#### Windows (Scoop)

```powershell
scoop install uv
```

## 基本使用

### 初始化项目

```bash
uv init
```

### 安装依赖

根据 `pyproject.toml` 安装项目依赖：

```bash
uv sync
```

### 添加依赖

```bash
# 添加依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 指定版本
uv add "django==5.1.3"
```

### 移除依赖

```bash
uv remove package-name
```

### 运行 Python 脚本

```bash
uv run python script.py
```

### 运行 Django 项目

```bash
# 运行开发服务器
uv run python manage.py runserver

# 运行迁移
uv run python manage.py migrate

# 创建超级用户
uv run python manage.py createsuperuser
```

### 激活虚拟环境

```bash
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

## 项目配置

本项目在 `pyproject.toml` 中配置了以下镜像源：

- 华为云镜像（默认）：`https://mirrors.huaweicloud.com/repository/pypi/simple`
- 本地镜像：`http://pypi.local.xmov.ai/xmov/release/+simple/`

## 常用命令

```bash
# 查看已安装的包
uv pip list

# 更新所有依赖
uv sync --upgrade

# 锁定依赖版本（生成 uv.lock）
uv lock

# 清理缓存
uv cache clean
```

## 与 pip 的对比

| 功能 | pip | uv |
|------|-----|-----|
| 安装速度 | 较慢 | 快（10-100倍） |
| 依赖解析 | 基础 | 更智能 |
| 项目管理 | 需要额外工具 | 内置支持 |
| 虚拟环境 | 需要 venv | 自动管理 |

## 注意事项

1. `uv.lock` 文件应该提交到版本控制系统，确保团队成员使用相同的依赖版本
2. 使用 `uv sync` 而不是 `pip install` 来安装依赖
3. 项目要求 Python 3.12，确保本地 Python 版本匹配

## 参考资源

- 官方文档：https://docs.astral.sh/uv/
- GitHub：https://github.com/astral-sh/uv

