<script setup lang="ts">
import { createCategory, createTag } from '@/services/products';
import type { Category } from '@/types/types';
import { ref, computed, watchEffect, watch } from 'vue';

const props = defineProps({
  labelName: {
    type: String,
    required: true
  },
  creationName: {
    type: String,
    required: true
  },
  defaultWhitelist: {
    type: Array as () => Category[],
    required: true
  },
  limit: {
    type: Number
  }

})

const textInput = ref('')
const inputRef = ref<HTMLInputElement | null>(null)
const whiteList = ref<Category[]>(props.defaultWhitelist)
const dialogRef = ref<HTMLDialogElement | null>(null)

const seletedCategories = defineModel<Category[]>({
  required: true
})

watchEffect(() => {
  whiteList.value = props.defaultWhitelist
})



function onKey(event: KeyboardEvent) {
  if (event.key == "Enter" && textInput.value?.trim() !== "") {
    const valueInLowerCase = textInput.value.toLowerCase()
    if (seletedCategories.value.some((v) => v.name.toLowerCase() == valueInLowerCase)) {
      textInput.value = ''
      return
    }

    const isInWhiteList = whiteList.value.some((v) => v.name.toLowerCase() == valueInLowerCase)

    if (!isInWhiteList) {
      if (dialogRef.value) {
        dialogRef.value.showModal()
        dialogRef.value.focus()
      }
      return
    }

    const newCategory = whiteList.value.find((v) => v.name.toLowerCase() == valueInLowerCase)!

    CreateTagByText(newCategory)

  }


  if (event.key == "Backspace" && textInput.value == "") {
    seletedCategories.value.pop()
  }

}


function CreateTagByText(newCategory: Category) {
  if (props.limit !== undefined && props.limit == seletedCategories.value.length) {
    seletedCategories.value.pop()
  }
  textInput.value = ""
  seletedCategories.value.push(newCategory)
}


async function addToWhitelist() {
  if (props.labelName == "Tags") {
    createTag({ name: textInput.value.toLowerCase() }).then((data) => {
      whiteList.value.push(data)
      CreateTagByText(data)
    })
    if (dialogRef.value) dialogRef.value.close()
    return
  }


  createCategory({ name: textInput.value.toLowerCase() }).then((data) => {
    whiteList.value.push(data)
    CreateTagByText(data)
    if (dialogRef.value) dialogRef.value.close()
  })
}

function removeElement(id: number) {
  seletedCategories.value = seletedCategories.value.filter((v) => v.id !== id)
}

function DialogNo() {
  dialogRef.value?.close()
  textInput.value = ''
  if (inputRef.value) inputRef.value.focus()
}


function isInWhiteList(name: string) {
  return whiteList.value.some((v) => v.name.toLowerCase() == name.toLowerCase())
}

function isInCategories(name: string) {
  return seletedCategories.value.some((v) => v.name == name)
}



const filteredList = computed(() => {

  return whiteList.value.filter((v) => v.name.toLowerCase().includes(textInput.value.toLowerCase()) && !isInCategories(v.name))

})



</script>

<template>

  <div class="categoriContainer">
    <h3 class="font-bold text-xl mb-4">{{ props.labelName }}</h3>
    <input autocomplete="false" ref="inputRef" :id="props.labelName" autofocus @keydown="onKey" v-model="textInput" />
    <label @click="inputRef?.focus()" class="tags" for="tags-input">

      <TransitionGroup name="list">

        <span @click="removeElement(word.id)" class="tag cursor-pointer capitalize" v-for="word in seletedCategories"
          :key="word.id">
          {{ word.name }}
        </span>
        <span class="input" key="input-vall">{{ textInput }}</span>

      </TransitionGroup>

    </label>
    <Transition name="options">
      <div class="options" v-if="filteredList.length > 0">
        <TransitionGroup name="list" tag="ul">
          <li @click="CreateTagByText(element)" v-for="element in filteredList" :key="element.id">
            <button type="button" class="capitalize">{{ element.name }}</button>
          </li>
        </TransitionGroup>
      </div>
    </Transition>

  </div>

  <dialog ref="dialogRef" class="p-2  focus-visible:outline-none">
    <div class="flex flex-col gap-4 p-6 ">
      <h3 class="text-center">Quieres agregar la siguiente {{ props.creationName }}: <br /><span
          class="text-xl font-bold capitalize">{{ textInput
          }}</span></h3>
      <div class="flex gap-4">
        <button type="button"
          class="bg-blue-500 px-2 py-1 rounded-sm  w-full hover:bg-blue-400 focus:outline-none focus:bg-blue-400"
          @click="addToWhitelist">yes</button>
        <button @click="DialogNo"
          class="bg-red-500 px-2 py-1 rounded-sm w-full hover:bg-red-400 focus:outline-none focus:bg-red-400">No</button>


      </div>



    </div>

  </dialog>





</template>


<style scoped>
* {
  box-sizing: border-box;
}


.options-enter-active,
.options-leave-active {
  transition: all 0.4s ease;
  max-height: 250px
}

.options-enter-from,
.options-leave-to {
  max-height: 0;
  overflow: hidden;
}

.list-move,
/* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: scale(0);
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
  position: absolute;
}


.options {
  position: relative;
  left: 0px;
  width: 100%;
  border: 1px solid darkblue;
  background: white;

  ul {
    list-style: none;
    display: flex;
    gap: 4px;
    padding: 5px;
    margin: 0;
    flex-wrap: wrap;


    li {
      button {
        background-color: #ddd;
        padding: 5px 5px;
        border: 1px solid gray;
        width: 100%;
        height: 100%;
        font-size: inherit;
        transition: transform 100ms;

        &:focus-visible,
        &:hover {
          background-color: #bbb;
          outline: none;
          transform: scale(1.1);
        }


      }
    }


  }


}


input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.tags {
  border: 1px solid;
  padding: 8px;
  display: flex;
  gap: 7px;
  position: relative;
  flex-wrap: wrap;
  background-color: white;

  .tag {
    background-color: lightskyblue;
    padding: 2px 4px;
    border-radius: 2px;

    transition: all 0.100s ease;

    &:hover {
      background-color: lightblue;
      transform: scale(1.1);
    }

  }


}


@keyframes inputA {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 100;
  }
}

.input {
  line-height: normal;
  padding: 2px 4px;
  height: 26px;
}


input:focus+label .input::after {
  content: "|";
  font-size: 16px;
  animation: inputA 1s infinite ease-in-out;
}
</style>
