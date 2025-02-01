<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import type { TableRow } from '../stores/userStore'
//import type { VDataTable } from 'vuetify/components'


const store = useUserStore()
const { tableData, selectedFoodNutrients, expandedFoodNutrientsList } = storeToRefs(store)

const headers = [
  { title: 'Food1', key: 'food1_id' },
  { title: 'Food2', key: 'food2_id' },
  { title: 'Amount1', key: 'value1' },
  { title: 'Amount2', key: 'value2' },
  { title: 'Excess', key: 'excess' },
  { title: 'NDB', key: 'ndb_no2', hidden: true } // Hide from display
]

const expanded = ref<string[]>([])

const handleExpand = async (expandedRows: string[]) => {
  // Get previously expanded rows that are now collapsed
  const collapsedRows = expanded.value.filter(row => !expandedRows.includes(row))
  
  // Clear collapsed rows from store
  for (const ndb_no2 of collapsedRows) {
    store.clearExpandedFoodNutrients(Number(ndb_no2))
  }
  
  // Update expanded rows
  for (const ndb_no2 of expandedRows) {
    if (!expandedFoodNutrientsList.value[Number(ndb_no2)]) {
      await store.updateExpandedFoodNutrients(Number(ndb_no2))
    }
  }
  
  expanded.value = expandedRows
}

const calculateTotals = (item: TableRow) => {
  if (!selectedFoodNutrients.value) return null

  const expandedFoodNutrients = expandedFoodNutrientsList.value[item.ndb_no2]

  if (!expandedFoodNutrients) return null

  const totalMass = item.value1 + item.value2
  const totalEnergy =
      (selectedFoodNutrients.value.CAL_208_kcal * item.value1 / 100) +
      (expandedFoodNutrients.CAL_208_kcal * item.value2 / 100)

  return {
    mass: totalMass.toFixed(2),
    energy: totalEnergy.toFixed(2)
  }
}

watch(() => tableData.value, () => {
    expanded.value = [] // Reset expanded rows when table data changes
})
</script>

<template>
  <v-data-table
    :headers="headers"
    :items="tableData"
    :expanded="expanded"
    item-value="ndb_no2"
    show-expand
    @update:expanded="handleExpand"
  >
    <template v-slot:expanded-row="{ item }">
      <td :colspan="headers.length">
        <v-container v-if="calculateTotals(item)">
          <v-row>
            <v-col>Mass: {{ calculateTotals(item)?.mass }} g</v-col>
            <v-col>Energy: {{ calculateTotals(item)?.energy }} kcal</v-col>
          </v-row>
        </v-container>
      </td>
    </template>
  </v-data-table>
</template>