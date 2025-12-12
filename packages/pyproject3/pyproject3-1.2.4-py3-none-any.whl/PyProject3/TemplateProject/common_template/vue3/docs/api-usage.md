# API 使用指南

本文档说明如何在项目中添加和使用业务 API。

## 目录结构

```
src/api/
├── request.ts      # Axios 实例配置（请求/响应拦截器）
├── config.ts       # API 配置（端点、状态码等）
├── translate.ts    # 翻译相关 API
├── user.ts          # 用户管理 API
├── auth.ts         # 认证相关 API
└── index.ts        # 统一导出
```

## 添加新的业务 API

### 步骤 1: 定义类型（types/index.ts）

```typescript
// 例如：文章管理
export interface Article {
    id: number
    title: string
    content: string
    author_id: number
    created_at: string
}

export interface ArticleListParams {
    page?: number
    page_size?: number
    title?: string
    author_id?: number
}
```

### 步骤 2: 添加 API 端点（api/config.ts）

```typescript
export const API_ENDPOINTS = {
    // ... 现有端点
    article: '/articles',
    articleDetail: '/articles/:id',
} as const
```

### 步骤 3: 创建 API 文件（api/article.ts）

```typescript
import request from './request'
import { API_ENDPOINTS } from './config'
import type { Article, ArticleListParams } from '@/types'

/**
 * 获取文章列表
 */
export const getArticleList = async (params?: ArticleListParams) => {
    try {
        const response = await request<Article[]>({
            url: API_ENDPOINTS.article,
            method: 'GET',
            params: params,
        })
        return response
    } catch (error) {
        console.error('Get Article List Error:', error)
        throw new Error((error as Error).message || '获取文章列表失败')
    }
}

/**
 * 创建文章
 */
export const createArticle = async (data: Partial<Article>) => {
    try {
        const response = await request<Article>({
            url: API_ENDPOINTS.article,
            method: 'POST',
            data: data,
        })
        return response
    } catch (error) {
        console.error('Create Article Error:', error)
        throw new Error((error as Error).message || '创建文章失败')
    }
}
```

### 步骤 4: 导出 API（api/index.ts）

```typescript
// 文章相关 API
export * from './article'
```

## 在组件中使用 API

### 示例 1: 在组件中使用用户 API

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserList, createUser, deleteUser } from '@/api'
import type { User, CreateUserParams } from '@/types'
import { ElMessage } from 'element-plus'

const users = ref<User[]>([])
const loading = ref(false)

// 获取用户列表
const fetchUsers = async () => {
    loading.value = true
    try {
        const response = await getUserList({ page: 1, page_size: 10 })
        users.value = response.items
    } catch (error) {
        ElMessage.error('获取用户列表失败')
    } finally {
        loading.value = false
    }
}

// 创建用户
const handleCreate = async (userData: CreateUserParams) => {
    try {
        await createUser(userData)
        ElMessage.success('创建用户成功')
        fetchUsers() // 刷新列表
    } catch (error) {
        ElMessage.error('创建用户失败')
    }
}

// 删除用户
const handleDelete = async (id: number) => {
    try {
        await deleteUser(id)
        ElMessage.success('删除用户成功')
        fetchUsers() // 刷新列表
    } catch (error) {
        ElMessage.error('删除用户失败')
    }
}

onMounted(() => {
    fetchUsers()
})
</script>
```

### 示例 2: 使用认证 API

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, getUserInfo } from '@/api'
import type { LoginParams } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)

const handleLogin = async (form: LoginParams) => {
    loading.value = true
    try {
        const response = await login(form)
        
        // 保存 token 和用户信息
        localStorage.setItem('token', response.token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        ElMessage.success('登录成功')
        router.push('/admin/dashboard')
    } catch (error) {
        ElMessage.error('登录失败')
    } finally {
        loading.value = false
    }
}
</script>
```

## API 请求格式说明

### 请求拦截器自动处理

- **Token 认证**: 自动从 `localStorage` 读取 `token` 并添加到请求头
- **GET 请求**: 自动添加时间戳防止缓存
- **错误处理**: 自动处理常见 HTTP 状态码

### 响应格式

后端可以返回两种格式：

1. **标准格式**（推荐）:
```json
{
    "code": 200,
    "message": "成功",
    "data": { ... }
}
```

2. **直接数据格式**:
```json
{
    "id": 1,
    "name": "xxx"
}
```

响应拦截器会自动处理这两种格式。

## 错误处理

所有 API 函数都会：
1. 捕获错误并打印到控制台
2. 抛出包含错误信息的 Error
3. 在组件中可以通过 try-catch 捕获

```typescript
try {
    const user = await getUserById(1)
} catch (error) {
    // error 是 Error 类型
    console.error(error.message)
    ElMessage.error(error.message)
}
```

## 环境配置

### 开发环境
- 使用 Vite 代理: `/api` → `http://localhost:8000`
- 配置在 `vite.config.ts` 中

### 生产环境
- 通过环境变量 `VITE_API_BASE_URL` 配置
- 例如: `VITE_API_BASE_URL=https://api.example.com`

## 常见问题

### Q: 如何修改 API 基础地址？
A: 修改 `src/api/request.ts` 中的 `baseURL` 或设置环境变量 `VITE_API_BASE_URL`

### Q: 如何添加自定义请求头？
A: 在 `src/api/request.ts` 的请求拦截器中添加

### Q: 如何处理文件上传？
A: 使用 `FormData` 并设置 `Content-Type: multipart/form-data`

```typescript
const formData = new FormData()
formData.append('file', file)
await request({
    url: '/upload',
    method: 'POST',
    data: formData,
    headers: {
        'Content-Type': 'multipart/form-data',
    },
})
```

