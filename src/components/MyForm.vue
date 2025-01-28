<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import MyTable from './MyTableClassic.vue'

interface Food {
  id: string | number
  name: string
}

const store = useUserStore()
const { count, inputText, appMessage, reversedText } = storeToRefs(store)
const { updateCount, updateInputText, fetchUsers } = store

const handleCount = (): void => {
  updateCount()
}

const updateInput = (event: Event): void => {
  updateInputText((event.target as HTMLInputElement).value)
}

const foods = ref<Food[]>([])
const selectedFood = ref<Food | null>(null)

const fetchFoods = async () => {
  try {
    const response = await fetch('/foods.json')
    const data = await response.json()
    foods.value = data
  } catch (error) {
    console.error('Error fetching foods:', error)
  }
}

// const sendSelectedFood = async () => {
//   if (!selectedFood.value) return
//
//   try {
//     console.log('Sending NDB_No:', selectedFood.value.id) // Debug log
//     const response = await axios.post('http://localhost:5000/api/get_data',
//         { NDB_No: selectedFood.value.id },
//         {
//           headers: {
//             'Content-Type': 'application/json',
//           }
//         }
//     )
//     console.log('API Response:', response.data)
//     store.updateTableData(response.data)
//   } catch (error: any) {
//     console.error('Error sending selected food:', error)
//     if (error.response) {
//       console.error('Error data:', error.response.data)
//       console.error('Error status:', error.response.status)
//     }
//   }
// }

const sendSelectedFood = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/get_data', { NDB_No: selectedFood.value.id })
    console.log('API Response:', response.data)
    store.updateTableData(response.data)
    console.log('TableData after update:', store.tableData)
  } catch (error) {
    console.error('Error sending selected food:', error)
  }
}

onMounted(() => {
  fetchUsers()
  fetchFoods()
})
</script>

<template>
  <v-container>
    <h1>{{ appMessage }}</h1>

    <v-card class="pa-3">
      <v-btn color="secondary" class="mb-3" @click="handleCount">
        count is {{ count }}
      </v-btn>
      <v-text-field v-model="inputText" class="mb-3" label="Type something"></v-text-field>
      <p>Rückwärts</p>
      <v-text-field v-model="reversedText" class="mb-3" readonly></v-text-field>

      <v-row class="mt-4">
        <v-col>
          <v-select
              v-model="selectedFood"
              :items="foods"
              item-title="name"
              item-value="id"
              label="Select Food"
              class="mb-3"
              return-object
          ></v-select>
          <v-btn
              color="secondary"
              class="mb-3"
              @click="sendSelectedFood"
              :disabled="!selectedFood"
          >
            anzeigen
          </v-btn>
        </v-col>
      </v-row>

      <MyTable />
    </v-card>
  </v-container>
</template>