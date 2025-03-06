import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UnityVersion {
  code: string
  date: string
  hub: string
  component: Array<VersionComponent>
}

interface VersionGroup {
  main: string
  version_list: UnityVersion[]
}

interface VersionComponent {
  key: string
  list: Array<{ key: string; value: string }>
}
export const useVersionStore = defineStore('versions', () => {
  const versions = ref<VersionGroup[]>([])
  const isLoading = ref(false)
  // 加载简化版本数据
  const loadSimplifiedData = async () => {
    try {
      const data = await import('../assets/version_simplify.json')
      // 将版本列表按照日期降序排序
      const allVersions = data.default.flatMap(group =>
        group.version_list.map(version => ({
          ...version,
          main: group.main
        }))
      ).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

      // 重新组织数据结构
      const groupedVersions = allVersions.reduce((acc, version) => {
        const main = version.main;
        if (!acc.find(g => g.main === main)) {
          acc.push({
            main,
            version_list: []
          });
        }
        const groupFind = acc.find(g => g.main === main);
        groupFind.version_list.push(version);
        return acc;
      }, [] as VersionGroup[]);
      versions.value = groupedVersions;
    } catch (error) {
      console.error('Failed to load simplified version data:', error)
      versions.value = []
    }
  } 

  // 加载完整版本数据
  const loadVersionData = async (versionYear: string) => {
    try {
      const data = await import(`../assets/data/${versionYear}.json`)
      return data.default
    } catch (error) {
      console.error(`Failed to load version data for year ${versionYear}:`, error)
      return []
    }
  }

  // 更新版本平台数据
  const updateVersionPlatform = async (version: UnityVersion) => {
    if (version.component) {
      return
    }

    try {
      const version_code = version.code
      const componentData = await loadVersionData(version_code)
      version.component = []
      for (const key in componentData) {
        if (Object.prototype.hasOwnProperty.call(componentData, key)) {
          const element = componentData[key];
          if (key == 'Windows') {
            version.component.push({
              key: 'Windows',
              list: element
            })
          } else if (key == 'Windows ARM64') {
            version.component.push({
              key: 'Windows ARM64',
              list: element
            })
          } else if (key == 'macOS') {
            version.component.push({
              key: 'macOS',
              list: element
            })
          } else if (key == 'macOS ARM64') {
            version.component.push({
              key: 'macOS ARM64',
              list: element
            })
          } else if (key == 'Linux') {
            version.component.push({
              key: 'Linux',
              list: element
            })
          }
        }
      }

      console.log(version.component)
    } catch (error) {
      console.error('Error updating version platform:', error)
      throw error
    }
  }

  // 初始化数据
  const initialize = async () => {
    await loadSimplifiedData()
  }

  // 执行初始化
  initialize()

  return {
    versions,
    filteredVersions: computed(() => versions.value),
    isLoading: computed(() => isLoading.value),
    updateVersionPlatform
  }
})