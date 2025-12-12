import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { Theme } from '@/types'

const THEME_KEY = 'app-theme'

/**
 * 主题状态管理 Store
 */
export const useThemeStore = defineStore('theme', () => {
    // 状态 - 从 localStorage 或系统偏好初始化
    const getInitialTheme = (): boolean => {
        const savedTheme = localStorage.getItem(THEME_KEY)
        if (savedTheme) {
            return savedTheme === 'dark'
        }
        // 检测系统偏好
        if (typeof window !== 'undefined') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches
        }
        return false
    }

    const isDark = ref<boolean>(getInitialTheme())

    // 计算属性
    const theme = computed<Theme>(() => (isDark.value ? 'dark' : 'light'))

    // 应用主题到 DOM
    const applyTheme = (dark: boolean): void => {
        const html = document.documentElement
        if (dark) {
            html.classList.add('dark')
            html.setAttribute('data-theme', 'dark')
        } else {
            html.classList.remove('dark')
            html.setAttribute('data-theme', 'light')
        }
    }

    // 切换主题
    const toggleTheme = (): void => {
        isDark.value = !isDark.value
        localStorage.setItem(THEME_KEY, isDark.value ? 'dark' : 'light')
        applyTheme(isDark.value)
    }

    // 设置主题
    const setTheme = (newTheme: Theme): void => {
        isDark.value = newTheme === 'dark'
        localStorage.setItem(THEME_KEY, newTheme)
        applyTheme(isDark.value)
    }

    // 监听系统主题变化
    const watchSystemTheme = (): void => {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        mediaQuery.addEventListener('change', (e: MediaQueryListEvent) => {
            // 只有在用户没有手动设置主题时才跟随系统
            if (!localStorage.getItem(THEME_KEY)) {
                isDark.value = e.matches
                applyTheme(isDark.value)
            }
        })
    }

    // 初始化主题
    const initTheme = (): void => {
        applyTheme(isDark.value)
        watchSystemTheme()
    }

    // 监听主题变化并应用到 DOM
    watch(isDark, (newVal) => {
        applyTheme(newVal)
    }, { immediate: true })

    // 初始化
    if (typeof window !== 'undefined') {
        initTheme()
    }

    return {
        // 状态
        isDark,
        theme,

        // 方法
        toggleTheme,
        setTheme,
        initTheme,
    }
})

