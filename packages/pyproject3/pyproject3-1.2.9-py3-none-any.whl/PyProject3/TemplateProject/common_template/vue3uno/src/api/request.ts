import axios, { AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '@/types'

// 创建 axios 实例
const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 30000, // 30秒超时
    headers: {
        'Content-Type': 'application/json',
    },
})

// 请求拦截器
request.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // 可以在这里添加 token 等认证信息
        const token = localStorage.getItem('token')
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`
        }

        // 添加时间戳防止缓存
        if (config.method === 'get') {
            config.params = {
                ...config.params,
                _t: Date.now(),
            }
        }

        console.log('请求发送:', {
            url: config.url,
            method: config.method,
            params: config.params,
            data: config.data,
        })

        return config
    },
    (error) => {
        console.error('请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
request.interceptors.response.use(
    (response: AxiosResponse<ApiResponse | any>) => {
        const { data } = response

        // 如果后端返回的数据格式是 { code, data, message }
        if (typeof data === 'object' && data !== null && 'code' in data) {
            const apiResponse = data as ApiResponse
            // 根据你的后端 API 规范调整
            if (apiResponse.code === 200 || apiResponse.code === 0) {
                return apiResponse
            } else {
                ElMessage.error(apiResponse.message || '请求失败')
                return Promise.reject(new Error(apiResponse.message || '请求失败'))
            }
        }

        // 直接返回数据
        return data
    },
    (error) => {
        console.error('响应错误:', error)

        let message = '请求失败，请稍后重试'

        if (error.response) {
            // 服务器返回了错误状态码
            const { status, data } = error.response

            switch (status) {
                case 400:
                    message = (data as any)?.message || '请求参数错误'
                    break
                case 401:
                    message = '未授权，请重新登录'
                    // 可以在这里清除 token 并跳转到登录页
                    localStorage.removeItem('token')
                    // router.push('/login')
                    break
                case 403:
                    message = '拒绝访问'
                    break
                case 404:
                    message = '请求的资源不存在'
                    break
                case 500:
                    message = '服务器内部错误'
                    break
                case 502:
                    message = '网关错误'
                    break
                case 503:
                    message = '服务不可用'
                    break
                case 504:
                    message = '网关超时'
                    break
                default:
                    message = (data as any)?.message || `请求失败 (${status})`
            }
        } else if (error.request) {
            // 请求已发出，但没有收到响应
            message = '网络错误，请检查网络连接'
        } else {
            // 其他错误
            message = error.message || '请求配置错误'
        }

        ElMessage.error(message)
        return Promise.reject(error)
    }
)

export default request

