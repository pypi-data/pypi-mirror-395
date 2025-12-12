# Vue3 CMS Mock API

这是一个 FastAPI 实现的 Mock 后端，用于对接前端用户管理功能。

## 功能特性

### 用户管理 API
- ✅ `GET /users` - 获取用户列表（支持分页、搜索、筛选）
- ✅ `GET /users/{id}` - 获取用户详情
- ✅ `POST /users` - 创建用户
- ✅ `PUT /users/{id}` - 更新用户
- ✅ `DELETE /users/{id}` - 删除用户
- ✅ `DELETE /users/batch` - 批量删除用户

### 认证 API
- ✅ `POST /auth/login` - 用户登录
- ✅ `POST /auth/logout` - 用户登出
- ✅ `GET /auth/me` - 获取当前用户信息

## 安装依赖

```bash
pip install -r requirements.txt
```

或者使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 启动服务

```bash
python app.py
```

服务将在 `http://127.0.0.1:8000` 启动

## API 文档

启动服务后，可以访问：
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 测试账号

Mock 数据中预设了以下测试账号：

| 用户名 | 密码 | 角色 | 状态 |
|--------|------|------|------|
| admin | admin123 | admin | active |
| user1 | user123 | user | active |
| user2 | user123 | user | inactive |

## API 使用示例

### 1. 获取用户列表

```bash
curl "http://127.0.0.1:8000/users?page=1&page_size=10"
```

### 2. 搜索用户

```bash
curl "http://127.0.0.1:8000/users?username=admin&status=active"
```

### 3. 创建用户

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "123456",
    "role": "user",
    "status": "active"
  }'
```

### 4. 更新用户

```bash
curl -X PUT "http://127.0.0.1:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "updated_user",
    "status": "inactive"
  }'
```

### 5. 删除用户

```bash
curl -X DELETE "http://127.0.0.1:8000/users/1"
```

### 6. 用户登录

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

## 数据存储

⚠️ **注意**: 当前使用内存存储数据，服务重启后数据会丢失。实际项目中应该使用数据库（如 PostgreSQL、MySQL 等）。

## CORS 配置

当前配置允许所有来源的跨域请求（`allow_origins=["*"]`），生产环境应该指定具体的前端域名。

## 注意事项

1. 密码未加密存储，仅用于 Mock 测试
2. Token 是简单的字符串，实际项目应该使用 JWT
3. 数据存储在内存中，重启服务会丢失
4. 没有实现真正的权限验证

## 与前端对接

前端配置在 `vite.config.ts` 中已经设置了代理：

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),
  }
}
```

所以前端请求 `/api/users` 会被代理到 `http://localhost:8000/users`

