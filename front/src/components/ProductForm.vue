<script setup lang="ts">
import { ref } from 'vue';
import CategorySelector from "./CategorySelector.vue"
import InputFile from './inputFile.vue';

const selectedCategory = ref<string[]>([])
const selectedTags = ref<string[]>([])
// put a default image for the miniature
const seletedMiniature = ref<string>('https://placehold.co/150/webp')
const maxFilesError = ref(false)


function updateMiniature(image: string) {
  seletedMiniature.value = image
}

function errorMaxFiles(){
  maxFilesError.value = true
  setTimeout(() => {
    maxFilesError.value = false
  }, 3000)
}


</script>


<template>
  <form class="w-1/2 m-auto flex flex-col gap-4">
    <h1>Producto Formulario</h1>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Titulo
      <input type="text" name="title" class="text-sm font-normal p-2 border border-neutral-500 rounded  focus:outline-none focus:border-neutral-800" />
    </label>
    <label class="flex flex-col gap-2 text-xl font-bold">
      Descripcion
      <textarea name="description" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <CategorySelector v-model="selectedCategory" label-name="Categorias" creation-name="categoria" :default-whitelist="['cocina','electrodomesticos']" />
   <label class="flex flex-col gap-2 text-xl font-bold">
      Precio
      <input step="0.01" type="number" name="price" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Porcentaje de descuento
      <input step=".01" ype="number" name="discount" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Rating
      <input disabled value="5" step=".01" type="number" name="rating" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800 disabled:opacity-50" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Stock
      <input type="number" name="stock" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

   <CategorySelector v-model="selectedTags" label-name="Tags" creation-name="Tag"  :default-whitelist="['']"/>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Marca
      <input type="text" name="brand" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      SKU
      <input type="text" name="sku" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Peso
      <input type="number" name="weight" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Dimensiones
      <div class="flex gap-2">
        <div class="flex flex-col">
          <span>Ancho</span>
          <input type="number" name="width" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
        <div class="flex flex-col">
          <span>Alto</span>
          <input type="number" name="height" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
        <div class="flex flex-col">
          <span>Profundidad</span>
          <input type="number" name="depth" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
        </div>
      </div>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de garantia
      <textarea name="warranty" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Informacion de envio
      <textarea name="shipping" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Estado de disponibilidad
      <select name="availability" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800">
        <option value="available">Disponible</option>
        <option value="unavailable">No disponible</option>
      </select>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Politica de devolucion
      <textarea name="return" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800"></textarea>
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Cantidad minima de orden
      <input type="number" name="minOrder" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>

  <InputFile @change-miniature="updateMiniature"  @error-max-files="errorMaxFiles" />

  <label v-if="maxFilesError" class="text-red-500
text-sm font-bold

  ">Maximo de 3 imagenes</label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Miniatura
      <img :src="seletedMiniature" class="w-24 h-24 object-cover" />
    </label>

    <label class="flex flex-col gap-2 text-xl font-bold">
      Codigo de barras
      <input type="text" name="barcode" class="text-sm font-normal p-2 border border-neutral-500 rounded focus:outline-none focus:border-neutral-800" />
    </label>


    <label class="flex flex-col gap-2 text-xl font-bold">
      <button type="button" class="bg-primary
-500  p-2 rounded">Agregar Review</button>
    </label>


    <button type="submit" class="bg-primary-500 p-2 rounded">Guardar</button>


  </form>
</template>
