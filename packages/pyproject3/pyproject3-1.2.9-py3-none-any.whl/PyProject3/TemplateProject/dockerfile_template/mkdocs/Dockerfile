# 使用 Python 官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /docs

# 安装 vim
RUN apt-get update && \
    apt-get install -y vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 mkdocs 及常用插件
RUN pip install --no-cache-dir \
    mkdocs \
    mkdocs-material \
    mkdocs-minify-plugin \
    mkdocs-git-revision-date-localized-plugin \
    pymdown-extensions

# 复制文档源文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]