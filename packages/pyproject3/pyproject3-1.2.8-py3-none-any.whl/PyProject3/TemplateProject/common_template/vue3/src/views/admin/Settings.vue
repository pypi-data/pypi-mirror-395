<template>
  <div class="settings-container">
    <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">系统设置</h1>

    </div>
    <el-row :gutter="20">
      <el-col :xs="24" :md="16">
        <el-card class="mb-4">
          <template #header>
            <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">基本设置</span>
          </template>
          <el-form :model="settingsForm" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="settingsForm.systemName" placeholder="请输入系统名称" />
            </el-form-item>
            <el-form-item label="系统描述">
              <el-input
                v-model="settingsForm.systemDesc"
                type="textarea"
                :rows="3"
                placeholder="请输入系统描述"
              />
            </el-form-item>
            <el-form-item label="API 地址">
              <el-input v-model="settingsForm.apiUrl" placeholder="请输入 API 地址" />
            </el-form-item>
            <el-form-item label="超时时间">
              <el-input-number v-model="settingsForm.timeout" :min="1000" :max="60000" :step="1000" />
              <span class="ml-2 text-gray-500 dark:text-gray-400">毫秒</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave">保存设置</el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="mb-4">
          <template #header>
            <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">功能开关</span>
          </template>
          <el-form :model="settingsForm" label-width="120px">
            <el-form-item label="启用注册">
              <el-switch v-model="settingsForm.enableRegister" />
            </el-form-item>
            <el-form-item label="启用邮件通知">
              <el-switch v-model="settingsForm.enableEmail" />
            </el-form-item>
            <el-form-item label="启用短信通知">
              <el-switch v-model="settingsForm.enableSms" />
            </el-form-item>
            <el-form-item label="维护模式">
              <el-switch v-model="settingsForm.maintenanceMode" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="8">
        <el-card class="mb-4">
          <template #header>
            <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">系统信息</span>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统版本">v1.0.0</el-descriptions-item>
            <el-descriptions-item label="Vue 版本">3.3.4</el-descriptions-item>
            <el-descriptions-item label="Node 版本">18.0.0</el-descriptions-item>
            <el-descriptions-item label="运行时间">15 天</el-descriptions-item>
            <el-descriptions-item label="服务器">Linux</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card>
          <template #header>
            <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">快捷操作</span>
          </template>
          <div class="space-y-2">
            <el-button type="primary" style="width: 100%" @click="handleClearCache">清除缓存</el-button>
            <el-button type="warning" style="width: 100%" @click="handleRestart">重启服务</el-button>
            <el-button type="danger" style="width: 100%" @click="handleBackup">备份数据</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

interface SettingsForm {
  systemName: string
  systemDesc: string
  apiUrl: string
  timeout: number
  enableRegister: boolean
  enableEmail: boolean
  enableSms: boolean
  maintenanceMode: boolean
}

const settingsForm = reactive<SettingsForm>({
  systemName: '翻译管理系统',
  systemDesc: '一个功能强大的翻译管理系统',
  apiUrl: 'http://localhost:8000/api',
  timeout: 30000,
  enableRegister: true,
  enableEmail: true,
  enableSms: false,
  maintenanceMode: false,
})

const handleSave = (): void => {
  ElMessage.success('设置已保存')
}

const handleReset = (): void => {
  ElMessageBox.confirm('确定要重置所有设置吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      Object.assign(settingsForm, {
        systemName: '翻译管理系统',
        systemDesc: '一个功能强大的翻译管理系统',
        apiUrl: 'http://localhost:8000/api',
        timeout: 30000,
        enableRegister: true,
        enableEmail: true,
        enableSms: false,
        maintenanceMode: false,
      })
      ElMessage.success('设置已重置')
    })
    .catch(() => {})
}

const handleClearCache = (): void => {
  ElMessageBox.confirm('确定要清除缓存吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      ElMessage.success('缓存已清除')
    })
    .catch(() => {})
}

const handleRestart = (): void => {
  ElMessageBox.confirm('确定要重启服务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      ElMessage.success('服务已重启')
    })
    .catch(() => {})
}

const handleBackup = (): void => {
  ElMessage.success('备份任务已启动')
}
</script>

<style scoped>
.settings-container {
  padding: 0;
}
</style>

