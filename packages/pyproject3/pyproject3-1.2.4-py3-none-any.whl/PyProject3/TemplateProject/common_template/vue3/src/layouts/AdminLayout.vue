<template>
  <el-container class="admin-layout h-screen">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="transition-all duration-300">
      <div class="logo-container flex items-center justify-center h-16 bg-gray-800 dark:bg-gray-900">
        <span v-if="!isCollapse" class="text-white text-lg font-bold">CMS管理后台</span>
        <span v-else class="text-white text-xl">⚡</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        class="border-r-0"

      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>
        <el-sub-menu index="users">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/admin/users">用户列表</el-menu-item>
          <el-menu-item index="/admin/users?id=1">添加用户</el-menu-item>
          <el-menu-item index="/admin/users?id=2">角色管理</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/admin/translations">
          <el-icon><Document /></el-icon>
          <template #title>翻译记录</template>
        </el-menu-item>
        <el-menu-item index="/admin/settings">
          <el-icon><Setting /></el-icon>
          <template #title>系统设置</template>
        </el-menu-item>
        <el-menu-item index="/admin/my-settings">
          <el-icon><Timer /></el-icon>
          <template #title>我的设置</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header-container flex items-center justify-between bg-white dark:bg-gray-800 shadow-sm">
        <div class="flex items-center">
          <el-button
            :icon="isCollapse ? Expand : Fold"
            circle
            @click="toggleCollapse"
            class="mr-4"
          />
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">管理后台</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="flex items-center space-x-4">
          <!-- 主题切换 -->
          <el-button circle @click="toggleTheme" class="mr-2">
            <el-icon>
              <Sunny v-if="isDark" />
              <Moon v-else />
            </el-icon>
          </el-button>
          <!-- 用户信息 -->
          <el-dropdown @command="handleCommand">
            <span class="flex items-center cursor-pointer">
              <el-avatar :size="32" class="mr-2">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="text-gray-700 dark:text-gray-200">{{ userStore.username || '管理员' }}</span>
              <el-icon class="ml-1"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="settings">设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 标签页 -->
      <div :class="['tabs-container', isDark ? 'tabs-dark' : 'tabs-light']">
        <el-tabs
          v-model="activeTab"
          type="card"
          closable
          @tab-remove="handleTabRemove"
          @tab-click="handleTabClick"
          class="tabs-wrapper"
        >
          <el-tab-pane
            v-for="tab in tabs"
            :key="tab.path"
            :label="tab.title"
            :name="tab.path"
            :closable="tab.closable"
          >
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 内容区域 -->
      <el-main class="main-content bg-gray-50 dark:bg-gray-900">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore, useUserStore, useAuthStore } from '@/stores'
