<template>
    <div class="container">
      <form @submit.prevent="createSong" enctype="multipart/form-data">
        <fieldset class="form-group">
          <legend class="border-bottom mb-2">Create a New Song</legend>
          <div class="form-group">
            <label class="form-control-label">Song Title</label>
            <input v-model="formData.song_title" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.song_title }">
            <div class="invalid-feedback" v-if="formErrors.song_title">
              <span>{{ formErrors.song_title }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Genre</label>
            <input v-model="formData.genre" type="text" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.genre }">
            <div class="invalid-feedback" v-if="formErrors.genre">
              <span>{{ formErrors.genre }}</span>
            </div>
          </div>
          <div class="form-group">
            <label for="formFile" class="form-label">Song File</label>
            <input @change="handleFileChange" type="file" class="form-control" id="formFile" required> 
            <div class="invalid-feedback" v-if="formErrors.song_file">
              <span>{{ formErrors.song_file }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Lyrics</label>
            <textarea v-model="formData.lyrics" class="form-control form-control-lg" :class="{ 'is-invalid': formErrors.lyrics }"></textarea>
            <div class="invalid-feedback" v-if="formErrors.lyrics">
              <span>{{ formErrors.lyrics }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label">Album</label>
            <select v-model="formData.album_id" class="form-control" :class="{ 'is-invalid': formErrors.album }">
              <option v-for="album in albums" :key="album.id" :value="album.id">{{ album.title }}</option>
            </select>
            <div class="invalid-feedback" v-if="formErrors.album">
              <span>{{ formErrors.album }}</span>
            </div>
          </div>
        </fieldset>
        <div class="form-group mt-3">
          <button type="submit" class="btn btn-outline-info">Submit</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapActions } from 'vuex';
  import { CREATE_NEW_SONG_ACTION } from '../store/storeconstants';
  
  export default {
    data() {
      return {
        formData: {
          song_title: '',
          genre: '',
          song_file: null,
          lyrics: '',
          album_id: 0
        },
        formErrors: {},
        albums: [],
      };
    },
    methods: {
      ...mapActions('auth', {
        createSongAction: CREATE_NEW_SONG_ACTION
      }),
      handleFileChange(event) {
        this.formData.song_file = event.target.files[0];
      },
      createSong() {  
        this.formErrors = {};
        // Validate form data
        if (!this.formData.song_title.trim()) {
          this.formErrors.song_title = 'Song Title is required';
        }
  
        if (!this.formData.genre.trim()) {
          this.formErrors.genre = 'Genre is required';
        }
  
        if (!this.formData.song_file) {
          this.formErrors.song_file = 'Song File is required';
        }
  
        // Submit form if no errors
        if (Object.keys(this.formErrors).length === 0) {
          const formdata = {
            title: this.formData.song_title,
            genre: this.formData.genre,
            lyrics: this.formData.lyrics,
            album_id: this.formData.album_id,
            song_file: this.formData.song_file
          }
  
          // Call action to create song
          this.createSongAction(formdata)
            .then(() => this.$router.push('/creator/songs'));
        }
      }
    },
    mounted(){
      axios.get('https://miniature-space-trout-gv5pxqq6457cvj4w-5000.app.github.dev/album', { 
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } 
      })
      .then(response => this.albums = [{id: 0, title: "Release as Single", genre: "None"}, ...response.data])
    }
  };
  </script>
  