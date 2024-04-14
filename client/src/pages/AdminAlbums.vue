<template>
    <div class="container">
      <form @submit.prevent="search" class="container input-group rounded w-50">
        <input v-model="searchTerm" type="search" class="form-control rounded border border-primary" placeholder="Search Songs" aria-label="Search" aria-describedby="search-addon" />
        <span class="input-group-text border-0" id="search-addon">
          <button type="submit" class="btn btn-link"><i class="fas fa-search"></i></button>
        </span>
      </form>
      <br>
      <template v-if="length === 0">
        <h4>No Albums</h4>
      </template>
      <template v-else>
        <div v-for="album in albums" :key="album.id">
          <div style="text-decoration: none; color:#212529">
            <div class="card w-75">
              <div class="card-body">
                <div>
                  <h5 class="card-title mb-1">{{album.album_name}}</h5>
                </div>
                <p class="card-text mb-3">Genre: {{album.genre}}</p>
                <a v-if="album.is_flagged" @click="flag(album.id)" class="btn btn-primary mx-2">Unflag</a>
                <a v-else @click="flag(album.id)" class="btn btn-primary mx-2">Flag</a>
                <button class="btn btn-primary" @click="deleteAlbum(album.id)">Remove</button>
              </div>
            </div>
        </div>
          <br>
        </div>
      </template>
    </div>
  </template>
  
<script>
    import axios from 'axios';
    
    export default {
        data () {
            return {
                albums: [],
            };
        },
        computed: {
            length() {
                return this.albums.length;
            }
        },
        mounted () {
            axios.get(`${import.meta.env.VITE_SERVER_URL}/admin/albums`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => this.albums = response.data)
        },
        methods: {
            deleteAlbum(albumId) {
                axios.get(`${import.meta.env.VITE_SERVER_URL}/album/${albumId}/delete`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(() => location.reload());
            },
            flag(id){
                axios.get(`${import.meta.env.VITE_SERVER_URL}/flag/${id}/album`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(() => location.reload());
            },
            search() {
                axios.get(`${import.meta.env.VITE_SERVER_URL}/admin/albums/search`, 
                { params: { q: this.searchTerm }, headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(response => this.albums = response.data)
            }
        }
    }
</script>