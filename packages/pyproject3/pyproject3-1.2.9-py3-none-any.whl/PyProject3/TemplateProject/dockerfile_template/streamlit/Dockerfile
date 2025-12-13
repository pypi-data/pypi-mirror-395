# 使用 Python 官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序文件
COPY . .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 启动 Streamlit 应用
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]