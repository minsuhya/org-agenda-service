<script setup lang="ts">
import TheWelcome from '@/components/TheWelcome.vue'
</script>

<template>
  <main>
    <TheWelcome />
    <div class="flex gap-1 mt-5">
      <div class="w-14 flex-none bg-blue-200 rounded">01</div>
      <div class="w-64 flex-1 bg-yellow-200 rounded">Tailwindcss</div>
      <div class="w-32 flex-1 bg-red-200 rounded">03</div>
    </div>
  </main>
</template>
