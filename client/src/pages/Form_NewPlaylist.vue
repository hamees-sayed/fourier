<template>
    <div class="container">
      <form @submit.prevent="createPlaylist" class="needs-validation" novalidate>
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Create a New Playlist</legend>
          <div class="form-group">
            <label for="playlist_name" class="form-control-label">Playlist Name</label>
            <input v-model="playlist_name" type="text" id="playlist_name" class="form-control form-control-lg" required>
          </div>
          <div class="form-group">
            <label for="playlist_desc" class="form-control-label">Playlist Description</label>
            <input v-model="playlist_desc" type="text" id="playlist_desc" class="form-control form-control-lg" required>
          </div>
        </fieldset>
        <br>
        <div class="form-group">
          <button type="submit" class="btn btn-outline-info">Create Playlist</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  import { CREATE_PLAYLIST_ACTION } from '../store/storeconstants';
  
  export default {
    data() {
      return {
        playlist_name: '',
        playlist_desc: ''
      };
    },
    methods: {
      ...mapActions('auth', {
        create_playlist: CREATE_PLAYLIST_ACTION
      }),
      createPlaylist() {
        if (!this.playlist_name) {
          this.usernameError = 'Username is required';
        } else {
          this.usernameError = '';
        }
  
        if (this.playlist_name) {
          this.create_playlist({ playlist_name: this.playlist_name, playlist_desc: this.playlist_desc })
            .then(() => {this.$router.push('/account');})
        }
      },
    },
  };
</script>