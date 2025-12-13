<template>
  <div
    ref="nodeRef"
    :class="[
      'node-item absolute cursor-move select-none',
      isSelected ? 'ring-2 ring-blue-500' : ''
    ]"
    :style="{
      left: `${node.position.x}px`,
      top: `${node.position.y}px`
    }"
    @mousedown="handleMouseDown"
    @contextmenu.prevent="handleContextMenu"
  >
    <div class="relative flex items-center bg-white border-2 border-gray-300 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
      <!-- 左侧输入端口区域 -->
      <div v-if="node.inputs && node.inputs.length > 0" class="flex flex-col justify-center gap-2 px-2 py-4">
        <div
          v-for="input in node.inputs"
          :key="input.id"
          class="relative"
        >
          <!-- 输入连接点 -->
          <div
            :ref="el => setInputPortRef(el, input.id)"
            :data-port-id="input.id"
            :data-node-id="node.id"
            :data-port-type="input.type"
            class="absolute -left-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-md cursor-default hover:bg-blue-600 hover:scale-110 transition-all"
            style="z-index: 100;"
            title="输入端口(只能作为连接目标)"
            @mousedown.stop
          ></div>
          <!-- 输入标签 -->
          <div class="ml-4 text-sm text-gray-700 whitespace-nowrap">
            {{ input.label }}
          </div>
        </div>
      </div>

      <!-- 节点内容区域 -->
      <div class="px-6 py-4 min-w-[120px] text-center border-x border-gray-200">
        <div class="font-semibold text-gray-800 mb-1">{{ node.title }}</div>
        <div class="text-xs text-gray-500">{{ node.type }}</div>
        
        <!-- 输入节点配置 -->
        <div v-if="node.type === 'input'" class="mt-2">
          <input
            type="text"
            :value="node.config?.value ?? ''"
            @input="handleInputValueChange"
            @click.stop
            @mousedown.stop
            placeholder="输入数值"
            class="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>
        <div v-if="node.type === 'select'" class="mt-2">
          <select
            :id="node.id + '_select'"
            :value="node.config?.value ?? true"
            @change="handleSelectChange"
            @click.stop
            @mousedown.stop
            class="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option v-for="option in node.config?.options" :key="option.id" :value="option.id">{{ option.label }}</option>
          </select>
        </div>
        
        <!-- 正弦波信号源节点配置 -->
        <div v-if="node.type === 'sine_wave'" class="mt-2 space-y-1">
          <div class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-12 text-left">频率:</label>
            <input
              type="number"
              :value="node.config?.frequency ?? 1"
              @input="handleConfigChange('frequency', $event)"
              @click.stop
              @mousedown.stop
              step="0.1"
              min="0.1"
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
            />
          </div>
          <div class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-12 text-left">幅度:</label>
            <input
              type="number"
              :value="node.config?.amplitude ?? 1"
              @input="handleConfigChange('amplitude', $event)"
              @click.stop
              @mousedown.stop
              step="0.1"
              min="0"
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
            />
          </div>
          <div class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-12 text-left">相位:</label>
            <input
              type="number"
              :value="node.config?.phase ?? 0"
              @input="handleConfigChange('phase', $event)"
              @click.stop
              @mousedown.stop
              step="0.1"
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
              title="相位角（弧度），例如：0, π/2, π, 3π/2 等"
            />
          </div>
          <div class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-12 text-left">采样:</label>
            <input
              type="number"
              :value="node.config?.samples ?? 100"
              @input="handleConfigChange('samples', $event)"
              @click.stop
              @mousedown.stop
              step="10"
              min="10"
              max="1000"
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
            />
          </div>
        </div>
        
        <!-- 信号处理节点配置 -->
        <div v-if="node.type === 'signal_process'" class="mt-2 space-y-1">
          <div class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-16 text-left">类型:</label>
            <select
              :value="node.config?.processType ?? 'amplify'"
              @change="handleConfigChange('processType', $event)"
              @click.stop
              @mousedown.stop
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
            >
              <option value="amplify">放大</option>
              <option value="lowpass">低通滤波</option>
              <option value="highpass">高通滤波</option>
              <option value="normalize">归一化</option>
            </select>
          </div>
          <div v-if="node.config?.processType === 'amplify'" class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-16 text-left">增益:</label>
            <input
              type="number"
              :value="node.config?.gain ?? 1"
              @input="handleConfigChange('gain', $event)"
              @click.stop
              @mousedown.stop
              step="0.1"
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
            />
          </div>
          <div v-if="node.config?.processType === 'lowpass' || node.config?.processType === 'highpass'" class="flex items-center gap-1">
            <label class="text-xs text-gray-600 w-16 text-left">窗口:</label>
            <input
              type="number"
              :value="node.config?.windowSize ?? 3"
              @input="handleConfigChange('windowSize', $event)"
              @click.stop
              @mousedown.stop
              step="1"
              min="1"
              max="20"
              class="flex-1 px-1 py-0.5 text-xs border border-gray-300 rounded"
            />
          </div>
        </div>
        
        <!-- 波形显示节点 -->
        <div v-if="node.type === 'waveform_display'" class="mt-2">
          <canvas
            ref="waveformCanvas"
            :width="200"
            :height="80"
            class="w-full border border-gray-300 rounded"
            @click.stop
            @mousedown.stop
          ></canvas>
        </div>
        
        <!-- 输出节点显示结果 -->
        <div v-if="node.type === 'output' && node.data?.outputs" class="mt-2">
          <div class="px-2 py-1 text-xs bg-green-50 border border-green-200 rounded text-green-800 break-all">
            输出: {{ formatOutputValue(node.data.outputs.result) }}
          </div>
        </div>
        
        <div v-if="node.data?.status" class="mt-1 text-xs" :class="statusColor">
          {{ node.data.status }}
        </div>
      </div>

      <!-- 右侧输出端口区域 -->
      <div v-if="node.outputs && node.outputs.length > 0" class="flex flex-col justify-center gap-2 px-2 py-4">
        <div
          v-for="output in node.outputs"
          :key="output.id"
          class="relative"
        >
          <!-- 输出标签 -->
          <div class="mr-4 text-sm text-gray-700 whitespace-nowrap text-right">
            {{ output.label }}
          </div>
          <!-- 输出连接点 -->
          <div
            :ref="el => setOutputPortRef(el, output.id)"
            :data-port-id="output.id"
            :data-node-id="node.id"
            :data-port-type="output.type"
            class="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-green-500 rounded-full border-2 border-white shadow-md cursor-crosshair hover:bg-green-600 hover:scale-110 transition-all"
            style="z-index: 100;"
            :title="output.label + ' - 点击并拖拽到输入端口创建连接'"
            @mousedown.stop="handlePortMouseDown($event, 'output', output.id)"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import type { NodeData } from './types'

