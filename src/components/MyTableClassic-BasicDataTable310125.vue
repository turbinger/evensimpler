<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'

const store = useUserStore()
const { tableData } = storeToRefs(store)

const headers = [
  { title: 'Food1', key: 'food1_id' },
  { title: 'Food2', key: 'food2_id' },
  { title: 'Amount1', key: 'value1' },
  { title: 'Amount2', key: 'value2' },
  { title: 'Excess', key: 'excess' }
]

const handleRowClick = (event: { item: any }) => {
  const row = event.item.raw  // In Vuetify 3, die Daten sind in .raw
  console.log('Clicked row:', row);
  // Hier später weitere Logik
}
</script>

<template>
  <v-data-table
      :headers="headers"
      :items="tableData"
      hover
      @click:row="handleRowClick"
      density="compact"
  ></v-data-table>
</template>