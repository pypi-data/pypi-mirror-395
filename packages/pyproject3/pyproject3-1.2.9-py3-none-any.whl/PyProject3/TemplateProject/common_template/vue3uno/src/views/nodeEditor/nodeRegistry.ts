// 节点注册系统 - 可扩展的节点类型管理

import type { NodeDefinition, ExecutionContext } from './types'

class NodeRegistry {
    private nodes: Map<string, NodeDefinition> = new Map()

    // 注册节点类型
    register(definition: NodeDefinition) {
        if (this.nodes.has(definition.type)) {
            console.warn(`节点类型 ${definition.type} 已存在，将被覆盖`)
        }
        this.nodes.set(definition.type, definition)
    }

    // 获取节点定义
    get(type: string): NodeDefinition | undefined {
        return this.nodes.get(type)
    }

    // 获取所有节点类型
    getAll(): NodeDefinition[] {
        return Array.from(this.nodes.values())
    }

    // 按分类获取节点
    getByCategory(category: string): NodeDefinition[] {
        return this.getAll().filter(node => node.category === category)
    }

    // 检查节点类型是否存在
    has(type: string): boolean {
        return this.nodes.has(type)
    }
}

// 创建全局注册表实例
export const nodeRegistry = new NodeRegistry()

// 注册内置节点类型

// 输入节点
nodeRegistry.register({
    type: 'input',
    title: '数据输入',
    description: '输入数据节点',
    category: '基础',
    inputs: [],
    outputs: [
        { id: 'output', label: '输出', type: 'data' }
    ],
    executor: async (context: ExecutionContext) => {
        // 输入节点从配置中获取数据，返回给输出端口
        const value = context.config?.value ?? ''
        return { output: value }
    },
    defaultConfig: {
        value: ''
    }
})

// 输出节点
nodeRegistry.register({
    type: 'output',
    title: '数据输出',
    description: '输出数据节点',
    category: '基础',
    inputs: [
        { id: 'input', label: '输入', type: 'data' }
    ],
    outputs: [],
    executor: async (context: ExecutionContext) => {
        // 输出节点接收输入值并返回（用于显示）
        const inputValue = context.inputs.input
        return { result: inputValue }
    },
    defaultConfig: {}
})

// 加法节点
nodeRegistry.register({
    type: 'add',
    title: '加法',
    description: '两个数字相加',
    category: '数学',
    inputs: [
        { id: 'a', label: '数字 A', type: 'number' },
        { id: 'b', label: '数字 B', type: 'number' }
    ],
    outputs: [
        { id: 'result', label: '结果', type: 'number' }
    ],
    executor: async (context: ExecutionContext) => {
        const a = Number(context.inputs.a) || 0
        const b = Number(context.inputs.b) || 0
        return { result: a + b }
    }
})

// 乘法节点
nodeRegistry.register({
    type: 'multiply',
    title: '乘法',
    description: '两个数字相乘',
    category: '数学',
    inputs: [
        { id: 'a', label: '数字 A', type: 'number' },
        { id: 'b', label: '数字 B', type: 'number' }
    ],
    outputs: [
        { id: 'result', label: '结果', type: 'number' }
    ],
    executor: async (context: ExecutionContext) => {
        const a = Number(context.inputs.a) || 0
        const b = Number(context.inputs.b) || 0
        return { result: a * b }
    }
})

// 字符串连接节点
nodeRegistry.register({
    type: 'concat',
    title: '字符串连接',
    description: '连接两个字符串',
    category: '字符串',
    inputs: [
        { id: 'str1', label: '字符串 1', type: 'string' },
        { id: 'str2', label: '字符串 2', type: 'string' }
    ],
    outputs: [
        { id: 'result', label: '结果', type: 'string' }
    ],
    executor: async (context: ExecutionContext) => {
        const str1 = String(context.inputs.str1 || '')
        const str2 = String(context.inputs.str2 || '')
        return { result: str1 + str2 }
    }
})

// 条件判断节点
nodeRegistry.register({
    type: 'condition',
    title: '条件判断',
    description: '根据条件返回不同值',
    category: '逻辑',
    inputs: [
        { id: 'condition', label: '条件', type: 'boolean' },
        { id: 'trueValue', label: '真值', type: 'data' },
        { id: 'falseValue', label: '假值', type: 'data' }
    ],
    outputs: [
        { id: 'result', label: '结果', type: 'data' }
    ],
    executor: async (context: ExecutionContext) => {
        const condition = Boolean(context.inputs.condition)
        return {
            result: condition ? context.inputs.trueValue : context.inputs.falseValue
        }
    }
})

nodeRegistry.register({
    type: 'select',
    title: '布尔值',
    description: '输入布尔值节点',
    category: '逻辑',
    inputs: [],
    outputs: [
        { id: 'output', label: '输出', type: 'data' }
    ],
    executor: async (context: ExecutionContext) => {
        // 输入节点从配置中获取数据，返回给输出端口
        const value = context.config?.value ?? false
        return { output: value }
    },
    defaultConfig: {
        value: true,
        options: [
            { id: 'true', label: '是' },
            { id: 'false', label: '否' }
        ]
    }
})



