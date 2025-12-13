<template>
  <div class="rete-editor-container" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; width: 100vw; height: 100vh; z-index: 1000; display: flex; flex-direction: column; background-color: #f3f4f6;">
    <!-- 工具栏 -->
    <div class="bg-white border-b border-gray-200 px-4 py-2 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-4">
        <h1 class="text-xl font-bold text-gray-800">Rete.js 节点编辑器</h1>
        <div class="flex gap-2">
          <button
            @click="handleClear"
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
          >
            清空
          </button>
          <button
            @click="handleExport"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            导出
          </button>
          <button
            @click="handleImport"
            class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
          >
            导入
          </button>
        </div>
      </div>
    </div>

    <!-- 节点面板 -->
    <div class="flex flex-1 overflow-hidden">
      <div class="w-64 bg-white border-r border-gray-200 overflow-y-auto p-4">
        <h2 class="text-lg font-semibold mb-4">节点库</h2>
        <div class="space-y-2">
          <div
            v-for="nodeType in nodeTypes"
            :key="nodeType"
            class="p-3 bg-gray-50 rounded cursor-move hover:bg-gray-100 border border-gray-200 mb-2 transition-colors"
            draggable="true"
            @dragstart="handleDragStart($event, nodeType)"
            @dragend="handleDragEnd"
          >
            <div class="font-medium text-sm text-gray-800">{{ getNodeTypeLabel(nodeType) }}</div>
          </div>
        </div>
      </div>

      <!-- 编辑器画布 -->
      <div 
        class="flex-1 relative overflow-hidden"
        style="background-image: linear-gradient(to right, #6b7280 1px, transparent 1px), linear-gradient(to bottom, #6b7280 1px, transparent 1px); background-size: 50px 50px; background-color: #ffffff;"
        @dragover.prevent="handleDragOver"
        @drop.prevent="handleCanvasDrop"
        @dragenter.prevent
      >
        <div ref="editorContainer" class="w-full h-full" style="background-image: linear-gradient(to right, #6b7280 1px, transparent 1px), linear-gradient(to bottom, #6b7280 1px, transparent 1px); background-size: 50px 50px; background-color: #ffffff;"></div>
        <!-- 拖拽提示 -->
        <div 
          v-if="isDragging"
          class="absolute inset-0 flex items-center justify-center pointer-events-none z-50"
        >
          <div class="bg-blue-500 bg-opacity-20 border-2 border-dashed border-blue-500 rounded-lg p-8">
            <p class="text-blue-600 text-lg font-semibold">释放鼠标以添加节点</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
// @ts-ignore
import { NodeEditor, ClassicPreset } from 'rete'
// @ts-ignore
import { VuePlugin, Presets as VuePresets } from 'rete-vue-plugin'
// @ts-ignore
import { ConnectionPlugin, Presets as ConnectionPresets } from 'rete-connection-plugin'
// @ts-ignore
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin'

// 节点类型
const nodeTypes = ['Number', 'Add', 'Multiply', 'Result']

// 编辑器容器引用
const editorContainer = ref<HTMLElement>()

// 拖拽状态
const isDragging = ref(false)

// 初始化状态
const isInitialized = ref(false)

// Rete 编辑器实例
let editor: any = null
let area: any = null
let render: any = null
let preset: any = null

// 获取节点类型标签
const getNodeTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    'Number': '数字',
    'Add': '加法',
    'Multiply': '乘法',
    'Result': '结果'
  }
  return labels[type] || type
}

// Socket 定义（延迟初始化，在 preset 准备好后）
let socket: any = null

// 创建数字节点
const createNumberNode = (preset: any, socketInstance: any) => {
  const node = new preset.Node('Number')
  const out = new preset.Output(socketInstance, 'Number')
  const control = new preset.InputControl('number', { 
    initial: 0,
    change: () => node.update()
  })
  
  node.addOutput('value', out)
  node.addControl('num', control)
  node.label = '数字'
  return node
}

// 创建加法节点
const createAddNode = (preset: any, socketInstance: any) => {
  const node = new preset.Node('Add')
  const in1 = new preset.Input(socketInstance, 'A')
  const in2 = new preset.Input(socketInstance, 'B')
  const out = new preset.Output(socketInstance, 'Sum')
  
  node.addInput('a', in1)
  node.addInput('b', in2)
  node.addOutput('value', out)
  node.label = '加法'
  return node
}

