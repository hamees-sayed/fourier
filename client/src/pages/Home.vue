<template>
  <div class="container vertical-center d-flex flex-column align-items-center" v-if="!isAuthenticated">
    <img src="../assets/logo.png" width="300" height="190" />
    <h3>Dive into the world of Music today.</h3>
    <div class="buttons">
      <router-link to="/register" class="btn btn-light border mx-2" role="button">Register</router-link>
      <router-link to="/login" class="btn btn-light border" role="button">Login</router-link>
    </div>
  </div>
  <div v-if="isAuthenticated">
    <form @submit.prevent="search" class="container input-group rounded w-50">
      <input v-model="searchTerm" type="search" class="form-control rounded border border-primary" placeholder="Search Songs" aria-label="Search" aria-describedby="search-addon" />
      <span class="input-group-text border-0" id="search-addon">
        <button type="submit" class="btn btn-link"><i class="fas fa-search"></i></button>
      </span>
    </form>
    <br>
    <div v-for="song in data" :key="song.song_id">
      <div v-if="song.creator_id && !song.is_flagged && !song.creator_is_blacklisted" class="card w-75 container">
        <div class="card-body position-relative">
          <div class="d-flex align-items-center">
            <h4 class="card-title mb-0">{{ song.song_title }}</h4>
            <div class="rating position-absolute mx-5" style="right: 0;"><b>{{ song.average_rating }}</b>&nbsp<i class="fa-solid fa-star"></i></div>
          </div>
          <h6 class="card-title mt-1">Genre: {{ song.genre }}</h6>
          <p class="card-title mt-2">By: {{ song.creator_username }}</p>
          <a class="btn btn-outline-secondary mb-2" role="button" @click="toggleCollapse(song.song_id)">Show/Hide Lyrics</a>
          <div :id="'lyrics-' + song.song_id" class="collapse">
            <pre>{{ song.lyrics }}</pre>
          </div>
          <audio class="w-100" controls>
            <source :src="'https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev'+song.song_file_url" type="audio/mp3" />
          </audio>
          <a href="#" class="btn btn-primary mx-2">Add to Playlist</a>
          <a href="#" class="btn btn-primary">Rate</a>
        </div>
      </div>
      <br>
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
        axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/", 
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(response => this.data = response.data)
    },
  methods: {
    toggleCollapse(songId) {
      const collapseElement = document.getElementById(`lyrics-${songId}`);
      collapseElement.classList.toggle('show');
    },
    search() {
      axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/search", 
        { params: { q: this.searchTerm }, headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(response => this.data = response.data)
    }
  }
};

</script>