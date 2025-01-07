<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'

// Props Definition mit defineProps
const props = defineProps({
  msg: String
})

// Store initialization
const store = useStore()

// Computed properties
const count = computed(() => store.state.count)
const inputText = computed(() => store.state.inputText)
const filteredUsers = computed(() => store.getters.filteredUsers)
const reversedText = computed(() => store.getters.reversedText)

// Methods
const handleCount = () => {
  store.dispatch('updateCount')
}

const updateInput = (event) => {
  store.dispatch('updateInputText', event.target.value)
}

// Lifecycle hooks
onMounted(() => {
  store.dispatch('fetchUsers')
})
</script>

<template>
  <h1>{{ msg }}</h1>

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

    <div class="container mt-4">
      <h3>Users:</h3>
      <table class="table">
        <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Name</th>
          <th scope="col">Email</th>
          <th scope="col">City</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="user in filteredUsers" :key="user.id">
          <th scope="row">{{ user.id }}</th>
          <td>{{ user.name }}</td>
          <td>{{ user.address.city }}</td>
          <td>{{ user.email }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 10px;
}
.card {
  margin-top: 20px;
}
input {
  margin-top: 10px;
  padding: 5px;
}
</style>