// 创建乘法节点
const createMultiplyNode = (preset: any, socketInstance: any) => {
  const node = new preset.Node('Multiply')
  const in1 = new preset.Input(socketInstance, 'A')
  const in2 = new preset.Input(socketInstance, 'B')
  const out = new preset.Output(socketInstance, 'Product')
  
  node.addInput('a', in1)
  node.addInput('b', in2)
  node.addOutput('value', out)
  node.label = '乘法'
  return node
}

// 创建结果节点
const createResultNode = (preset: any, socketInstance: any) => {
  const node = new preset.Node('Result')
  const in1 = new preset.Input(socketInstance, 'Value')
  const control = new preset.InputControl('number', { 
    readonly: true,
    initial: 0
  })
  
  node.addInput('value', in1)
  node.addControl('result', control)
  node.label = '结果'
  return node
}

// 拖拽开始
const handleDragStart = (e: DragEvent, nodeType: string) => {
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'copy'
    e.dataTransfer.setData('nodeType', nodeType)
    isDragging.value = true
  }
}

// 拖拽悬停
const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  if (e.dataTransfer) {
    e.dataTransfer.dropEffect = 'copy'
  }
}

// 初始化编辑器
const initEditor = async () => {
  console.log('开始初始化编辑器，editorContainer:', !!editorContainer.value)
  if (!editorContainer.value) {
    console.error('editorContainer 未准备好')
    return
  }

  try {
    console.log('步骤1: 创建编辑器')
    // 创建编辑器
    editor = new NodeEditor()
    console.log('编辑器创建成功:', !!editor)

    console.log('步骤2: 设置 preset')
    // 使用 ClassicPreset（不需要实例化，直接使用）
    preset = ClassicPreset
    console.log('preset 设置成功:', !!preset)
    
    console.log('步骤3: 初始化 Socket')
    // 初始化 Socket（在 preset 准备好后）
    if (!socket) {
      socket = new ClassicPreset.Socket('socket')
      console.log('Socket 已初始化:', !!socket)
    }

    console.log('步骤4: 创建区域插件')
    // 创建区域插件
    area = new AreaPlugin(editorContainer.value)
    console.log('区域插件创建成功:', !!area)
    
    // 先将 area 添加到 editor（建立父子关系）
    editor.use(area)
    console.log('AreaPlugin 已添加到 editor（建立父子关系）')
    
    console.log('步骤5: 创建 Vue 渲染插件')
    // 创建 VuePlugin 实例（根据官方文档）
    render = new VuePlugin()
    console.log('VuePlugin 实例创建成功:', !!render)
    
    // 添加 classic preset
    render.addPreset(VuePresets.classic.setup())
    console.log('VuePresets.classic 已添加')
    
    // 将 render 添加到 area（在 area 已添加到 editor 之后）
    area.use(render)
    console.log('VuePlugin 已添加到 area')
    
    console.log('步骤6: 添加连接插件')
    // 创建连接插件实例并添加到 area
    const connectionPlugin = new ConnectionPlugin()
    // 添加连接预设
    if (ConnectionPresets && ConnectionPresets.classic) {
      connectionPlugin.addPreset(ConnectionPresets.classic.setup())
      console.log('ConnectionPresets.classic 已添加到连接插件')
    }
    // 将连接插件添加到 area
    area.use(connectionPlugin)
    console.log('ConnectionPlugin 已添加到 area')

    // 配置区域功能
    if (AreaExtensions) {
      if (AreaExtensions.selectableNodes) {
        AreaExtensions.selectableNodes(area, AreaExtensions.selector(), {
          accumulating: AreaExtensions.accumulateOnCtrl()
        })
      }
      if (AreaExtensions.zoomAt) {
        AreaExtensions.zoomAt(area, editor.getNodes())
      }
    }

    // 使用 CSS 背景网格（更可靠的方式）
    if (editorContainer.value) {
      editorContainer.value.style.backgroundImage = `
        linear-gradient(to right, #ccc 1px, transparent 1px),
        linear-gradient(to bottom, #ccc 1px, transparent 1px)
      `
      editorContainer.value.style.backgroundSize = '20px 20px'
      editorContainer.value.style.backgroundColor = '#ffffff'
      console.log('已设置网格背景')
    }
    
    // 也尝试使用 area.use 添加背景（如果支持）
    try {
      const background = () => {
        const grid = document.createElement('canvas')
        const size = 50
        const ctx = grid.getContext('2d')
        if (ctx) {
          grid.width = size * 2
          grid.height = size * 2
          // 使用更深的颜色，提高可见性
          ctx.strokeStyle = '#6b7280'
          ctx.lineWidth = 2
          ctx.beginPath()
          ctx.moveTo(size, 0)
          ctx.lineTo(size, size * 2)
          ctx.moveTo(0, size)
          ctx.lineTo(size * 2, size)
          ctx.stroke()
        }
        return grid
      }
      area.use(background)
      console.log('已使用 area.use 添加背景')
    } catch (error) {
      console.warn('无法使用 area.use 添加背景，使用 CSS 背景:', error)
    }
    
    // 标记初始化完成
    console.log('步骤6: 标记初始化完成')
    isInitialized.value = true
    console.log('✅ 编辑器初始化完成！', { 
      editor: !!editor, 
      area: !!area, 
      preset: !!preset,
      socket: !!socket,
      isInitialized: isInitialized.value
    })
  } catch (error) {
    console.error('❌ 初始化 Rete 编辑器失败:', error)
    console.error('错误详情:', error)
    isInitialized.value = false
    // 即使出错也尝试设置，以便用户知道状态
    const errorMessage = error instanceof Error ? error.message : String(error)
    console.error('错误消息:', errorMessage)
    alert('编辑器初始化失败，请刷新页面重试。错误信息：' + errorMessage)
  }
}

