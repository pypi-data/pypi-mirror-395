# 文件上传 API 使用说明

## 概述

文件管理器现在支持通过 curl 命令直接上传文件，无需通过Web界面。

## API 端点

```
POST /files/api/upload/
```

## 基本用法

### 1. 上传文件（基本）

```bash
curl -X POST \
  -F "file=@/path/to/your/file.txt" \
  http://localhost:8000/files/api/upload/
```

### 2. 上传文件（带描述和标签）

```bash
curl -X POST \
  -F "file=@/path/to/your/file.txt" \
  -F "description=这是一个重要的文档文件" \
  -F "tags=文档,重要,工作" \
  -F "is_public=true" \
  http://localhost:8000/files/api/upload/
```

### 3. 上传图片文件

```bash
curl -X POST \
  -F "file=@/path/to/image.jpg" \
  -F "description=项目截图" \
  -F "tags=截图,项目,前端" \
  -F "is_public=false" \
  http://localhost:8000/files/api/upload/
```

## 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `file` | File | 是 | 要上传的文件 |
| `description` | String | 否 | 文件描述 |
| `tags` | String | 否 | 标签，用逗号分隔 |
| `is_public` | Boolean | 否 | 是否公开，默认false |

## 支持的文件类型

- 文档：`.txt`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`
- 图片：`.jpg`, `.jpeg`, `.png`, `.gif`
- 压缩：`.zip`, `.rar`

## 文件大小限制

最大文件大小：**10MB**

## 响应格式

### 成功响应 (201)

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

### 错误响应 (400/500)

```json
{
  "error": "错误描述信息"
}
```

## 实际示例

### 示例1：上传文本文件

```bash
# 创建一个测试文件
echo "这是一个测试文件" > test.txt

# 上传文件
curl -X POST \
  -F "file=@test.txt" \
  -F "description=测试文件" \
  -F "tags=测试,示例" \
  http://localhost:8000/files/api/upload/
```

### 示例2：上传多个文件

```bash
# 创建多个测试文件
echo "文件1内容" > file1.txt
echo "文件2内容" > file2.txt

# 上传文件1
curl -X POST \
  -F "file=@file1.txt" \
  -F "description=第一个文件" \
  -F "tags=文件1,测试" \
  http://localhost:8000/files/api/upload/

# 上传文件2
curl -X POST \
  -F "file=@file2.txt" \
  -F "description=第二个文件" \
  -F "tags=文件2,测试" \
  http://localhost:8000/files/api/upload/
```

### 示例3：使用变量

```bash
# 设置变量
FILE_PATH="/path/to/your/file.pdf"
DESCRIPTION="重要文档"
TAGS="文档,重要,PDF"

# 上传文件
curl -X POST \
  -F "file=@$FILE_PATH" \
  -F "description=$DESCRIPTION" \
  -F "tags=$TAGS" \
  -F "is_public=true" \
  http://localhost:8000/files/api/upload/
```

## 脚本化使用

### Bash 脚本示例

```bash
#!/bin/bash

# 文件上传脚本
upload_file() {
    local file_path="$1"
    local description="$2"
    local tags="$3"
    local is_public="${4:-false}"
    
    echo "正在上传文件: $file_path"
    
    response=$(curl -s -X POST \
        -F "file=@$file_path" \
        -F "description=$description" \
        -F "tags=$tags" \
        -F "is_public=$is_public" \
        http://localhost:8000/files/api/upload/)
    
    if [[ $? -eq 0 ]]; then
        echo "上传成功: $response"
    else
        echo "上传失败: $response"
    fi
}

# 使用示例
upload_file "document.pdf" "项目文档" "项目,文档,PDF" "true"
```

### Python 脚本示例

```python
import requests
import os

def upload_file(file_path, description="", tags="", is_public=False):
    """上传文件到文件管理器"""
    
    url = "http://localhost:8000/files/api/upload/"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'description': description,
            'tags': tags,
            'is_public': str(is_public).lower()
        }
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 201:
            print(f"上传成功: {response.json()}")
            return response.json()
        else:
            print(f"上传失败: {response.text}")
            return None

# 使用示例
upload_file(
    "example.txt",
    description="示例文件",
    tags="示例,测试,文本",
    is_public=True
)
```

## 注意事项

1. **无需认证**：此API端点无需登录认证
2. **文件大小**：单个文件不能超过10MB
3. **文件类型**：只支持指定的文件类型
4. **用户归属**：API上传的文件会归属于系统用户
5. **CSRF保护**：此端点已禁用CSRF保护以支持curl

## 故障排除

### 常见错误

1. **文件不存在**
   ```bash
   curl: (26) Couldn't open file '/path/to/file.txt'
   ```
   解决：检查文件路径是否正确

2. **文件过大**
   ```json
   {"error": "文件大小不能超过10MB"}
   ```
   解决：压缩文件或选择较小的文件

3. **不支持的文件类型**
   ```json
   {"error": "不支持的文件类型"}
   ```
   解决：使用支持的文件类型

4. **连接被拒绝**
   ```bash
   curl: (7) Failed to connect to localhost port 8000
   ```
   解决：确保Django服务器正在运行

## 更多信息

- Web界面：http://localhost:8000/files/
- 文件列表：http://localhost:8000/files/api/files/
- 项目文档：查看项目README.md 