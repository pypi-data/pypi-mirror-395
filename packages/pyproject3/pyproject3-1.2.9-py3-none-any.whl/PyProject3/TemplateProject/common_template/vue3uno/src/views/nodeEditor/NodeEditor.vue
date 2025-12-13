<template>
  <div class="node-editor" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; width: 100vw; height: 100vh; z-index: 1000; display: flex; flex-direction: column; background-color: #f3f4f6; overflow: hidden;">
    <!-- 工具栏 -->
    <div class="bg-white border-b border-gray-200 px-4 py-2 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-4">
        <h1 class="text-xl font-bold text-gray-800">节点编辑器</h1>
        <div class="flex gap-2">
          <!-- 调试信息 -->
          <span class="text-xs text-gray-500">isRunning: {{ isRunning }}</span>
          
          <button
            v-if="!isRunning"
            @click="handleRun"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            运行
          </button>
          <template v-else>
            <button
              @click="handlePause"
              class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition-colors"
            >
              {{ isPaused ? '继续' : '暂停' }}
            </button>
            <button
              @click="handleStop"
              class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
            >
              停止
            </button>
          </template>
          <button
            @click="handleClear"
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
          >
            清空
          </button>
          <button
            @click="showNodePalette = !showNodePalette"
            class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
          >
            添加节点
          </button>
          <label v-if="isRunning" class="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded cursor-pointer">
            <input
              type="checkbox"
              v-model="autoCalculate"
              class="cursor-pointer"
            />
            <span class="text-sm text-gray-700">自动计算</span>
          </label>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600">缩放: {{ Math.round(viewport.zoom * 100) }}%</span>
        <button
          @click="viewport.zoom = Math.min(2, viewport.zoom + 0.1)"
          class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          +
        </button>
        <button
          @click="viewport.zoom = Math.max(0.5, viewport.zoom - 0.1)"
          class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          -
        </button>
        <button
          @click="resetViewport"
          class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          重置
        </button>
      </div>
    </div>

    <div class="flex flex-1 overflow-hidden">
      <!-- 节点面板 -->
      <div
        v-if="showNodePalette"
        class="w-64 bg-white border-r border-gray-200 overflow-y-auto p-4"
      >
        <h2 class="text-lg font-semibold mb-4">节点库</h2>
        <div class="space-y-2">
          <div
            v-for="category in nodeCategories"
            :key="category"
            class="mb-4"
          >
            <h3 class="text-sm font-medium text-gray-700 mb-2">{{ category }}</h3>
            <div
              v-for="nodeDef in getNodesByCategory(category)"
              :key="nodeDef.type"
              class="p-3 bg-gray-50 rounded cursor-move hover:bg-gray-100 border border-gray-200 mb-2"
              draggable="true"
              @dragstart="handleDragStart($event, nodeDef)"
            >
              <div class="font-medium text-sm">{{ nodeDef.title }}</div>
              <div class="text-xs text-gray-500 mt-1">{{ nodeDef.description }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 画布区域 -->
      <div
        ref="canvasRef"
        class="flex-1 relative overflow-hidden bg-gray-50"
        style="min-height: 0;"
        @drop="handleDrop"
        @dragover.prevent
        @mousedown="handleCanvasMouseDown"
        @mousemove="handleCanvasMouseMove"
        @mouseup="handleCanvasMouseUp"
        @wheel.prevent="handleWheel"
      >
        <!-- SVG 连线层 -->
        <svg
          class="absolute inset-0 pointer-events-none"
          style="width: 100%; height: 100%; z-index: 1;"
        >
          <g 
            :transform="`translate(${viewport.x}, ${viewport.y}) scale(${viewport.zoom})`"
            style="transform-origin: 0 0;"
          >
            <!-- 临时连线（正在拖拽） -->
            <path
              v-if="tempConnection"
              :d="getTempConnectionPath()"
              stroke="#3b82f6"
              stroke-width="3"
              fill="none"
              stroke-dasharray="5,5"
              class="pointer-events-none"
            />
            
            <!-- 已连接的线 -->
            <g v-for="connection in connections" :key="`${connection.id}-${viewport.zoom}`">
              <path
                :d="getConnectionPath(connection)"
                stroke="#10b981"
                stroke-width="3"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
                :class="{ 'stroke-red-500': isConnectionSelected(connection.id) }"
                class="pointer-events-none"
              />
            </g>
          </g>
        </svg>

        <!-- 节点层 -->
        <div
          class="absolute inset-0"
          :style="{ transform: `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`, transformOrigin: '0 0', zIndex: 2 }"
        >
          <NodeItem
            v-for="node in nodes"
            :key="node.id"
            :ref="el => setNodeRef(el, node.id)"
            :node="node"
            :is-selected="isNodeSelected(node.id)"
            :zoom="viewport.zoom"
            @update:position="handleNodePositionUpdate(node.id, $event)"
            @port-mousedown="(e, portType, portId) => handlePortMouseDown(e, node.id, portType, portId)"
            @select="handleNodeSelect(node.id)"
            @context-menu="handleNodeContextMenu($event, node.id)"
            @update:config="handleNodeConfigUpdate(node.id, $event)"
          />
        </div>

        <!-- 右键菜单 -->
        <div
          v-if="contextMenu.show"
          class="fixed bg-white border border-gray-200 rounded shadow-lg py-1 z-50"
          :style="{
            left: `${contextMenu.x}px`,
            top: `${contextMenu.y}px`
          }"
          @click.stop
        >
          <button
            v-if="contextMenu.nodeId"
            @click.stop="handleDeleteNode"
            class="w-full px-4 py-2 text-left hover:bg-gray-100 text-red-600"
          >
            删除节点
          </button>
          <button
            v-if="contextMenu.connectionId"
            @click.stop="handleDeleteConnection"
            class="w-full px-4 py-2 text-left hover:bg-gray-100 text-red-600"
          >
            删除连线
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import NodeItem from './NodeItem.vue'
import { NodeExecutorEngine } from './executor'
import { nodeRegistry } from './nodeRegistry'
import type { NodeData, Connection, NodeDefinition } from './types'

