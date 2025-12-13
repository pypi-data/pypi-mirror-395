<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-gray-800"></h1>
      
      <!-- 节点容器 -->
      <div class="mb-6 flex justify-center">
        <div class="relative inline-block">
          <!-- 节点主体 -->
          <div class="relative flex items-center bg-white border-2 border-gray-300 rounded-lg shadow-lg">
            <!-- 左侧输入端口区域 -->
            <div class="flex flex-col justify-center gap-2 px-2 py-4">
              <div 
                v-for="(input, index) in inputs" 
                :key="`input-${index}`"
                class="relative"
              >
                <!-- 输入连接点 -->
                <div 
                  class="absolute -left-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-md cursor-pointer hover:bg-blue-600 transition-colors"
                  :title="input.label"
                ></div>
                <!-- 输入标签 -->
                <div class="ml-4 text-sm text-gray-700 whitespace-nowrap">
                  {{ input.label }}
                </div>
              </div>
            </div>

            <!-- 节点内容区域 -->
            <div class="px-6 py-4 min-w-[120px] text-center border-x border-gray-200">
              <div class="font-semibold text-gray-800 mb-1">{{ nodeTitle }}</div>
              <div class="text-xs text-gray-500">{{ nodeType }}</div>
            </div>

            <!-- 右侧输出端口区域 -->
            <div class="flex flex-col justify-center gap-2 px-2 py-4">
              <div 
                v-for="(output, index) in outputs" 
                :key="`output-${index}`"
                class="relative"
              >
                <!-- 输出标签 -->
                <div class="mr-4 text-sm text-gray-700 whitespace-nowrap text-right">
                  {{ output.label }}
                </div>
                <!-- 输出连接点 -->
                <div 
                  class="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-green-500 rounded-full border-2 border-white shadow-md cursor-pointer hover:bg-green-600 transition-colors"
                  :title="output.label"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 多个节点示例 -->
      <div class="mt-12">
        <h2 class="text-2xl font-semibold mb-6 text-gray-700">多个节点示例</h2>
        <div class="space-y-8">
          <NodeComponent 
            v-for="(node, index) in nodes" 
            :key="index"
            :node="node"
          />
        </div>
      </div>

      <!-- 控制面板 -->
      <div class="mt-12 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700">节点配置</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">输入端口数量</label>
            <input 
              type="number" 
              v-model.number="inputCount" 
              min="1" 
              max="10"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">输出端口数量</label>
            <input 
              type="number" 
              v-model.number="outputCount" 
              min="1" 
              max="10"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 节点配置
const nodeTitle = ref('处理节点')
const nodeType = ref('Processor')
const inputCount = ref(3)
const outputCount = ref(2)

// 输入端口
const inputs = computed(() => {
  return Array.from({ length: inputCount.value }, (_, i) => ({
    label: `输入 ${i + 1}`,
    type: 'data'
  }))
})

// 输出端口
const outputs = computed(() => {
  return Array.from({ length: outputCount.value }, (_, i) => ({
    label: `输出 ${i + 1}`,
    type: 'data'
  }))
})

// 多个节点示例数据
const nodes = ref([
  {
    title: '数据输入',
    type: 'Input',
    inputs: [],
    outputs: [
      { label: '数据流', type: 'data' },
      { label: '元数据', type: 'metadata' }
    ]
  },
  {
    title: '数据处理',
    type: 'Process',
    inputs: [
      { label: '原始数据', type: 'data' },
      { label: '配置', type: 'config' }
    ],
    outputs: [
      { label: '处理后', type: 'data' },
      { label: '日志', type: 'log' },
      { label: '错误', type: 'error' }
    ]
  },
  {
    title: '数据输出',
    type: 'Output',
    inputs: [
      { label: '结果', type: 'data' },
      { label: '状态', type: 'status' }
    ],
    outputs: []
  }
])

// 节点组件
const NodeComponent = {
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  template: `
    <div class="flex justify-center">
      <div class="relative inline-block">
        <div class="relative flex items-center bg-white border-2 border-gray-300 rounded-lg shadow-lg">
          <!-- 左侧输入 -->
          <div v-if="node.inputs.length > 0" class="flex flex-col justify-center gap-2 px-2 py-4">
            <div 
              v-for="(input, index) in node.inputs" 
              :key="'input-' + index"
              class="relative"
            >
              <div 
                class="absolute -left-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-md cursor-pointer hover:bg-blue-600 transition-colors"
                :title="input.label"
              ></div>
              <div class="ml-4 text-sm text-gray-700 whitespace-nowrap">
                {{ input.label }}
              </div>
            </div>
          </div>

          <!-- 节点内容 -->
          <div class="px-6 py-4 min-w-[120px] text-center border-x border-gray-200">
            <div class="font-semibold text-gray-800 mb-1">{{ node.title }}</div>
            <div class="text-xs text-gray-500">{{ node.type }}</div>
          </div>

          <!-- 右侧输出 -->
          <div v-if="node.outputs.length > 0" class="flex flex-col justify-center gap-2 px-2 py-4">
            <div 
              v-for="(output, index) in node.outputs" 
              :key="'output-' + index"
              class="relative"
            >
              <div class="mr-4 text-sm text-gray-700 whitespace-nowrap text-right">
                {{ output.label }}
              </div>
              <div 
                class="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-green-500 rounded-full border-2 border-white shadow-md cursor-pointer hover:bg-green-600 transition-colors"
                :title="output.label"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
}
</script>