# Element Plus Icons 使用指南

## 概述

Element Plus Icons 是 Element Plus 组件库的官方图标库，提供了丰富的图标组件。在本项目中，所有图标已在 `main.ts` 中全局注册，可以直接使用。

## 全局注册

在 `src/main.ts` 中，所有图标已被全局注册：

```typescript
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 注册所有 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
```

这意味着你可以直接使用图标组件，无需单独导入。

## 使用方式

### 方式一：直接使用（已全局注册）

```vue
<template>
  <el-icon><Odometer /></el-icon>
</template>
```

### 方式二：按需导入（推荐，更清晰）

```vue
<template>
  <el-icon><Odometer /></el-icon>
</template>

<script setup>
import { Odometer, User, Setting } from '@element-plus/icons-vue'
</script>
```

## 项目中已使用的图标

### AdminLayout.vue
- `Odometer` - 仪表盘
- `User` - 用户
- `Document` - 文档
- `Setting` - 设置
- `Fold` - 折叠
- `Expand` - 展开
- `Sunny` - 太阳（浅色模式）
- `Moon` - 月亮（深色模式）
- `ArrowDown` - 向下箭头

### UserManagement.vue
- `Plus` - 添加
- `Search` - 搜索
- `Refresh` - 刷新
- `Edit` - 编辑
- `Delete` - 删除

### Login.vue
- `User` - 用户
- `Lock` - 锁定

### Dashboard.vue
- `User` - 用户
- `Document` - 文档
- `TrendCharts` - 趋势图
- `Timer` - 定时器
- `CircleCheck` - 圆形勾选
- `InfoFilled` - 信息填充

### Translations.vue
- `Search` - 搜索
- `Refresh` - 刷新
- `Download` - 下载
- `View` - 查看
- `Delete` - 删除

### Translator.vue
- `ArrowRight` - 右箭头
- `DocumentCopy` - 文档复制

### MySettings.vue
- `Picture` - 图片

## 常用图标分类

### 导航和方向
- `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight` - 基础箭头
- `ArrowUpBold`, `ArrowDownBold`, `ArrowLeftBold`, `ArrowRightBold` - 粗体箭头
- `DArrowLeft`, `DArrowRight` - 双箭头
- `Back`, `Right`, `Top`, `Bottom` - 方向
- `TopLeft`, `TopRight`, `BottomLeft`, `BottomRight` - 角落方向
- `CaretTop`, `CaretBottom`, `CaretLeft`, `CaretRight` - 插入符号
- `Fold`, `Expand` - 折叠/展开

### 用户和权限
- `User`, `UserFilled` - 用户
- `Avatar` - 头像
- `Lock`, `Unlock` - 锁定/解锁
- `Key` - 钥匙

### 文档和文件
- `Document` - 文档
- `DocumentAdd` - 添加文档
- `DocumentCopy` - 复制文档
- `DocumentChecked` - 已检查文档
- `DocumentDelete` - 删除文档
- `DocumentRemove` - 移除文档
- `Files` - 文件
- `Folder`, `FolderOpened` - 文件夹
- `FolderAdd`, `FolderDelete`, `FolderRemove`, `FolderChecked` - 文件夹操作
- `Notebook`, `Memo`, `Reading` - 笔记相关

### 操作按钮
- `Plus`, `CirclePlus`, `CirclePlusFilled` - 添加
- `Minus`, `Remove`, `RemoveFilled` - 移除
- `Edit`, `EditPen` - 编辑
- `Delete`, `DeleteFilled` - 删除
- `Search` - 搜索
- `Refresh`, `RefreshLeft`, `RefreshRight` - 刷新
- `Download`, `Upload`, `UploadFilled` - 下载/上传
- `CopyDocument` - 复制
- `View` - 查看

### 设置和配置
- `Setting`, `SetUp` - 设置
- `Tools`, `Operation`, `Management` - 工具和管理
- `Switch`, `SwitchFilled`, `SwitchButton` - 开关

### 数据和图表
- `Odometer` - 仪表盘（里程表）
- `TrendCharts` - 趋势图
- `DataAnalysis`, `DataBoard`, `DataLine` - 数据分析
- `PieChart`, `Histogram` - 图表

