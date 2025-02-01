<template>
  <div class="min-h-screen bg-gray-900 text-green-300 font-mono">
    <div class="flex h-screen">
      <!-- 좌측 Agenda View -->
      <div class="flex-1 p-4 overflow-y-auto">
        <div class="mb-4 text-sm text-gray-500">
          Week-agenda (W05):
        </div>

        <div v-for="day in weekDays" :key="day.date" class="mb-2">
          <div class="text-yellow-500 mb-1">
            {{ formatDate(day.date) }}
          </div>
          
          <div v-for="item in day.items" :key="item.time" 
               class="flex items-start hover:bg-gray-800 p-1 text-sm"
               :class="{'pl-8': !item.time}">
            <div class="w-16 text-gray-500">{{ item.time || '' }}</div>
            <div class="w-20 text-green-400">
              {{ item.category }}
            </div>
            <div class="w-12 text-yellow-500">{{ item.priority || '' }}</div>
            <div class="flex-1">{{ item.content }}</div>
            <div class="text-gray-500 ml-2">
              {{ item.tags ? ':' + item.tags.join(':') + ':' : '' }}
            </div>
            <div class="ml-2 text-gray-500">{{ item.location || '' }}</div>
          </div>
        </div>
      </div>

      <!-- 우측 Org Mode Editor -->
      <div class="w-1/3 border-l border-gray-700 bg-gray-900 p-4 overflow-y-auto">
        <div class="mb-2 text-sm text-gray-500">
          * Press '?' for help, 'q' to quit
        </div>
        <div 
          ref="editor"
          class="font-mono whitespace-pre-wrap outline-none text-sm"
          contenteditable="true"
          @input="handleEditorInput"
          @keydown="handleEditorKeydown"
        >
* TODO [#A] [HUB] 버터샵 API 작업 진행 및 일정 계획 및 문서 통합 비정형화
SCHEDULED: <2024-01-25 Thu>
:PROPERTIES:
:CATEGORY: 업무
:LOCATION: stock:aws:
:END:

* DONE [#B] [emon] 어드민과 ezypay 큐선 어드민 미팅
DEADLINE: <2024-01-25 Thu 14:00>
:PROPERTIES:
:CATEGORY: 회의
:END:

* TODO [emon] 어드민과 ezypay 큐선 어드민 미팅
SCHEDULED: <2024-01-25 Thu 15:00>
:PROPERTIES:
:CATEGORY: 회의
:END:
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { format, addDays, startOfWeek, startOfMonth, endOfMonth, eachDayOfInterval } from 'date-fns'
import { ko } from 'date-fns/locale'

interface AgendaItem {
  time?: string
  category: string
  content: string
  done: boolean
  priority?: string
  location?: string
  tags?: string[]
}

interface DayAgenda {
  date: Date
  items: AgendaItem[]
}

const weekDays = ref<DayAgenda[]>([])

const formatDate = (date: Date) => {
  return format(date, 'EEEE dd MMMM yyyy', { locale: ko })
}

const formatCategory = (category: string) => {
  return category ? `[${category}]` : ''
}

const getItemColorClass = (category: string) => {
  const colors: Record<string, string> = {
    'TODO': 'text-red-600',
    'DONE': 'text-green-600',
    'SCHEDULED': 'text-blue-600',
    'DEADLINE': 'text-orange-600'
  }
  return colors[category] || 'text-gray-900'
}

const generateMockWeekData = () => {
  const startDate = startOfWeek(new Date())
  const days: DayAgenda[] = []

  for (let i = 0; i < 7; i++) {
    const currentDate = addDays(startDate, i)
    days.push({
      date: currentDate,
      items: [
        {
          time: '09:00',
          category: 'TODO',
          priority: '[#A]',
          content: '[HUB] 버터샵 API 작업 진행 및 일정 계획 및 문서 통합 비정형화',
          done: false,
          location: 'stock:aws:',
          tags: ['업무', '개발']
        },
        {
          time: '14:00',
          category: 'DONE',
          priority: '[#B]',
          content: '[emon] 어드민과 ezypay 큐선 어드민 미팅',
          done: true,
          tags: ['회의']
        }
      ]
    })
  }
  return days
}

onMounted(() => {
  weekDays.value = generateMockWeekData()
})

const showKeyboardHelp = ref(false)
const editor = ref<HTMLElement | null>(null)
const selectedDate = ref(new Date())

const currentMonth = computed(() => {
  return format(selectedDate.value, 'yyyy년 MM월', { locale: ko })
})

const monthDates = computed(() => {
  const start = startOfMonth(selectedDate.value)
  const end = endOfMonth(selectedDate.value)
  return eachDayOfInterval({ start, end }).map(date => ({
    date,
    day: format(date, 'd'),
    isToday: format(date, 'yyyy-MM-dd') === format(new Date(), 'yyyy-MM-dd')
  }))
})

const keyboardShortcuts = {
  'a': '새 일정 추가',
  't': 'TODO 상태 변경',
  'd': '완료 표시',
  'q': '종료',
  '?': '도움말 보기',
  'j/k': '항목 이동',
  'SPC': '항목 선택'
}

const handleEditorKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Tab') {
    e.preventDefault()
    document.execCommand('insertText', false, '  ')
  }
}

const handleEditorInput = (e: Event) => {
  // Org 모드 문법 하이라이팅 로직 구현
}

const getDateClass = (date: { isToday: boolean }) => {
  return {
    'cursor-pointer p-1 text-center': true,
    'bg-green-800 text-white rounded': date.isToday,
    'hover:bg-gray-800': !date.isToday
  }
}

// 키보드 단축키 처리
const handleKeyPress = (e: KeyboardEvent) => {
  switch(e.key) {
    case 'a':
      // TODO: 새 일정 추가 다이얼로그 표시
      break
    case 'd':
      // TODO: 선택된 일정 완료 처리
      break
    case 't':
      // TODO: TODO 항목으로 변경
      break
    case 'q':
      // TODO: 뒤로 가기
      break
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress)
})
</script>

<style scoped>
.font-mono {
  font-family: 'Courier New', Courier, monospace;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #444;
}

[contenteditable] {
  caret-color: #4ade80;
}
</style> 