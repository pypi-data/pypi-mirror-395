<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-gray-800">CSS 布局学习 - 基础布局模式</h1>

      <!-- 1. Flexbox 基础 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">1. Flexbox 布局</h2>
        <p class="text-gray-600 mb-4">Flexbox 用于一维布局（横向或纵向排列）</p>
        
        <!-- 横向排列 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">横向排列 (flex-row)</h3>
          <div class="flex gap-4 p-4 bg-blue-50 rounded">
            <div class="w-20 h-20 bg-blue-500 rounded flex items-center justify-center text-white font-bold">1</div>
            <div class="w-20 h-20 bg-blue-500 rounded flex items-center justify-center text-white font-bold">2</div>
            <div class="w-20 h-20 bg-blue-500 rounded flex items-center justify-center text-white font-bold">3</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="flex gap-4"</code>
        </div>

        <!-- 纵向排列 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">纵向排列 (flex-col)</h3>
          <div class="flex flex-col gap-4 p-4 bg-green-50 rounded w-32">
            <div class="h-16 bg-green-500 rounded flex items-center justify-center text-white font-bold">1</div>
            <div class="h-16 bg-green-500 rounded flex items-center justify-center text-white font-bold">2</div>
            <div class="h-16 bg-green-500 rounded flex items-center justify-center text-white font-bold">3</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="flex flex-col gap-4"</code>
        </div>

        <!-- 居中对齐 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">居中对齐</h3>
          <div class="flex items-center justify-center h-32 bg-purple-50 rounded">
            <div class="w-20 h-20 bg-purple-500 rounded flex items-center justify-center text-white font-bold">居中</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="flex items-center justify-center"</code>
        </div>

        <!-- 两端对齐 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">两端对齐 (justify-between)</h3>
          <div class="flex justify-between items-center p-4 bg-yellow-50 rounded">
            <div class="w-20 h-20 bg-yellow-500 rounded flex items-center justify-center text-white font-bold">左</div>
            <div class="w-20 h-20 bg-yellow-500 rounded flex items-center justify-center text-white font-bold">右</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="flex justify-between"</code>
        </div>
      </section>

      <!-- 2. Grid 布局 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">2. Grid 布局</h2>
        <p class="text-gray-600 mb-4">Grid 用于二维布局（行列同时控制）</p>
        
        <!-- 基础网格 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">3x3 网格</h3>
          <div class="grid grid-cols-3 gap-4 p-4 bg-red-50 rounded">
            <div class="h-20 bg-red-500 rounded flex items-center justify-center text-white font-bold">1</div>
            <div class="h-20 bg-red-500 rounded flex items-center justify-center text-white font-bold">2</div>
            <div class="h-20 bg-red-500 rounded flex items-center justify-center text-white font-bold">3</div>
            <div class="h-20 bg-red-500 rounded flex items-center justify-center text-white font-bold">4</div>
            <div class="h-20 bg-red-500 rounded flex items-center justify-center text-white font-bold">5</div>
            <div class="h-20 bg-red-500 rounded flex items-center justify-center text-white font-bold">6</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="grid grid-cols-3 gap-4"</code>
        </div>

        <!-- 响应式网格 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">响应式网格 (移动端1列，桌面端3列)</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-indigo-50 rounded">
            <div class="h-20 bg-indigo-500 rounded flex items-center justify-center text-white font-bold">1</div>
            <div class="h-20 bg-indigo-500 rounded flex items-center justify-center text-white font-bold">2</div>
            <div class="h-20 bg-indigo-500 rounded flex items-center justify-center text-white font-bold">3</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="grid grid-cols-1 md:grid-cols-3 gap-4"</code>
        </div>
      </section>

      <!-- 3. 定位系统 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">3. 定位系统</h2>
        <p class="text-gray-600 mb-4">理解 relative、absolute、fixed 的区别</p>
        
        <!-- Relative 定位 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">Relative 定位（相对自己）</h3>
          <div class="relative p-8 bg-pink-50 rounded">
            <div class="w-20 h-20 bg-pink-500 rounded flex items-center justify-center text-white font-bold">正常</div>
            <div class="w-20 h-20 bg-pink-600 rounded flex items-center justify-center text-white font-bold relative top-4 left-4">相对定位</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="relative top-4 left-4"</code>
        </div>

        <!-- Absolute 定位 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">Absolute 定位（相对父元素）</h3>
          <div class="relative h-40 p-8 bg-orange-50 rounded">
            <div class="w-20 h-20 bg-orange-500 rounded flex items-center justify-center text-white font-bold">父元素</div>
            <div class="absolute top-4 right-4 w-20 h-20 bg-orange-600 rounded flex items-center justify-center text-white font-bold">绝对定位</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">父: class="relative" | 子: class="absolute top-4 right-4"</code>
        </div>

        <!-- Fixed 定位 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">Fixed 定位（相对视口，滚动时固定）</h3>
          <div class="relative h-40 p-8 bg-teal-50 rounded">
            <div class="w-20 h-20 bg-teal-500 rounded flex items-center justify-center text-white font-bold">内容区域</div>
            <div class="fixed bottom-4 right-4 w-16 h-16 bg-teal-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg">固定</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="fixed bottom-4 right-4"</code>
          <p class="text-sm text-gray-500 mt-2">（这个按钮会固定在屏幕右下角，即使滚动页面）</p>
        </div>
      </section>

      <!-- 4. 盒模型 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">4. 盒模型</h2>
        <p class="text-gray-600 mb-4">理解 padding、margin、border 的区别</p>
        
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">Padding（内边距）vs Margin（外边距）</h3>
          <div class="flex gap-8">
            <!-- Padding 示例 -->
            <div>
              <p class="text-sm text-gray-600 mb-2">Padding（内边距）</p>
              <div class="bg-blue-100 p-8 rounded">
                <div class="bg-blue-500 text-white p-4 rounded">内容</div>
              </div>
              <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="p-8" (padding)</code>
            </div>
            
            <!-- Margin 示例 -->
            <div>
              <p class="text-sm text-gray-600 mb-2">Margin（外边距）</p>
              <div class="bg-green-100 rounded">
                <div class="bg-green-500 text-white p-4 rounded m-8">内容</div>
              </div>
              <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="m-8" (margin)</code>
            </div>
          </div>
        </div>
      </section>

      <!-- 5. 响应式设计 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">5. 响应式设计</h2>
        <p class="text-gray-600 mb-4">使用断点适配不同屏幕尺寸</p>
        
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">响应式文字大小</h3>
          <div class="p-4 bg-gray-50 rounded">
            <p class="text-sm md:text-base lg:text-lg xl:text-xl text-gray-700">
              这段文字在小屏幕是 text-sm，中等屏幕是 text-base，大屏幕是 text-lg，超大屏幕是 text-xl
            </p>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">class="text-sm md:text-base lg:text-lg xl:text-xl"</code>
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">响应式显示/隐藏</h3>
          <div class="p-4 bg-gray-50 rounded">
            <div class="block md:hidden bg-red-500 text-white p-2 rounded mb-2">移动端显示</div>
            <div class="hidden md:block bg-blue-500 text-white p-2 rounded">桌面端显示</div>
          </div>
          <code class="block mt-2 p-2 bg-gray-800 text-green-400 rounded text-sm">移动端: class="block md:hidden" | 桌面端: class="hidden md:block"</code>
        </div>
      </section>

      <!-- 6. 常用布局模式 -->
      <section class="mb-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">6. 常用布局模式</h2>
        
        <!-- 卡片布局 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">卡片布局</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <h4 class="text-xl font-semibold mb-2">卡片标题</h4>
              <p class="text-gray-600">这是卡片内容，展示如何使用边框、圆角、阴影等效果。</p>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <h4 class="text-xl font-semibold mb-2">卡片标题</h4>
              <p class="text-gray-600">这是卡片内容，展示如何使用边框、圆角、阴影等效果。</p>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <h4 class="text-xl font-semibold mb-2">卡片标题</h4>
              <p class="text-gray-600">这是卡片内容，展示如何使用边框、圆角、阴影等效果。</p>
            </div>
          </div>
        </div>

        <!-- 侧边栏布局 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-2 text-gray-700">侧边栏布局</h3>
          <div class="flex flex-col md:flex-row gap-4">
            <aside class="w-full md:w-64 bg-gray-800 text-white p-6 rounded-lg">
              <h4 class="text-lg font-semibold mb-4">侧边栏</h4>
              <ul class="space-y-2">
                <li><a href="#" class="hover:text-gray-300">菜单项 1</a></li>
                <li><a href="#" class="hover:text-gray-300">菜单项 2</a></li>
                <li><a href="#" class="hover:text-gray-300">菜单项 3</a></li>
              </ul>
            </aside>
            <main class="flex-1 bg-white p-6 rounded-lg shadow-md">
              <h4 class="text-lg font-semibold mb-4">主内容区</h4>
              <p class="text-gray-600">这是主要内容区域，使用 flex-1 占据剩余空间。</p>
            </main>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
// CSS 布局学习组件
</script>

