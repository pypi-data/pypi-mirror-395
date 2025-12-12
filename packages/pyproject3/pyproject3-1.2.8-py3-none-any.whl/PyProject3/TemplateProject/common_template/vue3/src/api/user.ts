import request from './request'
import { API_ENDPOINTS } from './config'
import type { User, UserListParams, UserListResponse, CreateUserParams, UpdateUserParams } from '@/types'

/**
 * 获取用户列表
 * @param params - 查询参数
 * @returns 用户列表
 */
export const getUserList = async (params?: UserListParams): Promise<UserListResponse> => {
    try {
        const response = await request<UserListResponse>({
            url: API_ENDPOINTS.userList,
            method: 'GET',
            params: {
                page: params?.page || 1,
                page_size: params?.page_size || 10,
                username: params?.username,
                email: params?.email,
                status: params?.status,
            },
        })

        return response
    } catch (error) {
        console.error('Get User List Error:', error)
        throw new Error((error as Error).message || '获取用户列表失败')
    }
}

/**
 * 获取用户详情
 * @param id - 用户 ID
 * @returns 用户信息
 */
export const getUserById = async (id: number): Promise<User> => {
    try {
        const response = await request<User>({
            url: `${API_ENDPOINTS.userList}/${id}`,
            method: 'GET',
        })

        return response
    } catch (error) {
        console.error('Get User Error:', error)
        throw new Error((error as Error).message || '获取用户信息失败')
    }
}

/**
 * 创建用户
 * @param params - 用户信息
 * @returns 创建的用户信息
 */
export const createUser = async (params: CreateUserParams): Promise<User> => {
    try {
        const response = await request<User>({
            url: API_ENDPOINTS.userList,
            method: 'POST',
            data: params,
        })

        return response
    } catch (error) {
        console.error('Create User Error:', error)
        throw new Error((error as Error).message || '创建用户失败')
    }
}

/**
 * 更新用户
 * @param id - 用户 ID
 * @param params - 更新的用户信息
 * @returns 更新后的用户信息
 */
export const updateUser = async (id: number, params: UpdateUserParams): Promise<User> => {
    try {
        const response = await request<User>({
            url: `${API_ENDPOINTS.userList}/${id}`,
            method: 'PUT',
            data: params,
        })

        return response
    } catch (error) {
        console.error('Update User Error:', error)
        throw new Error((error as Error).message || '更新用户失败')
    }
}

/**
 * 删除用户
 * @param id - 用户 ID
 * @returns 删除结果
 */
export const deleteUser = async (id: number): Promise<void> => {
    try {
        await request({
            url: `${API_ENDPOINTS.userList}/${id}`,
            method: 'DELETE',
        })
    } catch (error) {
        console.error('Delete User Error:', error)
        throw new Error((error as Error).message || '删除用户失败')
    }
}

/**
 * 批量删除用户
 * @param ids - 用户 ID 数组
 * @returns 删除结果
 */
export const deleteUsers = async (ids: number[]): Promise<void> => {
    try {
        await request({
            url: `${API_ENDPOINTS.userList}/batch`,
            method: 'DELETE',
            data: { ids },
        })
    } catch (error) {
        console.error('Batch Delete Users Error:', error)
        throw new Error((error as Error).message || '批量删除用户失败')
    }
}

