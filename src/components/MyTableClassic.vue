<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import type { TableRow } from '../stores/userStore'
import AminoAcidChart from './AminoAcidChart.vue'


const store = useUserStore()
const { tableData, selectedFoodNutrients, expandedFoodNutrientsList } = storeToRefs(store)

const headers = [
  { title: 'Food1', key: 'food1_id', hidden: true },
  { title: '+Food2', key: 'food2_id' },
  { title: 'Amount1', key: 'value1' },
  { title: 'Amount2', key: 'value2' },
  { title: 'Excess', key: 'excess' },
  { title: 'NDB', key: 'ndb_no2', hidden: true }
]

const displayedHeaders = computed(() => headers.filter(h => !h.hidden))

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

const dialogOpen = ref(false)
const selectedChartItem = ref<TableRow | null>(null)

const openLargeChart = (item: TableRow) => {
  selectedChartItem.value = item
  dialogOpen.value = true
}
</script>

<template>
  <v-data-table
      :headers="displayedHeaders"
      :items="tableData"
      :expanded="expanded"
      item-value="ndb_no2"
      show-expand
      @update:expanded="handleExpand"
  >
    <template v-slot:expanded-row="{ item }">
      <td :colspan="headers.length">
        <v-container>
          <v-row>
            <v-col cols="12" md="4">
              <div><h5>food combination</h5></div>
              <div>Mass: {{ calculateTotals(item)?.mass }} g</div>
              <div>Energy: {{ calculateTotals(item)?.energy }} kcal</div>
            </v-col>
            <v-col cols="12" md="8">
              <AminoAcidChart
                  v-if="selectedFoodNutrients && expandedFoodNutrientsList[item.ndb_no2]"
                  :item="item"
                  :selected-nutrients="selectedFoodNutrients"
                  :expanded-nutrients="expandedFoodNutrientsList[item.ndb_no2]"
                  @chart-click="() => openLargeChart(item)"
              />
            </v-col>
          </v-row>
        </v-container>
      </td>
    </template>
  </v-data-table>
  <v-dialog
      v-model="dialogOpen"
      width="75%"
      height="85%"
      :max-width="'75vw'"
      :max-height="'75vh'"
      transition="dialog-bottom-transition"
  >
    <v-card>
      <v-toolbar
          dark
          color="primary"
      >
        <v-btn icon @click="dialogOpen = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Amino Acid Details</v-toolbar-title>
      </v-toolbar>

      <v-card-text class="pa-0">
        <AminoAcidChart
            v-if="selectedChartItem && selectedFoodNutrients && expandedFoodNutrientsList[selectedChartItem.ndb_no2]"
            :item="selectedChartItem"
            :full-size="true"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>