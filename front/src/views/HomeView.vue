<script setup lang="ts">
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-dt'
import LenguageSpanish from 'datatables.net-plugins/i18n/es-MX.json'
import { onMounted, ref } from 'vue';
import type { Product } from '@/types/types';
import { getProducts } from '@/services/products';

const products = ref<Product[]>()
const table = ref()
DataTable.use(DataTablesCore);

const columns = [
  { data: 'id', title: 'ID' },
  { data: 'title', title: 'Título' },
  { data: 'price', title: 'Precio' },
  { data: 'category', title: 'Categoría' },
];

onMounted(() => {
  getProducts().then(data => {
    products.value = data
  })
})

</script>
<template>
  <main>
    <h1 class="text-center text-6xl">Pagina principal</h1>
    <p>aqui tal vez va algo mas</p>
    <div class="text-sm">
      <DataTable ref="table" class="cell-border hover stripe row-border order-column compact" :columns="columns"
        :data="products" :options="{ language: LenguageSpanish }">

      </DataTable>

    </div>


  </main>


</template>

<style>
@import 'datatables.net-dt'
</style>
