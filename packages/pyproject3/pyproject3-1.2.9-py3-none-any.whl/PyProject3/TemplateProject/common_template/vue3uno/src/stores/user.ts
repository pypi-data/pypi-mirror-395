import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/api/auth'

/**
 * 用户信息状态管理 Store
 */
export const useUserStore = defineStore('user', () => {
    // 状态 - 从 localStorage 初始化
    const getInitialUserInfo = (): UserInfo | null => {
        const savedUser = localStorage.getItem('user')
        if (savedUser) {
            try {
                return JSON.parse(savedUser)
            } catch {
                return null
            }
        }
        return null
    }

    const userInfo = ref<UserInfo | null>(getInitialUserInfo())

    // 计算属性
    const username = computed(() => userInfo.value?.username || '')
    const email = computed(() => userInfo.value?.email || '')
    const role = computed(() => userInfo.value?.role || 'user')
    const isAdmin = computed(() => userInfo.value?.role === 'admin')
    const userId = computed(() => userInfo.value?.id || 0)

    // 设置用户信息
    const setUserInfo = (info: UserInfo | null): void => {
        userInfo.value = info
        if (info) {
            localStorage.setItem('user', JSON.stringify(info))
        } else {
            localStorage.removeItem('user')
        }
    }

    // 更新用户信息（部分更新）
    const updateUserInfo = (updates: Partial<UserInfo>): void => {
        if (userInfo.value) {
            userInfo.value = { ...userInfo.value, ...updates }
            localStorage.setItem('user', JSON.stringify(userInfo.value))
        }
    }

    // 清除用户信息
    const clearUserInfo = (): void => {
        userInfo.value = null
        localStorage.removeItem('user')
    }

    // 从 localStorage 同步
    const syncFromStorage = (): void => {
        const savedUser = localStorage.getItem('user')
        if (savedUser) {
            try {
                userInfo.value = JSON.parse(savedUser)
            } catch {
                userInfo.value = null
            }
        } else {
            userInfo.value = null
        }
    }

    return {
        // 状态
        userInfo,

        // 计算属性
        username,
        email,
        role,
        isAdmin,
        userId,

        // 方法
        setUserInfo,
        updateUserInfo,
        clearUserInfo,
        syncFromStorage,
    }
})

