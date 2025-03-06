<template>
  <el-card class="version-card">
    <div class="footer-buttons">
      <div style="display: flex; align-items: center; gap: 8px">
        <el-tag v-if="version.code.includes('f')" type="success">LTS</el-tag>
        <el-text size="large">{{ version.code }}</el-text>        
      </div>
      <el-text size="large"> </el-text>
      <el-button type="success" @click="openUnityHub(version.hub)">
        <el-icon class="unity-hub-icon">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path fill="currentColor" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z" />
          </svg>
        </el-icon>
        在 Unity Hub 中打开
      </el-button>

      <el-button type="primary" @click="handleExpandClick">
        <el-icon class="button-icon">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path fill="currentColor" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z" />
          </svg>
        </el-icon>
        {{ showDownloads ? '收起扩展组件下载选项' : '展开扩展组件下载选项' }}
      </el-button>
      <el-text size="large"> </el-text>
      <el-text size="large">发布时间: {{ version.date }}</el-text>
    </div>
    <el-divider />
    <el-card v-show="showDownloads">
      <el-collapse-transition>
        <div>
          <el-tabs type="card" lazy stretch v-model="activeTab" v-if="version.component">
            <el-tab-pane v-for="(component, key) in version.component" :key="component.key" :label="`${component.key}`"
              :name="component.key">
              <el-space fill wrap alignment="flex-start" style="width: 100%">
                <el-button v-for="download in component.list" :key="download.key" type="primary" plain
                  class="download-link-item" @click="openDownload(download.value)">
                  {{ download.key }}
                </el-button>
              </el-space>
            </el-tab-pane>
          </el-tabs>
          <div v-else class="loading-state">
            <el-skeleton :rows="3" animated />
          </div>
        </div>
      </el-collapse-transition>
    </el-card>
  </el-card>
</template>

<script setup lang="ts">
import { UnityVersion } from '../stores/versions'
import { ref, computed } from 'vue'
import { useVersionStore } from '../stores/versions'

const props = defineProps<{
  version: UnityVersion
}>()

const versionStore = useVersionStore()
const activeTab = ref('windows')
const showDownloads = ref(false)
const isLoading = ref(false)

const handleExpandClick = async () => {
  if (!showDownloads.value) {
    isLoading.value = true
    try {
      await versionStore.updateVersionPlatform(props.version)
      if (props.version.component && props.version.component.length > 0) {
        const component = props.version.component[0]
        activeTab.value = component.key
      }
    } catch (error) {
      console.error('Failed to load platform data:', error)
    } finally {
      isLoading.value = false
    }
  }
  showDownloads.value = !showDownloads.value
}

const openDownload = (url: string) => {
  window.open(url, '_blank')
}

const openUnityHub = (url: string) => {
  window.location.href = url
}
</script>

<style scoped>
.download-link-item {
  display: block;
  gap: 8px;
  width: 100%;
}

.download-buttons {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.version-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.unity-hub-icon {
  margin-right: 8px;
  width: 1.2em;
  height: 1.2em;
}

:deep(.el-card__footer) {
  text-align: center;
}

.footer-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.button-icon {
  margin-right: 8px;
  width: 1.2em;
  height: 1.2em;
}

:deep(.el-card__footer) {
  text-align: center;
}

.loading-state {
  padding: 20px;
}
</style>