// 延迟节点（用于演示异步执行）
nodeRegistry.register({
    type: 'delay',
    title: '延迟',
    description: '延迟执行',
    category: '控制',
    inputs: [
        { id: 'input', label: '输入', type: 'data' },
        { id: 'ms', label: '延迟(ms)', type: 'number' }
    ],
    outputs: [
        { id: 'output', label: '输出', type: 'data' }
    ],
    executor: async (context: ExecutionContext) => {
        const ms = Number(context.inputs.ms) || 1000
        await new Promise(resolve => setTimeout(resolve, ms))
        return { output: context.inputs.input }
    },
    defaultConfig: {
        ms: 1000
    }
})

// Python 风格加法节点
nodeRegistry.register({
    type: 'python_add',
    title: 'Python 加法',
    description: 'Python 风格的数字相加 (a + b)',
    category: 'Python',
    inputs: [
        { id: 'a', label: 'a', type: 'number' },
        { id: 'b', label: 'b', type: 'number' }
    ],
    outputs: [
        { id: 'result', label: 'result', type: 'number' }
    ],
    executor: async (context: ExecutionContext) => {
        // Python 风格的加法：支持多种类型
        const a = context.inputs.a
        const b = context.inputs.b

        // 尝试转换为数字
        const numA = typeof a === 'number' ? a : Number(a) || 0
        const numB = typeof b === 'number' ? b : Number(b) || 0

        // Python 风格的加法运算
        const result = numA + numB

        return { result }
    }
})

// 如果需要执行真正的 Python 代码，可以添加 Python 执行节点
nodeRegistry.register({
    type: 'python_exec',
    title: 'Python 执行',
    description: '执行 Python 代码（需要后端支持）',
    category: 'Python',
    inputs: [
        { id: 'code', label: '代码', type: 'string' },
        { id: 'input_data', label: '输入数据', type: 'data' }
    ],
    outputs: [
        { id: 'result', label: '结果', type: 'data' },
        { id: 'error', label: '错误', type: 'string' }
    ],
    executor: async (context: ExecutionContext) => {
        const code = context.inputs.code || ''
        // const inputData = context.inputs.input_data // 暂时未使用，保留供未来扩展

        // 注意：这里只是示例，实际需要调用后端 Python 执行服务
        // 例如通过 API 调用后端 Python 解释器
        try {
            // 这里应该调用后端 API
            // const response = await fetch('/api/python/execute', {
            //     method: 'POST',
            //     body: JSON.stringify({ code, input_data: inputData })
            // })
            // const result = await response.json()

            // 临时实现：简单的数学表达式计算
            if (code.includes('+')) {
                const parts = code.split('+').map((s: string) => s.trim())
                const a = Number(parts[0]) || 0
                const b = Number(parts[1]) || 0
                return { result: a + b, error: null }
            }

            return { result: null, error: '需要后端 Python 执行支持' }
        } catch (error) {
            return {
                result: null,
                error: error instanceof Error ? error.message : String(error)
            }
        }
    },
    defaultConfig: {
        code: 'a + b'
    }
})

// 正弦波信号源节点
nodeRegistry.register({
    type: 'sine_wave',
    title: '正弦波信号源',
    description: '生成正弦波信号，可调频率和幅度',
    category: '信号',
    inputs: [],
    outputs: [
        { id: 'signal', label: '信号', type: 'array' }
    ],
    executor: async (context: ExecutionContext) => {
        const frequency = Number(context.config?.frequency) || 1 // Hz
        const amplitude = Number(context.config?.amplitude) || 1
        const phase = Number(context.config?.phase) || 0 // 相位角（弧度）
        const sampleRate = Number(context.config?.sampleRate) || 100 // 采样率
        const samples = Number(context.config?.samples) || 100 // 采样点数

        // 生成正弦波数据
        const signal: number[] = []

        for (let i = 0; i < samples; i++) {
            const t = (i / sampleRate) // 时间（秒）
            // 添加相位角：sin(2πft + φ)
            const value = amplitude * Math.sin(2 * Math.PI * frequency * t + phase)
            signal.push(value)
        }

        return { signal }
    },
    defaultConfig: {
        frequency: 1,
        amplitude: 1,
        phase: 0, // 相位角（弧度），默认 0
        sampleRate: 100,
        samples: 100
    }
})

