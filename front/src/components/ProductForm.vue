<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import CategorySelector from "./CategorySelector.vue"
import InputFile from './inputFile.vue';
import { createProduct, getCategories, getTags } from '@/services/products';
import type { Category, } from '@/types/types';

const selectedCategory = ref<string[]>([])
const selectedTags = ref<string[]>([])
// put a default image for the miniature
const seletedMiniature = ref<{ id: string, url: string }>({ id: "algo", url: 'https://placehold.co/150/webp' })
const maxFilesError = ref(false)

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
const tags = ref<{id:number,name:string}[]>([])

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
  .then((data)=>{
    tags.value = data
    console.log(data)
  })
  .catch((err)=>{
    console.log(err)
  })


})


function submitForm(event: Event) {
  const formData = new FormData(event.target as HTMLFormElement)

  const images: File[] = formData.getAll('images') as File[]
  let thumbnail = images.find((image) => image.name === seletedMiniature.value.id)
  if (!thumbnail) {
    thumbnail = images[0]
  }


  formData.append('category', selectedCategory.value[0])
  formData.append('tags', selectedTags.value.join(','))
  formData.append('thumnail', thumbnail as File)



}




</script>

<template>
  <form @submit.prevent="submitForm" class="w-1/2 m-auto flex flex-col gap-4
    bg-neutral-100 p-6 rounded-lg shadow-md mb-4

  ">



    <h1 class="text-2xl font-bold text-center">Crea un producto</h1>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Titulo
      <input type="text" name="title"
        class="text-sm font-normal p-2 border border-neutral-500 rounded  focus:outline-none focus:border-neutral-800" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Descripcion
      <textarea name="description"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <CategorySelector v-model="selectedCategory" label-name="Categorias" creation-name="categoria"
      :default-whitelist="categories" :limit="1"/>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Precio
      <input step="0.01" type="number" name="price"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Porcentaje de descuento
      <input step=".01" ype="number" name="discount"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Rating
      <input disabled value="5" step=".01" type="number" name="rating"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 disabled:opacity-50" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Stock
      <input type="number" name="stock"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <CategorySelector v-model="selectedTags" label-name="Tags" creation-name="Tag" :default-whitelist="tags" />

    <label class="flex flex-col gap-2 text-xl font-bold">
      Marca
      <input type="text" name="brand"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      SKU
      <input type="text" name="sku"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Peso
      <input type="number" name="weight"
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
          <input type="number" name="height"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
        <div class="flex flex-col">
          <span>Profundidad</span>
          <input type="number" name="depth"
            class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
      </div>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de garantia
      <textarea name="warranty"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de envio
      <input name="shipping"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"
        type="date" v-model="shippingDate" :min="tomorrow" />



      <span v-if="shippingFormated">
        Se envia {{ shippingFormated }}
      </span>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Estado de disponibilidad
      <select name="availability"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800">
        <option value="inStock">en existencia</option>
        <option value="lowStock">Baja cantidad</option>
      </select>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Politica de devolucion
      <textarea name="return"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Cantidad minima de orden
      <input type="number" name="minOrder"
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
      <input type="text" name="barcode"
        class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <button type="submit" class="p-2 rounded bg-blue-500 text-white">Guardar</button>


  </form>
</template>
