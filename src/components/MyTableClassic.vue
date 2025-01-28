<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import { ref, computed } from 'vue'

const store = useUserStore()
const { tableData } = storeToRefs(store)

// Sortierzustand
const currentSortColumn = ref<string | null>(null) // Initial null
const isAscending = ref<boolean>(true)

// Sortierbare Spalten definieren
const columns = [
  { label: 'Food1', field: 'food1_id' },
  { label: 'Food2', field: 'food2_id' },
  { label: 'Amount1', field: 'value1' },
  { label: 'Amount2', field: 'value2' },
  { label: 'Excess', field: 'excess' }
]

// Sortierte Daten als computed property
const sortedData = computed(() => {
  if (!tableData.value || !currentSortColumn.value) return tableData.value || [] // Leeres Array zurückgeben, wenn keine Sortierung aktiv ist

  return [...tableData.value].sort((a, b) => {
    const aValue = a[currentSortColumn.value!] // Nicht null, da im if geprüft
    const bValue = b[currentSortColumn.value!] // Nicht null, da im if geprüft

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return isAscending.value ? aValue - bValue : bValue - aValue
    }

    return isAscending.value
        ? String(aValue).localeCompare(String(bValue))
        : String(bValue).localeCompare(String(aValue))
  })
})

// Sortierfunktion
const sortBy = (field: string) => {
  if (currentSortColumn.value === field) {
    isAscending.value = !isAscending.value
  } else {
    currentSortColumn.value = field
    isAscending.value = true
  }
}
</script>

<template>
  <div class="container mt-4">
    <h3>Users:</h3>
    <table class="table table-striped">
      <thead>
      <tr>
        <th
            v-for="column in columns"
            :key="column.field"
            @click="sortBy(column.field)"
            style="cursor: pointer"
        >
          {{ column.label }}
          <span v-if="currentSortColumn === column.field">
              {{ isAscending ? '▲' : '▼' }}
            </span>
        </th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(row, index) in sortedData" :key="index">
        <td>{{ row.food1_id }}</td>
        <td>{{ row.food2_id }}</td>
        <td>{{ row.value1 }}</td>
        <td>{{ row.value2 }}</td>
        <td>{{ row.excess }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>