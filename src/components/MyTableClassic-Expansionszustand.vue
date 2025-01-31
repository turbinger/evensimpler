<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import type { TableRow } from '../stores/userStore'

const store = useUserStore()
const { tableData, selectedFoodNutrients, expandedFoodNutrients } = storeToRefs(store)

const headers = [
  { title: 'Food1', key: 'food1_id' },
  { title: 'Food2', key: 'food2_id' },
  { title: 'Amount1', key: 'value1' },
  { title: 'Amount2', key: 'value2' },
  { title: 'Excess', key: 'excess' }
]

const expanded = ref<string[]>([])
const previousExpanded = ref<string[]>([])

const handleExpand = async (newExpandedItems: string[]) => {
  if (!newExpandedItems) return;

  // Find newly expanded items by comparing with previous state
  const newlyExpanded = newExpandedItems.filter(id => !previousExpanded.value.includes(id));

  // For each newly expanded item, fetch its nutrient data
  for (const expandedId of newlyExpanded) {
    const expandedItem = tableData.value.find(item => item.food2_id === expandedId);
    if (expandedItem?.ndb_no2) {
      console.log('Fetching nutrients for NDB_No:', expandedItem.ndb_no2);
      await store.updateExpandedFoodNutrients(expandedItem.ndb_no2);
    }
  }

  // Update previous state
  previousExpanded.value = newExpandedItems;
}

// Update the calculateTotals function to use TableRow type
const calculateTotals = (item: TableRow) => {
  if (!selectedFoodNutrients.value || !expandedFoodNutrients.value) return null

  const totalMass = item.value1 + item.value2
  const totalEnergy =
      (selectedFoodNutrients.value.CAL_208_kcal * item.value1 / 100) +
      (expandedFoodNutrients.value.CAL_208_kcal * item.value2 / 100)

  return {
    mass: totalMass.toFixed(2),
    energy: totalEnergy.toFixed(2)
  }
}
</script>

<template>
  <v-data-table
      :headers="headers"
      :items="tableData"
      v-model:expanded="expanded"
      show-expand
      density="compact"
      item-value="food2_id"
      @update:expanded="handleExpand"
  >
    <template v-slot:expanded-row="{ item }">
      <td :colspan="headers.length">
        <v-card flat v-if="selectedFoodNutrients && expandedFoodNutrients">
          <v-card-text>
            <div class="d-flex justify-space-around">
              <div>
                <h3>Gesamtmasse: {{ calculateTotals(item)?.mass }} g</h3>
              </div>
              <div>
                <h3>Gesamtenergie: {{ calculateTotals(item)?.energy }} kcal</h3>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </td>
    </template>
  </v-data-table>
</template>