import {
  Odometer,
  User,
  Document,
  Setting,
  Fold,
  Expand,
  Sunny,
  Moon,
  ArrowDown,
  Timer,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()
const userStore = useUserStore()
const authStore = useAuthStore()

const isDark = computed(() => themeStore.isDark)
const toggleTheme = () => themeStore.toggleTheme()

const isCollapse = ref(false)

// 标签页管理
interface TabItem {
  path: string
  title: string
  closable: boolean
}

const tabs = ref<TabItem[]>([])
const activeTab = ref<string>('')

// 页面标题映射
const titleMap: Record<string, string> = {
  '/admin/dashboard': '仪表盘',
  '/admin/users': '用户列表',
  '/admin/users?id=1': '添加用户',
  '/admin/users?id=2': '角色管理',
  '/admin/translations': '翻译记录',
  '/admin/settings': '系统设置',
  '/admin/my-settings': '我的设置',
}

// 获取页面标题
const getPageTitle = (path: string): string => {
  // 处理带查询参数的路径
  const basePath = path.split('?')[0]
  const query = path.includes('?') ? path.split('?')[1] : ''
  
  if (query) {
    const fullPath = path
    return titleMap[fullPath] || titleMap[basePath] || '未知页面'
  }
  
  return titleMap[path] || route.meta.title as string || '未知页面'
}

// 添加标签页
const addTab = (path: string) => {
  // 检查标签页是否已存在
  const existingTab = tabs.value.find(tab => tab.path === path)
  if (existingTab) {
    activeTab.value = path
    return
  }

  // 添加新标签页
  const title = getPageTitle(path)
  const isDashboard = path === '/admin/dashboard'
  tabs.value.push({
    path,
    title,
    closable: !isDashboard && tabs.value.length > 0, // 仪表盘不可关闭
  })
  activeTab.value = path
}

// 监听路由变化
watch(
  () => route.fullPath,
  (newPath) => {
    if (newPath.startsWith('/admin') && newPath !== '/admin/login') {
      addTab(newPath)
    }
  },
  { immediate: true }
)

// 关闭标签页
const handleTabRemove = (targetName: string) => {
  // 仪表盘标签页不可关闭
  if (targetName === '/admin/dashboard') {
    return
  }

  const targetIndex = tabs.value.findIndex(tab => tab.path === targetName)
  if (targetIndex === -1) return

  tabs.value.splice(targetIndex, 1)

  // 如果关闭的是当前激活的标签页，切换到相邻的标签页
  if (activeTab.value === targetName) {
    if (tabs.value.length > 0) {
      const newIndex = targetIndex >= tabs.value.length ? tabs.value.length - 1 : targetIndex
      const newTab = tabs.value[newIndex]
      activeTab.value = newTab.path
      router.push(newTab.path)
    } else {
      // 如果没有标签页了，跳转到仪表盘
      router.push('/admin/dashboard')
    }
  }
}

// 点击标签页切换
const handleTabClick = (tab: any) => {
  const targetPath = tab.paneName
  if (targetPath && targetPath !== route.fullPath) {
    router.push(targetPath)
  }
}

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 当前页面标题
const currentPageTitle = computed(() => {
  return getPageTitle(route.fullPath)
})

// 切换侧边栏折叠
const toggleCollapse = (): void => {
  isCollapse.value = !isCollapse.value
}

// 处理下拉菜单命令
const handleCommand = async (command: string): Promise<void> => {
  switch (command) {
    case 'profile':
      // 个人中心功能开发中...
      break
    case 'settings':
      router.push('/admin/settings')
      break
    case 'logout':
      await handleLogout()
      break
  }
}

// 退出登录
const handleLogout = async (): Promise<void> => {
  await authStore.userLogout()
  userStore.clearUserInfo()
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-layout {
  overflow: hidden;
}

.logo-container {
  transition: all 0.3s;
}

.header-container {
  border-bottom: 1px solid #e4e7ed;
}

.tabs-container {
  padding: 4px 10px;
  min-height: 40px;
  height: auto;
  overflow: visible;
  border-bottom: 1px solid #e4e7ed;
  flex-shrink: 0;
}

.tabs-container.tabs-light {
  background-color: #fff;
  border-bottom-color: #e4e7ed;
}

.tabs-container.tabs-dark {
  background-color: #1f2937;
  border-bottom-color: #374151;
}

.tabs-wrapper {
  height: 100%;
}

:deep(.el-tabs__header) {
  margin: 0;
  border: none;
}

:deep(.el-tabs__nav) {
  border: none;
  display: flex;
  flex-wrap: wrap;
}

:deep(.el-tabs__nav-wrap) {
  overflow: visible;
}

:deep(.el-tabs__nav-scroll) {
  overflow: visible;
}

/* 浅色模式 */
.tabs-light :deep(.el-tabs__item) {
  height: 32px;
  line-height: 32px;
  padding: 0 15px;
  margin-right: 8px;
  margin-bottom: 4px;
  border: 1px solid #dcdfe6;
  border-radius: 4px 4px 0 0;
  background-color: #f5f7fa;
  color: #606266;
  flex-shrink: 0;
}

.tabs-light :deep(.el-tabs__item.is-active) {
  background-color: #fff;
  color: #409eff;
  border-bottom-color: #fff;
}

.tabs-light :deep(.el-tabs__item:hover) {
  color: #409eff;
}

/* 深色模式 */
.tabs-dark :deep(.el-tabs__item) {
  height: 32px;
  line-height: 32px;
  padding: 0 15px;
  margin-right: 8px;
  margin-bottom: 4px;
  border: 1px solid #374151;
  border-radius: 4px 4px 0 0;
  background-color: #1f2937;
  color: #d1d5db;
  flex-shrink: 0;
}

.tabs-dark :deep(.el-tabs__item.is-active) {
  background-color: #111827;
  color: #409eff;
  border-bottom-color: #111827;
}

.tabs-dark :deep(.el-tabs__item:hover) {
  color: #409eff;
}

/* 通用样式 */
:deep(.el-tabs__item .is-closable) {
  padding-right: 20px;
}

:deep(.el-tabs__item .el-icon-close) {
  width: 14px;
  height: 14px;
  font-size: 14px;
  margin-left: 4px;
}

.tabs-light :deep(.el-tabs__item .el-icon-close:hover) {
  background-color: #c0c4cc;
  border-radius: 50%;
  color: #fff;
}

.tabs-dark :deep(.el-tabs__item .el-icon-close:hover) {
  background-color: #4b5563;
  border-radius: 50%;
  color: #fff;
}

:deep(.el-tabs__content) {
  display: none;
}

.main-content {
  padding: 20px;
  overflow-y: auto;
}

/* 深色模式下的菜单样式 */
:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}

:deep(.el-menu-item:hover) {
  background-color: #263445 !important;
}

:deep(.el-menu-item.is-active) {
  background-color: #1890ff !important;
  color: #fff !important;
}
</style>

