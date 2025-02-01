<template>
  <div class="editor-container">
    <div class="toolbar">
      <button @click="insertHeading" class="toolbar-btn">
        Heading
      </button>
      <button @click="insertTodo" class="toolbar-btn">
        TODO
      </button>
      <button @click="toggleBold" class="toolbar-btn">
        Bold
      </button>
      <button @click="toggleItalic" class="toolbar-btn">
        Italic
      </button>
      <button @click="insertList" class="toolbar-btn">
        List
      </button>
    </div>
    <div class="editor-layout">
      <div
        ref="editorContent"
        class="editor-content"
        contenteditable="true"
        @input="handleInput"
        @keydown="handleKeydown"
      >
        {{ content }}
      </div>
      <div class="preview" v-html="preview"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useWebSocket } from '@vueuse/core'
import axios from 'axios'
import { API_ROUTES } from '../constants/api'
import api from '../utils/api'

const content = ref('')
const preview = ref('')
const editorContent = ref<HTMLElement | null>(null)

const { data, send } = useWebSocket('ws://localhost:8000/ws/editor')

const updatePreview = async () => {
  try {
    const response = await api.post(API_ROUTES.ORG.PARSE, {
      content: content.value
    })
    preview.value = response.data.html
  } catch (error) {
    console.error('Preview update failed:', error)
  }
}

const handleInput = (e: Event) => {
  const target = e.target as HTMLElement
  content.value = target.innerText
  send(JSON.stringify({ type: 'content', data: content.value }))
  updatePreview()
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Tab') {
    e.preventDefault()
    document.execCommand('insertText', false, '  ')
  } else if (e.key === 'Enter' && e.shiftKey) {
    e.preventDefault()
    insertTodo()
  }
}

const insertHeading = () => {
  const level = prompt('Enter heading level (1-6):', '1')
  if (level && /^[1-6]$/.test(level)) {
    const stars = '*'.repeat(parseInt(level))
    document.execCommand('insertText', false, `${stars} `)
  }
}

const insertTodo = () => {
  document.execCommand('insertText', false, '- [ ] ')
}

const toggleBold = () => {
  const selection = window.getSelection()
  if (selection && selection.toString()) {
    const text = selection.toString()
    document.execCommand('insertText', false, `*${text}*`)
  }
}

const toggleItalic = () => {
  const selection = window.getSelection()
  if (selection && selection.toString()) {
    const text = selection.toString()
    document.execCommand('insertText', false, `/${text}/`)
  }
}

const insertList = () => {
  document.execCommand('insertText', false, '- ')
}

watch(data, (newData) => {
  if (newData) {
    const parsed = JSON.parse(newData)
    if (parsed.type === 'content') {
      content.value = parsed.data
      updatePreview()
    }
  }
})

onMounted(() => {
  if (data.value) {
    const parsed = JSON.parse(data.value)
    if (parsed.type === 'content') {
      content.value = parsed.data
      updatePreview()
    }
  }
})
</script>

<style scoped>
.editor-container {
  @apply w-full h-full flex flex-col;
}

.toolbar {
  @apply flex gap-2 p-2 border-b;
}

.toolbar-btn {
  @apply px-3 py-1 rounded bg-gray-100 hover:bg-gray-200;
}

.editor-layout {
  @apply flex-1 flex gap-4 p-4;
}

.editor-content {
  @apply flex-1 p-4 border rounded overflow-y-auto focus:outline-none font-mono;
}

.preview {
  @apply flex-1 p-4 border rounded overflow-y-auto prose prose-sm max-w-none;
}

:deep(.todo-item) {
  @apply flex items-center gap-2 my-1;
}

:deep(.todo-item input[type="checkbox"]) {
  @apply w-4 h-4;
}
</style> 
