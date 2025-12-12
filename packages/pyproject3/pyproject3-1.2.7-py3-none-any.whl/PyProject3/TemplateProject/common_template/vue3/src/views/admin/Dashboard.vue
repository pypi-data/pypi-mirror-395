<template>
  <div class="dashboard-container">
    <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">仪表盘</h1>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb-6">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="flex items-center">
            <div class="stat-icon bg-blue-100 dark:bg-blue-900 p-3 rounded-lg mr-4">
              <el-icon class="text-blue-600 dark:text-blue-400 text-2xl"><User /></el-icon>
            </div>
            <div>
              <div class="stat-value text-2xl font-bold text-gray-800 dark:text-gray-200">1,234</div>
              <div class="stat-label text-gray-500 dark:text-gray-400">总用户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="flex items-center">
            <div class="stat-icon bg-green-100 dark:bg-green-900 p-3 rounded-lg mr-4">
              <el-icon class="text-green-600 dark:text-green-400 text-2xl"><Document /></el-icon>
            </div>
            <div>
              <div class="stat-value text-2xl font-bold text-gray-800 dark:text-gray-200">5,678</div>
              <div class="stat-label text-gray-500 dark:text-gray-400">翻译记录</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="flex items-center">
            <div class="stat-icon bg-yellow-100 dark:bg-yellow-900 p-3 rounded-lg mr-4">
              <el-icon class="text-yellow-600 dark:text-yellow-400 text-2xl"><TrendCharts /></el-icon>
            </div>
            <div>
              <div class="stat-value text-2xl font-bold text-gray-800 dark:text-gray-200">89.2%</div>
              <div class="stat-label text-gray-500 dark:text-gray-400">成功率</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="flex items-center">
            <div class="stat-icon bg-purple-100 dark:bg-purple-900 p-3 rounded-lg mr-4">
              <el-icon class="text-purple-600 dark:text-purple-400 text-2xl"><Timer /></el-icon>
            </div>
            <div>
              <div class="stat-value text-2xl font-bold text-gray-800 dark:text-gray-200">12.5s</div>
              <div class="stat-label text-gray-500 dark:text-gray-400">平均响应时间</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">翻译趋势</span>
            </div>
          </template>
          <div class="chart-placeholder h-64 flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded">
            <span class="text-gray-500 dark:text-gray-400">图表区域（可集成 ECharts）</span>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">语言分布</span>
            </div>
          </template>
          <div class="chart-placeholder h-64 flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded">
            <span class="text-gray-500 dark:text-gray-400">图表区域（可集成 ECharts）</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-row :gutter="20" class="mt-6">
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">最近翻译</span>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in recentTranslations"
              :key="index"
              :timestamp="item.time"
              placement="top"
            >
              <el-card>
                <p class="text-gray-700 dark:text-gray-300">{{ item.text }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  {{ item.source }} → {{ item.target }}
                </p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-lg font-semibold text-gray-800 dark:text-gray-200">系统通知</span>
            </div>
          </template>
          <el-scrollbar height="400px">
            <div
              v-for="(notice, index) in notices"
              :key="index"
              class="notice-item p-4 border-b border-gray-200 dark:border-gray-700 last:border-0"
            >
              <div class="flex items-start">
                <el-icon class="mr-2 mt-1" :class="notice.type === 'success' ? 'text-green-500' : 'text-blue-500'">
                  <CircleCheck v-if="notice.type === 'success'" />
                  <InfoFilled v-else />
                </el-icon>
                <div class="flex-1">
                  <p class="text-gray-800 dark:text-gray-200 font-medium">{{ notice.title }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ notice.content }}</p>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-2">{{ notice.time }}</p>
                </div>
              </div>
            </div>
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { User, Document, TrendCharts, Timer, CircleCheck, InfoFilled } from '@element-plus/icons-vue'

interface Translation {
  text: string
  source: string
  target: string
  time: string
}

interface Notice {
  title: string
  content: string
  time: string
  type: 'success' | 'info'
}

const recentTranslations = ref<Translation[]>([
  {
    text: 'Hello, how are you?',
    source: '英语',
    target: '中文',
    time: '2024-01-15 10:30',
  },
  {
    text: 'こんにちは',
    source: '日语',
    target: '中文',
    time: '2024-01-15 09:15',
  },
  {
    text: 'Bonjour',
    source: '法语',
    target: '英语',
    time: '2024-01-15 08:45',
  },
])

const notices = ref<Notice[]>([
  {
    title: '系统更新完成',
    content: '系统已成功更新到最新版本，新增了多项功能优化。',
    time: '2024-01-15 10:00',
    type: 'success',
  },
  {
    title: '翻译服务优化',
    content: '翻译服务响应速度已优化，平均响应时间减少 20%。',
    time: '2024-01-14 15:30',
    type: 'info',
  },
  {
    title: '新功能上线',
    content: '批量翻译功能已上线，支持同时翻译多条文本。',
    time: '2024-01-13 09:00',
    type: 'success',
  },
])
</script>

<style scoped>
.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.chart-placeholder {
  min-height: 256px;
}
</style>

