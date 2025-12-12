<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="text-center">
          <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-200">管理后台登录</h2>
        </div>
      </template>
      <el-form
        :model="loginForm"
        :rules="rules"
        ref="loginFormRef"
        label-width="80px"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%" size="large" @click="handleLogin" :loading="loading">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { FormInstance, FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore, useUserStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  username: 'admin',
  password: 'admin123',
  remember: false,
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async (): Promise<void> => {
  if (!loginFormRef.value) return

  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 使用 store 进行登录
        await authStore.userLogin({
          username: loginForm.username,
          password: loginForm.password,
        })

        // 获取用户信息并保存到 user store
        const userInfo = await authStore.fetchUserInfo()
        if (userInfo) {
          userStore.setUserInfo(userInfo)
        }

        router.push('/admin/dashboard')
      } catch (error) {
        // 错误已在 store 中处理
        console.error('Login failed:', error)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 100%;
  max-width: 400px;
}
</style>

