<template>
  <div class="translator-page">
    <div class="page-header">
      <h1 class="page-title">翻译工具</h1>
      <p class="page-subtitle">输入文本，选择目标语言，即可获得翻译结果</p>
    </div>

    <div class="translator-container">
      <!-- 左侧输入区 -->
      <div class="input-panel">
        <div class="panel-header">
          <span class="panel-title">原文</span>
          <el-button
            v-if="sourceText"
            size="small"
            type="danger"
            text
            @click="clearAll"
          >
            清空
          </el-button>
        </div>
        <el-input
          v-model="sourceText"
          type="textarea"
          :rows="20"
          placeholder="请输入要翻译的内容..."
          class="textarea-input"
          @input="handleInput"
        />
        <div class="char-count">
          {{ sourceText.length }} 字符
        </div>
      </div>

      <!-- 中间操作区 -->
      <div class="action-panel">
        <el-button
          type="primary"
          :loading="loading"
          :disabled="!sourceText.trim()"
          @click="handleTranslate"
          class="translate-button"
        >
          <el-icon v-if="!loading"><ArrowRight /></el-icon>
          {{ loading ? '翻译中...' : '翻译' }}
        </el-button>
        <el-select
          v-model="targetLang"
          class="lang-select"
          placeholder="选择语言"
          @change="handleTranslate"
        >
          <el-option
            v-for="lang in languages"
            :key="lang.code"
            :label="`${lang.flag} ${lang.name}`"
            :value="lang.code"
          />
        </el-select>
      </div>

      <!-- 右侧翻译区 -->
      <div class="output-panel">
        <div class="panel-header">
          <span class="panel-title">译文</span>
          <el-button
            v-if="translatedText"
            size="small"
            type="primary"
            text
            @click="copyResult"
          >
            <el-icon><DocumentCopy /></el-icon>
            复制
          </el-button>
        </div>
        <el-input
          v-model="translatedText"
          type="textarea"
          :rows="20"
          readonly
          :loading="loading"
          placeholder="翻译结果将显示在这里..."
          class="textarea-output"
        />
        <div v-if="translatedText" class="char-count">
          {{ translatedText.length }} 字符
        </div>

        <!-- 错误提示 -->
        <el-alert
          v-if="error"
          :title="error"
          type="error"
          show-icon
          :closable="true"
          @close="error = ''"
          class="error-alert"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTranslator } from '../composables/useTranslator'
import { LANGUAGES } from '../constants/languages'
import { ArrowRight, DocumentCopy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const {
  sourceText,
  translatedText,
  targetLang,
  loading,
  error,
  handleInput,
  handleTranslate,
  clearAll: clearTranslator,
  copyResult: copyTranslatorResult,
} = useTranslator()

const languages = LANGUAGES

const clearAll = (): void => {
  clearTranslator()
}

const copyResult = async (): Promise<void> => {
  const success = await copyTranslatorResult()
  if (success) {
    ElMessage.success('已复制到剪贴板')
  } else {
    ElMessage.error('复制失败')
  }
}
</script>

<style scoped>
.translator-page {
  min-height: calc(100vh - var(--header-height));
  padding: 2rem;
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6b7280;
  font-size: 1.125rem;
}

.translator-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.5rem;
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.input-panel,
.output-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.panel-title {
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
}

.textarea-input,
.textarea-output {
  flex: 1;
}

:deep(.el-textarea__inner) {
  font-size: 1rem;
  line-height: 1.6;
  resize: none;
}

.char-count {
  font-size: 0.875rem;
  color: #9ca3af;
  text-align: right;
}

.action-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  padding: 0 1rem;
}

.translate-button {
  width: 100%;
  min-width: 120px;
  height: 48px;
  font-size: 1rem;
}

.lang-select {
  width: 100%;
  min-width: 120px;
}

.error-alert {
  margin-top: 0.75rem;
}

@media (max-width: 1024px) {
  .translator-container {
    grid-template-columns: 1fr;
  }

  .action-panel {
    flex-direction: row;
    padding: 1rem 0;
  }

  .translate-button {
    width: auto;
    flex: 1;
  }

  .lang-select {
    width: auto;
    flex: 1;
  }
}

@media (max-width: 768px) {
  .translator-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.75rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .translator-container {
    padding: 1rem;
  }
}
</style>

