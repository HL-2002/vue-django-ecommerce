<script setup lang="ts" >

import { ref } from 'vue';

// defini chamge miniature
const emit = defineEmits(['changeMiniature','errorMaxFiles'])

const files = ref<File[]>([])
const images = ref<string[]>([])

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const filesList = target.files
  if (filesList) {
    if (filesList.length > 3) {
      emit('errorMaxFiles')
      return
    }

    files.value = Array.from(filesList)
    const urls = files.value.map((file) => URL.createObjectURL(file))
    console.log(urls)
    images.value = urls
  }
}


  function clickImage(image: string) {
    emit('changeMiniature', image)
  }





</script>



<template>
<!-- make style button -->
<label class="px-2 py-1 text-white rounded text-lg bg-blue-500 cursor-pointer">
      Subir imagenes
      <input
      accept="image/*"
      multiple
      @change="onFileChange" type="file" name="images" class="hidden absolute pointer-events-none" />
</label>

<div class="flex gap-4 border border-neutral-500 p-2 h-28">
  <img v-for="image in images" :src="image" :key="image" class="w-24 h-24 object-cover"
  @click="clickImage(image)"
  />
</div>

</template>
