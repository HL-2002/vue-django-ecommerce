<script setup lang="ts">
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-dt'

DataTable.use(DataTablesCore);


const columns = [
  {
    title: 'Title',
    data: 'title',
  },
  {
    title: 'Price',
    data: 'price',
  },
]
const defaultData = Array.from({ length: 100 }, (_, i) => ({
  title: `Title ${i}`,
  price: Math.random() * 1000,
}))



</script>
<template>
  <main>
    <h1 class="text-center text-6xl">Pagina principal</h1>
    <p>aqui tal vez va algo mas</p>

    <DataTable :columns="columns" :data="defaultData">


    </DataTable>
  </main>
</template>

<style>
@import 'datatables.net-dt';
</style>
