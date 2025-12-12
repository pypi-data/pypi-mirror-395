<template>
  <div class="mysettings-container">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">我的设置</h1>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card class="mb-4">
          <template #header>
            <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">哈吉米信息</span>
          </template>
          <el-form :model="mySettingsForm" label-width="160px">
            <el-form-item label="哈吉米名称">
              <el-input v-model="mySettingsForm.hajimiName" placeholder="请输入哈吉米名称" />
            </el-form-item>
            <el-form-item label="哈吉米年龄">
              <el-input-number v-model="mySettingsForm.hajimiAge" :min="1" :max="100" :step="1" />
            </el-form-item>
            <el-form-item label="哈吉米品种">
              <el-input v-model="mySettingsForm.hajimiBreed" placeholder="请输入哈吉米品种" />
            </el-form-item>
            <el-form-item label="哈吉米颜色">
              <el-input v-model="mySettingsForm.hajimiColor" placeholder="请输入哈吉米颜色" />
            </el-form-item>
            <el-form-item label="哈吉米性别">
              <el-input v-model="mySettingsForm.hajimiGender" placeholder="请输入哈吉米性别" />
            </el-form-item>
            <el-form-item label="哈吉米体重">
              <el-input-number v-model="mySettingsForm.hajimiWeight" :min="1" :max="100" :step="1" />
            </el-form-item>
            <el-form-item label="哈吉米身高">
              <el-input-number v-model="mySettingsForm.hajimiHeight" :min="1" :max="100" :step="1" />
            </el-form-item>
            <el-form-item label="哈吉米健康状况">
              <el-input v-model="mySettingsForm.hajimiHealth" placeholder="请输入哈吉米健康状况" />
            </el-form-item>
            <el-form-item label="哈吉米疫苗接种">
              <el-input v-model="mySettingsForm.hajimiVaccination" placeholder="请输入哈吉米疫苗接种" />
            </el-form-item>
            <el-form-item label="哈吉米疫苗接种日期">
              <el-input v-model="mySettingsForm.hajimiVaccinationDate" placeholder="请输入哈吉米疫苗接种日期" />
            </el-form-item>
            <el-form-item label="哈吉米疫苗接种地点">
              <el-input v-model="mySettingsForm.hajimiVaccinationPlace" placeholder="请输入哈吉米疫苗接种地点" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSavehajimiInfo">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card class="mb-4">
          <template #header>
            <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">哈吉米照片</span>
          </template>
          <div class="flex flex-col items-center space-y-4">
            <el-image
              :src="mySettingsForm.hajimiPhoto"
              :preview-src-list="[mySettingsForm.hajimiPhoto]"
              width="200px"
              height="200px"
              fit="cover"
              class="border rounded"
              :lazy="true"
            >
              <template #error>
                <div class="flex items-center justify-center w-full h-full bg-gray-100 dark:bg-gray-800">
                  <el-icon :size="40" class="text-gray-400">
                    <Picture />
                  </el-icon>
                </div>
              </template>
            </el-image>
            <el-button type="primary" @click="handleUploadPhoto">上传照片</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

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
import { Picture } from '@element-plus/icons-vue'
import { updatehajimiInfo } from '@/api/hajimi'
import type { hajimiParams, hajimiResponse } from '@/types/hajimi'

interface MySettingsForm {
  hajimiName: string
  hajimiAge: number
  hajimiBreed: string
  hajimiColor: string
  hajimiGender: string
  hajimiWeight: number
  hajimiHeight: number
  hajimiHealth: string
  hajimiVaccination: string
  hajimiVaccinationDate: string
  hajimiVaccinationPlace: string
  hajimiPhoto: string
}


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


const mySettingsForm = reactive<MySettingsForm>({
  hajimiName: '旺财',
  hajimiAge: 3,
  hajimiBreed: '金毛',
  hajimiColor: '金色',
  hajimiGender: '公',
  hajimiWeight: 30,
  hajimiHeight: 100,
  hajimiHealth: '健康',
  hajimiVaccination: '是',
  hajimiVaccinationDate: '2025-01-01',
  hajimiVaccinationPlace: '宠物医院',
  hajimiPhoto: 'https://picsum.photos/200/300', // 初始为空，显示占位符
})

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

const handleSavehajimiInfo = async (): Promise<void> => {
  try {
    const params: hajimiParams = {
      id: 1,
      hajimi_name: mySettingsForm.hajimiName,
      hajimi_age: mySettingsForm.hajimiAge,
      hajimi_breed: mySettingsForm.hajimiBreed,
      hajimi_color: mySettingsForm.hajimiColor,
      hajimi_gender: mySettingsForm.hajimiGender,
      hajimi_weight: mySettingsForm.hajimiWeight,
      hajimi_height: mySettingsForm.hajimiHeight,
      hajimi_health: mySettingsForm.hajimiHealth,
      hajimi_vaccination: mySettingsForm.hajimiVaccination,
      hajimi_vaccination_date: mySettingsForm.hajimiVaccinationDate,
      hajimi_vaccination_place: mySettingsForm.hajimiVaccinationPlace,
    }
    const response: hajimiResponse = await updatehajimiInfo(params)
    console.log(response)

    if (response.code === 200) {
      mySettingsForm.hajimiName = response.data.hajimi_name
      mySettingsForm.hajimiAge = response.data.hajimi_age
      mySettingsForm.hajimiBreed = response.data.hajimi_breed
      mySettingsForm.hajimiColor = response.data.hajimi_color
      mySettingsForm.hajimiGender = response.data.hajimi_gender
      mySettingsForm.hajimiWeight = response.data.hajimi_weight
      mySettingsForm.hajimiHeight = response.data.hajimi_height
      mySettingsForm.hajimiHealth = response.data.hajimi_health
      mySettingsForm.hajimiVaccination = response.data.hajimi_vaccination
      mySettingsForm.hajimiVaccinationDate = response.data.hajimi_vaccination_date
      mySettingsForm.hajimiVaccinationPlace = response.data.hajimi_vaccination_place
      ElMessage.success('哈吉米信息已保存')
    } else {
      ElMessage.error('哈吉米信息保存失败' + response.message)
    }
  } catch (error) {
    ElMessage.error((error as Error).message || '哈吉米信息保存失败')
  }
}

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

// 上传照片
const handleUploadPhoto = (): void => {
  // 创建文件输入元素
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]
    if (file) {
      // 验证文件类型
      if (!file.type.startsWith('image/')) {
        ElMessage.error('请选择图片文件')
        return
      }
      
      // 验证文件大小（限制 5MB）
      if (file.size > 5 * 1024 * 1024) {
        ElMessage.error('图片大小不能超过 5MB')
        return
      }

      // 使用 FileReader 读取文件并转换为 base64 或 URL
      const reader = new FileReader()
      reader.onload = (e: ProgressEvent<FileReader>) => {
        const result = e.target?.result as string
        if (result) {
          mySettingsForm.hajimiPhoto = result
          ElMessage.success('照片上传成功')
        }
      }
      reader.onerror = () => {
        ElMessage.error('图片读取失败')
      }
      reader.readAsDataURL(file)
    }
  }
  input.click()
}
</script>

<style scoped>
.mysettings-container {
  padding: 0;
}
</style>

