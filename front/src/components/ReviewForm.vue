<script setup lang="ts">
import { CreateReview, getProducts } from '@/services/products';
import { useNotificationStore } from '@/stores/notification';
import type { Product } from '@/types/types';
import { computed, onMounted, ref } from 'vue';

const { notify } = useNotificationStore()

const products = ref<Product[]>()
const product = ref<Product>()

onMounted(() => {
  getProducts().then(data => {
    products.value = data
  })
})

function onChange(event: Event) {
  const target = event.target as HTMLSelectElement
  const selectedProduct = products?.value?.find(product => product.id === Number(target.value))
  product.value = selectedProduct
}

function submitForm(event: Event) {
  const formData = new FormData(event.target as HTMLFormElement)
  if (formData.get('product') === '0') {
    notify({ message: 'Selecciona un producto', type: 'error' })
    return
  }

  CreateReview(formData).then(() => {
    notify({ message: 'Review creada', type: 'success' })
  }).catch(() => {
    notify({ message: 'Error al crear la review', type: 'error' })
  })
}

const minDate = computed(() => {
  if (!product.value) return ''
  return new Date(product.value?.meta?.createdAt).toISOString().split('T')[0]
})
</script>

<template>
  <form @submit.prevent="submitForm"
    class="w-1/2 m-auto flex flex-col gap-4 bg-gray-700 p-6 justify-center rounded shadow-lg text-white">
    <label for="product" class="font-semibold">Producto</label>
    <select @change="onChange" name="product" id="product"
      class="bg-gray-800 border border-gray-600 rounded p-2 text-white">
      <option value="0">Selecciona un producto</option>
      <option :key="product.id" v-for="product in products" :value="product.id">{{ product.title }}</option>
    </select>

    <label for="name" class="font-semibold">Nombre</label>
    <input required type="text" name="reviewerName" id="name"
      class="bg-gray-800 border border-gray-600 rounded p-2 text-white">

    <label for="email" class="font-semibold">Correo Electrónico</label>
    <input required type="email" name="reviewerEmail" id="email"
      class="bg-gray-800 border border-gray-600 rounded p-2 text-white">

    <label for="date" class="font-semibold">Fecha</label>
    <input required :min="minDate" type="date" name="date" id="date"
      class="bg-gray-800 border border-gray-600 rounded p-2 text-white">

    <label for="rating" class="font-semibold">Calificación</label>
    <input required type="number" name="rating" id="rating" min="1" max="5"
      class="bg-gray-800 border border-gray-600 rounded p-2 text-white">

    <label for="comment" class="font-semibold">Comentario</label>
    <textarea required name="comment" id="comment"
      class="bg-gray-800 border border-gray-600 rounded p-2 text-white"></textarea>

    <button class="bg-blue-500 rounded w-fit text-white px-4 py-2 m-auto hover:bg-blue-600"
      type="submit">Registrar</button>
  </form>
</template>
