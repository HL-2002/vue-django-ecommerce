<script setup lang="ts">
import { defineProps, watchEffect } from 'vue';

type NotificationType = 'success' | 'error';


const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  show: {
    type: Boolean,
    required: true,
  },
  type: {
    type: String as () => NotificationType,
    required: true,
  }

});

const emit = defineEmits(['close']);

watchEffect(() => {
  if (props.show) {
    setTimeout(() => {
      emit('close');
    }, 3000);
  }
});



</script>


<template>
  <Transition>
    <div v-if="props.show" class="fixed top-4 left-0 right-0 flex justify-center items-center z-10 pointer-events-none">
      <div class="bg-slate-50 py-2 px-3 shadow-xl rounded flex">
        <span v-if="props.type === 'error'" class="mr-2">❌</span>
        <span v-else class="mr-2">🎉</span>
        <p class="m-0">{{ props.message }}</p>
      </div>
    </div>

  </Transition>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: transform 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  transform: translateY(-150%);
}
</style>
