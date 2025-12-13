import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': resolve(__dirname, 'src'),
        },
    },
    server: {
        host: '127.0.0.1', // 或者使用 '0.0.0.0' 来允许外部访问
        port: 3300,
        open: true,
        proxy: {
            '/api': {
                // 开发环境代理目标
                // 修改为你的后端 API 地址
                target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
                secure: false,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                configure: (proxy, options) => {
                    proxy.on('proxyReq', (proxyReq, req, res) => {
                        console.log('代理请求:', {
                            method: req.method,
                            url: req.url,
                            target: options.target,
                        })
                    })
                    proxy.on('proxyRes', (proxyRes, req, res) => {
                        console.log('代理响应:', {
                            status: proxyRes.statusCode,
                            url: req.url,
                        })
                    })
                    proxy.on('error', (err, req, res) => {
                        console.error('代理错误:', err.message)
                    })
                },
            }
        }
    }
})

