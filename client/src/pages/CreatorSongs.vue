<template>
    <div class="container">
      <h1>Your Songs</h1>
      <div class="buttons">
        <router-link to="/creator/song/new" class="btn btn-light border" role="button">Create a new Song</router-link>
      </div>
      <br>
      <br>
      <template v-if="length === 0">
        <h4>You haven't created any songs yet. Share yours songs with the community now 🎸</h4>
      </template>
      <template v-else>
        <div v-for="song in songs" :key="song.id" class="card w-75 mb-3">
          <div class="card-body">
            <template v-if="song.is_flagged">
              <h4 class="card-title">{{ song.title }} &nbsp <span style="color:red;"><b>FLAGGED</b></span></h4>
            </template>
            <template v-else>
              <h4 class="card-title">{{ song.title }}</h4>
            </template>
            <h6 class="card-title mt-1">Genre: {{ song.genre }}</h6>
            <button class="btn btn-outline-secondary mb-2" @click="toggleCollapse(song.id)">Show/Hide Lyrics</button>
            <div v-if="song.lyrics" :id="'lyrics-' + song.id" class="collapse">
              <pre>{{ song.lyrics }}</pre>
            </div>
            <div v-else :id="'lyrics-' + song.id" class="collapse">
              <pre>Lyrics not Available</pre>
            </div>
            <audio class="w-100" controls>
                <source :src="`${SERVER_URL}/${song.song_file_url}`" type="audio/mp3" />
            </audio>
            <router-link :to="'/creator/song/update/'+song.id" class="btn btn-primary mx-2">Update</router-link>
            <button @click="deleteSong(song.id)" class="btn btn-primary">Delete</button>
          </div>
        </div>
      </template>
    </div>
  </template>
  
<script>
    import axios from 'axios';

    export default {
        data () {
            return {
                songs: [],
                SERVER_URL: import.meta.env.VITE_SERVER_URL,
            }
        },
        methods: {
            toggleCollapse(songId) {
                const collapseElement = document.getElementById(`lyrics-${songId}`);
                collapseElement.classList.toggle('show');
            },
            deleteSong(songId) {
                axios.get(`${import.meta.env.VITE_SERVER_URL}/song/${songId}/delete`, 
                { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }).then(() => location.reload())
                .then(() => location.reload());
            },
            length(){
                return this.songs.length
            }
        },
        mounted() {
            axios.get(`${import.meta.env.VITE_SERVER_URL}/song`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => {
                this.songs = response.data
            })
        }
    }
</script>