<template>
    <div class="container">
      <h1>Your Albums</h1>
      <div class="buttons">
        <router-link to="/creator/album/new" class="btn btn-light border" role="button">Create a new Album</router-link>
      </div>
      <br>
      <br>
      <template v-if="length === 0">
        <h4>You haven't created any Albums yet. Create and share yours albums with the community now 📼</h4>
      </template>
      <template v-else>
        <div v-for="album in albums" :key="album.id">
          <router-link :to="'/creator/album/'+album.id" style="text-decoration: none; color:#212529">
            <div class="card w-75">
              <div class="card-body">
                <template v-if="album.is_flagged">
                  <h5 class="card-title mb-1">{{album.title}} &nbsp <span style="color:red;"><b>FLAGGED</b> (Policy Violation)</span></h5>
                </template>
                <template v-else>
                  <h5 class="card-title mb-1">{{album.title}}</h5>
                </template>
                <p class="card-text mb-3">Genre: {{album.genre}}</p>
                <router-link :to="'/creator/album/update/'+album.id" class="btn btn-primary mx-2">Update</router-link>
                <button class="btn btn-primary" @click="deleteAlbum(album.id)">Delete</button>
              </div>
            </div>
        </router-link>
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
            axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/album", 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => this.albums = response.data)
        },
        methods: {
            deleteAlbum(albumId) {
                axios.get(`https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/album/${albumId}/delete`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                .then(() => location.reload());
            }
        }
    }
</script>