<script setup lang="ts">



</script>



<template>
  <form class="w-1/2 m-auto flex flex-col gap-4 bg-neutral-100 p-4 justify-center rounded shadow-lg">
    <label for="product">Product</label>
    <select name="product" id="product" class="bg-white border border-gray-300 rounded">
      <option>aluminio</option>
      <option>pc gamer</option>
    </select>

    <label for="name">Name</label>
    <input type="text" name="name" id="name" class="border border-gray-300 rounded">

    <label for="email">Email</label>
    <input type="email" name="email" id="email" class="border border-gray-300 rounded">

    <label for="date">Date</label>
    <input type="date" name="date" id="date" class="border border-gray-300 rounded">

    <label for="rating">Rating</label>
    <input type="number" name="rating" id="rating" min="1" max="5" class="border border-gray-300 rounded">

    <label for="comment">Comment</label>
    <textarea name="comment" id="comment" class="border border-gray-300 rounded"></textarea>

    <button class="bg-blue-500 rounded w-fit text-white px-2 py-1 m-auto" type="submit">Registrar</button>
  </form>
</template>
