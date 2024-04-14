<template>
    <h1>Songs in {{ playlist.playlist_name }}</h1>
    <h3>{{ playlist.playlist_desc }}</h3>
    <br>
    <div v-if="data.length === 0">
      <h3>No songs in the album.</h3>
    </div>
    <div v-else>
        <div v-for="song in data" :key="song.song_id">
            <div class="card w-75 container">
                <div class="card-body position-relative">
                <div class="d-flex align-items-center">
                    <h4 class="card-title mb-0">{{ song.song_title }}</h4>
                </div>
                <h6 class="card-title mt-1">Genre: {{ song.genre }}</h6>
                <a class="btn btn-outline-secondary mb-2" role="button" @click="toggleCollapse(song.id)">Show/Hide Lyrics</a>
                <div :id="'lyrics-' + song.id" class="collapse">
                    <pre>{{ song.lyrics }}</pre>
                </div>
                <audio class="w-100" controls>
                    <source :src="`${SERVER_URL}/${song.song_file_url}`" type="audio/mp3" />
                </audio>
                <router-link :to="'/playlist/add/'+song.song_id" class="btn btn-primary mx-2">Add to Playlist</router-link>
                <a @click="handleRateClick(song.song_id)" class="btn btn-primary">Rate</a>
            </div>
        </div>
      <br>
    </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { mapGetters } from 'vuex';
    import { IS_AUTHENTICATED } from '../store/storeconstants';

    export default {
        data () {
            return {
                id: this.$route.params.id,
                data: [],
                playlist: {},
                SERVER_URL: import.meta.env.VITE_SERVER_URL,
            }
        },
        computed: {
            ...mapGetters('auth', {
            isAuthenticated: IS_AUTHENTICATED,
            })
        },
        mounted () {
            axios.get(`${import.meta.env.VITE_SERVER_URL}/playlist/${this.id}`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => {
                this.data = response.data.songs;
                this.playlist = response.data.playlist;
            })
        },
        methods: {
            toggleCollapse(songId) {
            const collapseElement = document.getElementById(`lyrics-${songId}`);
            collapseElement.classList.toggle('show');
        },
        handleRateClick(id) {
            this.$router.push(`/rate/${id}`);
        },
  }
    }
</script>