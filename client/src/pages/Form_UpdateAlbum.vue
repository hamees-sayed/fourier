<template>
    <div class="container">
      <form @submit.prevent="updateAlbum">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Update Album</legend>
          <div class="form-group">
            <label class="form-control-label">Album Name</label>
            <input v-model="formData.album_name" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.album_name }">
            <div class="invalid-feedback" v-if="formErrors.album_name">
              <span>{{ formErrors.album_name }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Genre</label>
            <input v-model="formData.genre" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.genre }">
            <div class="invalid-feedback" v-if="formErrors.genre">
              <span>{{ formErrors.genre }}</span>
            </div>
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
  import { UPDATE_ALBUM_ACTION } from '../store/storeconstants';
  
  export default {
    data() {
      return {
        formData: {
          album_name: '',
          genre: ''
        },
        formErrors: {}
      };
    },
    methods: {
      ...mapActions('auth', {
        update_album: UPDATE_ALBUM_ACTION
      }),
      updateAlbum() {
        // Perform form validation
        this.formErrors = {};
  
        if (!this.formData.album_name.trim()) {
          this.formErrors.album_name = 'Album Name is required';
        }
  
        if (!this.formData.genre.trim()) {
          this.formErrors.genre = 'Genre is required';
        }
  
        if (Object.keys(this.formErrors).length === 0) {
          this.update_album({ title: this.formData.album_name, genre: this.formData.genre, album_id: parseInt(this.$route.params.id) })
            .then(() => this.$router.push('/creator/albums'));
        }
      }
    },
    mounted(){
        axios.get("https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/album/"+parseInt(this.$route.params.id), 
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(response => {
            this.formData.album_name = response.data.album.album_name;
            this.formData.genre = response.data.album.album_genre;
        })
    }
  };
  </script>
