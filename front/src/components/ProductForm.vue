<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import CategorySelector from "./CategorySelector.vue"
import NotificationDialog from './NotificationDialog.vue'
import InputFile from './inputFile.vue';
import { API_URL, createProduct, getCategories, getTags } from '@/services/products';
import type { Category, Tag, Product, NotificationSooner } from '@/types/types';

const selectedCategory = ref<Category[]>([])
const selectedTags = ref<Tag[]>([])
// put a default image for the miniature
const seletedMiniature = ref<{ id: string, url: string }>({ id: "algo", url: 'https://placehold.co/150/webp' })
const maxFilesError = ref(false)
const notification = ref<NotificationSooner>({ message: '', show: false, type: 'success' })
// null is the default value or date
const shippingDate = ref()

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
const tags = ref<{ id: number, name: string }[]>([])

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


async function submitForm(event: Event) {
  const formData = new FormData(event.target as HTMLFormElement)
  const images: File[] = formData.getAll('images') as File[]

  if (images.length < 3) {
    notification.value = {
      message: 'Se requieren al menos 3 imagenes',
      show: true,
      type: 'error'
    }
    return
  }

  if (selectedCategory.value.length === 0) {
    notification.value = {
      message: 'Se requiere una categoria',
      show: true,
      type: 'error'
    }
    return
  }


  if (selectedTags.value.length === 0) {
    notification.value = {
      message: 'Se requiere al menos un tag',
      show: true,
      type: 'error'
    }
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


  fetch(`${API_URL}/API/product/`, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then((data: Product) => {
      console.log(data)
    })
    .catch(err => {
      console.log(err)
    })

}


/* {
    "id": [
        "This field is required."
    ],
    "discountPercentage": [
        "This field is required."
    ],
    "rating": [
        "This field is required."
    ],
    "warrantyInformation": [
        "This field is required."
    ],
    "shippingInformation": [
        "This field is required."
    ],
    "returnPolicy": [
        "This field is required."
    ],
    "minimumOrderQuantity": [
        "This field is required."
    ],
    "thumbnail": [
        "No file was submitted."
    ],
    "dimensions": [
        "This field is required."
    ],
    "meta": [
        "This field is required."
    ],
    "tags": [
        "Incorrect type. Expected pk value, received str."
    ]
} */


</script>

<template>
  <NotificationDialog :show="notification.show" :message="notification.message" :type="notification.type"
    @close="notification.show = false" />
  <form enctype="multipart/form-data" @submit.prevent="submitForm" class="w-1/2 m-auto flex flex-col gap-4
    bg-neutral-100 p-6 rounded-lg shadow-md mb-4

  ">



    <h1 @click="notification.show = !notification.show" class="text-2xl font-bold text-center">Crea un producto</h1>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Titulo
      <input required type="text" name="title"
        class="text-sm font-normal p-2 border border-neutral-500 rounded  focus:outline-none focus:border-neutral-800" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Descripcion
      <textarea name="description"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <CategorySelector v-model="selectedCategory" label-name="Categorias" creation-name="categoria"
      :default-whitelist="categories" :limit="1" />
    <label class="flex flex-col gap-2 text-xl font-bold">
      Precio
      <input required step="0.01" type="number" name="price"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Porcentaje de descuento
      <input required step=".01" type="number" name="discountPercentage"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Rating
      <input value="5" required type="number" name="rating"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 disabled:opacity-50" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Stock
      <input required type="number" name="stock"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <CategorySelector v-model="selectedTags" label-name="Tags" creation-name="Tag" :default-whitelist="tags" />

    <label class="flex flex-col gap-2 text-xl font-bold">
      Marca
      <input required type="text" name="brand"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      SKU
      <input required type="text" name="sku"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Peso
      <input required type="number" name="weight"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Dimensiones
      <div class="flex gap-2">
        <div class="flex flex-col">
          <span>Ancho</span>
          <input type="number" name="width"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
        <div class="flex flex-col">
          <span>Alto</span>
          <input required type="number" name="height"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
        <div class="flex flex-col">
          <span>Profundidad</span>
          <input required type="number" name="depth"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
      </div>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de garantia
      <textarea required name="warrantyInformation"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de envio
      <input required name="shippingInformation"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"
        type="date" v-model="shippingDate" :min="tomorrow" />



      <span v-if="shippingFormated">
        Se envia {{ shippingFormated }}
      </span>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Estado de disponibilidad
      <select required name="availabilityStatus"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800">
        <option value="inStock">en existencia</option>
        <option value="lowStock">Baja cantidad</option>
      </select>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Politica de devolucion
      <textarea required name="returnPolicy"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Cantidad minima de orden
      <input required type="number" name="minimumOrderQuantity"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <InputFile @change-miniature="updateMiniature" @error-max-files="errorMaxFiles" />

    <label v-if="maxFilesError" class="text-red-500
text-sm font-bold

  ">Maximo de 3 imagenes</label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Miniatura
      <img :src="seletedMiniature.url" class="w-24 h-24 object-cover" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Codigo de barras
      <input required type="text" name="barcode"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <button type="submit" class="p-2 rounded bg-blue-500 text-white">Guardar</button>


  </form>
</template>
