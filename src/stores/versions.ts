import { defineStore } from 'pinia'
import data2017 from '../assets/data/download-archive-2017.json'
import data2018 from '../assets/data/download-archive-2018.json'
import data2019 from '../assets/data/download-archive-2019.json'
import data2020 from '../assets/data/download-archive-2020.json'
import data2021 from '../assets/data/download-archive-2021.json'
import data2022 from '../assets/data/download-archive-2022.json'
import data2023 from '../assets/data/download-archive-2023.json'
import data6000 from '../assets/data/download-archive-6000.json'
import { ref, computed } from 'vue'

export interface UnityVersion {
  version_code: string
  version_build_date: string
  unity_hub_url: string
  platform: {
    win: Array<{ key: string; value: string }>
    mac: Array<{ key: string; value: string }>
    linux: Array<{ key: string; value: string }>
  }
}

export const useVersionStore = defineStore('versions', () => {
  const versions = ref<UnityVersion[]>([...data6000, ...data2023,...data2022,...data2021,...data2020,...data2019,...data2018,...data2017])
  
  const sortedVersions = computed(() => {
    return [...versions.value].sort((a, b) => {
      return new Date(b.version_build_date).getTime() - new Date(a.version_build_date).getTime()
    })
  })
  const searchQuery = ref('')
  const filteredVersions = computed(() => {
    if (!searchQuery.value) return sortedVersions.value
    const query = searchQuery.value.toLowerCase()
    return sortedVersions.value.filter(version => 
      version.version_code.toLowerCase().includes(query) ||
      version.version_build_date.toLowerCase().includes(query)
    )
  })
  const versionsByYear = computed(() => {
    const grouped = {}
    filteredVersions.value.forEach(version => {
      const year = version.version_code.split('.')[0]
      if (!grouped[year]) {
        grouped[year] = []
      }
      grouped[year].push(version)
    })
    return grouped
  })
  return {
    versions,
    searchQuery,
    filteredVersions,
    versionsByYear // 导出新的计算属性
  }
})