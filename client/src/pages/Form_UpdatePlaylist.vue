<template>
    <div class="container">
      <form @submit.prevent="updatePlaylist" class="needs-validation" novalidate>
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Update playlist</legend>
          <div class="form-group">
            <label for="playlist_name" class="form-control-label">Playlist Name</label>
            <div class="invalid-feedback" v-if="playlist_nameError">
              <span>{{ playlist_nameError }}</span>
            </div>
            <input v-model="playlist_name" type="text" id="playlist_name" class="form-control form-control-lg" required>
          </div>
          <div class="form-group">
            <label for="playlist_desc" class="form-control-label">Playlist Description</label>
            <textarea v-model="playlist_desc" id="playlist_desc" class="form-control form-control-lg" rows="4" required></textarea>
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
import { UPDATE_PLAYLIST_ACTION } from '../store/storeconstants';

export default {
    data() {
        return {
            playlist_name: '',
            playlist_nameError: '',
            playlist_desc: '',
            id: this.$route.params.id,
        }
    },
    methods: {
        ...mapActions('auth', {
            update_playlist: UPDATE_PLAYLIST_ACTION
        }),
        updatePlaylist() {
            if (!this.playlist_name) {
                this.playlist_nameError = 'Username is required';
            } else {
                this.usernameError = '';
            }
    
            if (this.playlist_name) {
            this.update_playlist({ playlist_name: this.playlist_name, playlist_desc: this.playlist_desc, playlist_id: this.id })
                .then(() => {this.$router.push('/account');})
            }
        },
    },
    mounted() {
        axios.get(`${import.meta.env.VITE_SERVER_URL}/playlist/${this.id}`, 
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(response => {
            this.playlist_name = response.data.playlist.playlist_name;
            this.playlist_desc = response.data.playlist.playlist_desc;
        })
    }
}
</script>