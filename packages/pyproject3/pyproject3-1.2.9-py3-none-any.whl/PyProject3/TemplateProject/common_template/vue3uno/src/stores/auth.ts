import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, logout, getUserInfo } from '@/api'
import type { LoginParams, LoginResponse, UserInfo } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { useUserStore } from './user'

/**
 * 认证状态管理 Store
 */
export const useAuthStore = defineStore('auth', () => {
    // 状态
    const token = ref<string | null>(localStorage.getItem('token'))
    const isAuthenticated = computed(() => !!token.value)

    // 从 localStorage 初始化
    const initAuth = (): void => {
        const savedToken = localStorage.getItem('token')
        if (savedToken) {
            token.value = savedToken
        }
    }

    // 登录
    const userLogin = async (params: LoginParams): Promise<void> => {
        try {
            const response: LoginResponse = await login(params)

            // 保存 token 和用户信息
            token.value = response.token
            localStorage.setItem('token', response.token)

            // 转换登录响应的 user 为 UserInfo 格式
            const userInfo: UserInfo = {
                id: response.user.id,
                username: response.user.username,
                email: response.user.email,
                role: response.user.role as 'admin' | 'user',
                status: 'active', // 默认状态
            }

            localStorage.setItem('user', JSON.stringify(userInfo))

            // 同步更新 userStore
            const userStore = useUserStore()
            userStore.setUserInfo(userInfo)

            ElMessage.success('登录成功')
        } catch (error) {
            ElMessage.error((error as Error).message || '登录失败')
            throw error
        }
    }

    // 登出
    const userLogout = async (): Promise<void> => {
        try {
            await logout()
        } catch (error) {
            console.error('Logout error:', error)
        } finally {
            // 清除状态
            token.value = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')

            // 清除 userStore
            const userStore = useUserStore()
            userStore.clearUserInfo()

            ElMessage.success('已登出')
        }
    }

    // 获取当前用户信息
    const fetchUserInfo = async (): Promise<UserInfo | null> => {
        if (!token.value) {
            return null
        }

        try {
            const userInfo = await getUserInfo()
            localStorage.setItem('user', JSON.stringify(userInfo))

            // 同步更新 userStore
            const userStore = useUserStore()
            userStore.setUserInfo(userInfo)

            return userInfo
        } catch (error) {
            console.error('Get user info error:', error)
            // 如果获取用户信息失败，清除 token
            token.value = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')

            // 清除 userStore
            const userStore = useUserStore()
            userStore.clearUserInfo()

            return null
        }
    }

    // 设置 token（用于外部设置，如从 localStorage 恢复）
    const setToken = (newToken: string | null): void => {
        token.value = newToken
        if (newToken) {
            localStorage.setItem('token', newToken)
        } else {
            localStorage.removeItem('token')
        }
    }

    // 清除认证信息
    const clearAuth = (): void => {
        token.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }

    // 初始化
    initAuth()

    return {
        // 状态
        token,
        isAuthenticated,

        // 方法
        userLogin,
        userLogout,
        fetchUserInfo,
        setToken,
        clearAuth,
        initAuth,
    }
})

