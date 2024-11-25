<script setup lang="ts">
import { useNotificationStore } from '@/stores/notification';

const { notifications } = useNotificationStore();
</script>

<template>
  <TransitionGroup tag="div"
    class="fixed top-4 left-0 right-0 flex flex-col justify-center items-center z-10 pointer-events-none gap-2">
    <div v-for="noti in notifications" :key="noti.message" class="bg-blue-100 py-2 px-3 shadow-xl rounded flex">
      <span v-if="noti.type === 'error'" class="mr-2 text-red-500">❌</span>
      <span v-else class="mr-2 text-green-500">🎉</span>
      <p class="m-0 text-gray-800">{{ noti.message }}</p>
    </div>
  </TransitionGroup>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  transform: translateY(-150%);
  opacity: 0;
}
</style>
