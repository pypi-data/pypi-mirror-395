import request from './request'
import type { hajimiParams, hajimiResponse } from '@/types/hajimi'


export const gethajimiInfo = async (params: hajimiParams): Promise<hajimiResponse> => {
    const response = await request<hajimiResponse>({
        url: '/hajimi/info',
        method: 'GET',
        params,
    })
    return response
}

export const updatehajimiInfo = async (params: hajimiParams): Promise<hajimiResponse> => {
    const response = await request<hajimiResponse>({
        url: '/hajimi/info',
        method: 'POST',
        data: params,
    })
    return response
}