interface Props {
  node: NodeData
  isSelected?: boolean
  zoom?: number
}

const props = withDefaults(defineProps<Props>(), {
  isSelected: false,
  zoom: 1
})

const emit = defineEmits<{
  'update:position': [position: { x: number; y: number }]
  'port-mousedown': [event: MouseEvent, portType: 'input' | 'output', portId: string]
  'select': []
  'context-menu': [event: MouseEvent]
  'update:config': [config: Record<string, any>]
}>()

const nodeRef = ref<HTMLElement>()
const waveformCanvas = ref<HTMLCanvasElement>()
const inputPortRefs = new Map<string, HTMLElement>()
const outputPortRefs = new Map<string, HTMLElement>()

let isDragging = false
let dragStart = { x: 0, y: 0 }
let nodeStartPos = { x: 0, y: 0 }

const statusColor = computed(() => {
  const status = props.node.data?.status
  if (status === 'running') return 'text-blue-600'
  if (status === 'success') return 'text-green-600'
  if (status === 'error') return 'text-red-600'
  return 'text-gray-600'
})

const formatOutputValue = (value: any): string => {
  if (value === null || value === undefined) return 'null'
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value)
    } catch {
      return String(value)
    }
  }
  return String(value)
}

const setInputPortRef = (el: any, portId: string) => {
  if (el && el instanceof HTMLElement) {
    inputPortRefs.set(portId, el)
  } else {
    inputPortRefs.delete(portId)
  }
}

const setOutputPortRef = (el: any, portId: string) => {
  if (el && el instanceof HTMLElement) {
    outputPortRefs.set(portId, el)
  } else {
    outputPortRefs.delete(portId)
  }
}

