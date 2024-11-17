<script setup lang="ts">
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-dt'
import LenguageSpanish from 'datatables.net-plugins/i18n/es-MX.json'
import { onMounted, ref } from 'vue';
import type { Product } from '@/types/types';
import { getProducts } from '@/services/products';

import { useRouter } from 'vue-router';

const router = useRouter()

const products = ref<Product[]>()
const table = ref()
DataTable.use(DataTablesCore);

const columns = [
  { data: 'id', title: 'ID' },
  { data: 'title', title: 'Título' },
  { data: 'price', title: 'Precio' },
  { data: 'category.name', title: 'Categoría' },
];

onMounted(() => {
  getProducts().then(data => {
    products.value = data
  })

  const dt = table.value.dt
  dt.on('click', 'tr', function (this: HTMLElement) {
    const data = dt.row(this).data()

    router.push({ name: 'product', params: { id: data.id } })

  })


})

</script>
<template>
  <main>
    <div class="text-sm p-10">
      <DataTable ref="table" class="cell-border hover stripe row-border order-column compact" :columns="columns"
        :data="products" :options="{ language: LenguageSpanish }">
      </DataTable>

    </div>


  </main>


</template>

<style>
@import 'datatables.net-dt'
</style>
