<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue';
import CategorySelector from "./CategorySelector.vue"
import InputFile from './inputFile.vue';
import { API_URL, getCategories, getTags, getProductById } from '@/services/products';
import type { Category, Tag, Product } from '@/types/types';
import { useNotificationStore } from '@/stores/notification';

const props = defineProps<{ productId?: string }>();

const notification = useNotificationStore()
const { notify } = notification

const selectedCategory = ref<Category[]>([])
const selectedTags = ref<Tag[]>([])
const seletedMiniature = ref<{ id: string, url: string }>({ id: "algo", url: 'https://placehold.co/150/webp' })
const maxFilesError = ref(false)
const shippingDate = ref()
const formData = ref({
  title: '',
  description: '',
  price: 0,
  discountPercentage: 0,
  rating: 5,
  stock: 0,
  brand: '',
  sku: '',
  weight: 0,
  dimensions: {
    width: 0,
    height: 0,
    depth: 0
  },
  warrantyInformation: '',
  shippingInformation: '',
  availabilityStatus: 'inStock',
  returnPolicy: '',
  minimumOrderQuantity: 1,
  barcode: ''
});

const images = ref<File[]>([])


function updateMiniature(image: { id: string, url: string }) {
  seletedMiniature.value = image
}

function errorMaxFiles() {
  maxFilesError.value = true
  setTimeout(() => {
    maxFilesError.value = false
  }, 3000)
}

const intlFormatDateShort = new Intl.RelativeTimeFormat('es', { numeric: 'auto' })

function formatTime(date: Date) {
  const currentDate = new Date()
  const shipping = new Date(date)
  const diff = shipping.getTime() - currentDate.getTime()
  const moths = Math.floor(diff / (1000 * 60 * 60 * 24 * 30))
  if (moths > 0) return intlFormatDateShort.format(moths, 'month')
  const weeks = Math.floor(diff / (1000 * 60 * 60 * 24 * 7))
  if (weeks > 0) return intlFormatDateShort.format(weeks, 'week')
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days > 0) return intlFormatDateShort.format(days, 'day')
  const hours = Math.floor(diff / (1000 * 60 * 60))
  if (hours > 0) return intlFormatDateShort.format(hours, 'hour')
}

const shippingFormated = computed(() => {
  if (!shippingDate.value) return ''
  return formatTime(shippingDate.value)
})

let tomorrow: Date | string = new Date()
tomorrow.setDate(tomorrow.getDate() + 1)
tomorrow = new Date(tomorrow.toISOString().split('T')[0]).toISOString().split('T')[0]

const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

onMounted(() => {
  getCategories()
    .then(data => {
      categories.value = data
      console.log(data)
    })
    .catch(err => {
      console.log(err)
    })

  getTags()
    .then((data) => {
      tags.value = data
      console.log(data)
    })
    .catch((err) => {
      console.log(err)
    })
})

watch(() => props.productId, (newId) => {
  console.log(newId)
  if (newId) {
    loadProduct(newId);
  }
}, { immediate: true });

async function loadProduct(productId: string) {
  try {
    const product = await getProductById(productId);
    formData.value = {
      title: product.title,
      description: product.description,
      price: product.price,
      discountPercentage: product.discountPercentage,
      rating: product.rating,
      stock: product.stock,
      brand: product.brand,
      sku: product.sku,
      weight: product.weight,
      dimensions: {
        width: product.dimensions.width,
        height: product.dimensions.height,
        depth: product.dimensions.depth
      },
      warrantyInformation: product.warrantyInformation,
      shippingInformation: product.shippingInformation,
      availabilityStatus: product.availabilityStatus,
      returnPolicy: product.returnPolicy,
      minimumOrderQuantity: product.minimumOrderQuantity,
      barcode: product.meta.barcode,
    };
    selectedCategory.value = [product.category]
    selectedTags.value = product.tags
    seletedMiniature.value = { id: product.thumbnail, url: product.thumbnail };
    shippingDate.value = new Date(product.shippingInformation);

    images.value = await Promise.all(product.images.map(async (image) => await toFile(image.url)));
  } catch (err) {
    console.log(err);
  }
}

async function toFile(url: string) {
  const response = await fetch(url)
  const name = new URL(url).pathname.split('/').pop()
  const blob = await response.blob()
  return new File([blob], name || crypto.randomUUID())
}




