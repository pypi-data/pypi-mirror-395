<template>
  <div class="flow-engine-demo p-6 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">FlowEngine 示例</h1>
      
      <!-- 控制面板 -->
      <div class="bg-white rounded-lg shadow-md p-4 mb-6">
        <div class="flex items-center gap-4">
          <button
            @click="handleStart"
            :disabled="isRunning"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            启动引擎
          </button>
          <button
            @click="handleStop"
            :disabled="!isRunning"
            class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            停止引擎
          </button>
          <button
            @click="clearLogs"
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
          >
            清空日志
          </button>
          <div class="ml-auto flex items-center gap-2">
            <span class="text-sm text-gray-600">状态:</span>
            <span
              class="px-3 py-1 rounded text-sm font-semibold"
              :class="isRunning ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
            >
              {{ isRunning ? '运行中' : '已停止' }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 节点状态面板 -->
        <div class="bg-white rounded-lg shadow-md p-4">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">节点状态</h2>
          <div class="space-y-3">
            <div
              v-for="node in nodeStates"
              :key="node.id"
              class="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="font-semibold text-gray-800">{{ node.name }}</span>
                <span class="text-xs px-2 py-1 rounded" :class="node.statusClass">
                  {{ node.status }}
                </span>
              </div>
              <div class="text-sm text-gray-600 space-y-1">
                <div v-if="node.inputs && Object.keys(node.inputs).length > 0">
                  <div class="font-medium text-gray-700 mb-1">输入:</div>
                  <div
                    v-for="(value, key) in node.inputs"
                    :key="key"
                    class="ml-2 text-xs"
                  >
                    {{ key }}: <span class="font-mono">{{ formatValue(value) }}</span>
                  </div>
                </div>
                <div v-if="node.outputs && Object.keys(node.outputs).length > 0">
                  <div class="font-medium text-gray-700 mb-1 mt-2">输出:</div>
                  <div
                    v-for="(value, key) in node.outputs"
                    :key="key"
                    class="ml-2 text-xs"
                  >
                    {{ key }}: <span class="font-mono text-blue-600">{{ formatValue(value) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 日志面板 -->
        <div class="bg-white rounded-lg shadow-md p-4">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">执行日志</h2>
          <div
            ref="logContainer"
            class="bg-gray-900 text-green-400 font-mono text-xs p-4 rounded-lg h-96 overflow-y-auto"
          >
            <div
              v-for="(log, index) in logs"
              :key="index"
              class="mb-1"
              :class="log.type === 'error' ? 'text-red-400' : log.type === 'info' ? 'text-blue-400' : 'text-green-400'"
            >
              <span class="text-gray-500">[{{ log.time }}]</span> {{ log.message }}
            </div>
            <div v-if="logs.length === 0" class="text-gray-500">
              暂无日志...
            </div>
          </div>
        </div>
      </div>

      <!-- 连接关系图 -->
      <div class="bg-white rounded-lg shadow-md p-4 mt-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">连接关系</h2>
        <div class="flex flex-wrap gap-4">
          <div
            v-for="link in links"
            :key="`${link.from.node}-${link.from.port}-${link.to.node}-${link.to.port}`"
            class="px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg text-sm"
          >
            <span class="font-semibold text-blue-800">{{ link.from.node }}</span>
            <span class="text-gray-500 mx-2">.</span>
            <span class="text-blue-600">{{ link.from.port }}</span>
            <span class="text-gray-400 mx-2">→</span>
            <span class="font-semibold text-green-800">{{ link.to.node }}</span>
            <span class="text-gray-500 mx-2">.</span>
            <span class="text-green-600">{{ link.to.port }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import type { BaseNode, Link } from './FlowEngine'
import { Engine, SourceNode, AdderNode, PrintNode } from './FlowEngine'

// 状态
const isRunning = ref(false)
const logs = ref<Array<{ time: string; message: string; type?: string }>>([])
const nodeStates = ref<Array<{
  id: string
  name: string
  status: string
  statusClass: string
  inputs?: Record<string, any>
  outputs?: Record<string, any>
}>>([])
const links = ref<Link[]>([])
const logContainer = ref<HTMLElement>()

// 引擎实例
let engine: Engine | null = null
let source1: SourceNode | null = null
let source2: SourceNode | null = null
let adder: AdderNode | null = null
let printer: PrintNode | null = null

// 拦截 console.log 来捕获日志
const originalLog = console.log
const originalError = console.error

const addLog = (message: string, type: 'log' | 'error' | 'info' = 'log') => {
  const time = new Date().toLocaleTimeString()
  logs.value.push({ time, message, type })
  
  // 自动滚动到底部
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
  
  // 限制日志数量
  if (logs.value.length > 1000) {
    logs.value = logs.value.slice(-500)
  }
}

// 更新节点状态
const updateNodeStates = () => {
  if (!engine) return
  
  nodeStates.value = []
  
  // Source Node 1
  if (source1) {
    nodeStates.value.push({
      id: source1.id,
      name: 'Source A (随机数, 300ms)',
      status: isRunning.value ? '运行中' : '已停止',
      statusClass: isRunning.value ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800',
      outputs: { ...source1.outputs }
    })
  }
  
  // Source Node 2
  if (source2) {
    nodeStates.value.push({
      id: source2.id,
      name: 'Source B (随机数, 500ms)',
      status: isRunning.value ? '运行中' : '已停止',
      statusClass: isRunning.value ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800',
      outputs: { ...source2.outputs }
    })
  }
  
  // Adder Node
  if (adder) {
    nodeStates.value.push({
      id: adder.id,
      name: 'Adder (加法器)',
      status: '就绪',
      statusClass: 'bg-blue-100 text-blue-800',
      inputs: { ...adder.inputs },
      outputs: { ...adder.outputs }
    })
  }
  
  // Print Node
  if (printer) {
    nodeStates.value.push({
      id: printer.id,
      name: 'Printer (输出)',
      status: '就绪',
      statusClass: 'bg-purple-100 text-purple-800',
      inputs: { ...printer.inputs }
    })
  }
}

// 初始化引擎
const initEngine = () => {
  // 创建引擎
  engine = new Engine()
  
  // 创建节点
  source1 = new SourceNode(() => Math.floor(Math.random() * 10), 300, 'srcA')
  source2 = new SourceNode(() => Math.floor(Math.random() * 10), 500, 'srcB')
  adder = new AdderNode('adder1')
  printer = new PrintNode('printer1')
  
  // 注册节点
  engine.addNode(source1)
  engine.addNode(source2)
  engine.addNode(adder)
  engine.addNode(printer)
  
  // 创建连接
  const link1: Link = { from: { node: 'srcA', port: 'out' }, to: { node: 'adder1', port: 'a' } }
  const link2: Link = { from: { node: 'srcB', port: 'out' }, to: { node: 'adder1', port: 'b' } }
  const link3: Link = { from: { node: 'adder1', port: 'sum' }, to: { node: 'printer1', port: 'in' } }
  
  engine.addLink(link1)
  engine.addLink(link2)
  engine.addLink(link3)
  
  links.value = [link1, link2, link3]
  
  // 拦截 console.log 和 console.error
  console.log = (...args: any[]) => {
    originalLog(...args)
    const message = args.map(arg => 
      typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
    ).join(' ')
    addLog(message, 'log')
  }
  
  console.error = (...args: any[]) => {
    originalError(...args)
    const message = args.map(arg => 
      typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
    ).join(' ')
    addLog(message, 'error')
  }
  
  updateNodeStates()
}

// 启动引擎
const handleStart = () => {
  if (!engine || isRunning.value) return
  
  isRunning.value = true
  addLog('启动引擎...', 'info')
  
  if (engine) {
    engine.startAllSources()
    addLog('所有源节点已启动', 'info')
  }
  
  // 定期更新节点状态
  const updateInterval = setInterval(() => {
    if (!isRunning.value) {
      clearInterval(updateInterval)
      return
    }
    updateNodeStates()
  }, 100)
  
  // 存储 interval ID 以便清理
  ;(window as any).__flowEngineUpdateInterval = updateInterval
}

// 停止引擎
const handleStop = () => {
  if (!engine || !isRunning.value) return
  
  isRunning.value = false
  addLog('停止引擎...', 'info')
  
  if (engine) {
    engine.stopAllSources()
    addLog('所有源节点已停止', 'info')
  }
  
  // 清理更新间隔
  if ((window as any).__flowEngineUpdateInterval) {
    clearInterval((window as any).__flowEngineUpdateInterval)
    delete (window as any).__flowEngineUpdateInterval
  }
  
  updateNodeStates()
}

// 清空日志
const clearLogs = () => {
  logs.value = []
}

// 格式化值
const formatValue = (value: any): string => {
  if (value === undefined || value === null) return 'undefined'
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value)
    } catch {
      return String(value)
    }
  }
  return String(value)
}

// 组件挂载时初始化
onMounted(() => {
  initEngine()
})

// 组件卸载时清理
onUnmounted(() => {
  handleStop()
  
  // 恢复原始 console 方法
  console.log = originalLog
  console.error = originalError
  
  // 清理更新间隔
  if ((window as any).__flowEngineUpdateInterval) {
    clearInterval((window as any).__flowEngineUpdateInterval)
  }
})
</script>

<style scoped>
.flow-engine-demo {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>

