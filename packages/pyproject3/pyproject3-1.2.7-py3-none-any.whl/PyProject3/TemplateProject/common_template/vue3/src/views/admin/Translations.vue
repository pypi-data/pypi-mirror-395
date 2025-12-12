<template>
  <div class="translations-container">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-200">翻译记录</h1>
      <el-button type="primary" :icon="Download" @click="handleExport">导出数据</el-button>
    </div>

    <!-- 筛选栏 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="filterForm" class="demo-form-inline">
        <el-form-item label="源语言">
          <el-select v-model="filterForm.sourceLang" placeholder="请选择源语言" clearable>
            <el-option label="全部" value="" />
            <el-option label="中文" value="ZH" />
            <el-option label="英语" value="EN-US" />
            <el-option label="日语" value="JA" />
            <el-option label="韩语" value="KO" />
          </el-select>
        </el-form-item>
        <el-form-item label="目标语言">
          <el-select v-model="filterForm.targetLang" placeholder="请选择目标语言" clearable>
            <el-option label="全部" value="" />
            <el-option label="中文" value="ZH" />
            <el-option label="英语" value="EN-US" />
            <el-option label="日语" value="JA" />
            <el-option label="韩语" value="KO" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 翻译记录表格 -->
    <el-card>
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="sourceText" label="原文" min-width="200" show-overflow-tooltip />
        <el-table-column prop="translatedText" label="译文" min-width="200" show-overflow-tooltip />
        <el-table-column prop="sourceLang" label="源语言" width="100" />
        <el-table-column prop="targetLang" label="目标语言" width="100" />
        <el-table-column prop="user" label="用户" width="120" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link :icon="View" @click="handleView(row)">查看</el-button>
            <el-button type="danger" link :icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="mt-4 flex justify-end">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="翻译详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ currentRecord?.id }}</el-descriptions-item>
        <el-descriptions-item label="原文">
          <div class="max-h-32 overflow-y-auto">{{ currentRecord?.sourceText }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="译文">
          <div class="max-h-32 overflow-y-auto">{{ currentRecord?.translatedText }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="源语言">{{ currentRecord?.sourceLang }}</el-descriptions-item>
        <el-descriptions-item label="目标语言">{{ currentRecord?.targetLang }}</el-descriptions-item>
        <el-descriptions-item label="用户">{{ currentRecord?.user }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRecord?.createTime }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Download, View, Delete } from '@element-plus/icons-vue'

interface Translation {
  id: number
  sourceText: string
  translatedText: string
  sourceLang: string
  targetLang: string
  user: string
  createTime: string
}

interface FilterForm {
  sourceLang: string
  targetLang: string
  dateRange: string[]
}

const loading = ref(false)
const detailVisible = ref(false)
const currentRecord = ref<Translation | null>(null)

const filterForm = reactive<FilterForm>({
  sourceLang: '',
  targetLang: '',
  dateRange: [],
})

const tableData = ref<Translation[]>([
  {
    id: 1,
    sourceText: 'Hello, how are you?',
    translatedText: '你好，你好吗？',
    sourceLang: 'EN-US',
    targetLang: 'ZH',
    user: 'user1',
    createTime: '2024-01-15 10:30:00',
  },
  {
    id: 2,
    sourceText: 'こんにちは',
    translatedText: '你好',
    sourceLang: 'JA',
    targetLang: 'ZH',
    user: 'user2',
    createTime: '2024-01-15 09:15:00',
  },
  {
    id: 3,
    sourceText: 'Bonjour',
    translatedText: 'Hello',
    sourceLang: 'FR',
    targetLang: 'EN-US',
    user: 'user1',
    createTime: '2024-01-14 15:20:00',
  },
])

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0,
})

const handleSearch = (): void => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('搜索完成')
  }, 500)
}

const handleReset = (): void => {
  filterForm.sourceLang = ''
  filterForm.targetLang = ''
  filterForm.dateRange = []
  handleSearch()
}

const handleView = (row: Translation): void => {
  currentRecord.value = row
  detailVisible.value = true
}

const handleDelete = (row: Translation): void => {
  ElMessageBox.confirm('确定要删除这条翻译记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      const index = tableData.value.findIndex((item) => item.id === row.id)
      if (index > -1) {
        tableData.value.splice(index, 1)
        ElMessage.success('删除成功')
      }
    })
    .catch(() => {})
}

const handleExport = (): void => {
  ElMessage.success('导出功能开发中...')
}

const handleSizeChange = (val: number): void => {
  pagination.pageSize = val
  handleSearch()
}

const handleCurrentChange = (val: number): void => {
  pagination.currentPage = val
  handleSearch()
}

onMounted(() => {
  pagination.total = tableData.value.length
})
</script>

<style scoped>
.translations-container {
  padding: 0;
}
</style>

