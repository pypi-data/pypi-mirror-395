<template>
  <div class="home-container">
    <div class="hero-section">
      <h1 class="hero-title">智能翻译工具</h1>
      <p class="hero-subtitle">支持多语言实时翻译，快速准确</p>
      <router-link to="/translator" class="cta-button">
        开始翻译
      </router-link>
    </div>

    <div class="features-section">
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <h3 class="feature-title">快速翻译</h3>
          <p class="feature-desc">毫秒级响应，实时翻译体验</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌍</div>
          <h3 class="feature-title">多语言支持</h3>
          <p class="feature-desc">支持10+种常用语言互译</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3 class="feature-title">准确可靠</h3>
          <p class="feature-desc">基于先进的AI翻译引擎</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💡</div>
          <h3 class="feature-title">简单易用</h3>
          <p class="feature-desc">界面简洁，操作便捷</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 首页组件
</script>

<style scoped>
.home-container {
  min-height: calc(100vh - var(--header-height));
  padding: 2rem;
}

.hero-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1rem;
  color: white;
  margin-bottom: 4rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #fff, #e0e7ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  display: inline-block;
  padding: 0.875rem 2rem;
  background: white;
  color: #667eea;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1.125rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.features-section {
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.feature-desc {
  color: #6b7280;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>