// 处理画布拖拽
const handleCanvasDrop = async (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false
  
  // 检查初始化状态（更宽松的检查）
  const isReady = isInitialized.value && editor && area && preset && socket
  console.log('拖拽检查:', {
    isInitialized: isInitialized.value,
    hasEditor: !!editor,
    hasArea: !!area,
    hasPreset: !!preset,
    hasSocket: !!socket,
    isReady
  })
  
  if (!isReady) {
    console.warn('编辑器尚未初始化完成，当前状态:', {
      isInitialized: isInitialized.value,
      editor: !!editor,
      area: !!area,
      preset: !!preset,
      socket: !!socket
    })
    // 尝试重新初始化（如果可能）
    if (!editor || !area || !preset) {
      alert('编辑器正在初始化，请稍候再试。如果持续出现此问题，请刷新页面。')
      return
    }
    // 如果只是 socket 未初始化，尝试初始化它
    if (!socket && preset) {
      try {
        socket = new ClassicPreset.Socket('socket')
        console.log('延迟初始化 Socket 成功')
      } catch (err) {
        console.error('延迟初始化 Socket 失败:', err)
        alert('编辑器初始化不完整，请刷新页面重试')
        return
      }
    }
  }
  
  const nodeType = e.dataTransfer?.getData('nodeType')
  console.log('Drop event:', { 
    nodeType, 
    hasEditor: !!editor, 
    hasArea: !!area, 
    hasPreset: !!preset,
    isInitialized: isInitialized.value
  })
  
  if (!nodeType) {
    console.warn('Drop failed: no nodeType', { dataTransfer: e.dataTransfer })
    alert('拖拽失败：无法获取节点类型')
    return
  }
  
  if (!editor) {
    console.warn('Drop failed: editor not initialized')
    alert('拖拽失败：编辑器未初始化')
    return
  }
  
  if (!area) {
    console.warn('Drop failed: area not initialized')
    alert('拖拽失败：区域插件未初始化')
    return
  }
  
  if (!preset) {
    console.warn('Drop failed: preset not initialized')
    alert('拖拽失败：预设未初始化')
    return
  }

  const rect = editorContainer.value?.getBoundingClientRect()
  if (!rect) {
    console.warn('Drop failed: no rect')
    return
  }

  // 获取区域变换信息
  const transform = area.area?.transform || { x: 0, y: 0, k: 1 }
  console.log('Transform:', transform)
  
  // 计算画布坐标
  const x = (e.clientX - rect.left - transform.x) / transform.k
  const y = (e.clientY - rect.top - transform.y) / transform.k
  
  console.log('Calculated position:', { x, y, clientX: e.clientX, clientY: e.clientY, rect })

  let node: any

  if (!socket) {
    console.error('Socket 未初始化')
    alert('拖拽失败：Socket 未初始化')
    return
  }

  switch (nodeType) {
    case 'Number':
      node = createNumberNode(preset, socket)
      break
    case 'Add':
      node = createAddNode(preset, socket)
      break
    case 'Multiply':
      node = createMultiplyNode(preset, socket)
      break
    case 'Result':
      node = createResultNode(preset, socket)
      break
    default:
      console.warn('Unknown node type:', nodeType)
      return
  }

  if (!node) {
    console.error('Failed to create node')
    return
  }

  // 设置节点位置
  if ('position' in node) {
    node.position = [x, y]
  } else {
    // 如果节点没有 position 属性，尝试其他方式
    console.warn('Node does not have position property, trying alternative')
  }
  
  console.log('Adding node:', node)
  try {
    await editor.addNode(node)
    console.log('Node added successfully')
    // 添加成功提示
    const nodes = editor.getNodes()
    console.log('Total nodes:', nodes.length)
  } catch (error) {
    console.error('Failed to add node:', error)
    alert('添加节点失败：' + (error as Error).message)
  }
}

