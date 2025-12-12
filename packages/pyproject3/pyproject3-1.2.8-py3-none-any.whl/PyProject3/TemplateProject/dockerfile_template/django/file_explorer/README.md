# 文件上传下载功能

这是一个完整的 Django 文件上传下载系统，支持多种文件类型，包含用户权限管理和美观的 Web 界面。

## 功能特性

### 🚀 核心功能
- **文件上传**: 支持拖拽上传，最大文件大小 10MB
- **文件下载**: 安全的文件下载，支持权限控制
- **文件管理**: 完整的 CRUD 操作
- **用户权限**: 基于用户的文件访问控制
- **搜索功能**: 支持文件名、描述、标签搜索

### 📁 支持的文件类型
- **文档**: PDF, DOC, DOCX, XLS, XLSX, TXT
- **图片**: JPG, JPEG, PNG, GIF
- **压缩包**: ZIP, RAR

### 🔐 权限系统
- **私有文件**: 只有上传者和管理员可以访问
- **公开文件**: 所有用户都可以查看和下载
- **超级用户**: 可以管理所有文件

## 技术架构

### 后端技术
- **Django 5.1**: 主框架
- **Django REST Framework**: API 接口
- **SQLite**: 数据库（可配置为其他数据库）

### 前端技术
- **Bootstrap 5**: UI 框架
- **Font Awesome**: 图标库
- **原生 JavaScript**: 交互功能

## 安装和配置

### 1. 环境要求
- Python 3.8+
- Django 5.1+
- 其他依赖见 requirements.txt

### 2. 安装步骤
```bash
# 克隆项目
git clone <repository-url>
cd django_app_template

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建数据库迁移
python manage.py makemigrations file_explorer

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

### 3. 配置说明
在 `core/settings.py` 中已配置：
- 媒体文件路径: `MEDIA_ROOT = 'media/'`
- 临时文件路径: `FILE_UPLOAD_TEMP_DIR = 'temp/'`
- 最大文件大小: `FILE_UPLOAD_MAX_MEMORY_SIZE = 10MB`

## 使用方法

### Web 界面访问
- **文件列表**: http://localhost:8000/files/
- **文件上传**: http://localhost:8000/files/upload/
- **管理后台**: http://localhost:8000/admin/

### API 接口
- **文件列表**: `GET /files/api/files/`
- **文件上传**: `POST /files/api/files/`
- **文件下载**: `GET /files/api/files/{id}/download/`
- **我的文件**: `GET /files/api/files/my_files/`
- **公开文件**: `GET /files/api/files/public_files/`
- **搜索文件**: `GET /files/api/files/search/?q=关键词`

## 文件结构

```
file_explorer/
├── models.py          # 数据模型
├── views.py           # 视图逻辑
├── serializers.py     # 序列化器
├── urls.py            # URL 配置
├── admin.py           # 管理界面
├── apps.py            # 应用配置
└── templates/         # 模板文件
    └── file_explorer/
        ├── base.html      # 基础模板
        ├── file_list.html # 文件列表
        └── file_upload.html # 文件上传
```

## 模型设计

### FileUpload 模型
- **基本信息**: 文件名、原始名、文件路径、文件大小
- **类型信息**: 文件类型、MIME 类型
- **元数据**: 描述、标签、权限设置
- **用户信息**: 上传者、上传时间
- **统计信息**: 下载次数、最后下载时间

## 安全特性

### 文件验证
- 文件大小限制
- 文件类型白名单
- 文件内容验证

### 权限控制
- 基于用户的访问控制
- 文件所有权验证
- 管理员权限管理

### 安全防护
- CSRF 保护
- 文件路径安全
- 上传目录隔离

## 部署说明

### 生产环境配置
1. 修改 `DEBUG = False`
2. 配置生产数据库
3. 设置静态文件和媒体文件服务
4. 配置 HTTPS
5. 设置文件上传大小限制

### 性能优化
- 启用数据库连接池
- 配置 CDN 加速
- 启用文件压缩
- 设置缓存策略

## 扩展功能

### 可能的增强
- 文件预览功能
- 版本控制
- 批量操作
- 文件分享链接
- 云存储集成
- 文件加密

## 故障排除

### 常见问题
1. **文件上传失败**: 检查文件大小和类型限制
2. **权限错误**: 确认用户登录状态和文件权限
3. **数据库错误**: 检查迁移文件是否正确应用
4. **静态文件404**: 确认静态文件配置和收集

### 日志查看
- Django 日志: `logs/django.log`
- 应用日志: 控制台输出

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

本项目采用 MIT 许可证。 