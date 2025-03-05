<template>
  <el-card class="version-card">
    <div class="footer-buttons">
        <el-text size="large">{{ version.version_code }}</el-text>
      
        <el-button
          type="success"
          @click="openUnityHub(version.unity_hub_url)"
        >
          <el-icon class="unity-hub-icon">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path fill="currentColor" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.54-2.77 8.62-7 10-4.23-1.38-7-5.46-7-10V6.3l7-3.12z"/>
            </svg>
          </el-icon>
          在 Unity Hub 中打开
        </el-button>

        <el-button
          type="primary"
          @click="showDownloads = !showDownloads"
        >
          <el-icon class="button-icon">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path fill="currentColor" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
            </svg>
          </el-icon>
          {{ showDownloads ? '收起扩展组件下载选项' : '展开扩展组件下载选项' }}
        </el-button>
        <el-tag type="info">{{ formattedDate }}</el-tag>
    </div>
    <el-divider />
    <el-card v-show="showDownloads">         
      <el-collapse-transition>
        <div>
          <el-tabs type="card" lazy stretch v-model="activeTab">
            <el-tab-pane label="Windows" name="windows">
              <div class="download-buttons">
                <el-button
                  v-for="download in version.platform.win"
                  :key="download.key"
                  type="primary"
                  plain
                  @click="openDownload(download.value)"
                  class="download-button"
                >
                  {{ download.key }}
                </el-button>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="macOS" name="mac">
              <div class="download-buttons">
                <el-button
                  v-for="download in version.platform.mac"
                  :key="download.key"
                  type="primary"
                  plain
                  @click="openDownload(download.value)"
                  class="download-button"
                >
                  {{ download.key }}
                </el-button>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="Linux" name="linux">
              <div class="download-buttons">
                <el-button
                  v-for="download in version.platform.linux"
                  :key="download.key"
                  type="primary"
                  plain
                  @click="openDownload(download.value)"
                  class="download-button"
                >
                  {{ download.key }}
                </el-button>
              </div>
            </el-tab-pane>

          </el-tabs>
        </div>
      </el-collapse-transition>
    </el-card>
  </el-card>
</template>

<script setup lang="ts">
import { UnityVersion } from '../stores/versions'
import { ref, computed } from 'vue'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'

const props = defineProps<{
  version: UnityVersion
}>()

const activeTab = ref('windows') // 设置默认选中的标签页

const formattedDate = computed(() => {
  const date = new Date(props.version.version_build_date)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
})

const showDownloads = ref(false)

const openDownload = (url: string) => {
  window.open(url, '_blank')
}

const openUnityHub = (url: string) => {
  window.location.href = url
}
</script>

<style scoped>
.download-buttons {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.download-button {
  width: 100%;
  max-width: 400px;
  margin-bottom: 8px;
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
</style>