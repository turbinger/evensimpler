<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import MyTable from './MyTable.vue'

const store = useUserStore()
const { count, inputText, appMessage, reversedText } = storeToRefs(store)
const { updateCount, updateInputText, fetchUsers } = store

const handleCount = (): void => {
  updateCount()
}

const updateInput = (event: Event): void => {
  updateInputText((event.target as HTMLInputElement).value)
}

onMounted(() => {
  fetchUsers()
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

    <MyTable />
  </div>
</template>