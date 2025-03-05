<template>
  <div class="version-list">
    <el-space direction="vertical" size="large" fill>
      <el-input
        v-model="versionStore.searchQuery"
        placeholder="搜索版本..."
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-tabs type="border-card" stretch v-model="activeTab">
        <el-tab-pane 
          v-for="(versions, year) in versionStore.versionsByYear" 
          :key="year"
          :label="`${year}`"
          :name="year"
        >
          <el-row :gutter="24">
            <el-col 
              v-for="version in versions" 
              :key="version.version_code"
              :span="24"
            >
              <version-card :version="version" />
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-space>
  </div>
</template>

<script setup lang="ts">
import { useVersionStore } from '../stores/versions'
import VersionCard from './VersionCard.vue'
import { Search } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'

const versionStore = useVersionStore()
const activeTab = ref('')

onMounted(() => {
  // 获取第一个标签页的值作为默认值
  const firstYear = Object.keys(versionStore.versionsByYear)[0]
  if (firstYear) {
    activeTab.value = firstYear
  }
})
</script>

<style scoped>
.version-list {
  min-height: 200px;
}
</style>