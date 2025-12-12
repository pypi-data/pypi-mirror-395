import request from './request'
import { API_ENDPOINTS } from './config'
import type { TranslateParams, TranslateResponse, BatchTranslateParams } from '@/types'

/**
 * 翻译文本
 * @param params - 翻译参数
 * @returns 翻译结果
 */
export const translateText = async (params: TranslateParams): Promise<TranslateResponse> => {
    try {
        const response = await request<TranslateResponse | { translatedText: string } | { result: string } | { translation: string }>({
            url: API_ENDPOINTS.translate,
            method: 'POST',
            data: {
                text: params.text,
                target_lang: params.target_lang,
                source_lang: params.source_lang, // 可选
            },
        })

        // 根据后端返回的数据结构调整
        // 如果后端直接返回 translatedText
        if (typeof response === 'object' && response !== null) {
            if ('translatedText' in response) {
                return {
                    translatedText: response.translatedText,
                }
            }
            // 如果后端返回格式不同，在这里转换
            // 例如：{ result: '...' } 或 { translation: '...' }
            if ('result' in response) {
                return {
                    translatedText: response.result,
                }
            }
            if ('translation' in response) {
                return {
                    translatedText: response.translation,
                }
            }
        }

        // 如果返回的是字符串
        if (typeof response === 'string') {
            return {
                translatedText: response,
            }
        }

        return {
            translatedText: '',
        }
    } catch (error) {
        console.error('Translation Error:', error)
        throw new Error((error as Error).message || '翻译服务出错，请稍后重试')
    }
}

/**
 * 批量翻译
 * @param params - 批量翻译参数
 * @returns 翻译结果数组
 */
export const translateBatch = async (params: BatchTranslateParams): Promise<TranslateResponse[]> => {
    try {
        const response = await request<TranslateResponse[]>({
            url: `${API_ENDPOINTS.translate}/batch`,
            method: 'POST',
            data: {
                texts: params.texts,
                target_lang: params.target_lang,
            },
        })

        return response
    } catch (error) {
        console.error('Batch Translation Error:', error)
        throw new Error((error as Error).message || '批量翻译失败，请稍后重试')
    }
}