async function submitForm(event: Event) {
  const formData = new FormData(event.target as HTMLFormElement)
  const images: File[] = formData.getAll('images') as File[]
  // set image in formData,how image.url
  formData.delete('images')

  images.forEach((image, index) => {
    formData.append(`images`, image)
  })


  console.log(images)
  if (images.length < 3) {
    notify({
      message: 'Se requieren al menos 3 imagenes',
      type: 'error'
    })
    return
  }
  if (selectedCategory.value.length === 0) {
    notify({
      message: 'Se requiere una categoria',
      type: 'error'
    })
    return
  }

  if (selectedTags.value.length === 0) {
    notify({
      message: 'Se requiere al menos un tag',
      type: 'error'
    })
    return
  }

  let thumbnail = images.find((image) => image.name === seletedMiniature.value.id)
  if (!thumbnail) {
    thumbnail = images[0]
  }

  formData.append('category', selectedCategory.value[0].id.toString())
  formData.append('thumbnail', thumbnail as File)

  formData.append('dimensions.depth', formData.get('depth') as string)
  formData.append('dimensions.width', formData.get("width") as string)
  formData.append('dimensions.height', formData.get("height") as string)

  selectedTags.value.forEach((tag) => {
    formData.append('tags', tag.id.toString())
  })

  formData.append("meta", formData.get("barcode") as string)
  formData.append("meta.barcode", formData.get("barcode") as string)

  // comprueba que el formData si tenga las imagenes
  for (let [key, value] of formData.entries()) {
    console.log(key, value)
  }

  try {
    let response;
    if (props.productId) {
      response = await fetch(`${API_URL}/API/product/${props.productId}/`, {
        method: 'PUT',
        body: formData
      });
    } else {
      response = await fetch(`${API_URL}/API/product/`, {
        method: 'POST',
        body: formData
      });
    }

    if (!response.ok) {
      notify({
        message: 'Error al crear el producto',
        type: 'error'
      })
      return
    }
    if (!props.productId) {
      const data: Product = await response.json();
      const url = `${window.location.origin}/product/${data.id}`

      const divElement = document.createElement('div')
      new QRCode(divElement, url)
      const canvas = divElement.getElementsByTagName("canvas")
      const qrCodeFile = await new Promise((resolve, reject) => {
      canvas[0].toBlob((blob) => {
        if (blob) {
        resolve(new File([blob], 'qrCode.png'))
        } else {
        reject(new Error('Failed to create QR code blob'))
        }
      })
      })

      const qrCodeForm = new FormData()
      qrCodeForm.append('meta', data.meta.id.toString())
      qrCodeForm.append('url', qrCodeFile as File)

      response = await fetch(`${API_URL}/API/qrCode/`, {
      method: 'POST',
      body: qrCodeForm
      })
    }

    if (response.ok) {
      notify({
      message: props.productId ? 'Producto actualizado' : 'Producto creado',
      type: 'success'
      })
    }
  } catch (err) {
    console.log(err)
    notify({
      message: 'Error al crear el producto',
      type: 'error'
    })
  }
}

function throwNotification() {
  notify({
    message: 'hola',
    type: 'success'
  })
}
</script>

<template>
  <form enctype="multipart/form-data" @submit.prevent="submitForm"
    class="w-full max-w-2xl mx-auto flex flex-col gap-4 bg-gray-800 p-6 rounded-lg shadow-md mb-4 text-white mt-4">
    <h1 @click="throwNotification" class="text-2xl font-bold text-center mb-4">{{
    props.productId ? 'Editar Producto' : 'Crear Producto'
    }}</h1>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Titulo
      <input v-model="formData.title" required type="text" name="title"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Descripcion
      <textarea v-model="formData.description" name="description"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white"></textarea>
    </label>
    <CategorySelector v-model="selectedCategory" label-name="Categorias" creation-name="categoria"
      :default-whitelist="categories" :limit="1" />
    <label class="flex flex-col gap-2 text-xl font-bold">
      Precio
      <input v-model="formData.price" required step="0.01" type="number" name="price"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Porcentaje de descuento
      <input v-model="formData.discountPercentage" required step=".01" type="number" name="discountPercentage"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Rating
      <input v-model="formData.rating" required type="number" name="rating"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 disabled:opacity-50 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Stock
      <input v-model="formData.stock" required type="number" name="stock"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <CategorySelector v-model="selectedTags" label-name="Tags" creation-name="Tag" :default-whitelist="tags" />
    <label class="flex flex-col gap-2 text-xl font-bold">
      Marca
      <input v-model="formData.brand" required type="text" name="brand"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      SKU
      <input v-model="formData.sku" required type="text" name="sku"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Peso
      <input v-model="formData.weight" required type="number" name="weight"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Dimensiones
      <div class="flex flex-col md:flex-row gap-2">
        <div class="flex flex-col">
          <span>Ancho</span>
          <input v-model="formData.dimensions.width" type="number" name="width"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
        </div>
        <div class="flex flex-col">
          <span>Alto</span>
          <input v-model="formData.dimensions.height" required type="number" name="height"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
        </div>
        <div class="flex flex-col">
          <span>Profundidad</span>
          <input v-model="formData.dimensions.depth" required type="number" name="depth"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
        </div>
      </div>
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de garantia
      <textarea v-model="formData.warrantyInformation" required name="warrantyInformation"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white"></textarea>
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de envio
      <input v-model="formData.shippingInformation" required name="shippingInformation" type="date" :min="tomorrow"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
      <span v-if="shippingFormated">
        Se envia {{ shippingFormated }}
      </span>
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Estado de disponibilidad
      <select v-model="formData.availabilityStatus" required name="availabilityStatus"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white">
        <option value="inStock">en existencia</option>
        <option value="lowStock">Baja cantidad</option>
      </select>
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Politica de devolucion
      <textarea v-model="formData.returnPolicy" required name="returnPolicy"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white"></textarea>
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Cantidad minima de orden
      <input v-model="formData.minimumOrderQuantity" required type="number" name="minimumOrderQuantity"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <InputFile @change-miniature="updateMiniature" @error-max-files="errorMaxFiles" :initialImages="images" />
    <label v-if="maxFilesError" class="text-red-500 text-sm font-bold">Maximo de 3 imagenes</label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Miniatura
      <img :src="seletedMiniature.url" class="w-24 h-24 object-cover" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Codigo de barras
      <input v-model="formData.barcode" required type="text" name="barcode"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 bg-gray-700 text-white" />
    </label>
    <button type="submit"
      class="p-2 rounded bg-blue-500 text-white hover:bg-blue-600 transition-colors">
      {{ props.productId ? 'Editar Producto' : 'Crear Producto' }}
    </button>
  </form>
</template>
