import { ref, Ref } from 'vue'
import { translateText } from '../api/translate'
import debounce from 'lodash/debounce'
import { DEFAULT_TARGET_LANG } from '../constants/languages'

/**
 * 翻译功能组合式函数
 */
export function useTranslator() {
    const sourceText: Ref<string> = ref('')
    const translatedText: Ref<string> = ref('')
    const targetLang: Ref<string> = ref(DEFAULT_TARGET_LANG)
    const loading: Ref<boolean> = ref(false)
    const error: Ref<string> = ref('')

    // 防抖处理翻译请求
    const handleInput = debounce(async (): Promise<void> => {
        if (sourceText.value.trim()) {
            await handleTranslate()
        } else {
            translatedText.value = ''
        }
    }, 500)

    // 翻译处理
    const handleTranslate = async (): Promise<void> => {
        if (!sourceText.value.trim()) {
            translatedText.value = ''
            return
        }

        loading.value = true
        error.value = ''

        try {
            const result = await translateText({
                text: sourceText.value,
                target_lang: targetLang.value,
            })
            translatedText.value = result.translatedText
        } catch (err) {
            error.value = (err as Error).message || '翻译失败，请稍后重试'
            translatedText.value = ''
            console.error('翻译错误:', err)
        } finally {
            loading.value = false
        }
    }

    // 清空内容
    const clearAll = (): void => {
        sourceText.value = ''
        translatedText.value = ''
        error.value = ''
    }

    // 复制翻译结果
    const copyResult = async (): Promise<boolean> => {
        if (translatedText.value) {
            try {
                await navigator.clipboard.writeText(translatedText.value)
                return true
            } catch (err) {
                console.error('复制失败:', err)
                return false
            }
        }
        return false
    }

    return {
        sourceText,
        translatedText,
        targetLang,
        loading,
        error,
        handleInput,
        handleTranslate,
        clearAll,
        copyResult,
    }
}

