<template>
    <div class="container">
      <div v-if="playlistError" class="alert alert-danger">
        {{ playlistError }}
      </div>
      <form @submit.prevent="addSongToPlaylist" class="needs-validation" novalidate>
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Your Playlists</legend>
          <div class="form-group">
            <br>
            <select v-model="selected">
                <option v-for="playlist in playlists" :key="playlist.id" :value="parseInt(playlist.id)">{{ playlist.playlist_name }}</option>
            </select>
          </div>
        </fieldset>
        <br>
        <div class="form-group">
          <button type="submit" class="btn btn-outline-info">Submit</button>
        </div>
      </form>
    </div>
</template>

<script>
    import axios from 'axios';
    import { mapActions } from 'vuex';
    import { ADD_SONG_TO_PLAYLIST_ACTION } from '../store/storeconstants';
    
    export default {
        data() {
            return {
                playlists: [],
                selected: null,
                playlistError: '',
            }
        }, 
        mounted() {
            axios.get(`${import.meta.env.VITE_SERVER_URL}/account`, 
            { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
            .then(response => {
                this.playlists = response.data;
            })
        },
        methods: {
            ...mapActions('auth', {
                add_song_playlist: ADD_SONG_TO_PLAYLIST_ACTION
            }),
            addSongToPlaylist(){
                if (this.selected !== null) {
                    this.add_song_playlist({ playlist_id: this.selected, song_id: this.$route.params.id })
                    .then(() => {this.$router.push('/account');})
                } else {
                    this.playlistError = 'No playlist selected.';
                }
            }
        }
    }
</script>