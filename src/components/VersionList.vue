<template>
  <div class="version-list">
    <el-space direction="vertical" size="large" fill>
      <div v-loading="loading" class="tabs-container">
        <el-tabs type="border-card" lazy stretch v-model="activeTab">
          <el-tab-pane v-for="version_group in versionStore.filteredVersions" :key="version_group.main"
            :label="`${version_group.main}`" :name="version_group.main">
            <el-row :gutter="24">
              <el-col v-for="version in version_group.version_list" :key="version.code" :span="24">
                <version-card :version="version" />
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-space>
  </div>
</template>

<script setup lang="ts">
import { useVersionStore } from '../stores/versions'
import VersionCard from './VersionCard.vue'
import { ref, watch, nextTick } from 'vue'

const versionStore = useVersionStore()
const activeTab = ref('')
const loading = ref(true)  // 添加 loading 状态

watch(
  () => versionStore.filteredVersions,
  async (newVersions) => {
    if (newVersions && Object.keys(newVersions).length > 0) {
      await nextTick()
      activeTab.value = newVersions[0].main
      loading.value = false  // 数据加载完成，关闭 loading
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.version-list {
  min-height: 200px;
}

.tabs-container {
  min-height: 300px;
  width: 100%;
}
</style>