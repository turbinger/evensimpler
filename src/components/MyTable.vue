<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'

const store = useUserStore()
const { filteredUsers } = storeToRefs(store)
</script>

<template>
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
        <td>{{ user.email }}</td>
        <td>{{ user.address.city }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>