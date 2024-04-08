<template>
    <div class="container">
      <h2 class="mb-3">Admin Dashboard</h2>
      <div>
        <ul class="dashboard-stats admin-detail d-flex flex-wrap">
          <li class="list-group-item list-group-item-primary px-3 rounded me-2">Total Number of Users: {{ totalUsers }}</li>
          <li class="list-group-item list-group-item-success px-3 rounded me-2">Total Number of Creators: {{ totalCreators }}</li>
          <li class="list-group-item list-group-item-danger px-3 rounded me-2">Total Number of Songs: {{ totalSongs }}</li>
          <li class="list-group-item list-group-item-warning px-3 rounded">Total Number of Albums: {{ totalAlbums }}</li>
        </ul>
      </div>
      <div class="plot d-flex flex-wrap">
        <img :src="'data:image/png;base64,' + currentUsersPlot" alt="Current User Line Chart" width="600" height="460">
        <img :src="'data:image/png;base64,' + songRatingHist" alt="Song Rating Histogram" width="600" height="460">
      </div>
    </div>
  </template>
  
<script>
    import axios from 'axios';
    
    export default {
        data () {
            return {
                totalUsers: 0,
                totalCreators: 0,
                totalSongs: 0,
                totalAlbums: 0,
                currentUsersPlot: '',
                songRatingHist: '',
            };
        },
        mounted () {
            axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/admin", 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => {
                this.totalUsers = response.data.users;
                this.totalCreators = response.data.creators;
                this.totalSongs = response.data.songs;
                this.totalAlbums = response.data.albums;
                this.currentUsersPlot = response.data.current_users_plot;
                this.songRatingHist = response.data.song_rating_hist;
            })
        },
    }
</script>