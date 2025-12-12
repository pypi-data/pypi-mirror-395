# Curl 文件上传示例

## 快速开始

### 基本上传
```bash
curl -X POST -F "file=@your_file.txt" http://localhost:8000/files/api/upload/
```

### 带描述和标签
```bash
curl -X POST \
  -F "file=@your_file.txt" \
  -F "description=文件描述" \
  -F "tags=标签1,标签2" \
  -F "is_public=true" \
  http://localhost:8000/files/api/upload/
```

## 常用示例

### 上传文本文件
```bash
curl -X POST \
  -F "file=@document.txt" \
  -F "description=重要文档" \
  -F "tags=文档,重要" \
  http://localhost:8000/files/api/upload/
```

### 上传图片
```bash
curl -X POST \
  -F "file=@screenshot.png" \
  -F "description=项目截图" \
  -F "tags=截图,项目" \
  http://localhost:8000/files/api/upload/
```

### 上传PDF文档
```bash
curl -X POST \
  -F "file=@report.pdf" \
  -F "description=月度报告" \
  -F "tags=报告,月度,PDF" \
  -F "is_public=true" \
  http://localhost:8000/files/api/upload/
```

### 上传压缩文件
```bash
curl -X POST \
  -F "file=@project.zip" \
  -F "description=项目源码" \
  -F "tags=源码,项目,ZIP" \
  http://localhost:8000/files/api/upload/
```

## 批量上传脚本

### Bash 脚本
```bash
#!/bin/bash
for file in *.txt; do
    echo "上传文件: $file"
    curl -s -X POST \
        -F "file=@$file" \
        -F "description=批量上传: $file" \
        -F "tags=批量,上传" \
        http://localhost:8000/files/api/upload/
    echo "完成: $file"
done
```

### Python 脚本
```python
import os
import requests

def upload_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'description': f'批量上传: {filename}'}
                response = requests.post('http://localhost:8000/files/api/upload/', 
                                      files=files, data=data)
                print(f"上传 {filename}: {response.status_code}")

# 使用
upload_files_in_directory('./documents/')
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `file` | 文件路径（必需） | `-F "file=@/path/to/file.txt"` |
| `description` | 文件描述 | `-F "description=这是文件描述"` |
| `tags` | 标签（逗号分隔） | `-F "tags=标签1,标签2,标签3"` |
| `is_public` | 是否公开 | `-F "is_public=true"` |

## 支持的文件类型

- **文档**: `.txt`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`
- **图片**: `.jpg`, `.jpeg`, `.png`, `.gif`
- **压缩**: `.zip`, `.rar`

## 文件大小限制

最大文件大小：**10MB**

## 响应示例

### 成功响应
```json
{
  "message": "文件上传成功",
  "file_id": 123,
  "file_name": "example.txt",
  "file_size": 1024,
  "file_type": "txt",
  "uploaded_at": "2025-08-21T10:30:00Z",
  "download_url": "/files/file/123/download/",
  "view_url": "/files/file/123/"
}
```

### 错误响应
```json
{
  "error": "文件大小不能超过10MB"
}
```

## 故障排除

### 常见问题

1. **服务器未运行**
   ```bash
   curl: (7) Failed to connect to localhost port 8000
   ```
   解决：启动Django服务器 `python manage.py runserver 0.0.0.0:8000`

2. **文件不存在**
   ```bash
   curl: (26) Couldn't open file 'file.txt'
   ```
   解决：检查文件路径是否正确

3. **文件过大**
   ```json
   {"error": "文件大小不能超过10MB"}
   ```
   解决：压缩文件或选择较小的文件

4. **不支持的文件类型**
   ```json
   {"error": "不支持的文件类型"}
   ```
   解决：使用支持的文件类型

## 测试命令

运行测试脚本：
```bash
./test_curl_upload.sh
```

手动测试：
```bash
# 创建测试文件
echo "测试内容" > test.txt

# 上传测试
curl -X POST -F "file=@test.txt" http://localhost:8000/files/api/upload/

# 清理
rm test.txt
``` 