<template>
  <div class="min-h-screen bg-gray-100">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-lg shadow">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-medium text-gray-900">
                Org 문서 편집기
              </h2>
              <div class="flex space-x-3">
                <button
                  @click="saveDocument"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  저장
                </button>
              </div>
            </div>
            <OrgEditor
              ref="editor"
              @content-change="handleContentChange"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import OrgEditor from '../components/OrgEditor.vue'
import api from '../utils/api'
import { API_ROUTES } from '../constants/api'

const editor = ref()
let currentContent = ''

const handleContentChange = (content: string) => {
  currentContent = content
}

const saveDocument = async () => {
  try {
    await api.post(API_ROUTES.DOCUMENTS.CREATE, {
      content: currentContent
    })
    // TODO: 성공 메시지 표시
  } catch (error) {
    console.error('Failed to save document:', error)
    // TODO: 에러 메시지 표시
  }
}
</script>

<style scoped>
.editor-container {
  @apply min-h-[600px];
}
</style> 