// 调试：确保组件加载
console.log('NodeEditor component loaded')
console.log('NodeRegistry nodes:', nodeRegistry.getAll().length)

// 状态
const canvasRef = ref<HTMLElement>()
const nodeRefs = new Map<string, any>()
const nodes = ref<NodeData[]>([])
const connections = ref<Connection[]>([])
const selectedNodes = ref<string[]>([])
const selectedConnections = ref<string[]>([])
const viewport = ref({ x: 0, y: 0, zoom: 1 })
const showNodePalette = ref(true)
const isRunning = ref(false)
const isPaused = ref(false)
const autoCalculate = ref(true) // 运行中自动计算

// 连线相关
const tempConnection = ref<{
  startX: number
  startY: number
  endX: number
  endY: number
  sourceNodeId?: string
  sourcePortId?: string
  portType?: 'input' | 'output'
} | null>(null)

const connectingPort = ref<{
  nodeId: string
  portId: string
  portType: 'input' | 'output'
} | null>(null)

// 右键菜单
const contextMenu = ref<{
  show: boolean
  x: number
  y: number
  nodeId?: string
  connectionId?: string
}>({
  show: false,
  x: 0,
  y: 0
})

// 画布拖拽
let isPanning = false
let panStart = { x: 0, y: 0 }

// 执行引擎
const executor = new NodeExecutorEngine()

// 计算属性
const nodeCategories = computed(() => {
  const categories = new Set<string>()
  nodeRegistry.getAll().forEach(node => {
    categories.add(node.category || '其他')
  })
  return Array.from(categories).sort()
})

// 方法
const setNodeRef = (el: any, nodeId: string) => {
  if (el) {
    nodeRefs.set(nodeId, el)
  } else {
    nodeRefs.delete(nodeId)
  }
}

const getNodesByCategory = (category: string) => {
  return nodeRegistry.getByCategory(category)
}

