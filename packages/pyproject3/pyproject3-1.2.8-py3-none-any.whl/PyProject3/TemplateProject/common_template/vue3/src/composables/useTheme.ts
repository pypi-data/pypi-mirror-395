import { ref, watch, onMounted } from 'vue'
import type { Theme } from '@/types'

const THEME_KEY = 'app-theme'
const isDark = ref<boolean>(false)

// 应用主题
function applyTheme(dark: boolean): void {
    const html = document.documentElement
    if (dark) {
        html.classList.add('dark')
        html.setAttribute('data-theme', 'dark')
    } else {
        html.classList.remove('dark')
        html.setAttribute('data-theme', 'light')
    }
}

// 初始化主题
function initTheme(): void {
    const savedTheme = localStorage.getItem(THEME_KEY)
    if (savedTheme) {
        isDark.value = savedTheme === 'dark'
    } else {
        // 检测系统偏好
        isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyTheme(isDark.value)
}

// 切换主题
function toggleTheme(): void {
    isDark.value = !isDark.value
    localStorage.setItem(THEME_KEY, isDark.value ? 'dark' : 'light')
    applyTheme(isDark.value)
}

// 设置主题
function setTheme(theme: Theme): void {
    isDark.value = theme === 'dark'
    localStorage.setItem(THEME_KEY, theme)
    applyTheme(isDark.value)
}

// 监听系统主题变化
function watchSystemTheme(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e: MediaQueryListEvent) => {
        if (!localStorage.getItem(THEME_KEY)) {
            isDark.value = e.matches
            applyTheme(isDark.value)
        }
    })
}

export function useTheme() {
    onMounted(() => {
        initTheme()
        watchSystemTheme()
    })

    watch(isDark, (newVal: boolean) => {
        applyTheme(newVal)
    })

    return {
        isDark,
        toggleTheme,
        setTheme,
    }
}

// 在模块加载时立即初始化（用于 main.js）
if (typeof window !== 'undefined') {
    initTheme()
}

