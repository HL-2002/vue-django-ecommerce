<script setup lang="ts">
import { ref } from 'vue';
import CategorySelector from "./CategorySelector.vue"

const selectedCategory = ref<string[]>([])

</script>


<template>
  <form class="max-w-80">
    <h1>Y que un formulario</h1>
    <CategorySelector v-model="selectedCategory" />
  </form>
</template>
