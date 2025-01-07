<script setup>

import {computed, ref} from "vue";

  defineProps({
    list: Array,
  })

  const list = ref([])
  const filteredUsers = computed(() => {
    return list.value.filter(user => user.id <= 5)
  })


</script>

<template>
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
</template>

<style scoped>

</style>