// 监听拖拽结束（即使没有成功拖拽也要重置状态）
const handleDragEnd = () => {
  isDragging.value = false
}

// 清空编辑器
const handleClear = () => {
  if (!editor) return
  if (confirm('确定要清空所有节点吗？')) {
    const nodes = editor.getNodes()
    nodes.forEach((node: any) => {
      if (editor && node.id) {
        editor.removeNode(node.id)
      }
    })
  }
}

// 导出
const handleExport = () => {
  if (!editor) return
  try {
    const data = (editor as any).toJSON ? (editor as any).toJSON() : editor
    const json = JSON.stringify(data, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'rete-editor.json'
    a.click()
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败，请查看控制台')
  }
}

// 导入
const handleImport = () => {
  if (!editor) return
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'application/json'
  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0]
    if (!file) return
    try {
      const text = await file.text()
      const data = JSON.parse(text)
      if ((editor as any).fromJSON) {
        await (editor as any).fromJSON(data)
      } else {
        console.warn('编辑器不支持 fromJSON 方法')
      }
    } catch (error) {
      console.error('导入失败:', error)
      alert('导入失败，请查看控制台')
    }
  }
  input.click()
}

// 组件挂载
onMounted(async () => {
  console.log('组件挂载，开始初始化编辑器...')
  try {
    await initEditor()
    // 等待一下确保所有异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100))
    console.log('编辑器初始化完成，isInitialized:', isInitialized.value, {
      editor: !!editor,
      area: !!area,
      preset: !!preset,
      socket: !!socket
    })
    
    if (!isInitialized.value) {
      console.error('警告：编辑器初始化未完成')
    }
  } catch (error) {
    console.error('组件挂载时初始化失败:', error)
    alert('编辑器初始化失败：' + (error as Error).message)
  }
})

// 组件卸载
onUnmounted(() => {
  if (area) {
    area.destroy()
  }
  if (editor) {
    editor.destroy()
  }
})
</script>

<style scoped>
.rete-editor-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 确保编辑器容器有网格背景 */
:deep(.rete-area) {
  background-image: 
    linear-gradient(to right, #9ca3af 1px, transparent 1px),
    linear-gradient(to bottom, #9ca3af 1px, transparent 1px) !important;
  background-size: 50px 50px !important;
  background-color: #ffffff !important;
}

/* 如果编辑器容器本身需要网格 */
.rete-editor-container :deep(> div > div:last-child) {
  background-image: 
    linear-gradient(to right, #9ca3af 1px, transparent 1px),
    linear-gradient(to bottom, #9ca3af 1px, transparent 1px) !important;
  background-size: 20px 20px !important;
  background-color: #ffffff !important;
}

/* 确保 Rete.js 节点文本可见 */
:deep(.rete-node) {
  color: #1f2937 !important;
  background-color: #ffffff !important;
  border: 2px solid #3b82f6 !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

:deep(.rete-node .rete-node-title) {
  color: #1f2937 !important;
  font-weight: 600 !important;
  background-color: #3b82f6 !important;
  color: #ffffff !important;
  padding: 8px 12px !important;
  border-radius: 6px 6px 0 0 !important;
}

:deep(.rete-node .rete-socket) {
  background-color: #3b82f6 !important;
  border: 2px solid #ffffff !important;
}

:deep(.rete-node .rete-control) {
  color: #1f2937 !important;
}

:deep(.rete-node input) {
  color: #1f2937 !important;
  background-color: #ffffff !important;
  border: 1px solid #d1d5db !important;
}

:deep(.rete-connection) {
  stroke: #3b82f6 !important;
  stroke-width: 2px !important;
}
</style>

