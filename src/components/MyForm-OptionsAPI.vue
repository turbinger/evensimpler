<template>
  <h1>{{ msg }}</h1>

  <div class="card p-3">
    <button type="button" class="btn btn-secondary mb-3" @click="count++">count is {{ count }}</button>
    <input type="text" v-model="inputText" class="form-control mb-3" placeholder="Type something" />
    <p>Rückwärts</p>
    <div class="form-control mb-3">{{ reversedText }}</div>

    <div class="container mt-4">
      <h3> Users:</h3>
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
          <td>{{ user.email }}</td>
          <td>{{ user.address.city }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MyForm',
  props: {
    msg: String
  },
  data() {
    return {
      count: 0,
      inputText: '',
      users: []
    }
  },
  computed: {
    reversedText() {
      return this.inputText.split('').reverse().join('')
    },
    filteredUsers() {
      return this.users.filter(user => user.id <= 5)
    }
  },
  mounted() {
    axios.get('https://jsonplaceholder.typicode.com/users')
        .then(res => {
          this.users = res.data
        })
  }
}
</script>

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