# 管理后台使用指南

## 📋 功能概览

已创建完整的管理后台系统，包含以下功能模块：

### 1. 登录系统
- **路径**: `/admin/login`
- **功能**: 管理员登录
- **默认账号**: `admin` / `admin123`
- **特性**: 
  - 表单验证
  - 记住我功能
  - 登录状态管理

### 2. 仪表盘 (Dashboard)
- **路径**: `/admin/dashboard`
- **功能**: 
  - 数据统计卡片（用户数、翻译记录、成功率、响应时间）
  - 图表展示区域（可集成 ECharts）
  - 最近翻译记录
  - 系统通知

### 3. 用户管理 (User Management)
- **路径**: `/admin/users`
- **功能**:
  - 用户列表展示
  - 搜索和筛选
  - 新增用户
  - 编辑用户信息
  - 删除用户
  - 启用/禁用用户
  - 分页功能

### 4. 翻译记录 (Translations)
- **路径**: `/admin/translations`
- **功能**:
  - 翻译记录列表
  - 按语言筛选
  - 按日期范围筛选
  - 查看详情
  - 删除记录
  - 导出数据

### 5. 系统设置 (Settings)
- **路径**: `/admin/settings`
- **功能**:
  - 基本设置（系统名称、描述、API 地址等）
  - 功能开关（注册、邮件通知、短信通知、维护模式）
  - 系统信息展示
  - 快捷操作（清除缓存、重启服务、备份数据）

## 🎨 界面特性

### 布局设计
- **侧边栏导航**: 可折叠，响应式设计
- **顶部导航栏**: 面包屑导航、主题切换、用户菜单
- **内容区域**: 卡片式布局，支持深色模式

### 深色模式
- 所有页面支持深色模式
- 自动适配 Element Plus 组件
- 平滑过渡动画

### 响应式设计
- 支持移动端、平板、桌面端
- 自适应布局
- 触摸友好

## 🔐 权限管理

### 路由守卫
- 自动检查登录状态
- 未登录自动跳转到登录页
- 已登录访问登录页自动跳转到仪表盘

### Token 管理
- 登录后保存 token 到 localStorage
- 请求自动携带 token
- 退出登录清除 token

## 📁 文件结构

```
src/
├── layouts/
│   └── AdminLayout.vue          # 管理后台布局组件
├── views/
│   └── admin/
│       ├── Login.vue            # 登录页面
│       ├── Dashboard.vue        # 仪表盘
│       ├── UserManagement.vue   # 用户管理
│       ├── Translations.vue      # 翻译记录
│       └── Settings.vue         # 系统设置
└── router/
    └── index.ts                 # 路由配置（已更新）
```

## 🚀 快速开始

### 1. 访问管理后台
```
http://localhost:3001/admin/login
```

### 2. 登录
- 用户名: `admin`
- 密码: `admin123`

### 3. 导航
登录后会自动跳转到仪表盘，可以通过侧边栏导航访问各个功能模块。

## 🔧 自定义配置

### 修改默认登录账号
编辑 `src/views/admin/Login.vue`:
```typescript
const loginForm = reactive({
  username: 'your-username',
  password: 'your-password',
  remember: false,
})
```

### 添加新的菜单项
编辑 `src/layouts/AdminLayout.vue`:
```vue
<el-menu-item index="/admin/your-route">
  <el-icon><YourIcon /></el-icon>
  <template #title>菜单名称</template>
</el-menu-item>
```

然后在 `src/router/index.ts` 中添加路由：
```typescript
{
  path: 'your-route',
  name: 'YourPage',
  component: () => import('../views/admin/YourPage.vue'),
  meta: {
    title: '页面标题',
  },
}
```

### 集成真实 API
所有页面目前使用模拟数据，可以：

1. 在 `src/api/` 目录下创建对应的 API 文件
2. 在组件中导入并使用 API
3. 替换模拟数据

例如，用户管理页面：
```typescript
import { getUserList, createUser, updateUser, deleteUser } from '@/api/user'

// 替换模拟数据
const loadUsers = async () => {
  loading.value = true
  try {
    const res = await getUserList()
    tableData.value = res.data
  } finally {
    loading.value = false
  }
}
```

## 📊 数据展示

### 统计卡片
仪表盘的统计卡片可以连接真实 API：
```typescript
const stats = await getDashboardStats()
```

### 图表集成
可以集成 ECharts 或其他图表库：
```bash
npm install echarts
```

然后在组件中使用：
```vue
<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted, ref } from 'vue'

const chartRef = ref<HTMLDivElement>()

onMounted(() => {
  const chart = echarts.init(chartRef.value!)
  chart.setOption({
    // 图表配置
  })
})
</script>
```

## 🎯 最佳实践

1. **API 集成**: 将所有 API 调用放在 `src/api/` 目录
2. **类型定义**: 在 `src/types/` 中定义接口类型
3. **状态管理**: 复杂状态可以使用 Pinia
4. **权限控制**: 可以根据用户角色显示/隐藏菜单
5. **错误处理**: 统一使用 ElMessage 显示错误信息

## 🔄 后续扩展

可以继续添加的功能：
- [ ] 角色权限管理
- [ ] 操作日志
- [ ] 数据导入/导出
- [ ] 图表分析
- [ ] 消息通知系统
- [ ] 文件管理
- [ ] 系统监控

## 📝 注意事项

1. 当前为演示版本，所有数据都是模拟数据
2. 需要连接真实后端 API 才能使用完整功能
3. 登录功能需要后端支持 JWT 或其他认证方式
4. 建议在生产环境中添加更严格的权限控制

