import request from './request'
import { API_ENDPOINTS } from './config'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'
/**
 * 登录参数
 */
export interface LoginParams {
    username: string
    password: string
    remember?: boolean
}

/**
 * 登录响应
 */
export interface LoginResponse {
    token: string
    user: {
        id: number
        username: string
        email: string
        role: string
    }
}

/**
 * 用户信息
 */
export interface UserInfo {
    id: number
    username: string
    email: string
    role: 'admin' | 'user'
    status: 'active' | 'inactive'
    created_at?: string
}

/**
 * 用户登录
 * @param params - 登录参数
 * @returns 登录响应（包含 token 和用户信息）
 */
export const login = async (params: LoginParams): Promise<LoginResponse> => {
    try {
        const response = await request<LoginResponse>({
            url: API_ENDPOINTS.login,
            method: 'POST',
            data: {
                username: params.username,
                password: params.password,
            },
        })

        return response
    } catch (error) {
        console.error('Login Error:', error)
        throw new Error((error as Error).message || '登录失败，请检查用户名和密码')
    }
}

/**
 * 用户登出
 * @returns 登出结果
 */
export const logout = async (): Promise<void> => {
    try {
        await request({
            url: API_ENDPOINTS.logout,
            method: 'POST',
        })
    } catch (error) {
        console.error('Logout Error:', error)
        // 即使登出失败，也清除本地 token
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }
}

/**
 * 获取当前用户信息
 * @returns 用户信息
 */
export const getUserInfo = async (): Promise<UserInfo> => {
    try {
        const response = await request<UserInfo>({
            url: API_ENDPOINTS.getUserInfo,
            data: {
                username: useUserStore().username,
                token: useAuthStore().token,
            },
            method: 'POST',
        })

        return response
    } catch (error) {
        console.error('Get User Info Error:', error)
        throw new Error((error as Error).message || '获取用户信息失败')
    }
}

