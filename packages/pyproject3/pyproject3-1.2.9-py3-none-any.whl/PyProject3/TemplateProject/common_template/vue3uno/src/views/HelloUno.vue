<template>
  <div class="min-h-screen bg-black text-white">
    <!-- 导航栏 -->
    <nav class="sticky top-0 z-50 bg-black/80 backdrop-blur-md border-b border-white/10">
      <div class="max-w-7xl mx-auto px-6 h-12 flex items-center justify-between">
        <div class="flex items-center gap-8">
          <div class="text-xl font-semibold">

        <a class="i-carbon-logo-github"></a>
          </div>
          <router-link to="/" class="text-sm hover:text-gray-400 transition-colors">首页</router-link>
          <router-link to="/css/layout" class="text-sm hover:text-gray-400 transition-colors">布局学习</router-link>
          <router-link to="/css/components" class="text-sm hover:text-gray-400 transition-colors">组件学习</router-link>
          <router-link to="/css/playground" class="text-sm hover:text-gray-400 transition-colors">交互学习</router-link>
          <router-link to="/css/node" class="text-sm hover:text-gray-400 transition-colors">Node学习</router-link>
          <router-link to="/node-editor" class="text-sm hover:text-gray-400 transition-colors">Node编辑器</router-link>
        
        </div>
        <div class="text-sm">🔍</div>
      </div>
    </nav>

    <!-- 主横幅 - iPhone 15 Pro -->
    <section class="relative h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 via-black to-black overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-pink-500/20 blur-3xl"></div>
      <div class="relative z-10 text-center px-6">
        <h1 class="text-6xl md:text-8xl font-bold mb-4 tracking-tight">iPhone 15 Pro</h1>
        <p class="text-2xl md:text-3xl text-gray-400 mb-6">钛金属，如此强大</p>
        <div class="flex gap-4 justify-center">
          <a href="#" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-full text-sm font-medium transition-colors">
            了解更多
          </a>
          <a href="#" class="px-6 py-2 border border-white/30 hover:bg-white/10 rounded-full text-sm font-medium transition-colors">
            购买
          </a>
        </div>
      </div>
    </section>

    <!-- iPhone 15 -->
    <section class="relative h-screen flex items-center justify-center bg-gradient-to-b from-pink-100 via-blue-100 to-purple-100 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-pink-200/50 via-blue-200/50 to-purple-200/50"></div>
      <div class="relative z-10 text-center px-6">
        <h2 class="text-6xl md:text-8xl font-bold mb-4 tracking-tight text-black">iPhone 15</h2>
        <p class="text-2xl md:text-3xl text-gray-700 mb-6">全新设计，全新色彩</p>
        <div class="flex gap-4 justify-center">
          <a href="#" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-full text-sm font-medium text-white transition-colors">
            了解更多
          </a>
          <a href="#" class="px-6 py-2 border border-gray-800 hover:bg-gray-800/10 rounded-full text-sm font-medium text-gray-800 transition-colors">
            购买
          </a>
        </div>
      </div>
    </section>

    <!-- 双栏布局 - Apple Watch & AirPods -->
    <section class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      <!-- Apple Watch -->
      <div class="relative h-[600px] bg-gradient-to-br from-red-900 via-red-800 to-black rounded-2xl overflow-hidden flex items-center justify-center">
        <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
        <div class="relative z-10 text-center px-6">
          <h3 class="text-5xl md:text-6xl font-bold mb-3">Apple Watch</h3>
          <p class="text-xl text-gray-300 mb-4">Series 9</p>
          <p class="text-lg text-gray-400 mb-6">更强大，更智能</p>
          <div class="flex gap-4 justify-center">
            <a href="#" class="px-6 py-2 bg-white text-black hover:bg-gray-200 rounded-full text-sm font-medium transition-colors">
              了解更多
            </a>
            <a href="#" class="px-6 py-2 border border-white/30 hover:bg-white/10 rounded-full text-sm font-medium transition-colors">
              购买
            </a>
          </div>
        </div>
      </div>

      <!-- AirPods Pro -->
      <div class="relative h-[600px] bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl overflow-hidden flex items-center justify-center">
        <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
        <div class="relative z-10 text-center px-6">
          <h3 class="text-5xl md:text-6xl font-bold mb-3">AirPods Pro</h3>
          <p class="text-xl text-gray-200 mb-4">第二代</p>
          <p class="text-lg text-gray-300 mb-6">自适应音频，全新体验</p>
          <div class="flex gap-4 justify-center">
            <a href="#" class="px-6 py-2 bg-white text-black hover:bg-gray-200 rounded-full text-sm font-medium transition-colors">
              了解更多
            </a>
            <a href="#" class="px-6 py-2 border border-white/30 hover:bg-white/10 rounded-full text-sm font-medium transition-colors">
              购买
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- MacBook Pro -->
    <section class="relative h-screen flex items-center justify-center bg-gradient-to-b from-gray-800 via-gray-900 to-black overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600/30 via-purple-600/30 to-pink-600/30 blur-3xl"></div>
      <div class="relative z-10 text-center px-6">
        <h2 class="text-6xl md:text-8xl font-bold mb-4 tracking-tight">MacBook Pro</h2>
        <p class="text-2xl md:text-3xl text-gray-400 mb-6">M3 芯片，性能飞跃</p>
        <div class="flex gap-4 justify-center">
          <a href="#" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-full text-sm font-medium transition-colors">
            了解更多
          </a>
          <a href="#" class="px-6 py-2 border border-white/30 hover:bg-white/10 rounded-full text-sm font-medium transition-colors">
            购买
          </a>
        </div>
      </div>
    </section>

    <!-- iPad -->
    <section class="relative h-screen flex items-center justify-center bg-gradient-to-b from-yellow-100 via-orange-100 to-pink-100 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-yellow-200/50 via-orange-200/50 to-pink-200/50"></div>
      <div class="relative z-10 text-center px-6">
        <h2 class="text-6xl md:text-8xl font-bold mb-4 tracking-tight text-black">iPad</h2>
        <p class="text-2xl md:text-3xl text-gray-700 mb-6">强大到超乎想象</p>
        <div class="flex gap-4 justify-center">
          <a href="#" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-full text-sm font-medium text-white transition-colors">
            了解更多
          </a>
          <a href="#" class="px-6 py-2 border border-gray-800 hover:bg-gray-800/10 rounded-full text-sm font-medium text-gray-800 transition-colors">
            购买
          </a>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="bg-black border-t border-white/10 py-12">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 class="text-sm font-semibold mb-4 text-gray-400">选购及了解</h4>
            <ul class="space-y-2 text-sm text-gray-500">
              <li><a href="#" class="hover:text-white transition-colors">商店</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Mac</a></li>
              <li><a href="#" class="hover:text-white transition-colors">iPad</a></li>
              <li><a href="#" class="hover:text-white transition-colors">iPhone</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-semibold mb-4 text-gray-400">服务</h4>
            <ul class="space-y-2 text-sm text-gray-500">
              <li><a href="#" class="hover:text-white transition-colors">Apple Music</a></li>
              <li><a href="#" class="hover:text-white transition-colors">iCloud</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Apple Pay</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-semibold mb-4 text-gray-400">账户</h4>
            <ul class="space-y-2 text-sm text-gray-500">
              <li><a href="#" class="hover:text-white transition-colors">管理你的 Apple ID</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Apple Store 账户</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-semibold mb-4 text-gray-400">关于 Apple</h4>
            <ul class="space-y-2 text-sm text-gray-500">
              <li><a href="#" class="hover:text-white transition-colors">新闻中心</a></li>
              <li><a href="#" class="hover:text-white transition-colors">工作机会</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-white/10 pt-8 text-sm text-gray-500 text-center">
          <p>Copyright © 2024 Apple Inc. 保留所有权利。</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 这是一个展示 UnoCSS 的组件
</script>
