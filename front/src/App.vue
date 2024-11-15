<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router';
import NotificationDialog from './components/NotificationDialog.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-800 text-white">
    <header class="flex justify-between items-center p-4 shadow-md">
      <div class="flex gap-6">
        <RouterLink to="/" class="hover:text-gray-400">Home</RouterLink>
        <RouterLink to="/form/products" class="hover:text-gray-400">Crear producto</RouterLink>
        <RouterLink to="/form/reviews" class="hover:text-gray-400">Agregar review</RouterLink>
      </div>
    </header>
    <NotificationDialog />
    <RouterView />
  </div>
</template>
