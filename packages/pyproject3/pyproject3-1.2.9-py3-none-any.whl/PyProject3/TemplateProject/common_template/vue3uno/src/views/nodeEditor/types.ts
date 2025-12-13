// 节点编辑器类型定义

// 端口类型
export interface Port {
    id: string
    label: string
    type: string // 数据类型：'data', 'number', 'string', 'boolean' 等
}

// 节点位置
export interface NodePosition {
    x: number
    y: number
}

// 节点数据
export interface NodeData {
    id: string
    type: string // 节点类型：'input', 'process', 'output', 'custom' 等
    title: string
    position: NodePosition
    inputs: Port[]
    outputs: Port[]
    config?: Record<string, any> // 节点配置参数
    data?: Record<string, any> // 节点运行时数据
}

// 连接线
export interface Connection {
    id: string
    sourceNodeId: string
    sourcePortId: string
    targetNodeId: string
    targetPortId: string
}

// 节点执行上下文
export interface ExecutionContext {
    inputs: Record<string, any>
    outputs: Record<string, any>
    config?: Record<string, any>
}

// 节点执行函数类型
export type NodeExecutor = (context: ExecutionContext) => Promise<any> | any

// 节点定义（用于注册新节点）
export interface NodeDefinition {
    type: string
    title: string
    description?: string
    category?: string
    inputs: Port[]
    outputs: Port[]
    executor: NodeExecutor
    defaultConfig?: Record<string, any>
    icon?: string
}

// 编辑器状态
export interface EditorState {
    nodes: NodeData[]
    connections: Connection[]
    selectedNodes: string[]
    selectedConnections: string[]
    viewport: {
        x: number
        y: number
        zoom: number
    }
}

