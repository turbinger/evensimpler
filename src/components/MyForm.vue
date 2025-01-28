<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import MyTable from './MyTableClassic.vue'

const store = useUserStore()
const { count, inputText, appMessage, reversedText } = storeToRefs(store)
const { updateCount, updateInputText, fetchUsers } = store

const handleCount = (): void => {
  updateCount()
}

const updateInput = (event: Event): void => {
  updateInputText((event.target as HTMLInputElement).value)
}

const foods = ref([])
const selectedFood = ref('')

// const fetchFoods = async () => {
//   try {
//     const response = await axios.get('http://localhost:5000/api/foods')
//     foods.value = response.data
//   } catch (error) {
//     console.error('Error fetching foods:', error)
//   }
// }

const fetchFoods = async () => {
  try {
    const response = await fetch('/foods.json')
    const data = await response.json()
    foods.value = data
  } catch (error) {
    console.error('Error fetching foods:', error)
  }
}
const sendSelectedFood = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/get_data', { NDB_No: selectedFood.value })
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
  <h1>{{ appMessage }}</h1>

  <div class="card p-3">
    <button type="button" class="btn btn-secondary mb-3" @click="handleCount">
      count is {{ count }}
    </button>
    <input
        type="text"
        :value="inputText"
        @input="updateInput"
        class="form-control mb-3"
        placeholder="Type something"
    />
    <p>Rückwärts</p>
    <div class="form-control mb-3">{{ reversedText }}</div>

<!--    <select v-model="selectedFood" class="form-control mb-3">-->
<!--      <option v-for="food in foods" :key="food.id" :value="food.id">-->
<!--        {{ food.name }}-->
<!--      </option>-->
<!--    </select>-->
<!--    <button type="button" class="btn btn-secondary mb-3" @click="sendSelectedFood">-->
<!--      anzeigen-->
<!--    </button>-->

    <div class="d-flex justify-content-between">
      <select v-model="selectedFood" class="form-control mb-3">
        <option v-for="food in foods" :key="food.id" :value="food.id">
          {{ food.name }}
        </option>
      </select>
      <button type="button" class="btn btn-secondary mb-3" @click="sendSelectedFood">
        anzeigen
      </button>
    </div>

    <MyTable />
  </div>
</template>