const handleMouseDown = (e: MouseEvent) => {
  if (e.button !== 0) return // 只处理左键
  
  emit('select')
  isDragging = true
  dragStart = { x: e.clientX, y: e.clientY }
  nodeStartPos = { ...props.node.position }
  
  e.preventDefault()
}

const handlePortMouseDown = (e: MouseEvent, portType: 'input' | 'output', portId: string) => {
  emit('port-mousedown', e, portType, portId)
}

const handleContextMenu = (e: MouseEvent) => {
  emit('context-menu', e)
}

const handleInputValueChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const value = target.value
  
  // 更新节点配置
  const newConfig = {
    ...props.node.config,
    value: value
  }
  
  // 通知父组件配置已更新
  emit('update:config', newConfig)
}

const handleSelectChange = (e: Event) => {
  const target = e.target as HTMLSelectElement
  const value = target.value
  console.log('handleSelectChange', value)
  // 更新节点配置
  const newConfig = {
    ...props.node.config,
    value: value
  }
  
  // 通知父组件配置已更新
  emit('update:config', newConfig)
}

const handleConfigChange = (key: string, e: Event) => {
  const target = e.target as HTMLInputElement | HTMLSelectElement
  let value: any = target.value
  
  // 如果是数字输入，转换为数字
  if (target.type === 'number') {
    value = parseFloat(value) || 0
  }
  
  // 更新节点配置
  const newConfig = {
    ...props.node.config,
    [key]: value
  }
  
  // 通知父组件配置已更新
  emit('update:config', newConfig)
}

// 绘制波形
const drawWaveform = () => {
  if (!waveformCanvas.value || props.node.type !== 'waveform_display') return
  
  const canvas = waveformCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  // 从 outputs.waveform 获取数据（executor 返回的数据）
  let waveform = props.node.data?.outputs?.waveform
  
  // 如果没有 waveform，尝试从其他可能的输出字段获取（兼容信号处理节点等）
  if (!Array.isArray(waveform) || waveform.length === 0) {
    // 尝试从其他输出字段获取
    const outputs = props.node.data?.outputs
    if (outputs) {
      // 检查是否有 'output' 字段（信号处理节点、波形相加节点等）
      if (Array.isArray(outputs.output)) {
        waveform = outputs.output
      } else if (Array.isArray(outputs.signal)) {
        waveform = outputs.signal
      } else if (Array.isArray(outputs.result)) {
        waveform = outputs.result
      }
    }
  }
  
  if (!Array.isArray(waveform) || waveform.length === 0) {
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = '#999'
    ctx.font = '12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText('无信号', canvas.width / 2, canvas.height / 2)
    
    // 调试信息
    console.log('波形显示节点 - 无数据:', {
      nodeId: props.node.id,
      outputs: props.node.data?.outputs,
      hasOutputs: !!props.node.data?.outputs,
      waveformType: typeof waveform,
      waveformLength: Array.isArray(waveform) ? waveform.length : 'not array',
      nodeData: props.node.data
    })
    return
  }
  
  const width = canvas.width
  const height = canvas.height
  const padding = 10
  
  // 清空画布
  ctx.clearRect(0, 0, width, height)
  
  // 设置样式
  ctx.strokeStyle = '#3b82f6'
  ctx.lineWidth = 2
  ctx.fillStyle = '#3b82f6'
  
  // 计算数据范围
  const values = waveform as number[]
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1 // 避免除零
  
  // 绘制网格线
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 1
  const centerY = height / 2
  ctx.beginPath()
  ctx.moveTo(padding, centerY)
  ctx.lineTo(width - padding, centerY)
  ctx.stroke()
  
  // 绘制波形
  ctx.strokeStyle = '#3b82f6'
  ctx.lineWidth = 2
  ctx.beginPath()
  
  const stepX = (width - padding * 2) / (values.length - 1)
  
  for (let i = 0; i < values.length; i++) {
    const x = padding + i * stepX
    // 归一化到 0-1，然后映射到画布高度
    const normalized = (values[i] - min) / range
    const y = padding + (1 - normalized) * (height - padding * 2)
    
    if (i === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  }
  
  ctx.stroke()
  
  // 绘制坐标轴标签
  ctx.fillStyle = '#6b7280'
  ctx.font = '10px Arial'
  ctx.textAlign = 'left'
  ctx.fillText(`Max: ${max.toFixed(2)}`, padding, 10)
  ctx.textAlign = 'right'
  ctx.fillText(`Min: ${min.toFixed(2)}`, width - padding, height - 5)
}

// 监听波形数据变化
watch(
  () => props.node.data?.outputs?.waveform,
  () => {
    nextTick(() => {
      drawWaveform()
    })
  },
  { deep: true }
)

// 监听节点类型变化
watch(
  () => props.node.type,
  () => {
    if (props.node.type === 'waveform_display') {
      nextTick(() => {
        drawWaveform()
      })
    }
  }
)

const handleMouseMove = (e: MouseEvent) => {
  if (!isDragging) return
  
  const dx = e.clientX - dragStart.x
  const dy = e.clientY - dragStart.y
  
  emit('update:position', {
    x: nodeStartPos.x + dx,
    y: nodeStartPos.y + dy
  })
}

const handleMouseUp = () => {
  isDragging = false
}

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
  
  // 如果是波形显示节点，初始化绘制
  if (props.node.type === 'waveform_display') {
    nextTick(() => {
      drawWaveform()
    })
  }
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
})

