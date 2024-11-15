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
    class="w-1/2 m-auto flex flex-col gap-4 bg-neutral-100 p-4 justify-center rounded shadow-lg">
    <label for="product">Product</label>
    <select @change="onChange" name="product" id="product" class="bg-white border border-gray-300 rounded">
      <option value="0">Select a product</option>
      <option :key="product.id" v-for="product in products" :value="product.id">{{ product.title }}</option>
    </select>

    <label for="name">Name</label>
    <input requiredtype="text" name="reviewerName" id="name" class="border border-gray-300 rounded">

    <label for="email">Email</label>
    <input required type="email" name="reviewerEmail" id="email" class="border border-gray-300 rounded">

    <label for="date">Date</label>
    <input required :min="minDate" type="date" name="date" id="date" class="border border-gray-300 rounded">

    <label for="rating">Rating</label>
    <input required type="number" name="rating" id="rating" min="1" max="5" class="border border-gray-300 rounded">

    <label for="comment">Comment</label>
    <textarea required name="comment" id="comment" class="border border-gray-300 rounded"></textarea>

    <button class="bg-blue-500 rounded w-fit text-white px-2 py-1 m-auto" type="submit">Registrar</button>
  </form>
</template>
