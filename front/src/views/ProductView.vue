<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter ,RouterLink} from 'vue-router';
import type { Product } from '@/types/types';
import { API_URL } from '@/services/products';
import { useNotificationStore } from '@/stores/notification';

const route = useRoute();
const product = ref<Product | null>(null);
const error = ref<string | null>(null);
const mainImage = ref<string>("");

const {notify} = useNotificationStore()
const router = useRouter()

const fetchProduct = async () => {
  try {
    const response = await fetch(`${API_URL}/API/product/${route.params.id}/?format=json`);
    if (!response.ok) throw new Error('Failed to fetch product');
    product.value = await response.json();
    mainImage.value = product.value?.thumbnail || "https://placehold.co/600x400"
  } catch (err) {
    error.value = (err as Error).message;
  }
};

const updateMainImage = (url: string) => {
  mainImage.value = url;
};

async function deleteProduct(){
  const res = await fetch(`${API_URL}/API/product/${route.params.id}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (res.ok) {
    notify({
      message: 'El producto ha sido eliminado correctamente',
      type: 'success',
    })
    router.push('/')
  } else {
    alert('Error al eliminar el producto');
  }
}





onMounted(fetchProduct);
</script>

<template>
  <div class="container mx-auto p-6">
    <div v-if="error" class="text-red-500 text-center">{{ error }}</div>
    <div v-else-if="!product" class="text-gray-500 text-center">Cargando...</div>
    <div v-else class="max-w-6xl mx-auto bg-gray-800 text-white shadow-xl rounded-xl overflow-hidden">
      <div class="flex flex-col md:flex-row">
        <div class="md:w-1/2 p-6 bg-gray-700">
          <img :src="mainImage" alt="Imagen del Producto" class="w-full h-96 object-contain rounded-lg shadow-md">
          <div class="flex flex-wrap mt-4">
            <img v-for="image in product.images" :key="image.url" :src="image.url" alt="Imagen del Producto"
              class="w-20 h-20 object-cover m-1 border border-gray-500 rounded-lg transition-transform transform hover:scale-105 cursor-pointer"
              @click="updateMainImage(image.url)">
          </div>
        </div>
        <div class="p-6 md:w-1/2">
          <h1 class="text-4xl font-extrabold mb-3 text-white">{{ product.title }}</h1>
          <p class="text-gray-300 mb-6">{{ product.description }}</p>
          <div class="mb-6">
            <span class="text-3xl font-semibold text-green-400">${{ product.price }}</span>
            <span class="text-sm text-gray-400 line-through ml-2" v-if="product.discountPercentage">
              ${{ (product.price / (1 - product.discountPercentage / 100)).toFixed(2) }}
            </span>
            <span class="text-sm text-red-400 ml-2" v-if="product.discountPercentage">
              {{ product.discountPercentage }}% de descuento
            </span>
          </div>
          <div class="space-y-2">
            <div><span class="text-gray-300 font-medium">Categoría:</span> {{ product.category.name }}</div>
            <div><span class="text-gray-300 font-medium">Stock:</span> {{ product.stock }}</div>
            <div><span class="text-gray-300 font-medium">Marca:</span> {{ product.brand }}</div>
            <div><span class="text-gray-300 font-medium">SKU:</span> {{ product.sku }}</div>
            <div><span class="text-gray-300 font-medium">Peso:</span> {{ product.weight }} kg</div>
            <div><span class="text-gray-300 font-medium">Dimensiones:</span> {{ product.dimensions.width }} x
              {{ product.dimensions.height }} x {{ product.dimensions.depth }} cm</div>
            <div><span class="text-gray-300 font-medium">Garantía:</span> {{ product.warrantyInformation }}</div>
            <div><span class="text-gray-300 font-medium">Envío:</span> {{ product.shippingInformation }}</div>
            <div><span class="text-gray-300 font-medium">Disponibilidad:</span> {{ product.availabilityStatus }}</div>
            <div><span class="text-gray-300 font-medium">Política de Devolución:</span> {{ product.returnPolicy }}</div>
            <div><span class="text-gray-300 font-medium">Calificación:</span> {{ product.rating }}</div>
            <div><span class="text-gray-300 font-medium">Etiquetas:</span> {{ product.tags.map((tag) => tag.name).join(",") }}</div>
          </div>
            <div class="flex gap-4">
            <button @click="deleteProduct" class="mt-4 bg-red-600 hover:bg-red-800 text-white font-bold py-2 px-4 rounded-lg shadow-md transition-transform transform hover:scale-105">
              Eliminar Producto
            </button>
            <router-link :to="`/product/${$route.params.id}/edit`"
            class="mt-4 bg-blue-600 hover:bg-blue-800 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition-transform transform hover:scale-105">
            Editar Producto
            </router-link>
        </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="product && product.reviews.length" class="mt-6 mx-4 md:mx-8 lg:mx-12">
    <h2 class="text-2xl font-bold mb-4">Reseñas</h2>
    <div v-for="review in product.reviews" :key="review.reviewerEmail" class="bg-gray-700 p-4 rounded-lg mb-4">
      <div class="flex items-center mb-2">
        <span class="text-yellow-400 font-bold">{{ review.rating }} / 5</span>
        <span class="ml-2 text-gray-400">por {{ review.reviewerName }}</span>
      </div>
      <p class="text-gray-300">{{ review.comment }}</p>
      <span class="text-gray-500 text-sm">{{ new Date(review.date).toLocaleDateString() }}</span>
    </div>
  </div>
</template>
