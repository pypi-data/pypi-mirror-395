<template>
  <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: red; z-index: 9999;">
    <h1 style="color: white; padding: 20px;">测试：如果你看到这个，说明路由正常</h1>
    <p style="color: white; padding: 20px;">如果还是黑屏，可能是组件加载问题</p>
  </div>
</template>

<script setup lang="ts">
console.log('NodeEditorTest loaded')
</script>

