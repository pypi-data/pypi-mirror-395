# Pinia 状态管理使用指南

## 📦 已创建的 Store

### 1. **auth Store** - 认证状态管理
位置: `src/stores/auth.ts`

**功能：**
- 管理登录 token
- 处理登录/登出逻辑
- 获取用户信息

**使用示例：**
```typescript
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()

// 检查是否已登录
if (authStore.isAuthenticated) {
  // 已登录
}

// 登录
await authStore.userLogin({
  username: 'admin',
  password: 'admin123'
})

// 登出
await authStore.userLogout()

// 获取用户信息
const userInfo = await authStore.fetchUserInfo()
```

### 2. **user Store** - 用户信息管理
位置: `src/stores/user.ts`

**功能：**
- 管理当前用户信息
- 提供用户相关的计算属性

**使用示例：**
```typescript
import { useUserStore } from '@/stores'

const userStore = useUserStore()

// 访问用户信息
console.log(userStore.userInfo)
console.log(userStore.username)
console.log(userStore.email)
console.log(userStore.role)
console.log(userStore.isAdmin) // 是否为管理员

// 更新用户信息
userStore.setUserInfo(newUserInfo)
userStore.updateUserInfo({ username: 'newName' })

// 清除用户信息
userStore.clearUserInfo()
```

### 3. **theme Store** - 主题管理
位置: `src/stores/theme.ts`

**功能：**
- 管理深色/浅色主题
- 自动同步到 localStorage
- 监听系统主题变化

**使用示例：**
```typescript
import { useThemeStore } from '@/stores'

const themeStore = useThemeStore()

// 访问主题状态
console.log(themeStore.isDark) // boolean
console.log(themeStore.theme)  // 'dark' | 'light'

// 切换主题
themeStore.toggleTheme()

// 设置主题
themeStore.setTheme('dark')
themeStore.setTheme('light')
```

## 🔄 迁移说明

### 已迁移的组件

1. **Login.vue** - 使用 `authStore` 和 `userStore`
2. **AdminLayout.vue** - 使用 `themeStore`、`userStore`、`authStore`
3. **router/index.ts** - 使用 `authStore` 检查登录状态

### 替换 localStorage 的使用

**之前：**
```typescript
// 读取 token
const token = localStorage.getItem('token')

// 保存 token
localStorage.setItem('token', token)
```

**现在：**
```typescript
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()
const token = authStore.token // 响应式
```

## 📝 在其他组件中使用

### 示例 1: 在组件中检查登录状态

```vue
<script setup lang="ts">
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()

if (!authStore.isAuthenticated) {
  // 未登录，跳转到登录页
  router.push('/admin/login')
}
</script>
```

### 示例 2: 显示用户信息

```vue
<template>
  <div>
    <p>用户名: {{ userStore.username }}</p>
    <p>邮箱: {{ userStore.email }}</p>
    <p v-if="userStore.isAdmin">您是管理员</p>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores'

const userStore = useUserStore()
</script>
```

### 示例 3: 切换主题

```vue
<template>
  <el-button @click="toggleTheme">
    {{ themeStore.isDark ? '切换到浅色' : '切换到深色' }}
  </el-button>
</template>

<script setup lang="ts">
import { useThemeStore } from '@/stores'

const themeStore = useThemeStore()
const toggleTheme = () => themeStore.toggleTheme()
</script>
```

## 🎯 最佳实践

### 1. 统一导入
```typescript
// 推荐：从统一入口导入
import { useAuthStore, useUserStore, useThemeStore } from '@/stores'
```

### 2. 在 setup 中使用
```typescript
// ✅ 正确
const authStore = useAuthStore()

// ❌ 错误（在 setup 外使用）
const authStore = useAuthStore() // 必须在 setup 中调用
```

### 3. 响应式访问
```typescript
// ✅ 正确 - 使用计算属性或 ref
const isAuth = computed(() => authStore.isAuthenticated)

// ✅ 正确 - 直接访问（自动响应式）
const token = authStore.token

// ❌ 错误 - 解构会失去响应式
const { token } = authStore // 不要这样做
```

### 4. 使用 storeToRefs 保持响应式
```typescript
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()
const { token, isAuthenticated } = storeToRefs(authStore) // 保持响应式
```

## 🔧 扩展 Store

### 添加新的 Store

1. 在 `src/stores/` 目录创建新文件
2. 使用 `defineStore` 定义
3. 在 `src/stores/index.ts` 中导出

**示例：**
```typescript
// src/stores/settings.ts
import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', () => {
  const language = ref('zh-CN')
  
  const setLanguage = (lang: string) => {
    language.value = lang
  }
  
  return {
    language,
    setLanguage,
  }
})
```

## 📚 相关文档

- [Pinia 官方文档](https://pinia.vuejs.org/)
- [Vue 3 Composition API](https://vuejs.org/api/composition-api-setup.html)

