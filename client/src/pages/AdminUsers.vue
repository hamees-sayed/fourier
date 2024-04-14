<template>
    <div>
      <div v-for="user in users" :key="user.id" class="card w-75 container my-2">
        <div class="card-body d-flex align-items-center justify-content-between">
          <div class="d-flex flex-column">
            <h5 class="card-title mb-1">{{ user.username }}</h5>
            <p class="card-text mb-0">{{ user.email }}</p>
          </div>
          <div>
            <button @click="deleteUser(user.id)" class="btn btn-primary">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
      data() {
          return {
              users: [],
          };
      },
      mounted() {
          axios.get(`${import.meta.env.VITE_SERVER_URL}/users`, 
          { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
          .then(response => this.users = response.data)
      },
      methods: {
          deleteUser(userId) {
            axios.get(`${import.meta.env.VITE_SERVER_URL}/user/${userId}/delete`, 
              { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
              .then(() => location.reload());
          },
      }
  }
</script>
