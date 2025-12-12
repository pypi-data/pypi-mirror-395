/**
 * 全局类型定义
 */

// API 响应基础类型
export interface ApiResponse<T = any> {
    code?: number
    message?: string
    data?: T
    [key: string]: any
}

// 翻译相关类型
export interface TranslateParams {
    text: string
    target_lang: string
    source_lang?: string
}

export interface TranslateResponse {
    translatedText: string
}

export interface BatchTranslateParams {
    texts: string[]
    target_lang: string
}

// 语言类型
export interface Language {
    code: string
    name: string
    flag: string
}

// 主题类型
export type Theme = 'light' | 'dark'

// 用户相关类型
export interface User {
    id: number
    username: string
    email: string
    role: 'admin' | 'user'
    status: 'active' | 'inactive'
    created_at?: string
    updated_at?: string
}

export interface UserListParams {
    page?: number
    page_size?: number
    username?: string
    email?: string
    status?: 'active' | 'inactive'
}

export interface UserListResponse {
    items: User[]
    total: number
    page: number
    page_size: number
}

export interface CreateUserParams {
    username: string
    email: string
    password: string
    role?: 'admin' | 'user'
    status?: 'active' | 'inactive'
}

export interface UpdateUserParams {
    username?: string
    email?: string
    password?: string
    role?: 'admin' | 'user'
    status?: 'active' | 'inactive'
}

