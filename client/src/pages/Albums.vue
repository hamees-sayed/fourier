<template>
    <div v-if="isAuthenticated">
        <form @submit.prevent="search" class="container input-group rounded w-50">
            <input v-model="searchTerm" type="search" class="form-control rounded border border-primary" placeholder="Search Albums" aria-label="Search" aria-describedby="search-addon" />
            <span class="input-group-text border-0" id="search-addon">
                <button type="submit" class="btn btn-link"><i class="fas fa-search"></i></button>
            </span>
        </form>
        <br>
        <div v-for="album in data" :key="album.id" class="card w-75 container mb-3" @click="handleAlbumClick(album.id)" style="cursor:pointer">
        <div class="card-body d-flex justify-content-between align-items-center">
          <div class="d-flex flex-column">
            <h5 class="card-title mb-1">{{ album.title }}</h5>
            <h6 class="card-text mb-0">Genre: {{ album.genre }}</h6>
            <p class="card-text mt-3">By: {{ album.album_creator }}</p>
          </div>
        </div>
    </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';
  import { IS_AUTHENTICATED } from '../store/storeconstants';
  import axios from 'axios';
  
  export default {
    data () {
          return {
              data: [],
              searchTerm: '',
              is_admin: false,
              is_creator: false,
          };
      },
    computed: {
      ...mapGetters('auth', {
        isAuthenticated: IS_AUTHENTICATED,
      })
    },
    mounted () {
          this.is_admin = localStorage.getItem("is_admin");
          this.is_creator = localStorage.getItem("is_creator");
          axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/albums", 
          { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
          .then(response => this.data = response.data)
    },
    methods: {
        search() {
            axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/albums/search", 
            { params: { q: this.searchTerm }, headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => this.data = response.data)
        },
        handleAlbumClick(albumId) {
            this.$router.push(`/albums/${albumId}`);
        }
    }
  };
  
  </script>