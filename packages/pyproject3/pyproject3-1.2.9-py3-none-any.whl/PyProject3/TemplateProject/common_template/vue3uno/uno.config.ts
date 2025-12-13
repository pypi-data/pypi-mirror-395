import { defineConfig, presetUno, presetAttributify, presetIcons } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(), // 默认预设，提供 Tailwind CSS 兼容的工具类
    presetAttributify(), // 属性化模式，支持 <div bg="blue-500"> 这样的写法
    presetIcons(), // 图标预设，支持使用图标
  ],
  // 安全列表：确保动态生成的类名被识别
  safelist: [
    // Flexbox 方向
    'flex-row', 'flex-column', 'flex-row-reverse', 'flex-column-reverse',
    // Justify content
    'justify-start', 'justify-center', 'justify-end', 'justify-between', 'justify-around', 'justify-evenly',
    // Align items
    'items-start', 'items-center', 'items-end', 'items-stretch', 'items-baseline',
    // Gap
    ...Array.from({ length: 33 }, (_, i) => `gap-${i}`),
    // 颜色背景
    'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-pink-500', 'bg-red-500', 'bg-yellow-500', 'bg-indigo-500', 'bg-gray-500',
    // 文字颜色
    'text-white', 'text-black', 'text-gray-600', 'text-blue-600',
  ],
  // 自定义规则
  rules: [],
  // 快捷方式
  shortcuts: {
    'btn': 'px-4 py-2 rounded bg-blue-500 text-white hover:bg-blue-600',
    'btn-primary': 'px-4 py-2 rounded bg-blue-500 text-white hover:bg-blue-600',
    'btn-secondary': 'px-4 py-2 rounded bg-gray-500 text-white hover:bg-gray-600',
  },
  // 主题配置
  theme: {
    colors: {
      // 可以在这里扩展颜色
    },
  },
})