// 信号处理节点
nodeRegistry.register({
    type: 'signal_process',
    title: '信号处理',
    description: '对信号进行处理（滤波、放大等）',
    category: '信号',
    inputs: [
        { id: 'signal', label: '输入信号', type: 'array' }
    ],
    outputs: [
        { id: 'output', label: '处理后信号', type: 'array' }
    ],
    executor: async (context: ExecutionContext) => {
        const inputSignal = context.inputs.signal
        const processType = context.config?.processType || 'amplify'
        const gain = Number(context.config?.gain) || 1

        // 确保输入是数组
        if (!Array.isArray(inputSignal)) {
            return { output: [] }
        }

        const signal = inputSignal as number[]
        let output: number[] = []

        switch (processType) {
            case 'amplify':
                // 放大
                output = signal.map(v => v * gain)
                break
            case 'lowpass':
                // 简单低通滤波（移动平均）
                const windowSize = Math.max(1, Math.floor(Number(context.config?.windowSize) || 3))
                output = []
                for (let i = 0; i < signal.length; i++) {
                    let sum = 0
                    let count = 0
                    for (let j = Math.max(0, i - windowSize); j <= Math.min(signal.length - 1, i + windowSize); j++) {
                        sum += signal[j]
                        count++
                    }
                    output.push(sum / count)
                }
                break
            case 'highpass':
                // 简单高通滤波（减去低通）
                const lowpassWindow = Math.max(1, Math.floor(Number(context.config?.windowSize) || 3))
                const lowpass: number[] = []
                for (let i = 0; i < signal.length; i++) {
                    let sum = 0
                    let count = 0
                    for (let j = Math.max(0, i - lowpassWindow); j <= Math.min(signal.length - 1, i + lowpassWindow); j++) {
                        sum += signal[j]
                        count++
                    }
                    lowpass.push(sum / count)
                }
                output = signal.map((v, i) => v - lowpass[i])
                break
            case 'normalize':
                // 归一化
                const max = Math.max(...signal.map(Math.abs))
                output = max > 0 ? signal.map(v => v / max) : signal
                break
            default:
                output = signal
        }

        return { output }
    },
    defaultConfig: {
        processType: 'amplify',
        gain: 1,
        windowSize: 3
    }
})

// 波形相加节点
nodeRegistry.register({
    type: 'waveform_add',
    title: '波形相加',
    description: '将两个信号波形相加',
    category: '信号',
    inputs: [
        { id: 'signal1', label: '信号1', type: 'array' },
        { id: 'signal2', label: '信号2', type: 'array' }
    ],
    outputs: [
        { id: 'output', label: '相加结果', type: 'array' }
    ],
    executor: async (context: ExecutionContext) => {
        const inputSignal1 = context.inputs.signal1
        const inputSignal2 = context.inputs.signal2

        // 确保输入都是数组
        if (!Array.isArray(inputSignal1) || !Array.isArray(inputSignal2)) {
            console.warn('波形相加节点: 输入信号不是数组', { signal1: inputSignal1, signal2: inputSignal2 })
            return { output: [] }
        }

        const signal1 = inputSignal1 as number[]
        const signal2 = inputSignal2 as number[]

        // 确保所有值都是数字
        const validSignal1 = signal1.filter(v => typeof v === 'number' && !isNaN(v))
        const validSignal2 = signal2.filter(v => typeof v === 'number' && !isNaN(v))

        if (validSignal1.length === 0 || validSignal2.length === 0) {
            console.warn('波形相加节点: 没有有效的数字数据', { signal1: validSignal1, signal2: validSignal2 })
            return { output: [] }
        }

        // 取两个信号中较短的长度
        const minLength = Math.min(validSignal1.length, validSignal2.length)
        const output: number[] = []

        // 逐点相加
        for (let i = 0; i < minLength; i++) {
            const value1 = validSignal1[i] || 0
            const value2 = validSignal2[i] || 0
            output.push(value1 + value2)
        }

        return { output }
    },
    defaultConfig: {}
})

// 波形显示节点
nodeRegistry.register({
    type: 'waveform_display',
    title: '波形显示',
    description: '显示信号波形图',
    category: '信号',
    inputs: [
        { id: 'signal', label: '输入信号', type: 'array' }
    ],
    outputs: [],
    executor: async (context: ExecutionContext) => {
        const inputSignal = context.inputs.signal

        // 调试信息
        console.log('波形显示节点 executor:', {
            inputSignal,
            inputType: typeof inputSignal,
            isArray: Array.isArray(inputSignal),
            inputs: context.inputs
        })

        // 确保输入是数组
        if (!Array.isArray(inputSignal)) {
            console.warn('波形显示节点: 输入信号不是数组', inputSignal)
            return { waveform: [] }
        }

        const signal = inputSignal as number[]

        // 确保所有值都是数字
        const validSignal = signal.filter(v => typeof v === 'number' && !isNaN(v))

        if (validSignal.length === 0) {
            console.warn('波形显示节点: 没有有效的数字数据', signal)
            return { waveform: [] }
        }

        console.log('波形显示节点: 返回波形数据，长度:', validSignal.length)

        // 返回波形数据供显示组件使用
        return { waveform: validSignal }
    },
    defaultConfig: {}
})

// 导出注册函数，方便外部扩展
export function registerNode(definition: NodeDefinition) {
    nodeRegistry.register(definition)
}

