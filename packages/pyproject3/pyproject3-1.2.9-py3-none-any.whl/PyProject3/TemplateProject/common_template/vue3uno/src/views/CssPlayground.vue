<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-gray-800">CSS 交互式学习 - 实时预览</h1>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 左侧：控制面板 -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-2xl font-semibold mb-6 text-gray-700">控制面板</h2>
          
          <!-- Flexbox 控制 -->
          <div class="mb-8">
            <h3 class="text-lg font-medium mb-4 text-gray-700">Flexbox 布局</h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">方向 (flex-direction)</label>
                <select v-model="flexDirection" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                  <option value="row">row (横向)</option>
                  <option value="col">column (纵向)</option>
                  <option value="row-reverse">row-reverse</option>
                  <option value="column-reverse">column-reverse</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">主轴对齐 (justify-content)</label>
                <select v-model="justifyContent" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                  <option value="start">flex-start</option>
                  <option value="center">center</option>
                  <option value="end">flex-end</option>
                  <option value="between">space-between</option>
                  <option value="around">space-around</option>
                  <option value="evenly">space-evenly</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">交叉轴对齐 (align-items)</label>
                <select v-model="alignItems" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                  <option value="start">flex-start</option>
                  <option value="center">center</option>
                  <option value="end">flex-end</option>
                  <option value="stretch">stretch</option>
                  <option value="baseline">baseline</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">间距 (gap)</label>
                <input 
                  type="range" 
                  v-model.number="gap" 
                  min="0" 
                  max="32" 
                  step="2"
                  class="w-full"
                />
                <span class="text-sm text-gray-600">{{ gap }}px</span>
              </div>
            </div>
          </div>

          <!-- 颜色控制 -->
          <div class="mb-8">
            <h3 class="text-lg font-medium mb-4 text-gray-700">颜色</h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">背景色</label>
                <div class="flex gap-2 flex-wrap">
                  <button 
                    v-for="color in colors" 
                    :key="color"
                    @click="bgColor = color"
                    :class="[
                      'w-10 h-10 rounded border-2',
                      `bg-${color}-500`,
                      bgColor === color ? 'border-gray-800' : 'border-transparent'
                    ]"
                  ></button>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">文字颜色</label>
                <select v-model="textColor" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                  <option value="white">白色</option>
                  <option value="black">黑色</option>
                  <option value="gray-600">灰色</option>
                  <option value="blue-600">蓝色</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 尺寸控制 -->
          <div class="mb-8">
            <h3 class="text-lg font-medium mb-4 text-gray-700">尺寸</h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">容器高度</label>
                <input 
                  type="range" 
                  v-model.number="containerHeight" 
                  min="200" 
                  max="600" 
                  step="50"
                  class="w-full"
                />
                <span class="text-sm text-gray-600">{{ containerHeight }}px</span>
              </div>
            </div>
          </div>

          <!-- 代码显示 -->
          <div class="mb-8">
            <h3 class="text-lg font-medium mb-4 text-gray-700">生成的代码</h3>
            <div class="bg-gray-800 p-4 rounded-lg overflow-x-auto">
              <code class="text-green-400 text-sm">
                {{ generatedCode }}
              </code>
            </div>
          </div>
        </div>

        <!-- 右侧：预览区域 -->
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-2xl font-semibold mb-6 text-gray-700">实时预览</h2>
          
          <div 
            :class="[
              'flex',
              `flex-${flexDirection}`,
              `justify-${justifyContent}`,
              `items-${alignItems}`,
              `gap-${gap}`,
              `bg-${bgColor}-500`,
              `text-${textColor}`,
              'p-6 rounded-lg border-2 border-dashed border-gray-300'
            ]"
            :style="{ height: `${containerHeight}px` }"
          >
            <div class="w-20 h-20 bg-white/30 rounded flex items-center justify-center font-bold backdrop-blur-sm">
              1
            </div>
            <div class="w-20 h-20 bg-white/30 rounded flex items-center justify-center font-bold backdrop-blur-sm">
              2
            </div>
            <div class="w-20 h-20 bg-white/30 rounded flex items-center justify-center font-bold backdrop-blur-sm">
              3
            </div>
          </div>

          <!-- 说明 -->
          <div class="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 class="font-semibold mb-2 text-blue-900">💡 学习提示</h4>
            <ul class="text-sm text-blue-800 space-y-1">
              <li>• 调整方向看横向/纵向排列的区别</li>
              <li>• 改变对齐方式理解 justify-content 和 align-items</li>
              <li>• 修改间距观察 gap 属性的效果</li>
              <li>• 尝试不同颜色组合</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 常用布局模板 -->
      <div class="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-6 text-gray-700">常用布局模板</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 居中布局 -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">居中布局</h3>
            <div class="h-32 bg-gray-100 rounded flex items-center justify-center mb-2">
              <div class="w-16 h-16 bg-blue-500 rounded"></div>
            </div>
            <code class="text-xs bg-gray-800 text-green-400 p-2 rounded block">
              class="flex items-center justify-center"
            </code>
          </div>

          <!-- 两端对齐 -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">两端对齐</h3>
            <div class="h-32 bg-gray-100 rounded flex items-center justify-between px-4 mb-2">
              <div class="w-16 h-16 bg-blue-500 rounded"></div>
              <div class="w-16 h-16 bg-blue-500 rounded"></div>
            </div>
            <code class="text-xs bg-gray-800 text-green-400 p-2 rounded block">
              class="flex items-center justify-between"
            </code>
          </div>

          <!-- 垂直居中 -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">垂直居中</h3>
            <div class="h-32 bg-gray-100 rounded flex flex-col items-center justify-center mb-2">
              <div class="w-16 h-16 bg-blue-500 rounded mb-2"></div>
              <div class="w-16 h-16 bg-blue-500 rounded"></div>
            </div>
            <code class="text-xs bg-gray-800 text-green-400 p-2 rounded block">
              class="flex flex-col items-center justify-center"
            </code>
          </div>

          <!-- 等分布局 -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="font-semibold mb-2">等分布局</h3>
            <div class="h-32 bg-gray-100 rounded flex items-center gap-2 px-2 mb-2">
              <div class="flex-1 h-16 bg-blue-500 rounded"></div>
              <div class="flex-1 h-16 bg-blue-500 rounded"></div>
              <div class="flex-1 h-16 bg-blue-500 rounded"></div>
            </div>
            <code class="text-xs bg-gray-800 text-green-400 p-2 rounded block">
              class="flex" + class="flex-1" (子元素)
            </code>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const flexDirection = ref('row')
const justifyContent = ref('center')
const alignItems = ref('center')
const gap = ref(4)
const bgColor = ref('blue')
const textColor = ref('white')
const containerHeight = ref(300)

const colors = ['blue', 'green', 'purple', 'pink', 'red', 'yellow', 'indigo', 'gray']

// 生成代码字符串
const generatedCode = computed(() => {
  return `<div class="flex flex-${flexDirection.value} justify-${justifyContent.value} items-${alignItems.value} gap-${gap.value} bg-${bgColor.value}-500 text-${textColor.value}" style="height: ${containerHeight.value}px">`
})
</script>

