<script setup lang="ts">
import { ref, computed, defineModel } from 'vue';

const inputVal = ref('')
const inputRef = ref<HTMLInputElement | null>(null)
//const inputVals = ref<string[]>([])
const whiteList = ref(["javascript", "dragon ball", "html"])
const dialogRef = ref<HTMLDialogElement | null>(null)

const inputVals = defineModel<string[]>({
  required: true
})

function onKey(event: KeyboardEvent) {
  if (event.key == "Enter" && inputVal.value?.trim() !== "") {
    const valueInLowerCase = inputVal.value.toLowerCase()


    if (inputVals.value.includes(valueInLowerCase)) {
      inputVal.value = ''
      return
    }

    if (!whiteList.value.includes(valueInLowerCase)) {
      if (dialogRef.value) {
        dialogRef.value.showModal()
        dialogRef.value.focus()
      }
      return
    }

    CreateTagByText(inputVal.value)

  }


  if (event.key == "Backspace" && inputVal.value == "") {
    inputVals.value.pop()
  }

}


function CreateTagByText(name: string) {
  inputVal.value = ""
  inputVals.value.push(name.toLowerCase())
}


function addToWhitelist() {
  whiteList.value.push(inputVal.value.toLowerCase())
  CreateTagByText(inputVal.value)
  if (dialogRef.value) dialogRef.value.close()
}

function removeElement(name: string) {
  inputVals.value = inputVals.value.filter((v) => !v.includes(name))
}

function DialogNo() {
  dialogRef.value?.close()
  inputVal.value = ''
  if (inputRef.value) inputRef.value.focus()
}


const filteredList = computed(() => {

  return whiteList.value.filter((v) => v.includes(inputVal.value.toLowerCase()) && !inputVals.value.includes(v))

})

</script>

<template>

  <input autocomplete="false" ref="inputRef" id="tags-input" autofocus @keydown="onKey" v-model="inputVal" />
  <label @click="inputRef?.focus()" class="tags" for="tags-input">

    <TransitionGroup name="list">

      <span @click="removeElement(word)" class="tag cursor-pointer capitalize" v-for="word in inputVals" :key="word">
        {{ word }}
      </span>
      <span class="input" key="input-vall">{{ inputVal }}</span>

    </TransitionGroup>

    <Transition name="options">
      <div class="options" v-if="filteredList.length > 0">
        <TransitionGroup name="list" tag="ul">
          <li @click="CreateTagByText(element)" v-for="element in filteredList" :key="element">
            <button class="capitalize">{{ element }}</button>
          </li>
        </TransitionGroup>
      </div>
    </Transition>

  </label>


  <dialog ref="dialogRef" class="p-2  focus-visible:outline-none">
    <div class="flex flex-col gap-4 p-6 ">
      <h3 class="text-center">Quieres agregar la siguiente categoria: <br /><span
          class="text-xl font-bold capitalize">{{ inputVal
          }}</span></h3>
      <div class="flex gap-4">
        <button class="bg-blue-500 px-2 py-1 rounded-sm  w-full hover:bg-blue-400 focus:outline-none focus:bg-blue-400"
          @click="addToWhitelist">yes</button>
        <button @click="DialogNo"
          class="bg-red-500 px-2 py-1 rounded-sm w-full hover:bg-red-400 focus:outline-none focus:bg-red-400">No</button>


      </div>



    </div>

  </dialog>





</template>


<style>
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
  position: absolute;
  top: 45px;
  left: 0px;
  width: 100%;
  border: 1px solid darkblue;

  ul {
    list-style: none;
    display: flex;
    gap: 4px;
    padding: 5px;
    margin: 0;



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
