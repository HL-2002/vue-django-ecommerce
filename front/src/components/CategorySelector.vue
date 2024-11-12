<script setup lang="ts">
import { ref, computed } from 'vue';

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
    type: Array as () => string[],
    required: true
  }

})


const textInput = ref('')
const inputRef = ref<HTMLInputElement | null>(null)
const whiteList = ref<string[]>(props.defaultWhitelist)
const dialogRef = ref<HTMLDialogElement | null>(null)

const seletedCategories = defineModel<string[]>({
  required: true
})

function onKey(event: KeyboardEvent) {
  if (event.key == "Enter" && textInput.value?.trim() !== "") {
    const valueInLowerCase = textInput.value.toLowerCase()
    if (seletedCategories.value.includes(valueInLowerCase)) {
      textInput.value = ''
      return
    }

    if (!whiteList.value.includes(valueInLowerCase)) {
      if (dialogRef.value) {
        dialogRef.value.showModal()
        dialogRef.value.focus()
      }
      return
    }

    CreateTagByText(textInput.value)

  }


  if (event.key == "Backspace" && textInput.value == "") {
    seletedCategories.value.pop()
  }

}


function CreateTagByText(name: string) {
  textInput.value = ""
  seletedCategories.value.push(name.toLowerCase())
}


function addToWhitelist() {
  whiteList.value.push(textInput.value.toLowerCase())
  CreateTagByText(textInput.value)
  if (dialogRef.value) dialogRef.value.close()
}

function removeElement(name: string) {
  seletedCategories.value = seletedCategories.value.filter((v) => !v.includes(name))
}

function DialogNo() {
  dialogRef.value?.close()
  textInput.value = ''
  if (inputRef.value) inputRef.value.focus()
}


const filteredList = computed(() => {

  return whiteList.value.filter((v) => v.includes(textInput.value.toLowerCase()) && !seletedCategories.value.includes(v))

})

</script>

<template>

  <div class="categoriContainer">
    <h3 class="font-bold text-xl mb-4">{{ props.labelName }}</h3>
  <input autocomplete="false" ref="inputRef" :id="props.labelName" autofocus @keydown="onKey" v-model="textInput" />
  <label @click="inputRef?.focus()" class="tags" for="tags-input">

    <TransitionGroup name="list">

      <span @click="removeElement(word)" class="tag cursor-pointer capitalize" v-for="word in seletedCategories"
        :key="word">
        {{ word }}
      </span>
      <span class="input" key="input-vall">{{ textInput }}</span>

    </TransitionGroup>

  </label>
    <Transition name="options">
      <div class="options" v-if="filteredList.length > 0">
        <TransitionGroup name="list" tag="ul">
          <li @click="CreateTagByText(element)" v-for="element in filteredList" :key="element">
            <button type="button" class="capitalize">{{ element }}</button>
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
        <button type="button" class="bg-blue-500 px-2 py-1 rounded-sm  w-full hover:bg-blue-400 focus:outline-none focus:bg-blue-400"
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

.categoriContainer

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
