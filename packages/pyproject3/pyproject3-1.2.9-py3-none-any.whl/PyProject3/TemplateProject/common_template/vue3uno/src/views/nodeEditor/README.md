# 节点编辑器使用指南

## 功能特性

- ✅ 拖拽生成节点
- ✅ 连线连接输入输出
- ✅ 节点执行引擎
- ✅ 可扩展的节点系统
- ✅ 画布平移和缩放
- ✅ 节点选择和管理

## 使用方法

### 1. 访问编辑器

访问路由 `/node-editor` 即可打开节点编辑器。

### 2. 添加节点

1. 点击"添加节点"按钮打开节点面板
2. 从节点面板拖拽节点类型到画布
3. 节点会自动添加到画布上

### 3. 连接节点

1. 点击节点的输出端口（绿色圆点）
2. 拖拽到目标节点的输入端口（蓝色圆点）
3. 释放鼠标完成连接

### 4. 运行节点

1. 点击工具栏的"运行"按钮
2. 系统会按照依赖顺序执行所有节点
3. 节点状态会显示在节点上（运行中/成功/错误）

### 5. 画布操作

- **平移**：中键拖拽或 Ctrl+左键拖拽
- **缩放**：Ctrl+滚轮或使用缩放按钮
- **选择节点**：点击节点
- **删除节点**：右键点击节点选择"删除节点"
- **删除连线**：右键点击连线选择"删除连线"

## 扩展节点

### 注册新节点类型

在 `nodeRegistry.ts` 中使用 `registerNode` 函数注册新节点：

```typescript
import { registerNode } from './nodeRegistry'
import type { NodeDefinition } from './types'

registerNode({
  type: 'my-custom-node',
  title: '我的自定义节点',
  description: '这是一个自定义节点',
  category: '自定义',
  inputs: [
    { id: 'input1', label: '输入1', type: 'string' }
  ],
  outputs: [
    { id: 'output1', label: '输出1', type: 'string' }
  ],
  executor: async (context) => {
    // 执行逻辑
    const input = context.inputs.input1
    return {
      output1: `处理后的: ${input}`
    }
  },
  defaultConfig: {
    someOption: 'default value'
  }
})
```

### 节点执行器

执行器函数接收一个 `ExecutionContext` 参数：

```typescript
interface ExecutionContext {
  inputs: Record<string, any>  // 输入值
  outputs: Record<string, any> // 输出值（初始为空）
  config?: Record<string, any> // 节点配置
}
```

执行器应该返回一个对象，键为输出端口 ID，值为输出值：

```typescript
executor: async (context) => {
  // 访问输入
  const value = context.inputs.input1
  
  // 处理逻辑
  const result = processValue(value)
  
  // 返回输出（键名对应输出端口 ID）
  return {
    output1: result,
    output2: result * 2
  }
}
```

### 节点类型

- **type**: 节点唯一标识符
- **title**: 节点显示名称
- **description**: 节点描述（显示在节点面板）
- **category**: 节点分类（用于分组显示）
- **inputs**: 输入端口数组
- **outputs**: 输出端口数组
- **executor**: 执行函数（必需）
- **defaultConfig**: 默认配置（可选）

### 端口类型

端口可以有不同的数据类型：
- `data`: 通用数据
- `number`: 数字
- `string`: 字符串
- `boolean`: 布尔值
- 自定义类型（用于类型检查）

## 内置节点类型

### 基础节点
- **input**: 数据输入节点
- **output**: 数据输出节点

### 数学节点
- **add**: 加法
- **multiply**: 乘法

### 字符串节点
- **concat**: 字符串连接

### 逻辑节点
- **condition**: 条件判断

### 控制节点
- **delay**: 延迟执行

## 架构说明

### 文件结构

```
nodeEditor/
├── types.ts           # 类型定义
├── nodeRegistry.ts    # 节点注册系统
├── executor.ts        # 执行引擎
├── NodeItem.vue       # 节点组件
├── NodeEditor.vue     # 主编辑器
└── README.md          # 使用文档
```

### 核心概念

1. **节点注册系统** (`nodeRegistry.ts`)
   - 管理所有可用的节点类型
   - 提供注册和查询接口
   - 支持按分类查询

2. **执行引擎** (`executor.ts`)
   - 计算节点执行顺序（拓扑排序）
   - 处理节点依赖关系
   - 执行节点并传递数据

3. **节点组件** (`NodeItem.vue`)
   - 可拖拽的节点UI
   - 端口连接点
   - 状态显示

4. **主编辑器** (`NodeEditor.vue`)
   - 画布管理
   - 连线绘制
   - 用户交互

## 未来扩展方向

- [ ] 节点配置面板
- [ ] 节点分组/折叠
- [ ] 撤销/重做
- [ ] 保存/加载工作流
- [ ] 节点验证和类型检查
- [ ] 可视化调试
- [ ] 节点模板
- [ ] 批量操作

