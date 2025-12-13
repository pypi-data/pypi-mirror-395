import type { Language } from '@/types'

/**
 * 支持的语言列表
 */
export const LANGUAGES: Language[] = [
    { code: 'EN-US', name: '英语', flag: '🇬🇧' },
    { code: 'JA', name: '日语', flag: '🇯🇵' },
    { code: 'KO', name: '韩语', flag: '🇰🇷' },
    { code: 'FR', name: '法语', flag: '🇫🇷' },
    { code: 'DE', name: '德语', flag: '🇩🇪' },
    { code: 'ES', name: '西班牙语', flag: '🇪🇸' },
    { code: 'IT', name: '意大利语', flag: '🇮🇹' },
    { code: 'PT', name: '葡萄牙语', flag: '🇵🇹' },
    { code: 'RU', name: '俄语', flag: '🇷🇺' },
    { code: 'ZH', name: '中文', flag: '🇨🇳' },
]

export const DEFAULT_TARGET_LANG = 'EN-US'