// 获取端口在画布上的实际位置
const getPortPosition = (nodeId: string, portId: string, portType: 'input' | 'output') => {
  const nodeRef = nodeRefs.get(nodeId)
  const node = nodes.value.find(n => n.id === nodeId)
  
  if (!nodeRef || !node) {
    console.warn('Node ref or node not found:', { nodeId, nodeRef: !!nodeRef, node: !!node })
    return null
  }
  
  try {
    const position = portType === 'input' 
      ? nodeRef.getInputPortPosition?.(portId)
      : nodeRef.getOutputPortPosition?.(portId)
    
    if (position && position.x !== undefined && position.y !== undefined) {
      console.log('Got port position from ref:', { nodeId, portId, portType, position })
      return {
        x: position.x,
        y: position.y
      }
    } else {
      console.warn('Port position method returned invalid value:', position)
    }
  } catch (e) {
    console.error('Error getting port position:', e)
  }
  
  // 回退方案：使用节点位置估算
  console.log('Using fallback port position calculation')
  const nodeWidth = 150
  const portIndex = portType === 'input' 
    ? (node.inputs?.findIndex(p => p.id === portId) ?? -1)
    : (node.outputs?.findIndex(p => p.id === portId) ?? -1)
  const portOffset = portIndex >= 0 ? 40 + portIndex * 32 : 40 // 每个端口大约32px间距，第一个在40px
  
  const fallbackPos = {
    x: portType === 'input' ? node.position.x : node.position.x + nodeWidth,
    y: node.position.y + portOffset
  }
  
  console.log('Fallback port position:', { nodeId, portId, portType, portIndex, fallbackPos })
  return fallbackPos
}

