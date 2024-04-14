<template>
    <div class="container">
      <h2 v-if="isBlacklisted">Creator: {{ username }} <span style="color: red;"><b>BLACKLISTED</b> (Policy Violation)</span></h2>
      <h2 v-else>Creator: {{ username }}</h2>
  
      <div class="buttons mb-3">
        <router-link to="/creator/albums" class="btn btn-light border mx-3" role="button">View your Albums</router-link>
        <router-link to="/creator/songs" class="btn btn-light border" role="button">View your Songs</router-link>
      </div>
  
      <div>
        <ul class="dashboard-stats d-flex flex-wrap container mb-0">
          <li class="list-group-item list-group-item-primary px-3 rounded mx-3">Total Number of Songs: {{ num_of_songs }}</li>
          <li class="list-group-item list-group-item-warning px-3 rounded">Total Number of Albums: {{ num_of_albums }}</li>
        </ul>
      </div>
  
      <div class="plot d-flex flex-wrap justify-content-center">
        <img :src="'data:image/png;base64,' + song_rating_hist" alt="Song Rating Histogram" width="600" height="460">
      </div>
    </div>
  </template>
  
<script>
    import axios from 'axios';
    
    export default {
        data () {
            return {
                username: '',
                num_of_songs: 0,
                num_of_albums: 0,
                song_rating_hist: '',
                isBlacklisted: false,
            };
        },
        mounted () {
            axios.get(`${import.meta.env.VITE_SERVER_URL}/creator`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => {
                this.username = response.data.username;
                this.num_of_songs = response.data.num_of_songs;
                this.num_of_albums = response.data.num_of_albums;
                this.song_rating_hist = response.data.song_rating_hist;
                this.isBlacklisted = response.data.is_blacklisted;
            })
        },
    }
</script>