/**
 * API 配置
 */

// API 基础配置
export const API_CONFIG = {
    // 开发环境
    development: {
        baseURL: '/api', // 使用 Vite 代理
        timeout: 30000,
    },
    // 生产环境
    production: {
        baseURL: import.meta.env.VITE_API_BASE_URL || 'https://your-api-domain.com/api',
        timeout: 30000,
    },
} as const

// 获取当前环境配置
export const getApiConfig = () => {
    const env = import.meta.env.MODE || 'development'
    return API_CONFIG[env as keyof typeof API_CONFIG] || API_CONFIG.development
}

// API 端点配置
export const API_ENDPOINTS = {
    // 翻译相关
    translate: '/translate',

    // 用户相关
    userList: '/users',
    userDetail: '/users/:id',
    login: '/auth/login',
    logout: '/auth/logout',
    getUserInfo: '/auth/me',

    // 其他业务 API...
    // article: '/articles',
    // category: '/categories',
    // ...
} as const

// 请求状态码
export const HTTP_STATUS = {
    OK: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    INTERNAL_SERVER_ERROR: 500,
} as const

