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

const emit = defineEmits(['chart-click'])
const props = defineProps<{
  item: TableRow,
  fullSize?: boolean
}>()

const chartData = computed<ChartData<'bar'>>(() => {
  if (!selectedFoodNutrients.value || !expandedFoodNutrientsList.value[props.item.ndb_no2]) return {
    labels: [],
    datasets: []
  }

  const food1Values = AMINO_ACIDS.map(aa =>
      ((selectedFoodNutrients.value?.[aa.key as keyof typeof selectedFoodNutrients.value] ?? 0) / 100) * props.item.value1
  )

  const food2Values = AMINO_ACIDS.map(aa =>
      (expandedFoodNutrientsList.value[props.item.ndb_no2][aa.key as keyof typeof expandedFoodNutrientsList.value[typeof props.item.ndb_no2]] / 100) * props.item.value2
  )

  const referenceValues = AMINO_ACIDS.map(aa => aa.reference)

  // Food 1 alone calculation
  const food1_aa = AMINO_ACIDS.map(aa =>
      (selectedFoodNutrients.value?.[aa.key as keyof typeof selectedFoodNutrients.value] ?? 0) / 100
  )
  const food1Ratios = food1_aa.map((val, i) => val / (referenceValues[i] || 1))
  const minFood1Ratio = Math.min(...food1Ratios.filter(r => r > 0))
  const scaleFood1 = 1 / (minFood1Ratio || 1)
  const food1_aloneValues = food1_aa.map(val => val * scaleFood1)

  // Food 2 alone calculation
  const food2_aa = AMINO_ACIDS.map(aa =>
      ((expandedFoodNutrientsList.value[props.item.ndb_no2][aa.key as keyof typeof expandedFoodNutrientsList.value[typeof props.item.ndb_no2]]) ?? 0) / 100
  )
  const food2Ratios = food2_aa.map((val, i) => val / (referenceValues[i] || 1))
  const minFood2Ratio = Math.min(...food2Ratios.filter(r => r > 0))
  const scaleFood2 = 1 / (minFood2Ratio || 1)
  const food2_aloneValues = food2_aa.map(val => val * scaleFood2)


  return {
    labels: AMINO_ACIDS.map(aa => aa.label),
    datasets: [
      {
        label: 'Food 1',
        data: food1Values,
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
        stack: 'combined'
      },
      {
        label: 'Food 2',
        data: food2Values,
        backgroundColor: 'rgba(153, 102, 255, 0.8)',
        stack: 'combined'
      },
      {
        label: 'Reference',
        data: referenceValues,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        stack: 'reference'  // separater Stack für Referenzwerte
      },
      {
        label: 'Food 1 alone',
        data: food1_aloneValues,
        backgroundColor: 'rgba(255, 205, 86, 0.5)',
        stack: 'food1_alone'
      },
      {
        label: 'Food 2 alone',
        data: food2_aloneValues,
        backgroundColor: 'rgba(201, 203, 207, 0.5)',
        stack: 'food2_alone'
      }
    ]
  }
})

const chartOptions = computed<ChartOptions<'bar'>>(() => ({
  responsive: true,
  maintainAspectRatio: !props.fullSize, // Skalierung im Dialog
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'mg'
      }
    }
  },
  plugins: {
    tooltip: {
      callbacks: {
        footer: (tooltipItems) => {
          // Nur anzeigen, wenn stack 'combined' ist
          if (tooltipItems[0].dataset.stack !== 'combined') {
            return ''
          }
          const chart = tooltipItems[0].chart
          const dataIndex = tooltipItems[0].dataIndex
          const sum = chart.data.datasets
              .filter(ds => ds.stack === 'combined')
              .reduce((acc, ds) => acc + (typeof ds.data[dataIndex] === 'number' ? ds.data[dataIndex] : 0), 0)
          return `Total: ${sum.toFixed(1)} mg`
        }
      }
    },
    legend: {
      display: true // Always display the legend
    }
  },
  onClick: (event, elements) => {
    if (elements.length > 0) {
      emit('chart-click')
    }
  }
}))
</script>

<template>
  <Bar :data="chartData" :options="chartOptions" :class="{ 'full-size-chart': fullSize }"/>
</template>

<style scoped>
.full-size-chart {
  width: 100%;
  height: 600px; /* Oder dynamische Höhe */
}
</style>