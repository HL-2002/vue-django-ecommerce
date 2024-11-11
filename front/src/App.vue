<script setup lang="ts">
import { ref } from 'vue';
import CategorySelector from './components/CategorySelector.vue';
import HomeView from './views/HomeView.vue';

const seletedCategory = ref<string[]>([])
</script>

<template>
  <div class="flex gap-12 flex-col">
    <HomeView />
    <h1 class="text-2xl font-bold">Selected Categories</h1>
    <CategorySelector v-model="seletedCategory" />
    <p class="">{{ seletedCategory }}</p>
  </div>
</template>
