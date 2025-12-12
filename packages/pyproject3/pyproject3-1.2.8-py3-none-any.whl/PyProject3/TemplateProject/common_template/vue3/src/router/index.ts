import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores'
import Home from '../views/Home.vue'
import Translator from '../views/Translator.vue'
import About from '../views/About.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import AdminLogin from '../views/admin/Login.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import UserManagement from '../views/admin/UserManagement.vue'
import Settings from '../views/admin/Settings.vue'
import MySettings from '../views/admin/MySettings.vue'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Home',
        component: AdminLayout,
        meta: {
            title: '首页',
        },
    },
    {
        path: '/translator',
        name: 'Translator',
        component: Translator,
        meta: {
            title: '翻译工具',
        },
    },
    {
        path: '/about',
        name: 'About',
        component: About,
        meta: {
            title: '关于',
        },
    },
    // 管理后台路由
    {
        path: '/admin/login',
        name: 'AdminLogin',
        component: AdminLogin,
        meta: {
            title: '登录',
            requiresAuth: false,
        },
    },
    {
        path: '/admin',
        component: AdminLayout,
        redirect: '/admin/dashboard',
        meta: {
            requiresAuth: true,
        },
        children: [
            {
                path: 'dashboard',
                name: 'AdminDashboard',
                component: AdminDashboard,
                meta: {
                    title: '仪表盘',
                },
            },
            {
                path: 'users',
                name: 'UserManagement',
                component: UserManagement,
                meta: {
                    title: '用户管理',
                },
            },
            {
                path: 'translations',
                name: 'Translations',
                component: () => import('../views/admin/Translations.vue'),
                meta: {
                    title: '翻译记录',
                },
            },
            {
                path: 'settings',
                name: 'AdminSettings',
                component: Settings,
                meta: {
                    title: '系统设置',
                },
            },
            {
                path: 'my-settings',
                name: 'MySettings',
                component: MySettings,
                meta: {
                    title: '我的设置',
                },
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 路由守卫
router.beforeEach((to, _from, next) => {
    const title = (to.meta.title as string) || '翻译工具'
    document.title = `${title} - 翻译工具`

    const authStore = useAuthStore()

    // 检查是否需要登录
    if (to.meta.requiresAuth) {
        if (!authStore.isAuthenticated) {
            ElMessage.warning('请先登录')
            next('/admin/login')
            return
        }
    }

    // 如果已登录，访问登录页则跳转到仪表盘
    if (to.path === '/admin/login') {
        if (authStore.isAuthenticated) {
            next('/admin/dashboard')
            return
        }
    }

    next()
})

export default router

