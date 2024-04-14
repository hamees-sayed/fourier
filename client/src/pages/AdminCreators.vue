<template>
    <div>
      <div v-for="creator in creators" :key="creator.id" class="card w-75 container my-2">
        <div class="card-body d-flex align-items-center justify-content-between">
          <div class="d-flex flex-column">
            <h5 class="card-title mb-1">{{ creator.creator_name }}</h5>
            <p class="card-text mb-0">{{ creator.email }}</p>
          </div>
          <div>
            <button v-if="creator.is_blacklisted" @click="toggleWhitelist(creator.id)" class="btn btn-primary">Whitelist</button>
            <button v-else @click="toggleBlacklist(creator.id)" class="btn btn-primary">Blacklist</button>
            <button @click="deleteCreator(creator.id)" class="btn btn-primary mx-3">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
    import axios from 'axios';
    export default {
        data(){
            return {
                creators: [],
            }
        },
        mounted(){
            axios.get(`${import.meta.env.VITE_SERVER_URL}/creators`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => this.creators = response.data)
        },
        methods: {
            deleteCreator(creatorId){
                axios.get(`${import.meta.env.VITE_SERVER_URL}/creator/${creatorId}/delete`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(() => location.reload());
            },
            toggleBlacklist(creatorId){
                axios.get(`${import.meta.env.VITE_SERVER_URL}/creator/${creatorId}/blacklist`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(() => location.reload());
            },
            toggleWhitelist(creatorId){
                axios.get(`${import.meta.env.VITE_SERVER_URL}/creator/${creatorId}/whitelist`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(() => location.reload());
            }
        }
    }
</script>