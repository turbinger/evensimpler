<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import { ref, computed } from 'vue'

const store = useUserStore()
const { tableData } = storeToRefs(store)

const currentSortColumn = ref<string | null>(null)
const isAscending = ref<boolean>(true)

const columns = [
  { label: 'Food1', field: 'food1_id' },
  { label: 'Food2', field: 'food2_id' },
  { label: 'Amount1', field: 'value1' },
  { label: 'Amount2', field: 'value2' },
  { label: 'Excess', field: 'excess' }
]

const sortedData = computed(() => {
  if (!tableData.value || !currentSortColumn.value) return tableData.value || []

  return [...tableData.value].sort((a, b) => {
    const aValue = a[currentSortColumn.value!]
    const bValue = b[currentSortColumn.value!]

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return isAscending.value ? aValue - bValue : bValue - aValue
    }

    return isAscending.value
        ? String(aValue).localeCompare(String(bValue))
        : String(bValue).localeCompare(String(aValue))
  })
})

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
  <v-container class="mt-4">
    <h3>Users:</h3>
    <v-table>
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
    </v-table>
  </v-container>
</template>