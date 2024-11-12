<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router';

</script>

<template>
  <header class="flex gap-4 p-4">
    <RouterLink to="/">home</RouterLink>
    <RouterLink to="/form/products">Crear producto</RouterLink>

    <RouterLink to="/form/reviews">Agregar review</RouterLink>

  </header>
  <RouterView />
</template>
