<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-gray-800">CSS 组件学习 - 常见 UI 组件</h1>

      <!-- 1. 按钮 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">1. 按钮样式</h2>
        
        <div class="flex flex-wrap gap-4 mb-4">
          <button class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
            主要按钮
          </button>
          <button class="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors">
            次要按钮
          </button>
          <button class="px-6 py-2 border-2 border-blue-500 text-blue-500 rounded hover:bg-blue-50 transition-colors">
            边框按钮
          </button>
          <button class="px-6 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors">
            圆角按钮
          </button>
        </div>
        <code class="block p-2 bg-gray-800 text-green-400 rounded text-sm">
          class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        </code>
      </section>

      <!-- 2. 输入框 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">2. 输入框样式</h2>
        
        <div class="space-y-4 max-w-md">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">基础输入框</label>
            <input 
              type="text" 
              placeholder="请输入内容"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">带图标的输入框</label>
            <div class="relative">
              <input 
                type="text" 
                placeholder="搜索..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span class="absolute left-3 top-2.5 text-gray-400">🔍</span>
            </div>
          </div>
        </div>
        <code class="block mt-4 p-2 bg-gray-800 text-green-400 rounded text-sm">
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        </code>
      </section>

      <!-- 3. 卡片 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">3. 卡片组件</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white border border-gray-200 rounded-xl p-6 shadow-md hover:shadow-xl transition-shadow">
            <div class="w-12 h-12 bg-blue-500 rounded-lg mb-4 flex items-center justify-center text-white text-2xl">
              📦
            </div>
            <h3 class="text-xl font-semibold mb-2">卡片标题</h3>
            <p class="text-gray-600 mb-4">这是卡片描述内容，展示如何使用阴影和悬停效果。</p>
            <button class="text-blue-500 hover:text-blue-600 font-medium">了解更多 →</button>
          </div>
          
          <div class="bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl p-6 text-white shadow-lg">
            <div class="w-12 h-12 bg-white/20 rounded-lg mb-4 flex items-center justify-center text-2xl">
              ✨
            </div>
            <h3 class="text-xl font-semibold mb-2">渐变卡片</h3>
            <p class="text-white/90 mb-4">使用渐变背景的卡片样式。</p>
            <button class="bg-white text-purple-600 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors">
              了解更多
            </button>
          </div>
          
          <div class="bg-white border-2 border-dashed border-gray-300 rounded-xl p-6">
            <div class="w-12 h-12 bg-gray-100 rounded-lg mb-4 flex items-center justify-center text-2xl">
              📝
            </div>
            <h3 class="text-xl font-semibold mb-2">虚线边框</h3>
            <p class="text-gray-600 mb-4">使用虚线边框的卡片样式。</p>
            <button class="text-gray-600 hover:text-gray-800 font-medium">了解更多 →</button>
          </div>
        </div>
      </section>

      <!-- 4. 导航栏 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">4. 导航栏</h2>
        
        <nav class="bg-gray-800 text-white rounded-lg p-4 mb-4">
          <div class="flex items-center justify-between">
            <div class="text-xl font-bold">Logo</div>
            <div class="flex gap-6">
              <a href="#" class="hover:text-gray-300 transition-colors">首页</a>
              <a href="#" class="hover:text-gray-300 transition-colors">产品</a>
              <a href="#" class="hover:text-gray-300 transition-colors">关于</a>
              <a href="#" class="hover:text-gray-300 transition-colors">联系</a>
            </div>
            <button class="px-4 py-2 bg-blue-500 rounded hover:bg-blue-600 transition-colors">
              登录
            </button>
          </div>
        </nav>
        
        <code class="block p-2 bg-gray-800 text-green-400 rounded text-sm">
          class="flex items-center justify-between" (导航栏布局)
        </code>
      </section>

      <!-- 5. 徽章和标签 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">5. 徽章和标签</h2>
        
        <div class="flex flex-wrap gap-4 items-center">
          <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">标签</span>
          <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">成功</span>
          <span class="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">警告</span>
          <span class="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">错误</span>
          <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">默认</span>
          
          <span class="relative">
            <button class="px-4 py-2 bg-gray-200 rounded">通知</button>
            <span class="absolute -top-2 -right-2 w-5 h-5 bg-red-500 text-white rounded-full text-xs flex items-center justify-center">3</span>
          </span>
        </div>
        <code class="block mt-4 p-2 bg-gray-800 text-green-400 rounded text-sm">
          class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full" (标签)
        </code>
      </section>

      <!-- 6. 加载状态 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">6. 加载状态</h2>
        
        <div class="flex gap-8 items-center">
          <div class="flex flex-col items-center">
            <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
            <span class="text-sm text-gray-600">旋转加载</span>
          </div>
          
          <div class="flex gap-2">
            <div class="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
        <code class="block mt-4 p-2 bg-gray-800 text-green-400 rounded text-sm">
          class="border-4 border-blue-500 border-t-transparent rounded-full animate-spin" (旋转)
        </code>
      </section>

      <!-- 7. 提示框 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">7. 提示框（Alert）</h2>
        
        <div class="space-y-4">
          <div class="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
            <div class="flex items-center">
              <span class="text-blue-500 mr-2">ℹ️</span>
              <p class="text-blue-800">这是一条信息提示</p>
            </div>
          </div>
          
          <div class="p-4 bg-green-50 border-l-4 border-green-500 rounded">
            <div class="flex items-center">
              <span class="text-green-500 mr-2">✓</span>
              <p class="text-green-800">操作成功完成</p>
            </div>
          </div>
          
          <div class="p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded">
            <div class="flex items-center">
              <span class="text-yellow-500 mr-2">⚠️</span>
              <p class="text-yellow-800">请注意这个警告</p>
            </div>
          </div>
          
          <div class="p-4 bg-red-50 border-l-4 border-red-500 rounded">
            <div class="flex items-center">
              <span class="text-red-500 mr-2">✕</span>
              <p class="text-red-800">发生了一个错误</p>
            </div>
          </div>
        </div>
        <code class="block mt-4 p-2 bg-gray-800 text-green-400 rounded text-sm">
          class="p-4 bg-blue-50 border-l-4 border-blue-500 rounded" (提示框)
        </code>
      </section>

      <!-- 8. 模态框遮罩 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">8. 模态框遮罩效果</h2>
        
        <div class="relative h-64 bg-gray-200 rounded-lg overflow-hidden">
          <div class="absolute inset-0 bg-black/50 flex items-center justify-center">
            <div class="bg-white rounded-lg p-6 max-w-md mx-4">
              <h3 class="text-xl font-semibold mb-2">模态框标题</h3>
              <p class="text-gray-600 mb-4">这是模态框内容，使用绝对定位和半透明遮罩实现。</p>
              <div class="flex gap-2 justify-end">
                <button class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50">取消</button>
                <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">确认</button>
              </div>
            </div>
          </div>
        </div>
        <code class="block mt-4 p-2 bg-gray-800 text-green-400 rounded text-sm">
          遮罩: class="absolute inset-0 bg-black/50" | 内容: class="relative z-10 bg-white rounded-lg"
        </code>
      </section>

      <!-- 9. 工具提示 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">9. 工具提示（Tooltip）</h2>
        
        <div class="flex gap-8 items-center">
          <div class="relative group">
            <button class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">悬停我</button>
            <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-1 bg-gray-800 text-white text-sm rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              这是工具提示
              <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
            </div>
          </div>
        </div>
        <code class="block mt-4 p-2 bg-gray-800 text-green-400 rounded text-sm">
          使用 group 和 group-hover 实现悬停显示
        </code>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
// CSS 组件学习组件
</script>

