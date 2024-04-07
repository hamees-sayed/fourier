<template>
    <div class="container">
      <form @submit.prevent="createAlbum">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Create a New Album</legend>
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
  import { mapActions } from 'vuex';
  import { CREATE_NEW_ALBUM_ACTION } from '../store/storeconstants';
  
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
        create_album: CREATE_NEW_ALBUM_ACTION
      }),
      createAlbum() {
        // Perform form validation
        this.formErrors = {};
  
        if (!this.formData.album_name.trim()) {
          this.formErrors.album_name = 'Album Name is required';
        }
  
        if (!this.formData.genre.trim()) {
          this.formErrors.genre = 'Genre is required';
        }
  
        if (Object.keys(this.formErrors).length === 0) {
          this.create_album({ title: this.formData.album_name, genre: this.formData.genre })
            .then(() => this.$router.push('/creator/albums'));
        }
      }
    }
  };
  </script>