// 暴露方法供父组件获取端口位置
defineExpose({
  getInputPortPosition: (portId: string) => {
    const port = inputPortRefs.get(portId)
    if (!port || !nodeRef.value) return null
    
    // 使用 getBoundingClientRect 获取屏幕坐标
    const portRect = port.getBoundingClientRect()
    const nodeRect = nodeRef.value.getBoundingClientRect()
    
    // 计算端口中心点的屏幕坐标
    const portScreenX = portRect.left + portRect.width / 2
    const portScreenY = portRect.top + portRect.height / 2
    
    // 计算节点左上角的屏幕坐标
    const nodeScreenX = nodeRect.left
    const nodeScreenY = nodeRect.top
    
    // 端口相对于节点的屏幕坐标差
    const screenOffsetX = portScreenX - nodeScreenX
    const screenOffsetY = portScreenY - nodeScreenY
    
    // 关键：节点层应用了 scale(zoom)，所以屏幕坐标差 = 画布坐标差 * zoom
    // 因此画布坐标差 = 屏幕坐标差 / zoom
    // 注意：这里不需要考虑 viewport.x/y，因为它们对相对位置没有影响
    const canvasOffsetX = screenOffsetX / props.zoom
    const canvasOffsetY = screenOffsetY / props.zoom
    
    // 返回画布坐标（节点位置 + 端口相对位置）
    // SVG 会应用相同的缩放和偏移，所以坐标会自动对齐
    const result = {
      x: props.node.position.x + canvasOffsetX,
      y: props.node.position.y + canvasOffsetY
    }
    
    
    return result
  },
  getOutputPortPosition: (portId: string) => {
    const port = outputPortRefs.get(portId)
    if (!port || !nodeRef.value) return null
    
    // 使用 getBoundingClientRect 获取屏幕坐标
    const portRect = port.getBoundingClientRect()
    const nodeRect = nodeRef.value.getBoundingClientRect()
    
    // 计算端口中心点的屏幕坐标
    const portScreenX = portRect.left + portRect.width / 2
    const portScreenY = portRect.top + portRect.height / 2
    
    // 计算节点左上角的屏幕坐标
    const nodeScreenX = nodeRect.left
    const nodeScreenY = nodeRect.top
    
    // 端口相对于节点的屏幕坐标差
    const screenOffsetX = portScreenX - nodeScreenX
    const screenOffsetY = portScreenY - nodeScreenY
    
    // 关键：节点层应用了 scale(zoom)，所以屏幕坐标差 = 画布坐标差 * zoom
    // 因此画布坐标差 = 屏幕坐标差 / zoom
    // 注意：这里不需要考虑 viewport.x/y，因为它们对相对位置没有影响
    const canvasOffsetX = screenOffsetX / props.zoom
    const canvasOffsetY = screenOffsetY / props.zoom
    
    // 返回画布坐标（节点位置 + 端口相对位置）
    // SVG 会应用相同的缩放和偏移，所以坐标会自动对齐
    const result = {
      x: props.node.position.x + canvasOffsetX,
      y: props.node.position.y + canvasOffsetY
    }
    
    
    return result
  }
})
</script>

<style scoped>
.node-item {
  transform-origin: top left;
}
</style>

