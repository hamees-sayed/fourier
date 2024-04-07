<template>
    <h1>{{ album.album_creator }}</h1>
    <br>
    <div v-if="len === 0">
      <h3>No songs in the album.</h3>
    </div>
    <div v-else>
        <div v-for="song in data" :key="song.id">
            <div class="card w-75 container">
                <div class="card-body position-relative">
                <div class="d-flex align-items-center">
                    <h4 class="card-title mb-0">{{ song.title }}</h4>
                </div>
                <h6 class="card-title mt-1">Genre: {{ song.genre }}</h6>
                <a class="btn btn-outline-secondary mb-2" role="button" @click="toggleCollapse(song.id)">Show/Hide Lyrics</a>
                <div :id="'lyrics-' + song.id" class="collapse">
                    <pre>{{ song.lyrics }}</pre>
                </div>
                <audio class="w-100" controls>
                    <source :src="'https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev'+song.song_file_url" type="audio/mp3" />
                </audio>
                <router-link :to="'/playlist/add/'+song.id" class="btn btn-primary mx-2">Add to Playlist</router-link>
                <a @click="handleRateClick(song.id)" class="btn btn-primary">Rate</a>
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
                len: 0,
                album: {},
            }
        },
        computed: {
            ...mapGetters('auth', {
                isAuthenticated: IS_AUTHENTICATED,
            }),
        },
        mounted () {
            axios.get(`https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/album/${this.id}`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => {
                this.data = response.data.songs;
                this.album = response.data.album;
                this.len = response.data.songs.length
            })
        },
        methods: {
            toggleCollapse(songId) {
            const collapseElement = document.getElementById(`lyrics-${songId}`);
            collapseElement.classList.toggle('show');
        },
  }
    }
</script>