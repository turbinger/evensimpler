<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import type { TableRow } from '../stores/userStore'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import type { ChartData, ChartOptions } from 'chart.js'
import { AMINO_ACIDS } from '../utils/aminoAcidUtils'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useUserStore()
const { selectedFoodNutrients, expandedFoodNutrientsList } = storeToRefs(store)

const props = defineProps<{
  item: TableRow
}>()

const chartData = computed<ChartData<'bar'>>(() => {
  if (!selectedFoodNutrients.value || !expandedFoodNutrientsList.value[props.item.ndb_no2]) return {
    labels: [],
    datasets: []
  }

  const food1Values = AMINO_ACIDS.map(aa =>
      ((selectedFoodNutrients.value?.[aa.key as keyof typeof selectedFoodNutrients.value] ?? 0) / 100) * 1000 * props.item.value1
  )

  const food2Values = AMINO_ACIDS.map(aa =>
      (expandedFoodNutrientsList.value[props.item.ndb_no2][aa.key as keyof typeof expandedFoodNutrientsList.value[typeof props.item.ndb_no2]] / 100) * 1000 * props.item.value2
  )

  const combinedValues = food1Values.map((val, idx) => val + food2Values[idx])

  return {
    labels: AMINO_ACIDS.map(aa => aa.label),
    datasets: [
      {
        label: 'Food 1',
        data: food1Values,
        backgroundColor: 'rgba(75, 192, 192, 0.5)'
      },
      {
        label: 'Food 2',
        data: food2Values,
        backgroundColor: 'rgba(153, 102, 255, 0.5)'
      },
      {
        label: 'Combined',
        data: combinedValues,
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      }
    ]
  }
})

const chartOptions: ChartOptions<'bar'> = {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'mg'
      }
    }
  }
}
</script>

<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>