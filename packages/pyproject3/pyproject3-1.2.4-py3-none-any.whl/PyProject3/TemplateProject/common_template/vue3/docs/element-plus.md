# Element Plus 速查表

> Element Plus 是基于 Vue 3 的组件库，提供丰富的 UI 组件和工具。

## 目录

- [基础概念](#基础概念)
- [布局组件](#布局组件)
- [表单组件](#表单组件)
- [数据展示](#数据展示)
- [反馈组件](#反馈组件)
- [导航组件](#导航组件)
- [其他组件](#其他组件)
- [工具方法](#工具方法)
- [重要概念](#重要概念)

---

## 基础概念

### 安装和引入

```typescript
// main.ts
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css' // 深色模式

app.use(ElementPlus)
```

### 按需引入（推荐）

```typescript
import { ElButton, ElInput } from 'element-plus'
```

### 图标使用

```vue
<template>
  <el-icon><User /></el-icon>
</template>

<script setup>
import { User } from '@element-plus/icons-vue'
</script>
```

---

## 布局组件

### Container 布局容器

```vue
<el-container>
  <el-header>Header</el-header>
  <el-aside width="200px">Aside</el-aside>
  <el-main>Main</el-main>
  <el-footer>Footer</el-footer>
</el-container>
```

**常用属性：**
- `direction`: `horizontal` | `vertical` - 排列方向

### Row & Col 栅格系统

```vue
<el-row :gutter="20">
  <el-col :span="12" :xs="24" :sm="12" :md="8" :lg="6">
    <!-- 内容 -->
  </el-col>
</el-row>
```

**常用属性：**
- `gutter`: 栅格间隔
- `span`: 占据的列数（1-24）
- `xs/sm/md/lg/xl`: 响应式断点

### Card 卡片

```vue
<el-card>
  <template #header>
    <div>标题</div>
  </template>
  <div>内容</div>
</el-card>
```

**常用属性：**
- `shadow`: `always` | `hover` | `never` - 阴影显示时机
- `body-style`: 自定义 body 样式

---

## 表单组件

### Form 表单

```vue
<el-form
  :model="form"
  :rules="rules"
  ref="formRef"
  label-width="100px"
  @submit.prevent="handleSubmit"
>
  <el-form-item label="用户名" prop="username">
    <el-input v-model="form.username" />
  </el-form-item>
</el-form>
```

**常用属性：**
- `model`: 表单数据对象
- `rules`: 验证规则
- `label-width`: 标签宽度
- `label-position`: `left` | `right` | `top`

**常用方法：**
- `validate()`: 验证整个表单
- `validateField()`: 验证指定字段
- `resetFields()`: 重置表单

### Input 输入框

```vue
<el-input
  v-model="input"
  placeholder="请输入"
  clearable
  show-password
  :prefix-icon="User"
  :suffix-icon="Search"
  size="large"
/>
```

**常用属性：**
- `type`: `text` | `textarea` | `password` 等
- `clearable`: 是否显示清除按钮
- `show-password`: 密码显示/隐藏切换
- `prefix-icon` / `suffix-icon`: 图标
- `size`: `large` | `default` | `small`

### InputNumber 数字输入框

```vue
<el-input-number
  v-model="num"
  :min="1"
  :max="100"
  :step="1"
  :precision="2"
/>
```

### Select 选择器

```vue
<el-select v-model="value" placeholder="请选择" clearable>
  <el-option label="选项1" value="1" />
  <el-option label="选项2" value="2" />
</el-select>
```

**常用属性：**
- `multiple`: 多选
- `filterable`: 可搜索
- `clearable`: 可清空

### Switch 开关

```vue
<el-switch v-model="value" />
```

### Checkbox 复选框

```vue
<el-checkbox v-model="checked">选项</el-checkbox>
<el-checkbox-group v-model="checkList">
  <el-checkbox label="选项1" />
  <el-checkbox label="选项2" />
</el-checkbox-group>
```

### Radio 单选框

```vue
<el-radio v-model="radio" label="1">选项1</el-radio>
<el-radio-group v-model="radio">
  <el-radio label="1">选项1</el-radio>
  <el-radio label="2">选项2</el-radio>
</el-radio-group>
```

### DatePicker 日期选择器

```vue
<el-date-picker
  v-model="date"
  type="date"
  placeholder="选择日期"
  format="YYYY-MM-DD"
  value-format="YYYY-MM-DD"
/>
```

**常用类型：**
- `date`: 日期
- `datetime`: 日期时间
- `daterange`: 日期范围
- `month`: 月份

---

## 数据展示

### Table 表格

```vue
<el-table :data="tableData" stripe border v-loading="loading">
  <el-table-column type="selection" width="55" />
  <el-table-column type="index" label="序号" width="80" />
  <el-table-column prop="name" label="姓名" />
  <el-table-column prop="age" label="年龄" width="100" />
  <el-table-column label="操作" fixed="right" width="200">
    <template #default="{ row }">
      <el-button @click="handleEdit(row)">编辑</el-button>
    </template>
  </el-table-column>
</el-table>
```

**常用属性：**
- `stripe`: 斑马纹
- `border`: 边框
- `v-loading`: 加载状态
- `height`: 固定高度
- `max-height`: 最大高度

**常用列属性：**
- `type`: `selection` | `index` | `expand`
- `fixed`: `left` | `right` - 固定列
- `sortable`: 可排序
- `formatter`: 格式化函数

### Pagination 分页

```vue
<el-pagination
  v-model:current-page="currentPage"
  v-model:page-size="pageSize"
  :page-sizes="[10, 20, 50, 100]"
  :total="total"
  layout="total, sizes, prev, pager, next, jumper"
  @size-change="handleSizeChange"
  @current-change="handleCurrentChange"
/>
```

### Tag 标签

```vue
<el-tag>标签</el-tag>
<el-tag type="success" closable>可关闭</el-tag>
```

**类型：** `success` | `info` | `warning` | `danger`

### Descriptions 描述列表

```vue
<el-descriptions :column="2" border>
  <el-descriptions-item label="用户名">admin</el-descriptions-item>
  <el-descriptions-item label="邮箱">admin@example.com</el-descriptions-item>
</el-descriptions>
```

### Timeline 时间线

```vue
<el-timeline>
  <el-timeline-item timestamp="2024-01-01" placement="top">
    <el-card>内容</el-card>
  </el-timeline-item>
</el-timeline>
```

### Image 图片

```vue
<el-image
  src="url"
  fit="cover"
  :preview-src-list="[url]"
  lazy
/>
```

---

## 反馈组件

### Button 按钮

```vue
<el-button type="primary" :icon="Search" :loading="loading" @click="handleClick">
  按钮
</el-button>
```

**类型：** `primary` | `success` | `warning` | `danger` | `info` | `text`

**常用属性：**
- `size`: `large` | `default` | `small`
- `plain`: 朴素按钮
- `round`: 圆角按钮
- `circle`: 圆形按钮
- `link`: 链接按钮
- `loading`: 加载状态
- `disabled`: 禁用

### Message 消息提示

```typescript
import { ElMessage } from 'element-plus'

ElMessage.success('成功消息')
ElMessage.warning('警告消息')
ElMessage.error('错误消息')
ElMessage.info('信息消息')
```

**配置：**
```typescript
ElMessage({
  message: '消息内容',
  type: 'success',
  duration: 3000,
  showClose: true,
})
```

### Notification 通知

```typescript
import { ElNotification } from 'element-plus'

ElNotification({
  title: '标题',
  message: '消息内容',
  type: 'success',
  duration: 3000,
  position: 'top-right',
})
```

### MessageBox 消息框

```typescript
import { ElMessageBox } from 'element-plus'

// 确认框
ElMessageBox.confirm('确定删除吗？', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning',
}).then(() => {
  // 确定
}).catch(() => {
  // 取消
})

// 提示框
ElMessageBox.alert('提示内容', '标题', {
  confirmButtonText: '确定',
})

// 输入框
ElMessageBox.prompt('请输入', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
}).then(({ value }) => {
  console.log(value)
})
```

### Dialog 对话框

```vue
<el-dialog
  v-model="visible"
  title="标题"
  width="500px"
  :close-on-click-modal="false"
  @close="handleClose"
>
  <div>内容</div>
  <template #footer>
    <el-button @click="visible = false">取消</el-button>
    <el-button type="primary" @click="handleConfirm">确定</el-button>
  </template>
</el-dialog>
```

**常用属性：**
- `width`: 宽度
- `fullscreen`: 全屏
- `close-on-click-modal`: 点击遮罩关闭
- `close-on-press-escape`: 按 ESC 关闭
- `draggable`: 可拖拽

### Loading 加载

```vue
<!-- 指令方式 -->
<div v-loading="loading">内容</div>

<!-- 服务方式 -->
<script setup>
import { ElLoading } from 'element-plus'

const loading = ElLoading.service({
  lock: true,
  text: '加载中...',
  background: 'rgba(0, 0, 0, 0.7)',
})
loading.close()
</script>
```

### Progress 进度条

```vue
<el-progress :percentage="50" />
<el-progress :percentage="100" :status="'success'" />
```

**状态：** `success` | `exception` | `warning`

### Alert 警告

```vue
<el-alert
  title="成功提示"
  type="success"
  :closable="true"
  show-icon
/>
```

**类型：** `success` | `warning` | `info` | `error`

---

## 导航组件

### Menu 菜单

```vue
<el-menu
  :default-active="activeIndex"
  :collapse="isCollapse"
  router
  background-color="#304156"
  text-color="#bfcbd9"
  active-text-color="#409EFF"
>
  <el-menu-item index="/dashboard">
    <el-icon><Odometer /></el-icon>
    <template #title>仪表盘</template>
  </el-menu-item>
  <el-sub-menu index="1">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>设置</span>
    </template>
    <el-menu-item index="1-1">选项1</el-menu-item>
  </el-sub-menu>
</el-menu>
```

**常用属性：**
- `router`: 启用路由模式
- `collapse`: 折叠状态
- `default-active`: 默认激活项

### Breadcrumb 面包屑

```vue
<el-breadcrumb separator="/">
  <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
  <el-breadcrumb-item>当前页</el-breadcrumb-item>
</el-breadcrumb>
```

### Tabs 标签页

```vue
<el-tabs v-model="activeName" @tab-click="handleClick">
  <el-tab-pane label="用户管理" name="first">内容1</el-tab-pane>
  <el-tab-pane label="配置管理" name="second">内容2</el-tab-pane>
</el-tabs>
```

### Dropdown 下拉菜单

```vue
<el-dropdown @command="handleCommand">
  <span>
    下拉菜单
    <el-icon><ArrowDown /></el-icon>
  </span>
  <template #dropdown>
    <el-dropdown-menu>
      <el-dropdown-item command="a">选项1</el-dropdown-item>
      <el-dropdown-item command="b" divided>选项2</el-dropdown-item>
    </el-dropdown-menu>
  </template>
</el-dropdown>
```

### Steps 步骤条

```vue
<el-steps :active="active" finish-status="success">
  <el-step title="步骤1" />
  <el-step title="步骤2" />
  <el-step title="步骤3" />
</el-steps>
```

---

## 其他组件

### Avatar 头像

```vue
<el-avatar :size="50" :src="url">
  <el-icon><User /></el-icon>
</el-avatar>
```

### Badge 徽标

```vue
<el-badge :value="12" class="item">
  <el-button>消息</el-button>
</el-badge>
```

### Divider 分割线

```vue
<el-divider />
<el-divider content-position="left">文字</el-divider>
```

### Empty 空状态

```vue
<el-empty description="暂无数据" />
```

### Scrollbar 滚动条

```vue
<el-scrollbar height="400px">
  <div>内容</div>
</el-scrollbar>
```

### Space 间距

```vue
<el-space :size="20" wrap>
  <el-button>按钮1</el-button>
  <el-button>按钮2</el-button>
</el-space>
```

### Tooltip 文字提示

```vue
<el-tooltip content="提示文字" placement="top">
  <el-button>悬停显示</el-button>
</el-tooltip>
```

### Popover 弹出框

```vue
<el-popover
  placement="top"
  :width="200"
  trigger="hover"
  content="这是一段内容"
>
  <template #reference>
    <el-button>悬停显示</el-button>
  </template>
</el-popover>
```

### Popconfirm 气泡确认框

```vue
<el-popconfirm
  title="确定删除吗？"
  @confirm="handleConfirm"
>
  <template #reference>
    <el-button>删除</el-button>
  </template>
</el-popconfirm>
```

---

## 工具方法

### 表单验证规则

```typescript
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9]{6,}$/, message: '密码至少6位', trigger: 'blur' },
  ],
}
```

### 自定义验证器

```typescript
const validatePassword = (rule: any, value: string, callback: Function) => {
  if (value.length < 6) {
    callback(new Error('密码长度不能少于6位'))
  } else {
    callback()
  }
}
```

---

## 重要概念

### 1. 响应式设计

Element Plus 支持响应式断点：
- `xs`: < 768px
- `sm`: ≥ 768px
- `md`: ≥ 992px
- `lg`: ≥ 1200px
- `xl`: ≥ 1920px

### 2. 深色模式

```typescript
// 引入深色模式样式
import 'element-plus/theme-chalk/dark/css-vars.css'

// 通过 CSS 变量控制
:root {
  --el-color-primary: #409eff;
}
```

### 3. 国际化 (i18n)

```typescript
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

app.use(ElementPlus, {
  locale: zhCn,
})
```

### 4. 主题定制

通过 CSS 变量或 SCSS 变量定制主题：

```css
:root {
  --el-color-primary: #409eff;
  --el-color-success: #67c23a;
  --el-color-warning: #e6a23c;
  --el-color-danger: #f56c6c;
  --el-color-info: #909399;
}
```

### 5. 插槽 (Slots)

常用插槽：
- `#header`: 卡片头部
- `#footer`: 对话框底部
- `#default`: 默认内容
- `#title`: 标题
- `#reference`: 引用元素（Popover/Tooltip）

### 6. 事件处理

```vue
<!-- 组件事件 -->
<el-button @click="handleClick">按钮</el-button>

<!-- 表单验证 -->
<el-form @submit.prevent="handleSubmit">
  <!-- 表单内容 -->
</el-form>

<!-- 表格事件 -->
<el-table @selection-change="handleSelectionChange">
  <!-- 表格列 -->
</el-table>
```

### 7. 指令

- `v-loading`: 加载指令
- `v-infinite-scroll`: 无限滚动
- `v-click-outside`: 点击外部（需安装）

### 8. 组件引用

```vue
<script setup>
import { ref } from 'vue'
import type { FormInstance } from 'element-plus'

const formRef = ref<FormInstance>()

const validateForm = () => {
  formRef.value?.validate((valid) => {
    if (valid) {
      // 验证通过
    }
  })
}
</script>

<template>
  <el-form ref="formRef">
    <!-- 表单内容 -->
  </el-form>
</template>
```

### 9. 类型定义

```typescript
import type {
  FormInstance,
  FormRules,
  TableInstance,
  UploadInstance,
} from 'element-plus'
```

### 10. 最佳实践

1. **按需引入**：减少打包体积
2. **使用 TypeScript**：获得类型提示
3. **表单验证**：使用 rules 统一管理
4. **响应式设计**：合理使用栅格系统
5. **深色模式**：考虑用户体验
6. **加载状态**：提供用户反馈
7. **错误处理**：使用 Message/Notification 提示

---

## 常用组合模式

### 搜索表单 + 表格 + 分页

```vue
<template>
  <el-card>
    <el-form :inline="true" :model="searchForm">
      <el-form-item label="关键词">
        <el-input v-model="searchForm.keyword" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </el-form-item>
    </el-form>
  </el-card>

  <el-card>
    <el-table :data="tableData" v-loading="loading">
      <!-- 表格列 -->
    </el-table>
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      @current-change="handlePageChange"
    />
  </el-card>
</template>
```

### 表单对话框

```vue
<el-dialog v-model="dialogVisible" title="编辑">
  <el-form :model="form" :rules="rules" ref="formRef">
    <!-- 表单字段 -->
  </el-form>
  <template #footer>
    <el-button @click="dialogVisible = false">取消</el-button>
    <el-button type="primary" @click="handleSubmit">确定</el-button>
  </template>
</el-dialog>
```

---

## 参考资源

- [Element Plus 官方文档](https://element-plus.org/zh-CN/)
- [Element Plus GitHub](https://github.com/element-plus/element-plus)
- [Element Plus Icons](https://element-plus.org/zh-CN/component/icon.html)

---

**最后更新：** 2024-01-15