### 状态和提示
- `CircleCheck`, `CircleCheckFilled` - 圆形勾选
- `CircleClose`, `CircleCloseFilled` - 圆形关闭
- `Check`, `Checked` - 勾选
- `Close`, `CloseBold` - 关闭
- `InfoFilled` - 信息填充
- `Warning`, `WarningFilled`, `WarnTriangleFilled` - 警告
- `SuccessFilled`, `Failed`, `Finished` - 成功/失败/完成

### 时间和日期
- `Timer`, `Stopwatch`, `AlarmClock`, `Clock` - 时间相关
- `Calendar` - 日历

### 主题和显示
- `Sunny`, `Moon`, `MoonNight` - 主题图标
- `Sunrise`, `Sunset` - 日出/日落
- `Hide`, `View` - 隐藏/显示
- `FullScreen` - 全屏

### 通信和消息
- `Message`, `MessageBox` - 消息
- `ChatRound`, `ChatSquare`, `ChatDotRound`, `ChatDotSquare` - 聊天
- `ChatLineRound`, `ChatLineSquare` - 聊天线
- `Bell`, `BellFilled`, `Notification`, `MuteNotification` - 通知

### 媒体
- `Picture`, `PictureFilled`, `PictureRounded` - 图片
- `Camera`, `CameraFilled` - 相机
- `VideoCamera`, `VideoCameraFilled`, `VideoPlay`, `VideoPause` - 视频
- `Film`, `Microphone`, `Mic` - 媒体设备

### 购物和商品
- `ShoppingCart`, `ShoppingCartFull`, `ShoppingBag`, `ShoppingTrolley` - 购物车
- `Goods`, `GoodsFilled` - 商品
- `PriceTag`, `Discount`, `Promotion` - 价格和促销

### 位置和地图
- `Location`, `LocationFilled`, `LocationInformation` - 位置
- `MapLocation`, `AddLocation`, `DeleteLocation` - 地图位置
- `Coordinate`, `Compass`, `Place`, `Position` - 坐标和方向

### 其他常用
- `Menu`, `Grid`, `List` - 菜单和列表
- `Filter`, `Sort`, `SortUp`, `SortDown` - 筛选和排序
- `Link`, `Share` - 链接和分享
- `Printer`, `Paperclip` - 打印和附件
- `Help`, `HelpFilled`, `QuestionFilled` - 帮助
- `Star`, `StarFilled` - 星标
- `Collection`, `CollectionTag` - 收藏
- `Flag`, `Trophy`, `TrophyBase`, `Medal`, `GoldMedal` - 标志和奖章

## 完整图标列表

Element Plus Icons 包含超过 200 个图标。所有可用的图标组件名称可以在以下路径查看：

```
node_modules/@element-plus/icons-vue/dist/types/components/
```

每个图标都有对应的 `.d.ts` 类型定义文件，文件名即为组件名（首字母大写，如 `odometer.vue.d.ts` 对应 `Odometer` 组件）。

## 使用示例

### 在按钮中使用

```vue
<el-button :icon="Search">搜索</el-button>
```

### 在菜单中使用

```vue
<el-menu-item index="/dashboard">
  <el-icon><Odometer /></el-icon>
  <template #title>仪表盘</template>
</el-menu-item>
```

### 条件显示图标

```vue
<el-icon>
  <Sunny v-if="isDark" />
  <Moon v-else />
</el-icon>
```

### 动态图标

```vue
<el-button :icon="isCollapse ? Expand : Fold" @click="toggleCollapse" />
```

## 注意事项

1. **命名规范**：图标组件名采用 PascalCase（首字母大写），如 `Odometer`、`User`、`Setting`
2. **全局注册**：虽然图标已全局注册，但按需导入可以让代码更清晰，也便于 Tree Shaking
3. **响应式**：图标组件是响应式的，可以配合 Vue 的响应式系统使用
4. **样式**：图标可以通过 CSS 设置颜色、大小等样式

## 参考资源

- [Element Plus Icons 官方文档](https://element-plus.org/zh-CN/component/icon.html)
- [Element Plus Icons GitHub](https://github.com/element-plus/element-plus-icons)