const generateNodeId = () => {
  return `node_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

const generateConnectionId = () => {
  return `conn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// 节点操作
const handleDragStart = (e: DragEvent, nodeDef: NodeDefinition) => {
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'copy'
    e.dataTransfer.setData('nodeType', nodeDef.type)
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  const nodeType = e.dataTransfer?.getData('nodeType')
  if (!nodeType || !canvasRef.value) return

  const definition = nodeRegistry.get(nodeType)
  if (!definition) return

  const rect = canvasRef.value.getBoundingClientRect()
  const x = (e.clientX - rect.left - viewport.value.x) / viewport.value.zoom
  const y = (e.clientY - rect.top - viewport.value.y) / viewport.value.zoom

  const newNode: NodeData = {
    id: generateNodeId(),
    type: nodeType,
    title: definition.title,
    position: { x, y },
    inputs: definition.inputs.map(port => ({ ...port })),
    outputs: definition.outputs.map(port => ({ ...port })),
    config: { ...definition.defaultConfig }
  }

  nodes.value.push(newNode)
}

const handleNodePositionUpdate = (nodeId: string, position: { x: number; y: number }) => {
  const node = nodes.value.find(n => n.id === nodeId)
  if (node) {
    node.position = position
  }
}

const handleNodeConfigUpdate = (nodeId: string, config: Record<string, any>) => {
  const node = nodes.value.find(n => n.id === nodeId)
  if (node) {
    node.config = { ...node.config, ...config }
    console.log('Node config updated:', nodeId, node.config)
    
    // 如果正在运行且启用自动计算，则重新计算
    if (isRunning.value && autoCalculate.value && !isPaused.value) {
      debouncedRecalculate()
    }
  }
}

// 防抖重新计算
let recalculateTimer: number | null = null
const debouncedRecalculate = () => {
  if (recalculateTimer) {
    clearTimeout(recalculateTimer)
  }
  recalculateTimer = window.setTimeout(() => {
    recalculateNodes()
  }, 300) // 300ms 防抖
}

// 重新计算节点（现在使用持续运行模式，这个函数保留用于防抖触发）
const recalculateNodes = async () => {
  if (!isRunning.value || isPaused.value) return
  
  // 直接执行一次
  await executeOnce()
}

const handleNodeSelect = (nodeId: string) => {
  if (!selectedNodes.value.includes(nodeId)) {
    selectedNodes.value = [nodeId]
  }
}

const isNodeSelected = (nodeId: string) => {
  return selectedNodes.value.includes(nodeId)
}

// 连线操作
const handlePortMouseDown = (
  e: MouseEvent,
  nodeId: string,
  portType: 'input' | 'output',
  portId: string
) => {
  e.stopPropagation()
  e.preventDefault()
  
  console.log('=== Port mouse down ===', { nodeId, portType, portId })
  
  // 只允许从输出端口开始连线
  if (portType === 'input') {
    console.log('⚠️ Cannot start connection from input port. Please start from output port (green).')
    return
  }
  
  if (!canvasRef.value) {
    console.error('Canvas ref not available')
    return
  }
  
  // 获取端口实际位置
  const portPos = getPortPosition(nodeId, portId, portType)
  console.log('Port position:', portPos)
  
  if (!portPos) {
    console.error('Failed to get port position, using fallback')
    // 使用节点位置作为回退
    const node = nodes.value.find(n => n.id === nodeId)
    if (!node) {
      console.error('Node not found:', nodeId)
      return
    }
    const startX = node.position.x + 150 // 输出端口在右侧
    const startY = node.position.y + 50
    
    connectingPort.value = { nodeId, portId, portType }
    tempConnection.value = {
      startX,
      startY,
      endX: startX,
      endY: startY,
      sourceNodeId: nodeId,
      sourcePortId: portId,
      portType: 'output'
    }
  } else {
    const startX = portPos.x
    const startY = portPos.y

    connectingPort.value = { nodeId, portId, portType: 'output' }
    tempConnection.value = {
      startX,
      startY,
      endX: startX,
      endY: startY,
      sourceNodeId: nodeId,
      sourcePortId: portId,
      portType: 'output'
    }
  }

  console.log('✅ Starting connection from output port:', tempConnection.value)

  document.addEventListener('mousemove', handleConnectionMouseMove, { passive: true })
  document.addEventListener('mouseup', handleConnectionMouseUp)
}

const handleConnectionMouseMove = (e: MouseEvent) => {
  if (!tempConnection.value || !canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  // 计算鼠标在画布坐标系中的位置（考虑视口偏移和缩放）
  const mouseX = (e.clientX - rect.left - viewport.value.x) / viewport.value.zoom
  const mouseY = (e.clientY - rect.top - viewport.value.y) / viewport.value.zoom
  
  tempConnection.value.endX = mouseX
  tempConnection.value.endY = mouseY
}

const handleConnectionMouseUp = (e: MouseEvent) => {
  console.log('=== Connection mouse up ===', { 
    hasTempConnection: !!tempConnection.value,
    hasConnectingPort: !!connectingPort.value,
    mouseX: e.clientX,
    mouseY: e.clientY
  })
  
  if (!tempConnection.value || !connectingPort.value || !canvasRef.value) {
    console.log('Cleaning up - missing data')
    cleanupConnection()
    return
  }

  // 查找鼠标下的所有元素
  const elements = document.elementsFromPoint(e.clientX, e.clientY)
  console.log('Elements at point:', elements.map(el => ({
    tag: el.tagName,
    class: el.className,
    dataset: (el as HTMLElement).dataset
  })))

  // 查找端口元素
  let portElement: HTMLElement | null = null
  for (const el of elements) {
    if (el.hasAttribute('data-port-id')) {
      portElement = el as HTMLElement
      break
    }
    const closest = (el as HTMLElement).closest?.('[data-port-id]')
    if (closest) {
      portElement = closest as HTMLElement
      break
    }
  }

  console.log('Port element found:', portElement, portElement?.dataset)

  if (portElement) {
    const targetNodeId = portElement.dataset.nodeId
    const targetPortId = portElement.dataset.portId
    // 从 data-port-type 或通过查找节点来确定端口类型
    let targetPortType: 'input' | 'output' = 'input'
    
    // 尝试从元素位置判断（左侧是输入，右侧是输出）
    const nodeElement = portElement.closest('.node-item')
    if (nodeElement) {
      const portRect = portElement.getBoundingClientRect()
      const nodeRect = nodeElement.getBoundingClientRect()
      const relativeX = portRect.left - nodeRect.left
      const nodeWidth = nodeRect.width
      targetPortType = relativeX < nodeWidth / 2 ? 'input' : 'output'
    }
    
    console.log('Target port:', { targetNodeId, targetPortId, targetPortType })

      // 验证连接有效性
      if (targetNodeId && targetPortId) {
        // 不能连接到同一个端口（同一个节点的同一个端口）
        if (targetNodeId === connectingPort.value.nodeId && 
            targetPortId === connectingPort.value.portId) {
          console.log('❌ Cannot connect to same port')
          cleanupConnection()
          return
        }

        // 输出只能连接到输入
        if (targetPortType !== 'input') {
          console.log('❌ Can only connect output to input port. Target is:', targetPortType)
          cleanupConnection()
          return
        }

        // 检查是否已经存在相同的连接
        const existing = connections.value.find(
          conn => conn.sourceNodeId === connectingPort.value!.nodeId && 
                  conn.sourcePortId === connectingPort.value!.portId &&
                  conn.targetNodeId === targetNodeId && 
                  conn.targetPortId === targetPortId
        )
        
        if (existing) {
          console.log('⚠️ Connection already exists')
          cleanupConnection()
          return
        }

        // 检查目标输入端口是否已经被连接（一个输入端口只能有一个连接）
        const targetInputAlreadyConnected = connections.value.find(
          conn => conn.targetNodeId === targetNodeId && 
                  conn.targetPortId === targetPortId
        )
        
        if (targetInputAlreadyConnected) {
          console.log('⚠️ Target input port already has a connection. Removing old connection.')
          // 移除旧连接
          const index = connections.value.findIndex(
            conn => conn.id === targetInputAlreadyConnected.id
          )
          if (index > -1) {
            connections.value.splice(index, 1)
          }
        }

        // 创建新连接：输出 -> 输入
        const newConnection: Connection = {
          id: generateConnectionId(),
          sourceNodeId: connectingPort.value.nodeId,
          sourcePortId: connectingPort.value.portId,
          targetNodeId: targetNodeId,
          targetPortId: targetPortId
        }
        connections.value.push(newConnection)
        console.log('✅ Connection created:', newConnection)
        console.log('Total connections:', connections.value.length)
      } else {
        console.log('❌ Missing target node or port ID')
      }
  } else {
    console.log('❌ No port element found at drop point')
  }

  cleanupConnection()
}

const cleanupConnection = () => {
  tempConnection.value = null
  connectingPort.value = null
  document.removeEventListener('mousemove', handleConnectionMouseMove)
  document.removeEventListener('mouseup', handleConnectionMouseUp)
}

// 获取连线路径
const getConnectionPath = (connection: Connection): string => {
  const sourcePos = getPortPosition(connection.sourceNodeId, connection.sourcePortId, 'output')
  const targetPos = getPortPosition(connection.targetNodeId, connection.targetPortId, 'input')
  
  if (!sourcePos || !targetPos) {
    // 回退方案
    const sourceNode = nodes.value.find(n => n.id === connection.sourceNodeId)
    const targetNode = nodes.value.find(n => n.id === connection.targetNodeId)
    if (!sourceNode || !targetNode) {
      return ''
    }
    
    // 估算端口位置
    const x1 = sourceNode.position.x + 150 // 输出端口在右侧
    const y1 = sourceNode.position.y + 40 // 第一个端口大约在顶部40px
    const x2 = targetNode.position.x // 输入端口在左侧
    const y2 = targetNode.position.y + 40
    
    const dx = x2 - x1
    const cp1x = x1 + Math.max(50, Math.abs(dx) * 0.5)
    const cp1y = y1
    const cp2x = x2 - Math.max(50, Math.abs(dx) * 0.5)
    const cp2y = y2
    
    return `M ${x1} ${y1} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${x2} ${y2}`
  }

  const x1 = sourcePos.x
  const y1 = sourcePos.y
  const x2 = targetPos.x
  const y2 = targetPos.y

  const dx = x2 - x1
  const cp1x = x1 + Math.max(50, Math.abs(dx) * 0.5)
  const cp1y = y1
  const cp2x = x2 - Math.max(50, Math.abs(dx) * 0.5)
  const cp2y = y2

  return `M ${x1} ${y1} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${x2} ${y2}`
}

const getTempConnectionPath = (): string => {
  if (!tempConnection.value) return ''
  
  const { startX, startY, endX, endY } = tempConnection.value
  const dx = endX - startX
  const dy = endY - startY
  const cp1x = startX + dx * 0.5
  const cp1y = startY
  const cp2x = endX - dx * 0.5
  const cp2y = endY

  return `M ${startX} ${startY} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${endX} ${endY}`
}

// 画布操作
const handleCanvasMouseDown = (e: MouseEvent) => {
  if (e.button === 1 || (e.button === 0 && e.ctrlKey)) {
    // 中键或 Ctrl+左键：平移
    isPanning = true
    panStart = { x: e.clientX - viewport.value.x, y: e.clientY - viewport.value.y }
    e.preventDefault()
  } else if (e.button === 0) {
    // 左键：取消选择
    selectedNodes.value = []
    selectedConnections.value = []
    contextMenu.value.show = false
  }
}

const handleCanvasMouseMove = (e: MouseEvent) => {
  if (isPanning) {
    viewport.value.x = e.clientX - panStart.x
    viewport.value.y = e.clientY - panStart.y
  }
}

const handleCanvasMouseUp = () => {
  isPanning = false
}

const handleWheel = (e: WheelEvent) => {
  if (e.ctrlKey || e.metaKey) {
    e.preventDefault()
    const delta = e.deltaY > 0 ? -0.1 : 0.1
    viewport.value.zoom = Math.max(0.5, Math.min(2, viewport.value.zoom + delta))
    // 强制触发响应式更新，确保连线重新计算
    nextTick(() => {
      // 连线路径会在 nextTick 后自动重新计算
    })
  }
}

const resetViewport = () => {
  viewport.value = { x: 0, y: 0, zoom: 1 }
}

// 执行一次所有节点
const executeOnce = async () => {
  // 更新执行引擎
  executor.setNodes(nodes.value)
  executor.setConnections(connections.value)
  
  // 重置节点状态
  nodes.value.forEach(node => {
    if (!node.data) node.data = {}
    node.data.status = 'running'
  })
  
  try {
    const results = await executor.executeAll()
    
    // 更新节点状态和结果
    results.forEach((result, nodeId) => {
      const node = nodes.value.find(n => n.id === nodeId)
      if (node) {
        if (!node.data) node.data = {}
        if (result.success) {
          node.data.status = 'success'
          node.data.outputs = result.outputs
        } else {
          node.data.status = 'error'
          node.data.error = result.error
        }
      }
    })
  } catch (error) {
    console.error('执行失败:', error)
  }
}

// 执行（持续运行模式）
const handleRun = async () => {
  // 如果已暂停，恢复执行
  if (isPaused.value) {
    executor.resume()
    isPaused.value = false
    // 继续执行
    executeOnce()
    return
  }
  
  // 如果正在运行且未暂停，不执行
  if (isRunning.value) {
    return
  }
  
  // 立即更新状态，显示暂停按钮
  isRunning.value = true
  isPaused.value = false
  
  // 强制触发响应式更新，确保 UI 先更新
  await nextTick()
  
  // 立即执行一次
  await executeOnce()
  
  // 持续运行模式：监听变化并自动重新计算
  // 这个循环会一直运行，直到用户点击停止或暂停
  const runLoop = async () => {
    while (isRunning.value && !isPaused.value) {
      // 等待一小段时间，避免过于频繁的计算
      await new Promise(resolve => setTimeout(resolve, 100))
      
      // 如果启用了自动计算，检查是否有变化并重新计算
      if (autoCalculate.value && isRunning.value && !isPaused.value) {
        await executeOnce()
      }
    }
  }
  
  // 启动持续运行循环（不阻塞）
  runLoop().catch(error => {
    console.error('运行循环错误:', error)
    isRunning.value = false
  })
}


// 暂停执行
const handlePause = () => {
  if (isPaused.value) {
    // 继续执行
    executor.resume()
    isPaused.value = false
    // 继续执行一次
    executeOnce()
  } else {
    // 暂停执行
    executor.pause()
    isPaused.value = true
  }
}

// 停止执行
const handleStop = () => {
  isRunning.value = false
  isPaused.value = false
  executor.resume() // 确保恢复，以便下次运行
}

const handleClear = () => {
  if (confirm('确定要清空所有节点和连线吗？')) {
    nodes.value = []
    connections.value = []
    selectedNodes.value = []
    selectedConnections.value = []
  }
}

// 右键菜单
const handleNodeContextMenu = (e: MouseEvent, nodeId: string) => {
  e.preventDefault()
  contextMenu.value = {
    show: true,
    x: e.clientX,
    y: e.clientY,
    nodeId
  }
}

const handleConnectionClick = (connectionId: string) => {
  selectedConnections.value = [connectionId]
  contextMenu.value = {
    show: true,
    x: 0,
    y: 0,
    connectionId
  }
}

const isConnectionSelected = (connectionId: string) => {
  return selectedConnections.value.includes(connectionId)
}

const handleDeleteNode = () => {
  console.log('Delete node called, contextMenu:', contextMenu.value)
  if (contextMenu.value.nodeId) {
    const nodeId = contextMenu.value.nodeId
    console.log('Deleting node:', nodeId)
    
    // 删除节点
    const beforeCount = nodes.value.length
    nodes.value = nodes.value.filter(n => n.id !== nodeId)
    const afterCount = nodes.value.length
    console.log(`Nodes: ${beforeCount} -> ${afterCount}`)
    
    // 删除相关连线
    const beforeConnCount = connections.value.length
    connections.value = connections.value.filter(
      conn => conn.sourceNodeId !== nodeId && conn.targetNodeId !== nodeId
    )
    const afterConnCount = connections.value.length
    console.log(`Connections: ${beforeConnCount} -> ${afterConnCount}`)
    
    // 清除选中状态
    selectedNodes.value = selectedNodes.value.filter(id => id !== nodeId)
    
    // 关闭菜单
    contextMenu.value = {
      show: false,
      x: 0,
      y: 0
    }
    
    console.log('Node deleted successfully')
  } else {
    console.warn('No nodeId in contextMenu')
  }
}

const handleDeleteConnection = () => {
  console.log('Delete connection called, contextMenu:', contextMenu.value)
  if (contextMenu.value.connectionId) {
    const connectionId = contextMenu.value.connectionId
    console.log('Deleting connection:', connectionId)
    
    const beforeCount = connections.value.length
    connections.value = connections.value.filter(
      conn => conn.id !== connectionId
    )
    const afterCount = connections.value.length
    console.log(`Connections: ${beforeCount} -> ${afterCount}`)
    
    // 清除选中状态
    selectedConnections.value = selectedConnections.value.filter(id => id !== connectionId)
    
    // 关闭菜单
    contextMenu.value = {
      show: false,
      x: 0,
      y: 0
    }
    
    console.log('Connection deleted successfully')
  } else {
    console.warn('No connectionId in contextMenu')
  }
}

// 点击外部关闭菜单
const handleClickOutside = (e: MouseEvent) => {
  // 检查点击是否在菜单内部
  const menuElement = (e.target as HTMLElement)?.closest('.fixed')
  if (contextMenu.value.show && !menuElement) {
    contextMenu.value.show = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  cleanupConnection()
})
</script>

<style scoped>
.node-editor {
  user-select: none;
}
</style>

