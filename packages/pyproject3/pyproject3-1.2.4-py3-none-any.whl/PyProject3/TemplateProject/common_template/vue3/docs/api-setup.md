# API 接入指南

## 📁 文件结构

```
src/api/
├── request.js      # Axios 实例配置（请求/响应拦截器）
├── config.js       # API 配置（端点、状态码等）
├── translate.js    # 翻译相关 API
└── index.js        # 统一导出
```

## 🚀 快速开始

### 1. 配置后端 API 地址

#### 方式一：修改 vite.config.js（开发环境）

在 `vite.config.js` 中修改代理目标：

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000', // 改为你的后端地址
    // ...
  }
}
```

#### 方式二：使用环境变量（推荐）

创建 `.env.development` 文件：

```bash
# 开发环境
VITE_API_BASE_URL=http://localhost:8000
```

创建 `.env.production` 文件：

```bash
# 生产环境
VITE_API_BASE_URL=https://your-api-domain.com
```

然后在 `vite.config.js` 中使用：

```javascript
target: process.env.VITE_API_BASE_URL || 'http://localhost:8000'
```

### 2. 后端 API 接口规范

#### 翻译接口示例

**请求：**
```http
POST /api/translate
Content-Type: application/json

{
  "text": "你好",
  "target_lang": "EN-US",
  "source_lang": "ZH" // 可选
}
```

**响应（方式一 - 直接返回数据）：**
```json
{
  "translatedText": "Hello"
}
```

**响应（方式二 - 标准格式）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "translatedText": "Hello"
  }
}
```

**响应（方式三 - 其他字段名）：**
```json
{
  "result": "Hello"
}
// 或
{
  "translation": "Hello"
}
```

如果后端返回格式不同，可以在 `src/api/translate.js` 中调整数据提取逻辑。

### 3. 添加认证 Token

如果需要添加认证，在 `src/api/request.js` 的请求拦截器中会自动从 localStorage 读取 token：

```javascript
const token = localStorage.getItem('token')
if (token) {
  config.headers.Authorization = `Bearer ${token}`
}
```

登录后保存 token：
```javascript
localStorage.setItem('token', 'your-token-here')
```

### 4. 使用 API

在组件中使用：

```vue
<script setup>
import { translateText } from '@/api/translate'

const handleTranslate = async () => {
  try {
    const result = await translateText({
      text: '你好',
      target_lang: 'EN-US'
    })
    console.log(result.translatedText)
  } catch (error) {
    console.error('翻译失败:', error)
  }
}
</script>
```

## 🔧 自定义配置

### 修改请求超时时间

在 `src/api/request.js` 中：

```javascript
const request = axios.create({
  timeout: 30000, // 修改为需要的超时时间（毫秒）
})
```

### 添加自定义请求头

在 `src/api/request.js` 的请求拦截器中：

```javascript
request.interceptors.request.use((config) => {
  config.headers['X-Custom-Header'] = 'value'
  return config
})
```

### 处理不同的响应格式

如果后端返回格式不同，修改 `src/api/request.js` 的响应拦截器：

```javascript
request.interceptors.response.use((response) => {
  const { data } = response
  
  // 根据你的后端格式调整
  if (data.success) {
    return data.data
  }
  
  return data
})
```

## 📝 添加新的 API

### 1. 创建新的 API 文件

例如：`src/api/user.js`

```javascript
import request from './request'
import { API_ENDPOINTS } from './config'

// 获取用户信息
export const getUserInfo = async (userId) => {
  return await request({
    url: `${API_ENDPOINTS.user}/${userId}`,
    method: 'GET',
  })
}

// 更新用户信息
export const updateUser = async (userId, data) => {
  return await request({
    url: `${API_ENDPOINTS.user}/${userId}`,
    method: 'PUT',
    data,
  })
}
```

### 2. 在 config.js 中添加端点

```javascript
export const API_ENDPOINTS = {
  translate: '/translate',
  user: '/user', // 新增
}
```

### 3. 在 index.js 中导出

```javascript
export * from './user'
```

## 🐛 调试技巧

### 查看请求日志

所有请求和响应都会在控制台输出日志，包括：
- 请求 URL、方法、参数
- 响应状态码
- 错误信息

### 使用浏览器开发者工具

1. 打开 Network 面板
2. 查看 `/api/*` 请求
3. 检查请求头、请求体、响应数据

### 常见问题

**问题：CORS 跨域错误**

解决：
- 确保后端设置了正确的 CORS 头
- 开发环境使用 Vite 代理（已配置）
- 生产环境需要后端支持 CORS

**问题：401 未授权**

解决：
- 检查 token 是否正确设置
- 检查 token 是否过期
- 确认后端认证逻辑

**问题：请求超时**

解决：
- 增加 `timeout` 配置
- 检查网络连接
- 检查后端服务是否正常运行

## 📚 更多示例

查看 `src/composables/useTranslator.js` 了解如何在 composable 中使用 API。

