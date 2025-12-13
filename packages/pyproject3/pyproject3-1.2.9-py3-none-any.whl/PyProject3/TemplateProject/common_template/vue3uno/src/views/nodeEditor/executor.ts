// 节点执行引擎

import type { NodeData, Connection, ExecutionContext, NodeExecutor } from './types'
import { nodeRegistry } from './nodeRegistry'

export interface ExecutionResult {
    nodeId: string
    success: boolean
    outputs?: Record<string, any>
    error?: string
    duration?: number
}

export class NodeExecutorEngine {
    private nodes: Map<string, NodeData> = new Map()
    private connections: Connection[] = []
    private executionCache: Map<string, any> = new Map()
    private executionOrder: string[] = []
    private isPaused: boolean = false
    private pauseResolve: (() => void) | null = null

    // 设置节点和连接
    setNodes(nodes: NodeData[]) {
        this.nodes.clear()
        nodes.forEach(node => {
            this.nodes.set(node.id, node)
        })
    }

    setConnections(connections: Connection[]) {
        this.connections = connections
    }

    // 计算执行顺序（拓扑排序）
    private calculateExecutionOrder(): string[] {
        const order: string[] = []
        const visited = new Set<string>()
        const visiting = new Set<string>()

        const visit = (nodeId: string) => {
            if (visiting.has(nodeId)) {
                throw new Error(`检测到循环依赖: ${nodeId}`)
            }
            if (visited.has(nodeId)) {
                return
            }

            visiting.add(nodeId)

            // 找到所有依赖的节点（连接到输入的节点）
            const node = this.nodes.get(nodeId)
            if (node) {
                const dependencies = this.connections
                    .filter(conn => node.inputs.some(input => input.id === conn.targetPortId))
                    .map(conn => conn.sourceNodeId)

                dependencies.forEach(depId => visit(depId))
            }

            visiting.delete(nodeId)
            visited.add(nodeId)
            order.push(nodeId)
        }

        // 从所有节点开始遍历
        this.nodes.forEach((_, nodeId) => {
            if (!visited.has(nodeId)) {
                visit(nodeId)
            }
        })

        return order
    }

    // 获取节点的输入值
    private getNodeInputs(nodeId: string): Record<string, any> {
        const node = this.nodes.get(nodeId)
        if (!node) return {}

        const inputs: Record<string, any> = {}

        node.inputs.forEach(input => {
            // 查找连接到该输入的连接
            const connection = this.connections.find(
                conn => conn.targetNodeId === nodeId && conn.targetPortId === input.id
            )

            if (connection) {
                // 从源节点的输出获取值
                const sourceOutputs = this.executionCache.get(connection.sourceNodeId)
                if (sourceOutputs && sourceOutputs[connection.sourcePortId] !== undefined) {
                    inputs[input.id] = sourceOutputs[connection.sourcePortId]
                }
            } else {
                // 没有连接，使用节点配置中的默认值
                inputs[input.id] = node.config?.[input.id] ?? null
            }
        })

        return inputs
    }

    // 执行单个节点
    private async executeNode(nodeId: string): Promise<ExecutionResult> {
        const node = this.nodes.get(nodeId)
        if (!node) {
            return {
                nodeId,
                success: false,
                error: '节点不存在'
            }
        }

        const definition = nodeRegistry.get(node.type)
        if (!definition) {
            return {
                nodeId,
                success: false,
                error: `未找到节点类型定义: ${node.type}`
            }
        }

        const startTime = Date.now()

        try {
            // 检查是否需要暂停
            await this.checkPause()

            // 获取输入值
            const inputs = this.getNodeInputs(nodeId)

            // 创建执行上下文
            const context: ExecutionContext = {
                inputs,
                outputs: {},
                config: node.config
            }

            // 执行节点
            const result = await definition.executor(context)

            // 处理结果
            const outputs: Record<string, any> = {}

            if (result && typeof result === 'object') {
                // 如果返回对象，直接使用
                Object.assign(outputs, result)
            } else {
                // 如果返回单个值，分配给第一个输出端口
                if (node.outputs.length > 0) {
                    outputs[node.outputs[0].id] = result
                }
            }

            // 缓存输出
            this.executionCache.set(nodeId, outputs)

            const duration = Date.now() - startTime

            return {
                nodeId,
                success: true,
                outputs,
                duration
            }
        } catch (error) {
            const duration = Date.now() - startTime
            return {
                nodeId,
                success: false,
                error: error instanceof Error ? error.message : String(error),
                duration
            }
        }
    }

    // 暂停执行
    pause() {
        this.isPaused = true
    }

    // 恢复执行
    resume() {
        this.isPaused = false
        if (this.pauseResolve) {
            this.pauseResolve()
            this.pauseResolve = null
        }
    }

    // 检查是否暂停
    async checkPause() {
        if (this.isPaused) {
            return new Promise<void>((resolve) => {
                this.pauseResolve = resolve
            })
        }
    }

    // 执行所有节点
    async executeAll(): Promise<Map<string, ExecutionResult>> {
        // 如果未暂停，重新计算执行顺序并清空缓存
        if (!this.isPaused) {
            this.executionCache.clear()
            this.executionOrder = this.calculateExecutionOrder()
        }

        const results = new Map<string, ExecutionResult>()

        // 执行所有节点
        for (const nodeId of this.executionOrder) {
            // 检查是否需要暂停（在每个节点执行前检查）
            await this.checkPause()

            // 如果暂停了，跳出循环
            if (this.isPaused) {
                console.log('执行已暂停')
                break
            }

            console.log('执行节点:', nodeId)
            const result = await this.executeNode(nodeId)
            results.set(nodeId, result)

            // 在每个节点执行后也检查暂停
            await this.checkPause()
            if (this.isPaused) {
                console.log('执行已暂停（节点执行后）')
                break
            }
        }

        return results
    }

    // 执行单个节点（包括依赖）
    async executeNodeWithDependencies(nodeId: string): Promise<Map<string, ExecutionResult>> {
        this.executionCache.clear()

        // 找到所有依赖节点
        const dependencies = new Set<string>()
        const visit = (id: string) => {
            if (dependencies.has(id)) return
            dependencies.add(id)

            const node = this.nodes.get(id)
            if (node) {
                this.connections
                    .filter(conn => node.inputs.some(input => input.id === conn.targetPortId))
                    .forEach(conn => visit(conn.sourceNodeId))
            }
        }

        visit(nodeId)

        // 计算执行顺序
        this.executionOrder = this.calculateExecutionOrder()
            .filter(id => dependencies.has(id) || id === nodeId)

        const results = new Map<string, ExecutionResult>()

        for (const id of this.executionOrder) {
            const result = await this.executeNode(id)
            results.set(id, result)
        }

        return results
    }

    // 获取执行顺序
    getExecutionOrder(): string[] {
        return [...this.executionOrder]
    }

    // 清除缓存
    clearCache() {
        this.executionCache.clear()
    }
}

