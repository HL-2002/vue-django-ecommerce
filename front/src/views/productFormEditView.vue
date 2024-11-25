<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import ProductForm from '@/components/ProductForm.vue';

const route = useRoute();
const productId = ref(route.params.id as string);
</script>

<template>
  <ProductForm :productId="productId" />
</template>
