<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import type { TableRow } from '../stores/userStore'
import AminoAcidChart from './AminoAcidChart.vue'
import { AMINO_ACIDS } from '../utils/aminoAcidUtils'

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
// const aloneDataCache = ref<{ [key: number]: { food1_aloneValues: number[], food2_aloneValues: number[] } }>({})
const aloneDataCache = ref<{ [key: number]: ReturnType<typeof getAloneData> }>({})

const handleExpand = async (expandedRows: string[]) => {
  const collapsedRows = expanded.value.filter(row => !expandedRows.includes(row))
  for (const ndb_no2 of collapsedRows) {
    store.clearExpandedFoodNutrients(Number(ndb_no2))
    delete aloneDataCache.value[Number(ndb_no2)]
  }
  for (const ndb_no2 of expandedRows) {
    if (!expandedFoodNutrientsList.value[Number(ndb_no2)]) {
      await store.updateExpandedFoodNutrients(Number(ndb_no2))
    }
    if (!aloneDataCache.value[Number(ndb_no2)]) {
      aloneDataCache.value[Number(ndb_no2)] = getAloneData({ ndb_no2: Number(ndb_no2) } as TableRow)
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
  const totalProtein =
      (selectedFoodNutrients.value.PRO_203_g * item.value1 / 100) +
      (expandedFoodNutrients.PRO_203_g * item.value2 / 100)
  const totalFat =
      (selectedFoodNutrients.value.FAT_204_g * item.value1 / 100) +
      (expandedFoodNutrients.FAT_204_g * item.value2 / 100)
  return {
    mass: totalMass.toFixed(2),
    energy: totalEnergy.toFixed(2),
    protein: totalProtein.toFixed(2),
    fat: totalFat.toFixed(2)
  }
}

function compareScalefactor(prot_scale:number, scalefood:number) {
  return prot_scale < scalefood ? scalefood : prot_scale
}

function getAloneData(item: TableRow) {
  const referenceValues = AMINO_ACIDS.map(aa => aa.reference)
  let scaleFood1 = 1
  let prot_scale1 = 1
  let food1_aloneValues: number[] = []
  if (selectedFoodNutrients.value) {
    const food1_aa = AMINO_ACIDS.map(aa =>
        (selectedFoodNutrients.value ? selectedFoodNutrients.value[aa.key] ?? 0 : 0) / 100
    )
    const food1Ratios = food1_aa.map((val, i) => val / (referenceValues[i] || 1))
    const minFood1Ratio = Math.min(...food1Ratios.filter(r => r > 0))
    scaleFood1 = 1 / (minFood1Ratio || 1)
    prot_scale1 = (25*100) / (selectedFoodNutrients.value?.PRO_203_g || 1)
    food1_aloneValues = food1_aa.map(val => val * compareScalefactor(prot_scale1, scaleFood1))
  }

  let scaleFood2 = 1
  let prot_scale2 = 1
  let food2_aloneValues: number[] = []
  const expandedData = expandedFoodNutrientsList.value[item.ndb_no2]
  if (expandedData) {
    const food2_aa = AMINO_ACIDS.map(aa =>
        (expandedData[aa.key] ?? 0) / 100
    )
    const food2Ratios = food2_aa.map((val, i) => val / (referenceValues[i] || 1))
    const minFood2Ratio = Math.min(...food2Ratios.filter(r => r > 0))
    scaleFood2 = 1 / (minFood2Ratio || 1)
    console.log("scaleFood2", scaleFood2)
    prot_scale2 = (25*100) / (expandedData.PRO_203_g || 1)
    food2_aloneValues = food2_aa.map(val => val * compareScalefactor(prot_scale2, scaleFood2))
  }
  const excess_food1 = food1_aloneValues.reduce((acc, val, i) => acc + (val - referenceValues[i]), 0)
  const excess_food2 = food2_aloneValues.reduce((acc, val, i) => acc + (val - referenceValues[i]), 0)
  const mass_food1 = compareScalefactor(prot_scale1, scaleFood1)
  const mass_food2 = compareScalefactor(prot_scale2, scaleFood2)
  const energy_food1 = (selectedFoodNutrients.value?.CAL_208_kcal || 0) * mass_food1 / 100
  const energy_food2 = (expandedData?.CAL_208_kcal || 0) * mass_food2 / 100
  const protein_food1 = (selectedFoodNutrients.value?.PRO_203_g || 0) * mass_food1 / 100
  const protein_food2 = (expandedData?.PRO_203_g || 0) * mass_food2 / 100


  return {
    scaleFood1,
    scaleFood2,
    food1_aloneValues,
    food2_aloneValues,
    excess_food1,
    excess_food2,
    mass_food1,
    mass_food2,
    energy_food1,
    energy_food2,
    protein_food1,
    protein_food2
  }
}

watch(() => tableData.value, () => {
  expanded.value = []
  aloneDataCache.value = {}
})

const dialogOpen = ref(false)
const selectedChartItem = ref<TableRow | null>(null)
const food1AloneValues = ref<number[]>([])
const food2AloneValues = ref<number[]>([])

const openLargeChart = (item: TableRow) => {
  selectedChartItem.value = item
  const aloneData = aloneDataCache.value[item.ndb_no2]
  food1AloneValues.value = aloneData.food1_aloneValues
  food2AloneValues.value = aloneData.food2_aloneValues
  dialogOpen.value = true
}
</script>

<template>
  <v-data-table
      :headers="displayedHeaders"
      :items="tableData"
      :expanded.sync="expanded"
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
              <div>Protein: {{ calculateTotals(item)?.protein }} g</div>
              <div>Fat: {{ calculateTotals(item)?.fat }} g</div>
              <div><h5>food1 alone </h5></div>
              <div>Food1 excess: {{ aloneDataCache[item.ndb_no2]?.excess_food1.toFixed(2) }} mg</div>
              <div>Food1 mass: {{ aloneDataCache[item.ndb_no2]?.mass_food1.toFixed(2) }} g</div>
              <div>Food1 energy: {{ aloneDataCache[item.ndb_no2]?.energy_food1.toFixed(2) }} kcal</div>
              <div>Food1 protein: {{ aloneDataCache[item.ndb_no2]?.protein_food1.toFixed(2) }} g</div>
              <div><h5>food2 alone </h5></div>
              <div>Food2 excess: {{ aloneDataCache[item.ndb_no2]?.excess_food2.toFixed(2) }} mg</div>
              <div>Food2 mass: {{ aloneDataCache[item.ndb_no2]?.mass_food2.toFixed(2) }} g</div>
              <div>Food2 energy: {{ aloneDataCache[item.ndb_no2]?.energy_food2.toFixed(2) }} kcal</div>
              <div>Food2 protein: {{ aloneDataCache[item.ndb_no2]?.protein_food2.toFixed(2) }} g</div>

            </v-col>
            <v-col cols="12" md="8">
              <AminoAcidChart
                  v-if="selectedFoodNutrients && expandedFoodNutrientsList[item.ndb_no2]"
                  :item="item"
                  :selected-nutrients="selectedFoodNutrients"
                  :expanded-nutrients="expandedFoodNutrientsList[item.ndb_no2]"
                  :food1AloneValues="aloneDataCache[item.ndb_no2]?.food1_aloneValues"
                  :food2AloneValues="aloneDataCache[item.ndb_no2]?.food2_aloneValues"
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
            :food1AloneValues="food1AloneValues"
            :food2AloneValues="food2AloneValues"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>