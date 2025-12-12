<template>
  <div class="user-management-container">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-200">用户管理</h1>
      <el-button type="primary" :icon="Plus" @click="handleAdd">新增用户</el-button>
    </div>

    <!-- 搜索栏 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="searchForm.email" placeholder="请输入邮箱" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户表格 -->
    <el-card>
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link :icon="Edit" @click="handleEdit(row)">编辑</el-button>
            <el-button
              type="danger"
              link
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
            <el-button
              :type="row.status === 'active' ? 'warning' : 'success'"
              link
              @click="handleToggleStatus(row)"
            >
              {{ row.status === 'active' ? '禁用' : '启用' }}
            </el-button>
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

    <!-- 用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!userForm.id">
          <el-input
            v-model="userForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-else>
          <el-input
            v-model="userForm.password"
            type="password"
            placeholder="留空则不修改密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="userForm.status">
            <el-radio label="active">启用</el-radio>
            <el-radio label="inactive">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { Plus, Search, Refresh, Edit, Delete } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser, deleteUser } from '@/api'
import type { User, UserListParams, CreateUserParams, UpdateUserParams } from '@/types'

interface SearchForm {
  username: string
  email: string
  status: string
}

interface UserForm {
  id?: number
  username: string
  email: string
  password?: string
  role: 'admin' | 'user'
  status: 'active' | 'inactive'
}

const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const userFormRef = ref<FormInstance>()

const searchForm = reactive<SearchForm>({
  username: '',
  email: '',
  status: '',
})

const userForm = reactive<UserForm>({
  username: 'default',
  email: 'jiangbin@163.com',
  role: 'user',
  status: 'active',
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
  password: [
    {
      validator: (_rule, value, callback) => {
        // 新增用户时密码必填，编辑时密码可选
        if (!userForm.id && !value) {
          callback(new Error('请输入密码'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
}

const tableData = ref<User[]>([])

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0,
})

// 获取用户列表
const fetchUserList = async (): Promise<void> => {
  loading.value = true
  try {
    const params: UserListParams = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      username: searchForm.username || undefined,
      email: searchForm.email || undefined,
      status: (searchForm.status as 'active' | 'inactive') || undefined,
    }

    const response = await getUserList(params)
    tableData.value = response.items.map((user) => ({
      ...user,
      createTime: user.created_at
        ? new Date(user.created_at).toLocaleString('zh-CN')
        : '-',
    }))
    pagination.total = response.total
  } catch (error) {
    ElMessage.error((error as Error).message || '获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = (): void => {
  pagination.currentPage = 1 // 重置到第一页
  fetchUserList()
}

// 重置
const handleReset = (): void => {
  searchForm.username = ''
  searchForm.email = ''
  searchForm.status = ''
  pagination.currentPage = 1
  fetchUserList()
}

// 新增
const handleAdd = (): void => {
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: User): void => {
  dialogTitle.value = '编辑用户'
  userForm.id = row.id
  userForm.username = row.username
  userForm.email = row.email
  userForm.role = row.role
  userForm.status = row.status
  userForm.password = '' // 编辑时密码为空，不修改密码
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row: User): Promise<void> => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    loading.value = true
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchUserList() // 刷新列表
  } catch (error) {
    if ((error as Error).message !== 'cancel') {
      ElMessage.error((error as Error).message || '删除用户失败')
    }
  } finally {
    loading.value = false
  }
}

// 切换状态
const handleToggleStatus = async (row: User): Promise<void> => {
  try {
    const newStatus = row.status === 'active' ? 'inactive' : 'active'
    await updateUser(row.id, { status: newStatus })
    row.status = newStatus
    ElMessage.success('状态已更新')
  } catch (error) {
    ElMessage.error((error as Error).message || '更新状态失败')
  }
}

// 提交表单
const handleSubmit = async (): Promise<void> => {
  if (!userFormRef.value) return

  userFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (dialogTitle.value === '新增用户') {
          // 创建用户
          const createParams: CreateUserParams = {
            username: userForm.username,
            email: userForm.email,
            password: userForm.password || '',
            role: userForm.role,
            status: userForm.status,
          }
          await createUser(createParams)
          ElMessage.success('新增成功')
        } else {
          // 更新用户
          const updateParams: UpdateUserParams = {
            username: userForm.username,
            email: userForm.email,
            role: userForm.role,
            status: userForm.status,
          }
          // 如果密码不为空，才更新密码
          if (userForm.password) {
            updateParams.password = userForm.password
          }
          await updateUser(userForm.id!, updateParams)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchUserList() // 刷新列表
      } catch (error) {
        ElMessage.error((error as Error).message || '操作失败')
      } finally {
        loading.value = false
      }
    }
  })
}

// 关闭对话框
const handleDialogClose = (): void => {
  resetForm()
  userFormRef.value?.resetFields()
}

// 重置表单
const resetForm = (): void => {
  userForm.id = undefined
  userForm.username = ''
  userForm.email = ''
  userForm.password = ''
  userForm.role = 'user'
  userForm.status = 'active'
}

// 分页
const handleSizeChange = (val: number): void => {
  pagination.pageSize = val
  pagination.currentPage = 1
  fetchUserList()
}

const handleCurrentChange = (val: number): void => {
  pagination.currentPage = val
  fetchUserList()
}

onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
.user-management-container {
  padding: 0;
}
</style>

