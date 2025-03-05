<template>
  <el-container>
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-text">Unity国际版</span>
        </div>
        
        <el-menu
          :default-active="activeKey"
          mode="horizontal"
          class="nav-menu"
          @select="handleSelect"
        >
          <el-menu-item v-for="item in menuOptions" :key="item.key" :index="item.key">
            {{ item.label }}
          </el-menu-item>
        </el-menu>
      </div>
    </el-header>
    
    <el-main>
      <div class="hero-section">
        <h1 class="hero-title">下载 Unity</h1>
        <p class="hero-subtitle">选择适合您的版本开始创作</p>
      </div>

      <div class="content-section">
        <version-list />
      </div>
    </el-main>
    
    <el-footer class="footer">
      <div class="footer-content">
        <div class="footer-links">
          <a href="https://unity.com/de/releases/editor/archive">官方网站</a>
        </div>
      </div>
      <br/>
      <div class="footer-text">
        <span>  © {{ new Date().getFullYear() }} 我们旨在为部分特殊地区的Unity开发者提供与世界上大多数用户一致的Unity Editor下载方式。</span>
        <br/>
        <span>“Unity”、Unity 徽标及其他 Unity 商标是 Unity Technologies 或其在美国和其他地区的分支机构的商标或注册商标。本站不是Unity Technologies优美缔软件提供的一项服务。</span>
        <br/>
        <span>我们不会保存任何的文件与数据，所有的内容来自官方下载渠道，请自行甄别。</span>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import VersionList from '../components/VersionList.vue'

const activeKey = ref('home')

const menuOptions = [
  {
    label: '社区',
    key: 'community',
    url: 'https://forum.unity.com/'  // 添加跳转链接
  },
  {
    label: '深情推荐',
    key: 'recommend',
    url: 'https://gameframex.doc.alianblank.com/'  // 添加跳转链接
  }
]

const handleSelect = (key: string) => {
  const menuItem = menuOptions.find(item => item.key === key)
  if (menuItem?.url) {
    window.open(menuItem.url, '_blank')
  }
}
</script>

<style scoped>
.el-container {
  min-height: 100vh;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 0;
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.logo {
  margin-right: 48px;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
}

.nav-menu {
  flex: 1;
  border: none;
}

.hero-section {
  padding: 60px 0 30px;
  text-align: center;
  background: var(--el-bg-color);
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 16px;
  color: var(--el-text-color-primary);
}

.hero-subtitle {
  font-size: 18px;
  color: var(--el-text-color-secondary);
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}

.version-tabs {
  margin-bottom: 24px;
}

.el-main {
  padding-top: 0;
}

.footer {
  padding: 24px;
  text-align: center;
  border-top: 1px solid var(--el-border-color-light);
  background-color: var(--el-bg-color);
}

.footer-text {
  color: var(--el-text-color-secondary);
}
</style>