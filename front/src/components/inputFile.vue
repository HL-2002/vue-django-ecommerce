<script setup lang="ts">
import { ref, watch } from 'vue';

const emit = defineEmits(['changeMiniature', 'errorMaxFiles'])
const props = defineProps<{ initialImages: File[] }>()

const InputFile = ref<HTMLInputElement | null>(null)
const images = ref<{ id: string, url: string }[]>(props.initialImages ? props.initialImages.map(file => ({ id: file.name, url: URL.createObjectURL(file) })) : [])

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const filesList = target.files
  if (filesList) {
    if (filesList.length > 3) {
      emit('errorMaxFiles')
      return
    }

    const files = Array.from(filesList)
    images.value = files.map((file) => { return { id: file.name, url: URL.createObjectURL(file) } })
  }
}

function clickImage(image: { id: string, url: string }) {
  emit('changeMiniature', image)
}

watch(() => props.initialImages, (newImages) => {
  images.value = newImages ? newImages.map(file => ({ id: file.name, url: URL.createObjectURL(file) })) : []
  // insert the newImages into the input file
  if (InputFile.value) {
    const files = new DataTransfer()
    newImages.forEach(image => {
      files.items.add(new File([image], image.name))
    })
    InputFile.value.files = files.files
  }


}, { immediate: true })
</script>

<template>
  <label class="px-2 py-1 text-white rounded text-lg bg-blue-500 cursor-pointer">
    Subir imagenes
    <input accept="image/*" multiple @change="onFileChange" type="file" name="images" ref="InputFile"
      class="hidden absolute pointer-events-none" />
  </label>

  <div class="flex gap-4 border border-neutral-500 p-2 h-28">
    <img v-for="image in images" :src="image.url" :key="image.id" class="w-24 h-24 object-cover"
      @click="clickImage(image)" />
  </div>
</template>
